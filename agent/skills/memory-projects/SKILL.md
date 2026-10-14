---
name: memory-projects
description: 環境変数 AGENT_MEMORY_DIR が指すディレクトリの projects を作業場として、プロジェクトごとの dir (YYYY-MM-DD-<slug>) に文書・スクリプト・生データを配置する。プロジェクト進行中の調査結果や経緯も dir 内に置く。完了・中断したプロジェクトは projects/archived/YYYY/MM/ へ移す。dir の作成はユーザーの明示的な依頼のときだけ行う。
---

# プロジェクトの運用

`AGENT_MEMORY_DIR` は Obsidian vault 内のディレクトリを指し、ノートはファイル操作で直接読み書きする。

## 構成

```
$AGENT_MEMORY_DIR/projects/
├── YYYY-MM-DD-<slug>/        # 進行中のプロジェクト。日付は作成日、slug は records/ と同じく日本語可
│   ├── YYYY-MM-DD-<slug>.md  # index ノート (必須)。ファイル名は dir 名と同じ
│   └── ...                   # 文書・スクリプト・生データなど。配置は自由
└── archived/
    └── YYYY/                 # 完了・中断したプロジェクト。YYYY は dir 名の日付の年
        └── MM/               # MM は dir 名の日付の月
            └── YYYY-MM-DD-<slug>/
```

- index ノートのファイル名を dir 名と同じにする。`[[wikilink]]` はファイル名で解決されるため、archived へ移動しても壊れない。

## index ノート

frontmatter:

```yaml
---
title: pxna で独立する # 必須。表示名
status: active # 必須。active / hold / done
created: 2026-10-13 # 必須。dir 名の日付と一致させる
updated: 2026-10-13 # 必須。本文を最後に変更した日
---
```

本文の章立ては `## 目的` `## 現状` `## 次の一手` `## 関連`。該当しない章は省く。`## 関連` には、関係する records・knowledges・todo.md への `[[wikilink]]` を置く。

## 参照

- 作業する前に、関係するプロジェクトの index ノートを読み、現状と次の一手を確認する。
- どのプロジェクトに属する作業か分からないときは、ユーザーに尋ねる。

## 作成・更新

- プロジェクト dir の作成はユーザーが明示的に依頼したときだけ行う。作成前に、同じ趣旨の dir がないか `projects/` と `projects/archived/` を確認する。
- プロジェクト進行中の調査結果・作業の経緯は project dir 内に置く。`records/` には置かない。`records/` はプロジェクト外の記録専用 (`memory-records` スキル)。
- 再利用できる知識・本人の方針は `memory-knowledges` スキルに従って `knowledges/` に置く。
- 完了・中断したプロジェクトは、パスと移動先を示してユーザーの承認を得てから `projects/archived/YYYY/MM/` へ移す。`YYYY/MM` には dir 名の日付を使う。
- リポジトリが肥大化するような生データ (音声・動画・大容量 CSV など) は、置く前にユーザーに確認する。
- 複数のプロジェクトで使い回せるスクリプトは、パスと理由を示してユーザーの承認を得てから vault 直下の `scripts/` へ移す。
- コードリポジトリを持つプロジェクトでは、リポジトリ側の文書が主。projects の dir は計画・進行メモ・vault 内リンクのハブとして使う。

## 制約

- `AGENT_MEMORY_DIR` が未設定のとき、または指すディレクトリが存在しないときは、作業できなかったことを伝えて中止する。パスを推測せず、ディレクトリを作らず、Codex・Claude・Serena の Memory へ切り替えない。
- 読み書きは `$AGENT_MEMORY_DIR/projects/` の中だけで行う。`.obsidian/` など vault の他の場所には触れない。
- Obsidian MCP は使わない。
