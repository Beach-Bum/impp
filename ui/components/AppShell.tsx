'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import { BaseStyles, ThemeProvider, IconButton } from '@primer/react';
import { SunIcon, MoonIcon } from '@primer/octicons-react';
import { routes } from '@/lib/routes';
import MemoryMarketLogo from '@/components/MemoryMarketLogo';

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

  const isDark = colorMode === 'night';
  const activeIndicatorColor = isDark ? '#f0f6fc' : '#1f2328';

  if (pathname === '/') {
    return (
      <ThemeProvider colorMode={colorMode}>
        <BaseStyles>
          {children}
        </BaseStyles>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider colorMode={colorMode}>
      <BaseStyles>
        <nav style={{
          backgroundColor: isDark ? '#161b22' : '#ffffff',
          color: isDark ? '#f0f6fc' : '#1f2328',
          borderBottom: `1px solid ${isDark ? '#30363d' : '#d0d7de'}`,
          display: 'flex',
          alignItems: 'center',
          padding: '0 16px',
          height: '64px',
          gap: '16px',
        }}>
          <Link href="/market" style={{ fontSize: '14px', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '10px', color: 'inherit', textDecoration: 'none' }}>
            <MemoryMarketLogo inverse={isDark} size={28} />
            <span>AMM</span>
          </Link>
          <span style={{ opacity: 0.6, fontSize: '0.85rem' }}>
            Agentic Memory Exchange
          </span>
          <div style={{ flex: 1 }} />
          {routes.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              style={{
                color: 'inherit',
                textDecoration: 'none',
                fontSize: '14px',
                fontWeight: pathname === item.href ? 'bold' : 'normal',
                borderBottom: pathname === item.href ? `2px solid ${activeIndicatorColor}` : 'none',
                paddingBottom: '2px',
              }}
            >
              {item.label}
            </Link>
          ))}
          <IconButton
            icon={colorMode === 'day' ? MoonIcon : SunIcon}
            aria-label="Toggle color mode"
            variant="invisible"
            onClick={() => setColorMode(colorMode === 'day' ? 'night' : 'day')}
            style={{ color: isDark ? '#f0f6fc' : '#1f2328' }}
          />
        </nav>
        <main style={{ minHeight: 'calc(100vh - 64px)' }}>
          {children}
        </main>
      </BaseStyles>
    </ThemeProvider>
  );
}
