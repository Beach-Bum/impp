'use client';

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { getUserProfile } from '@/lib/directory';

export default function ProfileScreen() {
  const user = getUserProfile();

  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">My profile</h1>
      <p className="mb-6 text-sm text-muted-foreground">Buyer identity, verification posture, wallet defaults, and marketplace guardrails.</p>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Identity</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-1 text-sm text-muted-foreground">
              <div>Name: {user.displayName}</div>
              <div>Handle: {user.handle}</div>
              <div>Role: {user.role}</div>
              <div>Org: {user.orgName}</div>
            </div>
            <div className="mt-3 flex flex-wrap gap-1">
              <Badge>{user.verifiedTier}</Badge>
              <Badge variant="secondary">Verified buyer</Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Wallet</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-1 text-sm text-muted-foreground">
              <div>Address: {user.walletAddress}</div>
              <div>Default rail: {user.defaultPaymentRail}</div>
            </div>
            <div className="mt-3 flex gap-2">
              <Button render={<a href="/payments" />}>Manage payments</Button>
              <Button variant="ghost" render={<a href="/transactions" />}>Transactions</Button>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="mt-6 grid gap-8 border-t pt-6 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Spending policy</CardTitle></CardHeader>
          <CardContent><p className="text-sm leading-relaxed">{user.spendingPolicy}</p></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Moderation policy</CardTitle></CardHeader>
          <CardContent>
            <p className="text-sm leading-relaxed">{user.moderationPolicy}</p>
            <div className="mt-2 flex flex-wrap gap-1">
              {user.purchaseApprovals.map((item) => <Badge key={item} variant="outline">{item}</Badge>)}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
