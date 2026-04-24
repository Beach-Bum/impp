'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button, Heading, Label, TextInput, Select, Flash } from '@primer/react';

const PRIVY_ENABLED = !!process.env.NEXT_PUBLIC_PRIVY_APP_ID;

export default function SignupScreen() {
  const [email, setEmail] = useState('');
  const [org, setOrg] = useState('');
  const [role, setRole] = useState('buyer');
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function handlePrivyLogin() {
    // When @privy-io/react-auth is installed:
    // import { usePrivy } from '@privy-io/react-auth';
    // const { login } = usePrivy();
    // login();
    // For now, redirect to waitlist as a fallback
    window.location.href = '/waitlist';
  }

  async function handleEmailSignup() {
    if (!email) return;
    if (PRIVY_ENABLED) {
      // When Privy is wired, this will call login({ email })
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, name: org || email, company: org, use_case: role }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        setError(data.detail || 'Something went wrong. Please try again.');
      } else {
        setSubmitted(true);
      }
    } catch {
      setError('Could not reach the server. Please try again later.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Create your account</Heading>
      <p className="amm-screen-subtitle">
        Start with email, social, or wallet, then choose whether you are joining as a buyer, seller, or agent wallet.
      </p>

      <div className="amm-grid amm-grid-2col">
        <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" style={{ fontSize: "16px", marginBottom: "8px" }}>Sign up</Heading>
          {submitted ? (
            <Flash variant="success">
              Thanks! We&apos;ll notify you at {email} when accounts are live.
            </Flash>
          ) : (
            <div className="amm-card-stack">
              {error && <Flash variant="danger">{error}</Flash>}
              <TextInput
                placeholder="Email address"
                block
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <TextInput
                placeholder="Organization or team"
                block
                value={org}
                onChange={(e) => setOrg(e.target.value)}
              />
              <Select block value={role} onChange={(e) => setRole(e.target.value)}>
                <Select.Option value="buyer">Buyer</Select.Option>
                <Select.Option value="seller">Seller</Select.Option>
                <Select.Option value="agent-wallet">Agent Wallet</Select.Option>
              </Select>
              <div className="amm-action-row" style={{ flexWrap: 'wrap' }}>
                <Button onClick={handleEmailSignup} disabled={loading}>
                  {loading ? 'Submitting…' : 'Continue with email'}
                </Button>
                <Button variant="invisible" onClick={handlePrivyLogin}>
                  {PRIVY_ENABLED ? 'Continue with Google' : 'Join waitlist instead'}
                </Button>
                <Button variant="invisible" onClick={handlePrivyLogin}>
                  {PRIVY_ENABLED ? 'Continue with wallet' : 'Request seller access'}
                </Button>
              </div>
            </div>
          )}
        </div>

        <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" style={{ fontSize: "16px", marginBottom: "8px" }}>Recommended auth model</Heading>
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
        </div>
      </div>
    </div>
  );
}
