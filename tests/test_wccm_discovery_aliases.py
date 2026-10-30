"""Protect high-intent WCCM canonical discovery aliases in Netlify redirects."""
from pathlib import Path
import unittest

REDIRECTS = Path(__file__).resolve().parents[1] / "wccm-corporate" / "_redirects"
PUBLISH = REDIRECTS.parent

class MortgageDiscoveryAliasTests(unittest.TestCase):
    def test_california_and_program_aliases_reach_mortgage_pages(self):
        lines = [line.strip() for line in REDIRECTS.read_text(encoding="utf-8").splitlines()
                 if line.strip() and not line.lstrip().startswith("#")]
        expected = {
            "/california": "/california-mortgage-locations",
            "/california.html": "/california-mortgage-locations",
            "/programs": "/loans",
            "/programs.html": "/loans",
        }
        fallback = lines.index("/* /404.html 404")
        for source, dest in expected.items():
            rule = f"{source} {dest} 301!"
            self.assertEqual(lines.count(rule), 1, rule)
            self.assertLess(lines.index(rule), fallback)
            self.assertTrue((PUBLISH / (dest[1:] + ".html")).is_file(), dest)

if __name__ == "__main__":
    unittest.main()
