'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import {
  Button,
  Column,
  DataTable,
  Grid,
  InlineLoading,
  Search,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableHeader,
  TableRow,
  Tag,
  Tile,
} from '@carbon/react';
import AIExplainabilityHint from '@/components/AIExplainabilityHint';
import { fetchListings, ListingRecord } from '@/lib/api';

const headers = [
  { key: 'asset', header: 'Asset' },
  { key: 'lift', header: 'Transfer Lift' },
  { key: 'adversarial', header: 'Adversarial' },
  { key: 'trust', header: 'Trust Score' },
  { key: 'verifications', header: 'Verifications' },
  { key: 'license', header: 'License' },
  { key: 'price', header: 'Price' },
];

function domainTag(domain: string): string {
  const cat = domain.split(':')[0];
  return cat;
}

function trustColor(score: number | null): 'green' | 'red' | 'cool-gray' {
  if (score === null) return 'cool-gray';
  if (score >= 80) return 'green';
  if (score >= 50) return 'cool-gray';
  return 'red';
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

  const rows = useMemo(() => {
    const term = query.trim().toLowerCase();
    const filtered = term
      ? listings.filter((l) =>
          [l.title, l.domain, l.description].join(' ').toLowerCase().includes(term)
        )
      : listings;

    return filtered.map((l) => ({
      id: l.id,
      asset: l.title,
      domain: l.domain,
      description: l.description,
      lift: l.latest_transfer_efficiency != null ? `+${l.latest_transfer_efficiency.toFixed(1)}%` : '—',
      adversarial: l.latest_adversarial_score != null ? `${l.latest_adversarial_score.toFixed(0)}/100` : '—',
      trust: l.trust_score,
      verifications: l.verification_count,
      license: l.license_type,
      price: `$${l.price_usd.toFixed(2)}`,
      artifact_hash: l.artifact_hash,
      seller_id: l.seller_id,
    }));
  }, [query, listings]);

  const topListing = rows[0];

  return (
    <div className="amm-page">
      <Grid fullWidth>
        <Column lg={12} md={8} sm={4}>
          <h1 className="amm-screen-title">Marketplace</h1>
          <p className="amm-screen-subtitle">
            Search by outcome, shortlist governed assets, and compare before you attach anything.
          </p>
        </Column>
        <Column lg={4} md={8} sm={4}>
          <AIExplainabilityHint summary="Ranking blends transfer lift, adversarial score, trust, and freshness." />
        </Column>

        <Column lg={16} md={8} sm={4}>
          <div className="amm-toolbar">
            <Search
              id="market-search"
              labelText="Search assets"
              placeholder="Search by domain, objective, or workflow"
              size="lg"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
            <Button kind="secondary">Filter sheet</Button>
            <Button kind="tertiary">Open compare tray</Button>
          </div>
          <div className="amm-inline-tags amm-section">
            {Array.from(new Set(listings.map((l) => domainTag(l.domain)))).map((cat) => (
              <Tag key={cat} type="cool-gray">{cat}</Tag>
            ))}
          </div>
        </Column>

        <Column lg={11} md={8} sm={4}>
          {loading ? (
            <InlineLoading description="Loading marketplace..." />
          ) : error ? (
            <Tile className="amm-card">
              <p style={{ color: '#da1e28' }}>Failed to load: {error}</p>
              <p className="amm-subtle">Is the API server running on port 8100?</p>
            </Tile>
          ) : (
            <Tile className="amm-card">
              <DataTable rows={rows} headers={headers}>
                {({ rows: dataRows, headers: dataHeaders, getHeaderProps, getRowProps, getTableProps }) => (
                  <TableContainer title="Memory Artifacts" description={`${listings.length} verified artifacts available`}>
                    <Table {...getTableProps()} size="lg">
                      <TableHead>
                        <TableRow>
                          {dataHeaders.map((header) => {
                            const { key: _k, ...headerProps } = getHeaderProps({ header });
                            return (
                              <TableHeader key={header.key} {...headerProps}>
                                {header.header}
                              </TableHeader>
                            );
                          })}
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {dataRows.map((row) => {
                          const source = rows.find((r) => r.id === row.id);
                          return (
                            <TableRow key={row.id}>
                              <TableCell>
                                <Link href={`/asset/${row.id}`} className="amm-table-link">
                                  <strong>{source?.asset}</strong>
                                </Link>
                                <div className="amm-subtle">{source?.domain}</div>
                              </TableCell>
                              <TableCell>
                                <Tag type="green">{source?.lift}</Tag>
                              </TableCell>
                              <TableCell>{source?.adversarial}</TableCell>
                              <TableCell>
                                <Tag type={trustColor(source?.trust ?? null)}>
                                  {source?.trust != null ? `${source.trust}/100` : '—'}
                                </Tag>
                              </TableCell>
                              <TableCell>{source?.verifications}</TableCell>
                              <TableCell>{source?.license}</TableCell>
                              <TableCell>{source?.price}</TableCell>
                            </TableRow>
                          );
                        })}
                      </TableBody>
                    </Table>
                  </TableContainer>
                )}
              </DataTable>

              {topListing && (
                <div className="amm-surface-stack" style={{ marginTop: '1rem' }}>
                  <Tile>
                    <strong>Top artifact</strong>
                    <p className="amm-subtle">
                      {topListing.asset} — trust {topListing.trust}/100, transfer lift {topListing.lift}
                    </p>
                    <div className="amm-action-row">
                      <Button kind="ghost" size="sm">Sandbox</Button>
                      <Button kind="ghost" size="sm">Compare</Button>
                      <Button size="sm">Acquire</Button>
                    </div>
                  </Tile>
                </div>
              )}
            </Tile>
          )}
        </Column>

        <Column lg={5} md={8} sm={4}>
          <Tile className="amm-card">
            <h2>Shortlist</h2>
            <div className="amm-surface-stack">
              {rows.slice(0, 3).map((item) => (
                <Tile key={item.id}>
                  <strong>{item.asset}</strong>
                  <p className="amm-subtle">{item.domain} — {item.license}</p>
                  <div className="amm-inline-tags">
                    <Tag type="green">Lift {item.lift}</Tag>
                    <Tag type={trustColor(item.trust)}>Trust {item.trust ?? '—'}</Tag>
                  </div>
                  <div className="amm-action-row" style={{ marginTop: '0.75rem' }}>
                    <Button kind="ghost" size="sm" href={`/asset/${item.id}`}>Review</Button>
                    <Button kind="ghost" size="sm">Remove</Button>
                  </div>
                </Tile>
              ))}
            </div>
          </Tile>
        </Column>
      </Grid>
    </div>
  );
}
