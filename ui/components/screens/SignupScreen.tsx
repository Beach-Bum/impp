'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const PRIVY_ENABLED = !!process.env.NEXT_PUBLIC_PRIVY_APP_ID;

export default function SignupScreen() {
  const [email, setEmail] = useState('');
  const [org, setOrg] = useState('');
  const [role, setRole] = useState('buyer');
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function handlePrivyLogin() {
    window.location.href = '/waitlist';
  }

  async function handleEmailSignup() {
    if (!email) return;
    if (PRIVY_ENABLED) return;
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
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Create your account</h1>
      <p className="mb-6 text-sm text-muted-foreground">
        Start with email, social, or wallet, then choose whether you are joining as a buyer, seller, or agent wallet.
      </p>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Sign up</CardTitle></CardHeader>
          <CardContent>
            {submitted ? (
              <Alert>
                <AlertDescription>Thanks! We&apos;ll notify you at {email} when accounts are live.</AlertDescription>
              </Alert>
            ) : (
              <div className="flex flex-col gap-3">
                {error && <Alert variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>}
                <Input
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <Input
                  placeholder="Organization or team"
                  value={org}
                  onChange={(e) => setOrg(e.target.value)}
                />
                <Select value={role} onValueChange={(v) => v && setRole(v)}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="buyer">Buyer</SelectItem>
                    <SelectItem value="seller">Seller</SelectItem>
                    <SelectItem value="agent-wallet">Agent Wallet</SelectItem>
                  </SelectContent>
                </Select>
                <div className="flex flex-wrap gap-2">
                  <Button onClick={handleEmailSignup} disabled={loading}>
                    {loading ? 'Submitting...' : 'Continue with email'}
                  </Button>
                  <Button variant="ghost" onClick={handlePrivyLogin}>
                    {PRIVY_ENABLED ? 'Continue with Google' : 'Join waitlist instead'}
                  </Button>
                  <Button variant="ghost" onClick={handlePrivyLogin}>
                    {PRIVY_ENABLED ? 'Continue with wallet' : 'Request seller access'}
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Recommended auth model</CardTitle></CardHeader>
          <CardContent>
            <div className="mb-3 flex flex-wrap gap-1">
              <Badge variant="secondary">Privy</Badge>
              <Badge variant="outline">Embedded wallet</Badge>
              <Badge variant="outline">Wallet connect</Badge>
            </div>
            <div className="space-y-2 text-sm text-muted-foreground">
              <div>Human users should be able to start with email or social auth.</div>
              <div>Wallets should be connectable or created on demand.</div>
              <div>Agent-wallet accounts should route into spend-cap and allowance setup.</div>
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              <Button variant="ghost" render={<Link href="/waitlist" />}>Join waitlist</Button>
              <Button variant="ghost" render={<Link href="/seller-apply" />}>Request seller access</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
