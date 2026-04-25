import PackageDetailScreen from '@/components/screens/PackageDetailScreen';

export default async function PackagePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  return <PackageDetailScreen slug={slug} />;
}
