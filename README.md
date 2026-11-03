# LLM Security, Bounded-Memory Streaming Benchmarks & Philoprompts Corpus

**Author:** Mehrdad Poorhassan (`Dr. Metal`)  
**ORCID iD:** `0009-0004-9269-3912`  
**CERN Zenodo DOI:** `10.5281/zenodo.23758690`  
**Licenses:** Source Code under `Apache-2.0` ([`LICENSE`](./LICENSE)) · Technical Reports & Corpus under `CC BY 4.0`  

---

## 1. Architecture Overview (Omega-Stack v2.0)
This repository implements the **Omega-Stack v2.0 Multi-Document RAG Quarantine Engine**, four **Bounded-Memory Streaming ($O(B)$ batch-buffered) Corpus Generators**, and the **Philoprompts-v1.0 Multilingual & Non-BMP Script Corpus**.

To maintain strict alignment between code and documentation, `src/omega_stack_security_engine.py` consists of **5 active detection mechanisms (`L0`–`L4`)** followed by **1 deterministic policy aggregation gate (`L5`)**:

| Layer | Component | Operational Implementation in `src/omega_stack_security_engine.py` |
| :---: | :--- | :--- |
| **`L0`** | **Provenance & SHA-256 Verifier** | Computes SHA-256 over `repo_id:doc_id:chunk_id:text` and flags tampered digests or missing metadata. |
| **`L1`** | **Imperative Regex Detector** | Scans untrusted chunks (`trust_tier != "authored"`) for instruction-override, sudo/developer mode, and exfiltration patterns. |
| **`L2`** | **Boundary-Aware Split-Payload Detector** | Evaluates ordered untrusted chunk pairs `(c_a, c_b)` across distinct document boundaries and records exact provenance links (`docA:chunkA->docB:chunkB`). |
| **`L3`** | **Authority Spoofing Detector** | Flags untrusted chunks attempting to spoof `[SYSTEM]`, `LEVEL 0 DIRECTIVE`, or `AUTHORITY: ROOT` headers. |
| **`L4`** | **Entropy & Non-BMP Script Detector** | Flags anomalous character Shannon entropy (`> 4.85` bits/char) or non-BMP codepoint density (`> 0.15`). |
| **`L5`** | **Fail-Closed Policy Aggregator** | Boolean disjunction (`any(L0..L4)`) that quarantines the multi-document window when any active detector fires. |

---

## 2. Reproduce / Quick Start (`Linux x86_64, Python 3.11`)

```bash
pip install pyarrow numpy pandas
python3 llm_security_benchmark_suite.py
```

### Exact Verbatim Output (`python3 llm_security_benchmark_suite.py`)
Evaluated across the 20-window labeled benchmark dataset (`10` Benign windows including `W10` legacy `[SYSTEM]` log false-positive edge case; `10` Adversarial windows covering `L0`–`L4` plus `W20` subtle semantic paraphrase false-negative edge case):

```json
{
  "confusion_matrix": {
    "total": 20,
    "TP": 9,
    "FP": 1,
    "TN": 9,
    "FN": 1
  },
  "metrics": {
    "precision": 0.9,
    "recall": 0.9,
    "f1": 0.9,
    "fpr": 0.1,
    "eval_latency_ms": 0.89
  },
  "sample_W19_trace": {
    "quarantined": true,
    "triggers": {
      "L0": false,
      "L1": true,
      "L2": true,
      "L3": true,
      "L4": false,
      "L5": true
    },
    "provenance_pairs": [
      "d19_docA:c19a->d19_docB:c19b"
    ]
  },
  "philoprompts_encoding_profile": {
    "BMP_Persian_#0001": {
      "codepoints": 37,
      "utf8_bytes": 67,
      "bytes_per_codepoint": 1.81,
      "non_bmp_codepoints": 0
    },
    "NonBMP_Brahmi_#0001": {
      "codepoints": 50,
      "utf8_bytes": 182,
      "bytes_per_codepoint": 3.64,
      "non_bmp_codepoints": 43
    },
    "NonBMP_Sumerian_#0031": {
      "codepoints": 16,
      "utf8_bytes": 49,
      "bytes_per_codepoint": 3.06,
      "non_bmp_codepoints": 11
    }
  },
  "bounded_memory_stream": {
    "rows": 20000,
    "batch_size": 5000,
    "elapsed_sec": 0.094,
    "peak_heap_mb": 0.36
  }
}
```

---

## 3. Bounded-Memory Streaming Engines ($O(B)$ Batch Complexity)
All four streaming generators bound peak heap allocation strictly by the flush batch size $B$ rather than total corpus length $N$:

| Engine Script | Command | Default Batch / Buffer $B$ | Measured Peak Memory (`tracemalloc` / RSS) |
| :--- | :--- | :--- | :--- |
| **`src/omega_stack_security_engine.py`** | `python3 src/omega_stack_security_engine.py` | `5,000`–`10,000` rows/flush | `0.36 MB` (5k batch) / `1.40 MB` (10k batch) |
| **`src/parquet_snappy_streamer.py`** | `python3 src/parquet_snappy_streamer.py` | `1,000`–`5,000` rows/shard | `3.07 MB` (5k batch) |
| **`src/compressed_generator.cpp`** | `g++ -O3 src/compressed_generator.cpp -lz -o gen && ./gen` | `64 KB` `gzbuffer` + `gzwrite` checks | `~1.80 MB` RSS |
| **`src/posix_awk_split_streamer.sh`** | `bash src/posix_awk_split_streamer.sh` | OS pipe (`split -C`) | `~2.10 MB` RSS |

---

## 4. Citation

```bibtex
@misc{poorhassan2026llmsecurity,
  author       = {Poorhassan, Mehrdad},
  title        = {{sharr666/llm-security-and-streaming-benchmarks: v1.0.1: Multi-Document LLM Architecture, Streaming Corpus Engines & Philoprompts-v1.0}},
  month        = oct,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0.1},
  doi          = {10.5281/zenodo.23758690},
  note         = {ORCID: 0009-0004-9269-3912}
}
```
