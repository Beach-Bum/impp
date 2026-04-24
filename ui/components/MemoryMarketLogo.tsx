import type { CSSProperties } from 'react';

let counter = 0;

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
  const id = `mm-mask-${++counter}`;

  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 320 340"
      width={size}
      height={size}
      style={{ display: 'block', flexShrink: 0, ...style }}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <mask id={id} maskUnits="userSpaceOnUse" x="0" y="0" width="320" height="340">
          <rect width="320" height="340" fill="white" />
          <rect x="0" y="190" width="56" height="150" fill="black" />
          <rect x="0" y="258" width="112" height="82" fill="black" />
          <g transform="translate(160 115)" fill="black">
            <rect x="-14" y="-62" width="28" height="124" rx="4" />
            <rect x="-14" y="-62" width="28" height="124" rx="4" transform="rotate(60)" />
            <rect x="-14" y="-62" width="28" height="124" rx="4" transform="rotate(120)" />
          </g>
        </mask>
      </defs>
      <path
        d="M5 190C22 138 44 96 78 54C108 14 140 2 176 2H314C317 2 318 3 318 6V332C318 335 317 336 314 336H6C3 336 2 335 2 332V194C2 193 3 191 5 190Z"
        fill={fill}
        mask={`url(#${id})`}
      />
    </svg>
  );
}
