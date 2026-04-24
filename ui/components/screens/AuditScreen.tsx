'use client';

import { useEffect, useState } from 'react';
import { Box, Flash, Heading, Label, Spinner } from '@primer/react';
import { fetchListings, type ListingRecord } from '@/lib/api';
import { getAuditRecord, getSellerProfile } from '@/lib/directory';

function controlVariant(status: string): 'success' | 'attention' | 'danger' {
  if (status === 'pass') return 'success';
  if (status === 'warn') return 'attention';
  return 'danger';
}

export default function AuditScreen({ artifactId }: { artifactId: string }) {
  const [listings, setListings] = useState<ListingRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchListings().then(setListings).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="amm-page"><Spinner size="medium" /></div>;

  const listing = listings.find((item) => item.id === artifactId);
  if (!listing) return <div className="amm-page"><Flash variant="danger">Artifact not found.</Flash></div>;

  const audit = getAuditRecord(artifactId, listings);
  const seller = getSellerProfile(listing.seller_id);

  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Audit envelope</Heading>
      <p className="amm-screen-subtitle">Provenance, signature chain, payout controls, rollback policy, and gated payload release for {listing.title}.</p>

      <div className="amm-grid amm-grid-2col">
        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Artifact + seller</Heading>
          <span className="amm-subtle" style={{ display: 'block' }}>Artifact: {listing.title}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Seller: {seller?.name || listing.seller_id}</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Trust: {listing.trust_score?.toFixed(1) ?? '—'}/100</span>
          <span className="amm-subtle" style={{ display: 'block' }}>Hash: {listing.artifact_hash}</span>
        </Box>

        <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Policies</Heading>
          <span className="amm-subtle" style={{ display: 'block' }}>Payout: {audit.payoutPolicy}</span>
          <span className="amm-subtle" style={{ display: 'block', marginTop: '8px' }}>Rollback: {audit.rollbackPolicy}</span>
          <span className="amm-subtle" style={{ display: 'block', marginTop: '8px' }}>Access: {audit.accessPolicy}</span>
        </Box>
      </div>

      <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3, mt: 3 }}>
        <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Signature chain</Heading>
        <div className="amm-card-stack">
          {audit.signatureChain.map((step) => (
            <div key={`${step.actor}-${step.at}`} style={{ borderLeft: '2px solid var(--borderColor-accent-emphasis, #0969da)', paddingLeft: '12px' }}>
              <strong>{step.actor}</strong>
              <div className="amm-subtle">{step.action}</div>
              <div className="amm-subtle">{step.at.replace('T', ' ').slice(0, 16)} UTC</div>
            </div>
          ))}
        </div>
      </Box>

      <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, overflow: 'hidden', mt: 3 }}>
        <div style={{ padding: '16px', borderBottom: '1px solid var(--borderColor-default, #d0d7de)' }}>
          <Heading as="h2" sx={{ fontSize: 2 }}>Controls</Heading>
        </div>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--borderColor-default, #d0d7de)' }}>
              <th style={{ textAlign: 'left', padding: '8px 12px' }}>Control</th>
              <th style={{ textAlign: 'left', padding: '8px 12px' }}>Status</th>
              <th style={{ textAlign: 'left', padding: '8px 12px' }}>Detail</th>
            </tr>
          </thead>
          <tbody>
            {audit.controls.map((control) => (
              <tr key={control.name} style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                <td style={{ padding: '8px 12px', fontWeight: 600 }}>{control.name}</td>
                <td style={{ padding: '8px 12px' }}><Label variant={controlVariant(control.status)}>{control.status}</Label></td>
                <td style={{ padding: '8px 12px' }}>{control.detail}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Box>
    </div>
  );
}
