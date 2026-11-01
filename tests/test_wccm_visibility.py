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

    def test_shared_mortgage_company_entity_graph(self):
        self.assertEqual(schemas('about.html')[0]['@id'], ENTITY)
        self.assertEqual(schemas('florida.html')[0]['about']['provider']['@id'], ENTITY)
        self.assertEqual(schemas('mortgage-second-opinion.html')[0]['provider']['@id'], ENTITY)
        self.assertEqual(schemas('index.html')[0]['@id'], ENTITY)
        self.assertEqual(schemas('contact.html')[0]['@id'], ENTITY)

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

    def test_florida_guides_are_visible_and_high_intent_paths_are_local(self):
        css = (ROOT / 'styles.css').read_text()
        page = (ROOT / 'florida.html').read_text()
        # The homepage keeps its short funnel, but the Florida page must show
        # its county guides, lending scenarios, FAQ and consumer resources.
        self.assertIn('<body class="florida-mortgage-page">', page)
        self.assertIn('body:has(.mortgage-compact-hero):not(.florida-mortgage-page) > section', css)
        self.assertNotIn('body:has(.mortgage-compact-hero) > section:not', css)
        self.assertIn('href="florida-dscr-loans.html"', page)
        self.assertIn('href="/mortgage-second-opinion"', page)
        self.assertIn('South Florida mortgage guides', page)
        self.assertIn('Florida regulatory information', page)

    def test_high_intent_forms_explain_full_dollar_amount(self):
        script = (ROOT / 'script.js').read_text()
        self.assertEqual(script.count("hint:'Enter the full amount in dollars (e.g., 2000000 for $2 million).'"), 2)
        self.assertIn("control.setAttribute('aria-describedby',hint.id);", script)

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
