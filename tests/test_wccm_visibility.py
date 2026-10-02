"""Validate crawlable entity identity, Broward discovery and build normalization."""
import json
import os
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from tools import normalize_ai_mortgage_review_brand as brand

ROOT = Path(os.environ.get('WCCM_PUBLISH_DIR', Path(__file__).resolve().parents[1] / 'wccm-corporate'))
SLUG = 'fort-lauderdale-broward-mortgage'
DOMAIN = 'https://westcoastcapitalmortgage.com'
ENTITY = DOMAIN + '/#organization'


def schemas(name):
    return [json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', (ROOT / name).read_text(), re.S)]


class VisibilityTest(unittest.TestCase):
    def test_company_and_person_identifiers_stay_separate(self):
        for name in ('index.html', 'contact.html'):
            company = schemas(name)[0]
            self.assertEqual(company['@type'], 'FinancialService')
            self.assertEqual(company['@id'], ENTITY)
            self.assertEqual(company['name'], 'West Coast Capital Mortgage Inc.')
            self.assertNotIn('alternateName', company)
            self.assertEqual({i['value'] for i in company['identifier']}, {'2817729', '02440065'})
            self.assertEqual(company['telephone'], '+1-310-654-1577')
            self.assertEqual(company['address'], {'@type':'PostalAddress','streetAddress':'150 E Olive Ave, Unit 112','addressLocality':'Burbank','addressRegion':'CA','postalCode':'91502','addressCountry':'US'})
        person = schemas('index.html')[0]['founder']
        self.assertEqual(person['@type'], 'Person')
        self.assertEqual({i['value'] for i in person['identifier']}, {'2775380', '01385024'})

    def test_broward_is_linked_and_indexable(self):
        html = (ROOT / (SLUG + '.html')).read_text()
        self.assertIn('href="' + DOMAIN + '/' + SLUG + '"', html)
        self.assertIn('content="index,follow"', html)
        self.assertEqual(html.count('<h1>'), 1)
        self.assertIn('$832,750', html)
        self.assertIn('loan amount limit, not a purchase-price limit', html)
        self.assertIn('https://www.fhfa.gov/document/data/fullcountyloanlimitlist2026_hera-based_final_flat.pdf', html)
        self.assertIn('GTM-K2X3X454', html)
        self.assertIn('wccm_lead_submit', html)
        self.assertIn('underwriting approval', html)
        for name in ('florida.html','florida-dscr-loans.html','florida-bank-statement-loans.html','florida-jumbo-loans.html'):
            self.assertIn('href="/' + SLUG + '"', (ROOT / name).read_text())
        for name in ('sitemap.xml','growth-sitemap.xml'):
            urls = [node.text for node in ET.parse(ROOT / name).findall('.//{*}loc')]
            self.assertEqual(urls.count(DOMAIN + '/' + SLUG), 1)
        for link in re.findall(r'href="([^"]+)"', html):
            parsed = urlparse(link)
            if parsed.scheme or not parsed.path:
                continue
            path = ROOT / (parsed.path.lstrip('/') or 'index.html')
            self.assertTrue(path.is_file() or path.with_suffix('.html').is_file(), link)
        for name in ('index.html','contact.html',SLUG+'.html','ai-mortgage-review.html'):
            self.assertTrue(schemas(name))

    def test_normalizer_is_idempotent_and_preserves_tracking(self):
        fixture = '<a href="/existing-path">Ask Wallet AI</a><p>AI Strategy Advisor</p><script>window.dataLayer.push({event:"wccm_lead_submit"});</script>'
        with TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / 'index.html'
            page.write_text(fixture)
            original = brand.PUBLISH_DIR
            try:
                brand.PUBLISH_DIR = root
                brand.main()
                result = page.read_text()
                self.assertNotIn('Ask Wallet AI', result)
                self.assertNotIn('AI Strategy Advisor', result)
                self.assertIn('href="/existing-path"', result)
                self.assertIn('<script>window.dataLayer.push({event:"wccm_lead_submit"});</script>', result)
                brand.main()
                self.assertEqual(page.read_text(), result)
            finally:
                brand.PUBLISH_DIR = original


if __name__ == '__main__':
    unittest.main()
