"""
HTTP integration tests for app.py — spins up the real ThreadedHTTPServer on an
ephemeral port with all external calls stubbed (no network, no LLM, isolated
cache dir). Verifies endpoints, CORS headers, and error codes.

Stdlib unittest only. Run from the repo root:
    python -m unittest discover -s "Sovereign Code/backend/tests"
"""

import json
import os
import sys
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import data_fetcher as df
import agents
from app import QuantumStockAPIHandler, ThreadedHTTPServer

BASE = "http://127.0.0.1:{port}"


class ApiIntegrationTest(unittest.TestCase):
    """Hermetic environment: no API key, no LLM keys -> the pipeline never
    touches the network or writes cache files (simulation mode everywhere)."""

    @classmethod
    def setUpClass(cls):
        cls._orig_get_key = df._get_alpha_vantage_key
        cls._orig_llm_keys = agents.KEYS

        df._get_alpha_vantage_key = lambda: None
        agents.KEYS = {"openai": None, "anthropic": None}

        cls.httpd = ThreadedHTTPServer(("127.0.0.1", 0), QuantumStockAPIHandler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        df._get_alpha_vantage_key = cls._orig_get_key
        agents.KEYS = cls._orig_llm_keys

    def _get(self, path):
        req = Request(f"{BASE.format(port=self.port)}{path}")
        try:
            with urlopen(req, timeout=10) as resp:
                return resp.status, dict(resp.headers), json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            return e.code, dict(e.headers), json.loads(e.read().decode("utf-8"))

    def _post(self, path, body):
        req = Request(
            f"{BASE.format(port=self.port)}{path}",
            data=json.dumps(body).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    # --- GET endpoints ---

    def test_stocks_returns_universe_with_cors(self):
        status, headers, data = self._get("/api/stocks")
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("Access-Control-Allow-Origin"), "*")
        self.assertEqual(len(data["pure_play"]), 4)
        self.assertEqual(len(data["prairie_giants"]), 4)
        # overlay contract: every stock carries data_source
        for stock in data["pure_play"] + data["prairie_giants"]:
            self.assertIn("data_source", stock)

    def test_analyze_returns_full_pipeline(self):
        status, _, data = self._get("/api/analyze/IONQ")
        self.assertEqual(status, 200)
        self.assertEqual(data["ticker"], "IONQ")
        for key in ("stock_info", "director", "quant", "sentiment", "risk",
                    "execution", "upskill_tips", "data_source", "data_stale"):
            self.assertIn(key, data)
        self.assertEqual(data["quant"]["data_source"], data["data_source"])

    def test_analyze_respects_account_params(self):
        status, _, data = self._get("/api/analyze/IONQ?account_size=5000&risk_tolerance=1.0")
        self.assertEqual(status, 200)
        self.assertEqual(data["risk"]["account_size"], 5000.0)
        self.assertEqual(data["risk"]["risk_tolerance_pct"], 1.0)

    def test_quantum_prairie_endpoint(self):
        status, _, data = self._get("/api/quantum-prairie")
        self.assertEqual(status, 200)
        self.assertIn("key_anchors", data)
        self.assertIn("key_companies", data)

    def test_health_endpoint(self):
        status, _, data = self._get("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "online")

    def test_unknown_route_returns_404(self):
        status, _, data = self._get("/api/does-not-exist")
        self.assertEqual(status, 404)
        self.assertIn("error", data)

    # --- POST endpoints ---

    def test_simulate_trade(self):
        status, data = self._post("/api/simulate-trade", {
            "ticker": "IONQ", "action": "BUY_LIMIT", "quantity": 10, "entry_price": 14.85
        })
        self.assertEqual(status, 200)
        self.assertTrue(data["order_id"].startswith("ORD-IONQ-"))
        self.assertEqual(data["quantity"], 10)
        self.assertAlmostEqual(data["total_cost"], 148.5)

    def test_refresh_data_missing_ticker_returns_400(self):
        req = Request(
            f"{BASE.format(port=self.port)}/api/refresh-data",
            data=b"{}",
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaises(HTTPError) as ctx:
            urlopen(req, timeout=10)
        self.assertEqual(ctx.exception.code, 400)

    def test_refresh_data_single_ticker(self):
        status, data = self._post("/api/refresh-data", {"ticker": "IONQ"})
        self.assertEqual(status, 200)
        self.assertEqual(data["ticker"], "IONQ")
        self.assertIn("source", data)
        self.assertIn("stale", data)

    def test_refresh_data_all(self):
        status, data = self._post("/api/refresh-data", {"ticker": "ALL"})
        self.assertEqual(status, 200)
        self.assertEqual(len(data["tickers"]), 8)

    def test_bad_json_body_returns_400(self):
        req = Request(
            f"{BASE.format(port=self.port)}/api/simulate-trade",
            data=b"{not json",
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaises(HTTPError) as ctx:
            urlopen(req, timeout=10)
        self.assertEqual(ctx.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
