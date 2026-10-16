#!/usr/bin/env python3
"""Compare toy BED interval sets; this is NOT an assay accuracy or FDR estimator."""
from collections import defaultdict
from pathlib import Path
import sys
import json

def read_bed(path):
    intervals = defaultdict(list)
    with Path(path).open() as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip() or line.startswith("#"):
                continue
            fields = line.split()
            if len(fields) < 3:
                raise ValueError(f"{path}:{lineno} needs at least 3 BED columns")
            chrom, start, end = fields[:3]
            start, end = int(start), int(end)
            if start < 0 or end <= start:
                raise ValueError(f"{path}:{lineno} has invalid half-open interval")
            intervals[chrom].append((start, end))
    return intervals

def merge_intervals(intervals):
    out = {}
    for chrom, values in intervals.items():
        result = []
        for start, end in sorted(values):
            if result and start <= result[-1][1]:
                result[-1] = (result[-1][0], max(end, result[-1][1]))
            else:
                result.append((start, end))
        out[chrom] = result
    return out

def coverage(intervals):
    return sum(end - start for seq in intervals.values() for start, end in seq)

def intersection_bp(a, b):
    n = 0
    for chrom in set(a) & set(b):
        aa, bb = a[chrom], b[chrom]
        i = j = 0
        while i < len(aa) and j < len(bb):
            n += max(0, min(aa[i][1], bb[j][1]) - max(aa[i][0], bb[j][0]))
            if aa[i][1] < bb[j][1]:
                i += 1
            else:
                j += 1
    return n

def compare(path_a, path_b):
    raw_a, raw_b = read_bed(path_a), read_bed(path_b)
    a, b = merge_intervals(raw_a), merge_intervals(raw_b)
    ca, cb = coverage(a), coverage(b)
    inter = intersection_bp(a, b)
    union = ca + cb - inter
    return {
        "raw_intervals_a": sum(map(len, raw_a.values())),
        "raw_intervals_b": sum(map(len, raw_b.values())),
        "covered_bp_a": ca,
        "covered_bp_b": cb,
        "intersection_bp": inter,
        "union_bp": union,
        "jaccard_bp": inter / union if union else 1.0
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 compare_peaks.py A.bed B.bed")
    try:
        print(json.dumps(compare(sys.argv[1], sys.argv[2]), indent=2))
    except (OSError, ValueError) as exc:
        sys.exit(f"Input error: {exc}")
