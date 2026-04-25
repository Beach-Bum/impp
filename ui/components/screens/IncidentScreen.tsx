'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Separator } from '@/components/ui/separator';

export default function IncidentScreen() {
  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Incidents</h1>
      <p className="mb-6 text-sm text-muted-foreground">Handle revocations, failed sandbox runs, and evidence export.</p>

      <Alert variant="destructive" className="mb-4">
        <AlertTitle>Hostile replay sandbox failure</AlertTitle>
        <AlertDescription>A hostile replay test triggered an unsafe path. The artifact has been auto-detached pending review.</AlertDescription>
      </Alert>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Rollback sequence</CardTitle></CardHeader>
          <CardContent>
            {['1. Isolate agent — stop new mounts and freeze autonomous actions.',
              '2. Detach memory — detach the affected asset and preserve all state references.',
              '3. Replay sandbox — run a replay with the hostile conditions that triggered the failure.',
              '4. Export evidence — create the audit bundle for review and postmortem.',
            ].map((step) => (
              <div key={step} className="border-b py-2 text-sm leading-relaxed last:border-b-0">{step}</div>
            ))}
            <div className="mt-4 flex gap-2">
              <Button variant="destructive">Confirm rollback</Button>
              <Button variant="outline">Open postmortem</Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Evidence export</CardTitle></CardHeader>
          <CardContent>
            <pre className="whitespace-pre-wrap rounded-md bg-muted p-3 font-mono text-sm">{`incident: hostile-replay-failure
asset: defi-incident-triage
action: auto-detached
review_state: pending`}</pre>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
