'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { routes } from '@/lib/routes';
import MemoryMarketLogo from '@/components/MemoryMarketLogo';
import { ThemeTogglerButton } from '@/components/animate-ui/components/buttons/theme-toggler';

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <>
      <header className="border-b bg-background">
        <div className="mx-auto flex h-14 max-w-5xl items-center gap-6 px-5">
          <Link href="/" className="flex items-center gap-2.5 font-bold tracking-tight">
            <MemoryMarketLogo size={22} />
            <span>IMPP</span>
          </Link>

          <span className="hidden text-xs text-muted-foreground sm:inline">
            The Agent Memory Registry
          </span>

          <div className="flex-1" />

          <nav className="flex items-center gap-1">
            {routes.map((item) => {
              const active = pathname === item.href;
              return (
                <Button
                  key={item.href}
                  variant={active ? 'secondary' : 'ghost'}
                  size="sm"
                  render={<Link href={item.href} />}
                >
                  {item.label}
                </Button>
              );
            })}

            <Button variant="ghost" size="sm" render={<Link href="/signup" />}>
              Sign in
            </Button>

            <ThemeTogglerButton
              variant="ghost"
              size="sm"
              modes={['light', 'dark']}
              aria-label="Toggle color mode"
            />
          </nav>
        </div>
      </header>

      <main className="min-h-[calc(100vh-3.5rem-12rem)]">
        {children}
      </main>

      <footer className="border-t bg-muted/40">
        <div className="mx-auto grid max-w-5xl grid-cols-2 gap-8 px-5 py-10 text-sm sm:grid-cols-4">
          <div>
            <h4 className="mb-3 font-semibold">Registry</h4>
            <FooterLink href="/leaderboard">Browse Artifacts</FooterLink>
            <FooterLink href="/sandbox">Sandbox</FooterLink>
            <FooterLink href="/paper">Research Paper</FooterLink>
          </div>
          <div>
            <h4 className="mb-3 font-semibold">Develop</h4>
            <FooterLink href="/docs">Documentation</FooterLink>
            <FooterLink href="/sdk">SDK Reference</FooterLink>
            <FooterLink href="/docs">CLI Reference</FooterLink>
          </div>
          <div>
            <h4 className="mb-3 font-semibold">Protocol</h4>
            <FooterLink href="/paper">IMPP Spec</FooterLink>
            <FooterLink href="/paper">Verification Pipeline</FooterLink>
            <FooterLink href="/paper">Trust Scoring</FooterLink>
          </div>
          <div>
            <h4 className="mb-3 font-semibold">About</h4>
            <FooterLink href="https://github.com/Beach-Bum/impp">GitHub</FooterLink>
            <FooterLink href="/paper">Citation</FooterLink>
            <FooterLink href="/waitlist">Waitlist</FooterLink>
          </div>
        </div>
        <Separator />
        <div className="py-4 text-center text-xs text-muted-foreground">
          IMPP — The Interoperable Memory Publishing Protocol
        </div>
      </footer>
    </>
  );
}

function FooterLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <div className="mb-1.5">
      <Link href={href} className="text-muted-foreground hover:text-foreground transition-colors">
        {children}
      </Link>
    </div>
  );
}
