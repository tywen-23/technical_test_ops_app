import unittest
from datetime import date

from pace import calculate_pace


class PaceCalculationTests(unittest.TestCase):
    def test_current_month_projects_revenue_using_elapsed_days(self):
        result = calculate_pace(
            month="2026-09",
            mtd_revenue=4792.70,
            target=10000,
            today=date(2026, 9, 20),
        )

        self.assertEqual(result["elapsed_days"], 20)
        self.assertEqual(result["days_in_month"], 30)
        self.assertEqual(result["projected_revenue"], 7189.05)
        self.assertEqual(result["variance_amount"], -2810.95)
        self.assertEqual(result["variance_pct"], -28.1)
        self.assertEqual(result["status"], "at_risk")

    def test_past_month_uses_actual_revenue_as_projection(self):
        result = calculate_pace(
            month="2026-08",
            mtd_revenue=3100,
            target=3000,
            today=date(2026, 9, 20),
        )

        self.assertEqual(result["elapsed_days"], 31)
        self.assertEqual(result["projected_revenue"], 3100.0)
        self.assertEqual(result["status"], "on_track")

    def test_future_month_returns_na_without_dividing_by_zero(self):
        result = calculate_pace(
            month="2026-10",
            mtd_revenue=0,
            target=10000,
            today=date(2026, 9, 20),
        )

        self.assertEqual(result["elapsed_days"], 0)
        self.assertIsNone(result["projected_revenue"])
        self.assertIsNone(result["variance_amount"])
        self.assertIsNone(result["variance_pct"])
        self.assertEqual(result["status"], "n/a")

    def test_leap_year_uses_29_days_for_february(self):
        result = calculate_pace(
            month="2024-02",
            mtd_revenue=1450,
            target=2900,
            today=date(2024, 2, 15),
        )

        self.assertEqual(result["days_in_month"], 29)
        self.assertEqual(result["elapsed_days"], 15)

    def test_missing_target_returns_na(self):
        result = calculate_pace(
            month="2026-09",
            mtd_revenue=1000,
            target=None,
            today=date(2026, 9, 20),
        )

        self.assertIsNone(result["variance_amount"])
        self.assertIsNone(result["variance_pct"])
        self.assertEqual(result["status"], "n/a")


if __name__ == "__main__":
    unittest.main()