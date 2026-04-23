'use client';

import { Accordion, AccordionItem, Button, CodeSnippet, Column, Grid, InlineNotification, Tile } from '@carbon/react';
import { alerts } from '@/lib/mock-data';

export default function IncidentScreen() {
  const critical = alerts[1];

  return (
    <div className="amm-page">
      <Grid fullWidth>
        <Column lg={16} md={8} sm={4}>
          <h1 className="amm-screen-title">Incidents</h1>
          <p className="amm-screen-subtitle">Handle revocations, failed sandbox runs, and evidence export.</p>
        </Column>

        <Column lg={16} md={8} sm={4}>
          <InlineNotification
            kind="error"
            title={critical.title}
            subtitle={critical.summary}
            lowContrast
            hideCloseButton
          />
        </Column>

        <Column lg={8} md={8} sm={4}>
          <Tile className="amm-card">
            <h2>Rollback sequence</h2>
            <Accordion align="start">
              <AccordionItem title="1. Isolate agent">Stop new mounts and freeze autonomous actions.</AccordionItem>
              <AccordionItem title="2. Detach memory">Detach the affected asset and preserve all state references.</AccordionItem>
              <AccordionItem title="3. Replay sandbox">Run a replay with the hostile conditions that triggered the failure.</AccordionItem>
              <AccordionItem title="4. Export evidence">Create the audit bundle for review and postmortem.</AccordionItem>
            </Accordion>
            <div className="amm-action-row" style={{ marginTop: '1rem' }}>
              <Button kind="danger">Confirm rollback</Button>
              <Button kind="secondary">Open postmortem</Button>
            </div>
          </Tile>
        </Column>

        <Column lg={8} md={8} sm={4}>
          <Tile className="amm-card">
            <h2>Evidence export</h2>
            <CodeSnippet type="multi">
{`incident: hostile-replay-failure
asset: defi-incident-triage
action: auto-detached
review_state: pending`}
            </CodeSnippet>
          </Tile>
        </Column>
      </Grid>
    </div>
  );
}
