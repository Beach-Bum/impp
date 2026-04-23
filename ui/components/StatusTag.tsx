'use client';

import { Tag } from '@carbon/react';

type Status = 'Healthy' | 'Watch' | 'Warning' | 'Blocked' | 'Revoked' | 'Expired';

const map: Record<Status, string> = {
  Healthy: 'green',
  Watch: 'teal',
  Warning: 'yellow',
  Blocked: 'red',
  Revoked: 'magenta',
  Expired: 'cool-gray',
};

export default function StatusTag({ status }: { status: Status }) {
  return <Tag type={map[status] as any}>{status}</Tag>;
}
