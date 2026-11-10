"""The Meta pixel is installed once, follows the lead event, respects GPC, and can be removed."""
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib
import json
import re
import subprocess
import unittest

from tools import install_wccm_gtm as gtm


ROOT = Path(__file__).resolve().parents[1] / "wccm-corporate"


def load_with_pixel(pixel_id):
    module = importlib.reload(gtm)
    module.META_PIXEL_HEAD_SNIPPET = module.META_PIXEL_HEAD_SNIPPET.replace(
        f"w.fbq('init','{module.META_PIXEL_ID}')", f"w.fbq('init','{pixel_id}')"
    )
    module.META_PIXEL_ID = pixel_id
    return module


class MetaPixelTest(unittest.TestCase):
    def tearDown(self):
        importlib.reload(gtm)

    def test_install_is_idempotent_and_removable(self):
        with TemporaryDirectory() as directory:
            page = Path(directory) / "bank-statement-loans.html"
            page.write_bytes((ROOT / "bank-statement-loans.html").read_bytes())

            module = load_with_pixel("1234567890")
            for _ in range(2):
                module.inject(page)
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count(module.META_BLOCK_START), 1)
            self.assertIn("w.fbq('init','1234567890')", text)
            self.assertLess(text.find(module.ADS_BLOCK_END), text.find(module.META_BLOCK_START))
            module.verify_critical(page)

            module = load_with_pixel("")
            module.inject(page)
            text = page.read_text(encoding="utf-8")
            self.assertNotIn(module.META_BLOCK_START, text)
            self.assertNotIn("fbevents.js", text)

    def test_no_pixel_id_leaves_page_untouched(self):
        with TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_bytes((ROOT / "index.html").read_bytes())
            module = load_with_pixel("")
            module.inject(page)
            before = page.read_text(encoding="utf-8")
            module.inject(page)
            self.assertEqual(before, page.read_text(encoding="utf-8"))
            self.assertNotIn("fbevents.js", before)

    def test_lead_is_sent_once_and_nothing_loads_under_gpc(self):
        module = load_with_pixel("1234567890")
        block = module.META_PIXEL_HEAD_SNIPPET.split(module.META_BLOCK_START, 1)[1].split(module.META_BLOCK_END, 1)[0]
        script = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", block, re.S)[0]
        harness = """
(function() {  // a function scope: Node has its own global `navigator`
var scan = null, loaded = [];
var setInterval = function(fn) { scan = fn; };
var navigator = { globalPrivacyControl: %s };
var parent = { insertBefore: function(js) { loaded.push(js.src); } };
var document = {
  createElement: function() { return {}; },
  getElementsByTagName: function() { return [{ parentNode: parent }]; }
};
var window = { dataLayer: [] };
"""
        tail = """
var calls = window.fbq ? Array.prototype.map.call(window.fbq.queue, function(a) { return Array.prototype.slice.call(a); }) : [];
if (scan) {
  window.dataLayer.push({event:'wccm_lead_submit', lead_event_id:'lead_1', email:'a@example.com'});
  window.dataLayer.push({event:'wccm_lead_submit', lead_event_id:'lead_1'});
  window.dataLayer.push({event:'wccm_phone_click'});
  scan(); scan();
  calls = Array.prototype.map.call(window.fbq.queue, function(a) { return Array.prototype.slice.call(a); });
}
console.log(JSON.stringify({loaded: loaded, calls: calls}));
})();
"""
        def run(gpc):
            done = subprocess.run(["node", "-e", harness % gpc + script + tail],
                                  text=True, capture_output=True, check=False)
            self.assertEqual(done.returncode, 0, done.stderr)
            return json.loads(done.stdout)

        normal = run("false")
        self.assertEqual(normal["loaded"], ["https://connect.facebook.net/en_US/fbevents.js"])
        self.assertEqual(normal["calls"], [
            ["init", "1234567890"],
            ["track", "PageView"],
            ["track", "Lead", {}, {"eventID": "lead_1"}],
        ])
        private = run("true")
        self.assertEqual(private, {"loaded": [], "calls": []})


if __name__ == "__main__":
    unittest.main()
