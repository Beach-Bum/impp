'use client';

import { Button, Heading, Label, Select, TextInput } from '@primer/react';

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
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Sandbox</Heading>
      <p className="amm-screen-subtitle">
        Test memory artifacts against a scoped evaluation pack before you buy or attach.
      </p>

      <div className="amm-grid amm-grid-2col">
        <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Run evaluation</Heading>
          <div className="amm-card-stack">
            <TextInput placeholder="Artifact id or title" block />
            <Select block defaultValue="gpt-4o">
              <Select.Option value="gpt-4o">GPT-4o</Select.Option>
              <Select.Option value="claude-sonnet">Claude Sonnet</Select.Option>
              <Select.Option value="custom-agent">Custom agent</Select.Option>
            </Select>
            <Select block defaultValue="default-pack">
              <Select.Option value="default-pack">Default benchmark pack</Select.Option>
              <Select.Option value="adversarial-pack">Adversarial pack</Select.Option>
              <Select.Option value="org-pack">Organization pack</Select.Option>
            </Select>
            <div className="amm-action-row" style={{ flexWrap: 'wrap' }}>
              <Button>Run sandbox</Button>
              <Button variant="invisible">Save config</Button>
            </div>
          </div>
        </div>

        <div style={{ border: '1px solid var(--borderColor-default, #d8dee4)', borderRadius: '6px', padding: '16px' }}>
          <Heading as="h2" sx={{ fontSize: 2, mb: 2 }}>Example scorecard</Heading>
          <div className="amm-inline-tags" style={{ marginBottom: '12px' }}>
            <Label variant="success">Ready to attach</Label>
            <Label variant="accent">Scoped deployment</Label>
          </div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
            <tbody>
              {scorecard.map(([label, value]) => (
                <tr key={label} style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                  <td style={{ padding: '8px 0', fontWeight: 600 }}>{label}</td>
                  <td style={{ padding: '8px 0' }}>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
