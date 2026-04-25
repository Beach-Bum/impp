'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from '@/components/ui/alert-dialog';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { CodeBlock } from '@/components/ui/code-block';
import { ChevronDown } from 'lucide-react';

const rollbackSteps = [
  {
    title: '1. Isolate agent',
    detail: 'Stop all new mounts and freeze autonomous actions. The agent will continue to serve existing requests but will not accept new memory attachments or execute agentic workflows until isolation is lifted.',
  },
  {
    title: '2. Detach memory',
    detail: 'Detach the affected asset and preserve all state references. The detached artifact is moved to quarantine storage where it can be re-examined without risk of re-attachment.',
  },
  {
    title: '3. Replay sandbox',
    detail: 'Run a replay with the hostile conditions that triggered the failure. The sandbox captures the full execution trace, including all memory reads, tool calls, and decision points that led to the unsafe path.',
  },
  {
    title: '4. Export evidence',
    detail: 'Create the audit bundle for review and postmortem. The bundle includes the full sandbox replay, the original artifact, the verification certificate, and a timeline of all actions taken.',
  },
];

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
            <Accordion defaultValue={[]} className="w-full">
              {rollbackSteps.map((step, i) => (
                <AccordionItem key={i} value={`step-${i}`}>
                  <AccordionTrigger className="text-sm">{step.title}</AccordionTrigger>
                  <AccordionContent>
                    <p className="text-sm leading-relaxed text-muted-foreground">{step.detail}</p>
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
            <div className="mt-4 flex gap-2">
              <AlertDialog>
                <AlertDialogTrigger render={<Button variant="destructive" />}>
                  Confirm rollback
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Confirm rollback</AlertDialogTitle>
                    <AlertDialogDescription>
                      Are you sure? This will detach the artifact and freeze autonomous actions. The agent will be isolated until you manually lift the freeze.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <AlertDialogAction>Confirm rollback</AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
              <Button variant="outline">Open postmortem</Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Evidence export</CardTitle></CardHeader>
          <CardContent>
            <Collapsible defaultOpen>
              <CollapsibleTrigger render={<Button variant="ghost" size="sm" className="mb-2" />}>
                Toggle evidence <ChevronDown className="ml-1 h-4 w-4" />
              </CollapsibleTrigger>
              <CollapsibleContent>
                <CodeBlock language="yaml">{`incident: hostile-replay-failure
asset: defi-incident-triage
action: auto-detached
review_state: pending`}</CodeBlock>
              </CollapsibleContent>
            </Collapsible>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
