import unittest
from decimal import Decimal

from db import _line_net, summary


class FakeConnection:
    def __init__(self, rows, target=None):
        self.rows = rows
        self.target = target

    async def fetch(self, query, *params):
        return self.rows

    async def fetchval(self, query, *params):
        return self.target


class RevenueCalculationTests(unittest.IsolatedAsyncioTestCase):
    def test_line_net_applies_percentage_discount(self):
        sale = {
            "quantity": 2,
            "unit_price": Decimal("100.00"),
            "discount_pct": Decimal("10"),
        }

        self.assertEqual(_line_net(sale), 180.0)

    async def test_summary_calculates_completed_sales_correctly(self):
        rows = [
            {
                "category": "Cafe",
                "channel": "online",
                "quantity": 2,
                "unit_price": Decimal("100.00"),
                "discount_pct": Decimal("10"),
                "status": "completed",
            },
            {
                "category": "Cafe",
                "channel": "in_store",
                "quantity": 1,
                "unit_price": Decimal("50.00"),
                "discount_pct": Decimal("0"),
                "status": "completed",
            },
            {
                "category": "Coaching",
                "channel": "online",
                "quantity": 1,
                "unit_price": Decimal("100.00"),
                "discount_pct": Decimal("20"),
                "status": "completed",
            },
            {
                "category": "Pro Shop",
                "channel": "in_store",
                "quantity": 1,
                "unit_price": Decimal("999.00"),
                "discount_pct": Decimal("0"),
                "status": "refunded",
            },
        ]

        result = await summary(
            FakeConnection(rows, Decimal("1000.00")),
            month="2026-09",
        )

        self.assertEqual(result["total_revenue"], 310.0)
        self.assertEqual(result["order_count"], 3)
        self.assertEqual(result["avg_order_value"], 103.33)
        self.assertEqual(result["attainment_pct"], 31.0)

        categories = {
            item["category"]: item["revenue"]
            for item in result["by_category"]
        }
        self.assertEqual(categories, {"Cafe": 230.0, "Coaching": 80.0})

        channels = {
            item["channel"]: item["revenue"]
            for item in result["by_channel"]
        }
        self.assertEqual(channels, {"online": 260.0, "in_store": 50.0})

    async def test_summary_handles_missing_target(self):
        result = await summary(
            FakeConnection([], None),
            month="2026-10",
        )

        self.assertEqual(result["total_revenue"], 0.0)
        self.assertEqual(result["order_count"], 0)
        self.assertEqual(result["avg_order_value"], 0.0)
        self.assertIsNone(result["target"])
        self.assertIsNone(result["attainment_pct"])


if __name__ == "__main__":
    unittest.main()