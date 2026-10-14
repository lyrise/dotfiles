---
name: memory-todo
description: 環境変数 AGENT_MEMORY_DIR が指すディレクトリ直下の todo.md を、projects の index ノートと入手できる予定情報を材料に更新する。todo.md は再生成せず、既存の構成・方針・優先順位を尊重する。更新はユーザーの明示的な依頼のときだけ行う。
---

# TODO の更新

`AGENT_MEMORY_DIR` は Obsidian vault 内のディレクトリを指し、ノートはファイル操作で直接読み書きする。

## 材料

- `$AGENT_MEMORY_DIR/todo.md` — 更新対象。最初に読み、書かれている方針と優先順位を確認する。
- `$AGENT_MEMORY_DIR/projects/` の index ノート — 各プロジェクトの現状と次の一手。
- `knowledges/me/` の方針ノート — 優先順位の判断材料 (例: career-strategy)。
- カレンダーや予定の情報 — 入手できる手段があるときだけ読む。手段は未定。なければ、予定が必要な場面ではユーザーに尋ねるか、予定なしで更新する。

## 更新

- todo.md を再生成しない。既存の見出し構成・方針の記述・優先順位を保ち、項目の追加・完了・並べ替えを行う。
- 完了した項目は todo.md から削除する。経緯を残す価値があるときは、該当する project dir 内に残す。
- プロジェクトの項目は index ノートの `## 次の一手` から取り、`[[wikilink]]` で project dir へつなぐ。
- 方針の記述は書き換えない。方針自体の変更が必要なときは、変更案を示してユーザーの承認を得る。
- 更新後は、todo.md の変更点 (追加・削除・並べ替え) を回答で簡潔に示す。

## 制約

- 更新はユーザーが明示的に依頼したときだけ行う。
- 書き込みは todo.md だけ。`projects/` と `knowledges/` は読むだけで変更しない。
- `work/` は参照しない。
- `AGENT_MEMORY_DIR` が未設定のとき、または指すディレクトリが存在しないときは、更新できなかったことを伝えて中止する。パスを推測せず、ディレクトリを作らず、Codex・Claude・Serena の Memory へ切り替えない。
- Obsidian MCP は使わない。
