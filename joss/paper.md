---
title: 'Omega-Stack: A Six-Layer Defense and Streaming Benchmark Toolkit for Multi-Document LLM Security'
tags:
  - natural language processing
  - artificial intelligence
  - security
  - benchmarks
  - data engineering
authors:
  - name: Mehrdad Poorhassan
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 25 November 2026
bibliography: paper.bib
---

# Summary

Omega-Stack is a Python toolkit for defending retrieval-augmented generation
(RAG) pipelines against multi-document prompt injection. Its core component,
`src/omega_stack_security_engine.py`, implements a six-layer defense
architecture that filters, isolates and aggregates retrieved document windows
before they reach a language model. The repository also contains
constant-memory streaming engines (batched CSV, C++/zlib and PyArrow Parquet
Snappy consumers) benchmarked at 127,373 rows/sec on commodity hardware with a
3.07 MB peak RAM footprint, together with a reproducible evaluation harness
(`llm_security_benchmark_suite.py`) over 200 adversarial test windows.

# Statement of need

Indirect prompt injection through retrieved documents is a documented attack
surface of LLM-integrated applications [@greshake2023not], and design-level
defenses are an active research area [@debenedetti2026camel]. Existing defenses
are usually embedded in closed systems; researchers need a modular,
open-source defense and benchmark stack they can run on their own corpora.
Omega-Stack provides (1) an isolated-then-aggregate defense engine that does
not require model fine-tuning, (2) a constant-memory streaming data layer for
billion-record pipelines, and (3) the Philoprompts-v1.0 corpus
[@poorhassan2026philoprompts] of 563 multilingual and ancient-script stress
items with a Zenodo DOI, enabling tokenizer and safety-alignment
stress-testing under out-of-distribution Unicode inputs. The included
pure-Python tokenizer study (papers/tokenizer_study) shows that all three
evaluated byte-level BPE tokenizers, including the o200k_base vocabulary,
decompose every tested ancient non-BMP character into four single-byte
fallback tokens. The toolkit is aimed at LLM-security researchers and data
engineers who need a reproducible baseline for injection-resistance and
streaming experiments.

# References
