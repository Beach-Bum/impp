'use client';

import { Box, Button, Flash, Heading, Label } from '@primer/react';
import { PAYMENT_RAILS, getUserProfile } from '@/lib/directory';

export default function PaymentsScreen() {
  const user = getUserProfile();

  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Payments</Heading>
      <p className="amm-screen-subtitle">Configure settlement rails, x402 allowances, and payout safety controls.</p>

      <Flash variant="warning" sx={{ mb: 3 }}>
        <strong>Design default:</strong> use USDC escrow for standard purchases, x402 for A2A metered access, and fiat only as a fallback for human procurement.
      </Flash>

      <div className="amm-grid amm-grid-2col">
        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Buyer wallet</Heading>
          <span className="amm-subtle" style={{ display: 'block' }}>Owner: {user.displayName}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Org: {user.orgName}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Address: {user.walletAddress}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Default rail: {user.defaultPaymentRail}</span>
          <div style={{ marginTop: '12px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <Label variant="success">Verified buyer</Label>
            <Label variant="accent">Escrow enabled</Label>
            <Label variant="attention">Spend cap active</Label>
          </div>
        </Box>

        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Policy</Heading>
          <span className="amm-subtle" style={{ display: 'block' }}>{user.spendingPolicy}</span>
          <span className="amm-subtle" style={{ display: 'block', marginTop: '8px' }}>{user.moderationPolicy}</span>
          <div style={{ marginTop: '12px' }}>
            {user.purchaseApprovals.map((item) => (
              <Label key={item} variant="secondary" sx={{ mr: 1, mb: 1 }}>{item}</Label>
            ))}
          </div>
        </Box>
      </div>

      <div className="amm-card-stack" style={{ marginTop: '24px' }}>
        {PAYMENT_RAILS.map((rail) => (
          <Box key={rail.id} sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap' }}>
              <div>
                <Heading as="h2" sx={{ fontSize: 2, mb: 1 }}>{rail.label}</Heading>
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
          </Box>
        ))}
      </div>

      <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3, mt: 3 }}>
        <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>x402 / A2A wallet stance</Heading>
        <span className="amm-subtle" style={{ display: 'block' }}>Use x402 for machine-native access control, metered retrieval, proof-of-payment routing, and capability-gated artifact APIs.</span>
        <span className="amm-subtle" style={{ display: 'block' }}>Require signed request envelopes, nonces, replay protection, artifact-specific allowances, and max-spend ceilings.</span>
      </Box>
    </div>
  );
}
