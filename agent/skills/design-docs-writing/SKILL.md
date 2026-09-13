---
name: design-docs-writing
description: プロジェクトの設計、用語、不具合、外部知識、計画、レビュー文書を書く、更新する、点検するときに使う。
---

# プロジェクト文書

依頼の文書型に対応する reference だけを読む。複数型を扱う場合だけ組み合わせる。

- 文書族の責務、親と子、識別子、文体、図、情報密度、根拠の扱い、リンク規約、検証は[共通規範](references/conventions.md)
- 設計文書は[設計文書](references/design-document.md)
- 用語文書は[用語文書](references/terms-document.md)
- 不具合一覧は[不具合一覧](references/issues-document.md)
- 外部知識は[外部知識](references/knowledges-document.md)
- 実装計画書は[実装計画書](references/implementation-plan.md)
- レビュー結果は[レビュー結果文書](references/review-document.md)

点検は読み取り専用で候補だけを報告する。

日本語部分は `japanese-tech-writing` に従って初稿から組み立て、完成前に `sanitize-artifacts` で制作過程の残滓を点検する。成果物固有の構造、根拠、制約、リポジトリ規約はこれらの skill より優先する。
