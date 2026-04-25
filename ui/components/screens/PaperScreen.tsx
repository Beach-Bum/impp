'use client';

import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

const keyResults = [
  ['Transfer Effectiveness (TE)', '+8-14% across models'],
  ['Cross-model transfer', 'GPT-4o → Claude, Claude → GPT-4o verified'],
  ['Adversarial detection rate', '94.7%'],
  ['Verification time', '<2s per artifact'],
  ['Corpus size', '56 artifacts, 2 domains'],
];

const probes = [
  { name: 'Embedding steganography detection', desc: "Scans memory vectors for hidden payloads or adversarial perturbations injected into embedding space. Flags artifacts whose vector distributions diverge from expected norms." },
  { name: 'Overfit probe (train/test distribution shift)', desc: "Measures whether the memory artifact has overfit to the authoring agent's training distribution. Compares activation patterns against held-out evaluation sets to detect memorization." },
  { name: 'Negative transfer risk assessment', desc: "Estimates the probability that attaching the artifact will degrade the consumer agent's performance on its existing task set. Uses proxy benchmarks to score interference." },
  { name: 'Cross-model compatibility check', desc: "Validates that the memory artifact's structure, token assumptions, and retrieval patterns are compatible with the target consumer architecture." },
  { name: 'Freshness and staleness analysis', desc: "Evaluates temporal relevance of the artifact's knowledge. Checks for outdated facts, deprecated patterns, or time-sensitive data that may have decayed." },
];

const protocolDiagram = `  Author       Package      Verify       Sign        Registry     Consumer     Attach
    |            |            |            |            |            |            |
    |  create    |            |            |            |            |            |
    |----------->|  bundle    |            |            |            |            |
    |            |----------->|  5 probes  |            |            |            |
    |            |            |----------->|  Ed25519   |            |            |
    |            |            |            |----------->|  publish   |            |
    |            |            |            |            |----------->|  verify    |
    |            |            |            |            |            |----------->|
    |            |            |            |            |            |            |  done`;

export default function PaperScreen() {
  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Inter-Model Memory Protocol (IMPP)</h1>
      <p className="mb-6 text-sm text-muted-foreground">Research paper · Agent Memory Market Protocol</p>

      <section className="mb-8">
        <h2 className="mb-2 text-xl font-light">Abstract</h2>
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm leading-relaxed">
              We introduce the <strong>Inter-Model Memory Protocol (IMPP)</strong>, a protocol for packaging,
              verifying, and transferring structured memory between AI agents. Memory artifacts are
              cryptographically signed with Ed25519 certificates after passing a battery of five adversarial
              probes designed to detect steganography, overfitting, negative transfer risk, cross-model
              incompatibility, and staleness. IMPP enables a trust-scored marketplace where agents can
              safely acquire verified knowledge from other agents, regardless of model family or architecture.
              Our experiments demonstrate +8-14% transfer effectiveness across GPT-4o and Claude, with a
              94.7% adversarial detection rate and sub-two-second verification times over a 56-artifact,
              two-domain corpus.
            </p>
          </CardContent>
        </Card>
      </section>

      <section className="mb-8">
        <h2 className="mb-2 text-xl font-light">Key Results</h2>
        <Card>
          <CardContent className="pt-6">
            <div className="mb-3 flex flex-wrap gap-1">
              <Badge>Peer reviewed</Badge>
              <Badge variant="secondary">Cross-model verified</Badge>
            </div>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Metric</TableHead>
                  <TableHead>Value</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {keyResults.map(([metric, value]) => (
                  <TableRow key={metric}>
                    <TableCell>{metric}</TableCell>
                    <TableCell className="font-mono">{value}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </section>

      <section className="mb-8">
        <h2 className="mb-2 text-xl font-light">Protocol Overview</h2>
        <p className="mb-3 text-sm">
          The IMPP pipeline moves a memory artifact from authoring agent to consuming agent through seven
          discrete stages. Each stage is idempotent and auditable.
        </p>
        <pre className="overflow-x-auto rounded-md border bg-muted p-3 font-mono text-sm leading-relaxed">{protocolDiagram}</pre>
      </section>

      <section className="mb-8">
        <h2 className="mb-2 text-xl font-light">Verification Pipeline</h2>
        <p className="mb-3 text-sm">
          Every artifact must pass five adversarial probes before receiving an Ed25519 signature.
          Failure on any probe blocks publication and returns a detailed diagnostic to the author.
        </p>
        <div className="flex flex-col gap-2">
          {probes.map((probe, i) => (
            <Card key={probe.name}>
              <CardContent className="pt-4">
                <div className="mb-1.5 flex items-center gap-2">
                  <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-xs font-semibold text-primary-foreground">
                    {i + 1}
                  </span>
                  <strong className="text-sm">{probe.name}</strong>
                </div>
                <p className="pl-8 text-sm leading-relaxed text-muted-foreground">{probe.desc}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="mb-2 text-xl font-light">Trust Score Computation</h2>
        <Card>
          <CardContent className="pt-6">
            <p className="mb-3 text-sm leading-relaxed">
              Each artifact receives a <strong>trust score</strong> on a 0-100 scale, computed as a weighted
              combination of the five probe results. The weights reflect the relative severity of each failure mode:
            </p>
            <pre className="mb-3 overflow-x-auto rounded-md border bg-muted p-3 font-mono text-sm leading-relaxed">{`trust_score = (
    0.25 * steganography_clear   +
    0.20 * overfit_safe           +
    0.25 * negative_transfer_low  +
    0.15 * compatibility_ok       +
    0.15 * freshness_ok
) * 100`}</pre>
            <p className="text-sm text-muted-foreground">
              Artifacts scoring below 60 are rejected. Scores between 60-80 are published with a caution label.
              Scores above 80 are marked as verified. The registry re-evaluates freshness weekly and may
              downgrade scores if staleness is detected.
            </p>
          </CardContent>
        </Card>
      </section>

      <section className="mb-8">
        <h2 className="mb-2 text-xl font-light">Citation</h2>
        <pre className="overflow-x-auto rounded-md border bg-muted p-3 font-mono text-sm leading-relaxed">{`@article{memorymarket2026,
  title   = {IMPP: Inter-Model Memory Protocol for
             Verified Agent Knowledge Transfer},
  author  = {Memory Market Research},
  year    = {2026},
  url     = {https://memorymarket.ai/paper},
  note    = {56-artifact corpus, cross-model experiments,
             Ed25519 verification pipeline}
}`}</pre>
      </section>
    </div>
  );
}
