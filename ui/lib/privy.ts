export const PRIVY_APP_ID = process.env.NEXT_PUBLIC_PRIVY_APP_ID || '';

export const privyConfig = {
  loginMethods: ['email', 'google', 'wallet'] as const,
  appearance: {
    theme: 'light' as const,
    accentColor: '#0969da',
  },
};
