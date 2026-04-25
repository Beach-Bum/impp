import AgentScreen from '@/components/screens/AgentScreen';

export default async function AgentPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <AgentScreen id={id} />;
}
