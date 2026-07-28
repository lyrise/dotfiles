---
name: Global
alwaysApply: true
---

# Global

## Overview
- 日本語で簡潔かつ丁寧に回答してください

## Skills
- 利用可能な skill が作業内容に該当する場合は、着手前に `read_skill` でその内容を読み、記載された手順に従う
- skill は `~/.continue/skills`、`.continue/skills`、`.claude/skills` から読み込まれる

### playwright-cli (SKILL)
- Web UI や localhost のブラウザ検証、DOM 操作、console/network 確認が必要な場合に使用する
- 操作対象は snapshot の element ref で特定し、必要に応じて `eval`、`console`、`network` で状態を確認する
- screenshot はレイアウトや表示崩れの確認など、視覚的な証拠が必要な場合に限定して使用する

## Git

### コミット
- `Co-Authored-By:` トレーラーは付けない
