---
name: xcode-cli
description: Xcode、Simulator、実機が必要なAppleプロジェクトのビルド、テスト、実行、診断で使う。
---

# Xcode CLI

Xcodeの起動状態に依存せず、リポジトリ設定をsource of truthとしてCLIで扱う。必要な節だけ[ワークフロー](references/workflows.md)から読む。

- project、workspace、scheme、destinationの特定は「最初に確認すること」
- Swift package、build、test、診断は「Swift package」「ビルドとテスト」「診断」
- Simulatorまたは実機の実行・画面確認は対応する節
- Swiftコード片の確認、XcodeGenまたはprojectへのファイル追加は「Swift コード片の確認」「ファイルの追加」

scheme、destination、Simulator名を推測せず、リポジトリまたはCLI出力で特定する。build、test、Simulator、実機の結果は別々の証拠として報告し、未実行の段階を成功としない。既存のSimulator、実機、インストール済みアプリは自動削除しない。
