'use client';

import Link from 'next/link';
import { Box, Button, Heading, Label, TextInput, Select } from '@primer/react';

export default function SignupScreen() {
  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Create your account</Heading>
      <p className="amm-screen-subtitle">
        Start with email, social, or wallet, then choose whether you are joining as a buyer, seller, or agent wallet.
      </p>

      <div className="amm-grid amm-grid-2col">
        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Sign up</Heading>
          <div className="amm-card-stack">
            <TextInput placeholder="Email address" block />
            <TextInput placeholder="Organization or team" block />
            <Select block defaultValue="buyer">
              <Select.Option value="buyer">Buyer</Select.Option>
              <Select.Option value="seller">Seller</Select.Option>
              <Select.Option value="agent-wallet">Agent Wallet</Select.Option>
            </Select>
            <div className="amm-action-row" style={{ flexWrap: 'wrap' }}>
              <Button>Continue with email</Button>
              <Button variant="invisible">Continue with Google</Button>
              <Button variant="invisible">Continue with wallet</Button>
            </div>
          </div>
        </Box>

        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Recommended auth model</Heading>
          <div className="amm-inline-tags" style={{ marginBottom: '12px' }}>
            <Label variant="accent">Privy</Label>
            <Label variant="secondary">Embedded wallet</Label>
            <Label variant="secondary">Wallet connect</Label>
          </div>
          <div className="amm-card-stack">
            <span className="amm-subtle">• Human users should be able to start with email or social auth.</span>
            <span className="amm-subtle">• Wallets should be connectable or created on demand.</span>
            <span className="amm-subtle">• Agent-wallet accounts should route into spend-cap and allowance setup.</span>
          </div>
          <div className="amm-action-row" style={{ marginTop: '1rem', flexWrap: 'wrap' }}>
            <Button as={Link} href="/waitlist" variant="invisible">Join waitlist</Button>
            <Button as={Link} href="/seller-apply" variant="invisible">Request seller access</Button>
          </div>
        </Box>
      </div>
    </div>
  );
}
