import AuditScreen from '@/components/screens/AuditScreen';

export default async function AuditPage({
  params,
}: {
  params: Promise<{ artifactId: string }>;
}) {
  const { artifactId } = await params;
  return <AuditScreen artifactId={artifactId} />;
}
