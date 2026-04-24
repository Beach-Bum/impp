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
  const fill = inverse ? '#ffffff' : '#0f172a';

  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 309 330"
      width={size}
      height={size}
      style={{ display: 'block', ...style }}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <mask id={`mm-cut-${inverse ? 'inv' : 'std'}`} maskUnits="userSpaceOnUse" x="0" y="0" width="309" height="330">
          <rect width="309" height="330" fill="white" />
          <rect x="0" y="184" width="53" height="146" fill="black" />
          <rect x="0" y="252" width="108" height="78" fill="black" />
          <g transform="translate(154 110)" fill="black">
            <rect x="-16" y="-66" width="32" height="132" />
            <rect x="-16" y="-66" width="32" height="132" transform="rotate(60)" />
            <rect x="-16" y="-66" width="32" height="132" transform="rotate(120)" />
          </g>
        </mask>
      </defs>
      <path
        d="M0 184C18 134 39 94 72 51C102 12 133 0 170 0H309V330H0V184Z"
        fill={fill}
        mask={`url(#mm-cut-${inverse ? 'inv' : 'std'})`}
      />
    </svg>
  );
}
