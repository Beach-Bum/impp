'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import StatusTag from '@/components/StatusTag';
import { getAgentById } from '@/lib/mock-data';

export default function AgentScreen({ id }: { id: string }) {
  const agent = getAgentById(id);

  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <div className="mb-6 flex items-start justify-between">
        <div>
          <h1 className="mb-1 text-2xl font-light">{agent.name}</h1>
          <p className="text-sm text-muted-foreground">Mounted memories, health, and rollback history.</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Replay sandbox</Button>
          <Button variant="destructive">Detach memory</Button>
        </div>
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Current status</CardTitle></CardHeader>
          <CardContent>
            <StatusTag status={agent.status} />
            <p className="mt-2 text-sm text-muted-foreground">Last evaluation: {agent.lastEval}</p>
            <p className="text-sm leading-relaxed">Mounted memory: {agent.memory}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Rollback history</CardTitle></CardHeader>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Event</TableHead>
                  <TableHead>When</TableHead>
                  <TableHead>Actor</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {[
                  ['Mounted asset', '3 days ago', 'Policy engine'],
                  ['Replay sandbox passed', '2 days ago', 'Security operator'],
                  ['Drift watch refreshed', '6 hours ago', 'Automated evaluator'],
                ].map(([event, when, actor]) => (
                  <TableRow key={event}>
                    <TableCell>{event}</TableCell>
                    <TableCell>{when}</TableCell>
                    <TableCell>{actor}</TableCell>
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
