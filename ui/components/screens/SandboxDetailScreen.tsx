'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from '@/components/ui/breadcrumb';
import { Progress, ProgressTrack } from '@/components/animate-ui/components/base/progress';
import { CodeBlock } from '@/components/ui/code-block';

type RunMetrics = {
  transfer_efficiency: number;
  adversarial_score: number;
  trust_score: number;
  training_accuracy: number;
  heldout_accuracy: number;
  negative_transfer_risk: string;
  freshness_days: number;
};

type EvalRun = {
  id: string;
  artifact: string;
  domain: string;
  model: string;
  date: string;
  status: string;
  metrics: RunMetrics;
  recommendation: string;
};

function getMockRun(runId: string): EvalRun {
  return {
    id: runId,
    artifact: 'DeFi Risk Calibration Pack v2.1',
    domain: 'DeFi:risk-assessment',
    model: 'GPT-4o',
    date: '2026-04-23',
    status: 'completed',
    metrics: {
      transfer_efficiency: 92.2,
      adversarial_score: 12.0,
      trust_score: 92.5,
      training_accuracy: 94.1,
      heldout_accuracy: 89.3,
      negative_transfer_risk: 'Low',
      freshness_days: 12,
    },
    recommendation: 'Ready to attach — scoped deployment recommended',
  };
}

const metricTooltips: Record<string, string> = {
  'Transfer efficiency': 'How effectively the artifact improves agent performance on the target task',
  'Adversarial score': 'Lower is better — measures resistance to adversarial probe battery',
  'Trust score': 'Composite 0-100 score from all verification probes',
  'Training accuracy': 'Performance on the artifact author\'s original training set',
  'Held-out accuracy': 'Performance on unseen evaluation data — the real test',
  'Negative transfer risk': 'Probability the artifact degrades existing agent capabilities',
  'Freshness': 'Days since last verification — artifacts are re-evaluated weekly',
};

const scorecard = (metrics: RunMetrics): [string, string][] => [
  ['Transfer efficiency', `${metrics.transfer_efficiency}%`],
  ['Adversarial score', `${metrics.adversarial_score}%`],
  ['Trust score', `${metrics.trust_score}/100`],
  ['Training accuracy', `${metrics.training_accuracy}%`],
  ['Held-out accuracy', `${metrics.heldout_accuracy}%`],
  ['Negative transfer risk', metrics.negative_transfer_risk],
  ['Freshness', `${metrics.freshness_days} days`],
];

export default function SandboxDetailScreen({ runId }: { runId: string }) {
  const run = getMockRun(runId);

  const statusVariant = run.status === 'completed' ? 'default' as const : run.status === 'failed' ? 'destructive' as const : 'secondary' as const;
  const accuracyGap = (run.metrics.training_accuracy - run.metrics.heldout_accuracy).toFixed(1);
  const gapVariant = parseFloat(accuracyGap) <= 5 ? 'default' as const : 'secondary' as const;

  return (
    <TooltipProvider>
      <div className="mx-auto max-w-5xl px-5 py-8">
        <Breadcrumb className="mb-4">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink render={<Link href="/leaderboard" />}>Registry</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbLink render={<Link href="/sandbox" />}>Sandbox</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbPage>Run {runId}</BreadcrumbPage></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>

        <h1 className="mb-1 text-2xl font-light">{run.artifact}</h1>
        <div className="mb-1">
          <span className="text-sm text-muted-foreground">Run ID: </span>
          <CodeBlock className="inline-block">{run.id}</CodeBlock>
        </div>
        <div className="mb-6 flex flex-wrap gap-1">
          <Badge variant="outline">{run.domain}</Badge>
          <Badge>{run.model}</Badge>
          <Badge variant={statusVariant}>{run.status}</Badge>
          <span className="self-center text-xs text-muted-foreground">{run.date}</span>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader><CardTitle className="text-xl font-light">Evaluation scorecard</CardTitle></CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableBody>
                  {scorecard(run.metrics).map(([label, value]) => (
                    <TableRow key={label}>
                      <TableCell className="font-semibold">
                        <Tooltip>
                          <TooltipTrigger className="cursor-help underline decoration-dotted">{label}</TooltipTrigger>
                          <TooltipContent className="max-w-xs">{metricTooltips[label]}</TooltipContent>
                        </Tooltip>
                      </TableCell>
                      <TableCell>{value}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          <div className="flex flex-col gap-4">
            <Card>
              <CardHeader><CardTitle className="text-xl font-light">Accuracy comparison</CardTitle></CardHeader>
              <CardContent>
                <div className="mb-3 space-y-3">
                  <div>
                    <div className="mb-1 flex items-center justify-between">
                      <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Training</span>
                      <span className="text-sm font-semibold">{run.metrics.training_accuracy}%</span>
                    </div>
                    <Progress value={run.metrics.training_accuracy}><ProgressTrack /></Progress>
                  </div>
                  <div>
                    <div className="mb-1 flex items-center justify-between">
                      <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Held-out</span>
                      <span className="text-sm font-semibold">{run.metrics.heldout_accuracy}%</span>
                    </div>
                    <Progress value={run.metrics.heldout_accuracy}><ProgressTrack /></Progress>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={gapVariant}>Gap: {accuracyGap}pp</Badge>
                  <span className="text-xs text-muted-foreground">
                    {parseFloat(accuracyGap) <= 5 ? 'Low generalization risk' : 'Monitor generalization'}
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card className="border-green-600/30 bg-green-50/50 dark:bg-green-950/20">
              <CardHeader><CardTitle className="text-xl font-light">Recommendation</CardTitle></CardHeader>
              <CardContent>
                <p className="mb-3 text-sm">{run.recommendation}</p>
                <div className="flex gap-2">
                  <Button size="sm">Attach artifact</Button>
                  <Button size="sm" variant="ghost">Export report</Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </TooltipProvider>
  );
}
