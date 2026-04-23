'use client';

import { Label } from '@primer/react';

type Status = 'Healthy' | 'Watch' | 'Warning' | 'Blocked' | 'Revoked' | 'Expired';

const map: Record<Status, 'success' | 'danger' | 'attention' | 'secondary' | 'accent'> = {
  Healthy: 'success',
  Watch: 'accent',
  Warning: 'attention',
  Blocked: 'danger',
  Revoked: 'danger',
  Expired: 'secondary',
};

export default function StatusTag({ status }: { status: Status }) {
  return <Label variant={map[status] ?? 'secondary'}>{status}</Label>;
}
