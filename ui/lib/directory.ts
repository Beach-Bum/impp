import type { ListingRecord } from '@/lib/api';

export type VerificationTier = 'verified' | 'institutional' | 'agent-wallet';

export type SellerProfile = {
  id: string;
  name: string;
  handle: string;
  bio: string;
  website?: string;
  joinedAt: string;
  verifiedTier: VerificationTier;
  reputation: number;
  stakingUsd: number;
  disputeRatePct: number;
  successfulDeliveries: number;
  listedAssets: number;
  categories: string[];
  walletScheme: string;
  location: string;
};

export type UserProfile = {
  id: string;
  displayName: string;
  handle: string;
  role: string;
  verifiedTier: VerificationTier;
  orgName: string;
  walletAddress: string;
  defaultPaymentRail: string;
  spendingPolicy: string;
  moderationPolicy: string;
  purchaseApprovals: string[];
};

export type PaymentRail = {
  id: string;
  label: string;
  settlement: string;
  useCase: string;
  riskControls: string[];
};

export type TransactionRecord = {
  id: string;
  assetId: string;
  sellerId: string;
  buyerId: string;
  amountUsd: number;
  rail: string;
  status: string;
  createdAt: string;
  notes: string;
};

export type AuditRecord = {
  artifactId: string;
  signatureChain: { actor: string; action: string; at: string }[];
  controls: { name: string; status: 'pass' | 'warn' | 'blocked'; detail: string }[];
  payoutPolicy: string;
  rollbackPolicy: string;
  accessPolicy: string;
};

export const SELLERS: SellerProfile[] = [
  {
    id: 'sentinel-labs',
    name: 'Sentinel Labs',
    handle: '@sentinel',
    bio: 'Produces governed memory assets for fraud, escalation, and trust-sensitive workflows.',
    website: 'https://sentinel.example',
    joinedAt: '2026-02-18',
    verifiedTier: 'institutional',
    reputation: 97,
    stakingUsd: 25000,
    disputeRatePct: 0.8,
    successfulDeliveries: 214,
    listedAssets: 6,
    categories: ['Support', 'Fraud', 'Trust & Safety'],
    walletScheme: 'x402 + USDC settlement',
    location: 'London, UK',
  },
  {
    id: 'neuroforge',
    name: 'Neuroforge Security',
    handle: '@neuroforge',
    bio: 'Cybersecurity-focused artifact seller with CVE, triage, and exploit-analysis packs.',
    website: 'https://neuroforge.example',
    joinedAt: '2026-01-03',
    verifiedTier: 'verified',
    reputation: 94,
    stakingUsd: 12000,
    disputeRatePct: 1.6,
    successfulDeliveries: 132,
    listedAssets: 4,
    categories: ['CyberSec', 'Incident Response'],
    walletScheme: 'Escrow wallet + manual release',
    location: 'Berlin, Germany',
  },
  {
    id: 'meridian-ai',
    name: 'Meridian AI',
    handle: '@meridian',
    bio: 'Research and citation quality packs with strong provenance discipline.',
    joinedAt: '2026-03-10',
    verifiedTier: 'verified',
    reputation: 91,
    stakingUsd: 8000,
    disputeRatePct: 1.2,
    successfulDeliveries: 81,
    listedAssets: 3,
    categories: ['Research', 'Citation'],
    walletScheme: 'USDC + card fallback',
    location: 'Toronto, Canada',
  },
  {
    id: 'cipher-collective',
    name: 'Cipher Collective',
    handle: '@cipher',
    bio: 'Fast-moving DeFi response packs with higher variance and more aggressive tactics.',
    joinedAt: '2026-04-01',
    verifiedTier: 'agent-wallet',
    reputation: 79,
    stakingUsd: 3500,
    disputeRatePct: 4.9,
    successfulDeliveries: 26,
    listedAssets: 2,
    categories: ['DeFi', 'Incident Triage'],
    walletScheme: 'A2A wallet only',
    location: 'Distributed',
  },
];

export const USERS: UserProfile[] = [
  {
    id: 'founder',
    displayName: 'Market Operator',
    handle: '@operator',
    role: 'Admin / Buyer',
    verifiedTier: 'institutional',
    orgName: 'AMM Labs',
    walletAddress: '0xA2A...402',
    defaultPaymentRail: 'USDC on Base with escrow release',
    spendingPolicy: 'Auto-buy under $2,000 for low-risk verified sellers. Human approval above medium risk.',
    moderationPolicy: 'Only verified sellers can list. Agent wallets require stake, attestation keys, and rate limits.',
    purchaseApprovals: ['Low risk / verified seller', 'USDC escrow', 'No raw payload until post-purchase'],
  },
];

export const PAYMENT_RAILS: PaymentRail[] = [
  {
    id: 'usdc-escrow',
    label: 'USDC Escrow',
    settlement: 'Near-instant stablecoin settlement with delayed release',
    useCase: 'Standard artifact purchases and royalty splits',
    riskControls: ['escrow hold', 'refund window', 'dispute mediation'],
  },
  {
    id: 'x402',
    label: 'x402 Agentic Wallet',
    settlement: 'Machine-native request payment and capability-gated API flow',
    useCase: 'A2A purchases, metered retrieval, sandbox trials, and proof-of-payment routes',
    riskControls: ['signed requests', 'spend caps', 'per-artifact allowance', 'nonce + replay protection'],
  },
  {
    id: 'card-fallback',
    label: 'Card / Fiat Fallback',
    settlement: 'Traditional checkout',
    useCase: 'Human buyers and enterprise procurement',
    riskControls: ['manual review', 'fraud checks', 'KYC/KYB for sellers'],
  },
];

export const TRANSACTIONS: TransactionRecord[] = [
  {
    id: 'txn-1001',
    assetId: 'demo-3',
    sellerId: 'sentinel-labs',
    buyerId: 'founder',
    amountUsd: 12,
    rail: 'USDC Escrow',
    status: 'Released',
    createdAt: '2026-04-24T09:12:00Z',
    notes: 'Fraud escalation pack attached to Support-17 after sandbox pass.',
  },
  {
    id: 'txn-1002',
    assetId: 'demo-2',
    sellerId: 'neuroforge',
    buyerId: 'founder',
    amountUsd: 8,
    rail: 'x402 Agentic Wallet',
    status: 'Metered',
    createdAt: '2026-04-24T10:48:00Z',
    notes: 'Per-request scoring attachment with spend cap and signed capability token.',
  },
  {
    id: 'txn-1003',
    assetId: 'demo-5',
    sellerId: 'cipher-collective',
    buyerId: 'founder',
    amountUsd: 3.5,
    rail: 'USDC Escrow',
    status: 'Held',
    createdAt: '2026-04-24T11:30:00Z',
    notes: 'Held pending additional adversarial review because seller is agent-wallet tier.',
  },
];

export function getSellerProfile(id: string) {
  return SELLERS.find((seller) => seller.id === id) || null;
}

export function getUserProfile(id = 'founder') {
  return USERS.find((user) => user.id === id) || USERS[0];
}

export function getSellerListings(listings: ListingRecord[], sellerId: string) {
  return listings.filter((listing) => listing.seller_id === sellerId);
}

export function getAuditRecord(artifactId: string, listings: ListingRecord[]): AuditRecord {
  const listing = listings.find((item) => item.id === artifactId);
  const seller = getSellerProfile(listing?.seller_id || 'sentinel-labs');

  return {
    artifactId,
    signatureChain: [
      { actor: seller?.name || 'Unknown seller', action: 'Signed artifact manifest', at: '2026-04-22T13:02:00Z' },
      { actor: 'Marketplace Referee', action: 'Verified transfer and adversarial checks', at: '2026-04-23T09:15:00Z' },
      { actor: 'Buyer policy engine', action: 'Approved sandbox mount', at: '2026-04-24T08:31:00Z' },
    ],
    controls: [
      { name: 'Seller verification', status: seller?.verifiedTier === 'agent-wallet' ? 'warn' : 'pass', detail: seller?.verifiedTier === 'agent-wallet' ? 'Agent wallet seller requires stake and tighter spend caps.' : 'Identity and signing keys verified.' },
      { name: 'Prompt / memory poisoning screen', status: 'pass', detail: 'Artifact passed static checks and sandbox replay filters.' },
      { name: 'Negative transfer guard', status: listing?.trust_score && listing.trust_score < 80 ? 'warn' : 'pass', detail: listing?.trust_score && listing.trust_score < 80 ? 'Review required if negative transfer exceeds threshold.' : 'Auto-revoke if observed negative transfer exceeds 5%.' },
      { name: 'Payload release control', status: 'pass', detail: 'Raw payload stays encrypted until escrow release and audit retention is written.' },
    ],
    payoutPolicy: 'Release escrow after sandbox pass and 24h dispute window. Royalty split can flow to seller and co-signers.',
    rollbackPolicy: 'Detach asset and freeze new purchases if drift, poisoning, or rights breach is detected.',
    accessPolicy: 'Verified buyers only. Agent wallets must present signed x402 proofs and artifact-specific allowances.',
  };
}
