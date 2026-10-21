"""The OpenAI Ads pixel is installed once, follows the lead event, and can be removed."""
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib
import unittest

from tools import install_wccm_gtm as gtm


ROOT = Path(__file__).resolve().parents[1] / "wccm-corporate"


def load_with_pixel(pixel_id):
    module = importlib.reload(gtm)
    module.OPENAI_PIXEL_HEAD_SNIPPET = module.OPENAI_PIXEL_HEAD_SNIPPET.replace(
        f'pixelId:"{module.OPENAI_PIXEL_ID}"', f'pixelId:"{pixel_id}"'
    )
    module.OPENAI_PIXEL_ID = pixel_id
    return module


class OpenAiPixelTest(unittest.TestCase):
    def tearDown(self):
        importlib.reload(gtm)

    def test_install_is_idempotent_and_removable(self):
        with TemporaryDirectory() as directory:
            page = Path(directory) / "bank-statement-loans.html"
            page.write_bytes((ROOT / "bank-statement-loans.html").read_bytes())

            module = load_with_pixel("px_test123")
            for _ in range(2):
                module.inject(page)
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count(module.OPENAI_BLOCK_START), 1)
            self.assertIn('pixelId:"px_test123"', text)
            self.assertIn('"lead_created"', text)
            self.assertIn("wccm_lead_submit", text)
            self.assertLess(text.find(module.ADS_BLOCK_END), text.find(module.OPENAI_BLOCK_START))
            module.verify_critical(page)

            module = load_with_pixel("")
            module.inject(page)
            text = page.read_text(encoding="utf-8")
            self.assertNotIn(module.OPENAI_BLOCK_START, text)
            self.assertNotIn("oaiq", text)

    def test_no_pixel_id_leaves_page_untouched(self):
        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_bytes((ROOT / "index.html").read_bytes())
            module = load_with_pixel("")
            module.inject(page)
            before = page.read_text(encoding="utf-8")
            module.inject(page)
            self.assertEqual(before, page.read_text(encoding="utf-8"))
            self.assertNotIn("oaiq", before)


if __name__ == "__main__":
    unittest.main()
