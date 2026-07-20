#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Manage agent skills and config files.

update  - fetch skills declared in skills.toml into ./skills, record commits in skills.lock.json
install - symlink ./skills and config files into the locations Claude Code and Codex read
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS_DIR = ROOT / "skills"
MANIFEST = ROOT / "skills.toml"
LOCK = ROOT / "skills.lock.json"

NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")
DEFAULT_REF = "main"


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def skill_dests() -> list[Path]:
    return [Path.home() / ".claude" / "skills", codex_home() / "skills"]


def config_links() -> list[tuple[Path, Path]]:
    return [
        (ROOT / "config" / "claude" / "CLAUDE.md", Path.home() / ".claude" / "CLAUDE.md"),
        (ROOT / "config" / "codex" / "AGENTS.md", codex_home() / "AGENTS.md"),
    ]


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True
    )
    return result.stdout


def skill_path(name: str) -> Path:
    """Resolve a skill directory, rejecting names that could escape SKILLS_DIR."""
    if not NAME_RE.match(name) or name in {".", ".."}:
        raise ValueError(f"invalid skill name: {name!r}")
    path = (SKILLS_DIR / name).resolve()
    if path.parent != SKILLS_DIR.resolve():
        raise ValueError(f"skill name escapes {SKILLS_DIR}: {name!r}")
    return path


# --- update ---------------------------------------------------------------


def read_manifest() -> dict[str, dict]:
    with MANIFEST.open("rb") as f:
        return tomllib.load(f).get("skills", {})


def read_lock() -> dict[str, dict]:
    if not LOCK.exists():
        return {}
    return json.loads(LOCK.read_text())


def write_lock(lock: dict[str, dict]) -> None:
    LOCK.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n")


def remote_commit(url: str, ref: str) -> str:
    out = git("ls-remote", url, ref).strip()
    if not out:
        raise RuntimeError(f"ref {ref!r} not found at {url}")
    return out.splitlines()[0].split("\t")[0]


def ignore_for(src: Path, exclude: list[str]) -> callable:
    """Ignore .git plus any path matching a glob, relative to the skill root.

    Excluding a directory drops its whole subtree, since copytree never
    descends into a name the callback returned.
    """

    def ignore(dirpath: str, names: list[str]) -> set[str]:
        rel = Path(dirpath).relative_to(src)
        ignored = {".git"}
        for name in names:
            candidate = (rel / name).as_posix()
            if any(fnmatch.fnmatch(candidate, pattern) for pattern in exclude):
                ignored.add(name)
        return ignored

    return ignore


def fetch(url: str, ref: str, subpath: str | None, exclude: list[str], dest: Path) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        clone = Path(tmp) / "repo"
        git("clone", "--depth", "1", "--branch", ref, "--quiet", url, str(clone))
        commit = git("-C", str(clone), "rev-parse", "HEAD").strip()

        src = clone / subpath if subpath else clone
        if not src.is_dir():
            raise RuntimeError(f"path {subpath!r} is not a directory in {url}")

        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest, ignore=ignore_for(src, exclude))
    return commit


def cmd_update(_args: argparse.Namespace) -> int:
    manifest = read_manifest()
    lock = read_lock()
    errors: list[str] = []

    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    for name in sorted(set(lock) - set(manifest)):
        try:
            path = skill_path(name)
        except ValueError as e:
            errors.append(f"{name}: {e}")
            continue
        if path.is_dir():
            shutil.rmtree(path)
        del lock[name]
        print(f"removed  {name}")

    for name in sorted(manifest):
        spec = manifest[name]
        try:
            path = skill_path(name)
            url = spec["url"]
            subpath = spec.get("path")
            ref = spec.get("ref", DEFAULT_REF)
            exclude = spec.get("exclude", [])

            commit = remote_commit(url, ref)
            entry = {
                "url": url,
                "path": subpath,
                "ref": ref,
                "exclude": exclude,
                "commit": commit,
            }
            if lock.get(name) == entry and path.is_dir():
                print(f"current  {name}  {commit[:8]}")
                continue

            fetch(url, ref, subpath, exclude, path)
            lock[name] = entry
            print(f"updated  {name}  {commit[:8]}")
        except (KeyError, ValueError, RuntimeError, subprocess.CalledProcessError) as e:
            detail = e.stderr.strip() if isinstance(e, subprocess.CalledProcessError) else e
            errors.append(f"{name}: {detail}")

    write_lock(lock)

    if errors:
        print("\nfailed:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1
    return 0


# --- install --------------------------------------------------------------


def link(src: Path, dst: Path, force: bool) -> bool:
    """Point dst at src. Returns False if an existing real file was left alone."""
    if dst.is_symlink():
        if Path(os.readlink(dst)) == src:
            return True
        dst.unlink()
    elif dst.exists():
        if not force:
            print(f"skipped  {dst}  (not a symlink; use --force to replace)", file=sys.stderr)
            return False
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()
        print(f"replaced {dst}")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)

    dst.symlink_to(src)
    return True


def prune(dest_root: Path) -> None:
    """Drop symlinks we own whose skill no longer exists."""
    skills = SKILLS_DIR.resolve()
    for entry in sorted(dest_root.iterdir()):
        if not entry.is_symlink():
            continue
        target = Path(os.readlink(entry))
        if not target.is_absolute():
            target = (dest_root / target).resolve()
        if target.parent != skills:
            continue
        if not (skills / entry.name).is_dir():
            entry.unlink()
            print(f"pruned   {entry}")


def cmd_install(args: argparse.Namespace) -> int:
    ok = True

    sources = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()) if SKILLS_DIR.is_dir() else []

    for dest_root in skill_dests():
        dest_root.mkdir(parents=True, exist_ok=True)
        prune(dest_root)
        for src in sources:
            ok &= link(src.resolve(), dest_root / src.name, args.force)

    for src, dst in config_links():
        ok &= link(src, dst, args.force)

    print(f"\n{len(sources)} skills -> {', '.join(str(d) for d in skill_dests())}")
    return 0 if ok else 1


# --- cli ------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("update", help="fetch skills declared in skills.toml").set_defaults(
        func=cmd_update
    )

    install = sub.add_parser("install", help="symlink skills and config files into place")
    install.add_argument(
        "--force", action="store_true", help="replace existing files that are not symlinks"
    )
    install.set_defaults(func=cmd_install)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
