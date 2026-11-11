# check-japanese-text

日本語として生成された文字列に、中国語が混入していないか検査するCLIです。
中国語らしい箇所を1件でも検出すると終了コード`1`を返すため、生成パイプラインの再試行条件やCIのゲートとして使えます。
`--fix`を付けると、訂正語録に従った機械訂正を検出の前に行います。

判定は4つの検出器と、`--fix-words`で渡した訂正語録の和です。

| 検出器 | 何を見るか | 例 |
| --- | --- | --- |
| `simplified` | 中国語の簡体字。Unihanで`kTraditionalVariant`を持ち、日本の文字規格に採録されていない6,072字 | `这` `书` `龙` |
| `kyujitai` | 常用漢字表の通用字体に対する旧字体318字。中国語の繁体字と同じ字形です | `獻` `靜` `傳` |
| `unknown-word` | SudachiPyで日本語として解析したときの未知語のうち、漢字を含み数詞でないもの | `這個` `靠近` |
| `chinese-sentence` | 句点で終わり、漢字5字以上で、仮名も助詞も助動詞も無い文 | `我明日去学校。` |
| `fix-flag` | 訂正語録の報告専用行（`正`が`-`）。機械置換せず報告だけする | `逆袭`（候補: 逆襲/下剋上） |

文字集合だけでは、日中で共通する漢字で書かれた中国語を検出できません。
逆に形態素解析だけでは、送り仮名に続く旧字体（`靜かな`、`傳わる`）を検出できません。
この2つを補い合わせたうえで、どちらにもかからない共通漢字だけの文を`chinese-sentence`が拾います。

## セットアップ

Python 3.11以上と[uv](https://docs.astral.sh/uv/)を使用します。

```console
uv sync
```

## 使い方

標準入力を検査します。

```console
$ printf 'これは日本語です。' | uv run check-japanese-text
<stdin>: OK: 中国語混入は検出されませんでした
```

UTF-8ファイルも指定できます。

```console
uv run check-japanese-text answer.txt
```

中国語が見つかると、診断を標準エラーへ出力して終了コード`1`を返します。

```console
$ printf 'ここに这が混ざっています。' | uv run check-japanese-text
<stdin>:1:4: error: 中国語混入を検出 [...]
```

`--json`では、`status`、入力元、文字数、中国語固有文字の出現数と含有率、検出区間を標準出力へ返します。
位置の`start`と`end`は0始まりのUnicodeコードポイント位置、`line`と`column`は1始まりです。

```console
uv run check-japanese-text --json answer.txt
```

ファイルは複数指定できます。
その場合、人間向け出力はファイルごとに出力され、`--json`は結果の配列を返します。
終了コードは、どれか1つでも汚染があれば`1`です。

```console
uv run check-japanese-text chapter01.txt chapter02.txt
```

`--allow-words`には、誤検出した正しい日本語を登録した許容語録ファイルを指定します。
語が本文に出現する区間に検出が完全に収まる場合だけ、その検出は無視され、サマリーに抑制件数が表示されます。
抑制は語そのものではなく出現位置で効くため、`東京大学`を登録しても、別の場所に単独で現れる`東`は検出されたままです。
`--deny-words`には、見逃し対策の中国語句を登録した検出語録ファイルを指定します。
テキストに部分一致した箇所が、detector`custom-deny`として検出されます。
どちらの語録も1語1行で、`#`で始まる行はコメント、`語<TAB>理由`の理由付記ができます。
検出語録と許容語録の両方に一致した場合は、許容が優先されます。

```console
uv run check-japanese-text --allow-words allow_words.txt --deny-words deny_words.txt answer.txt
```

`--fix`を付けると、検出の前に`--fix-words`の訂正語録に従ってファイルを書き換えます。
訂正語録は`誤<TAB>正<TAB>理由`の1語1行で、`正`が`-`の行は報告専用になります。
報告専用行に一致した箇所は書き換えず、detector`fix-flag`として`warn`出力されます。
書き換えの適用件数は人間向け出力に表示され、`--json`では`fixes_applied`に入ります。
`--fix`は標準入力と併用できません。

```console
uv run check-japanese-text --fix --fix-words fix_words.txt chapter01.md
```

終了コードは次のとおりです。

- `0`: 中国語混入なし
- `1`: 中国語混入あり（`fix-flag`の要確認を含む）
- `2`: 引数、読込み、UTF-8、内部処理のエラー

## 判定範囲と制約

- 検査対象は渡された最終回答だけです。thinkingタグなどは解釈しません。
- 中国語の企業名、人名、引用も例外なく失敗にします。
- 英語など、中国語以外の言語は失敗条件にしません。
- 中国語固有文字の含有率は診断情報であり、合否は1件以上検出したかで決まります。
- 日中共通の漢字だけで書かれ、かつ仮名に囲まれた短い句（`この術は可以使用の状態にある`）は、
  どの検出器にもかかりません。`--deny-words`で個別に登録してください。
- 旧字体は日本語でも使われるため、意図して使う字は`--allow-words`に登録してください。
- 漢字5字以上の体言止め（`焔牙結界発動。`）は`chinese-sentence`が誤検出します。
  四字熟語（`絶体絶命。`）は閾値の下なので誤検出しません。

## 開発

```console
uv run pytest
```

同梱データはUnicode 17.0.0と常用漢字表（平成22年内閣告示第2号）へ固定しています。
更新時だけネットワークを使用し、公式の`Unihan.zip`とWikipedia「常用漢字一覧」から再生成します。

```console
uv run python tools/generate_data.py --version 17.0.0
```

生成元URL、ZIPのSHA-256、抽出条件は`src/japanese_checker/data/data_metadata.json`に記録されます。
簡体字集合には[Unicode License v3](https://www.unicode.org/license.txt)が、
旧字体対応表にはCC BY-SA 4.0が適用されます。
