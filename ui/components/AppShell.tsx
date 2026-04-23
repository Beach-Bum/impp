'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BaseStyles, ThemeProvider, Header } from '@primer/react';

const nav = [
  { href: '/market', label: 'Market' },
  { href: '/portfolio', label: 'Portfolio' },
  { href: '/policies', label: 'Policies' },
  { href: '/incidents', label: 'Incidents' },
];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <ThemeProvider>
      <BaseStyles>
        <Header>
          <Header.Item>
            <Header.Link as={Link} href="/market" style={{ fontSize: '14px', fontWeight: 'bold' }}>
              AMM
            </Header.Link>
          </Header.Item>
          <Header.Item>
            <span style={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.85rem' }}>
              Agentic Memory Exchange
            </span>
          </Header.Item>
          <Header.Item full />
          {nav.map((item) => (
            <Header.Item key={item.href}>
              <Header.Link
                as={Link}
                href={item.href}
                style={{
                  fontWeight: pathname === item.href ? 'bold' : 'normal',
                  borderBottom: pathname === item.href ? '2px solid white' : 'none',
                  paddingBottom: '2px',
                }}
              >
                {item.label}
              </Header.Link>
            </Header.Item>
          ))}
        </Header>
        <main>{children}</main>
      </BaseStyles>
    </ThemeProvider>
  );
}
