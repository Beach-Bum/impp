'use client';

import Link from 'next/link';
import { Button, Heading, Label } from '@primer/react';

const trustPoints = [
  'Verified sellers',
  'Sandbox before attach',
  'Escrow and agent-wallet payments',
  'Audit trails and rollback controls',
];

const howItWorks = [
  {
    title: 'Upload and verify',
    body: 'Sellers submit memory artifacts. Referees verify transfer, safety, and adversarial resilience before anything is listed.',
  },
  {
    title: 'Compare and audit',
    body: 'Buyers compare artifacts side by side, inspect seller trust posture, and review the audit envelope before purchase.',
  },
  {
    title: 'Sandbox and deploy',
    body: 'Run a scoped evaluation, inspect scorecards, then attach via controlled payment rails and rollback policies.',
  },
];

const businessModel = [
  'Marketplace take rate on primary sales',
  'Verification and premium listing fees',
  'Sandbox and evaluation credits',
  'Escrow / payout routing fees',
  'Enterprise subscriptions for private markets and policy controls',
];

export default function LandingScreen() {
  return (
    <div className="amm-page">
      <div className="amm-hero">
        <div>
          <Label variant="accent" sx={{ mb: 2 }}>memorymarket.ai</Label>
          <Heading as="h1" sx={{ fontSize: 6, lineHeight: 1.1, mb: 3 }}>
            The marketplace for verified agent memory.
          </Heading>
          <p className="amm-screen-subtitle" style={{ fontSize: '1.1rem', maxWidth: 760 }}>
            Buy, compare, audit, and deploy verified memory artifacts for AI agents with seller verification, sandbox testing, and controlled payment rails.
          </p>
          <div className="amm-action-row" style={{ marginTop: '1rem', flexWrap: 'wrap' }}>
            <Button as={Link} href="/market">Browse market</Button>
            <Button as={Link} href="/signup" variant="invisible">Create account</Button>
            <Button as={Link} href="/sandbox" variant="invisible">Open sandbox</Button>
          </div>
        </div>
        <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '8px', padding: '16px', backgroundColor: 'var(--bgColor-muted, #f6f8fa)' }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Why buyers trust it</Heading>
          <div className="amm-inline-tags" style={{ marginBottom: '1rem' }}>
            <Label variant="success">Verified</Label>
            <Label variant="accent">Sandboxed</Label>
            <Label variant="secondary">Escrow-ready</Label>
          </div>
          <div className="amm-card-stack">
            {trustPoints.map((point) => (
              <span key={point} className="amm-subtle">• {point}</span>
            ))}
          </div>
        </div>
      </div>

      <div className="amm-grid amm-grid-3col" style={{ marginTop: '2rem' }}>
        {howItWorks.map((item) => (
          <div key={item.title} style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
            <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>{item.title}</Heading>
            <p style={{ margin: 0 }}>{item.body}</p>
          </div>
        ))}
      </div>

      <div className="amm-grid amm-grid-2col" style={{ marginTop: '2rem' }}>
        <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>How Memory Market makes money</Heading>
          <div className="amm-card-stack">
            {businessModel.map((line) => (
              <span key={line} className="amm-subtle">• {line}</span>
            ))}
          </div>
        </div>
        <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Get started</Heading>
          <div className="amm-card-stack">
            <Button as={Link} href="/waitlist">Join waitlist</Button>
            <Button as={Link} href="/seller-apply" variant="invisible">Request seller access</Button>
            <Button as={Link} href="/payments" variant="invisible">View payment rails</Button>
          </div>
        </div>
      </div>
    </div>
  );
}
