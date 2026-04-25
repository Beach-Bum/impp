'use client';

import { ReactNode } from 'react';

const PRIVY_APP_ID = process.env.NEXT_PUBLIC_PRIVY_APP_ID || '';

// Privy is loaded conditionally — when NEXT_PUBLIC_PRIVY_APP_ID is set,
// install @privy-io/react-auth and uncomment the PrivyProvider below.
// Until then, this wrapper is a passthrough so the app builds without Privy deps.

export default function PrivyWrapper({ children }: { children: ReactNode }) {
  if (!PRIVY_APP_ID) {
    return <>{children}</>;
  }

  // When Privy is installed:
  // import { PrivyProvider } from '@privy-io/react-auth';
  // return (
  //   <PrivyProvider
  //     appId={PRIVY_APP_ID}
  //     config={{
  //       loginMethods: ['email', 'google', 'wallet'],
  //       appearance: { theme: 'light', accentColor: '#0969da' },
  //     }}
  //   >
  //     {children}
  //   </PrivyProvider>
  // );

  return <>{children}</>;
}
