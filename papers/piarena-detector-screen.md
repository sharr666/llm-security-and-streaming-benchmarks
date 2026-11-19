# A Detector-Only Screen of a Pinned Rule-Based RAG Quarantine Engine on 1,500 PIArena-Derived Examples

**Author:** Mehrdad Poorhassan (Dr. Metal) · **ORCID:** [0009-0004-9269-3912](https://orcid.org/0009-0004-9269-3912) · **License:** CC BY 4.0 (repository report policy)

**Status:** Preliminary technical report; not peer-reviewed. The author identity and ORCID have been confirmed. No institutional affiliation is stated. AI-assisted preparation is disclosed; final contribution review, venue-specific AI disclosure, and data-rights review remain pending.

## Abstract

Prompt-injection benchmarks can test text detectors without establishing whether an injected instruction changes a model’s answer. We conducted a detector-only screen of an unchanged, hash-pinned rule-based quarantine engine against 1,500 English examples in a PIArena-derived configuration: 750 rows labeled as injected and 750 labeled benign for injection detection. Each row was supplied, unchanged, as a single untrusted retrieved-text chunk. All 1,500 invocations completed without errors. The engine quarantined 0/750 injected-labeled rows and 0/750 benign-labeled rows. Its multi-chunk split-payload layer was structurally unexercised by this single-chunk mapping. No model, answer-generation process, external tool, or inference API was used. The result therefore describes only this engine’s detector output under one declared representation; it is not an attack-success rate, an end-to-end RAG result, or an estimate of real-world security. The study is exploratory, uses a fixed derived benchmark subset, and does not claim an unseen test set or independent replication. Public release of the original data bundle is not proposed because the benchmark combines sources with different terms, including MS MARCO material whose official terms limit use to non-commercial research and do not grant underlying intellectual-property rights. [1] [2] [3] [4]

**Keywords:** prompt injection; retrieval-augmented generation; rule-based detector; security screening; PIArena; reproducibility

## 1. Introduction

Indirect prompt injection places instructions in content that an application retrieves or otherwise processes as data. Evaluation must distinguish detecting suspicious text from showing that a model followed an injected instruction. PIArena provides a platform and benchmark for evaluating prompt-injection attacks and defenses across tasks and datasets; its ACL 2026 paper emphasizes the need to test defenses across varied settings and warns that apparent effectiveness may not generalize. [1]

This note reports a narrow screen of one rule-based quarantine engine on a pinned 1,500-row PIArena-derived dataset configuration. The question is limited: when each provided text is presented to the engine as one untrusted chunk, which rows does the engine quarantine? We do not test a language model, query answering, retrieval, tool use, authentication, or attack success.

## 2. Materials and methods

### 2.1 Engine and data

We used an unchanged copy of `omega_stack_security_engine.py` with SHA-256 `d3b97027626bc416c20ba4014f4f502089c111890aebb59df84d0ae68a433ab3`. The file corresponds to commit `95e6f1bbe5444afd9a514abd0b2483aa8bc7ce6e` in the public project repository. [5] Parameters were held at `entropy_threshold=4.85`, `non_bmp_ratio_threshold=0.15`, and `max_rank_gap=2`; no model training or parameter tuning was performed.

The data were taken from the `piarena` configuration of Horizon-Labs’ Prompt Injection Eval Suite, pinned to revision `d6dd8d499d0087661afd6cd7ecdfcf94a5af1c05`. The file contained 1,500 rows: 750 labeled 1 (injection/jailbreak) and 750 labeled 0 (benign for injection detection), with no null or empty texts. All rows were supplied as English and indirect examples. These are the suite’s labels; they were not independently adjudicated, and “benign” does not mean harmless or useful in every context. [2]

### 2.2 Input mapping and procedure

The engine accepts structured `RetrievedChunk` envelopes rather than raw dataset rows. We mapped each full text, without truncation, to one `external_untrusted` chunk and ran one engine invocation per row. Local bookkeeping identifiers were unrelated to labels. A public synthetic fixture key was used only to satisfy the engine’s local envelope-consistency check; it was not an authentic publisher signature and cannot establish source authenticity, provenance, or trust.

The protocol and dataset structure were inspected before detector execution. The protocol was not preregistered before seeing the data or engine. Analysis ran without network access, and no model or inference API was called. The detector parameters and source code were not altered.

The engine’s L2 layer requires multiple chunks and therefore could not be exercised by this singleton mapping. Its zero count is not a result about split-payload detection. L0 reflects only the synthetic wrapper check, and L5 is the aggregate of the other layers rather than an independent detector.

### 2.3 Outcomes

The primary outcome was whether the engine returned `quarantined=true`, reported separately for each supplied label. We also recorded individual layer outputs and checked duplicate texts and candidate inserted-task/clean-context links. We report descriptive counts only. We do not compute population confidence intervals, significance tests, or causal effects because this is a narrow exploratory screen with repeated and potentially dependent source material.

## 3. Results

All 1,500 invocations completed; none errored or was excluded. The engine quarantined **0/750 injected-labeled rows (0%)** and **0/750 benign-labeled rows (0%)**. Each content layer available under the singleton mapping returned zero flags. L2 was structurally unavailable under this representation, not tested successfully and found negative. Four synthetic diagnostic controls outside the dataset confirmed that selected rule paths could produce flags; those controls are not included in the 1,500-row denominators.

The dataset contained 1,493 unique exact texts and seven excess duplicate rows, all among supplied benign rows. The duplicate-text sensitivity check did not change the all-zero quarantine result. We also reconstructed 750 candidate injected/clean links where removing one contiguous inserted span restored the corresponding clean text. The outputs were unchanged within those links, but these descriptive links are not independent observations and do not establish a causal effect.

## 4. Interpretation

Under this specific mapping, the engine’s available content rules did not flag any of the supplied injected-labeled texts. This is a useful implementation-screening result: it identifies a gap between this rule set and this subset of benchmark text under the tested input representation. It does not establish that attacks succeeded, that a model would follow them, or that the engine fails in every deployment setting.

The distinction matters because the benchmark’s labels describe injected versus clean text, while this experiment did not run a target model or measure its answer. The balanced label counts also do not make the observed outputs a reliable estimate of deployment performance. A different chunking design could activate L2, but would constitute a different experiment and must be reported separately.

## 5. Limitations

This is one detector, one pinned data configuration, and one input mapping. The source rows are all English and indirect. The study does not include user queries, retrieval ranks, real document boundaries, model responses, tool execution, or authenticated document provenance. The dataset labels were accepted as supplied. The protocol was frozen after inspection rather than preregistered before data access. The study does not establish independence from prior development or audits, an unseen test set, a population-level false-negative rate, generalization, or production readiness.

The upstream dataset card describes per-configuration licensing and notes that derived components retain their upstream terms. The composite includes Dolly, HotpotQA, Natural Questions, and MS MARCO-derived material. Their published terms are not uniform; in particular, Microsoft states that MS MARCO is intended for non-commercial research and does not extend underlying intellectual-property rights. No legal conclusion is made here. This draft contains no source-text examples and does not include the dataset, row-level intermediate outputs, or reproduction archive. Those materials are not cleared for public redistribution by this draft. [2] [3] [4] [6] [7] [8]

## 6. Reproducibility and availability

The study bundle, including the pinned dataset, row-level outputs, local analysis scripts, and evidence snapshots, remains in the private working archive. It has not been prepared as a public-release package. The engine source is available at the cited repository commit, but this draft does not claim that the complete experiment can be reproduced from the public repository alone. A public release would require a clean reproduction package that does not redistribute third-party data or examples, a review of dataset terms, and author approval of the code and outputs to be shared.

## Author and AI-use statement

The confirmed author is Mehrdad Poorhassan (Dr. Metal), ORCID [0009-0004-9269-3912](https://orcid.org/0009-0004-9269-3912). No institutional affiliation or additional co-author is stated. This draft was prepared from a Co-Scientist-generated research bundle; this statement does not claim independent validation beyond the documented checks. Before release, the author should review the final claims and confirm the contribution statement. AI assistance in the study and drafting should be disclosed according to the chosen venue’s current policy.

## References

[1]: https://aclanthology.org/2026.acl-long.1533/ "PIArena: A Platform for Prompt Injection Evaluation"
[2]: https://huggingface.co/datasets/Horizon-Labs/prompt-injection-eval-suite/blob/d6dd8d499d0087661afd6cd7ecdfcf94a5af1c05/README.md "Prompt Injection Eval Suite dataset card at pinned revision"
[3]: https://huggingface.co/datasets/sleeepeer/PIArena "PIArena dataset card"
[4]: https://microsoft.github.io/msmarco/ "MS MARCO Terms and Conditions"
[5]: https://github.com/sharr666/llm-security-and-streaming-benchmarks/blob/95e6f1bbe5444afd9a514abd0b2483aa8bc7ce6e/src/omega_stack_security_engine.py "Omega-Stack engine at the pinned source commit"
[6]: https://huggingface.co/datasets/databricks/databricks-dolly-15k "Databricks Dolly 15k dataset card"
[7]: https://huggingface.co/datasets/hotpotqa/hotpot_qa "HotpotQA dataset card"
[8]: https://huggingface.co/datasets/google-research-datasets/natural_questions "Natural Questions dataset card"
