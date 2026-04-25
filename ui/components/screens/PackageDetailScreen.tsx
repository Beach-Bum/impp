'use client';

import Link from 'next/link';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Progress } from '@/components/ui/progress';
import { CodeBlock } from '@/components/ui/code-block';
import { CountingNumber } from '@/components/animate-ui/primitives/texts/counting-number';
import { CopyButton } from '@/components/animate-ui/components/buttons/copy';
import { Shield, GitBranch, Clock, User, ExternalLink, FileText, Download } from 'lucide-react';

// Package data keyed by slug (matches landing page newPackages)
const PACKAGES: Record<string, PackageData> = {
  'impp-defi-risk-assessment': {
    name: 'impp/defi-risk-assessment',
    version: 'v2.1.0',
    description: 'Expert-calibrated risk scoring for DeFi protocols. Trained on 20 protocols across lending, bridges, yield aggregators, and stablecoins. Cross-model validated on GPT-4o and Claude Sonnet.',
    domain: 'DeFi',
    license: 'MIT',
    installCmd: 'impp install impp/defi-risk-assessment',
    publishedAt: '2026-04-23',
    updatedAt: '2026-04-25 18:42 UTC',
    author: 'Sentinel Labs',
    authorHandle: '@sentinel',
    sellerId: 'sentinel-labs',
    repoUrl: 'github.com/sentinel-labs/defi-risk-assessment',
    trustScore: 92.5,
    transferEfficiency: 92.2,
    adversarialScore: 12.0,
    verificationCount: 3,
    installs: 214,
    dependents: 4,
    stars: 12,
    openIssues: 0,
    advisories: 0,
    versions: ['v2.1.0', 'v2.0.0', 'v1.4.2', 'v1.4.1', 'v1.4.0', 'v1.3.0', 'v1.2.0', 'v1.1.0', 'v1.0.0'],
    artifactHash: 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0',
    certFingerprint: 'ed25519:7f3a9c2d...e8b1',
    requires: { 'impp/core': '^1.0', 'impp/verification': '^0.5' },
    requiresDev: { 'impp/test-harness': '^1.0' },
    probes: [
      { name: 'Steganography detection', status: 'pass', score: 98 },
      { name: 'Overfit detection', status: 'pass', score: 95 },
      { name: 'Negative transfer risk', status: 'pass', score: 88 },
      { name: 'Cross-model compatibility', status: 'pass', score: 94 },
      { name: 'Freshness analysis', status: 'pass', score: 91 },
    ],
    readme: `## DeFi Risk Calibration Pack v2.1

Expert-calibrated risk assessment memory for DeFi protocol evaluation. This artifact encodes learned risk heuristics from 20 real DeFi protocols across lending, bridges, yield aggregators, and stablecoins.

### What's Included

- **Risk scoring framework** — Calibrated scoring rules for protocol attributes including TVL, audit history, governance model, team concentration, and insurance coverage.
- **Protocol templates** — Pre-scored baselines for major protocol categories (lending, DEX, bridge, yield, stablecoin).
- **Trap detection** — Learned patterns for identifying deceptively safe-looking protocols with hidden risk factors.

### Cross-Model Transfer

This artifact has been validated across GPT-4o and Claude Sonnet with +8-14% transfer effectiveness improvement over baseline.

### Usage

\`\`\`python
import impp

artifact = impp.load("impp/defi-risk-assessment")
result = artifact.assess(protocol_data)
print(result.risk_score)  # 0-100
print(result.flags)       # List of risk factors
\`\`\`

### Verification

All versions pass the full IMPP adversarial probe battery:
- Steganography detection detection
- Overfit probe (train/test distribution shift)
- Negative transfer risk assessment
- Cross-model compatibility check
- Freshness and staleness analysis`,
  },
  'impp-cybersec-threat-intel': {
    name: 'impp/cybersec-threat-intel',
    version: 'v1.4.0',
    description: 'Vulnerability severity assessment trained on 16 real CVEs including Log4Shell, MOVEit, Zerologon. CVSS-anchored with operational context adjustment.',
    domain: 'CyberSec',
    license: 'MIT',
    installCmd: 'impp install impp/cybersec-threat-intel',
    publishedAt: '2026-04-23',
    updatedAt: '2026-04-25 14:10 UTC',
    author: 'Neuroforge Security',
    authorHandle: '@neuroforge',
    sellerId: 'neuroforge',
    repoUrl: 'github.com/neuroforge/cybersec-threat-intel',
    trustScore: 94.2,
    transferEfficiency: 95.5,
    adversarialScore: 8.5,
    verificationCount: 3,
    installs: 132,
    dependents: 2,
    stars: 8,
    openIssues: 1,
    advisories: 0,
    versions: ['v1.4.0', 'v1.3.1', 'v1.3.0', 'v1.2.0', 'v1.1.0', 'v1.0.0'],
    artifactHash: 'f7e8d9c0b1a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6',
    certFingerprint: 'ed25519:3b8e1f7a...c4d2',
    requires: { 'impp/core': '^1.0', 'impp/verification': '^0.5' },
    requiresDev: { 'impp/test-harness': '^1.0' },
    probes: [
      { name: 'Steganography detection', status: 'pass', score: 99 },
      { name: 'Overfit detection', status: 'pass', score: 96 },
      { name: 'Negative transfer risk', status: 'pass', score: 92 },
      { name: 'Cross-model compatibility', status: 'pass', score: 97 },
      { name: 'Freshness analysis', status: 'pass', score: 89 },
    ],
    readme: `## CVE Severity Scorer v1.4

Vulnerability severity assessment memory trained on 16 real-world CVEs. CVSS-anchored scoring with operational context adjustment for realistic prioritization.

### Coverage

Log4Shell, MOVEit, Zerologon, SolarWinds, PrintNightmare, ProxyLogon, Spring4Shell, and 9 more high-profile CVEs with full operational context.

### Usage

\`\`\`python
import impp

artifact = impp.load("impp/cybersec-threat-intel")
result = artifact.assess(cve_data)
print(result.severity)     # critical/high/medium/low
print(result.cvss_adjusted) # Context-adjusted CVSS score
\`\`\``,
  },
  'impp-code-review-patterns': {
    name: 'impp/code-review-patterns',
    version: 'v0.9.0',
    description: 'Learned code review heuristics from 500+ production PRs. Detects anti-patterns, security issues, and performance regressions with low false positive rate.',
    domain: 'Engineering',
    license: 'Apache-2.0',
    installCmd: 'impp install impp/code-review-patterns',
    publishedAt: '2026-04-21',
    updatedAt: '2026-04-24 09:30 UTC',
    author: 'Meridian AI',
    authorHandle: '@meridian',
    sellerId: 'meridian-ai',
    repoUrl: 'github.com/meridian-ai/code-review-patterns',
    trustScore: 87.3,
    transferEfficiency: 85.0,
    adversarialScore: 15.2,
    verificationCount: 2,
    installs: 81,
    dependents: 1,
    stars: 5,
    openIssues: 2,
    advisories: 0,
    versions: ['v0.9.0', 'v0.8.1', 'v0.8.0', 'v0.7.0'],
    artifactHash: 'd4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3',
    certFingerprint: 'ed25519:9a2c4e6f...b3d5',
    requires: { 'impp/core': '^1.0' },
    requiresDev: {},
    probes: [
      { name: 'Steganography detection', status: 'pass', score: 94 },
      { name: 'Overfit detection', status: 'pass', score: 88 },
      { name: 'Negative transfer risk', status: 'warn', score: 76 },
      { name: 'Cross-model compatibility', status: 'pass', score: 90 },
      { name: 'Freshness analysis', status: 'pass', score: 85 },
    ],
    readme: `## Code Review Patterns v0.9

Learned code review heuristics from 500+ production pull requests across Python, TypeScript, and Go codebases.

### Usage

\`\`\`python
import impp

artifact = impp.load("impp/code-review-patterns")
result = artifact.review(diff_text, language="python")
for finding in result.findings:
    print(f"{finding.severity}: {finding.message}")
\`\`\``,
  },
  'impp-medical-literature': {
    name: 'impp/medical-literature',
    version: 'v1.0.0',
    description: 'Research citation quality and verification memory for medical literature synthesis. Trained on PubMed and Cochrane systematic review datasets.',
    domain: 'Research',
    license: 'CC-BY-4.0',
    installCmd: 'impp install impp/medical-literature',
    publishedAt: '2026-04-19',
    updatedAt: '2026-04-22 16:00 UTC',
    author: 'Meridian AI',
    authorHandle: '@meridian',
    sellerId: 'meridian-ai',
    repoUrl: 'github.com/meridian-ai/medical-literature',
    trustScore: 85.1,
    transferEfficiency: 82.3,
    adversarialScore: 18.0,
    verificationCount: 2,
    installs: 47,
    dependents: 0,
    stars: 3,
    openIssues: 0,
    advisories: 0,
    versions: ['v1.0.0', 'v0.9.0', 'v0.8.0'],
    artifactHash: 'e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4',
    certFingerprint: 'ed25519:5d7e9f1a...a2c4',
    requires: { 'impp/core': '^1.0', 'impp/verification': '^0.5' },
    requiresDev: {},
    probes: [
      { name: 'Steganography detection', status: 'pass', score: 92 },
      { name: 'Overfit detection', status: 'pass', score: 84 },
      { name: 'Negative transfer risk', status: 'warn', score: 72 },
      { name: 'Cross-model compatibility', status: 'pass', score: 88 },
      { name: 'Freshness analysis', status: 'pass', score: 80 },
    ],
    readme: `## Medical Literature Memory v1.0

Research citation quality and verification for medical literature synthesis workflows. Trained on PubMed and Cochrane datasets.

### Usage

\`\`\`python
import impp

artifact = impp.load("impp/medical-literature")
result = artifact.verify_citation(paper_data)
print(result.quality_score)  # 0-100
print(result.issues)          # List of citation issues
\`\`\``,
  },
};

type PackageData = {
  name: string;
  version: string;
  description: string;
  domain: string;
  license: string;
  installCmd: string;
  publishedAt: string;
  updatedAt: string;
  author: string;
  authorHandle: string;
  sellerId: string;
  repoUrl: string;
  trustScore: number;
  transferEfficiency: number;
  adversarialScore: number;
  verificationCount: number;
  installs: number;
  dependents: number;
  stars: number;
  openIssues: number;
  advisories: number;
  versions: string[];
  artifactHash: string;
  certFingerprint: string;
  requires: Record<string, string>;
  requiresDev: Record<string, string>;
  probes: { name: string; status: string; score: number }[];
  readme: string;
};

function TrustBadge({ score }: { score: number }) {
  if (score >= 90) return <Badge className="bg-green-600 text-white">Verified</Badge>;
  if (score >= 70) return <Badge variant="secondary">Caution</Badge>;
  return <Badge variant="destructive">Low Trust</Badge>;
}

export default function PackageDetailScreen({ slug }: { slug: string }) {
  const pkg = PACKAGES[slug];

  if (!pkg) {
    return (
      <div className="mx-auto max-w-5xl px-5 py-16 text-center">
        <h1 className="text-2xl font-light mb-2">Package not found</h1>
        <p className="text-muted-foreground mb-4">No package matching &ldquo;{slug}&rdquo; in the registry.</p>
        <Link href="/leaderboard" className="text-primary underline">Browse all packages</Link>
      </div>
    );
  }

  return (
    <TooltipProvider>
      <div className="mx-auto max-w-5xl px-5 py-8">
        {/* Package title */}
        <h1 className="text-3xl font-light mb-1">{pkg.name}</h1>

        {/* Install command */}
        <div className="flex items-center gap-2 mb-3">
          <div className="flex items-center gap-2 rounded-md border bg-muted/50 px-3 py-1.5 font-mono text-sm flex-1 max-w-lg">
            <Download className="h-4 w-4 shrink-0 text-muted-foreground" />
            <span className="truncate">{pkg.installCmd}</span>
            <CopyButton content={pkg.installCmd} size="xs" variant="ghost" className="ml-auto shrink-0" />
          </div>
        </div>

        {/* Description */}
        <p className="text-sm text-muted-foreground mb-6 max-w-2xl">{pkg.description}</p>

        {/* Main layout: content + sidebar */}
        <div className="grid gap-8 lg:grid-cols-[1fr_290px]">
          {/* Main content */}
          <div className="min-w-0 space-y-8">
            {/* Version + date bar */}
            <div className="flex items-center justify-between border-b pb-3">
              <div className="flex items-center gap-2">
                <Badge variant="outline">{pkg.version}</Badge>
                <TrustBadge score={pkg.trustScore} />
                <Badge variant="secondary">{pkg.domain}</Badge>
              </div>
              <span className="text-xs text-muted-foreground">{pkg.updatedAt}</span>
            </div>

            {/* Trust Score Card */}
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 mb-4">
                  <Shield className="h-5 w-5 text-primary" />
                  <h2 className="text-lg font-medium">Trust Score</h2>
                  <span className="ml-auto text-2xl font-light tabular-nums">
                    <CountingNumber number={pkg.trustScore} decimalPlaces={1} inView />
                    <span className="text-sm text-muted-foreground">/100</span>
                  </span>
                </div>
                <Progress value={pkg.trustScore} className="h-2 mb-4" />

                <h3 className="text-sm font-medium mb-2">Adversarial Probes</h3>
                <div className="space-y-2">
                  {pkg.probes.map((probe) => (
                    <div key={probe.name} className="flex items-center gap-3">
                      <span className={`h-2 w-2 rounded-full shrink-0 ${probe.status === 'pass' ? 'bg-green-500' : 'bg-amber-500'}`} />
                      <span className="text-sm flex-1">{probe.name}</span>
                      <Tooltip>
                        <TooltipTrigger>
                          <span className="text-xs font-mono tabular-nums text-muted-foreground">{probe.score}/100</span>
                        </TooltipTrigger>
                        <TooltipContent>Probe score: {probe.score}/100 ({probe.status})</TooltipContent>
                      </Tooltip>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Dependencies */}
            <div>
              <h2 className="text-lg font-light mb-3">Dependencies</h2>
              <div className="grid gap-6 sm:grid-cols-2">
                <div>
                  <h3 className="text-sm font-medium mb-2">Requires</h3>
                  {Object.keys(pkg.requires).length > 0 ? (
                    <ul className="space-y-1">
                      {Object.entries(pkg.requires).map(([dep, ver]) => (
                        <li key={dep} className="text-sm">
                          <code className="rounded bg-muted px-1.5 py-0.5 text-xs">{dep}</code>
                          <span className="ml-2 text-muted-foreground">{ver}</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-sm text-muted-foreground">None</p>
                  )}
                </div>
                <div>
                  <h3 className="text-sm font-medium mb-2">Requires (Dev)</h3>
                  {Object.keys(pkg.requiresDev).length > 0 ? (
                    <ul className="space-y-1">
                      {Object.entries(pkg.requiresDev).map(([dep, ver]) => (
                        <li key={dep} className="text-sm">
                          <code className="rounded bg-muted px-1.5 py-0.5 text-xs">{dep}</code>
                          <span className="ml-2 text-muted-foreground">{ver}</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-sm text-muted-foreground">None</p>
                  )}
                </div>
              </div>
            </div>

            {/* License + Certificate */}
            <div className="flex flex-wrap items-center gap-4 text-sm">
              <div className="flex items-center gap-1.5">
                <FileText className="h-4 w-4 text-muted-foreground" />
                <span>{pkg.license}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <GitBranch className="h-4 w-4 text-muted-foreground" />
                <Tooltip>
                  <TooltipTrigger>
                    <code className="rounded bg-muted px-1.5 py-0.5 text-xs cursor-help">{pkg.artifactHash}</code>
                  </TooltipTrigger>
                  <TooltipContent>Artifact content hash (SHA-256)</TooltipContent>
                </Tooltip>
              </div>
            </div>
            <div className="text-sm text-muted-foreground">
              {pkg.author} &lt;{pkg.authorHandle}&gt;
            </div>

            <Separator />

            {/* README */}
            <div>
              <h2 className="text-lg font-light mb-4">README</h2>
              <div className="prose prose-sm dark:prose-invert max-w-none">
                <ReadmeRenderer content={pkg.readme} />
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-4">
            {/* Maintainers */}
            <SidebarSection title="Maintainers">
              <Link href={`/preview/sellers/${pkg.sellerId}`} className="flex items-center gap-2 text-sm hover:underline">
                <User className="h-4 w-4" />
                {pkg.author}
              </Link>
            </SidebarSection>

            {/* Package Info */}
            <SidebarSection title="Package info">
              <div className="space-y-1.5 text-sm">
                <p className="truncate">
                  <Link href={`https://${pkg.repoUrl}`} className="text-primary hover:underline flex items-center gap-1" target="_blank">
                    {pkg.repoUrl}
                    <ExternalLink className="h-3 w-3" />
                  </Link>
                </p>
                <p className="text-muted-foreground">Domain: {pkg.domain}</p>
                <p className="text-muted-foreground">Certificate: {pkg.certFingerprint}</p>
              </div>
            </SidebarSection>

            {/* Statistics */}
            <SidebarSection title="Statistics">
              <Table>
                <TableBody>
                  <StatRow label="Installs" value={pkg.installs} />
                  <StatRow label="Dependents" value={pkg.dependents} />
                  <StatRow label="Stars" value={pkg.stars} />
                  <StatRow label="Open Issues" value={pkg.openIssues} />
                  <StatRow label="Verifications" value={pkg.verificationCount} />
                </TableBody>
              </Table>
            </SidebarSection>

            {/* Security */}
            <SidebarSection title="Security">
              <div className="space-y-1.5 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Advisories:</span>
                  <span>{pkg.advisories}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Trust:</span>
                  <span className="font-mono">{pkg.trustScore}/100</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Transfer eff.:</span>
                  <span className="font-mono">{pkg.transferEfficiency}%</span>
                </div>
              </div>
            </SidebarSection>

            {/* Versions */}
            <SidebarSection title="Versions">
              <div className="space-y-1">
                {pkg.versions.map((v, i) => (
                  <div key={v} className={`text-sm px-2 py-0.5 rounded ${i === 0 ? 'bg-muted font-medium' : 'text-muted-foreground hover:text-foreground cursor-pointer'}`}>
                    {v}
                  </div>
                ))}
              </div>
            </SidebarSection>

            <div className="text-xs text-muted-foreground space-y-0.5">
              <p>This package is auto-updated.</p>
              <p>Last update: {pkg.updatedAt}</p>
            </div>
          </div>
        </div>
      </div>
    </TooltipProvider>
  );
}

function SidebarSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <Card>
      <CardContent className="pt-4 pb-4">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">{title}</h3>
        {children}
      </CardContent>
    </Card>
  );
}

function StatRow({ label, value }: { label: string; value: number }) {
  return (
    <TableRow>
      <TableCell className="py-1 pl-0 text-sm text-muted-foreground">{label}:</TableCell>
      <TableCell className="py-1 pr-0 text-right text-sm font-mono">{value}</TableCell>
    </TableRow>
  );
}

function ReadmeRenderer({ content }: { content: string }) {
  // Simple markdown-like rendering for README content
  const sections = content.split('\n\n');

  return (
    <>
      {sections.map((block, i) => {
        const trimmed = block.trim();
        if (!trimmed) return null;

        if (trimmed.startsWith('```')) {
          const lines = trimmed.split('\n');
          const langMatch = lines[0].match(/```(\w+)/);
          const lang = langMatch?.[1];
          const code = lines.slice(1, -1).join('\n');
          return <CodeBlock key={i} language={lang}>{code}</CodeBlock>;
        }

        if (trimmed.startsWith('### ')) {
          return <h3 key={i} className="text-base font-semibold mt-4 mb-1">{trimmed.slice(4)}</h3>;
        }
        if (trimmed.startsWith('## ')) {
          return <h2 key={i} className="text-lg font-semibold mt-6 mb-2">{trimmed.slice(3)}</h2>;
        }

        if (trimmed.startsWith('- ')) {
          const items = trimmed.split('\n').filter(l => l.startsWith('- '));
          return (
            <ul key={i} className="list-disc pl-5 space-y-1">
              {items.map((item, j) => {
                const text = item.slice(2);
                const boldMatch = text.match(/^\*\*(.+?)\*\*(.*)$/);
                return (
                  <li key={j} className="text-sm">
                    {boldMatch ? <><strong>{boldMatch[1]}</strong>{boldMatch[2]}</> : text}
                  </li>
                );
              })}
            </ul>
          );
        }

        return <p key={i} className="text-sm leading-relaxed">{trimmed}</p>;
      })}
    </>
  );
}
