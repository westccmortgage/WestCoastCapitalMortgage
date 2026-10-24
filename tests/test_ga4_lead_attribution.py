"""GA4 attribution must survive the WCCM production normalization workflow."""
from pathlib import Path
from tempfile import TemporaryDirectory
import re
import subprocess
import unittest

from tools import install_wccm_gtm as gtm


ROOT = Path(__file__).resolve().parents[1] / "wccm-corporate"


class GA4LeadAttributionTest(unittest.TestCase):
    def test_accepted_lead_context_is_safe_consistent_and_idempotent(self):
        for name in ("contact.html", "index.html", "bank-statement-loans.html", "dscr-loans.html"):
            with self.subTest(page=name), TemporaryDirectory() as directory:
                page = Path(directory) / name
                page.write_bytes((ROOT / name).read_bytes())

                # The installer is the source of truth, regardless of any direct
                # edits to the generated Google Ads / GA4 block in a page.
                gtm.inject(page)
                html = page.read_text(encoding="utf-8")
                self.assertEqual(html.count("window.gtag('event','generate_lead'"), 1)
                self.assertIn("'form_name':safeForm", html)
                self.assertIn("'program_interest':safeProgram", html)
                self.assertIn("'page_path':safePath", html)
                self.assertIn("'Mortgage Second Opinion'", html)
                self.assertIn("'Bank Statement / Self-Employed'", html)
                self.assertIn("new RegExp('^[a-z0-9-]+$')", html)
                self.assertIn("new RegExp('^[/a-z0-9-]+$','i')", html)
                self.assertLess(html.index("window.gtag('event','conversion'"),
                                html.index("window.gtag('event','generate_lead'"))

                ads_block = html.split(gtm.ADS_BLOCK_START, 1)[1].split(gtm.ADS_BLOCK_END, 1)[0]
                scripts = re.findall(r"<script(?:\\s[^>]*)?>(.*?)</script>", ads_block, re.S)
                self.assertEqual(len(scripts), 1)
                checked = subprocess.run(["node", "--check"], input=scripts[0],
                                         text=True, capture_output=True, check=False)
                self.assertEqual(checked.returncode, 0, checked.stderr)

                gtm.inject(page)
                self.assertEqual(html, page.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
