#!/usr/bin/env python3
"""Philoprompts-v1.0 tokenizer study: GPT-2 vs cl100k_base vs o200k_base.

Pure-stdlib implementation (no third-party packages). On first run it
downloads the corpus and official tokenizer artifacts into ./data and writes
per-block CSV files and aggregate JSON into ./results.

Verification: canonical token IDs (GPT-2 'Hello world' -> [15496, 995];
cl100k 'hello world' -> [15339, 1917]), byte round-trip integrity, and the
4-token decomposition of every tested ancient non-BMP character.
"""
import base64, json, re, statistics, urllib.request, csv
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
RESULTS = HERE / "results"

URLS = {
    "philoprompts.jsonl": "https://huggingface.co/datasets/Dr-Metal/philoprompts-v1/resolve/main/philoprompts.jsonl",
    "gpt2_vocab.json": "https://huggingface.co/gpt2/resolve/main/vocab.json",
    "gpt2_merges.txt": "https://huggingface.co/gpt2/resolve/main/merges.txt",
    "cl100k_base.tiktoken": "https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken",
    "o200k_base.tiktoken": "https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken",
}

def fetch():
    DATA.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    for name, url in URLS.items():
        p = DATA / name
        if not p.exists():
            print("downloading", name)
            req = urllib.request.Request(url, headers={"User-Agent": "philoprompts-tokenizer-study/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(p, "wb") as f:
                f.write(r.read())

@lru_cache()
def bytes_to_unicode():
    bs = list(range(ord("!"), ord("~") + 1)) + list(range(0xA1, 0xAC + 1)) + list(range(0xAE, 0xFF + 1))
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b); cs.append(256 + n); n += 1
    return dict(zip(bs, [chr(c) for c in cs]))

class GPT2BPE:
    def __init__(self):
        self.encoder = json.loads((DATA / "gpt2_vocab.json").read_text(encoding="utf-8"))
        merges = [tuple(l.split()) for l in (DATA / "gpt2_merges.txt").read_text(encoding="utf-8").split("\n")[1:] if l]
        self.bpe_ranks = {m: i for i, m in enumerate(merges)}
        self.byte_encoder = bytes_to_unicode()
        self.byte_decoder = {v: k for k, v in self.byte_encoder.items()}
        self.cache = {}
        self.pat = re.compile(r"'s|'t|'re|'ve|'m|'ll|'d| ?[^\W\d_]+| ?\d+| ?[^\s\w]+|\s+(?!\S)|\s+")

    def bpe(self, token):
        if token in self.cache:
            return self.cache[token].copy()
        word = tuple(token)
        pairs = set(zip(word[:-1], word[1:]))
        if not pairs:
            return [token]
        while True:
            bigram = min(pairs, key=lambda p: self.bpe_ranks.get(p, 1e18))
            if bigram not in self.bpe_ranks:
                break
            first, second = bigram
            new_word, i = [], 0
            while i < len(word):
                try:
                    j = word.index(first, i)
                    new_word.extend(word[i:j]); i = j
                except ValueError:
                    new_word.extend(word[i:]); break
                if word[i] == first and i < len(word) - 1 and word[i + 1] == second:
                    new_word.append(first + second); i += 2
                else:
                    new_word.append(word[i]); i += 1
            word = tuple(new_word)
            if len(word) == 1:
                break
            pairs = set(zip(word[:-1], word[1:]))
        self.cache[token] = list(word)
        return list(word)

    def encode(self, text):
        ids, pieces = [], []
        for m in self.pat.finditer(text):
            t = "".join(self.byte_encoder[b] for b in m.group(0).encode("utf-8"))
            for sub in self.bpe(t):
                i = self.encoder.get(sub)
                if i is None:
                    continue
                ids.append(i); pieces.append(bytes(self.byte_decoder[c] for c in sub))
        return ids, pieces

class RankBPE:
    def __init__(self, name, pat):
        self.ranks = {}
        for line in (DATA / (name + ".tiktoken")).read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            token_b64, _, rank_b64 = line.partition(" ")
            tok = base64.b64decode(token_b64.strip()) if token_b64.strip() else b""
            self.ranks.setdefault(tok, int(rank_b64))
        self.pat = re.compile(pat)

    def _merge(self, piece):
        parts = [piece[i:i+1] for i in range(len(piece))]
        while True:
            best_rank, best_i = None, None
            for i in range(len(parts) - 1):
                r = self.ranks.get(parts[i] + parts[i+1])
                if r is not None and (best_rank is None or r < best_rank):
                    best_rank, best_i = r, i
            if best_rank is None:
                return parts
            parts = parts[:best_i] + [parts[best_i] + parts[best_i+1]] + parts[best_i+2:]

    def encode(self, text):
        ids, pieces = [], []
        for m in self.pat.finditer(text):
            for p in self._merge(m.group(0).encode("utf-8")):
                r = self.ranks.get(p)
                if r is not None:
                    ids.append(r); pieces.append(p)
        return ids, pieces

L, N = r"[^\W\d_]", r"\d"
PAT_CL = (r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\w]?" + L + "+|" + N + "{1,3}"
          + r"| ?[^\s\w]+[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+")
PAT_O = ("[^\r\n\w]??" + L + "+|" + N + "{1,3}"
         + r"| ?[^\s\w]+[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+")

fetch()
TOKS = {"gpt2": GPT2BPE(), "cl100k_base": RankBPE("cl100k_base", PAT_CL), "o200k_base": RankBPE("o200k_base", PAT_O)}

def verify():
    checks = []
    ids, _ = TOKS["gpt2"].encode("Hello world")
    ids2, _ = TOKS["gpt2"].encode("hello world")
    ids3, _ = TOKS["cl100k_base"].encode("hello world")
    checks += [ids == [15496, 995], ids2 == [31373, 995], ids3 == [15339, 1917]]
    fa_sample = "\u062e\u0646\u062f\u06cc\u062f\u06cc"
    for s in ["Hello world", "hello world", fa_sample + " \U00012300\U00012301", "\U00012300"]:
        for name, tok in TOKS.items():
            i5, pieces = tok.encode(s)
            checks.append(b"".join(pieces) == s.encode("utf-8") and len(i5) == len(pieces))
    for name, tok in TOKS.items():
        i6, p6 = tok.encode("\U00012300")
        checks.append(len(i6) == 4 and all(len(p) == 1 for p in p6))
    assert all(checks), "verification failed"
    print("all verification checks passed")

verify()

RANGES = [
    ("Brahmi", 0x11000, 0x1107F), ("Cuneiform", 0x12000, 0x124FF),
    ("OldPersian", 0x103A0, 0x103DF), ("Avestan", 0x10B00, 0x10B3F),
    ("Geez", 0x13000, 0x1342F), ("InscriptionalParthian", 0x10B60, 0x10B7F),
    ("OldTurkic", 0x10C00, 0x10C4F), ("Arabic", 0x600, 0x6FF),
    ("Kana", 0x3040, 0x30FF), ("CJK", 0x4E00, 0x9FFF), ("CJK", 0x20000, 0x2FFFF),
    ("Greek", 0x370, 0x3FF), ("Cyrillic", 0x400, 0x4FF),
    ("Devanagari", 0x900, 0x97F), ("Balochi/Latin", 0x100, 0x24F),
    ("None-BMP-other", 0x10000, 0x2FFFF),
]

def detect_script(text):
    counts = {}
    for ch in text:
        o = ord(ch)
        if 0x41 <= o <= 0x7A or 0x30 <= o <= 0x39:
            continue
        for name, lo, hi in RANGES:
            if lo <= o <= hi:
                counts[name] = counts.get(name, 0) + 1
                break
    if not counts:
        return "PureASCII"
    cands = {k: v for k, v in counts.items() if k != "Arabic"}
    return max(cands, key=cands.get) if cands else "Persian(Arabic)"

rows = [json.loads(l) for l in open(DATA / "philoprompts.jsonl", encoding="utf-8") if l.strip()]
per_block = []
for r in rows:
    if r.get("status") == "INTENTIONAL_GAP":
        continue
    text = r.get("prompt") or r.get("input_text") or ""
    script = detect_script(text)
    nb = len(text.encode("utf-8"))
    rec = {"block_id": r.get("block_id"), "detected_script": script,
           "n_chars": len(text), "n_bytes": nb,
           "n_nonbmp": sum(1 for ch in text if ord(ch) > 0xFFFF)}
    for name, tok in TOKS.items():
        ids, pieces = tok.encode(text)
        ncont = sum(1 for p in pieces if len(p) == 1 and 0x80 <= p[0] <= 0xBF)
        rec[name + "_tokens"] = len(ids)
        rec[name + "_bpt"] = round(nb / max(len(ids), 1), 3)
        rec[name + "_fallback"] = round(ncont / max(len(ids), 1), 4)
    per_block.append(rec)

with open(RESULTS / "per_block_detected.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(per_block[0].keys()))
    w.writeheader(); w.writerows(per_block)

table = []
for s in sorted({r["detected_script"] for r in per_block}):
    sub = [r for r in per_block if r["detected_script"] == s]
    row = {"script": s, "blocks": len(sub),
           "nonbmp_blocks": sum(1 for r in sub if r["n_nonbmp"] > 0)}
    for name in TOKS:
        row[name + "_bpt_mean"] = round(statistics.mean(r[name + "_bpt"] for r in sub), 3)
        row[name + "_fb_mean"] = round(statistics.mean(r[name + "_fallback"] for r in sub), 4)
    table.append(row)
table.sort(key=lambda x: -x["blocks"])
(RESULTS / "by_detected_script.json").write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

overall = {}
for name in TOKS:
    nt = sum(r[name + "_tokens"] for r in per_block)
    n_bytes = sum(r["n_bytes"] for r in per_block)
    ncont = sum(r[name + "_fallback"] * r[name + "_tokens"] for r in per_block)
    nc = sum(r["n_chars"] for r in per_block)
    nnb = sum(r["n_nonbmp"] for r in per_block)
    overall[name] = {"blocks": len(per_block), "tokens": nt, "bytes": n_bytes,
                     "bytes_per_token": round(n_bytes / max(nt, 1), 3),
                     "chars_per_token": round(nc / max(nt, 1), 3),
                     "nonbmp_char_share": round(nnb / max(nc, 1), 4),
                     "byte_fallback_ratio": round(ncont / max(nt, 1), 4)}
(RESULTS / "overall.json").write_text(json.dumps(overall, indent=2) + "\n", encoding="utf-8")

sample_chars = {"Brahmi (U+11000)": "\U00011000", "Cuneiform (U+12000)": "\U00012300",
                "OldPersian (U+103A0)": "\U000103A0", "Avestan (U+10B00)": "\U00010B00",
                "Geez (U+13000)": "\U00013000", "CJK Ext-B (U+20000)": "\U00020000"}
cost = {k: {name: len(tok.encode(ch)[0]) for name, tok in TOKS.items()} for k, ch in sample_chars.items()}
(RESULTS / "single_char_cost.json").write_text(json.dumps(cost, indent=2) + "\n", encoding="utf-8")
print("done:", len(per_block), "blocks analyzed")
