---
name: obsidian-records
description: Obsidian vault の share/records を外部記憶として、過去の調査結果・作業の経緯・判断とその理由など時点の記録を参照し、明示された依頼に応じて保存する。旧記録の退避はユーザーが手動で行う。
---

# Obsidian の記録運用

## 構成

```
share/records/                # 不変。書いたら変えない時点の記録
├── YYYY-MM-DD-<topic>.md
└── archived/                 # 同じトピックの新しい記録に置き換えられた旧記録
    └── YYYY/
        └── MM/
            └── YYYY-MM-DD-<topic>.md
```

- `records/` には調査結果、作業の経緯、判断とその理由など、その時点の事実を置く。種別は frontmatter の `tags` で表し、`date` を持たせる。
- 現在も有効な知識は `obsidian-knowledges` スキルに従って `share/knowledges/` に置く。
- 特定リポジトリに固有の記録は vault に置かず、そのリポジトリ内の文書に置く。

## 参照

- 話題に関係する過去の記録が必要なときだけ Obsidian MCP で `share/records/` を検索し、必要なノートだけ読む。
- `records/` は記録時点の内容として扱い、現在の事実は必要に応じて原典や現行コードで確認する。
- `records/archived/YYYY/MM/` は、経緯や過去との比較が必要なときだけ開く。

## 保存

- 書き込みはユーザーが明示的に依頼したときだけ行う。
- `records/` のノートは作成後に書き換えない。訂正や続報は新しい日付のノートとして書く。
- `records/` に保存する前に同じトピックの既存記録を検索する。
- ニュースの定期レポートのように同じトピックを新しい記録で置き換える場合も、旧記録の移動・複製・削除はしない。退避はユーザーが手動で行う。新しい記録を保存して内容を確認したら、退避すべき旧記録のパスと退避先 `records/archived/YYYY/MM/` を回答に示す。`YYYY/MM` には旧記録のファイル名の日付を使う。

## 制約

- Obsidian MCP が使えない場合は参照・保存できなかったことを伝える。Codex・Claude・Serena の Memory や vault の直接ファイル操作へ切り替えない。
