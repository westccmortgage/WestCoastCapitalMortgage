"""Quick-lead pages must reserve the hero form's space before script.js runs.

script.js injects the hero lead form after first paint. Without the
.ql-pending reserve the hero grows on phones and pushes the page down
(Lighthouse mobile CLS was 0.28 on /dscr-loans in November 2026).
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1] / "wccm-corporate"


def quick_lead_paths():
    script = (ROOT / "script.js").read_text(encoding="utf-8")
    block = script.split("var QUICK_LEAD_FORMS={", 1)[1].split("\n  };", 1)[0]
    return re.findall(r"^    '(/[a-z0-9-]+)':\{", block, re.M)


class QuickLeadLayoutShiftTest(unittest.TestCase):
    def test_every_quick_lead_page_ships_with_reserve(self):
        paths = quick_lead_paths()
        self.assertGreaterEqual(len(paths), 5)
        for path in paths:
            with self.subTest(path=path):
                html = (ROOT / f"{path.lstrip('/')}.html").read_text(encoding="utf-8")
                hero = re.search(r'<section class="page-hero[^"]*"[^>]*>', html).group(0)
                self.assertIn("ql-pending", hero)
                self.assertIn("--ql-reserve:", hero)
                self.assertIn("--ql-reserve-sm:", hero)

    def test_script_releases_reserve_and_css_defines_it(self):
        script = (ROOT / "script.js").read_text(encoding="utf-8")
        css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("hero.classList.remove('ql-pending')", script)
        self.assertIn(".page-hero.ql-pending .page-hero-inner::after", css)
        self.assertIn("@keyframes ql-release", css)


if __name__ == "__main__":
    unittest.main()
