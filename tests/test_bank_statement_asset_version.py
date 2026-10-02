"""The build must not roll the Bank Statement disclosure assets back to cache-stale URLs."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools import install_wccm_ads_readiness as readiness
from tools import install_wccm_gtm as gtm


ROOT = Path(__file__).resolve().parents[1] / "wccm-corporate"


class BankStatementAssetVersionTest(unittest.TestCase):
    def test_build_scripts_preserve_narrow_version(self):
        with TemporaryDirectory() as directory:
            publish = Path(directory)
            for name in readiness.PAGE_FORMS:
                (publish / name).parent.mkdir(parents=True, exist_ok=True)
                (publish / name).write_bytes((ROOT / name).read_bytes())
            original_publish = readiness.PUBLISH_DIR
            try:
                readiness.PUBLISH_DIR = publish
                for _ in range(2):
                    for name in ("bank-statement-loans.html", "self-employed-borrowers.html"):
                        gtm.inject(publish / name)
                    readiness.main()
                    bank = (publish / "bank-statement-loans.html").read_text()
                    other = (publish / "self-employed-borrowers.html").read_text()
                    self.assertIn('styles.css?v=20261002-bank-disclosure', bank)
                    self.assertIn('script.js?v=20261002-bank-disclosure', bank)
                    self.assertIn('script.js?v=20261001-highlights', other)
            finally:
                readiness.PUBLISH_DIR = original_publish


if __name__ == "__main__":
    unittest.main()
