# Philoprompts Tokenizer Study

Empirical byte-level BPE tokenizer measurements over the full
[Philoprompts-v1.0](https://huggingface.co/datasets/Dr-Metal/philoprompts-v1)
corpus (563 blocks; 560 active blocks analyzed, 3 INTENTIONAL_GAP rows
excluded), supporting the preprint "Self-Intertwined Deconstructed
Philoprompts" and the planned arXiv submission "How Ancient Scripts Break
Modern Tokenizers".

## Tokenizers

- **GPT-2** byte-level BPE from the official OpenAI vocab.json + merges.txt
- **cl100k_base** (GPT-3.5/4 line) from the official .tiktoken rank file
- **o200k_base** (GPT-4o line) from the official .tiktoken rank file

All three are implemented in pure Python (standard library only) in
philoprompts_tokenizer_study.py, with verification checks.

## Headline results

1. **Every ancient non-BMP character tested decomposes into exactly 4
   single-byte fallback tokens in all three tokenizers, including the newest
   o200k_base.** Tested: Brahmi (U+11000 block), Sumero-Akkadian cuneiform,
   Old Persian, Avestan and Ge'ez characters. None of the vocabularies has
   any coverage of these scripts.
2. Corpus-wide continuation-byte token share (560 active blocks,
   1,563,559 bytes): GPT-2 **24.32%**, cl100k_base **5.83%**,
   o200k_base **2.96%**.
3. Brahmi-dominant blocks show the highest fallback rates even in modern
   tokenizers (GPT-2 27.5%, cl100k 14.0%, o200k 13.6%), vs Persian control
   blocks (23.5% / 4.5% / 1.5%): the fallback metric separates living-language
   text from ancient-script renderings.

## Overall metrics (560 active blocks)

| Tokenizer | Tokens | Bytes/token | Chars/token | Continuation-byte token share |
|---|---:|---:|---:|---:|
| GPT-2 | 1,026,596 | 1.523 | 0.97 | 24.32% |
| cl100k_base | 720,645 | 2.170 | 1.38 | 5.83% |
| o200k_base | 529,611 | 2.952 | 1.88 | 2.96% |

Per-block and per-script metrics: see results/ (regenerable with the script).

## Method and verification

- Canonical token IDs verified: GPT-2 "Hello world" -> [15496, 995];
  cl100k "hello world" -> [15339, 1917].
- Byte round-trip integrity verified for every tokenizer on English, Persian
  and cuneiform samples.
- Each ancient single character measured directly (results/single_char_cost.json).

## Reproduce

    python papers/tokenizer_study/philoprompts_tokenizer_study.py

The first run downloads the corpus (philoprompts.jsonl) and the official
tokenizer artifacts into ./data and writes per-block CSV files and aggregate
JSON into ./results.

## Caveats

- Pre-tokenizer regexes approximate the original tiktoken patterns with
  stdlib Unicode classes (\p{L} -> [^\W\d_], \p{N} -> \d); deviations affect
  underscore and rare numeric categories only and do not affect the headline
  fallback result.
- These metrics measure tokenizer behaviour, not model behaviour; no security
  claim follows from them alone.
- License: Apache License 2.0 (same as this repository).
