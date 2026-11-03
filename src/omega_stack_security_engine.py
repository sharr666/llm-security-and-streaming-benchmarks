"""
Author: Mehrdad Poorhassan (Dr. Metal) - ORCID: 0009-0004-9269-3912
CERN Zenodo DOI: 10.5281/zenodo.23758690
Omega-Stack v2.0 Multi-Document RAG Quarantine Engine (L0-L4 Active Detectors + L5 Fail-Closed Aggregator)
"""
import hashlib
import json
import math
import re
import time
import tracemalloc
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RetrievedChunk:
    chunk_id: str
    doc_id: str
    repo_id: str
    trust_tier: str  # "authored" vs "external_untrusted"
    text: str
    claimed_sha256: Optional[str] = None
    computed_sha256: str = field(init=False)

    def __post_init__(self) -> None:
        payload = f"{self.repo_id}:{self.doc_id}:{self.chunk_id}:{self.text}".encode("utf-8")
        self.computed_sha256 = hashlib.sha256(payload).hexdigest()
        if self.claimed_sha256 is None:
            self.claimed_sha256 = self.computed_sha256


class OmegaStackSecurityEngine:
    """
    Architecture: 5 Active Detection Layers (L0..L4) + 1 Policy Aggregation Gate (L5):
    - L0 (Provenance & Integrity): Verifies SHA-256 digest & non-empty repo/doc metadata.
    - L1 (Imperative Regex Detector): Detects direct instruction-override patterns in untrusted chunks.
    - L2 (Boundary-Aware Split-Payload Detector): Inspects ordered untrusted chunk pairs (c_a -> c_b)
      across document boundaries and logs exact source document/chunk provenance pairs.
    - L3 (Authority Spoofing Detector): Flags untrusted chunks claiming Level-0/SYSTEM root tags.
    - L4 (Entropy & Non-BMP Script Detector): Flags high Shannon entropy or non-BMP character density.
    - L5 (Fail-Closed Aggregator): Boolean disjunction over L0..L4 triggers (not an independent detector).
    """
    IMPERATIVE_PATTERNS = [
        re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|directives|rules|safety)", re.I),
        re.compile(r"(system\s+override|privileged\s+channel|sudo\s+mode|developer\s+mode)", re.I),
        re.compile(r"(exfiltrate|send\s+to|webhook|\?token=)", re.I),
        re.compile(r"(disregard\s+safety|bypass\s+guardrail|execute\s+shell|rm\s+-rf)", re.I),
    ]

    SPLIT_PAYLOAD_RULES = [
        ("ignore all previous", "and output the secret key"),
        ("system override:", "grant level 0 privileges"),
        ("bypass safety policy", "and exfiltrate context"),
        ("begin privileged directive", "execute unauthorized tool"),
    ]

    def __init__(self, entropy_threshold: float = 4.85, non_bmp_ratio_threshold: float = 0.15) -> None:
        self.entropy_threshold = entropy_threshold
        self.non_bmp_ratio_threshold = non_bmp_ratio_threshold

    @staticmethod
    def shannon_entropy(text: str) -> float:
        if not text:
            return 0.0
        freq: Dict[str, int] = {}
        for ch in text:
            freq[ch] = freq.get(ch, 0) + 1
        n = len(text)
        return -sum((c / n) * math.log2(c / n) for c in freq.values())

    @staticmethod
    def non_bmp_ratio(text: str) -> float:
        if not text:
            return 0.0
        return sum(1 for ch in text if ord(ch) > 0xFFFF) / len(text)

    def inspect_multi_document_window(self, chunks: List[RetrievedChunk]) -> Dict[str, Any]:
        triggers = {"L0": False, "L1": False, "L2": False, "L3": False, "L4": False, "L5": False}
        flags: List[str] = []
        provenance_pairs: List[str] = []

        # L0: Cryptographic SHA-256 & Provenance Metadata Integrity
        for c in chunks:
            if not c.repo_id or not c.doc_id or c.claimed_sha256 != c.computed_sha256:
                triggers["L0"] = True
                flags.append(f"L0: Provenance/SHA-256 mismatch in {c.doc_id}:{c.chunk_id}")

        untrusted = [c for c in chunks if c.trust_tier != "authored"]

        # L1, L3, L4: Per-Chunk Untrusted Inspection
        for c in untrusted:
            for pat in self.IMPERATIVE_PATTERNS:
                if pat.search(c.text):
                    triggers["L1"] = True
                    flags.append(f"L1: Imperative pattern in {c.doc_id}:{c.chunk_id}")
            if re.search(r"(\[SYSTEM\]|LEVEL\s*0\s*DIRECTIVE|AUTHORITY:\s*ROOT)", c.text, re.I):
                triggers["L3"] = True
                flags.append(f"L3: Authority spoofing in {c.doc_id}:{c.chunk_id}")
            ent = self.shannon_entropy(c.text)
            nbmp = self.non_bmp_ratio(c.text)
            if (len(c.text) >= 40 and ent > self.entropy_threshold) or nbmp > self.non_bmp_ratio_threshold:
                triggers["L4"] = True
                flags.append(f"L4: Anomaly (entropy={ent:.2f}, non_bmp={nbmp:.2f}) in {c.doc_id}:{c.chunk_id}")

        # L2: Document-Boundary-Aware Ordered Pairwise Split-Payload Inspection
        for i, ca in enumerate(untrusted):
            for j, cb in enumerate(untrusted):
                if i == j:
                    continue
                ta, tb = ca.text.lower(), cb.text.lower()
                for prefix_frag, suffix_frag in self.SPLIT_PAYLOAD_RULES:
                    if prefix_frag in ta and suffix_frag in tb:
                        triggers["L2"] = True
                        pair_id = f"{ca.doc_id}:{ca.chunk_id}->{cb.doc_id}:{cb.chunk_id}"
                        provenance_pairs.append(pair_id)
                        flags.append(f"L2: Split-payload across ({pair_id}): '{prefix_frag}' + '{suffix_frag}'")

        # L5: Fail-Closed Policy Aggregator over L0..L4
        triggers["L5"] = any(triggers[f"L{k}"] for k in range(5))
        return {
            "quarantined": triggers["L5"],
            "triggers": triggers,
            "provenance_pairs": provenance_pairs,
            "flags": flags,
        }


def python_batched_csv_streamer(output_path: str = "/tmp/part_00001.csv", n_rows: int = 20_000, batch_size: int = 5_000) -> Dict[str, Any]:
    """Bounded-memory O(batch_size) CSV generator."""
    tracemalloc.start()
    t0 = time.perf_counter()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("id,category,trust_tier,prompt_text,expected_complexity\n")
        for s in range(1, n_rows + 1, batch_size):
            e = min(s + batch_size, n_rows + 1)
            f.writelines([f"{i},LLM_Security,Level_30_Untrusted,Evaluate isolation boundary for node {i},High\n" for i in range(s, e)])
            f.flush()
    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"rows": n_rows, "batch_size": batch_size, "elapsed_sec": round(elapsed, 4), "peak_heap_mb": round(peak / (1024 * 1024), 2)}


if __name__ == "__main__":
    print(json.dumps(python_batched_csv_streamer(), indent=2))
