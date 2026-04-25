import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { Geist, Geist_Mono } from 'next/font/google';
import { RootProvider } from 'fumadocs-ui/provider/next';
import { cn } from '@/lib/utils';
import './globals.css';
import AppShell from '@/components/AppShell';
import PrivyWrapper from '@/components/PrivyWrapper';

const geist = Geist({ subsets: ['latin'], variable: '--font-sans' });
const geistMono = Geist_Mono({ subsets: ['latin'], variable: '--font-mono' });

export const metadata: Metadata = {
  title: 'IMPP — The Agent Memory Registry',
  description: 'The package registry for verified AI agent memory artifacts.',
  icons: {
    icon: '/icon',
    apple: '/apple-icon',
  },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning className={cn(geist.variable, geistMono.variable)}>
      <body className="font-sans antialiased">
        <RootProvider>
          <PrivyWrapper>
            <AppShell>{children}</AppShell>
          </PrivyWrapper>
        </RootProvider>
      </body>
    </html>
  );
}
