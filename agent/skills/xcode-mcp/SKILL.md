---
name: xcode-mcp
description: iOS/macOS 開発を Xcode の MCP サーバ (xcrun mcpbridge, サーバ名 xcode-tools) 経由で行うための規範。可用性の判定、MCP を使う場面と xcodebuild CLI に落とす場面の切り分け、SwiftUI プレビュー描画・Swift REPL・Apple ドキュメント検索といった MCP 専用機能、XcodeGen 構成でのファイル追加手順を定める。Swift/SwiftUI のビルド、テスト実行、ビルドエラーの調査、プレビュー確認、シミュレータ実行を頼まれたとき、または .xcodeproj/.xcworkspace/Package.swift/project.yml を含むプロジェクトで作業するときに使用する。
---

# Xcode MCP を用いた iOS 開発

Xcode 26 以降は `xcrun mcpbridge` で起動中の Xcode 本体に接続できる。
ビルド・テスト・診断は、まずこの MCP 経由で行う。`xcodebuild` を直接叩くのは
MCP が使えないと判定したときだけにする。

MCP を優先する理由は 2 つある。
第一に、Xcode が既に持っている増分ビルドの状態とインデックスをそのまま使うため、
結果がユーザーの見ている Xcode の表示と一致する。エラーの見え方が食い違わない。
第二に、プレビュー描画・REPL・Apple ドキュメント検索は CLI に代替手段がない。

ツール名は `mcp__xcode-tools__` を前置きして呼ぶ（例: `mcp__xcode-tools__BuildProject`）。
別名を変えて登録している場合は前置きもそれに従う。

## 可用性の判定

iOS 開発の作業を始めるとき、最初に一度だけ `XcodeListWindows` を呼び、その結果で
経路を決める。以後の作業中は再判定しない。

失敗したときは、原因ごとに次のように切り分ける。黙って CLI に落ちない。

| 症状 | 原因 | 対応 |
| --- | --- | --- |
| `mcp__xcode-tools__*` というツールが存在しない | MCP が未登録、またはこのディレクトリのスコープで有効になっていない | `claude mcp add -s user xcode-tools -- xcrun mcpbridge` をユーザーに促す。セッション再起動が要る |
| ツールはあるが呼ぶと接続エラーになる | Xcode 側で外部エージェントの接続が許可されていない | Xcode の設定 → Intelligence → **Allow external agents to use Xcode tools** を有効にするようユーザーに依頼する（後述） |
| 呼べるがウィンドウが 0 件 | Xcode が起動していない、あるいは対象プロジェクトを開いていない | 対象の `.xcodeproj` / `.xcworkspace` を Xcode で開くようユーザーに依頼する |
| 以前は動いていたのに接続が拒否される | Claude Code の更新でバイナリのハッシュが変わり、Xcode 側の信頼が失効した | Xcode を前面に出して承認ダイアログを許可するようユーザーに依頼する |

**`claude mcp list` の結果を可用性の判定に使わない。**
このヘルスチェックは `tools/list` の待ち時間が短く、`xcode-tools` は
`Connected · tools fetch failed` と表示されることが多い。実測では初回応答に
2.6 秒から 44.7 秒までのばらつきがあり、Xcode 側が正常に 21 個のツールを返して
いてもヘルスチェックだけが落ちる。実セッションではより長く待つので問題なく使える。
判定は必ず `XcodeListWindows` を実際に呼んで行う。

### 外部エージェントの許可

Xcode は既定で外部エージェントの MCP 接続を拒否する。この設定が無効のままだと、
`initialize` は成功するのに `tools/list` が無応答になり、Claude Code からは
`tools fetch failed` としか見えない。Xcode 側のログにだけ理由が出る。

```
An Xcode setting prevented an untrusted agent from connecting
```

Xcode の設定 → Intelligence の **Allow external agents to use Xcode tools** を
有効にすると、以後は未知のエージェントの接続時に承認ダイアログが出るようになる。
対応する設定キーは `com.apple.dt.Xcode` の `IDEAllowUnauthenticatedAgents`。
参考: <https://developer.apple.com/documentation/xcode/giving-agentic-coding-tools-access-to-xcode>

承認はエージェントバイナリの SHA-512・署名・notarization に紐づく。
Claude Code が更新されてバイナリが変わるたびに再承認が要る。これは仕様であり、
回避しようとしない。

原因の切り分けが必要なときは Xcode 側のログを見る。bridge 側のログには
`listTools request failed` としか出ない。

```bash
log stream --process Xcode --style compact --level info \
  | grep "IDEIntelligenceChat:MCP Server"
```

複数の Xcode を同時に起動している場合、bridge は `xcode-select` で選ばれた方に
つなぐ。意図した方でなければ `MCP_XCODE_PID` を明示する必要がある。

## tabIdentifier

`XcodeListWindows` 以外のすべてのツールは `tabIdentifier` を必須引数に取る。
これはワークスペースのタブを指す識別子で、`XcodeListWindows` の戻り値から得る。

したがって**最初の呼び出しは必ず `XcodeListWindows`** になる。得た
`tabIdentifier` はセッション中使い回す。ウィンドウが複数ある場合は、作業対象の
ワークスペースに対応するものを選ぶ。判断がつかなければユーザーに確認する。

## ツール

Xcode 26.5 で実測した 21 個。**公開される集合は Xcode のバージョンで変わる**ため、
食い違いに気づいたら `/mcp` で一覧を確認し、この表を実測値に直す。

### ビルドとテスト

| ツール | 用途 | 主な引数 |
| --- | --- | --- |
| `BuildProject` | アクティブスキームでビルドし、完了まで待つ | — |
| `GetBuildLog` | 直近ビルドのログ。ビルド進行中かも返る | `severity` (`error`/`warning`/`remark`), `pattern`, `glob` |
| `GetTestList` | アクティブテストプランのテスト一覧 | — |
| `RunAllTests` | 全テストを実行 | — |
| `RunSomeTests` | 指定テストのみ実行 | `tests` (`targetName` + `testIdentifier` の配列) |

`GetBuildLog` は既定で全件返る。**必ず `severity: "error"` を付けて絞る。**
`pattern`（メッセージの正規表現）と `glob`（ファイルパス）も併用できる。

`GetTestList` の結果は 100 件で打ち切られ、全件は `fullTestListPath` のファイルに
grep しやすい形で書かれる。`TEST_TARGET` / `TEST_IDENTIFIER` / `TEST_FILE_PATH` を
キーに grep して目的のテストを探し、その識別子を `RunSomeTests` に渡す。

### MCP でしかできないこと

| ツール | 用途 | 主な引数 |
| --- | --- | --- |
| `RenderPreview` | SwiftUI プレビューをビルドして画像化 | `sourceFilePath` (必須), `previewDefinitionIndexInFile` (既定 0), `previewVariantOverrides`, `timeout` (既定 120 秒) |
| `ExecuteSnippet` | 指定ファイルの文脈でコード片をビルド・実行し、`print` の出力を返す | `sourceFilePath`, `codeSnippet`, `purpose` (すべて必須), `timeout` (既定 600 秒) |
| `DocumentationSearch` | Apple Developer Documentation を意味検索 | `query` (必須), `frameworks` |

`sourceFilePath` は**ファイルシステム上のパスではなく Xcode プロジェクト構造上の
パス**を渡す（例: `ShadowView/Views/ContentView.swift`）。

同一ファイルに `#Preview` が複数ある場合は `previewDefinitionIndexInFile` で
上から 0 始まりの位置を指定する。ダークモードなどの切り替えは
`previewVariantOverrides` に、戻り値の `supportedPreviewVariants` にあるキーと値を渡す。

`ExecuteSnippet` の `purpose` に "test" という語を使わない（ユーザーがテスト実行と
誤解するため、とツール自身が指示している）。

### 診断

| ツール | 用途 | 主な引数 |
| --- | --- | --- |
| `XcodeListWindows` | 開いているウィンドウとワークスペースを列挙。`tabIdentifier` の取得元 | 引数なし |
| `XcodeListNavigatorIssues` | Issue Navigator に出ている問題。ビルド以外にパッケージ解決やワークスペース構成の問題も含む | `severity` (既定 `error`), `pattern`, `glob` |
| `XcodeRefreshCodeIssuesInFile` | 1 ファイルのコンパイラ診断を取り直す | `filePath` |
| `XcodeGetCurrentFile` | エディタで開いている現在のファイルの内容と選択範囲 | `includeContent`, `includeSelection`, `offset`, `limit` |

`XcodeListNavigatorIssues` は最後のビルド以降に判明した分も含め、Xcode が既に
解析済みの結果を返す。ビルドし直さずにエラーを把握したいときはこちらを使う。

ユーザーが「今開いているファイル」と言ったときは `XcodeGetCurrentFile` を使う。
選択範囲まで取れるので、「この部分」の指示にも応えられる。

### ファイル操作

`XcodeRead` / `XcodeWrite` / `XcodeUpdate` / `XcodeRM` / `XcodeMV` / `XcodeMakeDir` /
`XcodeLS` / `XcodeGlob` / `XcodeGrep` は、**ファイルシステムではなく Xcode の
プロジェクト構造**に対して働く。パスもプロジェクト構造上のもので指定する。

`XcodeWrite` は新規ファイルを自動でプロジェクト構造に追加する。
使い分けは「ファイルの追加」節を見る。

`XcodeRead` は既定 600 行まで。大きいファイルは `offset` / `limit` で分割する。

`XcodeUpdate` と `XcodeWrite` の文字列はリテラルで渡す。`XcodeRead` の出力で
`\\d` と見えたものは `\d` と書く。

## MCP を使う場面

- 起動中の Xcode のアクティブスキームでビルド、テストする
- ビルドエラーを読む。`GetBuildLog` は `severity: "error"` で絞れるので、CLI の
  全文ログよりはるかに軽い。`XcodeListNavigatorIssues` は Xcode が既に解析した
  結果を返すのでビルドし直す必要がない
- SwiftUI の見た目を確認する。`RenderPreview` の画像を見て直し、また描画する、を回す
- Swift の断片的な挙動を確かめる。`ExecuteSnippet` は既存ファイルの文脈をそのまま
  使えるので、確認用のターゲットやテストを作らずに済む
- ユーザーが「今開いているファイル」「ここ」と言う。`XcodeGetCurrentFile` で
  ファイルと選択範囲が取れる
- Apple の API 仕様を調べる。`DocumentationSearch` は Apple 純正なので、この用途では
  Context7 より近い

## CLI にフォールバックする場面

次の場合は MCP を使わず `xcodebuild` / `swift` を使う。どちらの経路を使ったかは
ユーザーに一言添える。

- Xcode が起動していない、または対象を開いていない
- スキーム、destination、configuration を明示的に指定する必要がある
  （MCP は Xcode のアクティブスキームで動く）
- CI と同じ条件を再現する
- SPM 単体で `swift build` / `swift test` で足りる

フォールバック時は時間と出力の両方を削る。

```bash
xcodebuild -project ShadowView.xcodeproj -scheme ShadowView \
  -destination 'platform=iOS Simulator,name=iPhone 17' \
  -skipMacroValidation -skipPackagePluginValidation -skipPackageUpdates \
  build 2>&1 | xcbeautify --quiet
```

`-skipPackageUpdates` は依存解決を省くので 2 回目以降が明確に速くなる。
依存を更新したいときは外す。

**全文ビルドログを会話に貼らない。** エラー行と該当ファイルの位置だけを抜き出して
報告する。ログをファイルへ落として `grep` で絞るのが確実である。

```bash
xcodebuild ... build > /tmp/build.log 2>&1
grep -E "error:|warning:" /tmp/build.log | head -30
```

## ファイルの追加

新規 Swift ファイルの置き方はプロジェクトの構成で分かれる。ここを間違えると、
ファイルは存在するのにビルド対象に入らない。

**リポジトリに `project.yml` がある場合（XcodeGen）**

`.xcodeproj` は生成物である。通常の `Write` でファイルを置き、`xcodegen generate`
で再生成する。`XcodeWrite` は使わない。プロジェクトファイルへ直接加えた変更は
次回の生成で失われる。

ターゲットへの入り方が `project.yml` の `sources` の指定に依存するので、
`excludes` に該当しない場所へ置く。

**`project.yml` がない場合**

`.xcodeproj` が正である。新規ファイルは `XcodeWrite` で追加する。このツールは
新規ファイルをプロジェクト構造へ自動で登録する。素の `Write` では、ファイルが
プロジェクトに登録されない孤児になり、ビルド対象に入らない。

既存ファイルの編集は、どちらの構成でも通常の `Edit` でよい。`XcodeUpdate` を
使ってもよいが、`tabIdentifier` とプロジェクト構造上のパスが要る分だけ手間が増える。

## やらないこと

- MCP が使えないときに黙って CLI へ落ちない。理由と使った経路を述べる
- `RenderPreview` に相当することを求められて MCP が使えないとき、勝手に
  代替へ進まない。シミュレータ起動とスクリーンショットという代替を提示して選ばせる
- ビルドログの全文を会話に持ち込まない
- Xcode の信頼ダイアログを迂回しようとしない
