'use client';

import { useSearchParams } from 'next/navigation';
import { useState, useMemo, Suspense } from 'react';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

type Artifact = {
  name: string;
  version: string;
  domain: 'DeFi' | 'Cybersec';
  trust: number;
  te: number;
  status: 'SAFE';
  verified: string;
};

const DEFI_ARTIFACTS: Artifact[] = [
  { name: 'defi-risk-assessment', version: 'v2.1', domain: 'DeFi', trust: 97, te: 13.8, status: 'SAFE', verified: '2h ago' },
  { name: 'defi-yield-optimizer', version: 'v1.3', domain: 'DeFi', trust: 95, te: 12.9, status: 'SAFE', verified: '3h ago' },
  { name: 'defi-protocol-scanner', version: 'v1.0', domain: 'DeFi', trust: 93, te: 12.1, status: 'SAFE', verified: '5h ago' },
  { name: 'defi-liquidity-monitor', version: 'v0.9', domain: 'DeFi', trust: 92, te: 11.7, status: 'SAFE', verified: '6h ago' },
  { name: 'defi-governance-tracker', version: 'v1.2', domain: 'DeFi', trust: 91, te: 11.4, status: 'SAFE', verified: '8h ago' },
  { name: 'defi-bridge-validator', version: 'v0.8', domain: 'DeFi', trust: 90, te: 11.0, status: 'SAFE', verified: '10h ago' },
  { name: 'defi-token-classifier', version: 'v1.5', domain: 'DeFi', trust: 89, te: 10.8, status: 'SAFE', verified: '12h ago' },
  { name: 'defi-whale-detector', version: 'v2.0', domain: 'DeFi', trust: 98, te: 14.1, status: 'SAFE', verified: '2h ago' },
  { name: 'defi-rug-pull-detector', version: 'v1.1', domain: 'DeFi', trust: 88, te: 10.5, status: 'SAFE', verified: '14h ago' },
  { name: 'defi-impermanent-loss', version: 'v0.7', domain: 'DeFi', trust: 82, te: 8.9, status: 'SAFE', verified: '1d ago' },
  { name: 'defi-flash-loan-monitor', version: 'v1.0', domain: 'DeFi', trust: 86, te: 10.1, status: 'SAFE', verified: '16h ago' },
  { name: 'defi-mev-analyzer', version: 'v0.6', domain: 'DeFi', trust: 78, te: 7.8, status: 'SAFE', verified: '2d ago' },
  { name: 'defi-staking-optimizer', version: 'v1.4', domain: 'DeFi', trust: 91, te: 11.3, status: 'SAFE', verified: '9h ago' },
  { name: 'defi-oracle-validator', version: 'v1.1', domain: 'DeFi', trust: 87, te: 10.3, status: 'SAFE', verified: '15h ago' },
  { name: 'defi-tvl-tracker', version: 'v1.3', domain: 'DeFi', trust: 85, te: 9.7, status: 'SAFE', verified: '18h ago' },
  { name: 'defi-gas-optimizer', version: 'v0.9', domain: 'DeFi', trust: 83, te: 9.2, status: 'SAFE', verified: '1d ago' },
  { name: 'defi-pool-analyzer', version: 'v1.0', domain: 'DeFi', trust: 80, te: 8.4, status: 'SAFE', verified: '2d ago' },
  { name: 'defi-apy-calculator', version: 'v2.2', domain: 'DeFi', trust: 94, te: 12.6, status: 'SAFE', verified: '4h ago' },
  { name: 'defi-dao-monitor', version: 'v0.8', domain: 'DeFi', trust: 76, te: 7.3, status: 'SAFE', verified: '3d ago' },
  { name: 'defi-swap-router', version: 'v1.6', domain: 'DeFi', trust: 93, te: 12.2, status: 'SAFE', verified: '5h ago' },
  { name: 'defi-collateral-tracker', version: 'v1.1', domain: 'DeFi', trust: 84, te: 9.5, status: 'SAFE', verified: '20h ago' },
  { name: 'defi-leverage-monitor', version: 'v0.7', domain: 'DeFi', trust: 77, te: 7.5, status: 'SAFE', verified: '3d ago' },
  { name: 'defi-vault-scanner', version: 'v1.2', domain: 'DeFi', trust: 88, te: 10.6, status: 'SAFE', verified: '13h ago' },
  { name: 'defi-fee-analyzer', version: 'v0.5', domain: 'DeFi', trust: 72, te: 6.4, status: 'SAFE', verified: '5d ago' },
  { name: 'defi-slippage-guard', version: 'v1.0', domain: 'DeFi', trust: 81, te: 8.6, status: 'SAFE', verified: '1d ago' },
  { name: 'defi-portfolio-rebalancer', version: 'v1.3', domain: 'DeFi', trust: 90, te: 11.1, status: 'SAFE', verified: '11h ago' },
  { name: 'defi-cross-chain-monitor', version: 'v0.6', domain: 'DeFi', trust: 74, te: 6.9, status: 'SAFE', verified: '4d ago' },
  { name: 'defi-liquidation-alert', version: 'v1.1', domain: 'DeFi', trust: 86, te: 10.0, status: 'SAFE', verified: '17h ago' },
];

const CYBERSEC_ARTIFACTS: Artifact[] = [
  { name: 'cybersec-threat-intel', version: 'v1.4', domain: 'Cybersec', trust: 96, te: 13.4, status: 'SAFE', verified: '2h ago' },
  { name: 'cybersec-vuln-scanner', version: 'v2.0', domain: 'Cybersec', trust: 97, te: 13.9, status: 'SAFE', verified: '3h ago' },
  { name: 'cybersec-malware-classifier', version: 'v1.2', domain: 'Cybersec', trust: 92, te: 11.8, status: 'SAFE', verified: '6h ago' },
  { name: 'cybersec-phishing-detector', version: 'v1.0', domain: 'Cybersec', trust: 89, te: 10.7, status: 'SAFE', verified: '10h ago' },
  { name: 'cybersec-incident-response', version: 'v0.9', domain: 'Cybersec', trust: 87, te: 10.2, status: 'SAFE', verified: '14h ago' },
  { name: 'cybersec-log-analyzer', version: 'v1.3', domain: 'Cybersec', trust: 91, te: 11.5, status: 'SAFE', verified: '8h ago' },
  { name: 'cybersec-network-monitor', version: 'v1.1', domain: 'Cybersec', trust: 88, te: 10.4, status: 'SAFE', verified: '12h ago' },
  { name: 'cybersec-apt-tracker', version: 'v0.8', domain: 'Cybersec', trust: 83, te: 9.1, status: 'SAFE', verified: '1d ago' },
  { name: 'cybersec-ransomware-detector', version: 'v1.0', domain: 'Cybersec', trust: 90, te: 11.2, status: 'SAFE', verified: '9h ago' },
  { name: 'cybersec-supply-chain-audit', version: 'v0.7', domain: 'Cybersec', trust: 79, te: 8.1, status: 'SAFE', verified: '2d ago' },
  { name: 'cybersec-zero-day-monitor', version: 'v1.2', domain: 'Cybersec', trust: 94, te: 12.5, status: 'SAFE', verified: '4h ago' },
  { name: 'cybersec-dns-analyzer', version: 'v0.9', domain: 'Cybersec', trust: 82, te: 8.8, status: 'SAFE', verified: '1d ago' },
  { name: 'cybersec-endpoint-guard', version: 'v1.5', domain: 'Cybersec', trust: 95, te: 13.1, status: 'SAFE', verified: '3h ago' },
  { name: 'cybersec-siem-connector', version: 'v1.0', domain: 'Cybersec', trust: 85, te: 9.8, status: 'SAFE', verified: '18h ago' },
  { name: 'cybersec-firewall-auditor', version: 'v1.1', domain: 'Cybersec', trust: 86, te: 10.0, status: 'SAFE', verified: '16h ago' },
  { name: 'cybersec-credential-scanner', version: 'v0.8', domain: 'Cybersec', trust: 80, te: 8.3, status: 'SAFE', verified: '2d ago' },
  { name: 'cybersec-traffic-analyzer', version: 'v1.3', domain: 'Cybersec', trust: 93, te: 12.3, status: 'SAFE', verified: '5h ago' },
  { name: 'cybersec-patch-validator', version: 'v0.6', domain: 'Cybersec', trust: 75, te: 7.1, status: 'SAFE', verified: '4d ago' },
  { name: 'cybersec-honeypot-manager', version: 'v1.0', domain: 'Cybersec', trust: 84, te: 9.4, status: 'SAFE', verified: '20h ago' },
  { name: 'cybersec-iam-auditor', version: 'v1.2', domain: 'Cybersec', trust: 88, te: 10.5, status: 'SAFE', verified: '13h ago' },
  { name: 'cybersec-dlp-monitor', version: 'v0.9', domain: 'Cybersec', trust: 81, te: 8.5, status: 'SAFE', verified: '1d ago' },
  { name: 'cybersec-cert-validator', version: 'v1.1', domain: 'Cybersec', trust: 87, te: 10.3, status: 'SAFE', verified: '15h ago' },
  { name: 'cybersec-container-scanner', version: 'v1.4', domain: 'Cybersec', trust: 92, te: 11.9, status: 'SAFE', verified: '7h ago' },
  { name: 'cybersec-osint-collector', version: 'v0.7', domain: 'Cybersec', trust: 76, te: 7.4, status: 'SAFE', verified: '3d ago' },
  { name: 'cybersec-waf-tester', version: 'v1.0', domain: 'Cybersec', trust: 83, te: 9.0, status: 'SAFE', verified: '1d ago' },
  { name: 'cybersec-forensic-toolkit', version: 'v1.3', domain: 'Cybersec', trust: 91, te: 11.4, status: 'SAFE', verified: '9h ago' },
  { name: 'cybersec-pentest-framework', version: 'v0.5', domain: 'Cybersec', trust: 69, te: 5.7, status: 'SAFE', verified: '7d ago' },
  { name: 'cybersec-compliance-checker', version: 'v1.1', domain: 'Cybersec', trust: 85, te: 9.6, status: 'SAFE', verified: '19h ago' },
];

const ALL_ARTIFACTS: Artifact[] = [...DEFI_ARTIFACTS, ...CYBERSEC_ARTIFACTS];

type SortKey = 'trust' | 'te' | 'newest' | 'name';
type DomainFilter = 'All' | 'DeFi' | 'Cybersec';

const VERIFIED_ORDER: Record<string, number> = {
  '2h ago': 2, '3h ago': 3, '4h ago': 4, '5h ago': 5, '6h ago': 6,
  '7h ago': 7, '8h ago': 8, '9h ago': 9, '10h ago': 10, '11h ago': 11,
  '12h ago': 12, '13h ago': 13, '14h ago': 14, '15h ago': 15, '16h ago': 16,
  '17h ago': 17, '18h ago': 18, '19h ago': 19, '20h ago': 20,
  '1d ago': 24, '2d ago': 48, '3d ago': 72, '4d ago': 96, '5d ago': 120,
  '7d ago': 168, '30d ago': 720,
};

function LeaderboardContent() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get('q') || '';

  const [domain, setDomain] = useState<DomainFilter>('All');
  const [sort, setSort] = useState<SortKey>('trust');
  const [search, setSearch] = useState(initialQuery);

  const filtered = useMemo(() => {
    let items = [...ALL_ARTIFACTS];
    if (domain !== 'All') items = items.filter((a) => a.domain === domain);
    if (search.trim()) {
      const q = search.trim().toLowerCase();
      items = items.filter((a) => a.name.toLowerCase().includes(q));
    }
    items.sort((a, b) => {
      switch (sort) {
        case 'trust': return b.trust - a.trust;
        case 'te': return b.te - a.te;
        case 'newest': return (VERIFIED_ORDER[a.verified] || 999) - (VERIFIED_ORDER[b.verified] || 999);
        case 'name': return a.name.localeCompare(b.name);
        default: return 0;
      }
    });
    return items;
  }, [domain, sort, search]);

  const avgTrust = filtered.length > 0 ? (filtered.reduce((s, a) => s + a.trust, 0) / filtered.length).toFixed(1) : '0.0';
  const avgTe = filtered.length > 0 ? (filtered.reduce((s, a) => s + a.te, 0) / filtered.length).toFixed(1) : '0.0';

  const domainButtons: DomainFilter[] = ['All', 'DeFi', 'Cybersec'];

  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Verified Artifacts</h1>
      <p className="mb-6 text-sm text-muted-foreground">
        56 artifacts across 2 domains. Every artifact passes adversarial probes before listing.
      </p>

      <div className="mb-4 flex flex-wrap items-center gap-2">
        {domainButtons.map((d) => (
          <Badge
            key={d}
            variant={domain === d ? 'default' : 'secondary'}
            className="cursor-pointer select-none"
            onClick={() => setDomain(d)}
          >
            {d}
          </Badge>
        ))}

        <Select value={sort} onValueChange={(v) => setSort(v as SortKey)}>
          <SelectTrigger className="ml-2 w-[180px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="trust">Trust Score</SelectItem>
            <SelectItem value="te">Transfer Effectiveness</SelectItem>
            <SelectItem value="newest">Newest</SelectItem>
            <SelectItem value="name">Name</SelectItem>
          </SelectContent>
        </Select>

        <Input
          type="text"
          placeholder="Search artifacts..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="ml-auto w-56"
        />
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-12">#</TableHead>
            <TableHead>Package</TableHead>
            <TableHead>Domain</TableHead>
            <TableHead className="text-right">Trust</TableHead>
            <TableHead className="text-right">TE</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Verified</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((item, idx) => (
            <TableRow key={item.name}>
              <TableCell className="font-mono text-xs text-muted-foreground">{idx + 1}</TableCell>
              <TableCell>
                <span className="font-semibold">{item.name}</span>
                <span className="ml-2 text-xs text-muted-foreground">{item.version}</span>
              </TableCell>
              <TableCell>
                <Badge variant={item.domain === 'DeFi' ? 'default' : 'secondary'}>{item.domain}</Badge>
              </TableCell>
              <TableCell className="text-right font-mono font-semibold">{item.trust}</TableCell>
              <TableCell className="text-right font-mono">+{item.te.toFixed(1)}%</TableCell>
              <TableCell><Badge>SAFE</Badge></TableCell>
              <TableCell className="text-xs text-muted-foreground">{item.verified}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <div className="mt-4 flex gap-6 border-t pt-3 text-sm text-muted-foreground">
        <span>Showing <strong className="text-foreground">{filtered.length}</strong> of 56 artifacts</span>
        <span>Avg trust: <strong className="font-mono text-foreground">{avgTrust}</strong></span>
        <span>Avg TE: <strong className="font-mono text-foreground">+{avgTe}%</strong></span>
      </div>
    </div>
  );
}

export default function LeaderboardPage() {
  return (
    <Suspense fallback={
      <div className="mx-auto max-w-5xl px-5 py-8">
        <h1 className="text-2xl font-light">Verified Artifacts</h1>
        <p className="text-sm text-muted-foreground">Loading...</p>
      </div>
    }>
      <LeaderboardContent />
    </Suspense>
  );
}
