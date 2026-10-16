#!/usr/bin/env python3
"""Minimal Phred+33 FASTQ summary for SYNTHETIC classroom reads, not production QC."""
import json
import sys
from pathlib import Path

def summarize(path):
    reads = bases = gc = ambiguous = quality_total = 0
    with Path(path).open(encoding="utf-8") as f:
        while True:
            h = f.readline()
            if not h:
                break
            seq, sep, qual = f.readline(), f.readline(), f.readline()
            if not (seq and sep and qual):
                raise ValueError("Incomplete FASTQ record")
            h, seq, sep, qual = h.rstrip("\r\n"), seq.rstrip("\r\n"), sep.rstrip("\r\n"), qual.rstrip("\r\n")
            if not h.startswith("@") or not sep.startswith("+"):
                raise ValueError("Invalid FASTQ header or separator")
            if len(seq) != len(qual):
                raise ValueError("Sequence and quality lengths differ")
            if not all(33 <= ord(ch) <= 126 for ch in qual):
                raise ValueError("Quality characters outside printable Phred+33 ASCII range")
            reads += 1
            bases += len(seq)
            gc += sum(ch.upper() in "GC" for ch in seq)
            ambiguous += sum(ch.upper() not in "ACGT" for ch in seq)
            quality_total += sum(ord(ch) - 33 for ch in qual)
    return {
        "reads": reads,
        "bases": bases,
        "mean_length": bases / reads if reads else 0,
        "gc_fraction": gc / bases if bases else 0,
        "ambiguous_fraction": ambiguous / bases if bases else 0,
        "mean_phred": quality_total / bases if bases else 0,
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 fastq_summary.py input.fastq")
    try:
        print(json.dumps(summarize(sys.argv[1]), indent=2))
    except (OSError, ValueError) as exc:
        sys.exit(f"Input error: {exc}")
