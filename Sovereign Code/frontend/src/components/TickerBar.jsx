import React from 'react';

export default function TickerBar({ stocks, selectedTicker, onSelectTicker }) {
  const allStocks = [...(stocks.pure_play || []), ...(stocks.prairie_giants || [])];

  return (
    <div className="ticker-bar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', paddingRight: '12px', color: 'var(--accent-cyan)', fontWeight: 'bold' }}>
        <span>⚡ QUANTUM FEED:</span>
      </div>
      {allStocks.map((stock) => {
        const isSelected = selectedTicker === stock.ticker;
        const isPrairie = !!stock.prairie_role;
        return (
          <div
            key={stock.ticker}
            className={`ticker-item ${isSelected ? 'active' : ''}`}
            onClick={() => onSelectTicker(stock.ticker)}
          >
            <span style={{ fontWeight: 'bold', color: 'var(--text-main)' }}>{stock.ticker}</span>
            <span style={{ color: 'var(--text-muted)' }}>${stock.price.toFixed(2)}</span>
            <span className={`badge ${isPrairie ? 'badge-purple' : 'badge-cyan'}`}>
              {isPrairie ? 'Prairie Hub' : 'Pure Play'}
            </span>
          </div>
        );
      })}
    </div>
  );
}
