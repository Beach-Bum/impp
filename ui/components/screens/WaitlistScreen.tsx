'use client';

import { Box, Button, Heading, Label, TextInput, Textarea } from '@primer/react';

export default function WaitlistScreen() {
  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Join the waitlist</Heading>
      <p className="amm-screen-subtitle">
        Get updates on verified seller onboarding, sandbox access, and private-market features.
      </p>

      <div className="amm-grid amm-grid-2col">
        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Request access</Heading>
          <div className="amm-card-stack">
            <TextInput placeholder="Email address" block />
            <TextInput placeholder="Name or team" block />
            <TextInput placeholder="Company" block />
            <Textarea placeholder="What do you want to use Memory Market for?" rows={5} block />
            <Button>Join waitlist</Button>
          </div>
        </Box>

        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>What you’ll get</Heading>
          <div className="amm-inline-tags" style={{ marginBottom: '12px' }}>
            <Label variant="accent">Sandbox access</Label>
            <Label variant="secondary">Seller onboarding</Label>
            <Label variant="secondary">Private markets</Label>
          </div>
          <div className="amm-card-stack">
            <span className="amm-subtle">• Early access to sandbox scorecards and artifact trials</span>
            <span className="amm-subtle">• Updates on buyer, seller, and agent-wallet onboarding</span>
            <span className="amm-subtle">• Access to escrow, x402, and enterprise policy features</span>
          </div>
        </Box>
      </div>
    </div>
  );
}
