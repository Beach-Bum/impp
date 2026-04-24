import type { CSSProperties } from 'react';

export default function MemoryMarketLogo({
  inverse = false,
  size = 28,
  style,
}: {
  inverse?: boolean;
  size?: number;
  style?: CSSProperties;
}) {
  const fg = inverse ? '#ffffff' : '#0f172a';

  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 32 32"
      width={size}
      height={size}
      fill="none"
      style={{ display: 'block', flexShrink: 0, ...style }}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Hexagon outline */}
      <path
        d="M16 2L28.5 9.5V24.5L16 32L3.5 24.5V9.5L16 2Z"
        stroke={fg}
        strokeWidth="2.5"
        strokeLinejoin="round"
      />
      {/* Memory node connections — asterisk pattern */}
      <line x1="16" y1="9" x2="16" y2="23" stroke={fg} strokeWidth="2" strokeLinecap="round" />
      <line x1="10" y1="12.5" x2="22" y2="19.5" stroke={fg} strokeWidth="2" strokeLinecap="round" />
      <line x1="22" y1="12.5" x2="10" y2="19.5" stroke={fg} strokeWidth="2" strokeLinecap="round" />
      {/* Center node */}
      <circle cx="16" cy="16" r="2.5" fill={fg} />
    </svg>
  );
}
