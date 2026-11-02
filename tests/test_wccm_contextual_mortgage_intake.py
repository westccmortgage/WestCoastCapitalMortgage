"""Protect high-intent WCCM callback paths without changing lending terms."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "wccm-corporate"


class ContextualMortgageIntakeTest(unittest.TestCase):
    def test_contact_form_preserves_known_scenario_and_source_fields(self):
        html = (ROOT / "contact.html").read_text(encoding="utf-8")
        self.assertIn('name="contact" netlify', html)
        self.assertIn('name="program_interest"', html)
        for field in ("gclid", "gbraid", "landing_page", "referrer", "conversion_page"):
            self.assertIn('name="' + field + '"', html)
        self.assertIn("'florida-condo':{", html)
        self.assertIn("program:'Florida / Condo'", html)
        self.assertIn("'foreign-national':{", html)
        self.assertIn("program:'Foreign National'", html)
        self.assertIn("Object.prototype.hasOwnProperty.call(intake,scenario)", html)
        self.assertIn("if(scenario!=='second-opinion')return", html)
        self.assertIn("interest.value='Mortgage Second Opinion'", html)

    def test_florida_condo_has_short_first_step_and_full_application(self):
        html = (ROOT / "florida-condo-financing.html").read_text(encoding="utf-8")
        self.assertIn('href="contact.html?scenario=florida-condo">Request a Florida Condo Review</a>', html)
        self.assertIn('href="/apply" data-cta="preapproval">Start Full Application</a>', html)
        self.assertIn("NMLS #2817729", html)

    def test_foreign_national_has_short_first_step_and_full_application(self):
        html = (ROOT / "foreign-national-loans.html").read_text(encoding="utf-8")
        self.assertIn('href="contact.html?scenario=foreign-national">Request a Foreign-National Mortgage Review</a>', html)
        self.assertIn('href="apply.html">Start Full Application</a>', html)
        self.assertIn("NMLS #2817729", html)


if __name__ == "__main__":
    unittest.main()
