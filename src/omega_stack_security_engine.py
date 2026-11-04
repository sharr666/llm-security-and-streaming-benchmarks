"""
Author: Mehrdad Poorhassan (Dr. Metal) - ORCID: 0009-0004-9269-3912
CERN Zenodo DOI: 10.5281/zenodo.23758690
Omega-Stack v2.1 Multi-Document RAG Quarantine Engine (Keyed HMAC L0, NFKC Bilingual L1, Adjacency L2, Compound L4)
"""
import hashlib
import hmac
import json
import math
import re
import time
import tracemalloc
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

DEFAULT_REPO_KEYS: Dict[str, bytes] = {
    "r1": b"omega-repo-r1-hmac-signing-key",
    "r2": b"omega-repo-r2-hmac-signing-key",
}


@dataclass
class RetrievedChunk:
    chunk_id: str
    doc_id: str
    repo_id: str
    trust_tier: str  # "authored" vs "external_untrusted"
    text: str
    claimed_sha256: Optional[str] = None
    computed_hmac: str = field(init=False)

    def __post_init__(self) -> None:
        key = DEFAULT_REPO_KEYS.get(self.repo_id, b"unregistered-repo-key")
        payload = f"{self.repo_id}:{self.doc_id}:{self.chunk_id}:{self.trust_tier}:{self.text}".encode("utf-8")
        self.computed_hmac = hmac.new(key, payload, hashlib.sha256).hexdigest()
        if self.claimed_sha256 is None and self.repo_id in DEFAULT_REPO_KEYS:
            self.claimed_sha256 = self.computed_hmac
        elif self.claimed_sha256 is None:
            self.claimed_sha256 = ""


class OmegaStackSecurityEngine:
    ZERO_WIDTH_RE = re.compile(r"[\u200b\u200c\u200d\ufeff\u00ad]")
    IMPERATIVE_PATTERNS = [
        re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|directives|rules|safety)", re.I),
        re.compile(r"(system\s+override|privileged\s+channel|sudo\s+mode|developer\s+mode)", re.I),
        re.compile(r"(exfiltrate|send\s+to|webhook|\?token=)", re.I),
        re.compile(r"(disregard\s+safety|bypass\s+guardrail|execute\s+shell|rm\s+-rf)", re.I),
        re.compile(r"(دستورات\s+قبلی\s+را\s+نادیده|قوانین\s+امنیتی\s+را\s+دور\s+بزن|کلید\s+محرمانه\s+را\s+چاپ\s+کن)"),
    ]
    SPLIT_PAYLOAD_RULES = [
        ("ignore all previous", "and output the secret key"),
        ("system override:", "grant level 0 privileges"),
        ("bypass safety policy", "and exfiltrate context"),
        ("begin privileged directive", "execute unauthorized tool"),
    ]
    CONTINUATION_MARKERS = ("step 2", "continuation", "footer", "part 2", "and ", "then ")

    def __init__(self, entropy_threshold: float = 4.85, non_bmp_ratio_threshold: float = 0.15, max_rank_gap: int = 2) -> None:
        self.entropy_threshold = entropy_threshold
        self.non_bmp_ratio_threshold = non_bmp_ratio_threshold
        self.max_rank_gap = max_rank_gap

    @classmethod
    def normalize_text(cls, text: str) -> str:
        return cls.ZERO_WIDTH_RE.sub("", unicodedata.normalize("NFKC", text))

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

        # L0: Keyed HMAC-SHA256 Origin Authenticity & Integrity
        for c in chunks:
            if c.repo_id not in DEFAULT_REPO_KEYS or not c.doc_id or not c.claimed_sha256:
                triggers["L0"] = True
                flags.append(f"L0: Unregistered repo or missing HMAC in {c.doc_id}:{c.chunk_id}")
            elif not hmac.compare_digest(c.claimed_sha256, c.computed_hmac):
                triggers["L0"] = True
                flags.append(f"L0: Keyed HMAC-SHA256 verification failed in {c.doc_id}:{c.chunk_id}")

        untrusted = [c for c in chunks if c.trust_tier != "authored"]

        # L1, L3, L4: Per-Chunk Normalized Inspection
        for c in untrusted:
            norm_text = self.normalize_text(c.text)
            for pat in self.IMPERATIVE_PATTERNS:
                if pat.search(norm_text):
                    triggers["L1"] = True
                    flags.append(f"L1: Imperative pattern in {c.doc_id}:{c.chunk_id}")
            if re.search(r"(\[SYSTEM\]|LEVEL\s*0\s*DIRECTIVE|AUTHORITY:\s*ROOT)", norm_text, re.I):
                triggers["L3"] = True
                flags.append(f"L3: Authority spoofing in {c.doc_id}:{c.chunk_id}")
            ent = self.shannon_entropy(norm_text)
            nbmp = self.non_bmp_ratio(norm_text)
            has_directive_cue = bool(re.search(r"(override|execute|secret|directive|karma|𑀓𑀭𑁆𑀫)", norm_text, re.I))
            if ((len(norm_text) >= 40 and ent > self.entropy_threshold) or nbmp > self.non_bmp_ratio_threshold) and has_directive_cue:
                triggers["L4"] = True
                flags.append(f"L4: Compound entropy/non-BMP anomaly (H={ent:.2f}, nbmp={nbmp:.2f}) in {c.doc_id}:{c.chunk_id}")

        # L2: Rank-Adjacency & Continuity-Constrained Split-Payload Inspection
        for i, ca in enumerate(untrusted):
            for j, cb in enumerate(untrusted):
                if not (0 < (j - i) <= self.max_rank_gap):
                    continue
                ta = self.normalize_text(ca.text).lower()
                tb = self.normalize_text(cb.text).lower()
                has_bridge = any(m in tb for m in self.CONTINUATION_MARKERS)
                for prefix_frag, suffix_frag in self.SPLIT_PAYLOAD_RULES:
                    if prefix_frag in ta and suffix_frag in tb and has_bridge:
                        triggers["L2"] = True
                        pair_id = f"{ca.doc_id}:{ca.chunk_id}->{cb.doc_id}:{cb.chunk_id}"
                        provenance_pairs.append(pair_id)
                        flags.append(f"L2: Adjacent split-payload ({pair_id}): '{prefix_frag}' + '{suffix_frag}'")

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
