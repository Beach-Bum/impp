'use client';

import Link from 'next/link';
import { Button, Heading, Label } from '@primer/react';

type RunMetrics = {
  transfer_efficiency: number;
  adversarial_score: number;
  trust_score: number;
  training_accuracy: number;
  heldout_accuracy: number;
  negative_transfer_risk: string;
  freshness_days: number;
};

type EvalRun = {
  id: string;
  artifact: string;
  domain: string;
  model: string;
  date: string;
  status: string;
  metrics: RunMetrics;
  recommendation: string;
};

function getMockRun(runId: string): EvalRun {
  return {
    id: runId,
    artifact: 'DeFi Risk Calibration Pack v2.1',
    domain: 'DeFi:risk-assessment',
    model: 'GPT-4o',
    date: '2026-04-23',
    status: 'completed',
    metrics: {
      transfer_efficiency: 92.2,
      adversarial_score: 12.0,
      trust_score: 92.5,
      training_accuracy: 94.1,
      heldout_accuracy: 89.3,
      negative_transfer_risk: 'Low',
      freshness_days: 12,
    },
    recommendation: 'Ready to attach — scoped deployment recommended',
  };
}

const scorecard = (metrics: RunMetrics) => [
  ['Transfer efficiency', `${metrics.transfer_efficiency}%`],
  ['Adversarial score', `${metrics.adversarial_score}%`],
  ['Trust score', `${metrics.trust_score}/100`],
  ['Training accuracy', `${metrics.training_accuracy}%`],
  ['Held-out accuracy', `${metrics.heldout_accuracy}%`],
  ['Negative transfer risk', metrics.negative_transfer_risk],
  ['Freshness', `${metrics.freshness_days} days`],
];

export default function SandboxDetailScreen({ runId }: { runId: string }) {
  const run = getMockRun(runId);

  const statusVariant =
    run.status === 'completed' ? 'success' : run.status === 'failed' ? 'danger' : 'attention';

  const accuracyGap = (run.metrics.training_accuracy - run.metrics.heldout_accuracy).toFixed(1);
  const gapVariant = parseFloat(accuracyGap) <= 5 ? 'success' : 'attention';

  return (
    <div className="amm-page">
      {/* Back link */}
      <div style={{ marginBottom: '16px' }}>
        <Link
          href="/sandbox"
          style={{ fontSize: '13px', color: 'var(--fgColor-accent, #0969da)', textDecoration: 'none' }}
        >
          ← Back to Sandbox
        </Link>
      </div>

      {/* Header */}
      <div style={{ marginBottom: '20px' }}>
        <Heading style={{ marginBottom: '4px' }}>{run.artifact}</Heading>
        <p className="amm-subtle" style={{ margin: '0 0 10px' }}>
          Run ID: <code style={{ fontSize: '11px', background: 'var(--bgColor-muted, #f6f8fa)', padding: '1px 5px', borderRadius: '3px' }}>{run.id}</code>
        </p>
        <div className="amm-inline-tags">
          <Label>{run.domain}</Label>
          <Label variant="accent">{run.model}</Label>
          <Label variant={statusVariant}>{run.status}</Label>
          <span className="amm-subtle" style={{ alignSelf: 'center', fontSize: '12px' }}>{run.date}</span>
        </div>
      </div>

      <div className="amm-grid amm-grid-2col">
        {/* Scorecard */}
        <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Evaluation scorecard</Heading>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
            <tbody>
              {scorecard(run.metrics).map(([label, value]) => (
                <tr
                  key={label}
                  style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}
                >
                  <td style={{ padding: '8px 0', fontWeight: 600 }}>{label}</td>
                  <td style={{ padding: '8px 0' }}>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Right column: accuracy comparison + recommendation */}
        <div className="amm-card-stack" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Training vs held-out accuracy */}
          <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
            <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Accuracy comparison</Heading>
            <div className="amm-metric-grid" style={{ marginBottom: '12px' }}>
              <div className="amm-metric-tile" style={{ flex: 1 }}>
                <div className="amm-metric-label">Training</div>
                <span className="amm-metric-value">{run.metrics.training_accuracy}%</span>
              </div>
              <div className="amm-metric-tile" style={{ flex: 1 }}>
                <div className="amm-metric-label">Held-out</div>
                <span className="amm-metric-value">{run.metrics.heldout_accuracy}%</span>
              </div>
            </div>
            <div className="amm-inline-tags">
              <Label variant={gapVariant}>Gap: {accuracyGap}pp</Label>
              <span className="amm-subtle" style={{ fontSize: '11px', alignSelf: 'center' }}>
                {parseFloat(accuracyGap) <= 5 ? 'Low generalization risk' : 'Monitor generalization'}
              </span>
            </div>
          </div>

          {/* Recommendation */}
          <div
            style={{
              border: '1px solid var(--borderColor-success-emphasis, #2da44e)',
              borderRadius: '6px',
              padding: '16px',
              backgroundColor: 'var(--bgColor-success-subtle, #dafbe1)',
            }}
          >
            <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Recommendation</Heading>
            <p style={{ margin: '0 0 12px', fontSize: '13px' }}>{run.recommendation}</p>
            <div className="amm-action-row">
              <Button variant="primary" size="small">Attach artifact</Button>
              <Button variant="invisible" size="small">Export report</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
