import AssetScreen from '@/components/screens/AssetScreen';

export default async function AssetPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return <AssetScreen slug={slug} />;
}
