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
  const fill = inverse ? '#ffffff' : '#020202';

  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 307.93 329.85"
      width={size}
      height={size}
      style={{ display: 'block', flexShrink: 0, ...style }}
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M169.48,263.15l-116.03-.03-.03-78.29-53.42-.13,43.64-103.73C69.07,20.52,135.57-10.58,199.2,3.25c61.18,13.29,108.36,67.69,108.45,132.03l.28,194.54-138.42.02-.03-66.7ZM187.86,215.57l.11-53.94,46.94,27,18.2-31.64-46.78-27.23,46.78-27.08-18.1-31.65-46.99,26.9-.22-54.16-36.48.02-.13,54.26-47-27.02-18.29,31.6,46.96,27.2-46.95,27.17,18.25,31.65,47.02-27.05.12,54.24,36.54-.25Z"
        fill={fill}
      />
    </svg>
  );
}
