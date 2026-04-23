'use client';

import { useEffect, useState } from 'react';
import { Heading, Button, Label, Flash, Spinner } from '@primer/react';
import { fetchListings, fetchPreview, fetchTrust, ListingRecord } from '@/lib/api';

const tabList = ['overview', 'provenance', 'safety', 'trust', 'payload'] as const;

export default function AssetScreen({ slug }: { slug: string }) {
  const [listing, setListing] = useState<ListingRecord | null>(null);
  const [preview, setPreview] = useState<any>(null);
  const [trust, setTrust] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState('overview');

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

  if (loading) return <div className="amm-page"><Spinner size="medium" /></div>;
  if (!listing) return <div className="amm-page"><Flash variant="danger">Artifact not found.</Flash></div>;

  return (
    <div className="amm-page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
        <div>
          <Heading>{listing.title}</Heading>
          <span className="amm-subtle">
            {listing.domain} · Trust: {listing.trust_score ?? '—'}/100 · Price: ${listing.price_usd.toFixed(2)}
          </span>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button variant="invisible">Sandbox</Button>
          <Button variant="invisible">Compare</Button>
          <Button variant="primary">Acquire</Button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '16px', marginBottom: '16px' }}>
        <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
          <Heading as="h3" style={{ fontSize: '14px', marginBottom: '8px' }}>Summary</Heading>
          <p>{listing.description}</p>
        </div>
        <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
          <Heading as="h3" style={{ fontSize: '14px', marginBottom: '8px' }}>Key metrics</Heading>
          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
            <Label variant="success">Lift +{listing.latest_transfer_efficiency?.toFixed(1) ?? '—'}%</Label>
            <Label variant="secondary">Adversarial {listing.latest_adversarial_score?.toFixed(0) ?? '—'}/100</Label>
            <Label variant="secondary">Verifications: {listing.verification_count}</Label>
          </div>
          <p className="amm-subtle" style={{ marginTop: '8px' }}>License: {listing.license_type}</p>
        </div>
        <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
          <Heading as="h3" style={{ fontSize: '14px', marginBottom: '8px' }}>Decision cues</Heading>
          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
            {listing.trust_score != null && listing.trust_score >= 80 && <Label variant="success">High trust</Label>}
            {listing.latest_adversarial_score != null && listing.latest_adversarial_score < 30 && <Label variant="success">Clean adversarial</Label>}
            {listing.verification_count > 0 && <Label variant="accent">Verified</Label>}
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '0', borderBottom: '1px solid #d0d7de', marginBottom: '16px' }}>
        {tabList.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            style={{
              padding: '8px 16px',
              cursor: 'pointer',
              background: 'none',
              border: 'none',
              borderBottom: tab === t ? '2px solid #0969da' : '2px solid transparent',
              fontWeight: tab === t ? 600 : 400,
              color: tab === t ? '#0969da' : '#656d76',
              fontSize: '14px',
            }}
          >
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {tab === 'overview' && preview && (
        <div className="amm-grid amm-grid-2col">
          <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', overflow: 'hidden' }}>
            <div style={{ padding: '16px', borderBottom: '1px solid #d0d7de' }}>
              <Heading as="h3" style={{ fontSize: '14px' }}>Artifact preview</Heading>
            </div>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
              <tbody>
                {[
                  ['Domain', `${preview.domain?.category}:${preview.domain?.subcategory}`],
                  ['Format', preview.knowledge_summary?.format],
                  ['Token count', preview.knowledge_summary?.token_count?.toLocaleString()],
                  ['Model', preview.provenance?.model],
                  ['Training rounds', preview.provenance?.training_rounds],
                  ['Expert avg error', preview.attestation?.expert_avg_error?.toFixed(2)],
                  ['Transfer efficiency', `${preview.attestation?.transfer_efficiency_pct?.toFixed(1)}%`],
                ].map(([k, v]) => (
                  <tr key={String(k)} style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                    <td style={{ padding: '8px 12px', fontWeight: 500, color: 'var(--fgColor-muted)' }}>{k}</td>
                    <td style={{ padding: '8px 12px' }}>{v}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
            <Heading as="h3" style={{ fontSize: '14px', marginBottom: '8px' }}>Artifact hash</Heading>
            <code style={{ padding: '8px', backgroundColor: '#f6f8fa', borderRadius: '3px', display: 'block', fontSize: '11px', wordBreak: 'break-all' }}>
              {listing.artifact_hash}
            </code>
            <p className="amm-subtle" style={{ marginTop: '8px' }}>Content-addressed SHA-256.</p>
          </div>
        </div>
      )}

      {tab === 'trust' && (
        <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
          <Heading as="h3" style={{ fontSize: '14px', marginBottom: '8px' }}>Trust history</Heading>
          {trust ? (
            <pre style={{ padding: '16px', backgroundColor: '#f6f8fa', borderRadius: '3px', fontSize: '11px', overflow: 'auto', whiteSpace: 'pre-wrap' }}>
              {trust.report}
            </pre>
          ) : <span>No trust history available.</span>}
        </div>
      )}

      {tab === 'payload' && (
        <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
          <Heading as="h3" style={{ fontSize: '14px', marginBottom: '8px' }}>Payload manifest</Heading>
          <pre style={{ padding: '16px', backgroundColor: '#f6f8fa', borderRadius: '3px', fontSize: '11px' }}>
{`artifact_hash: ${listing.artifact_hash}
domain: ${listing.domain}
license: ${listing.license_type}`}
          </pre>
        </div>
      )}
    </div>
  );
}
