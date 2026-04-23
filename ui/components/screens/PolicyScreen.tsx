'use client';

import { Button, Column, Dropdown, Grid, NumberInput, Tag, Tile, Toggle } from '@carbon/react';
import { policySnapshot } from '@/lib/mock-data';

const runtimes = ['Retrieval only / no tool autonomy', 'Retrieval + guarded tools', 'Full autonomy'];

export default function PolicyScreen() {
  return (
    <div className="amm-page">
      <Grid fullWidth>
        <Column lg={16} md={8} sm={4}>
          <h1 className="amm-screen-title">Policy center</h1>
          <p className="amm-screen-subtitle">Control budgets, risk gates, and allowed runtime scopes.</p>
        </Column>

        <Column lg={8} md={8} sm={4}>
          <Tile className="amm-card">
            <h2>Current policy snapshot</h2>
            <div className="amm-inline-tags">
              <Tag type="cool-gray">Auto-buy cap: {policySnapshot.autoBuyCap}</Tag>
              <Tag type="warm-gray">{policySnapshot.riskGate}</Tag>
              <Tag type="red">{policySnapshot.autoRevoke}</Tag>
            </div>
            <p style={{ marginTop: '1rem' }}>Runtime scope: {policySnapshot.runtimeScope}</p>
          </Tile>
        </Column>

        <Column lg={8} md={8} sm={4}>
          <Tile className="amm-card">
            <h2>Controls</h2>
            <div className="amm-surface-stack">
              <NumberInput id="cap" label="Auto-buy cap" min={0} value={2000} />
              <Dropdown id="runtime-scope" titleText="Allowed runtime scope" label="Choose a scope" items={runtimes} />
              <Toggle id="approval-toggle" labelText="Require human approval above Medium risk" defaultToggled />
              <Toggle id="revoke-toggle" labelText="Auto-revoke on negative transfer threshold breach" defaultToggled />
              <div className="amm-action-row">
                <Button>Save policy</Button>
                <Button kind="danger--tertiary">Reset changes</Button>
              </div>
            </div>
          </Tile>
        </Column>
      </Grid>
    </div>
  );
}
