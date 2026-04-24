'use client';

import { useState } from 'react';
import { Box, Button, Heading, Label, TextInput, Textarea } from '@primer/react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

export default function WaitlistScreen() {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [company, setCompany] = useState('');
  const [useCase, setUseCase] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_BASE}/api/waitlist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, name, company, use_case: useCase }),
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      setSuccess(true);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Join the waitlist</Heading>
      <p className="amm-screen-subtitle">
        Get updates on verified seller onboarding, sandbox access, and private-market features.
      </p>

      <div className="amm-grid amm-grid-2col">
        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Request access</Heading>
          {success ? (
            <p style={{ color: 'var(--fgColor-success, green)' }}>Thanks! We'll be in touch.</p>
          ) : (
            <form onSubmit={handleSubmit}>
              <div className="amm-card-stack">
                <TextInput
                  placeholder="Email address"
                  block
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  type="email"
                  required
                />
                <TextInput
                  placeholder="Name or team"
                  block
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
                <TextInput
                  placeholder="Company"
                  block
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                />
                <Textarea
                  placeholder="What do you want to use Memory Market for?"
                  rows={5}
                  block
                  value={useCase}
                  onChange={(e) => setUseCase(e.target.value)}
                />
                <Button type="submit" disabled={loading}>
                  {loading ? 'Submitting...' : 'Join waitlist'}
                </Button>
                {error && <span style={{ color: 'var(--fgColor-danger, red)', fontSize: '14px' }}>{error}</span>}
              </div>
            </form>
          )}
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
