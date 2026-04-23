'use client';

import {
  Content,
  Header,
  HeaderGlobalAction,
  HeaderGlobalBar,
  HeaderMenuItem,
  HeaderName,
  HeaderNavigation,
  SkipToContent,
  Theme,
} from '@carbon/react';
import { Notification, UserAvatar } from '@carbon/react/icons';
import { usePathname } from 'next/navigation';
import { routes } from '@/lib/routes';
import type { ReactNode } from 'react';

export default function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  return (
    <Theme theme="g10">
      <SkipToContent />
      <Header aria-label="Agentic Memory Exchange">
        <HeaderName href="/market" prefix="AMM">
          Agentic Memory Exchange
        </HeaderName>

        <HeaderNavigation aria-label="Primary">
          {routes.map((route) => {
            const active = pathname.startsWith(route.href);
            return (
              <HeaderMenuItem
                key={route.href}
                href={route.href}
                className={active ? 'amm-header-item is-active' : 'amm-header-item'}>
                {route.label}
              </HeaderMenuItem>
            );
          })}
        </HeaderNavigation>

        <HeaderGlobalBar>
          <HeaderGlobalAction aria-label="Notifications" tooltipAlignment="end">
            <Notification size={20} />
          </HeaderGlobalAction>
          <HeaderGlobalAction aria-label="User account" tooltipAlignment="end">
            <UserAvatar size={20} />
          </HeaderGlobalAction>
        </HeaderGlobalBar>
      </Header>

      <Content id="main-content" className="amm-content">
        {children}
      </Content>
    </Theme>
  );
}
