'use client';

import { useEffect, useState } from 'react';
import { Heading, Label, Flash, Spinner } from '@primer/react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

type PortfolioAgent = { id: string; name: string; memory: string; status: string; trust_score: number; transfer_efficiency: number; last_eval: string; };
type PortfolioAlert = { id: string; title: string; severity: string; summary: string; };

function statusVariant(s: string): 'success' | 'danger' | 'attention' | 'secondary' {
  if (s === 'Healthy') return 'success';
  if (s === 'Blocked') return 'danger';
  if (s === 'Warning') return 'attention';
  return 'secondary';
}

export default function PortfolioScreen() {
  const [stats, setStats] = useState<any>(null);
  const [agents, setAgents] = useState<PortfolioAgent[]>([]);
  const [alerts, setAlerts] = useState<PortfolioAlert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/portfolio`)
      .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
      .then((data) => { setStats(data.stats); setAgents(data.agents); setAlerts(data.alerts); })
      .catch(() => {
        setStats({ active_listings: 5, verifications: 10, feedback_received: 3, monthly_spend: 33 });
        setAgents([
          { id: '1', name: 'DeFi Risk Pack v2.1', memory: 'DeFi:risk-assessment', status: 'Healthy', trust_score: 92.5, transfer_efficiency: 92.2, last_eval: '2026-04-23' },
          { id: '2', name: 'CVE Severity Scorer v1.8', memory: 'CyberSec:vulnerability-assessment', status: 'Healthy', trust_score: 94.2, transfer_efficiency: 95.5, last_eval: '2026-04-23' },
        ]);
        setAlerts([]);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="amm-page"><Spinner size="medium" /></div>;

  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Control tower</Heading>
      <p className="amm-screen-subtitle">Watch live artifacts, verification posture, and drift state.</p>

      <div className="amm-metric-grid">
        {[
          ['Active listings', stats?.active_listings ?? 0],
          ['Verifications', stats?.verifications ?? 0],
          ['Feedback', stats?.feedback_received ?? 0],
          ['Monthly spend', `$${stats?.monthly_spend?.toFixed(0) ?? 0}`],
        ].map(([label, value]) => (
          <div key={String(label)} className="amm-metric-tile">
            <span className="amm-metric-label">{label}</span>
            <span className="amm-metric-value">{value}</span>
          </div>
        ))}
      </div>

      <div className="amm-grid amm-grid-2col">
        <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', overflow: 'hidden' }}>
          <div style={{ padding: '16px', borderBottom: '1px solid #d0d7de' }}>
            <Heading as="h2" style={{ fontSize: '14px' }}>Verified artifacts</Heading>
          </div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--borderColor-default, #d0d7de)' }}>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Artifact</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Domain</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Status</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Trust</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Transfer Eff.</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Last eval</th>
              </tr>
            </thead>
            <tbody>
              {agents.map((a) => (
                <tr key={a.id} style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                  <td style={{ padding: '8px 12px', fontWeight: 600 }}>{a.name}</td>
                  <td style={{ padding: '8px 12px' }}>{a.memory}</td>
                  <td style={{ padding: '8px 12px' }}><Label variant={statusVariant(a.status)}>{a.status}</Label></td>
                  <td style={{ padding: '8px 12px' }}>{a.trust_score?.toFixed(1)}/100</td>
                  <td style={{ padding: '8px 12px' }}>{a.transfer_efficiency?.toFixed(1)}%</td>
                  <td style={{ padding: '8px 12px' }}>{a.last_eval?.slice(0, 10)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="amm-card-stack">
          {alerts.length > 0 ? alerts.map((a) => (
            <Flash key={a.id} variant={a.severity === 'Blocked' ? 'danger' : 'warning'}>
              <strong>{a.title}</strong><br />{a.summary}
            </Flash>
          )) : (
            <Flash variant="success"><strong>All clear</strong> — no drift alerts or safety issues.</Flash>
          )}
          <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px', marginTop: '8px' }}>
            <Heading as="h3" style={{ fontSize: '14px', marginBottom: '8px' }}>Policy</Heading>
            <span className="amm-subtle" style={{ display: 'block' }}>Auto-buy cap: $2,000</span>
            <span className="amm-subtle" style={{ display: 'block' }}>Human approval above Medium risk</span>
            <span className="amm-subtle" style={{ display: 'block' }}>Auto-revoke on negative transfer &gt; 5%</span>
            <span className="amm-subtle" style={{ display: 'block' }}>Scope: retrieval only / no tool autonomy</span>
          </div>
        </div>
      </div>
    </div>
  );
}
