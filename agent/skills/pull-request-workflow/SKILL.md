---
name: pull-request-workflow
description: Pull Request の切り分け、依存順のコミット、本文、レビュー指摘、行指定コメント、依存 PR、根拠と数値、Draft、CI、ready 化を扱う規範。PR の構成を決めるとき、PR 本文やコミットメッセージを書くとき、コードレビューの指摘を書く・投稿するとき、PR を作成・点検・ready 化するときに使用する。
---

# Pull Request のワークフロー

依頼に必要な reference だけを読み、複数の作業を行う場合は該当する reference を組み合わせる。
作業前に `../japanese-tech-writing/SKILL.md` と `../sanitize-artifacts/SKILL.md` を読む。

成果物固有の構造、根拠、制約、リポジトリの慣習を両スキルより優先する。
PR 本文、レビューコメント、タイトル、コミットメッセージの日本語部分は、`japanese-tech-writing` に従って初稿から組み立てる。
英語部分には `japanese-tech-writing` を適用しない。
完成前にすべての成果物を `sanitize-artifacts` でも点検し、意味を変えずに冗長さ、不自然な日本語、制作過程の残滓を除く。

## Reference の選択

| 依頼 | 読む reference |
| --- | --- |
| レビュー指摘、行指定コメントを書く・投稿する | [GitHub のレビューコメント](references/github-review-comments.md) |
| PR の粒度、コミット順、依存関係を決める | [PR とコミットの構造](references/pull-request-structure.md) |
| PR 本文を書く・点検する | [PR 本文](references/pull-request-description.md) |
| PR を作成・監視・ready 化する | [PR とコミットの構造](references/pull-request-structure.md)、[PR 本文](references/pull-request-description.md)、[PR のライフサイクル](references/pull-request-lifecycle.md) |
| 性能、使用量などの数値を主張する | 上記に加えて [数値の主張](references/measured-claims.md) |

Draft 作成後の自己レビューで行指定コメントが必要になった場合は、[GitHub のレビューコメント](references/github-review-comments.md) も読む。

## 文章の検証

成果物を返す、コミットする、投稿する前に、同じ操作で扱う成果物をまとめて named strict read-only `verifier` に独立検証させる。
対象の成果物、根拠となる差分と事実、リポジトリの慣習、該当する reference、`japanese-tech-writing`、`sanitize-artifacts` を渡す。
判定は `pass` または `changes-required` とし、両スキルに基づく文体上の指摘も blocking とする。

`changes-required` の場合は修正して再検証する。
修正と再検証は最大 2 回までとし、通らなければ未解決の指摘を報告し、成果物の確定、コミット、投稿を行わない。
`verifier` を利用できない場合に限り、同じ基準で自己点検し、独立検証を省略したことを明示して続行する。
`pass` または自己点検の後、実際に使う成果物をメインエージェントが再確認する。

## 共通の確認

直近のコミットとマージ済み PR を読み、リポジトリの慣習に言語を合わせる。

```bash
git log --oneline -20
gh pr list --state merged --limit 10
```

判定できない場合はタイトルとコミットメッセージを英語、PR 本文と行指定コメントを日本語にする。
1 つの PR 本文の中で言語を混ぜない。
