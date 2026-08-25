# PR のライフサイクル

## Draft を作成する

既定ブランチで作業せず、PR は Draft で作る。

```bash
gh pr create --draft --title '...' --body-file pr-body.md
```

Draft 作成後に差分を通して自己レビューする。
行指定コメントが必要な場合は `SKILL.md` から `github-review-comments.md` を読み、投稿前にユーザーの承認を得る。

## CI を監視する

push 直後は check が未登録の場合があるため、登録を待ってから監視する。

```bash
until ! gh pr checks <number> 2>&1 | grep -q 'no checks reported'; do sleep 10; done
gh pr checks <number> --watch --interval 30
```

foreground で待機できない環境では、同じ登録条件と終了条件を持つ監視機能へ置き換える。
失敗した場合は、ジョブの URL と失敗ログを確認して報告する。

## ready 化する

ready 化はユーザーの明示指示がある場合だけ行う。
ready 化の前に次を確認する。

1. `pull-request-description.md` の本文要件を満たしている
2. 数値の主張がある場合は `measured-claims.md` の測定と verifier の要件を満たしている
3. CI が成功している
4. 自己レビューを完了し、必要な行指定コメントを承認後に投稿している
5. 依存先がマージ済みなら base を既定ブランチへ戻している
6. スコープ外の問題を記録している

満たしていない項目があれば ready 化せず、残っている項目を報告する。
