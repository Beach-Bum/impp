'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Spinner } from '@/components/ui/spinner';
import { fetchListings, type ListingRecord } from '@/lib/api';
import { getSellerListings, getSellerProfile } from '@/lib/directory';

export default function SellerProfileScreen({ sellerId }: { sellerId: string }) {
  const [listings, setListings] = useState<ListingRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const seller = getSellerProfile(sellerId);

  useEffect(() => {
    fetchListings().then(setListings).finally(() => setLoading(false));
  }, []);

  if (!seller) return <div className="mx-auto max-w-5xl px-5 py-8"><Alert variant="destructive"><AlertDescription>Seller not found.</AlertDescription></Alert></div>;

  const sellerListings = getSellerListings(listings, seller.id);

  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">{seller.name}</h1>
      <p className="mb-6 text-sm text-muted-foreground">Seller profile, verification, dispute posture, and wallet identity.</p>

      <div className="grid gap-8 lg:grid-cols-2">
        <div className="flex flex-col gap-3">
          <Card>
            <CardContent className="pt-6">
              <div className="mb-3 flex flex-wrap items-center gap-2">
                <Badge>{seller.verifiedTier}</Badge>
                <Badge variant="secondary">Rep {seller.reputation}</Badge>
                <Badge variant="secondary">Stake ${seller.stakingUsd.toLocaleString()}</Badge>
              </div>
              <p className="text-sm leading-relaxed">{seller.bio}</p>
              <div className="mt-3 space-y-1 text-sm text-muted-foreground">
                <div>Handle: {seller.handle}</div>
                <div>Location: {seller.location}</div>
                <div>Wallet rail: {seller.walletScheme}</div>
                <div>Joined: {seller.joinedAt}</div>
                {seller.website && <a href={seller.website} className="block hover:underline">{seller.website}</a>}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader><CardTitle className="text-xl font-light">Trust posture</CardTitle></CardHeader>
            <CardContent>
              <div className="mb-3 grid grid-cols-3 gap-4">
                {[
                  ['Deliveries', seller.successfulDeliveries],
                  ['Dispute rate', `${seller.disputeRatePct}%`],
                  ['Listings', seller.listedAssets],
                ].map(([label, value]) => (
                  <div key={String(label)} className="rounded-md border p-3">
                    <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{label}</div>
                    <div className="mt-1 text-lg font-semibold">{value}</div>
                  </div>
                ))}
              </div>
              <div className="flex flex-wrap gap-1">
                {seller.categories.map((c) => <Badge key={c} variant="outline">{c}</Badge>)}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="flex flex-col gap-3">
          <Alert>
            <AlertDescription>
              <strong>{seller.verifiedTier === 'agent-wallet' ? 'Enhanced review required' : 'Verified seller'}</strong>
              <br />
              {seller.verifiedTier === 'agent-wallet'
                ? 'Agent-wallet sellers need spend caps, signed allowances, and slower payout release.'
                : 'Seller identity and signing keys have passed listing review.'}
            </AlertDescription>
          </Alert>
          <Card>
            <CardHeader><CardTitle className="text-xl font-light">Commercial controls</CardTitle></CardHeader>
            <CardContent>
              <div className="space-y-1 text-sm text-muted-foreground">
                <div>Escrow release after sandbox pass</div>
                <div>Stake can be slashed on fraud or rights breach</div>
                <div>Royalty splits supported for co-signers and registries</div>
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                <Button render={<a href="/payments" />}>Payment rails</Button>
                <Button variant="ghost" render={<a href="/transactions" />}>Transactions</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <Card className="mt-6">
        <CardHeader><CardTitle className="text-xl font-light">Listed artifacts</CardTitle></CardHeader>
        <CardContent className="p-0">
          {loading ? (
            <div className="p-6"><Spinner /></div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Artifact</TableHead>
                  <TableHead>Trust</TableHead>
                  <TableHead>Lift</TableHead>
                  <TableHead>Price</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sellerListings.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell>
                      <strong>{item.title}</strong>
                      <div className="text-xs text-muted-foreground">{item.domain}</div>
                    </TableCell>
                    <TableCell>{item.trust_score?.toFixed(1) ?? '—'}/100</TableCell>
                    <TableCell>{item.latest_transfer_efficiency?.toFixed(1) ?? '—'}%</TableCell>
                    <TableCell>${item.price_usd.toFixed(2)}</TableCell>
                    <TableCell><Link href={`/asset/${item.id}`} className="hover:underline">Review</Link></TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
