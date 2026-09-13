---
name: pull-request-workflow
description: Pull Request の構成、本文、レビューコメント、作成やready化を扱うときに使う。
---

# Pull Request のワークフロー

依頼に必要なreferenceだけを読む。複数の操作を行う場合だけ組み合わせる。

| 依頼 | 読む reference |
| --- | --- |
| レビュー指摘、行指定コメントを書く・投稿する | [GitHub のレビューコメント](references/github-review-comments.md) |
| PR の粒度、コミット順、依存関係を決める | [PR とコミットの構造](references/pull-request-structure.md) |
| PR 本文を書く・点検する | [PR 本文](references/pull-request-description.md) |
| PR を作成・監視・ready 化する | [PR とコミットの構造](references/pull-request-structure.md)、[PR 本文](references/pull-request-description.md)、[PR のライフサイクル](references/pull-request-lifecycle.md) |
| 性能、使用量などの数値を主張する | 上記に加えて[数値の主張](references/measured-claims.md) |

リポジトリの慣習、差分、測定結果を根拠にし、未確認のことは未確認として扱う。日本語の完成稿を作るときだけ `japanese-tech-writing` を読み、外部へ渡す完成稿を整えるときだけ `sanitize-artifacts` を読む。独立した `verifier` はユーザーが明示的に求めたときだけ使う。
