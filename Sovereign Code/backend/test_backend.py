"""
Verification test script for RJ-Stock Backend.
"""

from config import QUANTUM_PURE_PLAY, QUANTUM_PRAIRIE_GIANTS
from quant_engine import analyze_quant_metrics
from risk_engine import evaluate_risk
from agents import run_full_agent_analysis
from quantum_prairie import get_quantum_prairie_summary

def test_pipeline():
    print("--- 1. Testing Config ---")
    print(f"Loaded {len(QUANTUM_PURE_PLAY)} Pure-Play and {len(QUANTUM_PRAIRIE_GIANTS)} Prairie Giant stocks.")
    
    print("\n--- 2. Testing Quant Engine (IONQ) ---")
    quant = analyze_quant_metrics("IONQ", 14.85)
    print(f"IONQ RSI: {quant['rsi']}, Technical Score: {quant['technical_score']}")
    
    print("\n--- 3. Testing Risk Engine (IONQ) ---")
    risk = evaluate_risk("IONQ", 14.85, account_size=10000, risk_tolerance_pct=2.0)
    print(f"Recommended Shares: {risk['recommended_shares']}, Stop Loss: ${risk['stop_loss_price']}")
    
    print("\n--- 4. Testing 5-Agent Workflow (IONQ) ---")
    full_res = run_full_agent_analysis("IONQ")
    print(f"Director Recommendation: {full_res['director']['recommendation']}")
    print(f"Sentiment Score: {full_res['sentiment']['sentiment_score']}")
    print(f"Execution Order Action: {full_res['execution']['action']}")
    
    print("\n--- 5. Testing Quantum Prairie Knowledge ---")
    prairie = get_quantum_prairie_summary()
    print(f"Region: {prairie['region']}, Key Anchors: {len(prairie['key_anchors'])}")
    print("\nSUCCESS: All backend modules verified!")

if __name__ == "__main__":
    test_pipeline()
