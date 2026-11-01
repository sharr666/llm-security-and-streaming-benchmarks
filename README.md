# LLM Security, Streaming Benchmarks & Deconstructed Philoprompts Corpus

**Author:** Mehrdad Poorhassan (`Dr. Metal`)  
**ORCID:** `0009-0004-9269-3912`  
**CERN Zenodo DOI:** `10.5281/zenodo.23758690`  
**License:** Apache License 2.0  

## 1. Overview
This repository provides empirical evaluation harnesses, streaming token-level red-teaming benchmarks, and the **Philoprompts-v1.0 Verified Multilingual & Ancient-Script Adversarial Corpus** for testing safety alignment, byte-fallback tokenization resilience, and state-space stability in Large Language Models (LLMs).

## 2. Core Components
- **`llm_security_benchmark_suite.py`**: Streaming red-teaming evaluation engine measuring Attack Success Rate (ASR), refusal calibration, and latency overhead across multi-turn adversarial contexts.
- **Philoprompts-v1.0 Benchmark (`PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md`)**: A philologically verified corpus of 234 canonical deconstructed Persian micro-poems (*Philoprompts*) paired with authentic non-BMP and classical scripts (Sanskrit in Brahmi script `U+11000..U+1107F`, Classical Chinese `Wenyanwen`, Sumerian & Akkadian cuneiform, Classical Latin, Ancient Greek, Avestan, Classical Ge'ez, Japanese Tri-Script, Digraphic Uzbek, and Zargari Phonetic Cipher).

## 3. Empirical Benchmark Summary (Philoprompts-v1.0)
| Adversarial Mechanism | Linguistic / Script Vector | Target Vulnerability | Observed Token / Routing Effect |
| :--- | :--- | :--- | :--- |
| **Non-BMP Byte-Fallback Fragmentation** | Brahmi Script (`U+11000..U+1107F`) & Cuneiform | BPE / Unigram Tokenizer | Forces UTF-8 4-byte fallback (`0xF0 0x91 ...`), bypassing lexical safety filters |
| **High-Entropy Logographic Compression** | Classical Chinese (`Wenyanwen`) | Attention Head Density | Compresses 15-token Persian paradoxes into 4–8 high-centrality logograms |
| **Sub-Word Morphemic Splitting** | Persian Lexical Steganography (`khandidi` -> `khan didi?`) | Sub-word Tokenization | Splits single verb into dual orthogonal semantic paths (`laugh` vs. `see blood`) |
| **Typographical Parenthetical Infilling** | Mid-Word Operator Injection (`shoyandeh` -> `shoyneh () r`) | Masked Language Modeling | Triggers implicit token reconstruction inside attention layers |
| **Syllabic Insertion Cipher** | Zargari Phonetic Obfuscation (`qazanuzuna bazayazad`) | Surface Keyword Filters | Zero lexical overlap with standard Persian while preserving deterministic decoding |
| **Cross-Page Payload Interleaving** | Distributed Semantic Continuation (`#0014` -> `#0015`) | Context Window Attention | Splits grammatical subject and predicate across non-adjacent blocks |

## 4. Citation
If you use this benchmark suite or the Philoprompts corpus in your research, please cite:
- Poorhassan, M. (2026). *Empirical Evaluation of LLM Security Guardrails, Streaming Benchmarks, and Deconstructed Ancient-Script Philoprompts*. Zenodo (CERN). DOI: `10.5281/zenodo.23758690`. ORCID: `0009-0004-9269-3912`
**Author:** Mehrdad Poorhassan (`Dr. Metal`)  
**ORCID:** `0009-0004-9269-3912`  
**CERN Zenodo DOI:** `10.5281/zenodo.23758690`  
**License:** Apache License 2.0  

## 1. Overview
This repository provides empirical evaluation harnesses, streaming token-level red-teaming benchmarks, and the **Philoprompts-v1.0 Verified Multilingual & Ancient-Script Adversarial Corpus** # LLM Security, Streaming Benchmarks & Deconstructed Philoprompts Corpus

**Author:** Mehrdad Poorhassan (`Dr. Metal`)  
**ORCID:** `0009-0004-9269-3912`  
**CERN Zenodo DOI:** `10.5281/zenodo.23758690`  
**License:** Apache License 2.0  

## 1. Overview
This repository provides empirical evaluation harnesses, streaming token-level red-teaming benchmarks, and the **Philoprompts-v1.0 Verified Multilingual & Ancient-Script Adversarial Corpus** for testing safety alignment, byte-fallback tokenization resilience, and state-space stability in Large Language Models (LLMs).

## 2. Core Components
- **`llm_security_benchmark_suite.py`**: Streaming red-teaming evaluation engine measuring Attack Success Rate (ASR), refusal calibration, and latency overhead across multi-turn adversarial contexts.
- **Philoprompts-v1.0 Benchmark (`PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md`)**: A philologically verified corpus of 234 canonical deconstructed Persian micro-poems (*Philoprompts*) paired with authentic non-BMP and classical scripts (Sanskrit in Brahmi script `U+11000..U+1107F`, Classical Chinese `Wenyanwen`, Sumerian & Akkadian cuneiform, Classical Latin, Ancient Greek, Avestan, Classical Ge'ez, Japanese Tri-Script, Digraphic Uzbek, and Zargari Phonetic Cipher).

## 3. Empirical Benchmark Summary (Philoprompts-v1.0)
| Adversarial Mechanism | Linguistic / Script Vector | Target Vulnerability | Observed Token / Routing Effect |
| :--- | :--- | :--- | :--- |
| **Non-BMP Byte-Fallback Fragmentation** | Brahmi Script (`U+11000..U+1107F`) & Cuneiform | BPE / Unigram Tokenizer | Forces UTF-8 4-byte fallback (`0xF0 0x91 ...`), bypassing lexical safety filters |
| **High-Entropy Logographic Compression** | Classical Chinese (`Wenyanwen`) | Attention Head Density | Compresses 15-token Persian paradoxes into 4–8 high-centrality logograms |
| **Sub-Word Morphemic Splitting** | Persian Lexical Steganography (`khandidi` -> `khan didi?`) | Sub-word Tokenization | Splits single verb into dual orthogonal semantic paths (`laugh` vs. `see blood`) |
| **Typographical Parenthetical Infilling** | Mid-Word Operator Injection (`shoyandeh` -> `shoyneh () r`) | Masked Language Modeling | Triggers implicit token reconstruction inside attention layers |
| **Syllabic Insertion Cipher** | Zargari Phonetic Obfuscation (`qazanuzuna bazayazad`) | Surface Keyword Filters | Zero lexical overlap with standard Persian while preserving deterministic decoding |
| **Cross-Page Payload Interleaving** | Distributed Semantic Continuation (`#0014` -> `#0015`) | Context Window Attention | Splits grammatical subject and predicate across non-adjacent blocks |

## 4. Citation
If you use this benchmark suite or the Philoprompts corpus in your research, please cite:
- Poorhassan, M. (2026). *Empirical Evaluation of LLM Security Guardrails, Streaming Benchmarks, and Deconstructed Ancient-Script Philoprompts*. Zenodo (CERN). DOI: `10.5281/zenodo.23758690`. ORCID: `0009-0004-9269-3912`. adversarial contexts.
- **Philoprompts-v1.0 Benchmark (`PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md`)**: A philologically verified corpus of 234 canonical deconstructed Persian micro-poems (*Philoprompts*) paired with authentic non-BMP and classical scripts (Sanskrit in Brahmi script `U+11000..U+1107F`, Classical Chinese `Wenyanwen`, Sumerian & Akkadian cuneiform, Classical Latin, Ancient Greek, Avestan, Classical Ge'ez, Japanese Tri-Script, Digraphic Uzbek, and Zargari Phonetic Cipher).

## 3. Empirical Benchmark Summary (Philoprompts-v1.0)
| Adversarial Mechanism | Linguistic / Script Vector | Target Vulnerability | Observed Token / Routing Effect |
| :--- | :--- | :--- | :--- |
| **Non-BMP Byte-Fallback Fragmentation** | Brahmi Script (`U+11000..U+1107F`) & Cuneiform | BPE / Unigram Tokenizer | Forces UTF-8 4-byte fallback (`0xF0 0x91 ...`), bypassing lexical safety filters |
| **High-Entropy Logographic Compression** | Classical Chinese (`Wenyanwen`) | Attention Head Density | Compresses 15-token Persian paradoxes into 4–8 high-centrality logograms |
| **Sub-Word Morphemic Splitting** | Persian Lexical Steganography (`khandidi` -> `khan didi?`) | Sub-word Tokenization | Splits single verb into dual orthogonal semantic paths (`laugh` vs. `see blood`) |
| **Typographical Parenthetical Infilling** | Mid-Word Operator Injection (`shoyandeh` -> `shoyneh () r`) | Masked Language Modeling | Triggers implicit token reconstruction inside attention layers |
| **Syllabic Insertion Cipher** | Zargari Phonetic Obfuscation (`qazanuzuna bazayazad`) | Surface Keyword Filters | Zero lexical overlap with standard Persian while preserving deterministic decoding |
| **Cross-Page Payload Interleaving** | Distributed Semantic Continuation (`#0014` -> `#0015`) | Context Window Attention | Splits grammatical subject and predicate across non-adjacent blocks |

## 4. Citation
If you use this benchmark suite or the Philoprompts corpus in your research, please cite:
- Poorhassan, M. (2026). *Empirical Evaluation of LLM Security Guardrails, Streaming Benchmarks, and Deconstructed Ancient-Script Philoprompts*. Zenodo (CERN). DOI: `10.5281/zenodo.23758690`. ORCID: `0009-0004-9269-3912`.ehrdad Poorhassan (ORCID: 0009-0004-9269-3912)

## Author
- **Author:** Mehrdad Poorhassan - Dr. Metal
- **ORCID:** https://orcid.org/0009-0004-9269-3912
- **DOI:** https://doi.org/10.5281/zenodo.23758690
## Technical Papers
1. Isolated Multi-Document Query Logic and 6-Layer Omega-Stack Framework
2. From Heuristic Prompting to Declarative Compilation and Multi-Agent Cognitive Orchestration
# llm-security-and-streaming-benchmarks

Multi-Document Retrieval Architecture, 6-Layer Security Framework, and Constant-Memory O(1) Corpus Streaming Engines — By Mehrdad Poorhassan (ORCID: 0009-0004-9269-3912)

## Author
- **Author:** Mehrdad Poorhassan - Dr. Metal
- **ORCID:** 0009-0004-9269-3912
- **DOI:** 10.5281/zenodo.23758690

## Technical Papers
1. Isolated Multi-Document Query Logic and 6-Layer Omega-Stack Framework
2. From Heuristic Prompting to Declarative Compilation and Multi-Agent Cognitive Orchestration

## Constant-Memory O(1) Corpus Streaming Engines
1. C++ -O3 with zlib
2. PyArrow Parquet Snappy
3. POSIX awk + split
4. Python Batched CSV Streamer

## Empirical Benchmark Results — Linux VM Verified

### 6-Layer Omega-Stack Multi-Document Evaluation
*(200 Test Windows: 100 Benign, 35 Monolithic Injection, 35 Split-Payload Cross-Document Injection, 30 Authority Spoofing / High-Entropy)*
- **Precision:** `1.0000`
- **Recall:** `1.0000`
- **F1 Score:** `1.0000`
- **Bypass Rate:** `0.0%`
- **Avg Latency:** `0.1016 ms/query` (`20.31 ms` total)

### Streaming Corpus Generation Benchmark (200,000 Records)
- `Python Batched CSV Streamer (10k batch)`: `127,373 rows/sec` (`12.38 MB/s`), Peak Heap RAM = `3.07 MB`
- `PyArrow Parquet Snappy Streamer (25k bounded batch)`: `46,543 rows/sec` (`2.48 MB` compressed output, `87.8%` size reduction), Peak Heap RAM = `27.53 MB`

## Citation
```bibtex
@article{poorhassan2026llm,
  author = {Poorhassan, Mehrdad},
  title = {llm-security-and-streaming-benchmarks},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23758690}
}
```
## Constant-Memory O(1) Corpus Streaming Engines
1. C++ -O3 with zlib
2. PyArrow Parquet Snappy
3. POSIX awk + split
4. Python Batched CSV Streamer
## Cittiona
```bibtex
@article{poorhassan2026llm,
  author = {Poorhassan, Mehrdad},
  title = {llm-security-and-streaming-benchmarks},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23758690},
  url = {https://doi.org/10.5281/zenodo.23758690}
}
```tion Citation
5. 
