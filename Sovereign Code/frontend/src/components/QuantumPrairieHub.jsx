import React from 'react';

export default function QuantumPrairieHub({ prairieData }) {
  if (!prairieData) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Prairie Banner */}
      <div className="glass-card" style={{ borderLeft: '4px solid var(--accent-purple)' }}>
        <div className="badge badge-purple" style={{ marginBottom: '8px' }}>🌾 REGIONAL SPOTLIGHT</div>
        <h1 style={{ fontSize: '2rem', background: 'var(--gradient-quantum)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: '8px' }}>
          {prairieData.title}
        </h1>
        <p style={{ color: 'var(--accent-cyan)', fontWeight: 'bold', marginBottom: '12px' }}>📍 {prairieData.region}</p>
        <p style={{ color: 'var(--text-muted)', lineHeight: '1.6' }}>{prairieData.overview}</p>
      </div>

      {/* Key Anchors Section */}
      <div>
        <h2 style={{ color: 'var(--accent-cyan)', marginBottom: '16px' }}>🏛️ Major Infrastructure & Research Anchors</h2>
        <div className="dashboard-grid" style={{ padding: 0 }}>
          {prairieData.key_anchors?.map((anchor, idx) => (
            <div key={idx} className="glass-card">
              <span className="badge badge-cyan" style={{ marginBottom: '8px' }}>{anchor.type}</span>
              <h3 style={{ color: 'var(--text-main)', marginBottom: '4px' }}>{anchor.name}</h3>
              <p style={{ color: 'var(--accent-purple)', fontSize: '0.85rem', marginBottom: '8px' }}>📍 {anchor.location}</p>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{anchor.highlights}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Companies & Stock Alignment */}
      <div>
        <h2 style={{ color: 'var(--accent-purple)', marginBottom: '16px' }}>🏢 Quantum Prairie Corporate Ecosystem & Public Stocks</h2>
        <div className="dashboard-grid" style={{ padding: 0 }}>
          {prairieData.key_companies?.map((comp, idx) => (
            <div key={idx} className="glass-card" style={{ background: 'rgba(168, 85, 247, 0.03)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <h3 style={{ color: 'var(--accent-cyan)' }}>{comp.name}</h3>
                <span className={`badge ${comp.status.includes('Public') ? 'badge-green' : 'badge-amber'}`}>
                  {comp.status}
                </span>
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{comp.focus}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
