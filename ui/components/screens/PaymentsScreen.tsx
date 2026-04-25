'use client';

import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Spinner } from '@/components/ui/spinner';
import { fetchUserProfile, type UserProfileRecord } from '@/lib/api';
import { PAYMENT_RAILS } from '@/lib/directory';

export default function PaymentsScreen() {
  const [user, setUser] = useState<UserProfileRecord | null>(null);

  useEffect(() => {
    fetchUserProfile().then(setUser);
  }, []);

  if (!user) return <div className="mx-auto max-w-5xl px-5 py-8"><Spinner /></div>;

  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Payments</h1>
      <p className="mb-6 text-sm text-muted-foreground">Configure settlement rails, x402 allowances, and payout safety controls.</p>

      <Alert className="mb-4">
        <AlertDescription>
          <strong>Design default:</strong> use USDC escrow for standard purchases, x402 for A2A metered access, and fiat only as a fallback for human procurement.
        </AlertDescription>
      </Alert>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Buyer wallet</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-1 text-sm text-muted-foreground">
              <div>Owner: {user.displayName}</div>
              <div>Org: {user.orgName}</div>
              <div>Address: {user.walletAddress}</div>
              <div>Default rail: {user.defaultPaymentRail}</div>
            </div>
            <div className="mt-3 flex flex-wrap gap-1">
              <Badge>Verified buyer</Badge>
              <Badge variant="secondary">Escrow enabled</Badge>
              <Badge variant="outline">Spend cap active</Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Policy</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-2 text-sm text-muted-foreground">
              <div>{user.spendingPolicy}</div>
              <div>{user.moderationPolicy}</div>
            </div>
            <div className="mt-3 flex flex-wrap gap-1">
              {user.purchaseApprovals.map((item) => <Badge key={item} variant="outline">{item}</Badge>)}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="mt-6 flex flex-col gap-3 border-t pt-6">
        {PAYMENT_RAILS.map((rail) => (
          <Card key={rail.id}>
            <CardContent className="pt-6">
              <div className="flex flex-wrap justify-between gap-3">
                <div>
                  <h2 className="mb-1 text-xl font-light">{rail.label}</h2>
                  <p className="mb-2 text-sm leading-relaxed">{rail.useCase}</p>
                  <span className="text-sm text-muted-foreground">Settlement: {rail.settlement}</span>
                </div>
                <div className="flex items-start gap-2">
                  <Button>Select</Button>
                  <Button variant="ghost">Configure</Button>
                </div>
              </div>
              <div className="mt-3 flex flex-wrap gap-1">
                {rail.riskControls.map((control) => <Badge key={control} variant="outline">{control}</Badge>)}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="mt-6">
        <CardHeader><CardTitle className="text-xl font-light">x402 / A2A wallet stance</CardTitle></CardHeader>
        <CardContent className="space-y-1 text-sm text-muted-foreground">
          <div>Use x402 for machine-native access control, metered retrieval, proof-of-payment routing, and capability-gated artifact APIs.</div>
          <div>Require signed request envelopes, nonces, replay protection, artifact-specific allowances, and max-spend ceilings.</div>
        </CardContent>
      </Card>
    </div>
  );
}
