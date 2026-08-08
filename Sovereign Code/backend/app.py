"""
RJ-Stock Backend Server (Zero-Dependency Python HTTP REST Server).
Serves stock universe, multi-agent AI analysis, risk calculations, and Quantum Prairie metadata.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

try:
    from .config import QUANTUM_PURE_PLAY, QUANTUM_PRAIRIE_GIANTS
    from .quantum_prairie import get_quantum_prairie_summary
    from .agents import run_full_agent_analysis
    from .quant_engine import analyze_quant_metrics
    from .risk_engine import evaluate_risk
except ImportError:
    from config import QUANTUM_PURE_PLAY, QUANTUM_PRAIRIE_GIANTS
    from quantum_prairie import get_quantum_prairie_summary
    from agents import run_full_agent_analysis
    from quant_engine import analyze_quant_metrics
    from risk_engine import evaluate_risk

PORT = 8000

class QuantumStockAPIHandler(BaseHTTPRequestHandler):
    
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def _json_response(self, data, code=200):
        self.send_response(code)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/stocks":
            self._json_response({
                "pure_play": QUANTUM_PURE_PLAY,
                "prairie_giants": QUANTUM_PRAIRIE_GIANTS
            })
        elif path == "/api/quantum-prairie":
            self._json_response(get_quantum_prairie_summary())
        elif path.startswith("/api/analyze/"):
            ticker = path.split("/")[-1].upper()
            account_size = float(query.get("account_size", [10000.0])[0])
            risk_tolerance = float(query.get("risk_tolerance", [2.0])[0])
            
            analysis = run_full_agent_analysis(ticker, account_size, risk_tolerance)
            self._json_response(analysis)
        elif path == "/api/health":
            self._json_response({"status": "online", "system": "RJ-Stock AI Engine"})
        else:
            self._json_response({"error": "Endpoint not found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/simulate-trade":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body) if body else {}
                ticker = data.get("ticker", "IONQ")
                action = data.get("action", "BUY_LIMIT")
                quantity = int(data.get("quantity", 10))
                entry_price = float(data.get("entry_price", 14.85))
                
                result = {
                    "status": "EXECUTED_SIMULATION",
                    "order_id": f"ORD-{ticker}-20268799",
                    "ticker": ticker,
                    "action": action,
                    "quantity": quantity,
                    "filled_price": entry_price,
                    "total_cost": round(quantity * entry_price, 2),
                    "message": f"Simulated Paper Trade Executed! {action} {quantity} shares of {ticker} at ${entry_price:.2f}."
                }
                self._json_response(result)
            except Exception as e:
                self._json_response({"error": str(e)}, 400)
        else:
            self._json_response({"error": "Endpoint not found"}, 404)

def run_server(port=PORT):
    server_address = ('', port)
    httpd = HTTPServer(server_address, QuantumStockAPIHandler)
    print(f"[RJ-Stock] AI Server running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
