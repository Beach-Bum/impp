'use client';

import { useState, useCallback } from 'react';
import { Check, Copy } from 'lucide-react';
import { cn } from '@/lib/utils';

interface CodeBlockProps {
  children: string;
  language?: string;
  className?: string;
}

export function CodeBlock({ children, language, className }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const copy = useCallback(() => {
    navigator.clipboard.writeText(children);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }, [children]);

  return (
    <div className={cn('group relative rounded-md border bg-muted/50', className)}>
      {language && (
        <div className="flex items-center justify-between border-b px-3 py-1.5">
          <span className="text-xs text-muted-foreground">{language}</span>
        </div>
      )}
      <pre className="overflow-x-auto p-3 font-mono text-sm leading-relaxed">
        <code>{children}</code>
      </pre>
      <button
        onClick={copy}
        className="absolute right-2 top-2 rounded-md border bg-background p-1.5 opacity-0 transition-opacity hover:bg-muted group-hover:opacity-100"
        aria-label="Copy code"
      >
        {copied ? (
          <Check className="h-3.5 w-3.5 text-green-500" />
        ) : (
          <Copy className="h-3.5 w-3.5 text-muted-foreground" />
        )}
      </button>
    </div>
  );
}
