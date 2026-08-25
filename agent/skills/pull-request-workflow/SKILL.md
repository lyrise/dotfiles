---
name: pull-request-workflow
description: Pull Request の切り分け、依存順のコミット、本文、レビュー指摘、行指定コメント、依存 PR、根拠と数値、Draft、CI、ready 化を扱う規範。PR の構成を決めるとき、PR 本文やコミットメッセージを書くとき、コードレビューの指摘を書く・投稿するとき、PR を作成・点検・ready 化するときに使用する。
---

# Pull Request のワークフロー

依頼に必要な reference だけを読み、複数の作業を行う場合は該当する reference を組み合わせる。
文体、表記、情報密度は `../design-docs-writing/SKILL.md` に従う。

## Reference の選択

| 依頼 | 読む reference |
| --- | --- |
| レビュー指摘、行指定コメントを書く・投稿する | [GitHub のレビューコメント](references/github-review-comments.md) |
| PR の粒度、コミット順、依存関係を決める | [PR とコミットの構造](references/pull-request-structure.md) |
| PR 本文を書く・点検する | [PR 本文](references/pull-request-description.md) |
| PR を作成・監視・ready 化する | [PR とコミットの構造](references/pull-request-structure.md)、[PR 本文](references/pull-request-description.md)、[PR のライフサイクル](references/pull-request-lifecycle.md) |
| 性能、使用量などの数値を主張する | 上記に加えて [数値の主張](references/measured-claims.md) |

Draft 作成後の自己レビューで行指定コメントが必要になった場合は、[GitHub のレビューコメント](references/github-review-comments.md) も読む。

## 共通の確認

直近のコミットとマージ済み PR を読み、リポジトリの慣習に言語を合わせる。

```bash
git log --oneline -20
gh pr list --state merged --limit 10
```

判定できない場合はタイトルとコミットメッセージを英語、PR 本文と行指定コメントを日本語にする。
1 つの PR 本文の中で言語を混ぜない。
