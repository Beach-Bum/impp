'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Spinner } from '@/components/ui/spinner';
import { Search } from 'lucide-react';
import { fetchListings, ListingRecord } from '@/lib/api';
import { getSellerProfile } from '@/lib/directory';

export default function MarketScreen() {
  const [query, setQuery] = useState('');
  const [listings, setListings] = useState<ListingRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchListings()
      .then(setListings)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    const t = query.trim().toLowerCase();
    if (!t) return listings;
    return listings.filter((l) =>
      [l.title, l.domain, l.description].join(' ').toLowerCase().includes(t)
    );
  }, [query, listings]);

  const domains = Array.from(new Set(listings.map((l) => l.domain.split(':')[0])));

  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Marketplace</h1>
      <p className="mb-6 text-sm text-muted-foreground">
        Search by outcome, shortlist governed assets, and compare before you attach anything.
      </p>

      <Alert className="mb-4">
        <AlertDescription>
          <Badge variant="secondary" className="mr-2">AI</Badge>
          Ranking blends transfer lift, adversarial score, trust, and freshness.
        </AlertDescription>
      </Alert>

      <div className="mb-4 flex flex-wrap items-end gap-2">
        <div className="relative min-w-[300px] flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search by domain, objective, or workflow"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-9"
          />
        </div>
        <Button variant="outline">Filter sheet</Button>
        <Button variant="ghost" render={<Link href="/compare" />}>Compare tray</Button>
      </div>

      <div className="mb-4 flex flex-wrap gap-1">
        {domains.map((d) => <Badge key={d} variant="secondary">{d}</Badge>)}
      </div>

      {loading ? (
        <Spinner />
      ) : error ? (
        <Alert variant="destructive"><AlertDescription>Failed to load: {error}. Is the API server running?</AlertDescription></Alert>
      ) : (
        <div className="grid gap-8 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl font-light">Memory Artifacts</CardTitle>
              <p className="text-xs text-muted-foreground">{listings.length} verified artifacts available</p>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Asset</TableHead>
                    <TableHead>Lift</TableHead>
                    <TableHead>Trust</TableHead>
                    <TableHead>Adversarial</TableHead>
                    <TableHead>License</TableHead>
                    <TableHead>Price</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filtered.map((l) => {
                    const seller = getSellerProfile(l.seller_id);
                    return (
                      <TableRow key={l.id}>
                        <TableCell>
                          <Link href={`/asset/${l.id}`} className="font-semibold hover:underline">{l.title}</Link>
                          <div className="text-xs text-muted-foreground">{l.domain}</div>
                          <Link href={`/sellers/${l.seller_id}`} className="text-xs text-muted-foreground hover:underline">
                            {seller?.name || l.seller_id}
                          </Link>
                        </TableCell>
                        <TableCell><Badge>+{l.latest_transfer_efficiency?.toFixed(1) ?? '—'}%</Badge></TableCell>
                        <TableCell><Badge variant="outline">{l.trust_score != null ? `${l.trust_score}/100` : '—'}</Badge></TableCell>
                        <TableCell>{l.latest_adversarial_score?.toFixed(0) ?? '—'}/100</TableCell>
                        <TableCell>{l.license_type}</TableCell>
                        <TableCell>${l.price_usd.toFixed(2)}</TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
              {filtered[0] && (
                <div className="border-t p-4">
                  <span className="font-bold">Top artifact</span>
                  <p className="mb-2 mt-1 text-xs text-muted-foreground">
                    {filtered[0].title} — trust {filtered[0].trust_score}/100, lift +{filtered[0].latest_transfer_efficiency?.toFixed(1)}%
                  </p>
                  <div className="flex gap-2">
                    <Button size="sm" variant="ghost" render={<Link href={`/audit/${filtered[0].id}`} />}>Audit</Button>
                    <Button size="sm" variant="ghost" render={<Link href="/compare" />}>Compare</Button>
                    <Button size="sm">Acquire</Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader><CardTitle className="text-xl font-light">Shortlist</CardTitle></CardHeader>
            <CardContent className="flex flex-col gap-3">
              {filtered.slice(0, 3).map((l) => (
                <div key={l.id} className="rounded-md border p-4">
                  <span className="font-bold">{l.title}</span>
                  <div className="text-xs text-muted-foreground">{l.domain} — {l.license_type}</div>
                  <div className="mt-2 flex gap-1">
                    <Badge>Lift +{l.latest_transfer_efficiency?.toFixed(1) ?? '—'}%</Badge>
                    <Badge variant="outline">Trust {l.trust_score ?? '—'}</Badge>
                  </div>
                  <div className="mt-2 flex gap-2">
                    <Button size="sm" variant="ghost" render={<Link href={`/asset/${l.id}`} />}>Review</Button>
                    <Button size="sm" variant="ghost" render={<Link href={`/sellers/${l.seller_id}`} />}>Seller</Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
