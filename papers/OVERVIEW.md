# Technical Reports & Monographs Overview

**Author:** Mehrdad Poorhassan (`Dr. Metal`) — **ORCID iD:** `0009-0004-9269-3912`  
**License:** `CC BY 4.0` (Reports & Monographs) · `Apache-2.0` (Source Code)

---

## 1. [Preprint / Technical Report] Isolated Multi-Document Query Logic and Defense-in-Depth Architecture Against Distributed Indirect Prompt Injection in Agentic Workflows
- **CERN Zenodo DOI:** `10.5281/zenodo.23758690`
- **Scope & Empirical Validation:** Formalizes multi-hop boolean query isolation (`deep-personal-search v2.0`), chunk-level provenance tagging ($T \in \{T_{\text{authored}}, T_{\text{archived}}\}$), passive tokenization, and the 6-layer **Omega-Stack** defense-in-depth blueprint (`OIAG-285`) validated across `86` personal knowledge bases (`4` target security repositories, `21` matched documents, and `58` retrieved chunks) under strict zero-web isolation.
- **Executable Implementation:** [`../src/omega_stack_security_engine.py`](../src/omega_stack_security_engine.py) & [`../llm_security_benchmark_suite.py`](../llm_security_benchmark_suite.py)

---

## 2. [Preprint / Technical Report] From Heuristic Prompting to Declarative Compilation and Multi-Agent Cognitive Orchestration: A Systematic Survey
- **CERN Zenodo DOI:** `10.5281/zenodo.23762055`
- **Scope & Empirical Validation:** Synthesizes the 6-level architectural taxonomy of LLM Systems Engineering (`PICCO`, `COAST`, `CARE`, `GCT`, `KERNEL`, `DSPy`, `OPRO`, `EvoPrompt`, `Promptbreeder`, `TextGrad`, `MCP`), evaluates 5 cognitive memory substrates, and benchmarks 4 **constant-memory $O(1)$ buffer** streaming corpus engines (`PyArrow Parquet Snappy` `peak heap ≈ 3.07 MB` on 5k batch / `1.40 MB` for Batched CSV on Linux `x86_64`, Python 3.11 `tracemalloc`).
- **Executable Implementation:** Companion repository `sharr666/declarative-prompt-compilation-and-agentic-systems` & [`../src/parquet_snappy_streamer.py`](../src/parquet_snappy_streamer.py)

---

## 3. [Preprint / Technical Monograph] Self-Intertwined Deconstructed Philoprompts (`Philoprompts-v1.0`)
- **Full Monograph & Verified Corpus:** [`../PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md`](../PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md)
- **Scope:** Formalizes 12 adversarial & linguistic tokenization mechanisms across 234 canonical deconstructed Persian micro-poems paired with philologically verified ancient and classical scripts (Asokan Brahmi `U+11000..U+1107F`, Sumero-Akkadian Cuneiform `U+12000..U+123FF`, Old Persian, Avestan, Classical Chinese `Wenyanwen`, Ancient Greek, Classical Latin, Classical Ge'ez, and Zargari syllabic cipher).
**Date:** October 2026  

## 1. Isolated Multi-Document Query Logic and Defense-in-Depth Architecture
Formalizes multi-hop boolean query isolation (`deep-personal-search v2.0`), chunk-level provenance tagging, passive tokenization, and the 6-layer **Omega-Stack** defense-in-depth blueprint validated across 4 repositories, 21 matched documents, and 58 retrieved chunks under strict zero-web isolation.

## 2. From Heuristic Prompting to Declarative Compilation and Multi-Agent Cognitive Orchestration
Synthesizes the 6-level architectural taxonomy of LLM Systems Engineering (`DSPy`, `EvoPrompt`, `Promptbreeder`, `OPRO`, `TextGrad`, `ProTeGi`, `MCP`), evaluates 5 cognitive memory substrates, and benchmarks 4 constant-memory O(1) high-throughput corpus streaming engines (`C++ -O3 + zlib`, `PyArrow Parquet Snappy`, `POSIX awk + split`, and batched Python CSV).
