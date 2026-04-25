import SellerProfileScreen from '@/components/screens/SellerProfileScreen';

export default async function SellerProfilePage({
  params,
}: {
  params: Promise<{ sellerId: string }>;
}) {
  const { sellerId } = await params;
  return <SellerProfileScreen sellerId={sellerId} />;
}
