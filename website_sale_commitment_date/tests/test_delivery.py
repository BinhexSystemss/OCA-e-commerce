# Copyright 2025 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date

from freezegun import freeze_time

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@freeze_time("2025-01-09 15:00:00")
@tagged("post_install", "-at_install")
class TestDeliveryCarrier(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.DeliveryCarrier = cls.env["delivery.carrier"]

    def test01_delivery_carrier(self):
        carrier = self.DeliveryCarrier.create(
            {
                "name": "Test carrier",
                "product_id": self.env.ref("product.product_product_4").id,
                "allow_commitment_date": True,
                "min_commitment_days": 2,
                "max_commitment_days": 15,
            }
        )
        self.assertTrue(carrier.allow_commitment_date)
        self.assertEqual(carrier.min_commitment_days, 2)
        self.assertEqual(carrier.max_commitment_days, 15)
        self.assertFalse(carrier.exclude_weekday_ids)

        carrier.write({"exclude_weekday_ids": [(6, 0, [1, 2])]})

        self.assertEqual(len(carrier.exclude_weekday_ids), 2)
        self.assertIn(1, carrier.exclude_weekday_ids.ids)
        self.assertIn(2, carrier.exclude_weekday_ids.ids)

        res = carrier._get_calendar_context()
        self.assertTrue(res)
        self.assertIn("month", res)
        self.assertIn("year", res)
        self.assertEqual(res["month"], 1)
        self.assertEqual(res["year"], 2025)

        res = carrier._get_calendar_context(start=date(2026, 2, 1))
        self.assertTrue(res)
        self.assertIn("month", res)
        self.assertIn("year", res)
        self.assertEqual(res["month"], 2)
        self.assertEqual(res["year"], 2026)

        res = carrier._check_calendar_disabled_day(date(2025, 1, 1))
        self.assertTrue(res)
        res = carrier._check_calendar_disabled_day(date(2025, 1, 9))
        self.assertTrue(res)
        res = carrier._check_calendar_disabled_day(date(2025, 1, 28))
        self.assertTrue(res)
        res = carrier._check_calendar_disabled_day(date(2025, 1, 13))
        self.assertTrue(res)
        res = carrier._check_calendar_disabled_day(date(2025, 1, 23))
        self.assertFalse(res)
