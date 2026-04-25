import { Badge } from '@/components/ui/badge';

export default function AIExplainabilityHint({ summary }: { summary: string }) {
  return (
    <div className="inline-flex items-center gap-2">
      <Badge variant="secondary">AI</Badge>
      <span className="text-sm text-muted-foreground">{summary}</span>
    </div>
  );
}
