'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Spinner } from '@/components/ui/spinner';
import { Tabs, TabsContent, TabsContents, TabsList, TabsTrigger } from '@/components/animate-ui/components/animate/tabs';
import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from '@/components/ui/breadcrumb';
import { CodeBlock } from '@/components/ui/code-block';
import { fetchListings, fetchPreview, fetchTrust, ListingRecord } from '@/lib/api';
import CheckoutDialog from '@/components/CheckoutDialog';

export default function AssetScreen({ slug }: { slug: string }) {
  const [listing, setListing] = useState<ListingRecord | null>(null);
  const [preview, setPreview] = useState<any>(null);
  const [trust, setTrust] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [showCheckout, setShowCheckout] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function load() {
      try {
        const listings = await fetchListings();
        const found = listings.find((l) => l.id === slug);
        if (!found) return;
        setListing(found);
        const [prev, tr] = await Promise.all([
          fetchPreview(found.artifact_hash).catch(() => null),
          fetchTrust(found.artifact_hash).catch(() => null),
        ]);
        setPreview(prev);
        setTrust(tr);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [slug]);

  if (loading) return <div className="mx-auto max-w-5xl px-5 py-8"><Spinner /></div>;
  if (!listing) return <div className="mx-auto max-w-5xl px-5 py-8"><Alert variant="destructive"><AlertDescription>Artifact not found.</AlertDescription></Alert></div>;

  return (
    <TooltipProvider>
      <div className="mx-auto max-w-5xl px-5 py-8">
        <Breadcrumb className="mb-4">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink render={<Link href="/leaderboard" />}>Registry</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink render={<Link href="/leaderboard" />}>{listing.domain.split(':')[0]}</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbPage>{listing.title}</BreadcrumbPage></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>

        <div className="mb-4 flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-light">{listing.title}</h1>
            <p className="text-sm text-muted-foreground">
              {listing.domain} · Trust: {listing.trust_score ?? '—'}/100 · Price: ${listing.price_usd.toFixed(2)}
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="ghost" size="sm">Sandbox</Button>
            <Button variant="ghost" size="sm">Compare</Button>
            <Button size="sm" onClick={() => setShowCheckout(true)}>Acquire</Button>
          </div>
        </div>

        <div className="mb-4 grid gap-4 sm:grid-cols-3">
          <Card>
            <CardHeader><CardTitle className="text-sm font-semibold">Summary</CardTitle></CardHeader>
            <CardContent><p className="text-sm">{listing.description}</p></CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-sm font-semibold">Key metrics</CardTitle></CardHeader>
            <CardContent>
              <div className="mb-2 flex flex-wrap gap-1">
                <Tooltip>
                  <TooltipTrigger>
                    <Badge>Lift +{listing.latest_transfer_efficiency?.toFixed(1) ?? '—'}%</Badge>
                  </TooltipTrigger>
                  <TooltipContent>How much better the agent performs with this artifact attached</TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger>
                    <Badge variant="secondary">Adversarial {listing.latest_adversarial_score?.toFixed(0) ?? '—'}/100</Badge>
                  </TooltipTrigger>
                  <TooltipContent>Score from adversarial probe battery — lower is cleaner</TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger>
                    <Badge variant="outline">Verifications: {listing.verification_count}</Badge>
                  </TooltipTrigger>
                  <TooltipContent>Number of independent verification runs completed</TooltipContent>
                </Tooltip>
              </div>
              <p className="text-xs text-muted-foreground">License: {listing.license_type}</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-sm font-semibold">Decision cues</CardTitle></CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-1">
                {listing.trust_score != null && listing.trust_score >= 80 && <Badge>High trust</Badge>}
                {listing.latest_adversarial_score != null && listing.latest_adversarial_score < 30 && <Badge>Clean adversarial</Badge>}
                {listing.verification_count > 0 && <Badge variant="secondary">Verified</Badge>}
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="overview">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="provenance">Provenance</TabsTrigger>
            <TabsTrigger value="safety">Safety</TabsTrigger>
            <TabsTrigger value="trust">Trust</TabsTrigger>
            <TabsTrigger value="payload">Payload</TabsTrigger>
          </TabsList>

          <TabsContents>
          <TabsContent value="overview">
            {preview && (
              <div className="grid gap-4 lg:grid-cols-2">
                <Card>
                  <CardHeader><CardTitle className="text-sm font-semibold">Artifact preview</CardTitle></CardHeader>
                  <CardContent className="p-0">
                    <Table>
                      <TableBody>
                        {[
                          ['Domain', `${preview.domain?.category}:${preview.domain?.subcategory}`],
                          ['Format', preview.knowledge_summary?.format],
                          ['Token count', preview.knowledge_summary?.token_count?.toLocaleString()],
                          ['Model', preview.provenance?.model],
                          ['Training rounds', preview.provenance?.training_rounds],
                          ['Expert avg error', preview.attestation?.expert_avg_error?.toFixed(2)],
                          ['Transfer efficiency', `${preview.attestation?.transfer_efficiency_pct?.toFixed(1)}%`],
                        ].map(([k, v]) => (
                          <TableRow key={String(k)}>
                            <TableCell className="font-medium text-muted-foreground">{k}</TableCell>
                            <TableCell>{v}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader><CardTitle className="text-sm font-semibold">Artifact hash</CardTitle></CardHeader>
                  <CardContent>
                    <CodeBlock>{listing.artifact_hash}</CodeBlock>
                    <p className="mt-2 text-xs text-muted-foreground">Content-addressed SHA-256.</p>
                  </CardContent>
                </Card>
              </div>
            )}
          </TabsContent>

          <TabsContent value="trust">
            <Card>
              <CardHeader><CardTitle className="text-sm font-semibold">Trust history</CardTitle></CardHeader>
              <CardContent>
                {trust ? (
                  <CodeBlock>{trust.report}</CodeBlock>
                ) : <span className="text-sm text-muted-foreground">No trust history available.</span>}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="payload">
            <Card>
              <CardHeader><CardTitle className="text-sm font-semibold">Payload manifest</CardTitle></CardHeader>
              <CardContent>
                <CodeBlock language="yaml">{`artifact_hash: ${listing.artifact_hash}\ndomain: ${listing.domain}\nlicense: ${listing.license_type}`}</CodeBlock>
              </CardContent>
            </Card>
          </TabsContent>
          </TabsContents>
        </Tabs>

        {showCheckout && (
          <CheckoutDialog
            listingId={listing.id}
            title={listing.title}
            priceUsd={listing.price_usd}
            domain={listing.domain}
            onClose={() => setShowCheckout(false)}
            onSuccess={() => router.push('/preview/portfolio')}
          />
        )}
      </div>
    </TooltipProvider>
  );
}
