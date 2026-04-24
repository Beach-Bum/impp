'use client';

import { Button, Heading, Label } from '@primer/react';
import { getUserProfile } from '@/lib/directory';

export default function ProfileScreen() {
  const user = getUserProfile();

  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>My profile</Heading>
      <p className="amm-screen-subtitle">Buyer identity, verification posture, wallet defaults, and marketplace guardrails.</p>

      <div className="amm-grid amm-grid-2col">
        <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" style={{ fontSize: '16px', marginBottom: '8px' }}>Identity</Heading>
          <span className="amm-subtle" style={{ display: 'block' }}>Name: {user.displayName}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Handle: {user.handle}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Role: {user.role}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Org: {user.orgName}</span>
          <div className="amm-inline-tags" style={{ marginTop: '12px' }}>
            <Label variant="success">{user.verifiedTier}</Label>
            <Label variant="accent">Verified buyer</Label>
          </div>
        </div>

        <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" style={{ fontSize: '16px', marginBottom: '8px' }}>Wallet</Heading>
          <span className="amm-subtle" style={{ display: 'block' }}>Address: {user.walletAddress}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Default rail: {user.defaultPaymentRail}</span>
          <div style={{ marginTop: '12px', display: 'flex', gap: '8px' }}>
            <Button as="a" href="/payments">Manage payments</Button>
            <Button as="a" href="/transactions" variant="invisible">Transactions</Button>
          </div>
        </div>
      </div>

      <div className="amm-grid amm-grid-2col" style={{ marginTop: '24px' }}>
        <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" style={{ fontSize: '16px', marginBottom: '8px' }}>Spending policy</Heading>
          <p style={{ marginTop: 0 }}>{user.spendingPolicy}</p>
        </div>
        <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" style={{ fontSize: '16px', marginBottom: '8px' }}>Moderation policy</Heading>
          <p style={{ marginTop: 0 }}>{user.moderationPolicy}</p>
          <div className="amm-inline-tags">
            {user.purchaseApprovals.map((item) => <Label key={item} variant="secondary">{item}</Label>)}
          </div>
        </div>
      </div>
    </div>
  );
}
