"""Protect high-intent denial/second-opinion paths on core WCCM pages."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / "wccm-corporate"


class SecondOpinionRoutesTest(unittest.TestCase):
    def test_denial_routes_exist_on_program_pages(self):
        scenarios = {
            "bank-statement-loans.html": "Was a mortgage declined because self-employed income was calculated too low?",
            "non-qm-loans.html": "Was your mortgage denied because standard income documentation did not fit?",
            "jumbo-loans.html": "Did a jumbo mortgage get declined or delayed?",
        }
        target = ROOT / "mortgage-second-opinion.html"
        self.assertTrue(target.is_file())
        for filename, question in scenarios.items():
            with self.subTest(page=filename):
                html = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn(question, html)
                self.assertIn('href="mortgage-second-opinion.html"', html)
                self.assertIn("NMLS #2817729", html)
                self.assertIn("does not guarantee approval", html)


if __name__ == "__main__":
    unittest.main()
