'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table';
import { Spinner } from '@/components/ui/spinner';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8100';

type CheckoutDialogProps = {
  listingId: string;
  title: string;
  priceUsd: number;
  domain: string;
  onClose: () => void;
  onSuccess: (orderId: string) => void;
};

export default function CheckoutDialog({
  listingId,
  title,
  priceUsd,
  domain,
  onClose,
  onSuccess,
}: CheckoutDialogProps) {
  const [step, setStep] = useState<'confirm' | 'processing' | 'success' | 'error'>('confirm');
  const [orderId, setOrderId] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState('');

  async function handlePurchase() {
    setStep('processing');
    try {
      const createRes = await fetch(`${API_BASE}/api/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ buyer_id: 'anonymous', listing_id: listingId }),
      });
      if (!createRes.ok) {
        const err = await createRes.json().catch(() => ({ detail: 'Failed to create order' }));
        throw new Error(err.detail || 'Failed to create order');
      }
      const order = await createRes.json();

      const confirmRes = await fetch(`${API_BASE}/api/orders/${order.id}/confirm`, {
        method: 'POST',
      });
      if (!confirmRes.ok) {
        const err = await confirmRes.json().catch(() => ({ detail: 'Failed to confirm order' }));
        throw new Error(err.detail || 'Failed to confirm order');
      }

      setOrderId(order.id);
      setStep('success');
    } catch (e: unknown) {
      setErrorMsg(e instanceof Error ? e.message : 'Purchase failed');
      setStep('error');
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="w-[90%] max-w-md rounded-lg border bg-background p-6">
        {step === 'confirm' && (
          <>
            <h2 className="mb-4 text-lg font-semibold">Confirm purchase</h2>
            <Table>
              <TableBody>
                <TableRow>
                  <TableCell className="font-semibold">Artifact</TableCell>
                  <TableCell>{title}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-semibold">Domain</TableCell>
                  <TableCell>{domain}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-semibold">Price</TableCell>
                  <TableCell><Badge>${priceUsd.toFixed(2)}</Badge></TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-semibold">License</TableCell>
                  <TableCell>Licensed (single-agent)</TableCell>
                </TableRow>
              </TableBody>
            </Table>
            <div className="mt-4 flex justify-end gap-2">
              <Button variant="ghost" onClick={onClose}>Cancel</Button>
              <Button onClick={handlePurchase}>Pay ${priceUsd.toFixed(2)}</Button>
            </div>
          </>
        )}

        {step === 'processing' && (
          <div className="py-6 text-center">
            <h2 className="mb-3 text-lg font-semibold">Processing...</h2>
            <Spinner />
            <p className="mt-3 text-sm text-muted-foreground">Creating order and confirming payment.</p>
          </div>
        )}

        {step === 'success' && (
          <>
            <Alert className="mb-4">
              <AlertDescription>Purchase complete! Order {orderId?.slice(0, 8)}...</AlertDescription>
            </Alert>
            <p className="mb-4 text-sm">
              The artifact content is now available in your portfolio. You can attach it to your agent or download the memory pack.
            </p>
            <div className="flex justify-end gap-2">
              <Button variant="ghost" onClick={onClose}>Close</Button>
              <Button onClick={() => { if (orderId) onSuccess(orderId); }}>View in portfolio</Button>
            </div>
          </>
        )}

        {step === 'error' && (
          <>
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>{errorMsg}</AlertDescription>
            </Alert>
            <div className="flex justify-end gap-2">
              <Button variant="ghost" onClick={onClose}>Cancel</Button>
              <Button onClick={() => setStep('confirm')}>Try again</Button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
