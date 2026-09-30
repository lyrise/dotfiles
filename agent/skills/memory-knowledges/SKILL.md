---
name: memory-knowledges
description: 環境変数 AGENT_MEMORY_DIR が指すディレクトリの knowledges を外部記憶として、再利用できる知識・ユーザー本人や人物の情報・サービスや製品など固有名のある対象の知識を、仕事と私生活を問わず参照し、明示された依頼に応じて保存・更新・整理する。フォルダ構成と運用規則は knowledges/GUIDELINES.md に従い、必要に応じて承認を得て育てる。
---

# 知識の運用

`$AGENT_MEMORY_DIR/knowledges/` には、現在も有効な知識だけを置く。`AGENT_MEMORY_DIR` は Obsidian vault 内のディレクトリを指し、ノートはファイル操作で直接読み書きする。フォルダ構成、カテゴリごとの置き場所、ファイル名、frontmatter、更新・統合・削除の規則は `$AGENT_MEMORY_DIR/knowledges/GUIDELINES.md` に定める。`GUIDELINES.md` がまだない場合は、[examples/GUIDELINES.md](examples/GUIDELINES.md) を雛形として作成案をユーザーに示し、承認を得てから作成する。

## 参照

- `knowledges/` のノートを検索・参照する前に `GUIDELINES.md` を読み、カテゴリの定義に沿って必要なノートだけ開く。
- 話題に関係する知識が必要なときだけ参照する。個人文脈が不要なら、ユーザー本人や人物のカテゴリは開かない。
- ノートの内容が現在の事実と食い違う可能性があるときは、必要に応じて原典や現行コードで確認する。

## 保存・更新・整理

- 書き込みはユーザーが明示的に依頼したときだけ行う。
- 書き込む前に `GUIDELINES.md` を読み、その規則に従って置き場所と形式を決める。
- 既存のカテゴリに当てはまらない場合や、規則を変える必要がある場合は、`GUIDELINES.md` の変更案をユーザーに示し、承認を得てから `GUIDELINES.md` を更新し、その後にノートを書く。承認なしに `GUIDELINES.md` を変更しない。
- 調査結果や作業の経緯など、その時点の記録は `memory-records` スキルに従って `$AGENT_MEMORY_DIR/records/` に置く。

## 制約

- `AGENT_MEMORY_DIR` が未設定のとき、または指すディレクトリが存在しないときは、参照・保存できなかったことを伝えて中止する。パスを推測せず、ディレクトリを作らず、Codex・Claude・Serena の Memory へ切り替えない。
- 読み書きは `$AGENT_MEMORY_DIR/knowledges/` の中だけで行う。`.obsidian/` など vault の他の場所には触れない。
- Obsidian MCP は使わない。
