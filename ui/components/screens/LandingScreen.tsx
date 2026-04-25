'use client';

import Link from 'next/link';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Badge } from '@/components/ui/badge';
import { Kbd } from '@/components/ui/kbd';
import { CodeBlock } from '@/components/ui/code-block';
import { CountingNumber } from '@/components/animate-ui/primitives/texts/counting-number';
import {
  PreviewCard,
  PreviewCardTrigger,
  PreviewCardPanel,
} from '@/components/animate-ui/components/base/preview-card';

const devBlogs = [
  { title: 'Cross-Model Transfer Upgrade', date: '2026-04-09' },
  { title: 'Adversarial Safety v2.0', date: '2026-04-01' },
  { title: 'Ed25519 Certificate System', date: '2026-03-28' },
  { title: 'CLI Reference v1.4', date: '2026-03-15' },
];

const securityAdvisories = [
  { title: 'Steganography detection fix', date: '2026-04-09' },
  { title: 'Overfit probe threshold update', date: '2026-04-01' },
  { title: 'Certificate expiry policy change', date: '2026-03-28' },
];

const newPackages = [
  { name: 'impp/defi-risk-assessment', slug: 'impp-defi-risk-assessment', version: 'v2.1', age: '2h ago', domain: 'DeFi', trust: 94.2 },
  { name: 'impp/cybersec-threat-intel', slug: 'impp-cybersec-threat-intel', version: 'v1.4', age: '1d ago', domain: 'CyberSec', trust: 91.8 },
  { name: 'impp/code-review-patterns', slug: 'impp-code-review-patterns', version: 'v0.9', age: '2d ago', domain: 'Engineering', trust: 87.3 },
  { name: 'impp/medical-literature', slug: 'impp-medical-literature', version: 'v1.0', age: '4d ago', domain: 'Research', trust: 85.1 },
];

const freshDocs = [
  { title: 'Verification Protocol', note: 'exploring v2' },
  { title: 'CLI Reference', note: 'v1.4' },
  { title: 'Publishing Guide', note: 'updated' },
  { title: 'Trust Score Computation', note: 'exploring v2' },
];

export default function LandingScreen() {
  return (
    <>
      {/* Search bar */}
      <div className="border-b bg-muted/40 py-3">
        <div className="mx-auto flex max-w-5xl items-center gap-2 px-5">
          <div className="relative flex-1">
            <Input
              placeholder="Search packages..."
              className="text-lg pr-16"
            />
            <div className="absolute right-2 top-1/2 -translate-y-1/2">
              <Kbd>⌘K</Kbd>
            </div>
          </div>
          <Button render={<Link href="/leaderboard" />}>
            Search
          </Button>
        </div>
      </div>

      {/* Tagline */}
      <div className="border-b bg-background py-2.5">
        <div className="mx-auto max-w-5xl px-5 text-sm text-muted-foreground">
          <strong className="text-foreground">IMPP</strong> is the agent memory registry. It aggregates and publishes{' '}
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger>
                <strong className="cursor-help text-foreground underline decoration-dotted">
                  <CountingNumber number={56} inView className="tabular-nums" />
                </strong>
              </TooltipTrigger>
              <TooltipContent>28 DeFi + 28 CyberSec artifacts across verified, evaluated, and parsed trust states</TooltipContent>
            </Tooltip>
          </TooltipProvider>
          {' '}AI agent memory packages installable with <code className="rounded bg-muted px-1.5 py-0.5 text-xs">impp</code>.
        </div>
      </div>

      <div className="mx-auto max-w-5xl px-5 py-7">
        {/* Two-column: Getting Started + Publishing */}
        <div className="grid gap-10 lg:grid-cols-2">
          <div>
            <h2 className="mb-4 text-2xl font-light">Getting Started</h2>

            <h3 className="mb-1 mt-4 text-sm font-semibold">Define Your Dependencies</h3>
            <p className="mb-2 text-sm text-muted-foreground">
              The <code className="rounded bg-muted px-1 py-0.5 text-xs">impp</code> CLI is at the root of your project, referencing your artifact dependencies. Add it to your agent&apos;s configuration.
            </p>
            <CodeBlock language="json">{`{
  "require": {
    "impp/defi-risk-assessment": "^2.1",
    "impp/cybersec-threat-intel": "^1.4"
  }
}`}</CodeBlock>

            <h3 className="mb-1 mt-4 text-sm font-semibold">Install IMPP In Your Project</h3>
            <p className="mb-2 text-sm text-muted-foreground">Run this in your terminal to get the latest IMPP CLI.</p>
            <CodeBlock language="bash">pip install impp</CodeBlock>

            <h3 className="mb-1 mt-4 text-sm font-semibold">Install Dependencies</h3>
            <p className="mb-2 text-sm text-muted-foreground">Download the artifacts in your <code className="rounded bg-muted px-1 py-0.5 text-xs">impp.json</code>.</p>
            <CodeBlock language="bash">impp install</CodeBlock>

            <h3 className="mb-1 mt-4 text-sm font-semibold">Autoload Dependencies</h3>
            <p className="mb-2 text-sm text-muted-foreground">
              For best runtime integration, let IMPP handle artifact loading. All artifacts are accessible as <code className="rounded bg-muted px-1 py-0.5 text-xs">impp.artifacts.*</code>.
            </p>
            <CodeBlock language="python">{`import impp
artifacts = impp.autoload()`}</CodeBlock>

            <p className="mt-4 text-sm text-muted-foreground">
              For additional info, <Link href="/docs" className="underline hover:text-foreground">see the IMPP docs</Link> on the basics of installing and using artifacts.
            </p>
          </div>

          <div>
            <h2 className="mb-4 text-2xl font-light">Publishing Packages</h2>

            <h3 className="mb-1 mt-4 text-sm font-semibold">Define Your Package</h3>
            <p className="mb-2 text-sm text-muted-foreground">
              Put a file named <code className="rounded bg-muted px-1 py-0.5 text-xs">impp.json</code> at the root of your package&apos;s repository, containing:
            </p>
            <CodeBlock language="json">{`{
  "name": "your-org/your-artifact",
  "description": "A brief description",
  "version": "1.0.0",
  "domain": "defi",
  "require": {}
}`}</CodeBlock>

            <h3 className="mb-1 mt-4 text-sm font-semibold">Validate The File</h3>
            <p className="mb-2 text-sm text-muted-foreground">
              Run <code className="rounded bg-muted px-1 py-0.5 text-xs">impp verify</code> to check that your file is valid for submission.
            </p>
            <CodeBlock language="bash">impp verify --local my-artifact.json</CodeBlock>

            <h3 className="mb-1 mt-4 text-sm font-semibold">Submit The File</h3>
            <p className="mb-2 text-sm text-muted-foreground">
              Use <code className="rounded bg-muted px-1 py-0.5 text-xs">impp publish</code> to submit your package to the registry.
            </p>
            <CodeBlock language="bash">impp publish my-artifact.json</CodeBlock>

            <h3 className="mb-1 mt-4 text-sm font-semibold">Manage Private Packages</h3>
            <p className="mb-2 text-sm text-muted-foreground">
              If you want to host private packages, you can create a Private Package with IMPP. You can publish from a CI/CD pipeline, manage team access, and integrate with any agent framework.
            </p>
            <p className="text-sm text-muted-foreground">
              Every published artifact goes through adversarial safety probes and receives a signed Ed25519 certificate that anyone can verify offline via <code className="rounded bg-muted px-1 py-0.5 text-xs">impp verify</code>.
            </p>
          </div>
        </div>

        {/* Announcements */}
        <Separator className="my-6" />

        <div className="space-y-6">
          <div>
            <div className="mb-1 flex items-center gap-2">
              <span className="flex h-7 w-7 items-center justify-center rounded-full bg-amber-500 text-xs font-bold text-white">!</span>
              <Link href="/paper" className="text-lg font-light hover:underline">The IMPP Protocol Upgrade</Link>
              <span className="text-xs text-muted-foreground">Apr 1, 2026</span>
            </div>
            <p className="text-sm leading-relaxed text-muted-foreground">
              A detailed blog post describing everything about the upcoming v2 update to the Verification Protocol is available in <Link href="/paper" className="underline">our research paper</Link>. From multi-model cross-validation to adversarial safety probes, here&apos;s what&apos;s changing.
            </p>
          </div>

          <div>
            <div className="mb-1 flex items-center gap-2">
              <span className="flex h-7 w-7 items-center justify-center rounded-full bg-sky-500 text-xs font-bold text-white">i</span>
              <Link href="/paper" className="text-lg font-light hover:underline">IMPP OKRs and Goals</Link>
              <span className="text-xs text-muted-foreground">Apr 1, 2026</span>
            </div>
            <div className="text-sm leading-relaxed text-muted-foreground">
              <p className="mb-2">A detailed look at where the IMPP project is headed. We are building something fundamentally new: a trust layer for agent knowledge transfer.</p>
              <p className="mb-2"><strong className="text-foreground">1. Trust &amp; Safety.</strong> Every artifact that reaches the registry runs through adversarial probes, checking for prompt injection, data poisoning, stego-encoded payloads, and distribution shift. We publish these results as signed Ed25519 verification certificates.</p>
              <p><strong className="text-foreground">2. Open Research.</strong> We believe verifiable AI memory is a public good. Our <Link href="/paper" className="underline">research paper</Link> describes the protocol in full, including cross-model transfer experiments with 56 artifacts across GPT-4o and Claude Sonnet.</p>
            </div>
          </div>
        </div>

        {/* Four-column bottom sections */}
        <Separator className="my-6" />

        <div className="grid gap-8 sm:grid-cols-2">
          <div>
            <h3 className="mb-1 text-lg font-light">Developer blogs <span className="text-xs text-muted-foreground">read the developer updates</span></h3>
            <Table>
              <TableBody>
                {devBlogs.map((item) => (
                  <TableRow key={item.title}>
                    <TableCell><Link href="/docs" className="hover:underline">{item.title}</Link></TableCell>
                    <TableCell className="text-right text-xs text-muted-foreground">{item.date}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          <div>
            <h3 className="mb-1 text-lg font-light">Security advisories <span className="text-xs text-muted-foreground">view the security advisories</span></h3>
            <Table>
              <TableBody>
                {securityAdvisories.map((item) => (
                  <TableRow key={item.title}>
                    <TableCell><Link href="/docs" className="hover:underline">{item.title}</Link></TableCell>
                    <TableCell className="text-right text-xs text-muted-foreground">{item.date}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          <div>
            <h3 className="mb-1 text-lg font-light">New packages <span className="text-xs text-muted-foreground">recently published</span></h3>
            <TooltipProvider>
              <Table>
                <TableBody>
                  {newPackages.map((item) => (
                    <TableRow key={item.name}>
                      <TableCell>
                        <PreviewCard>
                          <PreviewCardTrigger
                            render={<Link href={`/package/${item.slug}`} />}
                            className="hover:underline"
                          >
                            {item.name}
                          </PreviewCardTrigger>
                          <PreviewCardPanel className="w-72">
                            <div className="space-y-1.5">
                              <p className="text-sm font-semibold">{item.name}</p>
                              <div className="flex items-center gap-2">
                                <Badge variant="outline" className="text-[10px]">{item.version}</Badge>
                                <Badge variant="secondary" className="text-[10px]">{item.domain}</Badge>
                              </div>
                              <div className="flex items-center justify-between text-xs text-muted-foreground">
                                <span>Trust: <strong className="text-foreground">{item.trust}</strong>/100</span>
                                <span>{item.age}</span>
                              </div>
                              <p className="text-xs text-muted-foreground">Click to view full package details</p>
                            </div>
                          </PreviewCardPanel>
                        </PreviewCard>
                      </TableCell>
                      <TableCell className="text-xs">{item.version}</TableCell>
                      <TableCell className="text-right text-xs text-muted-foreground">{item.age}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TooltipProvider>
          </div>

          <div>
            <h3 className="mb-1 text-lg font-light">Fresh documentation <span className="text-xs text-muted-foreground">see all recent docs</span></h3>
            <Table>
              <TableBody>
                {freshDocs.map((item) => (
                  <TableRow key={item.title}>
                    <TableCell><Link href="/docs" className="hover:underline">{item.title}</Link></TableCell>
                    <TableCell className="text-right text-xs text-muted-foreground">{item.note}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
      </div>
    </>
  );
}
