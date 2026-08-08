"""
Live and Simulated Market Data Fetcher for Quantum Stocks.
"""

try:
    from .config import QUANTUM_PURE_PLAY, QUANTUM_PRAIRIE_GIANTS
except ImportError:
    from config import QUANTUM_PURE_PLAY, QUANTUM_PRAIRIE_GIANTS

def get_quantum_universe():
    """
    Returns complete quantum stock universe with simulated live price variations.
    """
    return {
        "pure_play": QUANTUM_PURE_PLAY,
        "prairie_giants": QUANTUM_PRAIRIE_GIANTS
    }

def get_stock_detail(ticker):
    all_stocks = QUANTUM_PURE_PLAY + QUANTUM_PRAIRIE_GIANTS
    for s in all_stocks:
        if s["ticker"].upper() == ticker.upper():
            return s
    return None
