# Changelog

All notable changes to this project are documented in this file.
Format is based on Keep a Changelog; this project adheres to Semantic Versioning.

## [Unreleased]
- Added a pure-Python (stdlib-only) tokenizer study for Philoprompts-v1.0
  (papers/tokenizer_study/): GPT-2, cl100k_base and o200k_base evaluated over
  all 560 active corpus blocks, with per-script byte-fallback metrics,
  verification checks and reproducible scripts + results.
- Added JOSS submission draft (joss/paper.md, joss/paper.bib).

## [v1.0.1] - 2026-11-08
- ARGON GEMINI v3.0 audit (Stage A/B): added Apache License 2.0, GitHub Actions
  CI matrix (Python 3.10-3.12), refactored declarative_prompt_compiler.py;
  both CI pipelines green.
- Zenodo record (versioned): https://doi.org/10.5281/zenodo.23758690

## [v1.0.0] - 2026-10-29
- Initial public release: Omega-Stack six-layer security engine
  (src/omega_stack_security_engine.py), constant-memory streaming engines
  (batched CSV, C++/zlib, PyArrow Parquet Snappy, POSIX awk),
  llm_security_benchmark_suite.py, and the PhiLLOPROMPTS ancient-script LLM
  security monograph.
