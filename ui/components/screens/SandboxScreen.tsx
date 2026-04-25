'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from '@/components/ui/breadcrumb';
import { Info } from 'lucide-react';

const scorecard: [string, string, string][] = [
  ['Transfer lift', '+14.2%', 'How much better the agent performs with this artifact'],
  ['Negative transfer risk', 'Low', 'Probability the artifact degrades existing performance'],
  ['Adversarial profile', 'Clean', 'Results from 5 adversarial safety probes'],
  ['Freshness', '12 days', 'Age of the artifact since last verification'],
  ['Seller tier', 'Institutional', 'Seller classification based on verification history'],
  ['Estimated monthly cost', '$420', 'Projected cost based on metered usage patterns'],
  ['Recommended scope', 'Retrieval only', 'Suggested attachment scope for this artifact'],
  ['Rollback rule', 'Auto-detach if negative transfer > 5%', 'Automatic safety threshold'],
];

export default function SandboxScreen() {
  return (
    <TooltipProvider>
      <div className="mx-auto max-w-5xl px-5 py-8">
        <Breadcrumb className="mb-4">
          <BreadcrumbList>
            <BreadcrumbItem><BreadcrumbLink render={<Link href="/leaderboard" />}>Registry</BreadcrumbLink></BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbPage>Sandbox</BreadcrumbPage></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>

        <h1 className="mb-1 text-2xl font-light">Sandbox</h1>
        <p className="mb-4 text-sm text-muted-foreground">
          Test memory artifacts against a scoped evaluation pack before you buy or attach.
        </p>

        <Alert className="mb-6">
          <Info className="h-4 w-4" />
          <AlertDescription>
            Sandbox evaluations run in isolation. No artifacts are attached to production agents during testing.
          </AlertDescription>
        </Alert>

        <div className="grid gap-8 lg:grid-cols-2">
          <Card>
            <CardHeader><CardTitle className="text-xl font-light">Run evaluation</CardTitle></CardHeader>
            <CardContent className="flex flex-col gap-3">
              <Input placeholder="Artifact id or title" />
              <Select defaultValue="gpt-4o">
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="gpt-4o">GPT-4o</SelectItem>
                  <SelectItem value="claude-sonnet">Claude Sonnet</SelectItem>
                  <SelectItem value="custom-agent">Custom agent</SelectItem>
                </SelectContent>
              </Select>
              <Select defaultValue="default-pack">
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="default-pack">Default benchmark pack</SelectItem>
                  <SelectItem value="adversarial-pack">Adversarial pack</SelectItem>
                  <SelectItem value="org-pack">Organization pack</SelectItem>
                </SelectContent>
              </Select>
              <div className="flex flex-wrap gap-2">
                <Button>Run sandbox</Button>
                <Button variant="ghost">Save config</Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader><CardTitle className="text-xl font-light">Example scorecard</CardTitle></CardHeader>
            <CardContent>
              <div className="mb-3 flex flex-wrap gap-1">
                <Badge>Ready to attach</Badge>
                <Badge variant="secondary">Scoped deployment</Badge>
              </div>
              <Table>
                <TableBody>
                  {scorecard.map(([label, value, tooltip]) => (
                    <TableRow key={label}>
                      <TableCell className="font-semibold">
                        <Tooltip>
                          <TooltipTrigger className="cursor-help underline decoration-dotted">{label}</TooltipTrigger>
                          <TooltipContent className="max-w-xs">{tooltip}</TooltipContent>
                        </Tooltip>
                      </TableCell>
                      <TableCell>{value}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </div>
    </TooltipProvider>
  );
}
