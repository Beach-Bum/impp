'use client';

import { Heading, Button, Flash } from '@primer/react';

export default function IncidentScreen() {
  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Incidents</Heading>
      <p className="amm-screen-subtitle">Handle revocations, failed sandbox runs, and evidence export.</p>

      <Flash variant="danger" style={{ marginBottom: '16px' }}>
        <strong>Hostile replay sandbox failure</strong><br />
        A hostile replay test triggered an unsafe path. The artifact has been auto-detached pending review.
      </Flash>

      <div className="amm-grid amm-grid-2col">
        <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
          <Heading as="h2" style={{ fontSize: '14px', marginBottom: '16px' }}>Rollback sequence</Heading>
          {['1. Isolate agent — stop new mounts and freeze autonomous actions.',
            '2. Detach memory — detach the affected asset and preserve all state references.',
            '3. Replay sandbox — run a replay with the hostile conditions that triggered the failure.',
            '4. Export evidence — create the audit bundle for review and postmortem.',
          ].map((step) => (
            <div key={step} style={{ padding: '8px', marginBottom: '4px', backgroundColor: '#f6f8fa', borderRadius: '3px', fontSize: '12px' }}>
              {step}
            </div>
          ))}
          <div style={{ display: 'flex', gap: '8px', marginTop: '16px' }}>
            <Button variant="danger">Confirm rollback</Button>
            <Button>Open postmortem</Button>
          </div>
        </div>

        <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
          <Heading as="h2" style={{ fontSize: '14px', marginBottom: '16px' }}>Evidence export</Heading>
          <pre style={{ padding: '16px', backgroundColor: '#f6f8fa', borderRadius: '3px', fontSize: '11px' }}>
{`incident: hostile-replay-failure
asset: defi-incident-triage
action: auto-detached
review_state: pending`}
          </pre>
        </div>
      </div>
    </div>
  );
}
