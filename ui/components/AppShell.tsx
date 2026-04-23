'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import { BaseStyles, ThemeProvider, Header, IconButton } from '@primer/react';
import { SunIcon, MoonIcon } from '@primer/octicons-react';

const nav = [
  { href: '/market', label: 'Market' },
  { href: '/portfolio', label: 'Portfolio' },
  { href: '/policies', label: 'Policies' },
  { href: '/incidents', label: 'Incidents' },
];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [colorMode, setColorMode] = useState<'day' | 'night'>('day');

  useEffect(() => {
    const saved = localStorage.getItem('amm-color-mode');
    if (saved === 'night') setColorMode('night');
  }, []);

  useEffect(() => {
    localStorage.setItem('amm-color-mode', colorMode);
    document.documentElement.setAttribute('data-color-mode', colorMode === 'night' ? 'dark' : 'light');
    document.documentElement.setAttribute('data-dark-theme', 'dark');
    document.documentElement.setAttribute('data-light-theme', 'light');
  }, [colorMode]);

  return (
    <ThemeProvider colorMode={colorMode}>
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
          <Header.Item>
            <IconButton
              icon={colorMode === 'day' ? MoonIcon : SunIcon}
              aria-label="Toggle color mode"
              variant="invisible"
              onClick={() => setColorMode(colorMode === 'day' ? 'night' : 'day')}
              style={{ color: 'white' }}
            />
          </Header.Item>
        </Header>
        <main style={{ backgroundColor: 'var(--bgColor-default, #fff)', minHeight: 'calc(100vh - 64px)' }}>
          {children}
        </main>
      </BaseStyles>
    </ThemeProvider>
  );
}
