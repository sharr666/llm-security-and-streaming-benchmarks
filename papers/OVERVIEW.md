# Technical Reports & Monographs Overview

**Author:** Mehrdad Poorhassan (`Dr. Metal`) — **ORCID iD:** `0009-0004-9269-3912`  
**License:** `CC BY 4.0` for reports unless a file states otherwise · `Apache-2.0` for source code; the Philoprompts monograph currently declares `Apache-2.0`.

---

## 1. [Preprint / Technical Report] Isolated Multi-Document Query Logic and Defense-in-Depth Architecture Against Distributed Indirect Prompt Injection in Agentic Workflows
- **CERN Zenodo DOI:** `10.5281/zenodo.23758690`
- **Scope & Reported Evaluation:** The preprint describes multi-hop query isolation, chunk-level provenance tagging, passive tokenization, and a six-layer **Omega-Stack** design (`OIAG-285`). It reports an evaluation over 86 personal knowledge bases, 4 target repositories, 21 matched documents, and 58 retrieved chunks. Those counts and results are claims made by the preprint; the public repository does not include the underlying 86-KB dataset, full protocol, or artifacts needed to reproduce that evaluation. The executable code here is a small heuristic prototype and does not independently validate those reported results.
- **Executable Implementation:** [`../src/omega_stack_security_engine.py`](../src/omega_stack_security_engine.py) & [`../llm_security_benchmark_suite.py`](../llm_security_benchmark_suite.py)

---

## 2. [Preprint / Technical Report] From Heuristic Prompting to Declarative Compilation and Multi-Agent Cognitive Orchestration: A Systematic Survey
- **CERN Zenodo DOI:** `10.5281/zenodo.23762055`
- **Scope & Implementation Boundary:** The report surveys prompt-engineering taxonomies and memory concepts. The companion implementation currently provides five named framing profiles and a bounded in-process memory prototype; it does not implement independent DSPy/OPRO/EvoPrompt/TextGrad/MCP backends or a general multi-agent orchestration runtime. Streaming examples have different memory characteristics: the CSV, C++/zlib, and shell examples emit records incrementally, while the PyArrow Parquet example materializes a full shard as Python lists before writing and therefore uses memory proportional to the number of rows in one shard. Previously reported heap measurements are environment-specific and are not reproduced by the current CI workflow.
- **Executable Implementation:** Companion repository `sharr666/declarative-prompt-compilation-and-agentic-systems` & [`../src/parquet_snappy_streamer.py`](../src/parquet_snappy_streamer.py)

---

## 3. [Preprint / Technical Monograph] Self-Intertwined Deconstructed Philoprompts (`Philoprompts-v1.0`)
- **Primary Monograph & Corpus DOI (COS / OSF):** `10.17605/OSF.IO/Y8J9G` (https://doi.org/10.17605/OSF.IO/Y8J9G)
- **Companion Philoprompts-v1.0 Release DOI (CERN / Zenodo; publication status not independently confirmed):** `10.5281/zenodo.24238946` (https://doi.org/10.5281/zenodo.24238946)
- **Monograph (exploratory research note):** [`../PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md`](../PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md)
- **Scope & Evidence Status:** Proposes linguistic and adversarial research mechanisms and shows selected author-created examples with candidate Unicode script renderings. The current Hugging Face release reports 563 rows (`#0001–#0563`); this repository does not contain the full JSONL dataset. Older references to a 234-entry corpus are unreconciled with that release. The script renderings have not been independently philologically verified here. The mechanisms are research hypotheses, not experimentally validated LLM vulnerabilities or benchmark results.
**Date:** October 2026  

---

## 4. [Preliminary Technical Report — not peer-reviewed] A Detector-Only Screen of a Pinned Rule-Based RAG Quarantine Engine on 1,500 PIArena-Derived Examples
- **Author:** Mehrdad Poorhassan (`Dr. Metal`) · **ORCID:** [0009-0004-9269-3912](https://orcid.org/0009-0004-9269-3912); no institutional affiliation stated.
- **Status & Scope:** Exploratory detector-only screen: 0/750 injected-labeled and 0/750 benign-labeled rows were quarantined under a single-chunk mapping. No model, answer generation, tools, or end-to-end RAG behavior was tested; L2 was structurally unexercised. These are detector outputs, not attack-success or deployment-performance results.
- **Data & Reproducibility:** The report contains no source-text examples or dataset rows. The local study bundle is not included, and public data-rights/reproduction review remains pending.
- **Manuscript:** [`piarena-detector-screen.md`](piarena-detector-screen.md)
- **License:** CC BY 4.0, consistent with this directory’s technical-report policy. No DOI is assigned.
