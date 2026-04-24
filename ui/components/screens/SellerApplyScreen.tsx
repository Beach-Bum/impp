'use client';

import { Box, Button, Heading, Label, Select, TextInput, Textarea } from '@primer/react';

export default function SellerApplyScreen() {
  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Request seller access</Heading>
      <p className="amm-screen-subtitle">
        Apply to list memory artifacts, connect payout rails, and begin marketplace verification.
      </p>

      <div className="amm-grid amm-grid-2col">
        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Seller application</Heading>
          <div className="amm-card-stack">
            <TextInput placeholder="Name or organization" block />
            <TextInput placeholder="Contact email" block />
            <TextInput placeholder="Payout wallet" block />
            <Select block defaultValue="verified">
              <Select.Option value="verified">Verified seller</Select.Option>
              <Select.Option value="institutional">Institutional seller</Select.Option>
              <Select.Option value="agent-wallet">Agent wallet seller</Select.Option>
            </Select>
            <Textarea placeholder="Describe the memory artifacts you want to list" rows={5} block />
            <Button>Submit application</Button>
          </div>
        </Box>

        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Verification requirements</Heading>
          <div className="amm-inline-tags" style={{ marginBottom: '12px' }}>
            <Label variant="success">Identity</Label>
            <Label variant="accent">Stake</Label>
            <Label variant="secondary">Escrow</Label>
          </div>
          <div className="amm-card-stack">
            <span className="amm-subtle">• Identity or org verification is required before public listing.</span>
            <span className="amm-subtle">• Sellers may need collateral or delayed payout release depending on trust tier.</span>
            <span className="amm-subtle">• Agent-wallet sellers should expect signed allowance and spend-cap requirements.</span>
          </div>
        </Box>
      </div>
    </div>
  );
}
