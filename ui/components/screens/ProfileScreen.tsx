'use client';

import { Box, Button, Heading, Label } from '@primer/react';
import { getUserProfile } from '@/lib/directory';

export default function ProfileScreen() {
  const user = getUserProfile();

  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>My profile</Heading>
      <p className="amm-screen-subtitle">Buyer identity, verification posture, wallet defaults, and marketplace guardrails.</p>

      <div className="amm-grid amm-grid-2col">
        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Identity</Heading>
          <span className="amm-subtle" style={{ display: 'block' }}>Name: {user.displayName}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Handle: {user.handle}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Role: {user.role}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Org: {user.orgName}</span>
          <div className="amm-inline-tags" style={{ marginTop: '12px' }}>
            <Label variant="success">{user.verifiedTier}</Label>
            <Label variant="accent">Verified buyer</Label>
          </div>
        </Box>

        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Wallet</Heading>
          <span className="amm-subtle" style={{ display: 'block' }}>Address: {user.walletAddress}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Default rail: {user.defaultPaymentRail}</span>
          <div style={{ marginTop: '12px', display: 'flex', gap: '8px' }}>
            <Button as="a" href="/payments">Manage payments</Button>
            <Button as="a" href="/transactions" variant="invisible">Transactions</Button>
          </div>
        </Box>
      </div>

      <div className="amm-grid amm-grid-2col" style={{ marginTop: '24px' }}>
        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Spending policy</Heading>
          <p style={{ marginTop: 0 }}>{user.spendingPolicy}</p>
        </Box>
        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Moderation policy</Heading>
          <p style={{ marginTop: 0 }}>{user.moderationPolicy}</p>
          <div className="amm-inline-tags">
            {user.purchaseApprovals.map((item) => <Label key={item} variant="secondary">{item}</Label>)}
          </div>
        </Box>
      </div>
    </div>
  );
}
