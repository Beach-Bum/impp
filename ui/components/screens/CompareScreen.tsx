'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import { Box, Button, Heading, Label, Spinner } from '@primer/react';
import { fetchListings, type ListingRecord } from '@/lib/api';
import { getSellerProfile } from '@/lib/directory';

export default function CompareScreen() {
  const [listings, setListings] = useState<ListingRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchListings().then(setListings).finally(() => setLoading(false));
  }, []);

  const selected = useMemo(() => listings.slice(0, 3), [listings]);

  if (loading) return <div className="amm-page"><Spinner size="medium" /></div>;

  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Compare artifacts</Heading>
      <p className="amm-screen-subtitle">Compare trust, transfer, seller quality, and price before you attach or buy.</p>

      <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--borderColor-default, #d0d7de)' }}>
              <th style={{ textAlign: 'left', padding: '8px 12px' }}>Field</th>
              {selected.map((item) => (
                <th key={item.id} style={{ textAlign: 'left', padding: '8px 12px' }}>{item.title}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[
              ['Domain', (i: ListingRecord) => i.domain],
              ['Seller', (i: ListingRecord) => getSellerProfile(i.seller_id)?.name || i.seller_id],
              ['Trust', (i: ListingRecord) => `${i.trust_score?.toFixed(1) ?? '—'}/100`],
              ['Transfer lift', (i: ListingRecord) => `${i.latest_transfer_efficiency?.toFixed(1) ?? '—'}%`],
              ['Adversarial', (i: ListingRecord) => `${i.latest_adversarial_score?.toFixed(1) ?? '—'}/100`],
              ['Price', (i: ListingRecord) => `$${i.price_usd.toFixed(2)}`],
              ['License', (i: ListingRecord) => i.license_type],
            ].map(([label, getter]) => (
              <tr key={String(label)} style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                <td style={{ padding: '8px 12px', fontWeight: 600 }}>{label}</td>
                {selected.map((item) => <td key={`${item.id}-${label}`} style={{ padding: '8px 12px' }}>{(getter as any)(item)}</td>)}
              </tr>
            ))}
            <tr>
              <td style={{ padding: '8px 12px', fontWeight: 600 }}>Action</td>
              {selected.map((item) => (
                <td key={`${item.id}-action`} style={{ padding: '8px 12px' }}>
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    <Button as="a" href={`/asset/${item.id}`}>Review</Button>
                    <Button as="a" href={`/audit/${item.id}`} variant="invisible">Audit</Button>
                  </div>
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </Box>

      <div className="amm-inline-tags" style={{ marginTop: '16px' }}>
        <Label variant="accent">Best for shortlist decisions</Label>
        <Label variant="secondary">Seller quality should be read alongside artifact quality</Label>
        <Label variant="secondary">Use audit page for provenance and payout controls</Label>
      </div>
    </div>
  );
}
