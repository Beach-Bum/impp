'use client';

import { useEffect, useState } from 'react';
import {
  Column,
  DataTable,
  Grid,
  InlineLoading,
  InlineNotification,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableHeader,
  TableRow,
  Tile,
} from '@carbon/react';
import StatusTag from '@/components/StatusTag';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

type PortfolioAgent = {
  id: string;
  name: string;
  memory: string;
  status: 'Healthy' | 'Watch' | 'Warning' | 'Blocked';
  trust_score: number;
  transfer_efficiency: number;
  last_eval: string;
};

type PortfolioAlert = {
  id: string;
  title: string;
  severity: 'Blocked' | 'Warning' | 'Watch';
  summary: string;
};

type PortfolioStats = {
  active_listings: number;
  verifications: number;
  feedback_received: number;
  monthly_spend: number;
};

const agentHeaders = [
  { key: 'name', header: 'Artifact' },
  { key: 'memory', header: 'Domain' },
  { key: 'status', header: 'Status' },
  { key: 'trust', header: 'Trust' },
  { key: 'te', header: 'Transfer Eff.' },
  { key: 'lastEval', header: 'Last eval' },
];

export default function PortfolioScreen() {
  const [stats, setStats] = useState<PortfolioStats | null>(null);
  const [agents, setAgents] = useState<PortfolioAgent[]>([]);
  const [alerts, setAlerts] = useState<PortfolioAlert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/portfolio`)
      .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
      .then((data) => {
        setStats(data.stats);
        setAgents(data.agents);
        setAlerts(data.alerts);
      })
      .catch(() => {
        // Fallback mock data for Vercel preview
        setStats({ active_listings: 5, verifications: 10, feedback_received: 3, monthly_spend: 33 });
        setAgents([
          { id: '1', name: 'DeFi Risk Calibration Pack v2.1', memory: 'DeFi:risk-assessment', status: 'Healthy', trust_score: 92.5, transfer_efficiency: 92.2, last_eval: '2026-04-23' },
          { id: '2', name: 'CVE Severity Scorer v1.8', memory: 'CyberSec:vulnerability-assessment', status: 'Healthy', trust_score: 94.2, transfer_efficiency: 95.5, last_eval: '2026-04-23' },
          { id: '3', name: 'Fraud Escalation Memory Pack v3.2', memory: 'Support:escalation', status: 'Healthy', trust_score: 93.4, transfer_efficiency: 94.1, last_eval: '2026-04-23' },
        ] as any);
        setAlerts([]);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="amm-page"><InlineLoading description="Loading control tower..." /></div>;

  const agentRows = agents.map((a) => ({
    id: a.id,
    name: a.name,
    memory: a.memory,
    status: a.status,
    trust: `${a.trust_score?.toFixed(1) ?? '—'}/100`,
    te: `${a.transfer_efficiency?.toFixed(1) ?? '—'}%`,
    lastEval: a.last_eval?.slice(0, 10) ?? '—',
  }));

  return (
    <div className="amm-page">
      <Grid fullWidth>
        <Column lg={16} md={8} sm={4}>
          <h1 className="amm-screen-title">Control tower</h1>
          <p className="amm-screen-subtitle">
            Watch live artifacts, verification posture, and drift state.
          </p>
        </Column>

        <Column lg={16} md={8} sm={4}>
          <div className="amm-metric-grid amm-section">
            <Tile className="amm-metric-tile">
              <span className="amm-subtle">Active listings</span>
              <span className="amm-metric-value">{stats?.active_listings ?? 0}</span>
            </Tile>
            <Tile className="amm-metric-tile">
              <span className="amm-subtle">Verifications</span>
              <span className="amm-metric-value">{stats?.verifications ?? 0}</span>
            </Tile>
            <Tile className="amm-metric-tile">
              <span className="amm-subtle">Feedback received</span>
              <span className="amm-metric-value">{stats?.feedback_received ?? 0}</span>
            </Tile>
            <Tile className="amm-metric-tile">
              <span className="amm-subtle">Monthly spend</span>
              <span className="amm-metric-value">${stats?.monthly_spend?.toFixed(0) ?? 0}</span>
            </Tile>
          </div>
        </Column>

        <Column lg={10} md={8} sm={4}>
          <Tile className="amm-card">
            <DataTable rows={agentRows} headers={agentHeaders}>
              {({ rows, headers, getHeaderProps, getRowProps, getTableProps }) => (
                <TableContainer title="Verified artifacts" description="Artifacts with verification certificates">
                  <Table {...getTableProps()} size="lg">
                    <TableHead>
                      <TableRow>
                        {headers.map((header) => {
                          const { key: _k, ...headerProps } = getHeaderProps({ header });
                          return (
                            <TableHeader key={header.key} {...headerProps}>
                              {header.header}
                            </TableHeader>
                          );
                        })}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {rows.map((row) => {
                        const source = agentRows.find((entry) => entry.id === row.id);
                        return (
                          <TableRow key={row.id}>
                            <TableCell><strong>{source?.name}</strong></TableCell>
                            <TableCell>{source?.memory}</TableCell>
                            <TableCell>
                              <StatusTag status={source?.status as any ?? 'Watch'} />
                            </TableCell>
                            <TableCell>{source?.trust}</TableCell>
                            <TableCell>{source?.te}</TableCell>
                            <TableCell>{source?.lastEval}</TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </DataTable>
          </Tile>
        </Column>

        <Column lg={6} md={8} sm={4}>
          <div className="amm-surface-stack">
            {alerts.length > 0 ? (
              alerts.map((alert) => (
                <InlineNotification
                  key={alert.id}
                  kind={alert.severity === 'Blocked' ? 'error' : alert.severity === 'Warning' ? 'warning' : 'info'}
                  title={alert.title}
                  subtitle={alert.summary}
                  hideCloseButton
                  lowContrast
                />
              ))
            ) : (
              <InlineNotification
                kind="success"
                title="All clear"
                subtitle="No drift alerts or safety issues detected."
                hideCloseButton
                lowContrast
              />
            )}
            <Tile className="amm-card">
              <h2>Policy</h2>
              <p className="amm-subtle">Auto-buy cap: $2,000</p>
              <p className="amm-subtle">Human approval above Medium risk</p>
              <p className="amm-subtle">Auto-revoke on negative transfer above 5%</p>
              <p className="amm-subtle">Allowed scope: retrieval only / no tool autonomy</p>
            </Tile>
          </div>
        </Column>
      </Grid>
    </div>
  );
}
