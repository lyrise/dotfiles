---
name: japanese-proofreading
description: Correct and proofread Japanese text, grounded in machine detection by textlint. Use when asked to polish Japanese text while preserving its style and meaning.
---

# Japanese Proofreading

Before correcting Japanese text, run `textlint-rule-preset-ai-words-ja` to machine-detect words and phrasings that AI tends to overuse. The detections are input for judgment, not a list of words to replace across the board.

## Input and Execution

- When a file is specified, inspect that file read-only. Do not modify the target file.
- When only the text is given in the conversation, write it out as a `.md` file in a safe temporary directory. Always delete it after the inspection, whether it succeeds or fails.
- Do not modify the target repository's `package.json`, lockfile, or `.textlintrc`. Do not read existing textlint settings either.

Run the following command. Do not use `--fix`.

```sh
npm exec --yes \
  --package=textlint@15.8.0 \
  --package=textlint-rule-preset-ai-words-ja@1.2.0 \
  -- textlint --no-textlintrc --rule preset-ai-words-ja --format json "$input"
```

Read stdout as JSON and handle each diagnostic's `line`, `column`, `ruleId`, and `message`. Judge the exit status as follows.

- `0`: detection succeeded. No diagnostics.
- `1`: detection succeeded. Use the diagnostics in the JSON as input for proofreading.
- `2`, an npm fetch failure, a JSON parse failure, or any other command failure: detection failed. Show only the reason for the failure and the command to rerun, and do not return corrected text.

## Correction

Correct only when detection succeeded.

- Preserve the original politeness level (敬体 or 常体), technical depth, familiarity, meaning, factual claims, and Markdown structure. Change the style, summarize, translate, fact-check, or substantially restructure only on explicit request.
- Do not change code, commands, URLs, identifiers, proper nouns including product names, or explicit quotations.
- Fix typos, grammar, awkward modifier relationships, and redundancy. Rephrase a word flagged by textlint only when doing so resolves a translationese, abstract, or contextually unfit expression while preserving the meaning.
- Keep a flagged word if it is needed as a technical term or a specific expression. Do not replace it merely because it was detected.

Respond in Japanese, in the following order.

1. Under `訂正文`, show the text ready to use as is.
2. Under `検知と変更`, briefly show only the textlint diagnostics actually adopted (location and reason) and the changes that affected meaning or expression.

See [textlint-rule-preset-ai-words-ja](https://github.com/p1ass/textlint-rule-preset-ai-words-ja) for the words targeted by the preset and its options.
