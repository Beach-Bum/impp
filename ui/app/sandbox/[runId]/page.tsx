import SandboxDetailScreen from '@/components/screens/SandboxDetailScreen';

export default function SandboxRunPage({ params }: { params: { runId: string } }) {
  return <SandboxDetailScreen runId={params.runId} />;
}
