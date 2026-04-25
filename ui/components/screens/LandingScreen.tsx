'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { RippleButton, RippleButtonRipples } from '@/components/animate-ui/components/buttons/ripple';

const trustPoints = [
  'Verified sellers',
  'Sandbox before attach',
  'Escrow and agent-wallet payments',
  'Audit trails and rollback controls',
];

const howItWorks = [
  {
    title: 'Upload and verify',
    body: 'Sellers submit memory artifacts. Referees verify transfer, safety, and adversarial resilience before anything is listed.',
  },
  {
    title: 'Compare and audit',
    body: 'Buyers compare artifacts side by side, inspect seller trust posture, and review the audit envelope before purchase.',
  },
  {
    title: 'Sandbox and deploy',
    body: 'Run a scoped evaluation, inspect scorecards, then attach via controlled payment rails and rollback policies.',
  },
];

const businessModel = [
  'Marketplace take rate on primary sales',
  'Verification and premium listing fees',
  'Sandbox and evaluation credits',
  'Escrow / payout routing fees',
  'Enterprise subscriptions for private markets and policy controls',
];

export default function LandingScreen() {
  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <div className="grid gap-8 lg:grid-cols-2">
        <div>
          <Badge className="mb-2">memorymarket.ai</Badge>
          <h1 className="mb-4 text-4xl font-light leading-tight">
            The marketplace for verified agent memory.
          </h1>
          <p className="mb-4 text-lg text-muted-foreground" style={{ maxWidth: 760 }}>
            Buy, compare, audit, and deploy verified memory artifacts for AI agents with seller verification, sandbox testing, and controlled payment rails.
          </p>
          <div className="flex flex-wrap gap-2">
            <Link href="/leaderboard">
              <RippleButton>
                Browse market
                <RippleButtonRipples />
              </RippleButton>
            </Link>
            <Link href="/signup">
              <RippleButton variant="ghost">
                Create account
                <RippleButtonRipples />
              </RippleButton>
            </Link>
            <Link href="/sandbox">
              <RippleButton variant="ghost">
                Open sandbox
                <RippleButtonRipples />
              </RippleButton>
            </Link>
          </div>
        </div>
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Why buyers trust it</CardTitle></CardHeader>
          <CardContent>
            <div className="mb-3 flex flex-wrap gap-1">
              <Badge>Verified</Badge>
              <Badge variant="secondary">Sandboxed</Badge>
              <Badge variant="outline">Escrow-ready</Badge>
            </div>
            <div className="space-y-1.5 text-sm text-muted-foreground">
              {trustPoints.map((point) => (
                <div key={point}>{point}</div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8 grid gap-6 sm:grid-cols-3">
        {howItWorks.map((item) => (
          <Card key={item.title}>
            <CardHeader><CardTitle className="text-xl font-light">{item.title}</CardTitle></CardHeader>
            <CardContent><p className="text-sm">{item.body}</p></CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-8 grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">How Memory Market makes money</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-1.5 text-sm text-muted-foreground">
              {businessModel.map((line) => (
                <div key={line}>{line}</div>
              ))}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Get started</CardTitle></CardHeader>
          <CardContent className="flex flex-col gap-2">
            <Button render={<Link href="/waitlist" />}>Join waitlist</Button>
            <Button variant="ghost" render={<Link href="/seller-apply" />}>Request seller access</Button>
            <Button variant="ghost" render={<Link href="/preview/payments" />}>View payment rails</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
