import React, { useState } from 'react';

export default function TradeSimulator({ executionOrder, onSimulateTrade }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  if (!executionOrder) return null;

  const handleExecute = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/simulate-trade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ticker: executionOrder.ticker,
          action: executionOrder.action,
          quantity: executionOrder.quantity,
          entry_price: executionOrder.entry_price
        })
      });
      const data = await res.json();
      setOrders([data, ...orders]);
      if (onSimulateTrade) onSimulateTrade(data);
    } catch (err) {
      // Fallback client simulation if server offline
      const mockOrder = {
        status: "EXECUTED_CLIENT_SIM",
        order_id: `ORD-${executionOrder.ticker}-${Date.now().toString().slice(-4)}`,
        ticker: executionOrder.ticker,
        action: executionOrder.action,
        quantity: executionOrder.quantity,
        filled_price: executionOrder.entry_price,
        total_cost: (executionOrder.quantity * executionOrder.entry_price).toFixed(2),
        message: `Paper Trade Executed! ${executionOrder.action} ${executionOrder.quantity} shares of ${executionOrder.ticker} at $${executionOrder.entry_price}.`
      };
      setOrders([mockOrder, ...orders]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Active Ticket */}
      <div className="glass-card">
        <div className="badge badge-cyan" style={{ marginBottom: '12px' }}>🎫 EXECUTION AGENT ORDER TICKET</div>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '20px' }}>
          <div>
            <small style={{ color: 'var(--text-muted)' }}>Ticker Symbol</small>
            <div style={{ fontSize: '1.4rem', fontWeight: 'bold', color: 'var(--accent-cyan)' }}>{executionOrder.ticker}</div>
          </div>
          <div>
            <small style={{ color: 'var(--text-muted)' }}>Order Type</small>
            <div style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>{executionOrder.order_type}</div>
          </div>
          <div>
            <small style={{ color: 'var(--text-muted)' }}>Quantity</small>
            <div style={{ fontSize: '1.4rem', fontWeight: 'bold', color: 'var(--accent-green)' }}>{executionOrder.quantity} Shares</div>
          </div>
          <div>
            <small style={{ color: 'var(--text-muted)' }}>Limit Entry Price</small>
            <div style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>${executionOrder.entry_price}</div>
          </div>
          <div>
            <small style={{ color: 'var(--text-muted)' }}>Estimated Cost</small>
            <div style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>${executionOrder.estimated_total}</div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <button className="btn-primary" onClick={handleExecute} disabled={loading}>
            {loading ? 'Executing...' : '🚀 Execute Paper Trade Order'}
          </button>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            Safeguards attached: Stop Loss @ ${executionOrder.stop_loss} | Take Profit @ ${executionOrder.take_profit}
          </span>
        </div>
      </div>

      {/* Executed Orders History */}
      {orders.length > 0 && (
        <div className="glass-card">
          <h3 style={{ color: 'var(--accent-green)', marginBottom: '16px' }}>📜 Simulated Paper Trading History</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {orders.map((ord, i) => (
              <div key={i} style={{ background: 'rgba(16, 185, 129, 0.05)', padding: '12px 16px', borderRadius: '8px', border: '1px solid rgba(16, 185, 129, 0.2)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span style={{ fontWeight: 'bold', color: 'var(--accent-cyan)' }}>{ord.order_id}</span>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-main)', marginTop: '2px' }}>{ord.message}</p>
                </div>
                <span className="badge badge-green">STATUS: FILLED</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
