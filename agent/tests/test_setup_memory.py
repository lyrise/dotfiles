import json
import os
import stat
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path

from agent import setup


class MemorySettingsTest(unittest.TestCase):
    def test_codex_config_preserves_other_settings_and_is_idempotent(self):
        original = 'model = "gpt-6-sol"\n\n[features]\nmemories = true # existing\ngoals = true\n\n[agents.verifier]\ndescription = "Keep me"\n'
        updated = setup.codex_config_without_memories(original)
        self.assertEqual(tomllib.loads(updated)["features"]["memories"], False)
        self.assertIn("goals = true", updated)
        self.assertIn('description = "Keep me"', updated)
        self.assertIn("memories = false # existing", updated)
        self.assertEqual(setup.codex_config_without_memories(updated), updated)

    def test_codex_config_adds_missing_features_table(self):
        updated = setup.codex_config_without_memories('model = "gpt-6-sol"')
        self.assertEqual(tomllib.loads(updated)["features"]["memories"], False)
        self.assertEqual(setup.codex_config_without_memories(updated), updated)

    def test_installed_settings_preserve_other_values_and_permissions(self):
        with tempfile.TemporaryDirectory() as root:
            codex = Path(root) / "codex.toml"
            claude = Path(root) / "claude.json"
            codex.write_text('[features]\nmemories = true\ngoals = true\n')
            claude.write_text('{"theme": "dark", "permissions": {"allow": ["Read"]}}\n')
            codex.chmod(0o600)
            claude.chmod(0o600)

            setup.disable_codex_memories(codex)
            setup.disable_claude_auto_memory(claude)
            first_codex = codex.read_bytes()
            first_claude = claude.read_bytes()
            setup.disable_codex_memories(codex)
            setup.disable_claude_auto_memory(claude)

            self.assertEqual(codex.read_bytes(), first_codex)
            self.assertEqual(claude.read_bytes(), first_claude)
            self.assertTrue(tomllib.loads(codex.read_text())["features"]["goals"])
            settings = json.loads(claude.read_text())
            self.assertEqual(settings["permissions"], {"allow": ["Read"]})
            self.assertIs(settings["autoMemoryEnabled"], False)
            self.assertEqual(stat.S_IMODE(codex.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(claude.stat().st_mode), 0o600)

    def test_invalid_config_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "config.toml"
            path.write_text("[features\n")
            with self.assertRaises(tomllib.TOMLDecodeError):
                setup.disable_codex_memories(path)
            self.assertEqual(path.read_text(), "[features\n")

    def test_install_twice_preserves_existing_settings(self):
        with tempfile.TemporaryDirectory() as root:
            home = Path(root)
            codex = home / ".codex"
            claude = home / ".claude"
            codex.mkdir()
            claude.mkdir()
            config_path = codex / "config.toml"
            settings_path = claude / "settings.json"
            config_path.write_text('[features]\nmemories = true\ngoals = true\n')
            settings_path.write_text('{"theme":"dark","permissions":{"allow":["Read"]}}\n')
            env = dict(
                os.environ,
                HOME=root,
                CODEX_HOME=str(codex),
                CONTINUE_GLOBAL_DIR=str(home / ".continue"),
            )

            first = subprocess.run(
                ["python3", str(setup.ROOT / "setup.py"), "install"],
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            first_config = config_path.read_bytes()
            first_settings = settings_path.read_bytes()
            second = subprocess.run(
                ["python3", str(setup.ROOT / "setup.py"), "install"],
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(config_path.read_bytes(), first_config)
            self.assertEqual(settings_path.read_bytes(), first_settings)

            features = tomllib.loads(config_path.read_text())["features"]
            settings = json.loads(settings_path.read_text())
            self.assertEqual(features, {"memories": False, "goals": True})
            self.assertIs(settings["autoMemoryEnabled"], False)
            self.assertEqual(settings["permissions"], {"allow": ["Read"]})
            self.assertTrue((codex / "skills/obsidian-knowledge/SKILL.md").exists())
            self.assertTrue((claude / "skills/obsidian-knowledge/SKILL.md").exists())
            self.assertTrue((home / ".continue/skills/obsidian-knowledge/SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
