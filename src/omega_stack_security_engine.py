"""Omega-Stack v2.2: heuristic RAG quarantine prototype. No production keys ship here."""
from __future__ import annotations
import hashlib, hmac, json, math, re, time, tracemalloc, unicodedata
from dataclasses import dataclass
from typing import Dict, List, Mapping


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    doc_id: str
    repo_id: str
    trust_tier: str
    text: str
    claimed_hmac: str


def chunk_signing_payload(chunk: RetrievedChunk) -> bytes:
    """Encode signed fields unambiguously with a versioned canonical JSON array."""
    if not isinstance(chunk, RetrievedChunk):
        raise TypeError("chunk must be a RetrievedChunk")
    fields = (chunk.repo_id, chunk.doc_id, chunk.chunk_id, chunk.trust_tier, chunk.text)
    if any(type(value) is not str for value in fields):
        raise ValueError("All signed chunk fields must be strings")
    return json.dumps(
        ["omega-stack-hmac-v1", *fields],
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def calculate_chunk_hmac(chunk: RetrievedChunk, key: bytes) -> str:
    """Producer-side helper. Keep the key outside source control."""
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("HMAC keys must be bytes with at least 32 bytes")
    return hmac.new(key, chunk_signing_payload(chunk), hashlib.sha256).hexdigest()


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
        ("ignore all previous", "output the secret key"),
        ("system override:", "grant level 0 privileges"),
        ("bypass safety policy", "exfiltrate context"),
        ("begin privileged directive", "execute unauthorized tool"),
    ]
    CONTINUATION_MARKERS = ("step 2", "continuation", "footer", "part 2", "and ", "then ")

    def __init__(self, repo_keys: Mapping[str, bytes], entropy_threshold: float = 4.85,
                 non_bmp_ratio_threshold: float = 0.15, max_rank_gap: int = 2) -> None:
        if not repo_keys:
            raise ValueError("Inject at least one externally provisioned repository key")
        for repo_id, key in repo_keys.items():
            if not repo_id or not isinstance(key, bytes) or len(key) < 32:
                raise ValueError("Every repository key must be named and contain at least 32 bytes")
        if entropy_threshold <= 0 or not 0 <= non_bmp_ratio_threshold <= 1 or max_rank_gap < 1:
            raise ValueError("Invalid detection thresholds")
        self.repo_keys = dict(repo_keys)
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
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        n = len(text)
        return -sum((count / n) * math.log2(count / n) for count in freq.values())

    @staticmethod
    def non_bmp_ratio(text: str) -> float:
        return sum(ord(char) > 0xFFFF for char in text) / len(text) if text else 0.0

    def inspect_multi_document_window(self, chunks: List[RetrievedChunk]) -> Dict[str, object]:
        triggers = {f"L{i}": False for i in range(6)}
        flags: List[str] = []
        provenance_pairs: List[str] = []
        valid_chunks: List[RetrievedChunk] = []
        if not isinstance(chunks, list):
            triggers["L0"] = True
            flags.append("L0: Retrieval window must be a list")
            triggers["L5"] = True
            return {"quarantined": True, "triggers": triggers,
                    "provenance_pairs": provenance_pairs, "flags": flags}
        if not chunks:
            triggers["L0"] = True
            flags.append("L0: Empty retrieval window")

        for index, chunk in enumerate(chunks):
            if not isinstance(chunk, RetrievedChunk):
                triggers["L0"] = True
                flags.append(f"L0: Invalid chunk object at index {index}")
                continue
            signed_fields = (
                chunk.repo_id, chunk.doc_id, chunk.chunk_id,
                chunk.trust_tier, chunk.text, chunk.claimed_hmac,
            )
            if (any(type(value) is not str for value in signed_fields)
                    or not chunk.repo_id or not chunk.doc_id or not chunk.chunk_id
                    or chunk.trust_tier not in ("authored", "external_untrusted")
                    or not re.fullmatch(r"[0-9a-f]{64}", chunk.claimed_hmac)):
                triggers["L0"] = True
                flags.append(f"L0: Malformed chunk envelope at index {index}")
                continue
            valid_chunks.append(chunk)
            key = self.repo_keys.get(chunk.repo_id)
            if key is None:
                triggers["L0"] = True
                flags.append(f"L0: Missing/unknown provenance or signing key for {chunk.doc_id}:{chunk.chunk_id}")
                continue
            try:
                expected = calculate_chunk_hmac(chunk, key)
            except (TypeError, ValueError):
                triggers["L0"] = True
                flags.append(f"L0: Invalid signed payload for {chunk.doc_id}:{chunk.chunk_id}")
                continue
            if not hmac.compare_digest(chunk.claimed_hmac, expected):
                triggers["L0"] = True
                flags.append(f"L0: HMAC-SHA256 verification failed for {chunk.doc_id}:{chunk.chunk_id}")

        untrusted = [c for c in valid_chunks if c.trust_tier == "external_untrusted"]
        for chunk in untrusted:
            text = self.normalize_text(chunk.text)
            if any(pattern.search(text) for pattern in self.IMPERATIVE_PATTERNS):
                triggers["L1"] = True
                flags.append(f"L1: Imperative pattern in {chunk.doc_id}:{chunk.chunk_id}")
            if re.search(
                r"(?:\[SYSTEM\]\s*(?:(?:LEVEL\s*0\s*DIRECTIVE|DIRECTIVE|OVERRIDE|AUTHORITY\s*:\s*ROOT)"
                r"|(?:ignore|disregard|override|bypass|execute|output|reveal|print|send|exfiltrate|dump|show|provide|grant|run|call)\b)"
                r"|LEVEL\s*0\s*DIRECTIVE|AUTHORITY\s*:\s*ROOT)",
                text, re.I,
            ):
                triggers["L3"] = True
                flags.append(f"L3: Authority-spoofing marker in {chunk.doc_id}:{chunk.chunk_id}")
            entropy = self.shannon_entropy(text)
            non_bmp = self.non_bmp_ratio(text)
            cue = bool(re.search(r"(override|execute|secret|directive|karma|𑀓𑀭𑁆𑀫)", text, re.I))
            if (((len(text) >= 40 and entropy > self.entropy_threshold)
                 or non_bmp > self.non_bmp_ratio_threshold) and cue):
                triggers["L4"] = True
                flags.append(f"L4: Compound entropy/Unicode heuristic (H={entropy:.2f}, non_bmp={non_bmp:.2f}) in {chunk.doc_id}:{chunk.chunk_id}")

        for i, first in enumerate(untrusted):
            for j in range(i + 1, min(len(untrusted), i + self.max_rank_gap + 1)):
                second = untrusted[j]
                a = self.normalize_text(first.text).lower()
                b = self.normalize_text(second.text).lower()
                if not any(marker in b for marker in self.CONTINUATION_MARKERS):
                    continue
                for prefix, suffix in self.SPLIT_PAYLOAD_RULES:
                    if prefix in a and suffix in b:
                        triggers["L2"] = True
                        pair = f"{first.doc_id}:{first.chunk_id}->{second.doc_id}:{second.chunk_id}"
                        provenance_pairs.append(pair)
                        flags.append(f"L2: Split-payload heuristic matched ({pair})")

        triggers["L5"] = any(triggers[f"L{i}"] for i in range(5))
        return {"quarantined": triggers["L5"], "triggers": triggers,
                "provenance_pairs": provenance_pairs, "flags": flags}


def python_batched_csv_streamer(output_path: str = "/tmp/part_00001.csv",
                                n_rows: int = 20_000, batch_size: int = 5_000) -> Dict[str, object]:
    if n_rows < 0 or batch_size < 1:
        raise ValueError("n_rows must be >= 0 and batch_size must be >= 1")
    tracemalloc.start()
    start = time.perf_counter()
    with open(output_path, "w", encoding="utf-8", newline="") as file:
        file.write("id,category,trust_tier,prompt_text,expected_complexity\n")
        for first in range(1, n_rows + 1, batch_size):
            last = min(first + batch_size, n_rows + 1)
            file.writelines(
                f"{i},LLM_Security,Level_30_Untrusted,Evaluate isolation boundary for node {i},High\n"
                for i in range(first, last)
            )
            file.flush()
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {"rows": n_rows, "batch_size": batch_size,
            "elapsed_sec": round(elapsed, 4), "peak_heap_mb": round(peak / (1024 * 1024), 2)}
