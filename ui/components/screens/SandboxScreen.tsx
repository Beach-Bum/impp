'use client';

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table';

const scorecard = [
  ['Transfer lift', '+14.2%'],
  ['Negative transfer risk', 'Low'],
  ['Adversarial profile', 'Clean'],
  ['Freshness', '12 days'],
  ['Seller tier', 'Institutional'],
  ['Estimated monthly cost', '$420'],
  ['Recommended scope', 'Retrieval only'],
  ['Rollback rule', 'Auto-detach if negative transfer > 5%'],
];

export default function SandboxScreen() {
  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Sandbox</h1>
      <p className="mb-6 text-sm text-muted-foreground">
        Test memory artifacts against a scoped evaluation pack before you buy or attach.
      </p>

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
                {scorecard.map(([label, value]) => (
                  <TableRow key={label}>
                    <TableCell className="font-semibold">{label}</TableCell>
                    <TableCell>{value}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
