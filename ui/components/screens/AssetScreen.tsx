'use client';

import { useEffect, useState } from 'react';
import {
  Accordion,
  AccordionItem,
  Button,
  CodeSnippet,
  Column,
  Grid,
  InlineLoading,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableHeader,
  TableRow,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Tag,
  Tile,
} from '@carbon/react';
import AIExplainabilityHint from '@/components/AIExplainabilityHint';
import { fetchListings, fetchPreview, fetchTrust, ListingRecord } from '@/lib/api';

export default function AssetScreen({ slug }: { slug: string }) {
  const [listing, setListing] = useState<ListingRecord | null>(null);
  const [preview, setPreview] = useState<any>(null);
  const [trust, setTrust] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        // slug is the listing ID
        const listings = await fetchListings();
        const found = listings.find((l) => l.id === slug);
        if (!found) return;
        setListing(found);

        const [prev, tr] = await Promise.all([
          fetchPreview(found.artifact_hash),
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

  if (loading) return <div className="amm-page"><InlineLoading description="Loading artifact details..." /></div>;
  if (!listing) return <div className="amm-page"><p>Artifact not found.</p></div>;

  return (
    <div className="amm-page">
      <Grid fullWidth>
        <Column lg={12} md={6} sm={4}>
          <h1 className="amm-screen-title">{listing.title}</h1>
          <p className="amm-screen-subtitle">
            {listing.domain} · Trust: {listing.trust_score ?? '—'}/100 · Price: ${listing.price_usd.toFixed(2)}
          </p>
        </Column>
        <Column lg={4} md={2} sm={4}>
          <div className="amm-action-row" style={{ justifyContent: 'flex-end' }}>
            <Button kind="ghost">Sandbox</Button>
            <Button kind="ghost">Compare</Button>
            <Button>Acquire</Button>
          </div>
        </Column>

        <Column lg={5} md={4} sm={4}>
          <Tile className="amm-card">
            <h2>Summary</h2>
            <p>{listing.description}</p>
          </Tile>
        </Column>
        <Column lg={5} md={4} sm={4}>
          <Tile className="amm-card">
            <h2>Key metrics</h2>
            <div className="amm-inline-tags">
              <Tag type="green">Lift {listing.latest_transfer_efficiency != null ? `+${listing.latest_transfer_efficiency.toFixed(1)}%` : '—'}</Tag>
              <Tag type="warm-gray">Adversarial {listing.latest_adversarial_score != null ? `${listing.latest_adversarial_score.toFixed(0)}/100` : '—'}</Tag>
              <Tag type="cool-gray">Verifications: {listing.verification_count}</Tag>
              <Tag type="cool-gray">Feedback: {listing.feedback_count}</Tag>
            </div>
            <p className="amm-subtle" style={{ marginTop: '0.5rem' }}>License: {listing.license_type}</p>
          </Tile>
        </Column>
        <Column lg={6} md={8} sm={4}>
          <Tile className="amm-card">
            <h2>Decision cues</h2>
            <AIExplainabilityHint summary="Trust score combines verified transfer efficiency, adversarial cleanliness, and freshness." />
            <div className="amm-inline-tags" style={{ marginTop: '1rem' }}>
              {listing.trust_score != null && listing.trust_score >= 80 && <Tag type="green">High trust</Tag>}
              {listing.latest_adversarial_score != null && listing.latest_adversarial_score < 30 && <Tag type="green">Clean adversarial</Tag>}
              {listing.verification_count > 0 && <Tag type="purple">Verified</Tag>}
            </div>
          </Tile>
        </Column>

        <Column lg={16} md={8} sm={4}>
          <Tabs>
            <TabList aria-label="Due diligence tabs">
              <Tab>Overview</Tab>
              <Tab>Provenance</Tab>
              <Tab>Safety</Tab>
              <Tab>Trust History</Tab>
              <Tab>Payload</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <Grid condensed fullWidth>
                  <Column lg={10} md={8} sm={4}>
                    <Tile className="amm-card">
                      {preview ? (
                        <TableContainer title="Artifact preview">
                          <Table size="md">
                            <TableHead>
                              <TableRow>
                                <TableHeader>Property</TableHeader>
                                <TableHeader>Value</TableHeader>
                              </TableRow>
                            </TableHead>
                            <TableBody>
                              <TableRow>
                                <TableCell>Domain</TableCell>
                                <TableCell>{preview.domain?.category}:{preview.domain?.subcategory}</TableCell>
                              </TableRow>
                              <TableRow>
                                <TableCell>Format</TableCell>
                                <TableCell>{preview.knowledge_summary?.format}</TableCell>
                              </TableRow>
                              <TableRow>
                                <TableCell>Sections</TableCell>
                                <TableCell>{preview.knowledge_summary?.sections?.join(', ') || '—'}</TableCell>
                              </TableRow>
                              <TableRow>
                                <TableCell>Token count</TableCell>
                                <TableCell>{preview.knowledge_summary?.token_count?.toLocaleString()}</TableCell>
                              </TableRow>
                              <TableRow>
                                <TableCell>Model</TableCell>
                                <TableCell>{preview.provenance?.model}</TableCell>
                              </TableRow>
                              <TableRow>
                                <TableCell>Training rounds</TableCell>
                                <TableCell>{preview.provenance?.training_rounds}</TableCell>
                              </TableRow>
                              <TableRow>
                                <TableCell>Training items</TableCell>
                                <TableCell>{preview.provenance?.training_items_count}</TableCell>
                              </TableRow>
                              <TableRow>
                                <TableCell>Expert avg error</TableCell>
                                <TableCell>{preview.attestation?.expert_avg_error?.toFixed(2)}</TableCell>
                              </TableRow>
                              <TableRow>
                                <TableCell>Transfer efficiency (self-reported)</TableCell>
                                <TableCell>{preview.attestation?.transfer_efficiency_pct?.toFixed(1)}%</TableCell>
                              </TableRow>
                            </TableBody>
                          </Table>
                        </TableContainer>
                      ) : (
                        <p>Preview unavailable.</p>
                      )}
                    </Tile>
                  </Column>
                  <Column lg={6} md={8} sm={4}>
                    <Tile className="amm-card">
                      <h2>Artifact hash</h2>
                      <CodeSnippet type="single">{listing.artifact_hash}</CodeSnippet>
                      <p className="amm-subtle" style={{ marginTop: '0.5rem' }}>
                        Content-addressed SHA-256. Verify integrity after purchase.
                      </p>
                    </Tile>
                  </Column>
                </Grid>
              </TabPanel>

              <TabPanel>
                <Tile className="amm-card">
                  {preview?.provenance ? (
                    <>
                      <h2>Provenance</h2>
                      <TableContainer title="Training provenance">
                        <Table size="md">
                          <TableHead>
                            <TableRow>
                              <TableHeader>Field</TableHeader>
                              <TableHeader>Value</TableHeader>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            <TableRow>
                              <TableCell>Model</TableCell>
                              <TableCell>{preview.provenance.model}</TableCell>
                            </TableRow>
                            <TableRow>
                              <TableCell>Training rounds</TableCell>
                              <TableCell>{preview.provenance.training_rounds}</TableCell>
                            </TableRow>
                            <TableRow>
                              <TableCell>Training items</TableCell>
                              <TableCell>{preview.provenance.training_items_count} items</TableCell>
                            </TableRow>
                            <TableRow>
                              <TableCell>Created</TableCell>
                              <TableCell>{preview.provenance.created_at?.slice(0, 10)}</TableCell>
                            </TableRow>
                          </TableBody>
                        </Table>
                      </TableContainer>
                    </>
                  ) : (
                    <p>Provenance data unavailable.</p>
                  )}
                </Tile>
              </TabPanel>

              <TabPanel>
                <Tile className="amm-card">
                  <h2>Adversarial safety</h2>
                  {preview?.latest_verification ? (
                    <TableContainer title="Verification results">
                      <Table size="md">
                        <TableHead>
                          <TableRow>
                            <TableHeader>Metric</TableHeader>
                            <TableHeader>Value</TableHeader>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          <TableRow>
                            <TableCell>Transfer efficiency (verified)</TableCell>
                            <TableCell>{preview.latest_verification.transfer_efficiency_pct?.toFixed(1)}%</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Adversarial score</TableCell>
                            <TableCell>{preview.latest_verification.adversarial_score?.toFixed(1)}/100</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Trust score</TableCell>
                            <TableCell>{preview.latest_verification.trust_score?.toFixed(1)}/100</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Verified on</TableCell>
                            <TableCell>{preview.latest_verification.created_at?.slice(0, 10)}</TableCell>
                          </TableRow>
                        </TableBody>
                      </Table>
                    </TableContainer>
                  ) : (
                    <p>No verification data yet.</p>
                  )}
                </Tile>
              </TabPanel>

              <TabPanel>
                <Tile className="amm-card">
                  <h2>Trust history</h2>
                  {trust ? (
                    <CodeSnippet type="multi">{trust.report}</CodeSnippet>
                  ) : (
                    <p>No trust history available.</p>
                  )}
                </Tile>
              </TabPanel>

              <TabPanel>
                <Tile className="amm-card">
                  <h2>Payload manifest</h2>
                  <p className="amm-subtle">Raw artifact content is encrypted and only accessible after purchase.</p>
                  <CodeSnippet type="multi">
{`artifact_hash: ${listing.artifact_hash}
domain: ${listing.domain}
license: ${listing.license_type}
sections: ${preview?.knowledge_summary?.sections?.join(', ') || 'unknown'}
token_count: ${preview?.knowledge_summary?.token_count || 'unknown'}`}
                  </CodeSnippet>
                </Tile>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Column>
      </Grid>
    </div>
  );
}
