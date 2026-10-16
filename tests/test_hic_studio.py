"""Lightweight, standard-library validation for the Hi-C teaching studio."""
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class StudioAssetTests(unittest.TestCase):
    def test_original_svg_figures_parse(self):
        for name in (
            "hic-structures-master.svg",
            "hic-interpretation-workflow.svg",
            "hic-comparison-workflow.svg",
            "hic-assay-family.svg",
        ):
            with self.subTest(name=name):
                root = ET.parse(ROOT / "assets" / name).getroot()
                self.assertTrue(root.tag.endswith("svg"))
                self.assertIn("viewBox", root.attrib)
                self.assertTrue(any(x.tag.endswith("title") for x in root.iter()))

    def test_3d_genome_embedded_lessons_exist(self):
        paths = [
            ROOT / "lessons" / "hic-structures.qmd",
            ROOT / "lessons" / "comparing-hic-samples.qmd",
        ]
        urls = []
        for p in paths:
            src = p.read_text()
            urls += re.findall(r'<iframe[^>]*src="([^"]+)"', src)
        self.assertEqual(len(urls), 2)
        for url in urls:
            self.assertTrue((ROOT / "lessons" / url).resolve().is_file())

    def test_glossary_and_methods_have_references(self):
        for name in ["hic-assays.qmd", "hic-glossary.qmd"]:
            with self.subTest(name=name):
                text = (ROOT / "lessons" / name).read_text()
                self.assertIn("10.1016/j.csbj.2024.12.018", text)
                self.assertNotIn("HiC-ECC benchmark results", text)

if __name__ == "__main__":
    unittest.main()
