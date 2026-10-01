---
name: git-change-workflow
description: コミット・push・PR・レビューを通じた変更の提出を扱う規範。コミットの構成やメッセージを決めるとき、変更をpushするとき、PRの構成・本文・ライフサイクルを扱うとき、レビュー指摘を書く・投稿するときに使用する。
---

# Git による変更の提出とレビュー

依頼に必要な reference だけを読み、複数の作業を行う場合は該当する reference を組み合わせる。
作業前に `../japanese-tech-writing/SKILL.md` と `../sanitize-artifacts/SKILL.md` を読む。

成果物固有の構造、根拠、制約、リポジトリの慣習を両スキルより優先する。
PR 本文、レビューコメント、タイトル、コミットメッセージの日本語部分は、`japanese-tech-writing` に従って初稿から組み立てる。
英語部分には `japanese-tech-writing` を適用しない。
完成前にすべての成果物を `sanitize-artifacts` でも点検し、意味を変えずに冗長さ、不自然な日本語、制作過程の残滓を除く。

## Reference の選択

| 依頼 | 読む reference |
| --- | --- |
| コミットの構成やメッセージを決める、PR を作らずにコミット・push する | [PR とコミットの構造](references/pull-request-structure.md) の「コミットを構成する」 |
| レビュー指摘、行指定コメントを書く・投稿する | [GitHub のレビューコメント](references/github-review-comments.md) |
| PR の粒度、コミット順、依存関係を決める | [PR とコミットの構造](references/pull-request-structure.md) |
| PR 本文を書く・点検する | [PR 本文](references/pull-request-description.md) |
| PR を作成・監視・ready 化する | [PR とコミットの構造](references/pull-request-structure.md)、[PR 本文](references/pull-request-description.md)、[PR のライフサイクル](references/pull-request-lifecycle.md) |
| 性能、使用量などの数値を主張する | 上記に加えて [数値の主張](references/measured-claims.md) |

Draft 作成後の自己レビューで行指定コメントが必要になった場合は、[GitHub のレビューコメント](references/github-review-comments.md) も読む。

## コミットと push

PR の作成は依頼に含まれる場合に行う。
コミット前に差分とステージ対象を確認し、依頼に必要な変更だけを含める。
push 前に送信先の remote・ブランチと送信するコミットを確認する。

## 文章の検証

成果物を完成稿として返す、コミットする、投稿する前に、同じ操作で扱う PR 本文、タイトル、コミットメッセージ、行指定コメントをまとめて named strict read-only `verifier` に独立検証させる。
途中案や選択肢は対象外とする。

`verifier` には、対象の完成稿、根拠となる差分と事実、リポジトリの慣習、該当する reference、数値を主張する場合は測定結果と再現手順を渡す。
成果物の構成、論理、根拠の配置、重複、事実と数値の整合、`sanitize-artifacts` を確認する。
日本語は `japanese-tech-writing`、英語はリポジトリの慣習と自然な技術英語に照らし、文体上の指摘も blocking とする。
判定は `pass` または `changes-required` とする。
`changes-required` では、成果物内の箇所、根拠、必要な修正を示す。

`changes-required` の場合は修正して再検証する。
修正と再検証は最大 2 回までとし、通らなければ未解決の指摘を報告し、成果物の確定、コミット、投稿を行わない。
`verifier` を利用できない場合も、成果物の確定、コミット、投稿を行わない。
`pass` の後、実際に使う成果物をメインエージェントが再確認する。

## 共通の確認

直近のコミットを読み、コミットメッセージの言語をリポジトリの慣習に合わせる。

```bash
git log --oneline -20
```

PR やレビューを扱う場合は、マージ済み PR も読む。

```bash
gh pr list --state merged --limit 10
```

判定できない場合はタイトルとコミットメッセージを英語、PR 本文と行指定コメントを日本語にする。
1 つの PR 本文の中で言語を混ぜない。
