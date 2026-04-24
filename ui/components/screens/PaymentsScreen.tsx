'use client';

import { Button, Flash, Heading, Label } from '@primer/react';
import { PAYMENT_RAILS, getUserProfile } from '@/lib/directory';

export default function PaymentsScreen() {
  const user = getUserProfile();

  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Payments</Heading>
      <p className="amm-screen-subtitle">Configure settlement rails, x402 allowances, and payout safety controls.</p>

      <Flash variant="warning" style={{ marginBottom: '16px' }}>
        <strong>Design default:</strong> use USDC escrow for standard purchases, x402 for A2A metered access, and fiat only as a fallback for human procurement.
      </Flash>

      <div className="amm-grid amm-grid-2col">
        <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" style={{ fontSize: '16px', marginBottom: '8px' }}>Buyer wallet</Heading>
          <span className="amm-subtle" style={{ display: 'block' }}>Owner: {user.displayName}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Org: {user.orgName}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Address: {user.walletAddress}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Default rail: {user.defaultPaymentRail}</span>
          <div style={{ marginTop: '12px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <Label variant="success">Verified buyer</Label>
            <Label variant="accent">Escrow enabled</Label>
            <Label variant="attention">Spend cap active</Label>
          </div>
        </div>

        <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" style={{ fontSize: '16px', marginBottom: '8px' }}>Policy</Heading>
          <span className="amm-subtle" style={{ display: 'block' }}>{user.spendingPolicy}</span>
          <span className="amm-subtle" style={{ display: 'block', marginTop: '8px' }}>{user.moderationPolicy}</span>
          <div style={{ marginTop: '12px' }}>
            {user.purchaseApprovals.map((item) => (
              <Label key={item} variant="secondary" style={{ marginRight: '4px', marginBottom: '4px' }}>{item}</Label>
            ))}
          </div>
        </div>
      </div>

      <div className="amm-card-stack" style={{ marginTop: '24px' }}>
        {PAYMENT_RAILS.map((rail) => (
          <div key={rail.id} style={{ border: '1px solid #d0d7de', borderRadius: '6px', padding: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
              <div>
                <Heading as="h2" style={{ fontSize: '16px', marginBottom: '4px' }}>{rail.label}</Heading>
                <p style={{ marginTop: 0, marginBottom: '8px' }}>{rail.useCase}</p>
                <span className="amm-subtle" style={{ display: 'block' }}>Settlement: {rail.settlement}</span>
              </div>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-start', flexWrap: 'wrap' }}>
                <Button variant="primary">Select</Button>
                <Button variant="invisible">Configure</Button>
              </div>
            </div>
            <div className="amm-inline-tags" style={{ marginTop: '12px' }}>
              {rail.riskControls.map((control) => (
                <Label key={control} variant="secondary">{control}</Label>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', padding: '16px', marginTop: '16px' }}>
        <Heading as="h2" style={{ fontSize: '16px', marginBottom: '8px' }}>x402 / A2A wallet stance</Heading>
        <span className="amm-subtle" style={{ display: 'block' }}>Use x402 for machine-native access control, metered retrieval, proof-of-payment routing, and capability-gated artifact APIs.</span>
        <span className="amm-subtle" style={{ display: 'block' }}>Require signed request envelopes, nonces, replay protection, artifact-specific allowances, and max-spend ceilings.</span>
      </div>
    </div>
  );
}
