import unittest
import pandas as pd
from datetime import datetime
from src.finance import safe_xirr, calculate_cagr, aggregate_units

class TestFinance(unittest.TestCase):
    def test_safe_xirr(self):
        # Basic XIRR test
        cfs = [
            (datetime(2023, 1, 1), -10000),
            (datetime(2024, 1, 1), 11000)
        ]
        result = safe_xirr(cfs)
        self.assertAlmostEqual(result, 0.1, places=4)

    def test_calculate_cagr(self):
        # 10% growth over 2 years
        # (1.21 / 1.0) ^ (1/2) - 1 = 0.1
        self.assertAlmostEqual(calculate_cagr(100, 121, 2), 0.1, places=4)

    def test_aggregate_units(self):
        df = pd.DataFrame({
            'Scheme Name': ['Fund A', 'Fund A', 'Fund B'],
            'Effective Units': [10.5, 5.5, 20.0]
        })
        self.assertEqual(aggregate_units(df, 'Fund A'), 16.0)
        self.assertEqual(aggregate_units(df, 'Fund B'), 20.0)

if __name__ == "__main__":
    unittest.main()
