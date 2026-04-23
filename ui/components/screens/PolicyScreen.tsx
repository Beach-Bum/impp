'use client';

import { Heading, Button, Label, TextInput, FormControl, Select } from '@primer/react';

export default function PolicyScreen() {
  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Policy center</Heading>
      <p className="amm-screen-subtitle">Control budgets, risk gates, and allowed runtime scopes.</p>

      <div className="amm-grid amm-grid-2col">
        <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
          <Heading as="h2" style={{ fontSize: '14px', marginBottom: '16px' }}>Current policy snapshot</Heading>
          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap', marginBottom: '8px' }}>
            <Label variant="secondary">Auto-buy cap: $2,000</Label>
            <Label variant="attention">Human approval above Medium</Label>
            <Label variant="danger">Auto-revoke: neg transfer &gt; 5%</Label>
          </div>
          <p style={{ marginTop: '8px' }}>Runtime scope: Retrieval only / no tool autonomy</p>
        </div>

        <div style={{ padding: '16px', border: '1px solid #d0d7de', borderRadius: '6px' }}>
          <Heading as="h2" style={{ fontSize: '14px', marginBottom: '16px' }}>Controls</Heading>
          <FormControl style={{ marginBottom: '16px' }}>
            <FormControl.Label>Auto-buy cap</FormControl.Label>
            <TextInput defaultValue="2000" type="number" />
          </FormControl>
          <FormControl style={{ marginBottom: '16px' }}>
            <FormControl.Label>Allowed runtime scope</FormControl.Label>
            <Select>
              <Select.Option value="retrieval">Retrieval only / no tool autonomy</Select.Option>
              <Select.Option value="guarded">Retrieval + guarded tools</Select.Option>
              <Select.Option value="full">Full autonomy</Select.Option>
            </Select>
          </FormControl>
          <div style={{ display: 'flex', gap: '8px', marginTop: '16px' }}>
            <Button variant="primary">Save policy</Button>
            <Button variant="danger">Reset changes</Button>
          </div>
        </div>
      </div>
    </div>
  );
}
