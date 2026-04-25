'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

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
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Request seller access</h1>
      <p className="mb-6 text-sm text-muted-foreground">
        Apply to list memory artifacts, connect payout rails, and begin marketplace verification.
      </p>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Seller application</CardTitle></CardHeader>
          <CardContent>
            {success ? (
              <p className="text-sm text-green-600 dark:text-green-400">Thanks! We&apos;ll be in touch.</p>
            ) : (
              <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                <Input
                  placeholder="Name or organization"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
                <Input
                  placeholder="Contact email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  type="email"
                  required
                />
                <Input
                  placeholder="Payout wallet"
                  value={wallet}
                  onChange={(e) => setWallet(e.target.value)}
                />
                <Select value={sellerType} onValueChange={(v) => v && setSellerType(v)}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="verified">Verified seller</SelectItem>
                    <SelectItem value="institutional">Institutional seller</SelectItem>
                    <SelectItem value="agent-wallet">Agent wallet seller</SelectItem>
                  </SelectContent>
                </Select>
                <Textarea
                  placeholder="Describe the memory artifacts you want to list"
                  rows={5}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
                <Button type="submit" disabled={loading}>
                  {loading ? 'Submitting...' : 'Submit application'}
                </Button>
                {error && <p className="text-sm text-destructive">{error}</p>}
              </form>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Verification requirements</CardTitle></CardHeader>
          <CardContent>
            <div className="mb-3 flex flex-wrap gap-1">
              <Badge>Identity</Badge>
              <Badge variant="secondary">Stake</Badge>
              <Badge variant="outline">Escrow</Badge>
            </div>
            <div className="space-y-2 text-sm text-muted-foreground">
              <div>Identity or org verification is required before public listing.</div>
              <div>Sellers may need collateral or delayed payout release depending on trust tier.</div>
              <div>Agent-wallet sellers should expect signed allowance and spend-cap requirements.</div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
