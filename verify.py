#!/usr/bin/env python3
"""Verify a forecast ledger's hash chain. Standard library only; copied into the
public ledger repository so anyone can check it without our code.

Usage: python verify.py forecasts.jsonl [resolutions.jsonl ...]

Each record's record_hash must equal the SHA-256 of its canonical JSON (keys
sorted, compact separators, UTF-8) with record_hash removed, and its prev_hash
must equal the previous record's record_hash (64 zeros for the first record).
Timestamp proofs for each batch are in batches/*.ots; check them with
`ots verify batches/<file>.txt.ots` (https://opentimestamps.org).
"""

import hashlib
import json
import sys

GENESIS = "0" * 64


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def verify(path):
    prev = GENESIS
    n = 0
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate((l for l in f if l.strip()), 1):
            r = json.loads(line)
            if r.get("prev_hash") != prev:
                raise SystemExit(f"{path}: record {n}: prev_hash does not chain")
            body = {k: v for k, v in r.items() if k != "record_hash"}
            if hashlib.sha256(canonical(body)).hexdigest() != r.get("record_hash"):
                raise SystemExit(f"{path}: record {n}: record_hash does not match contents")
            prev = r["record_hash"]
    return n


if __name__ == "__main__":
    for p in sys.argv[1:] or ["forecasts.jsonl"]:
        print(f"{p}: {verify(p)} records, hash chain OK")
