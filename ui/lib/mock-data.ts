export type AssetRecord = {
  slug: string;
  name: string;
  seller: string;
  domain: string;
  modelFamilies: string[];
  transferLift: string;
  negativeTransfer: string;
  freshness: string;
  rights: string;
  provenance: string;
  containment: string;
  price: string;
  summary: string;
};

export type AgentRecord = {
  id: string;
  name: string;
  memory: string;
  status: 'Healthy' | 'Watch' | 'Warning' | 'Blocked' | 'Revoked' | 'Expired';
  lastEval: string;
};

export type AlertRecord = {
  id: string;
  title: string;
  severity: 'Watch' | 'Warning' | 'Blocked';
  summary: string;
};

export const assets: AssetRecord[] = [
  {
    slug: 'fraud-escalation-memory-pack',
    name: 'Fraud Escalation Memory Pack v3.2',
    seller: 'Verified Org',
    domain: 'Support / Fintech',
    modelFamilies: ['Claude', 'GPT', 'Gemini'],
    transferLift: '+18%',
    negativeTransfer: '2.3%',
    freshness: '12 days',
    rights: 'Lease + revenue share',
    provenance: 'Signed lineage',
    containment: 'Retrieval only',
    price: '$1.8k / month',
    summary:
      'Improves escalation accuracy for ambiguous chargeback and support cases. Best on fintech support stacks and weaker on healthcare claims.',
  },
  {
    slug: 'defi-incident-triage',
    name: 'DeFi Incident Triage v1.7',
    seller: 'Research Lab',
    domain: 'DeFi / Security',
    modelFamilies: ['Claude', 'GPT'],
    transferLift: '+11%',
    negativeTransfer: '7.8%',
    freshness: '4 days',
    rights: 'No resale',
    provenance: 'Partial lineage',
    containment: 'Sandbox required',
    price: 'Usage based',
    summary:
      'Useful for fast incident triage, but requires tighter controls because drift rises faster under adversarial conditions.',
  },
  {
    slug: 'research-citation-memory',
    name: 'Research Citation Memory v2.0',
    seller: 'Independent Lab',
    domain: 'Research / Synthesis',
    modelFamilies: ['Claude', 'GPT', 'Llama'],
    transferLift: '+9%',
    negativeTransfer: '1.2%',
    freshness: '30 days',
    rights: 'Seat license',
    provenance: 'Signed lineage',
    containment: 'Standard',
    price: '$900 / month',
    summary:
      'Boosts citation consistency and reduces missing-source errors in synthesis-heavy workflows.',
  },
];

export const agents: AgentRecord[] = [
  { id: 'support-17', name: 'Support-17', memory: 'Fraud Escalation Memory Pack v3.2', status: 'Healthy', lastEval: '6h ago' },
  { id: 'cyber-blue-2', name: 'Cyber-Blue-2', memory: 'Vuln Prioritizer v1.4', status: 'Warning', lastEval: '2h ago' },
  { id: 'research-synth-4', name: 'Research-Synth-4', memory: 'Research Citation Memory v2.0', status: 'Healthy', lastEval: '14m ago' },
];

export const alerts: AlertRecord[] = [
  {
    id: 'alert-1',
    title: 'Drift alert on DeFi Triage',
    severity: 'Warning',
    summary: 'Held-out replay performance dropped and the artifact should stay sandboxed until re-evaluated.',
  },
  {
    id: 'alert-2',
    title: 'Hostile replay sandbox failure',
    severity: 'Blocked',
    summary: 'A hostile replay test triggered an unsafe path. The artifact has been auto-detached pending review.',
  },
  {
    id: 'alert-3',
    title: 'Renewal and rights review',
    severity: 'Watch',
    summary: 'One active lease expires in 9 days and will require renewed approval.',
  },
];

export const policySnapshot = {
  autoBuyCap: '$2,000',
  riskGate: 'Human approval above Medium',
  autoRevoke: 'Negative transfer > 5%',
  runtimeScope: 'Retrieval only / no tool autonomy',
};

export function getAssetBySlug(slug: string) {
  return assets.find((asset) => asset.slug === slug) ?? assets[0];
}

export function getAgentById(id: string) {
  return agents.find((agent) => agent.id === id) ?? agents[0];
}
