import { ImageResponse } from 'next/og';

export const size = {
  width: 64,
  height: 64,
};

export const contentType = 'image/png';

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'white',
        }}>
        <svg viewBox="0 0 309 330" width="52" height="56" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <mask id="mm-cut-icon" maskUnits="userSpaceOnUse" x="0" y="0" width="309" height="330">
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
          <path d="M0 184C18 134 39 94 72 51C102 12 133 0 170 0H309V330H0V184Z" fill="#0f172a" mask="url(#mm-cut-icon)" />
        </svg>
      </div>
    ),
    size,
  );
}
