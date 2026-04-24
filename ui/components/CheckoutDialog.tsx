'use client';

import { useState } from 'react';
import { Button, Heading, Label, Flash } from '@primer/react';

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
      // Create order
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

      // Confirm order
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
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0,0,0,0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div
        style={{
          backgroundColor: 'var(--bgColor-default, #fff)',
          border: '1px solid var(--borderColor-default, #d0d7de)',
          borderRadius: '12px',
          padding: '24px',
          maxWidth: '480px',
          width: '90%',
        }}
      >
        {step === 'confirm' && (
          <>
            <Heading as="h2" style={{ fontSize: '18px', marginBottom: '16px' }}>
              Confirm purchase
            </Heading>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', marginBottom: '16px' }}>
              <tbody>
                <tr style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                  <td style={{ padding: '8px 0', fontWeight: 600 }}>Artifact</td>
                  <td style={{ padding: '8px 0' }}>{title}</td>
                </tr>
                <tr style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                  <td style={{ padding: '8px 0', fontWeight: 600 }}>Domain</td>
                  <td style={{ padding: '8px 0' }}>{domain}</td>
                </tr>
                <tr style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                  <td style={{ padding: '8px 0', fontWeight: 600 }}>Price</td>
                  <td style={{ padding: '8px 0' }}>
                    <Label variant="accent">${priceUsd.toFixed(2)}</Label>
                  </td>
                </tr>
                <tr>
                  <td style={{ padding: '8px 0', fontWeight: 600 }}>License</td>
                  <td style={{ padding: '8px 0' }}>Licensed (single-agent)</td>
                </tr>
              </tbody>
            </table>
            <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
              <Button variant="invisible" onClick={onClose}>Cancel</Button>
              <Button variant="primary" onClick={handlePurchase}>
                Pay ${priceUsd.toFixed(2)}
              </Button>
            </div>
          </>
        )}

        {step === 'processing' && (
          <div style={{ textAlign: 'center', padding: '24px 0' }}>
            <Heading as="h2" style={{ fontSize: '18px', marginBottom: '12px' }}>
              Processing...
            </Heading>
            <p className="amm-subtle">Creating order and confirming payment.</p>
          </div>
        )}

        {step === 'success' && (
          <>
            <Flash variant="success" style={{ marginBottom: '16px' }}>
              Purchase complete! Order {orderId?.slice(0, 8)}...
            </Flash>
            <p style={{ fontSize: '13px', marginBottom: '16px' }}>
              The artifact content is now available in your portfolio. You can attach it to your agent or download the memory pack.
            </p>
            <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
              <Button variant="invisible" onClick={onClose}>Close</Button>
              <Button onClick={() => { if (orderId) onSuccess(orderId); }}>
                View in portfolio
              </Button>
            </div>
          </>
        )}

        {step === 'error' && (
          <>
            <Flash variant="danger" style={{ marginBottom: '16px' }}>
              {errorMsg}
            </Flash>
            <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
              <Button variant="invisible" onClick={onClose}>Cancel</Button>
              <Button onClick={() => setStep('confirm')}>Try again</Button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
