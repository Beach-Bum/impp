'use client';

import { Button, Column, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableHeader, TableRow, Tile } from '@carbon/react';
import StatusTag from '@/components/StatusTag';
import { getAgentById } from '@/lib/mock-data';

export default function AgentScreen({ id }: { id: string }) {
  const agent = getAgentById(id);

  return (
    <div className="amm-page">
      <Grid fullWidth>
        <Column lg={10} md={8} sm={4}>
          <h1 className="amm-screen-title">{agent.name}</h1>
          <p className="amm-screen-subtitle">Mounted memories, health, and rollback history.</p>
        </Column>
        <Column lg={6} md={8} sm={4}>
          <div className="amm-action-row" style={{ justifyContent: 'flex-end' }}>
            <Button kind="secondary">Replay sandbox</Button>
            <Button kind="danger">Detach memory</Button>
          </div>
        </Column>

        <Column lg={5} md={8} sm={4}>
          <Tile className="amm-card">
            <h2>Current status</h2>
            <StatusTag status={agent.status} />
            <p className="amm-subtle">Last evaluation: {agent.lastEval}</p>
            <p>Mounted memory: {agent.memory}</p>
          </Tile>
        </Column>

        <Column lg={11} md={8} sm={4}>
          <Tile className="amm-card">
            <TableContainer title="Rollback history">
              <Table size="md">
                <TableHead>
                  <TableRow>
                    <TableHeader>Event</TableHeader>
                    <TableHeader>When</TableHeader>
                    <TableHeader>Actor</TableHeader>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell>Mounted asset</TableCell>
                    <TableCell>3 days ago</TableCell>
                    <TableCell>Policy engine</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Replay sandbox passed</TableCell>
                    <TableCell>2 days ago</TableCell>
                    <TableCell>Security operator</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Drift watch refreshed</TableCell>
                    <TableCell>6 hours ago</TableCell>
                    <TableCell>Automated evaluator</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Tile>
        </Column>
      </Grid>
    </div>
  );
}
