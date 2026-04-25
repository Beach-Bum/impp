'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Spinner } from '@/components/ui/spinner';
import { fetchListings, type ListingRecord } from '@/lib/api';
import { getSellerProfile } from '@/lib/directory';

export default function CompareScreen() {
  const [listings, setListings] = useState<ListingRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchListings().then(setListings).finally(() => setLoading(false));
  }, []);

  const selected = useMemo(() => listings.slice(0, 3), [listings]);

  if (loading) return <div className="mx-auto max-w-5xl px-5 py-8"><Spinner /></div>;

  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Compare artifacts</h1>
      <p className="mb-6 text-sm text-muted-foreground">Compare trust, transfer, seller quality, and price before you attach or buy.</p>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Field</TableHead>
                {selected.map((item) => <TableHead key={item.id}>{item.title}</TableHead>)}
              </TableRow>
            </TableHeader>
            <TableBody>
              {[
                ['Domain', (i: ListingRecord) => i.domain],
                ['Seller', (i: ListingRecord) => getSellerProfile(i.seller_id)?.name || i.seller_id],
                ['Trust', (i: ListingRecord) => `${i.trust_score?.toFixed(1) ?? '—'}/100`],
                ['Transfer lift', (i: ListingRecord) => `${i.latest_transfer_efficiency?.toFixed(1) ?? '—'}%`],
                ['Adversarial', (i: ListingRecord) => `${i.latest_adversarial_score?.toFixed(1) ?? '—'}/100`],
                ['Price', (i: ListingRecord) => `$${i.price_usd.toFixed(2)}`],
                ['License', (i: ListingRecord) => i.license_type],
              ].map(([label, getter]) => (
                <TableRow key={String(label)}>
                  <TableCell className="font-semibold">{label as string}</TableCell>
                  {selected.map((item) => <TableCell key={`${item.id}-${label}`}>{(getter as any)(item)}</TableCell>)}
                </TableRow>
              ))}
              <TableRow>
                <TableCell className="font-semibold">Action</TableCell>
                {selected.map((item) => (
                  <TableCell key={`${item.id}-action`}>
                    <div className="flex flex-wrap gap-2">
                      <Button size="sm" render={<Link href={`/asset/${item.id}`} />}>Review</Button>
                      <Button size="sm" variant="ghost" render={<Link href={`/audit/${item.id}`} />}>Audit</Button>
                    </div>
                  </TableCell>
                ))}
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <div className="mt-4 flex flex-wrap gap-1">
        <Badge variant="secondary">Best for shortlist decisions</Badge>
        <Badge variant="outline">Seller quality should be read alongside artifact quality</Badge>
        <Badge variant="outline">Use audit page for provenance and payout controls</Badge>
      </div>
    </div>
  );
}
