'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Box, Button, Flash, Heading, Label, Link as PrimerLink, Spinner } from '@primer/react';
import { fetchListings, type ListingRecord } from '@/lib/api';
import { getSellerListings, getSellerProfile } from '@/lib/directory';

function tierVariant(tier: string): 'success' | 'accent' | 'attention' {
  if (tier === 'institutional') return 'success';
  if (tier === 'verified') return 'accent';
  return 'attention';
}

export default function SellerProfileScreen({ sellerId }: { sellerId: string }) {
  const [listings, setListings] = useState<ListingRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const seller = getSellerProfile(sellerId);

  useEffect(() => {
    fetchListings().then(setListings).finally(() => setLoading(false));
  }, []);

  if (!seller) {
    return <div className="amm-page"><Flash variant="danger">Seller not found.</Flash></div>;
  }

  const sellerListings = getSellerListings(listings, seller.id);

  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>{seller.name}</Heading>
      <p className="amm-screen-subtitle">Seller profile, verification, dispute posture, and wallet identity.</p>

      <div className="amm-grid amm-grid-2col">
        <div className="amm-card-stack">
          <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '12px', flexWrap: 'wrap' }}>
              <Label variant={tierVariant(seller.verifiedTier)}>{seller.verifiedTier}</Label>
              <Label variant="secondary">Rep {seller.reputation}</Label>
              <Label variant="secondary">Stake ${seller.stakingUsd.toLocaleString()}</Label>
            </div>
            <p style={{ marginTop: 0 }}>{seller.bio}</p>
            <div className="amm-card-stack">
              <span className="amm-subtle">Handle: {seller.handle}</span>
              <span className="amm-subtle">Location: {seller.location}</span>
              <span className="amm-subtle">Wallet rail: {seller.walletScheme}</span>
              <span className="amm-subtle">Joined: {seller.joinedAt}</span>
              {seller.website ? <PrimerLink href={seller.website}>{seller.website}</PrimerLink> : null}
            </div>
          </Box>

          <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
            <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Trust posture</Heading>
            <div className="amm-metric-grid" style={{ gridTemplateColumns: 'repeat(3, minmax(0, 1fr))' }}>
              <div className="amm-metric-tile"><span className="amm-metric-label">Deliveries</span><span className="amm-metric-value">{seller.successfulDeliveries}</span></div>
              <div className="amm-metric-tile"><span className="amm-metric-label">Dispute rate</span><span className="amm-metric-value">{seller.disputeRatePct}%</span></div>
              <div className="amm-metric-tile"><span className="amm-metric-label">Listings</span><span className="amm-metric-value">{seller.listedAssets}</span></div>
            </div>
            <div className="amm-inline-tags" style={{ marginTop: '12px' }}>
              {seller.categories.map((category) => <Label key={category} variant="secondary">{category}</Label>)}
            </div>
          </Box>
        </div>

        <div className="amm-card-stack">
          <Flash variant={seller.verifiedTier === 'agent-wallet' ? 'warning' : 'success'}>
            <strong>{seller.verifiedTier === 'agent-wallet' ? 'Enhanced review required' : 'Verified seller'}</strong>
            <br />
            {seller.verifiedTier === 'agent-wallet'
              ? 'Agent-wallet sellers need spend caps, signed allowances, and slower payout release.'
              : 'Seller identity and signing keys have passed listing review.'}
          </Flash>
          <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, p: 3 }}>
            <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Commercial controls</Heading>
            <span className="amm-subtle" style={{ display: 'block' }}>Escrow release after sandbox pass</span>
            <span className="amm-subtle" style={{ display: 'block' }}>Stake can be slashed on fraud or rights breach</span>
            <span className="amm-subtle" style={{ display: 'block' }}>Royalty splits supported for co-signers and marketplaces</span>
            <div style={{ marginTop: '12px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              <Button as="a" href="/payments">Payment rails</Button>
              <Button as="a" href="/transactions" variant="invisible">Transactions</Button>
            </div>
          </Box>
        </div>
      </div>

      <Box sx={{ border: '1px solid', borderColor: 'border.default', borderRadius: 2, overflow: 'hidden', mt: 3 }}>
        <div style={{ padding: '16px', borderBottom: '1px solid var(--borderColor-default, #d0d7de)' }}>
          <Heading as="h2" sx={{ fontSize: 2 }}>Listed artifacts</Heading>
        </div>
        {loading ? (
          <div style={{ padding: '24px' }}><Spinner size="medium" /></div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--borderColor-default, #d0d7de)' }}>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Artifact</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Trust</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Lift</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Price</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {sellerListings.map((item) => (
                <tr key={item.id} style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                  <td style={{ padding: '8px 12px' }}><strong>{item.title}</strong><div className="amm-subtle">{item.domain}</div></td>
                  <td style={{ padding: '8px 12px' }}>{item.trust_score?.toFixed(1) ?? '—'}/100</td>
                  <td style={{ padding: '8px 12px' }}>{item.latest_transfer_efficiency?.toFixed(1) ?? '—'}%</td>
                  <td style={{ padding: '8px 12px' }}>${item.price_usd.toFixed(2)}</td>
                  <td style={{ padding: '8px 12px' }}><Link href={`/asset/${item.id}`}>Review</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Box>
    </div>
  );
}
