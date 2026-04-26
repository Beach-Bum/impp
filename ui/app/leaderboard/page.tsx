'use client';

import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { useState, useMemo, Suspense } from 'react';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { ALL_ARTIFACTS, VERIFIED_ORDER, type Artifact } from '@/lib/artifacts';

type SortKey = 'trust' | 'te' | 'newest' | 'name';
type DomainFilter = 'All' | 'DeFi' | 'Cybersec';

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

        <Select value={sort} onValueChange={(v) => v && setSort(v as SortKey)}>
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
            <TableRow key={item.slug} className="cursor-pointer">
              <TableCell className="font-mono text-xs text-muted-foreground">{idx + 1}</TableCell>
              <TableCell>
                <Link href={`/package/${item.slug}`} className="hover:underline">
                  <span className="font-semibold">{item.name}</span>
                  <span className="ml-2 text-xs text-muted-foreground">{item.version}</span>
                </Link>
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
