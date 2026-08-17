"""
Pipeline tests for agents.py — H2 regression (quant.data_source must match the
fetcher's actual source) and response contract. All external calls are stubbed:
no network, no LLM, no real-universe cache writes (synthetic TEST* tickers only).

Stdlib unittest only. Run from the repo root:
    python -m unittest discover -s "Sovereign Code/backend/tests"
"""

import json
import os
import sys
import time
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import data_fetcher as df
import agents


def _ohlcv(n=20):
    return {
        "dates": [f"2026-07-{i + 1:02d}" for i in range(n)],
        "open": [10.0 + i * 0.1 for i in range(n)],
        "high": [10.5 + i * 0.1 for i in range(n)],
        "low": [9.5 + i * 0.1 for i in range(n)],
        "close": [10.0 + i * 0.1 for i in range(n)],
        "volume": [1000000 + i for i in range(n)],
    }


def _cleanup_test_cache():
    path = df._get_cache_path("TEST1")
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


class AgentPipelineTest(unittest.TestCase):
    """Hermetic: no API key, no LLM keys. Cache files only via synthetic TEST1."""

    def setUp(self):
        self._orig_get_key = df._get_alpha_vantage_key
        self._orig_llm_keys = agents.KEYS
        df._get_alpha_vantage_key = lambda: None
        agents.KEYS = {"openai": None, "anthropic": None}
        _cleanup_test_cache()

    def tearDown(self):
        _cleanup_test_cache()
        df._get_alpha_vantage_key = self._orig_get_key
        agents.KEYS = self._orig_llm_keys

    def test_simulated_source_labels_match(self):
        # H2 regression: quant_engine stamps "live" for any >=15-point series;
        # agents.py must override it to match the fetcher's actual source.
        res = agents.run_full_agent_analysis("QBTS")
        self.assertEqual(res["data_source"], "simulated")
        self.assertEqual(res["quant"]["data_source"], "simulated")
        self.assertFalse(res["data_stale"])
        self.assertIsNone(res["last_updated"])

    def test_stale_cache_path_labels(self):
        # Synthetic ticker + aged cache -> stale: True propagates through the pipeline
        df._save_cache("TEST1", _ohlcv(), source="alpha_vantage")
        path = df._get_cache_path("TEST1")
        with open(path, "r", encoding="utf-8") as f:
            cached = json.load(f)
        cached["last_updated"] = time.strftime(
            "%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - 48 * 3600)
        )
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cached, f)

        res = agents.run_full_agent_analysis("TEST1")
        self.assertEqual(res["data_source"], "live")
        self.assertTrue(res["data_stale"])
        self.assertEqual(res["quant"]["data_source"], "live")

    def test_response_contract(self):
        res = agents.run_full_agent_analysis("IONQ")
        for key in ("ticker", "stock_info", "director", "quant", "sentiment",
                    "risk", "execution", "upskill_tips",
                    "data_source", "last_updated", "data_stale"):
            self.assertIn(key, res)
        # Agent sub-results keep their shape
        self.assertIn("recommendation", res["director"])
        self.assertIn("rsi", res["quant"])
        self.assertIn("recommended_shares", res["risk"])

    def test_unknown_ticker_still_analyzes_with_sim(self):
        res = agents.run_full_agent_analysis("ZZZZ")
        self.assertEqual(res["ticker"], "ZZZZ")
        self.assertEqual(res["data_source"], "simulated")
        self.assertEqual(res["quant"]["data_source"], "simulated")
        self.assertIsNotNone(res["director"]["recommendation"])


if __name__ == "__main__":
    unittest.main()
