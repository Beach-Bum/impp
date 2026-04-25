'use client';

import { type ReactNode, type ReactElement, Children, isValidElement } from 'react';
import { CodeBlock } from '@/components/ui/code-block';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

function extractText(node: ReactNode): string {
  if (typeof node === 'string') return node;
  if (typeof node === 'number') return String(node);
  if (!isValidElement(node)) return '';
  const children = (node.props as { children?: ReactNode }).children;
  if (!children) return '';
  return Children.toArray(children).map(extractText).join('');
}

function Pre({ children }: { children?: ReactNode }) {
  if (isValidElement(children)) {
    const props = children.props as { className?: string; children?: ReactNode };
    const langMatch = props.className?.match(/language-(\w+)/);
    const language = langMatch?.[1];
    const text = extractText(children);
    return <CodeBlock language={language}>{text}</CodeBlock>;
  }
  return <pre>{children}</pre>;
}

export const mdxComponents = {
  pre: Pre,
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
  Alert,
  AlertDescription,
  AlertTitle,
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  Badge,
};
