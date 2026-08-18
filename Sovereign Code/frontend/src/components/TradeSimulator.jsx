import React, { useState } from 'react';

// ─── Order Type Education Data ───────────────────────────────────────────────
const ORDER_TYPES = [
  {
    id: 'market',
    label: 'Market Order',
    icon: '⚡',
    risk: 'medium',
    riskLabel: 'Slippage Risk',
    shortDesc: 'Buy/sell immediately at the best available price.',
    plain: 'You\'re telling the market: "I want in RIGHT NOW — give me whatever price is available." The trade fills almost instantly, but the price you get may differ from the quote you see.',
    whenPros: 'When speed matters more than price precision. Earnings just dropped and you need to act in seconds, or you\'re closing a losing position and every second of delay costs more.',
    watchOut: 'On low-volume quantum stocks (RGTI, QBTS), the bid-ask spread can be wide. A market order might fill $0.10–0.30 away from the quoted price — that\'s called slippage, and it eats your edge.',
    fields: ['ticker', 'quantity', 'estimatedCost'],
  },
  {
    id: 'limit',
    label: 'Limit Order',
    icon: '🎯',
    risk: 'low',
    riskLabel: 'Price Control',
    shortDesc: 'Buy/sell only at your specified price or better.',
    plain: 'You set the exact maximum price you\'re willing to pay (for a buy) or minimum you\'ll accept (for a sell). The order waits patiently until the market reaches your price — or it expires unfilled.',
    whenPros: 'The default professional order type. It gives you price discipline. You decide what a stock is worth to you, set the limit, and let the market come to you instead of chasing.',
    watchOut: 'Your order may never fill if the stock doesn\'t reach your price. In a fast-moving rally, you might watch the stock run away from your limit while you wait. Patience is required.',
    fields: ['ticker', 'quantity', 'limitPrice', 'estimatedCost'],
  },
  {
    id: 'stop',
    label: 'Stop Order',
    icon: '🛑',
    risk: 'medium',
    riskLabel: 'Gap Risk',
    shortDesc: 'Triggers a market order when the price hits your stop.',
    plain: 'A stop order is your safety net. You set a trigger price — if the stock drops to that level, it automatically converts into a market order and sells to protect you from further losses.',
    whenPros: 'Every position should have a stop-loss. Professionals place stops immediately after entering a trade. It removes the emotional temptation to "hold and hope" through a crash.',
    watchOut: 'Stops trigger a market order, not a limit. If a stock gaps down overnight (opens at $15 when your stop was $18), you\'ll sell at $15 — the stop doesn\'t guarantee your exact price.',
    fields: ['ticker', 'quantity', 'stopPrice'],
  },
  {
    id: 'stop_limit',
    label: 'Stop-Limit',
    icon: '🔒',
    risk: 'high',
    riskLabel: 'May Not Fill',
    shortDesc: 'Triggers a limit order when the price hits your stop.',
    plain: 'A two-part safety order: (1) your stop price triggers the order, then (2) a limit price sets the minimum you\'ll accept. It protects you from selling at a terrible gap-down price — but the risk is it might not fill at all.',
    whenPros: 'When you want downside protection but refuse to sell at a disastrous price. Common on volatile biotech and quantum stocks where 10% overnight gaps happen regularly.',
    watchOut: 'This is the riskiest protective order. If the stock crashes through BOTH your stop and limit in a flash crash, the order sits unfilled and you hold a plummeting position. It protects price but not execution.',
    fields: ['ticker', 'quantity', 'stopPrice', 'limitPrice'],
  },
  {
    id: 'trailing_stop',
    label: 'Trailing Stop',
    icon: '📈',
    risk: 'low',
    riskLabel: 'Adaptive',
    shortDesc: 'A dynamic stop that follows the price upward.',
    plain: 'Instead of a fixed stop price, you set a trail amount (e.g., $2 or 5%). As the stock rises, the stop automatically ratchets up with it — locking in profits. If the stock reverses by your trail amount, it triggers a sell.',
    whenPros: 'The "let your winners run" order. Perfect after a breakout when you don\'t know how high a stock will go. You capture the uptrend while automatically protecting gains if the trend reverses.',
    watchOut: 'Setting the trail too tight on a volatile stock triggers premature exits. A 2% trail on IONQ (which can swing 3–5% intraday) will stop you out during normal noise. Match the trail to the stock\'s average daily range.',
    fields: ['ticker', 'quantity', 'trailAmount'],
  },
];

export default function TradeSimulator({ executionOrder, onSimulateTrade }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedType, setSelectedType] = useState('limit');

  if (!executionOrder) {
    return (
      <div className="glass-card" style={{ textAlign: 'center', padding: '60px' }}>
        <h3 style={{ color: 'var(--text-muted)', marginBottom: '12px' }}>🚀 Trade Order Simulator</h3>
        <p style={{ color: 'var(--text-muted)' }}>
          Run a stock analysis from the <strong style={{ color: 'var(--accent-cyan)' }}>AI Stock Picker</strong> tab first to generate an Execution Agent order ticket.
        </p>
      </div>
    );
  }

  const activeType = ORDER_TYPES.find(t => t.id === selectedType) || ORDER_TYPES[1];

  // ─── Compute derived values per order type ──────────────────────────────────
  const entryPrice = parseFloat(executionOrder.entry_price) || 0;
  const stopLoss = parseFloat(executionOrder.stop_loss) || 0;
  const takeProfit = parseFloat(executionOrder.take_profit) || 0;
  const qty = executionOrder.quantity || 0;

  const trailAmount = entryPrice > 0 ? parseFloat((entryPrice - stopLoss).toFixed(2)) : 0;
  const trailPct = entryPrice > 0 ? ((trailAmount / entryPrice) * 100).toFixed(1) : '0';

  const getEstimatedCost = () => {
    switch (selectedType) {
      case 'market': return (qty * entryPrice).toFixed(2);
      case 'limit': return (qty * entryPrice).toFixed(2);
      case 'stop': return `~${(qty * stopLoss).toFixed(2)}`;
      case 'stop_limit': return `~${(qty * stopLoss * 0.98).toFixed(2)}–${(qty * stopLoss).toFixed(2)}`;
      case 'trailing_stop': return (qty * entryPrice).toFixed(2);
      default: return executionOrder.estimated_total;
    }
  };

  // ─── Execute handler ────────────────────────────────────────────────────────
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
          entry_price: executionOrder.entry_price,
          order_type: activeType.label,
        })
      });
      const data = await res.json();
      data.order_type_label = activeType.label;
      data.order_type_icon = activeType.icon;
      setOrders([data, ...orders]);
      if (onSimulateTrade) onSimulateTrade(data);
    } catch {
      const mockOrder = {
        status: "EXECUTED_CLIENT_SIM",
        order_id: `ORD-${executionOrder.ticker}-${Date.now().toString().slice(-4)}`,
        ticker: executionOrder.ticker,
        action: executionOrder.action,
        quantity: executionOrder.quantity,
        filled_price: executionOrder.entry_price,
        total_cost: (executionOrder.quantity * entryPrice).toFixed(2),
        order_type_label: activeType.label,
        order_type_icon: activeType.icon,
        message: `Paper Trade Executed! ${activeType.label}: ${executionOrder.action} ${executionOrder.quantity} shares of ${executionOrder.ticker} at $${executionOrder.entry_price}.`
      };
      setOrders([mockOrder, ...orders]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

      {/* ── Section 1: Order Type Selector ────────────────────────────────── */}
      <div className="glass-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px', marginBottom: '16px' }}>
          <h3 style={{ fontSize: '1.1rem', color: 'var(--text-main)' }}>
            Choose Your Order Type
          </h3>
          <span className="badge badge-purple">📚 Order Type Literacy</span>
        </div>

        <div className="order-type-grid">
          {ORDER_TYPES.map(type => (
            <div
              key={type.id}
              id={`order-type-${type.id}`}
              className={`order-type-card ${selectedType === type.id ? 'active' : ''}`}
              onClick={() => setSelectedType(type.id)}
            >
              <span className="ot-icon">{type.icon}</span>
              <span className="ot-label">{type.label}</span>
              <span className={`ot-risk ${type.risk}`}>{type.riskLabel}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ── Section 2: Education Card ─────────────────────────────────────── */}
      <div className="edu-card" key={selectedType}>
        <h4>
          <span>{activeType.icon}</span>
          {activeType.label} — How It Works
        </h4>

        <div className="edu-section">
          <div className="edu-section-label">Plain English</div>
          <p>{activeType.plain}</p>
        </div>

        <div className="edu-section">
          <div className="edu-section-label">When Professionals Use It</div>
          <p>{activeType.whenPros}</p>
        </div>

        <div className="edu-section">
          <div className="edu-watchout">
            <strong>⚠️ Watch Out:</strong> {activeType.watchOut}
          </div>
        </div>
      </div>

      {/* ── Section 3: Adaptive Order Ticket ──────────────────────────────── */}
      <div className="glass-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px', marginBottom: '20px' }}>
          <div className="badge badge-cyan">🎫 {activeType.icon} {activeType.label.toUpperCase()} ORDER TICKET</div>
          <span className={`badge ${activeType.risk === 'low' ? 'badge-green' : activeType.risk === 'medium' ? 'badge-amber' : 'badge-red'}`}>
            {activeType.risk === 'low' ? '✅' : activeType.risk === 'medium' ? '⚠️' : '🔴'} {activeType.riskLabel}
          </span>
        </div>

        <div className="order-field-group" style={{ marginBottom: '20px' }}>
          {/* Always show ticker */}
          <div className="order-field">
            <label>Ticker Symbol</label>
            <div className="field-value cyan">{executionOrder.ticker}</div>
          </div>

          {/* Always show quantity */}
          <div className="order-field">
            <label>Quantity</label>
            <div className="field-value green">{qty} Shares</div>
          </div>

          {/* Market: estimated price */}
          {selectedType === 'market' && (
            <div className="order-field">
              <label>Market Price (Est.)</label>
              <div className="field-value">~${entryPrice}</div>
            </div>
          )}

          {/* Limit: limit price */}
          {(selectedType === 'limit') && (
            <div className="order-field">
              <label>Limit Entry Price</label>
              <div className="field-value">${entryPrice}</div>
            </div>
          )}

          {/* Stop: stop/trigger price */}
          {(selectedType === 'stop') && (
            <div className="order-field">
              <label>Stop Trigger Price</label>
              <div className="field-value" style={{ color: 'var(--accent-red)' }}>${stopLoss}</div>
            </div>
          )}

          {/* Stop-Limit: both prices */}
          {selectedType === 'stop_limit' && (
            <>
              <div className="order-field">
                <label>Stop Trigger Price</label>
                <div className="field-value" style={{ color: 'var(--accent-red)' }}>${stopLoss}</div>
              </div>
              <div className="order-field">
                <label>Limit Floor Price</label>
                <div className="field-value" style={{ color: 'var(--accent-amber)' }}>${(stopLoss * 0.98).toFixed(2)}</div>
              </div>
            </>
          )}

          {/* Trailing Stop: trail amount + percent */}
          {selectedType === 'trailing_stop' && (
            <>
              <div className="order-field">
                <label>Trail Amount</label>
                <div className="field-value" style={{ color: 'var(--accent-purple)' }}>${trailAmount}</div>
              </div>
              <div className="order-field">
                <label>Trail Percentage</label>
                <div className="field-value" style={{ color: 'var(--accent-purple)' }}>{trailPct}%</div>
              </div>
            </>
          )}

          {/* Estimated cost / value */}
          <div className="order-field">
            <label>Estimated {selectedType === 'stop' || selectedType === 'stop_limit' ? 'Proceeds' : 'Cost'}</label>
            <div className="field-value">${getEstimatedCost()}</div>
          </div>
        </div>

        {/* Execute + Safeguards */}
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap' }}>
          <button className="btn-primary" id="execute-paper-trade" onClick={handleExecute} disabled={loading}>
            {loading ? 'Executing...' : `🚀 Execute ${activeType.label}`}
          </button>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            Safeguards: Stop Loss @ ${stopLoss} | Take Profit @ ${takeProfit}
          </span>
        </div>

        {/* Contextual tip based on order type */}
        {selectedType === 'market' && (
          <div style={{ marginTop: '14px', padding: '10px 14px', background: 'rgba(245, 158, 11, 0.06)', borderRadius: '8px', border: '1px solid rgba(245, 158, 11, 0.15)', fontSize: '0.85rem', color: 'var(--accent-amber)' }}>
            💡 <strong>Tip:</strong> Market orders on low-volume quantum stocks may fill at a different price than shown. Consider a Limit Order for better price control.
          </div>
        )}
        {selectedType === 'stop_limit' && (
          <div style={{ marginTop: '14px', padding: '10px 14px', background: 'rgba(239, 68, 68, 0.06)', borderRadius: '8px', border: '1px solid rgba(239, 68, 68, 0.15)', fontSize: '0.85rem', color: 'var(--accent-red)' }}>
            ⚠️ <strong>Advanced:</strong> The limit floor is set 2% below the stop trigger. If the stock gaps through both prices, this order will NOT fill — you remain exposed.
          </div>
        )}
        {selectedType === 'trailing_stop' && (
          <div style={{ marginTop: '14px', padding: '10px 14px', background: 'rgba(16, 185, 129, 0.06)', borderRadius: '8px', border: '1px solid rgba(16, 185, 129, 0.15)', fontSize: '0.85rem', color: 'var(--accent-green)' }}>
            📈 <strong>Pro Tip:</strong> The ${trailAmount} trail ({trailPct}%) is derived from your risk engine's stop-loss distance. As the price rises, the stop automatically ratchets up to lock in gains.
          </div>
        )}
      </div>

      {/* ── Section 4: Executed Orders History ────────────────────────────── */}
      {orders.length > 0 && (
        <div className="glass-card">
          <h3 style={{ color: 'var(--accent-green)', marginBottom: '16px' }}>📜 Paper Trading History</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {orders.map((ord, i) => (
              <div key={i} style={{
                background: 'rgba(16, 185, 129, 0.05)',
                padding: '14px 18px',
                borderRadius: '10px',
                border: '1px solid rgba(16, 185, 129, 0.2)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '10px',
              }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 'bold', color: 'var(--accent-cyan)' }}>{ord.order_id}</span>
                    {ord.order_type_label && (
                      <span className="badge badge-purple" style={{ fontSize: '0.65rem' }}>
                        {ord.order_type_icon} {ord.order_type_label}
                      </span>
                    )}
                  </div>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-main)' }}>{ord.message}</p>
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
