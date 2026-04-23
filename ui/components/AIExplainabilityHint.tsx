'use client';

import { Label } from '@primer/react';

export default function AIExplainabilityHint({ summary }: { summary: string }) {
  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
      <Label variant="accent">AI</Label>
      <span style={{ color: 'var(--fgColor-muted, #656d76)', fontSize: '0.85rem' }}>{summary}</span>
    </div>
  );
}
