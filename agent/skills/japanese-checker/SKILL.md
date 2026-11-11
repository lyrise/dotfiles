---
name: japanese-checker
description: >-
  Detect and mechanically fix Chinese-language contamination in Japanese text
  with the bundled check-japanese-text CLI. Inspect each finding in context,
  report true contamination, and grow the allow/deny/fix wordlists to reduce
  false positives and misses. Use when asked to check Japanese text for Chinese
  mixing, simplified or traditional Chinese characters, or Chinese-looking
  phrasing, or to maintain the checker's wordlists.
---

# Japanese Text Checker

Detect Chinese-language contamination in Japanese text, optionally apply the
fix wordlist, and judge each finding in context. Paths below are relative to
this skill's directory.

## Layout

- CLI: `vendor/check-japanese-text/` (detection logic and bundled Unicode data)
- Wrapper: `scripts/check-japanese-text.sh`
- Built-in wordlists: `allow_words.txt`, `deny_words.txt`, `fix_words.txt`
- Project wordlists: `<project root>/.agents/skills/japanese-checker/{allow,deny,fix}_words.txt`

Always run the wrapper from the target project, using the absolute path to this
skill's `scripts/check-japanese-text.sh`, so it can find that project's
wordlists. It adds the built-in wordlists and any project wordlists at the
project root (`git rev-parse --show-toplevel`, or the current directory), and
expands directory arguments to `.txt` and `.md` files. Directory expansion
skips the skill and project wordlist directories so `--fix` cannot rewrite
them. Extra `--allow-words`, `--deny-words`, and `--fix-words` flags are
additive.

## Commands

In these examples, `scripts/check-japanese-text.sh` means the absolute path to
this skill's wrapper, run from the target project.

Check files without editing:

```console
scripts/check-japanese-text.sh path/to/file.md
```

Apply the fix wordlist and then check:

```console
scripts/check-japanese-text.sh --fix path/to/file.md
```

Check a directory recursively (the wrapper expands `.txt` and `.md` files):

```console
scripts/check-japanese-text.sh path/to/dir
```

Check standard input (no `--fix`):

```console
printf '%s\n' 'text to check' | scripts/check-japanese-text.sh
```

Add `--json` for structured output. Exit codes:

- `0`: no contamination
- `1`: contamination or a `fix-flag` finding
- `2`: input or internal error

`--fix` rewrites files in place and cannot be used with standard input. Use it
only when the user asked for correction or the project workflow expects
mechanical fixes; otherwise run without it first.

## Detectors

The CLI combines the detectors below. The JSON `detectors` field names the ones
that fired, so the detector name tells you what kind of contamination it is.

| Detector | What it looks for | Examples |
| --- | --- | --- |
| `simplified` | Simplified Chinese characters that are not part of the Japanese character set (6,072 characters) | `这` `书` `龙` `们` |
| `kyujitai` | Old forms of common-use kanji (318 characters), which share glyphs with traditional Chinese | `獻` `靜` `傳` `樂` |
| `unknown-word` | Kanji words that the Japanese dictionary does not know | `這個` `靠近` `腾讯` |
| `chinese-sentence` | A sentence ending in a full stop, with five or more kanji and no kana, particles, or auxiliaries | `我明日去学校。` |
| `custom-deny` | A phrase registered in `deny_words.txt` | `可以使用` |
| `fix-flag` | A report-only row in `fix_words.txt` (`-` in the replacement column) | `逆袭` (candidates: 逆襲/下剋上) |

`fix-flag` positions refer to the text before any fix is applied.

Detector limits:

- A short phrase made only of kanji shared by Japanese and Chinese, surrounded
  by kana, escapes every detector (for example, `この術は可以使用の状態にある`).
  Register it in `deny_words.txt`.
- `chinese-sentence` only targets sentences that end with a full stop, contain
  five or more kanji, and have no kana, particles, or auxiliaries. Titles,
  headings, bullet items, and table cells are not sentences and are ignored.

## Wordlists

The built-in wordlists contain generally valid Japanese and general Chinese
contamination. Put project-specific names, terminology, and false positives in
the project wordlists, not in the built-in files.

`allow_words.txt` works on occurrence spans, not just words. A detection is
ignored only when the registered word fully covers the detected span. Register
the longest useful form; registering `東京大学` does not suppress a standalone
`東` elsewhere.

`deny_words.txt` matches substrings. Do not register short phrases that also
occur in valid Japanese; make the phrase specific enough to be uniquely
Chinese.

`fix_words.txt` rows with a replacement are applied by `--fix`. Rows with `-`
are report-only: they are not rewritten but appear as `fix-flag` findings.
Running without `--fix` does not apply fixes and does not report `fix-flag`
findings; register detection-only phrases in `deny_words.txt` as well when they
must be found in a dry run.

Format:

- allow / deny: `word<TAB>reason (optional)`
- fix: `wrong<TAB>right<TAB>reason (optional)`, or `wrong<TAB>-<TAB>reason`

`#` starts a comment line.

## Workflow

1. Run the wrapper on the requested target. Use `--fix` only when correction was
   requested or the project workflow expects it.
2. Read each finding in context, using the surrounding lines of the source file.
   Use `detectors` and `reasons` as clues.
   - **True contamination**: Chinese text has slipped into the body. Do not add
     it to the wordlists; report it. Do not edit the body beyond mechanical
     `--fix` corrections unless the user asked for it.
   - **False positive**: valid Japanese in context (a proper noun, a normal
     Japanese expression). Add the word to the project `allow_words.txt`.
   - **Miss**: text that is clearly Chinese in context but was not detected.
     - Detection only: add it to the project `deny_words.txt`.
     - One correct form is unambiguous: add `wrong<TAB>right` to the project
       `fix_words.txt`.
     - Several candidate corrections: add `wrong<TAB>-` to the project
       `fix_words.txt`, present the candidates, and ask the user before
       correcting.
   - **Uncertain**: do not add it to a wordlist. Ask the user when reporting.
3. After changing a wordlist, rerun the wrapper and confirm that only the
   intended findings disappeared. If a new word suppresses unrelated findings,
   make the word more specific.
4. Report:
   - per-file pass/fail and the contaminated locations (`file:line:column` and
     the matched text)
   - the judgment for each finding (true contamination / false positive / miss /
     needs confirmation)
   - wordlist changes and their reasons, or state that none were made

## Wordlist Editing Rules

- In `allow_words.txt`, register proper nouns and phrases in their longest form.
  Registering a single character suppresses that character everywhere in the
  body. The shipped old-form kanji entries are deliberate exceptions.
- Do not put short phrases that can occur in valid Japanese into
  `deny_words.txt`. Make a character that is also used in Japanese names part of
  a longer phrase.
- Add to `fix_words.txt` only when the correct Japanese form is unambiguous. Do
  not replace a character that has a valid Japanese use on its own (`后` occurs
  in `皇后`); use a phrase such as `死后` → `死後`.
- Add only words you are confident about from the current context. Do not turn
  one uncertain finding into a broad rule.
- Remove rows that a detector change made unnecessary only after running the
  checker and confirming they are unused. Do not keep rows whose reason is
  unknown.
