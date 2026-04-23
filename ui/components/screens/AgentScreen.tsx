'use client';

import { Heading, Button, Label } from '@primer/react';
import StatusTag from '@/components/StatusTag';
import { getAgentById } from '@/lib/mock-data';

export default function AgentScreen({ id }: { id: string }) {
  const agent = getAgentById(id);

  return (
    <div className="amm-page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
        <div>
          <Heading>{agent.name}</Heading>
          <p className="amm-screen-subtitle">Mounted memories, health, and rollback history.</p>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button>Replay sandbox</Button>
          <Button variant="danger">Detach memory</Button>
        </div>
      </div>

      <div className="amm-grid amm-grid-2col">
        <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
          <Heading as="h2" style={{ fontSize: '14px', marginBottom: '8px' }}>Current status</Heading>
          <StatusTag status={agent.status} />
          <p className="amm-subtle" style={{ marginTop: '8px' }}>Last evaluation: {agent.lastEval}</p>
          <p>Mounted memory: {agent.memory}</p>
        </div>

        <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', overflow: 'hidden' }}>
          <div style={{ padding: '16px', borderBottom: '1px solid #d0d7de' }}>
            <Heading as="h2" style={{ fontSize: '14px' }}>Rollback history</Heading>
          </div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--borderColor-default, #d0d7de)' }}>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Event</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>When</th>
                <th style={{ textAlign: 'left', padding: '8px 12px' }}>Actor</th>
              </tr>
            </thead>
            <tbody>
              {[
                ['Mounted asset', '3 days ago', 'Policy engine'],
                ['Replay sandbox passed', '2 days ago', 'Security operator'],
                ['Drift watch refreshed', '6 hours ago', 'Automated evaluator'],
              ].map(([event, when, actor]) => (
                <tr key={event} style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                  <td style={{ padding: '8px 12px' }}>{event}</td>
                  <td style={{ padding: '8px 12px' }}>{when}</td>
                  <td style={{ padding: '8px 12px' }}>{actor}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
