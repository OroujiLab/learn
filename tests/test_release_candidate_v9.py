"""Version 9 release-candidate asset and navigation smoke checks.

These are structural checks, not a substitute for subject-matter editorial review.
"""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
NEW_FIGURES=(
    "cutrun-cuttag-chip.svg",
    "peak-caller.svg",
    "gosling-workflow.svg",
    "chromatin-hero.svg",
)
CURRICULUM_FILES=(
    "local-to-hpc.qmd","hic-structures.qmd","hic-resolution-lab.qmd",
    "comparing-hic-samples.qmd","gosling-genome-tracks.qmd","hic-glossary.qmd",
    "atac-quality.qmd","chromatin-assays.qmd","cutrun-benchmarking.qmd",
    "hic-assays.qmd","organoid-epigenomics-design.qmd","enhancer-to-organoid.qmd",
    "biomarker-evidence.qmd",
)

class V9ReleaseCandidateTest(unittest.TestCase):
    def test_figures_are_parseable_original_svgs(self):
        for name in NEW_FIGURES:
            with self.subTest(name=name):
                r=ET.parse(ROOT / "assets" / name).getroot()
                self.assertTrue(r.tag.endswith("svg"))
                self.assertIn("viewBox", r.attrib)
                self.assertTrue(any(e.tag.endswith("title") for e in r.iter()))
                self.assertTrue(any(e.tag.endswith("desc") for e in r.iter()))

    def test_assay_mechanisms_explicit(self):
        src=(ROOT/"lessons"/"chromatin-assays.qmd").read_text()
        for name in ("CUT&RUN","CUT&Tag","MNase","Tn5","Ca²⁺","Mg²⁺"):
            self.assertIn(name,src)

    def test_directory_covers_all_lessons(self):
        directory=(ROOT/"lessons"/"index.qmd").read_text()
        for p in CURRICULUM_FILES:
            with self.subTest(lesson=p):
                self.assertTrue((ROOT/"lessons"/p).is_file())
                self.assertIn(p.removesuffix(".qmd")+".html",directory)
        for section in ("computational-genomics","experimental-epigenomics",
                        "cancer-biology-organoids","translational-oncology"):
            self.assertIn(section,directory)

    def test_website_navigation(self):
        cfg=(ROOT/"_quarto.yml").read_text()
        self.assertIn("page-navigation: true",cfg)
        self.assertIn("bread-crumbs: true",cfg)
        for section in ("01 · Computational","02 · Experimental","03 · Cancer","04 · Translational"):
            self.assertIn(section,cfg)

    def test_genome_visualization_fallback(self):
        src=(ROOT/"interactives"/"genome-track-studio.html").read_text()
        self.assertIn("gosling-workflow.svg",src)
        self.assertIn("id=\"gosling-figure\"",src)
        self.assertIn("gosling-figure",src)
        self.assertIn("gosling.min.js",src)

if __name__=="__main__":
    unittest.main()
