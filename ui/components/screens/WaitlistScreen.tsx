'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

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
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Join the waitlist</h1>
      <p className="mb-6 text-sm text-muted-foreground">
        Get updates on verified seller onboarding, sandbox access, and private-market features.
      </p>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Request access</CardTitle></CardHeader>
          <CardContent>
            {success ? (
              <p className="text-sm text-green-600 dark:text-green-400">Thanks! We&apos;ll be in touch.</p>
            ) : (
              <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                <Input
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  type="email"
                  required
                />
                <Input
                  placeholder="Name or team"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
                <Input
                  placeholder="Company"
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                />
                <Textarea
                  placeholder="What do you want to use Memory Market for?"
                  rows={5}
                  value={useCase}
                  onChange={(e) => setUseCase(e.target.value)}
                />
                <Button type="submit" disabled={loading}>
                  {loading ? 'Submitting...' : 'Join waitlist'}
                </Button>
                {error && <p className="text-sm text-destructive">{error}</p>}
              </form>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-xl font-light">What you&apos;ll get</CardTitle></CardHeader>
          <CardContent>
            <div className="mb-3 flex flex-wrap gap-1">
              <Badge>Sandbox access</Badge>
              <Badge variant="secondary">Seller onboarding</Badge>
              <Badge variant="outline">Private markets</Badge>
            </div>
            <div className="space-y-2 text-sm text-muted-foreground">
              <div>Early access to sandbox scorecards and artifact trials</div>
              <div>Updates on buyer, seller, and agent-wallet onboarding</div>
              <div>Access to escrow, x402, and enterprise policy features</div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
