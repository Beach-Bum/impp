'use client';

import { useState } from 'react';
import { Button, Heading, Label, Select, TextInput, Textarea } from '@primer/react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

export default function SellerApplyScreen() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [wallet, setWallet] = useState('');
  const [sellerType, setSellerType] = useState('verified');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_BASE}/api/seller-apply`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, wallet, seller_type: sellerType, description }),
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
      <Heading style={{ marginBottom: '4px' }}>Request seller access</Heading>
      <p className="amm-screen-subtitle">
        Apply to list memory artifacts, connect payout rails, and begin marketplace verification.
      </p>

      <div className="amm-grid amm-grid-2col">
        <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" style={{ fontSize: "16px", marginBottom: "8px" }}>Seller application</Heading>
          {success ? (
            <p style={{ color: 'var(--fgColor-success, green)' }}>Thanks! We'll be in touch.</p>
          ) : (
            <form onSubmit={handleSubmit}>
              <div className="amm-card-stack">
                <TextInput
                  placeholder="Name or organization"
                  block
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
                <TextInput
                  placeholder="Contact email"
                  block
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  type="email"
                  required
                />
                <TextInput
                  placeholder="Payout wallet"
                  block
                  value={wallet}
                  onChange={(e) => setWallet(e.target.value)}
                />
                <Select
                  block
                  value={sellerType}
                  onChange={(e) => setSellerType(e.target.value)}
                >
                  <Select.Option value="verified">Verified seller</Select.Option>
                  <Select.Option value="institutional">Institutional seller</Select.Option>
                  <Select.Option value="agent-wallet">Agent wallet seller</Select.Option>
                </Select>
                <Textarea
                  placeholder="Describe the memory artifacts you want to list"
                  rows={5}
                  block
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
                <Button type="submit" disabled={loading}>
                  {loading ? 'Submitting...' : 'Submit application'}
                </Button>
                {error && <span style={{ color: 'var(--fgColor-danger, red)', fontSize: '14px' }}>{error}</span>}
              </div>
            </form>
          )}
        </div>

        <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" style={{ fontSize: "16px", marginBottom: "8px" }}>Verification requirements</Heading>
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
        </div>
      </div>
    </div>
  );
}
