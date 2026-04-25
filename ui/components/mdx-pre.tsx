'use client';

import { type ReactNode, Children, isValidElement } from 'react';
import { CodeBlock } from '@/components/ui/code-block';

function extractText(node: ReactNode): string {
  if (typeof node === 'string') return node;
  if (typeof node === 'number') return String(node);
  if (!isValidElement(node)) return '';
  const children = (node.props as { children?: ReactNode }).children;
  if (!children) return '';
  return Children.toArray(children).map(extractText).join('');
}

export function MdxPre({ children }: { children?: ReactNode }) {
  if (isValidElement(children)) {
    const props = children.props as { className?: string; children?: ReactNode };
    const langMatch = props.className?.match(/language-(\w+)/);
    const language = langMatch?.[1];
    const text = extractText(children);
    return <CodeBlock language={language}>{text}</CodeBlock>;
  }
  return <pre>{children}</pre>;
}
