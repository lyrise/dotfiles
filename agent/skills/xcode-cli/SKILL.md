---
name: xcode-cli
description: iOS/macOS 開発を Xcode の起動やプロジェクトの事前オープンに依存せず、xcodebuild、swift、simctl、devicectl、xcresulttool で進めるための規範。プロジェクト・scheme・destination の検出、ビルド、テスト、診断、Simulator/実機での実行、スクリーンショット、XcodeGen と .xcodeproj へのファイル追加を扱う。Swift/SwiftUI のビルド、テスト、エラー調査、画面確認、シミュレータ実行を頼まれたとき、または .xcodeproj/.xcworkspace/Package.swift/project.yml を含むプロジェクトで作業するときに使用する。
---

# Xcode CLI を用いた Apple プラットフォーム開発

Xcode アプリの起動状態や、そこで選択されている scheme に依存しない。
リポジトリの設定を source of truth とし、`xcodebuild`、`swift`、`xcrun simctl`、
`xcrun devicectl`、`xcrun xcresulttool` を使う。

ビルド成功、テスト成功、Simulator での動作、実機での動作は別々の証拠として扱う。
実行していない段階を成功したように報告しない。

## 最初に確認すること

作業開始時に、選択中の toolchain と必要な CLI を確認する。

```bash
xcode-select -p
xcodebuild -version
xcrun --find simctl
xcrun --find xcresulttool
```

複数の Xcode がある場合は、必要なコマンドだけに `DEVELOPER_DIR` を指定する。
システム全体の `xcode-select --switch` は、明示的な依頼がない限り行わない。

リポジトリ内の `Package.swift`、ルートレベルの `.xcworkspace`、`.xcodeproj`、
`project.yml` を調べる。`.xcodeproj/project.xcworkspace` は独立した workspace として
数えない。

選択規則は次のとおりとする。

- Apple アプリの workspace があれば `.xcworkspace` を使う
- workspace がなければ `.xcodeproj` を使う
- Swift package 単体の作業なら `Package.swift` と `swift` を使う
- 候補が複数あり、対象をリポジトリから特定できなければユーザーに確認する

scheme と destination を推測しない。先に列挙する。

```bash
xcodebuild -list -json -workspace App.xcworkspace
xcodebuild -workspace App.xcworkspace -scheme App -showdestinations
```

`.xcodeproj` を使う場合は、`-workspace App.xcworkspace` を
`-project App.xcodeproj` に置き換える。
ビルドだけで実行環境を必要としない場合は
`-destination 'generic/platform=iOS Simulator'` のような generic destination を使う。
テストや起動では `-showdestinations` または `simctl list` で得た利用可能な ID を使う。

## Swift package

Swift package 単体で足りる場合は Xcode project を経由しない。

```bash
swift build
swift test
swift test list
swift test --filter 'TargetName.TestType/testName'
```

`Package.resolved` を固定する必要がある作業では、存在と更新意図を確認してから
`--only-use-versions-from-resolved-file` を使う。依存更新やネットワークアクセスを
暗黙に混ぜない。

## ビルドとテスト

workspace または project、scheme、configuration、destination をコマンドに明示する。

```bash
xcodebuild \
  -workspace App.xcworkspace \
  -scheme App \
  -configuration Debug \
  -destination 'generic/platform=iOS Simulator' \
  build
```

テストでは結果 bundle とログを一時ディレクトリへ保存する。固定パスを使い回さず、
先に `mktemp -d /tmp/xcode-cli.XXXXXX` でディレクトリを作る。

```bash
xcodebuild \
  -workspace App.xcworkspace \
  -scheme App \
  -destination 'platform=iOS Simulator,id=SIMULATOR_ID' \
  -resultBundlePath "$task_tmp_dir/Test.xcresult" \
  test >"$task_tmp_dir/xcodebuild.log" 2>&1
```

全テストを繰り返すと高コストな場合は、テストを列挙して対象だけ実行する。

```bash
xcodebuild \
  -workspace App.xcworkspace \
  -scheme App \
  -destination 'platform=iOS Simulator,id=SIMULATOR_ID' \
  test -enumerate-tests \
  -test-enumeration-format json \
  -test-enumeration-output-path -

xcodebuild \
  -workspace App.xcworkspace \
  -scheme App \
  -destination 'platform=iOS Simulator,id=SIMULATOR_ID' \
  -only-testing:AppTests/TestType/testName \
  test
```

ビルドとテストを分ける場合は `build-for-testing` の後に `test-without-building` を使う。
両方で同じ container、scheme、destination、configuration、`-derivedDataPath` を使う。

`Package.resolved` が正で依存更新を認めない場合だけ、
`-onlyUsePackageVersionsFromResolvedFile` を付ける。`-skipMacroValidation`、
`-skipPackagePluginValidation`、署名検証を弱める option は既定で付けない。

## 診断

最初にコマンドの exit status と、`** BUILD SUCCEEDED **` / `** TEST SUCCEEDED **` などの
本体結果を確認する。`DVTFilePathFSEvents` や cache 関連の警告だけで失敗と断定しない。

結果 bundle がある場合は構造化された結果を優先する。

```bash
xcrun xcresulttool get build-results \
  --path "$task_tmp_dir/Build.xcresult"

xcrun xcresulttool get test-results summary \
  --path "$task_tmp_dir/Test.xcresult"
```

補助的にログを絞る。

```bash
rg -n 'error:|warning:|failed|FAIL' "$task_tmp_dir/xcodebuild.log" | head -50
```

全文ログを会話へ貼らない。最初の実エラー、該当ファイルと位置、exit status、
成功・未実行の段階を報告する。compile が通っても UI や実機の挙動は保証しない。

## Simulator での実行と画面確認

利用可能な Simulator を JSON で列挙し、端末名ではなく ID を保持する。

```bash
xcrun simctl list devices available --json
xcrun simctl boot SIMULATOR_ID
xcrun simctl bootstatus SIMULATOR_ID -b
```

既に boot 済みなら再度 `boot` せず、その ID を使う。Simulator service が接続不能なら、
権限だけを原因と決めつけず、表示された service・runtime・disk image のエラーを保つ。

アプリ bundle の場所と bundle identifier は、同じ container、scheme、destination で
`xcodebuild -showBuildSettings -json` を実行し、`TARGET_BUILD_DIR`、`WRAPPER_NAME`、
`PRODUCT_BUNDLE_IDENTIFIER` から得る。

```bash
xcrun simctl install SIMULATOR_ID /path/to/App.app
xcrun simctl launch SIMULATOR_ID com.example.app
xcrun simctl io SIMULATOR_ID screenshot "$task_tmp_dir/screenshot.png"
```

SwiftUI の外観は、実アプリまたは専用の snapshot/UI test で対象状態を作り、
`simctl io ... screenshot` の画像を確認する。
起動できなければ画面確認は未実施と報告する。

## 実機での実行

実機が必要な場合は `devicectl` を使う。自動処理で読む結果は stdout ではなく
`--json-output` のファイルを使う。

```bash
xcrun devicectl list devices --json-output "$task_tmp_dir/devices.json"
xcrun devicectl device install app --device DEVICE_ID /path/to/App.app
xcrun devicectl device process launch \
  --device DEVICE_ID --terminate-existing com.example.app
```

実機登録、署名資産の変更、アプリ削除は勝手に行わない。`-allowProvisioningUpdates` は
Developer Portal に変更を加え得るため、必要性と対象を確認してから使う。

## Swift コード片の確認

プロジェクトに依存しない短いコードは `swift -e` で確認する。

```bash
swift -e 'import Foundation; print(ProcessInfo.processInfo.operatingSystemVersion)'
```

アプリの型、resource、build setting に依存するコードは、既存または追加する対象テストで
確認する。Git 管理対象の一時ファイルや検証専用 target を無断で残さない。

GUI 上の現在のファイルや選択範囲は参照せず、リポジトリと依頼内容から対象を特定する。
特定できなければファイルパスまたはシンボル名を確認する。

## ファイルの追加

新規ファイルが target に入る仕組みを確認してから追加する。

**`project.yml` がある場合**

`.xcodeproj` は生成物として扱う。`project.yml` の `sources` と `excludes` を確認し、
対象ディレクトリへファイルを追加して `xcodegen generate` を実行する。
生成された `.pbxproj` だけを直接直さない。

**`project.yml` がない場合**

`.pbxproj` に `PBXFileSystemSynchronizedRootGroup` があり、対象ディレクトリが同期対象なら、
その配下へファイルを追加してビルドで inclusion を確認する。

classic group の project では、リポジトリが既に使う generator や `xcodeproj` などの
管理手段があればそれを使う。なければ周辺の `PBXFileReference`、`PBXBuildFile`、group、
build phase の形式に合わせて `.pbxproj` を更新する。変更後は `plutil -lint`、
`xcodebuild -list`、対象 build で構造と target membership を確認する。

既存ファイルはファイルシステム上で通常どおり編集する。

## やらないこと

- scheme、destination、Simulator 名を根拠なく決めない
- security validation を弱める option を高速化目的で既定にしない
- 既存の Simulator、実機、インストール済みアプリを自動削除しない
- build、test、runtime、実機確認を一つの「動作確認済み」にまとめない
- ビルドログ全文を会話へ持ち込まない
