import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import './globals.scss';
import AppShell from '@/components/AppShell';

export const metadata: Metadata = {
  title: 'Agentic Memory Market',
  description: 'Carbon scaffold for a governed agentic memory market.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
