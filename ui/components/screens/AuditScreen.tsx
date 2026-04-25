'use client';

import { useEffect, useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Spinner } from '@/components/ui/spinner';
import { fetchListings, type ListingRecord } from '@/lib/api';
import { getAuditRecord, getSellerProfile } from '@/lib/directory';

function controlVariant(status: string): 'default' | 'outline' | 'destructive' {
  if (status === 'pass') return 'default';
  if (status === 'warn') return 'outline';
  return 'destructive';
}

export default function AuditScreen({ artifactId }: { artifactId: string }) {
  const [listings, setListings] = useState<ListingRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchListings().then(setListings).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="mx-auto max-w-5xl px-5 py-8"><Spinner /></div>;

  const listing = listings.find((item) => item.id === artifactId);
  if (!listing) return <div className="mx-auto max-w-5xl px-5 py-8"><Alert variant="destructive"><AlertDescription>Artifact not found.</AlertDescription></Alert></div>;

  const audit = getAuditRecord(artifactId, listings);
  const seller = getSellerProfile(listing.seller_id);

  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Audit envelope</h1>
      <p className="mb-6 text-sm text-muted-foreground">Provenance, signature chain, payout controls, rollback policy, and gated payload release for {listing.title}.</p>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Artifact + seller</CardTitle></CardHeader>
          <CardContent className="space-y-1 text-sm text-muted-foreground">
            <div>Artifact: {listing.title}</div>
            <div>Seller: {seller?.name || listing.seller_id}</div>
            <div>Trust: {listing.trust_score?.toFixed(1) ?? '—'}/100</div>
            <div>Hash: {listing.artifact_hash}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Policies</CardTitle></CardHeader>
          <CardContent className="space-y-2 text-sm text-muted-foreground">
            <div>Payout: {audit.payoutPolicy}</div>
            <div>Rollback: {audit.rollbackPolicy}</div>
            <div>Access: {audit.accessPolicy}</div>
          </CardContent>
        </Card>
      </div>

      <Card className="mt-6">
        <CardHeader><CardTitle className="text-xl font-light">Signature chain</CardTitle></CardHeader>
        <CardContent className="flex flex-col gap-3">
          {audit.signatureChain.map((step) => (
            <div key={`${step.actor}-${step.at}`} className="border-l-2 border-foreground/20 pl-3">
              <strong>{step.actor}</strong>
              <div className="text-sm text-muted-foreground">{step.action}</div>
              <div className="text-sm text-muted-foreground">{step.at.replace('T', ' ').slice(0, 16)} UTC</div>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader><CardTitle className="text-xl font-light">Controls</CardTitle></CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Control</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Detail</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {audit.controls.map((control) => (
                <TableRow key={control.name}>
                  <TableCell className="font-semibold">{control.name}</TableCell>
                  <TableCell><Badge variant={controlVariant(control.status)}>{control.status}</Badge></TableCell>
                  <TableCell>{control.detail}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
