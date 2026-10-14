"""Local skill installation tests; all install destinations are isolated."""

from __future__ import annotations

import argparse
import importlib.util
import io
import os
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

SETUP_PATH = Path(__file__).with_name("setup.py")
spec = importlib.util.spec_from_file_location("agent_setup", SETUP_PATH)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class SkillInstallTests(unittest.TestCase):
    def setUp(self):
        value = os.environ.get("AGENT_TEMP_DIR")
        if not value:
            print("AGENT_TEMP_DIR is unset; using /tmp for tests")
        parent = Path(value or "/tmp").expanduser()
        parent.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="test-agent-skills-", dir=parent)
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.root = self.base / "agent"
        self.skills = self.root / "skills"
        self.home = self.base / "home"
        self.codex = self.home / "custom-codex"
        self.continue_home = self.home / "custom-continue"
        self.continue_dest = self.continue_home / "skills"
        self.generated = self.root / ".generated" / "continue-skills"
        self.local = self.root / "skills.local.toml"
        self.staging = self.base / "staging"
        self.staging.mkdir()
        for name in ("alpha", "beta"):
            self.write(self.skills / name / "SKILL.md", f"# {name}\n")
        for client, filename in (
            ("claude", "CLAUDE.md"), ("codex", "AGENTS.md"), ("opencode", "AGENTS.md")
        ):
            self.write(self.root / "config" / client / filename, f"{client} instructions\n")
        self.enterContext(mock.patch.multiple(
            setup,
            ROOT=self.root,
            SKILLS_DIR=self.skills,
            MANIFEST=self.root / "skills.toml",
            LOCK=self.root / "skills.lock.json",
            LOCAL_SKILLS=self.local,
            CONTINUE_SKILLS_DIR=self.generated,
        ))
        self.enterContext(mock.patch.dict(os.environ, {
            "HOME": str(self.home),
            "CODEX_HOME": str(self.codex),
            "CONTINUE_GLOBAL_DIR": str(self.continue_home),
            "AGENT_MEMORY_DIR": "",
            "AGENT_TEMP_DIR": str(self.staging),
        }))

    def write(self, path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def exclude(self, *names: str):
        self.write(self.local, "[skills]\nexclude = " + repr(list(names)) + "\n")

    def install(self, force=False):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = setup.cmd_install(argparse.Namespace(force=force))
        self.stdout, self.stderr = stdout.getvalue(), stderr.getvalue()
        return result

    def snapshot(self, root=None):
        root = root or self.base
        result = {}
        for path in sorted(root.rglob("*")):
            name = str(path.relative_to(root))
            if path.is_symlink():
                result[name] = ("link", os.readlink(path))
            elif path.is_file():
                result[name] = ("file", path.read_bytes())
            else:
                result[name] = ("directory",)
        return result

    def test_defaults_and_omitted_items(self):
        for content in (None, "", "[skills]\n", "[skills]\nexclude = []\n"):
            with self.subTest(content=content):
                if content is None:
                    self.local.unlink(missing_ok=True)
                else:
                    self.write(self.local, content)
                self.assertEqual(self.install(), 0, self.stderr)
                for dest in setup.skill_dests():
                    for name in ("alpha", "beta"):
                        self.assertEqual((dest / name).resolve(), self.skills / name)
                self.assertEqual(self.continue_dest.resolve(), self.skills)
                self.assertFalse(self.generated.exists())
                self.assertIn("2 skills (0 excluded)", self.stdout)

    def test_exclude_existing_links_and_restore(self):
        self.assertEqual(self.install(), 0, self.stderr)
        self.exclude("alpha", "alpha")
        self.assertEqual(self.install(), 0, self.stderr)
        for dest in setup.skill_dests():
            self.assertFalse((dest / "alpha").is_symlink())
            self.assertEqual((dest / "beta").resolve(), self.skills / "beta")
        generation = self.continue_dest.resolve()
        self.assertEqual(generation.parent, self.generated)
        self.assertEqual([p.name for p in generation.iterdir()], ["beta"])
        self.assertFalse((generation / "beta").is_symlink())
        self.assertFalse((generation / "beta" / "SKILL.md").is_symlink())
        self.assertIn("1 skills (1 excluded)", self.stdout)
        self.exclude()
        self.assertEqual(self.install(), 0, self.stderr)
        self.assertEqual(self.continue_dest.resolve(), self.skills)
        self.assertFalse(generation.exists())
        for dest in setup.skill_dests():
            self.assertEqual((dest / "alpha").resolve(), self.skills / "alpha")

    def test_all_excluded(self):
        self.assertEqual(self.install(), 0, self.stderr)
        self.exclude("alpha", "beta")
        self.assertEqual(self.install(), 0, self.stderr)
        self.assertEqual(list(self.continue_dest.iterdir()), [])
        for dest in setup.skill_dests():
            self.assertEqual(list(dest.iterdir()), [])
        self.assertIn("0 skills (2 excluded)", self.stdout)

    def test_relative_and_absolute_managed_links(self):
        for index, dest in enumerate(setup.skill_dests()):
            dest.mkdir(parents=True)
            source = self.skills / "alpha"
            target = os.path.relpath(source, dest) if index else str(source)
            (dest / "alpha").symlink_to(target)
        self.exclude("alpha")
        self.assertEqual(self.install(), 0, self.stderr)
        for dest in setup.skill_dests():
            self.assertFalse((dest / "alpha").is_symlink())

    def test_excluded_unmanaged_entries_are_preserved_even_with_force(self):
        outside = self.base / "outside"
        self.write(outside / "SKILL.md", "local content")
        claude, codex = setup.skill_dests()
        claude.mkdir(parents=True)
        (claude / "alpha").symlink_to(outside)
        self.write(codex / "alpha" / "SKILL.md", "custom content")
        self.exclude("alpha")
        self.assertEqual(self.install(force=True), 0, self.stderr)
        self.assertEqual((claude / "alpha").resolve(), outside)
        self.assertEqual((codex / "alpha" / "SKILL.md").read_text(), "custom content")

    def test_wrong_named_source_link_is_not_removed(self):
        claude = setup.skill_dests()[0]
        claude.mkdir(parents=True)
        (claude / "alpha").symlink_to(self.skills / "beta")
        self.exclude("alpha")
        self.assertEqual(self.install(), 0, self.stderr)
        self.assertEqual((claude / "alpha").resolve(), self.skills / "beta")

    def test_deleted_sources_are_still_pruned(self):
        self.assertEqual(self.install(), 0, self.stderr)
        shutil.rmtree(self.skills / "beta")
        self.assertEqual(self.install(), 0, self.stderr)
        for dest in setup.skill_dests():
            self.assertFalse((dest / "beta").is_symlink())

    def test_invalid_settings_fail_before_any_changes(self):
        self.exclude("alpha")
        self.assertEqual(self.install(), 0, self.stderr)
        cases = (
            "[skills", 'other = []\n', 'skills = "alpha"\n',
            '[skills]\nexcludes = ["alpha"]\n', '[skills]\nexclude = "alpha"\n',
            '[skills]\nexclude = true\n', '[skills]\nexclude = [1]\n',
            '[skills]\nexclude = ["../alpha"]\n', '[skills]\nexclude = [".."]\n',
            '[skills]\nexclude = ["."]\n', '[skills]\nexclude = ["alp*"]\n',
            '[skills]\nexclude = ["missing"]\n',
        )
        for content in cases:
            with self.subTest(content=content):
                self.write(self.local, content)
                before = self.snapshot()
                self.assertEqual(self.install(force=True), 1)
                self.assertIn("failed:", self.stderr)
                self.assertEqual(self.snapshot(), before)

    def test_exclusion_cannot_escape_source_root(self):
        outside = self.base / "external-skill"
        self.write(outside / "SKILL.md", "outside")
        (self.skills / "external").symlink_to(outside)
        self.exclude("external")
        before = self.snapshot()
        self.assertEqual(self.install(), 1)
        self.assertIn("escapes", self.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_continue_refreshes_content_and_removes_old_generation(self):
        self.write(self.skills / "beta" / "docs" / "old.md", "old")
        self.exclude("alpha")
        self.assertEqual(self.install(), 0, self.stderr)
        previous = self.continue_dest.resolve()
        self.write(self.skills / "beta" / "SKILL.md", "new beta content")
        (self.skills / "beta" / "docs" / "old.md").unlink()
        self.write(self.skills / "beta" / "docs" / "new.md", "new")
        self.assertEqual(self.install(), 0, self.stderr)
        current = self.continue_dest.resolve()
        self.assertNotEqual(previous, current)
        self.assertFalse(previous.exists())
        self.assertEqual((current / "beta" / "SKILL.md").read_text(), "new beta content")
        self.assertFalse((current / "beta" / "docs" / "old.md").exists())
        contents = self.snapshot(current)
        self.assertEqual(self.install(), 0, self.stderr)
        self.assertEqual(self.snapshot(self.continue_dest.resolve()), contents)
        self.assertEqual(list(self.generated.iterdir()), [self.continue_dest.resolve()])
        self.assertEqual(list(self.staging.iterdir()), [])

    def test_continue_copies_source_symlinks_as_real_files_and_directories(self):
        self.write(self.skills / "beta" / "docs" / "reference.md", "reference")
        (self.skills / "beta" / "reference").symlink_to("docs")
        (self.skills / "beta" / "linked.md").symlink_to("docs/reference.md")
        self.exclude("alpha")
        self.assertEqual(self.install(), 0, self.stderr)
        root = self.continue_dest.resolve() / "beta"
        self.assertFalse((root / "reference").is_symlink())
        self.assertFalse((root / "linked.md").is_symlink())
        self.assertEqual((root / "reference" / "reference.md").read_text(), "reference")
        self.assertEqual((root / "linked.md").read_text(), "reference")

    def test_continue_directory_collision_and_force(self):
        self.write(self.continue_dest / "custom" / "SKILL.md", "custom")
        self.exclude("alpha")
        before = self.snapshot(self.continue_dest)
        self.assertEqual(self.install(), 1)
        self.assertEqual(self.snapshot(self.continue_dest), before)
        self.assertFalse(self.generated.exists())
        self.assertEqual(self.install(force=True), 0, self.stderr)
        self.assertTrue(self.continue_dest.is_symlink())
        self.assertEqual([p.name for p in self.continue_dest.iterdir()], ["beta"])

    def test_continue_external_link_collision_and_force(self):
        outside = self.base / "outside"
        self.write(outside / "custom" / "SKILL.md", "custom")
        self.continue_home.mkdir(parents=True)
        self.continue_dest.symlink_to(outside)
        self.exclude("alpha")
        before = self.snapshot(outside)
        self.assertEqual(self.install(), 1)
        self.assertEqual(self.continue_dest.resolve(), outside)
        self.assertEqual(self.install(force=True), 0, self.stderr)
        self.assertEqual(self.snapshot(outside), before)
        self.assertEqual(self.continue_dest.resolve().parent, self.generated)

    def test_copy_failures_preserve_active_generation_and_clean_candidates(self):
        self.exclude("alpha")
        self.assertEqual(self.install(), 0, self.stderr)
        original_copytree = shutil.copytree
        for phase in ("staging", "publishing"):
            with self.subTest(phase=phase):
                before = self.snapshot()

                def fail_copy(src, dst, *args, **kwargs):
                    dst = Path(dst)
                    publishing = dst.parent == self.generated
                    staging = dst.name == "beta" and dst.parent.name == "skills"
                    if (phase == "publishing" and publishing) or (phase == "staging" and staging):
                        self.write(dst / "incomplete", "incomplete")
                        raise OSError("injected copy failure")
                    return original_copytree(src, dst, *args, **kwargs)

                with mock.patch.object(setup.shutil, "copytree", side_effect=fail_copy):
                    self.assertEqual(self.install(), 1)
                self.assertIn("injected copy failure", self.stderr)
                self.assertEqual(self.snapshot(), before)

    def test_initial_copy_failure_preserves_original_continue_link(self):
        self.assertEqual(self.install(), 0, self.stderr)
        self.exclude("alpha")
        with mock.patch.object(setup.shutil, "copytree", side_effect=OSError("copy failed")):
            self.assertEqual(self.install(), 1)
        self.assertEqual(self.continue_dest.resolve(), self.skills)
        self.assertFalse(self.generated.exists())
        self.assertEqual(list(self.staging.iterdir()), [])

    def test_symlinked_generation_parents_are_rejected(self):
        outside = self.base / "outside"
        self.write(outside / "sentinel", "unchanged")
        self.assertEqual(self.install(), 0, self.stderr)
        self.exclude("alpha")
        for path in (self.generated.parent, self.generated):
            with self.subTest(path=path):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(outside)
                before = self.snapshot(outside)
                self.assertEqual(self.install(force=True), 1)
                self.assertIn("must not use a symlink", self.stderr)
                self.assertEqual(self.snapshot(outside), before)
                self.assertEqual(self.continue_dest.resolve(), self.skills)
                path.unlink()

    def test_symlinked_generation_is_rejected(self):
        outside = self.base / "outside"
        self.write(outside / "sentinel", "unchanged")
        self.generated.mkdir(parents=True)
        generation = self.generated / ("a" * 32)
        generation.symlink_to(outside)
        self.continue_home.mkdir(parents=True)
        self.continue_dest.symlink_to(generation)
        self.exclude("alpha")
        before = self.snapshot(outside)
        self.assertEqual(self.install(force=True), 1)
        self.assertEqual(os.readlink(self.continue_dest), str(generation))
        self.assertEqual(self.snapshot(outside), before)

    def test_staging_directory_default_and_creation(self):
        stderr = io.StringIO()
        with mock.patch.dict(os.environ, {"AGENT_TEMP_DIR": ""}), \
                mock.patch.object(Path, "mkdir") as mkdir, redirect_stderr(stderr):
            self.assertEqual(setup.skill_staging_dir(), Path("/tmp"))
            mkdir.assert_called_once_with(parents=True, exist_ok=True)
        self.assertIn("unset; using /tmp", stderr.getvalue())
        new_path = self.base / "new" / "temporary"
        with mock.patch.dict(os.environ, {"AGENT_TEMP_DIR": str(new_path)}):
            self.assertEqual(setup.skill_staging_dir(), new_path)
        self.assertTrue(new_path.is_dir())

    def test_unusable_staging_directory_preserves_continue(self):
        self.exclude("alpha")
        self.assertEqual(self.install(), 0, self.stderr)
        blocked = self.base / "not-a-directory"
        self.write(blocked, "file")
        previous = self.continue_dest.resolve()
        contents = self.snapshot(previous)
        with mock.patch.dict(os.environ, {"AGENT_TEMP_DIR": str(blocked)}):
            self.assertEqual(self.install(), 1)
        self.assertEqual(self.continue_dest.resolve(), previous)
        self.assertEqual(self.snapshot(previous), contents)
        self.assertEqual(list(self.generated.iterdir()), [previous])

    def test_exclusion_preserves_other_install_artifacts(self):
        self.write(self.root / "config" / "claude" / "agents" / "reviewer.md", "claude agent")
        self.write(self.root / "config" / "codex" / "agents" / "reviewer.toml", 'name = "reviewer"\n')
        self.write(self.root / "config" / "opencode" / "agents" / "reviewer.md", "opencode agent")
        self.write(self.root / "config" / "continue" / "rules" / "global.md", "global rule")
        self.exclude("alpha")
        self.assertEqual(self.install(), 0, self.stderr)
        self.assertTrue((self.home / ".claude" / "agents" / "reviewer.md").is_symlink())
        self.assertFalse((self.codex / "agents" / "reviewer.toml").is_symlink())
        self.assertEqual((self.codex / "agents" / "reviewer.toml").read_text(), 'name = "reviewer"\n')
        self.assertTrue((self.home / ".config" / "opencode" / "agents" / "reviewer.md").is_symlink())
        self.assertTrue((self.continue_home / "rules" / "global.md").is_symlink())
        for _, dest in setup.config_links():
            self.assertTrue(dest.is_symlink())

    def test_update_ignores_local_settings(self):
        self.write(setup.MANIFEST, '[skills]\nalpha = { url = "mock-alpha" }\nbeta = { url = "mock-beta" }\n')
        for content in ('[skills]\nexclude = ["alpha"]\n', "invalid [toml"):
            with self.subTest(content=content):
                self.write(self.local, content)
                setup.LOCK.unlink(missing_ok=True)
                with mock.patch.object(setup, "read_skill_exclusions", side_effect=AssertionError("read local settings")), \
                        mock.patch.object(setup, "remote_commit", return_value="abc123") as remote, \
                        mock.patch.object(setup, "fetch", return_value="abc123") as fetch, \
                        redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    self.assertEqual(setup.cmd_update(argparse.Namespace()), 0)
                self.assertEqual(remote.call_count, 2)
                self.assertEqual(fetch.call_count, 2)
                self.assertEqual({call.args[0] for call in fetch.call_args_list}, {"mock-alpha", "mock-beta"})

    def test_gitignore_rules(self):
        paths = ["agent/skills.local.toml", "agent/.generated/continue-skills/example/SKILL.md", "agent/skills.local.example.toml"]
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--stdin"],
            input="\n".join(paths) + "\n", text=True, capture_output=True,
            cwd=SETUP_PATH.parent.parent, check=True,
        )
        self.assertEqual(result.stdout.splitlines(), paths[:2])


if __name__ == "__main__":
    unittest.main()
