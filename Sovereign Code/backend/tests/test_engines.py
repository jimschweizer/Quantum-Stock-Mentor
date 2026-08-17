"""
Unit tests for quant_engine.py and risk_engine.py math edge cases
(division-by-zero guards, bounds, determinism).

Stdlib unittest only. Run from the repo root:
    python -m unittest discover -s "Sovereign Code/backend/tests"
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from quant_engine import (
    analyze_quant_metrics,
    calculate_rsi,
    calculate_sma,
    calculate_volatility,
    compute_key_levels,
    compute_key_levels_ohlc,
)
from risk_engine import evaluate_risk


RISING = [10.0 + i for i in range(20)]       # strictly rising -> RSI 100
FALLING = [10.0 - i for i in range(20)]      # strictly falling -> RSI ~0


class RsiTest(unittest.TestCase):

    def test_rsi_zero_loss_returns_100(self):
        self.assertEqual(calculate_rsi(RISING), 100.0)

    def test_rsi_zero_gain_returns_zero(self):
        self.assertAlmostEqual(calculate_rsi(FALLING), 0.0, places=5)

    def test_rsi_short_series_returns_neutral(self):
        self.assertEqual(calculate_rsi([1.0, 2.0, 3.0]), 50.0)

    def test_rsi_within_bounds(self):
        rsi = calculate_rsi([10, 11, 9, 12, 8, 13, 7, 14, 6, 15, 5, 16, 4, 17, 3, 18])
        self.assertGreaterEqual(rsi, 0.0)
        self.assertLessEqual(rsi, 100.0)


class SmaTest(unittest.TestCase):

    def test_sma_normal(self):
        self.assertEqual(calculate_sma([1.0, 2.0, 3.0, 4.0], period=2), 3.5)

    def test_sma_short_series_falls_back_to_mean(self):
        self.assertEqual(calculate_sma([1.0, 2.0, 3.0], period=20), 2.0)

    def test_sma_empty_returns_zero(self):
        self.assertEqual(calculate_sma([], period=20), 0.0)


class VolatilityTest(unittest.TestCase):

    def test_volatility_short_series_default(self):
        self.assertEqual(calculate_volatility([1.0]), 0.05)

    def test_volatility_zero_movement(self):
        self.assertEqual(calculate_volatility([10.0] * 10), 0.0)

    def test_volatility_positive(self):
        self.assertGreater(calculate_volatility([10.0, 11.0, 9.0, 12.0, 8.0]), 0.0)


class KeyLevelsTest(unittest.TestCase):

    def test_ohlc_uses_last_session_high_low_close(self):
        highs = [10.0, 12.0, 11.0]
        lows = [9.0, 10.0, 10.5]
        closes = [9.5, 11.5, 10.8]
        levels = compute_key_levels_ohlc(highs, lows, closes)
        pivot = (11.0 + 10.5 + 10.8) / 3.0
        self.assertAlmostEqual(levels["pivot"], round(pivot, 2))
        self.assertAlmostEqual(levels["resistance"], round(2 * pivot - 10.5, 2))
        self.assertAlmostEqual(levels["support"], round(max(0.1, 2 * pivot - 11.0), 2))

    def test_ohlc_empty_returns_zeros(self):
        self.assertEqual(compute_key_levels_ohlc([], [], []),
                         {"support": 0.0, "resistance": 0.0, "pivot": 0.0})

    def test_legacy_close_only_levels(self):
        levels = compute_key_levels([10.0, 11.0, 12.0, 13.0])
        self.assertIn("pivot", levels)
        self.assertGreater(levels["resistance"], levels["support"])


class AnalyzeMetricsTest(unittest.TestCase):

    def test_without_history_is_simulated(self):
        res = analyze_quant_metrics("IONQ", 14.85)
        self.assertEqual(res["data_source"], "simulated")
        for key in ("rsi", "sma7", "sma20", "sma30", "volatility_pct",
                    "technical_score", "volume_score", "trend_strength",
                    "probability_score", "key_levels", "trends"):
            self.assertIn(key, res)

    def test_with_history_is_live(self):
        res = analyze_quant_metrics("IONQ", RISING[-1], price_history=RISING)
        self.assertEqual(res["data_source"], "live")

    def test_probability_score_bounds(self):
        res = analyze_quant_metrics("IONQ", 14.85)
        self.assertGreaterEqual(res["probability_score"], 0.0)
        self.assertLessEqual(res["probability_score"], 1.0)

    def test_volume_score_deterministic(self):
        a = analyze_quant_metrics("IONQ", 14.85)
        b = analyze_quant_metrics("IONQ", 14.85)
        self.assertEqual(a["volume_score"], b["volume_score"])

    def test_volume_score_bounds(self):
        res = analyze_quant_metrics("IONQ", 14.85)
        self.assertGreaterEqual(res["volume_score"], 0.3)
        self.assertLessEqual(res["volume_score"], 1.0)

    def test_trends_present(self):
        res = analyze_quant_metrics("IONQ", 14.85)
        for horizon in ("day_1", "day_7", "day_30"):
            self.assertIn(horizon, res["trends"])
        self.assertIn("alignment", res["trends"])
        self.assertIn("alignment_score", res["trends"])


class RiskEngineTest(unittest.TestCase):

    def test_max_dollar_risk_rule(self):
        res = evaluate_risk("IONQ", 14.85, account_size=10000, risk_tolerance_pct=2.0)
        self.assertEqual(res["max_dollar_risk"], 200.0)

    def test_shares_floor_to_one(self):
        res = evaluate_risk("IONQ", 14.85, account_size=100, risk_tolerance_pct=0.5, volatility_pct=3.0)
        self.assertGreaterEqual(res["recommended_shares"], 1)

    def test_take_profit_is_2_5x_risk(self):
        res = evaluate_risk("IONQ", 14.85, account_size=10000, risk_tolerance_pct=2.0, volatility_pct=5.0)
        risk_per_share = res["current_price"] - res["stop_loss_price"]
        self.assertAlmostEqual(res["take_profit_price"],
                               round(res["current_price"] + risk_per_share * 2.5, 2))

    def test_stop_loss_below_entry(self):
        res = evaluate_risk("IONQ", 14.85, account_size=10000, risk_tolerance_pct=2.0, volatility_pct=10.0)
        self.assertLess(res["stop_loss_price"], res["current_price"])

    def test_risk_category_labels(self):
        low = evaluate_risk("IONQ", 14.85, account_size=10000, risk_tolerance_pct=0.5, volatility_pct=2.0)
        self.assertIn(low["risk_category"], ("Low Risk / Defensive", "Moderate Risk", "High Risk / Growth"))


if __name__ == "__main__":
    unittest.main()
