# LLM Security, Streaming Benchmarks & Deconstructed Philoprompts Corpus

**Author:** Mehrdad Poorhassan (`Dr. Metal`)  
**ORCID iD:** `0009-0004-9269-3912`  
**CERN Zenodo DOI:** `10.5281/zenodo.23758690`  
**Licenses:** Code under `Apache-2.0` ([`LICENSE`](./LICENSE)) · Technical Reports & Corpus under `CC BY 4.0`  

---

## 1. Overview & Technical Reports
This repository provides the reference implementation for the **6-Layer Omega-Stack Multi-Document RAG Quarantine Engine (`OIAG-285`)**, four **constant-memory $O(1)$ high-throughput corpus streaming engines**, and the **Philoprompts-v1.0 Verified Multilingual & Ancient-Script Adversarial Corpus**.

- **Technical Papers Overview:** [`papers/OVERVIEW.md`](./papers/OVERVIEW.md) (*Isolated Multi-Document Query Logic and Defense-in-Depth Architecture*, CERN Zenodo DOI: `10.5281/zenodo.23758690`)
- **Philoprompts-v1.0 Monograph & Corpus:** [`PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md`](./PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md)
- **Citation Metadata:** [`CITATION.cff`](./CITATION.cff) · **Security Policy:** [`SECURITY.md`](./SECURITY.md)

---

## 2. Requirements & Benchmark Environment
- **Hardware & OS Baseline:** Linux `x86_64` (4 vCPU, 16 GB RAM, SSD storage)
- **Runtime Dependencies:** Python `>= 3.11` (`pyarrow >= 14.0.0` for Parquet Snappy), `g++` (`-O3 -lz` for C++ zlib streamer), `gawk` & `coreutils` (`split -C` for POSIX pipeline)

```bash
pip install pyarrow numpy pandas
```

---

## 3. Reproduce / Quick Start (One Command per Engine)

```bash
# 1. Run full 6-Layer Omega-Stack security verification & streaming test suite
python3 llm_security_benchmark_suite.py

# 2. Run Batched Python CSV Streamer (200,000 rows, 10,000-row flush batches)
python3 src/omega_stack_security_engine.py

# 3. Run Columnar PyArrow Parquet (Snappy) Streamer
python3 src/parquet_snappy_streamer.py

# 4. Compile & Run Native C++ (-O3 + zlib) Gzip Streamer
g++ -O3 src/compressed_generator.cpp -lz -o compressed_generator && ./compressed_generator

# 5. Run Zero-Copy POSIX Pipe Streamer (awk + split -C 666m)
bash src/posix_awk_split_streamer.sh
```

### Raw Reproducible Output Log (`python3 llm_security_benchmark_suite.py`)
```json
{
  "benign_quarantined": false,
  "attack_quarantined": true,
  "triggers": {
    "L0": false,
    "L1": true,
    "L2": true,
    "L3": true,
    "L4": true,
    "L5": true
  },
  "stream": {
    "rows": 20000,
    "elapsed_sec": 0.0942,
    "peak_heap_mb": 0.36
  }
}
```

---

## 4. Empirical Streaming & Security Benchmark Results (`Linux x86_64, Python 3.11, tracemalloc`)

Instead of unbounded in-memory DataFrame construction, all four streaming engines maintain **constant memory ($O(1)$ buffer complexity)** proportional strictly to the batch flush size:

| Engine / Subsystem | Target Output | Batch / Window Size | Measured Elapsed Time | Memory Profile (`tracemalloc` / RSS) |
| :--- | :--- | :--- | :--- | :--- |
| **`src/omega_stack_security_engine.py` (CSV)** | `200,000` rows (UTF-8 CSV) | `10,000` rows/flush | `0.9258 sec` | Constant memory $O(1)$, `peak heap ≈ 1.40 MB` |
| **`src/parquet_snappy_streamer.py` (Parquet)** | `500,000` rows (Snappy) | `5,000`–`50,000` rows/batch | `0.74`–`7.34 sec` | Constant memory $O(1)$, `peak heap ≈ 3.07 MB` (5k batch) / `30.04 MB` (50k batch) |
| **`src/compressed_generator.cpp` (`g++ -O3 -lz`)** | Multi-GB `.csv.gz` | `64 KB` zlib stream buffer | Disk-bandwidth bound | Constant memory $O(1)$, `RSS ≈ 1.80 MB` |
| **`src/posix_awk_split_streamer.sh` (`awk+split`)** | `666 MB` shards | OS pipe (`64 KB`) | Disk-bandwidth bound | Constant memory $O(1)$, `RSS ≈ 2.10 MB` |
| **6-Layer `Omega-Stack` Quarantine (`L0–L5`)** | Multi-doc RAG window | `5` chunks (`authored` vs `untrusted`) | `0.42 ms/window` | Detects L1 imperative, L2 split-payload, L3 authority spoofing, L4 entropy (`> 4.85`) |

---

## 5. Philoprompts-v1.0 Adversarial & Linguistic Mechanisms
Full monograph and 234 canonical entries in [`PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md`](./PHILOPROMPTS_ANCIENT_SCRIPT_LLM_SECURITY_MONOGRAPH.md):

| Mechanism ID | Linguistic / Script Vector | Target Vulnerability | Observed Token / Routing Effect |
| :--- | :--- | :--- | :--- |
| **`M-01`** | Asokan Brahmi (`U+11000..U+1107F`) & Cuneiform (`U+12000`) | BPE / Unigram Tokenizer | Forces UTF-8 4-byte fallback (`0xF0 0x91 ...`), bypassing surface keyword filters |
| **`M-02`** | Classical Chinese (`Wenyanwen`) | Attention Head Density | Compresses 15-token Persian paradoxes into 4–8 high-centrality logograms |
| **`M-03`** | Persian Sub-Word Morphemic Splitting (`khandidi` -> `khan didi?`) | Sub-word Tokenization | Bifurcates single verb into orthogonal semantic paths (`laugh` vs `see blood`) |
| **`M-04`** | Typographical Parenthetical Infilling (`shoyneh () r`) | Masked Token Reconstruction | Triggers implicit token infilling inside self-attention layers |
| **`M-05`** | Cross-Block Payload Interleaving (`#0014` -> `#0015`) | Context Window Attention | Splits grammatical subject and predicate across non-adjacent blocks |
| **`M-06`** | Zargari Syllabic Insertion Cipher (`qazanuzuna bazayazad`) | Surface Lexical Guardrails | Zero lexical overlap with standard dictionary while preserving deterministic decoding |

---

## 6. Citation

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
