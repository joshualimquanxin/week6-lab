import unittest

from duckfine import DuckFine


class TestDuckFineInit(unittest.TestCase):
    def test_stores_member_id(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.member_id, "member-1")

    def test_starts_with_zero_total_owed(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.total_owed, 0.0)


class TestDuckFineChargeValidation(unittest.TestCase):
    def test_negative_days_late_raises_value_error(self):
        duck = DuckFine("member-1")
        with self.assertRaises(ValueError):
            duck.charge(-1)


class TestDuckFineGracePeriod(unittest.TestCase):
    def test_zero_days_late_is_free(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.charge(0), 0.0)

    def test_days_late_within_grace_period_is_free(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.charge(1), 0.0)

    def test_days_late_equal_to_grace_period_is_free(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.charge(2), 0.0)


class TestDuckFineStandardCharge(unittest.TestCase):
    def test_one_day_past_grace_period_charges_daily_fee(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.charge(3), 0.50)

    def test_multiple_days_past_grace_period_charges_accumulated_fee(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.charge(5), 1.50)


class TestDuckFineDeluxeCharge(unittest.TestCase):
    def test_deluxe_doubles_the_fee(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.charge(3, deluxe=True), 1.00)

    def test_non_deluxe_defaults_to_single_fee(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.charge(3, deluxe=False), 0.50)


class TestDuckFineMaxFeeCap(unittest.TestCase):
    def test_fee_is_capped_at_max_fee(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.charge(100), 5.00)

    def test_deluxe_fee_is_capped_at_max_fee(self):
        duck = DuckFine("member-1")
        self.assertEqual(duck.charge(10, deluxe=True), 5.00)


class TestDuckFineTotalOwed(unittest.TestCase):
    def test_charge_increases_total_owed(self):
        duck = DuckFine("member-1")
        duck.charge(3)
        self.assertEqual(duck.total_owed, 0.50)

    def test_total_owed_accumulates_across_multiple_charges(self):
        duck = DuckFine("member-1")
        duck.charge(3)
        duck.charge(5)
        self.assertEqual(duck.total_owed, 2.00)

    def test_charge_return_value_matches_total_owed_after_single_charge(self):
        duck = DuckFine("member-1")
        fee = duck.charge(4)
        self.assertEqual(fee, duck.total_owed)


if __name__ == "__main__":
    unittest.main()
