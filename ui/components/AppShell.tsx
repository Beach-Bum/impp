'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { routes } from '@/lib/routes';
import MemoryMarketLogo from '@/components/MemoryMarketLogo';
import { ThemeTogglerButton } from '@/components/animate-ui/components/buttons/theme-toggler';
function GithubIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={className}>
      <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
    </svg>
  );
}

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

            <Button
              variant="ghost"
              size="sm"
              render={<a href="https://github.com/Beach-Bum/impp" target="_blank" rel="noopener noreferrer" />}
              aria-label="GitHub"
            >
              <GithubIcon className="h-4 w-4" />
            </Button>

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
