const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

// Fallback mock data for when API is unreachable (e.g., Vercel preview)
const MOCK_LISTINGS: ListingRecord[] = [
  { id: 'demo-1', title: 'DeFi Risk Calibration Pack v2.1', description: 'Expert-calibrated risk scoring for DeFi protocols. Trained on 20 protocols across lending, bridges, yield aggregators, and stablecoins. Cross-model validated on GPT-4o.', domain: 'DeFi:risk-assessment', price_usd: 5.00, license_type: 'licensed', status: 'active', listed_at: '2026-04-23', seller_id: 'sentinel-labs', artifact_hash: 'a1b2c3d4e5f6...', trust_score: 92.5, verification_count: 1, feedback_count: 1, latest_transfer_efficiency: 92.2, latest_adversarial_score: 12.0 },
  { id: 'demo-2', title: 'CVE Severity Scorer v1.8', description: 'Vulnerability severity assessment trained on 16 real CVEs including Log4Shell, MOVEit, Zerologon. CVSS-anchored with operational context adjustment.', domain: 'CyberSec:vulnerability-assessment', price_usd: 8.00, license_type: 'licensed', status: 'active', listed_at: '2026-04-23', seller_id: 'neuroforge', artifact_hash: 'f7e8d9c0b1a2...', trust_score: 94.2, verification_count: 1, feedback_count: 1, latest_transfer_efficiency: 95.5, latest_adversarial_score: 12.0 },
  { id: 'demo-3', title: 'Fraud Escalation Memory Pack v3.2', description: 'Improves escalation accuracy for ambiguous chargeback and support cases. Best on fintech stacks. Signed provenance, cross-model validated.', domain: 'Support:escalation', price_usd: 12.00, license_type: 'licensed', status: 'active', listed_at: '2026-04-23', seller_id: 'sentinel-labs', artifact_hash: 'c3d4e5f6a7b8...', trust_score: 93.4, verification_count: 1, feedback_count: 0, latest_transfer_efficiency: 94.1, latest_adversarial_score: 12.0 },
  { id: 'demo-4', title: 'Research Citation Memory v2.0', description: 'Improves citation accuracy and source verification in research synthesis workflows. Low negative transfer risk.', domain: 'Research:citation-analysis', price_usd: 4.00, license_type: 'licensed', status: 'active', listed_at: '2026-04-23', seller_id: 'meridian-ai', artifact_hash: 'd4e5f6a7b8c9...', trust_score: 88.9, verification_count: 1, feedback_count: 1, latest_transfer_efficiency: 85.0, latest_adversarial_score: 12.0 },
  { id: 'demo-5', title: 'DeFi Incident Triage v1.7', description: 'Fast incident classification and response prioritization. Higher negative transfer risk under adversarial conditions.', domain: 'DeFi:incident-triage', price_usd: 3.50, license_type: 'licensed', status: 'active', listed_at: '2026-04-23', seller_id: 'cipher-collective', artifact_hash: 'e5f6a7b8c9d0...', trust_score: 85.6, verification_count: 1, feedback_count: 0, latest_transfer_efficiency: 78.4, latest_adversarial_score: 12.0 },
];

export type ListingRecord = {
  id: string;
  title: string;
  description: string;
  domain: string;
  price_usd: number;
  license_type: string;
  status: string;
  listed_at: string;
  seller_id: string;
  artifact_hash: string;
  trust_score: number | null;
  verification_count: number;
  feedback_count: number;
  latest_transfer_efficiency: number | null;
  latest_adversarial_score: number | null;
};

export type HealthResponse = {
  status: string;
  artifacts: number;
  listings: number;
  participants: number;
};

export async function fetchListings(params?: {
  domain?: string;
  min_trust?: number;
  max_price?: number;
}): Promise<ListingRecord[]> {
  try {
    const url = new URL(`${API_BASE}/api/listings`);
    if (params?.domain) url.searchParams.set('domain', params.domain);
    if (params?.min_trust) url.searchParams.set('min_trust', String(params.min_trust));
    if (params?.max_price) url.searchParams.set('max_price', String(params.max_price));

    const res = await fetch(url.toString());
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return data.listings;
  } catch {
    // Fallback to mock data when API is unreachable (Vercel preview)
    return MOCK_LISTINGS;
  }
}

export async function fetchListing(id: string): Promise<ListingRecord> {
  const res = await fetch(`${API_BASE}/api/listings/${id}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function fetchPreview(artifactHash: string) {
  const res = await fetch(`${API_BASE}/api/artifacts/${artifactHash}/preview`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function fetchTrust(artifactHash: string) {
  const res = await fetch(`${API_BASE}/api/trust/${artifactHash}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

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

const MOCK_TRANSACTIONS: TransactionRecord[] = [
  { id: 'txn-1001', assetId: 'demo-3', sellerId: 'sentinel-labs', buyerId: 'founder', amountUsd: 12, rail: 'USDC Escrow', status: 'Released', createdAt: '2026-04-24T09:12:00Z', notes: 'Fraud escalation pack attached to Support-17 after sandbox pass.' },
  { id: 'txn-1002', assetId: 'demo-2', sellerId: 'neuroforge', buyerId: 'founder', amountUsd: 8, rail: 'x402 Agentic Wallet', status: 'Metered', createdAt: '2026-04-24T10:48:00Z', notes: 'Per-request scoring attachment with spend cap and signed capability token.' },
  { id: 'txn-1003', assetId: 'demo-5', sellerId: 'cipher-collective', buyerId: 'founder', amountUsd: 3.5, rail: 'USDC Escrow', status: 'Held', createdAt: '2026-04-24T11:30:00Z', notes: 'Held pending additional adversarial review because seller is agent-wallet tier.' },
];

export async function fetchTransactions(): Promise<TransactionRecord[]> {
  try {
    const res = await fetch(`${API_BASE}/api/transactions`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return data.transactions;
  } catch {
    return MOCK_TRANSACTIONS;
  }
}

export type UserProfileRecord = {
  id: string;
  displayName: string;
  orgName: string;
  walletAddress: string;
  defaultPaymentRail: string;
  spendingPolicy: string;
  moderationPolicy: string;
  purchaseApprovals: string[];
};

const MOCK_USER_PROFILE: UserProfileRecord = {
  id: 'founder',
  displayName: 'Market Operator',
  orgName: 'AMM Labs',
  walletAddress: '0xA2A...402',
  defaultPaymentRail: 'USDC on Base with escrow release',
  spendingPolicy: 'Auto-buy under $2,000 for low-risk verified sellers. Human approval above medium risk.',
  moderationPolicy: 'Only verified sellers can list. Agent wallets require stake, attestation keys, and rate limits.',
  purchaseApprovals: ['Low risk / verified seller', 'USDC escrow', 'No raw payload until post-purchase'],
};

export async function fetchUserProfile(id = 'founder'): Promise<UserProfileRecord> {
  try {
    const res = await fetch(`${API_BASE}/api/identity/${id}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return {
      id: data.id,
      displayName: data.display_name || 'Unknown',
      orgName: data.org_name || '',
      walletAddress: data.wallet_address || '—',
      defaultPaymentRail: data.default_payment_rail || 'USDC',
      spendingPolicy: data.spending_policy || '',
      moderationPolicy: data.moderation_policy || '',
      purchaseApprovals: data.purchase_approvals || [],
    };
  } catch {
    return MOCK_USER_PROFILE;
  }
}
