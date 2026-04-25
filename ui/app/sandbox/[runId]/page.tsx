import SandboxDetailScreen from '@/components/screens/SandboxDetailScreen';

export default async function SandboxRunPage({
  params,
}: {
  params: Promise<{ runId: string }>;
}) {
  const { runId } = await params;
  return <SandboxDetailScreen runId={runId} />;
}
