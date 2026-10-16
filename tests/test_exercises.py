import sys
import unittest
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "exercises/local-to-hpc"))
sys.path.insert(0, str(ROOT / "exercises/cutrun-peak-calling"))
from fastq_summary import summarize
from compare_peaks import compare

class TeachingExerciseTests(unittest.TestCase):
    def test_fastq_summary(self):
        got = summarize(ROOT / "exercises/local-to-hpc/toy_reads.fastq")
        self.assertEqual(got["reads"], 4)
        self.assertEqual(got["bases"], 48)
        self.assertAlmostEqual(got["mean_length"], 12)
        self.assertAlmostEqual(got["ambiguous_fraction"], 2/48)
    def test_invalid_fastq(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.fastq"
            p.write_text("@test\nACGT\n+\nIII\n")
            with self.assertRaises(ValueError):
                summarize(p)
    def test_bed_overlap(self):
        a = ROOT / "exercises/cutrun-peak-calling/peaks_A.bed"
        b = ROOT / "exercises/cutrun-peak-calling/peaks_B.bed"
        result = compare(a, b)
        self.assertEqual(result["raw_intervals_a"], 3)
        self.assertEqual(result["raw_intervals_b"], 3)
        self.assertTrue(0 < result["jaccard_bp"] < 1)

if __name__ == "__main__":
    unittest.main()
