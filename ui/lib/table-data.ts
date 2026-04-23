import { agents, assets } from '@/lib/mock-data';

export const assetHeaders = [
  { key: 'asset', header: 'Asset' },
  { key: 'lift', header: 'Lift' },
  { key: 'negative', header: 'Negative' },
  { key: 'freshness', header: 'Freshness' },
  { key: 'provenance', header: 'Provenance' },
  { key: 'rights', header: 'Rights' },
  { key: 'price', header: 'Price' },
];

export const assetRows = assets.map((asset) => ({
  id: asset.slug,
  asset: asset.name,
  domain: asset.domain,
  modelFamilies: asset.modelFamilies.join(' / '),
  lift: asset.transferLift,
  negative: asset.negativeTransfer,
  freshness: asset.freshness,
  provenance: asset.provenance,
  rights: asset.rights,
  price: asset.price,
}));

export const agentHeaders = [
  { key: 'agent', header: 'Agent' },
  { key: 'memory', header: 'Attached memory' },
  { key: 'status', header: 'Status' },
  { key: 'lastEval', header: 'Last eval' },
];

export const agentRows = agents.map((agent) => ({
  id: agent.id,
  agent: agent.name,
  memory: agent.memory,
  status: agent.status,
  lastEval: agent.lastEval,
}));
