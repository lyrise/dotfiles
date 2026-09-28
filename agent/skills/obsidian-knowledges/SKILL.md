---
name: obsidian-knowledges
description: Obsidian vault の share/knowledges を外部記憶として、再利用できる知識・ユーザー本人や人物の情報・サービスやシステムの運用知識を参照し、明示された依頼に応じて保存・更新・整理する。フォルダ構成と運用規則は share/knowledges/GUIDELINES.md に従い、必要に応じて承認を得て育てる。
---

# Obsidian の知識運用

`share/knowledges/` には、現在も有効な知識だけを置く。フォルダ構成、カテゴリごとの置き場所、ファイル名、frontmatter、更新・統合・削除の規則は `share/knowledges/GUIDELINES.md` に定める。

## 参照

- `share/knowledges/` のノートを検索・参照する前に、`share/knowledges/GUIDELINES.md` を Obsidian MCP で読み、カテゴリの定義に沿って必要なノートだけ開く。
- 話題に関係する知識が必要なときだけ参照する。個人文脈が不要なら、ユーザー本人や人物のカテゴリは開かない。
- ノートの内容が現在の事実と食い違う可能性があるときは、必要に応じて原典や現行コードで確認する。

## 保存・更新・整理

- 書き込みはユーザーが明示的に依頼したときだけ行う。
- 書き込む前に `share/knowledges/GUIDELINES.md` を読み、その規則に従って置き場所と形式を決める。
- 既存のカテゴリに当てはまらない場合や、規則を変える必要がある場合は、`GUIDELINES.md` の変更案をユーザーに示し、承認を得てから `GUIDELINES.md` を更新し、その後にノートを書く。承認なしに `GUIDELINES.md` を変更しない。
- 調査結果や作業の経緯など、その時点の記録は `obsidian-records` スキルに従って `share/records/` に置く。
- 特定リポジトリに固有の知識は vault に置かず、そのリポジトリ内の文書に置く。

## 制約

- Obsidian MCP が使えない場合は参照・保存できなかったことを伝える。Codex・Claude・Serena の Memory や vault の直接ファイル操作へ切り替えない。
