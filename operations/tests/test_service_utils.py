from operations.services import services_utils
from django.test import TestCase

class RiskProfileTest(TestCase):

    def test_high_risk(self):
        result = services_utils.determine_risk_profile(
            critical_alerts=12,
            total_alerts=30,
        )

        self.assertEqual(
            result,
            "High Risk",
        )