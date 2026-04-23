'use client';

import { Tag } from '@carbon/react';

export default function AIExplainabilityHint({ summary }: { summary: string }) {
  return (
    <div className="amm-ai-hint">
      <Tag type="purple">AI</Tag>
      <span className="amm-subtle">{summary}</span>
    </div>
  );
}
