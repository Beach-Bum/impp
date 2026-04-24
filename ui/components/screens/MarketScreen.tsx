'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import { Heading, TextInput, Button, Label, Flash, Spinner } from '@primer/react';
import { SearchIcon } from '@primer/octicons-react';
import { fetchListings, ListingRecord } from '@/lib/api';
import { getSellerProfile } from '@/lib/directory';

function trustScheme(score: number | null): 'success' | 'danger' | 'secondary' {
  if (score === null) return 'secondary';
  if (score >= 80) return 'success';
  if (score >= 50) return 'secondary';
  return 'danger';
}

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
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Marketplace</Heading>
      <p className="amm-screen-subtitle">
        Search by outcome, shortlist governed assets, and compare before you attach anything.
      </p>

      <Flash style={{ marginBottom: '16px' }}>
        <Label variant="accent">AI</Label>{' '}
        Ranking blends transfer lift, adversarial score, trust, and freshness.
      </Flash>

      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px', flexWrap: 'wrap', alignItems: 'end' }}>
        <div style={{ flex: 1, minWidth: 300 }}>
          <TextInput
            leadingVisual={SearchIcon}
            placeholder="Search by domain, objective, or workflow"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ width: '100%' }}
          />
        </div>
        <Button>Filter sheet</Button>
        <Button as={Link} href="/compare" variant="invisible">Compare tray</Button>
      </div>

      <div style={{ display: 'flex', gap: '4px', marginBottom: '16px', flexWrap: 'wrap' }}>
        {domains.map((d) => (
          <Label key={d} variant="secondary">{d}</Label>
        ))}
      </div>

      {loading ? (
        <Spinner size="medium" />
      ) : error ? (
        <Flash variant="danger">Failed to load: {error}. Is the API server running?</Flash>
      ) : (
        <div className="amm-grid amm-grid-2col">
          <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', overflow: 'hidden' }}>
            <div style={{ padding: '16px', borderBottom: '1px solid #d0d7de' }}>
              <Heading as="h2" style={{ fontSize: '14px' }}>Memory Artifacts</Heading>
              <span className="amm-subtle">{listings.length} verified artifacts available</span>
            </div>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--borderColor-default, #d0d7de)' }}>
                  <th style={{ textAlign: 'left', padding: '8px 12px', fontWeight: 600 }}>Asset</th>
                  <th style={{ textAlign: 'left', padding: '8px 12px', fontWeight: 600 }}>Lift</th>
                  <th style={{ textAlign: 'left', padding: '8px 12px', fontWeight: 600 }}>Trust</th>
                  <th style={{ textAlign: 'left', padding: '8px 12px', fontWeight: 600 }}>Adversarial</th>
                  <th style={{ textAlign: 'left', padding: '8px 12px', fontWeight: 600 }}>License</th>
                  <th style={{ textAlign: 'left', padding: '8px 12px', fontWeight: 600 }}>Price</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((l) => {
                  const seller = getSellerProfile(l.seller_id);
                  return (
                    <tr key={l.id} style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                      <td style={{ padding: '10px 12px' }}>
                        <Link href={`/asset/${l.id}`} style={{ color: 'var(--fgColor-accent, #0969da)', textDecoration: 'none', fontWeight: 600 }}>
                          {l.title}
                        </Link>
                        <br />
                        <span className="amm-subtle">{l.domain}</span>
                        <br />
                        <Link href={`/sellers/${l.seller_id}`} className="amm-subtle">
                          {seller?.name || l.seller_id}
                        </Link>
                      </td>
                      <td style={{ padding: '10px 12px' }}>
                        <Label variant="success">+{l.latest_transfer_efficiency?.toFixed(1) ?? '—'}%</Label>
                      </td>
                      <td style={{ padding: '10px 12px' }}>
                        <Label variant={trustScheme(l.trust_score)}>
                          {l.trust_score != null ? `${l.trust_score}/100` : '—'}
                        </Label>
                      </td>
                      <td style={{ padding: '10px 12px' }}>
                        {l.latest_adversarial_score?.toFixed(0) ?? '—'}/100
                      </td>
                      <td style={{ padding: '10px 12px' }}>{l.license_type}</td>
                      <td style={{ padding: '10px 12px' }}>${l.price_usd.toFixed(2)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            {filtered[0] && (
              <div style={{ padding: '16px', borderTop: '1px solid #d0d7de', backgroundColor: '#f6f8fa' }}>
                <span style={{ fontWeight: 'bold' }}>Top artifact</span>
                <p className="amm-subtle">
                  {filtered[0].title} — trust {filtered[0].trust_score}/100, lift +{filtered[0].latest_transfer_efficiency?.toFixed(1)}%
                </p>
                <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
                  <Button size="small" as={Link} href={`/audit/${filtered[0].id}`} variant="invisible">Audit</Button>
                  <Button size="small" as={Link} href="/compare" variant="invisible">Compare</Button>
                  <Button size="small" variant="primary">Acquire</Button>
                </div>
              </div>
            )}
          </div>

          <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', padding: '16px' }}>
            <Heading as="h2" style={{ fontSize: '14px', marginBottom: '16px' }}>Shortlist</Heading>
            <div className="amm-card-stack">
              {filtered.slice(0, 3).map((l) => (
                <div key={l.id} style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px', marginBottom: '8px' }}>
                  <span style={{ fontWeight: 'bold' }}>{l.title}</span>
                  <br />
                  <span className="amm-subtle">{l.domain} — {l.license_type}</span>
                  <div style={{ display: 'flex', gap: '4px', marginTop: '8px' }}>
                    <Label variant="success">Lift +{l.latest_transfer_efficiency?.toFixed(1) ?? '—'}%</Label>
                    <Label variant={trustScheme(l.trust_score)}>Trust {l.trust_score ?? '—'}</Label>
                  </div>
                  <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
                    <Button size="small" variant="invisible" as={Link} href={`/asset/${l.id}`}>Review</Button>
                    <Button size="small" variant="invisible" as={Link} href={`/sellers/${l.seller_id}`}>Seller</Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
