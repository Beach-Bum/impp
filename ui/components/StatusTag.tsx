import { Badge } from '@/components/ui/badge';

type Status = 'Healthy' | 'Watch' | 'Warning' | 'Blocked' | 'Revoked' | 'Expired';

const map: Record<Status, 'default' | 'secondary' | 'destructive' | 'outline'> = {
  Healthy: 'default',
  Watch: 'secondary',
  Warning: 'outline',
  Blocked: 'destructive',
  Revoked: 'destructive',
  Expired: 'secondary',
};

export default function StatusTag({ status }: { status: Status }) {
  return <Badge variant={map[status] ?? 'secondary'}>{status}</Badge>;
}
