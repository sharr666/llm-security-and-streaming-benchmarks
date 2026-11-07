# LLM Security, Bounded-Memory Streaming Benchmarks & Philoprompts Corpus
**Author:** Mehrdad Poorhassan (`Dr. Metal`)
**ORCID iD:** `0009-0004-9269-3912`
**CERN Zenodo DOI:** `10.5281/zenodo.23758690`
**Open Science Framework (COS / OSF):** `23uab` (`osf.io/23uab`)
**arXiv Verified Author:** `Dr.Metal` (`cs.AI`, `cs.CL`, `cs.CR`)
**Scientific Memberships:** American Chemical Society (`ACS: dr.metal`) · CODATA Data Science Journal (`sharr666`)
**Research status:** Experimental prototype; independent validation is not claimed.

## Scope

This repository contains three separate artifacts:
1. **Omega-Stack v2.2:** a heuristic multi-document RAG quarantine prototype.
2. **Streaming examples:** small Python, C++/zlib, Parquet and POSIX pipeline demonstrations.
3. **Philoprompts:** an exploratory multilingual/Unicode test concept. The current monograph is a research note, not a fully released 234-record machine-readable corpus.

## Omega-Stack v2.2 layers

| Layer | Current implementation | Important limitation |
|---|---|---|
| L0 | HMAC-SHA256 verification against keys injected at runtime | Trust depends on independent key provisioning and producer controls; no production key ships here |
| L1 | NFKC/zero-width normalization and imperative-pattern rules | Lexical heuristic; paraphrases can evade it |
| L2 | Ordered adjacent-chunk split-payload pattern matching | Narrow pattern set; not semantic multi-hop reasoning |
| L3 | Authority-spoofing marker detection | Marker-based, not a general authority model |
| L4 | Entropy and non-BMP signals combined with directive cues | Heuristic anomaly signal, not proof of maliciousness |
| L5 | Fail-closed Boolean aggregation of L0–L4 | Can create false positives; policy tuning is required |

The engine deliberately does **not** create signatures for incoming data. The ingestion/producer service must supply a valid HMAC produced with an independently managed secret. Do not use test fixture keys or commit production secrets.

The current signed payload format is versioned canonical JSON (`omega-stack-hmac-v1`) over the repository, document, chunk, trust-tier and text fields. Producers must use the updated `chunk_signing_payload` helper or implement the exact same encoding. HMACs created with the earlier delimiter-joined format are not compatible and must be regenerated.

## Reproduce

Python 3.11+:

```bash
python -m unittest discover -s tests -v
python -m py_compile llm_security_benchmark_suite.py src/*.py
python llm_security_benchmark_suite.py
```

The benchmark contains 20 hand-authored examples. Its confusion matrix is a smoke-test diagnostic only. It is not a statistically powered evaluation and does not demonstrate generalization, robustness against adaptive attackers, or production readiness. The non-BMP report measures Unicode code points and UTF-8 byte lengths only; it does not measure a model tokenizer, MoE routing, or safety-classifier boundaries.

## Streaming demonstrations

The examples illustrate bounded temporary buffering for synthetic records. Memory observations depend on runtime, allocator, dependency versions and measurement method. The Parquet example currently builds each shard as Python lists before writing; it is **not** constant-memory in the number of rows per shard.

## Research notes and data status

- The Philoprompts monograph contains selected examples and a proposed taxonomy.
- The complete 234-entry corpus is not currently published as a validated, independently reproducible JSON/CSV dataset.
- Ancient-script transliterations, glyph assignments and linguistic interpretations require specialist review before being called philologically verified.

## Security reporting

Please report suspected vulnerabilities privately via GitHub Security Advisories. Do not publish secrets, exploit details or personal data in a public issue.

## License

Source code: Apache-2.0. Documentation and corpus text: CC BY 4.0 where explicitly identified. The exact license scope must be checked per file before reuse.
