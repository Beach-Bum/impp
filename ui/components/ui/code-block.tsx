'use client';

import * as React from 'react';
import { useTheme } from 'next-themes';
import { cn } from '@/lib/utils';
import { CopyButton } from '@/components/animate-ui/components/buttons/copy';

interface CodeBlockProps {
  children: string;
  language?: string;
  className?: string;
}

export function CodeBlock({ children, language, className }: CodeBlockProps) {
  const { resolvedTheme } = useTheme();
  const [highlighted, setHighlighted] = React.useState('');

  React.useEffect(() => {
    if (!language) return;
    let cancelled = false;
    (async () => {
      try {
        const { codeToHtml } = await import('shiki');
        const html = await codeToHtml(children, {
          lang: language,
          themes: { light: 'github-light', dark: 'github-dark' },
          defaultColor: resolvedTheme === 'dark' ? 'dark' : 'light',
        });
        if (!cancelled) setHighlighted(html);
      } catch {
        // language not supported, fall through to plain text
      }
    })();
    return () => { cancelled = true; };
  }, [children, language, resolvedTheme]);

  return (
    <div className={cn('group relative overflow-hidden rounded-md border bg-muted/50', className)}>
      {language && (
        <div className="flex items-center justify-between border-b bg-muted px-3 py-1.5">
          <span className="text-xs text-muted-foreground">{language}</span>
          <CopyButton
            content={children}
            size="xs"
            variant="ghost"
            className="h-auto w-auto p-1 -mr-1 opacity-0 group-hover:opacity-100 transition-opacity"
          />
        </div>
      )}
      {!language && (
        <CopyButton
          content={children}
          size="xs"
          variant="ghost"
          className="absolute right-2 top-2 h-auto w-auto p-1 opacity-0 group-hover:opacity-100 transition-opacity"
        />
      )}
      {highlighted ? (
        <div
          className="overflow-x-auto p-3 text-sm leading-relaxed [&>pre,_&_code]:!bg-transparent [&>pre,_&_code]:[background:transparent_!important] [&>pre,_&_code]:border-none [&_code]:!text-[13px] [&_code_.line]:!px-0"
          dangerouslySetInnerHTML={{ __html: highlighted }}
        />
      ) : (
        <pre className="overflow-x-auto p-3 font-mono text-sm leading-relaxed">
          <code>{children}</code>
        </pre>
      )}
    </div>
  );
}
