'use client';

import { useEffect, useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Spinner } from '@/components/ui/spinner';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

type PortfolioAgent = { id: string; name: string; memory: string; status: string; trust_score: number; transfer_efficiency: number; last_eval: string };
type PortfolioAlert = { id: string; title: string; severity: string; summary: string };

function statusVariant(s: string): 'default' | 'destructive' | 'secondary' | 'outline' {
  if (s === 'Healthy') return 'default';
  if (s === 'Blocked') return 'destructive';
  if (s === 'Warning') return 'outline';
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

  if (loading) return <div className="mx-auto max-w-5xl px-5 py-8"><Spinner /></div>;

  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Control tower</h1>
      <p className="mb-6 text-sm text-muted-foreground">Watch live artifacts, verification posture, and drift state.</p>

      <div className="mb-8 grid grid-cols-2 gap-4 md:grid-cols-4">
        {[
          ['Active listings', stats?.active_listings ?? 0],
          ['Verifications', stats?.verifications ?? 0],
          ['Feedback', stats?.feedback_received ?? 0],
          ['Monthly spend', `$${stats?.monthly_spend?.toFixed(0) ?? 0}`],
        ].map(([label, value]) => (
          <Card key={String(label)}>
            <CardContent className="pt-4">
              <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{label}</div>
              <div className="mt-1 text-xl font-semibold">{value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Verified artifacts</CardTitle></CardHeader>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Artifact</TableHead>
                  <TableHead>Domain</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Trust</TableHead>
                  <TableHead>Transfer Eff.</TableHead>
                  <TableHead>Last eval</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {agents.map((a) => (
                  <TableRow key={a.id}>
                    <TableCell className="font-semibold">{a.name}</TableCell>
                    <TableCell>{a.memory}</TableCell>
                    <TableCell><Badge variant={statusVariant(a.status)}>{a.status}</Badge></TableCell>
                    <TableCell>{a.trust_score?.toFixed(1)}/100</TableCell>
                    <TableCell>{a.transfer_efficiency?.toFixed(1)}%</TableCell>
                    <TableCell>{a.last_eval?.slice(0, 10)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <div className="flex flex-col gap-3">
          {alerts.length > 0 ? alerts.map((a) => (
            <Alert key={a.id} variant={a.severity === 'Blocked' ? 'destructive' : 'default'}>
              <AlertTitle>{a.title}</AlertTitle>
              <AlertDescription>{a.summary}</AlertDescription>
            </Alert>
          )) : (
            <Alert>
              <AlertTitle>All clear</AlertTitle>
              <AlertDescription>No drift alerts or safety issues.</AlertDescription>
            </Alert>
          )}
          <Card>
            <CardHeader><CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Policy</CardTitle></CardHeader>
            <CardContent className="space-y-1 text-sm text-muted-foreground">
              <div>Auto-buy cap: $2,000</div>
              <div>Human approval above Medium risk</div>
              <div>Auto-revoke on negative transfer &gt; 5%</div>
              <div>Scope: retrieval only / no tool autonomy</div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
