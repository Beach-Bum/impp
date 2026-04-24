'use client';

import Link from 'next/link';
import { Heading, Label } from '@primer/react';
import { TRANSACTIONS, getSellerProfile } from '@/lib/directory';

function statusVariant(status: string): 'success' | 'attention' | 'accent' {
  if (status === 'Released') return 'success';
  if (status === 'Held') return 'attention';
  return 'accent';
}

export default function TransactionsScreen() {
  return (
    <div className="amm-page">
      <Heading style={{ marginBottom: '4px' }}>Transactions</Heading>
      <p className="amm-screen-subtitle">Settlement history for purchases, metered usage, escrow holds, and payout release.</p>

      <div style={{ border: '1px solid #d0d7de', borderRadius: '6px', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--borderColor-default, #d0d7de)' }}>
              <th style={{ textAlign: 'left', padding: '8px 12px' }}>Transaction</th>
              <th style={{ textAlign: 'left', padding: '8px 12px' }}>Seller</th>
              <th style={{ textAlign: 'left', padding: '8px 12px' }}>Rail</th>
              <th style={{ textAlign: 'left', padding: '8px 12px' }}>Amount</th>
              <th style={{ textAlign: 'left', padding: '8px 12px' }}>Status</th>
              <th style={{ textAlign: 'left', padding: '8px 12px' }}>Notes</th>
            </tr>
          </thead>
          <tbody>
            {TRANSACTIONS.map((txn) => {
              const seller = getSellerProfile(txn.sellerId);
              return (
                <tr key={txn.id} style={{ borderBottom: '1px solid var(--borderColor-muted, #d8dee4)' }}>
                  <td style={{ padding: '8px 12px' }}><strong>{txn.id}</strong><div className="amm-subtle">{txn.createdAt.replace('T', ' ').slice(0, 16)} UTC</div></td>
                  <td style={{ padding: '8px 12px' }}>
                    <Link href={`/sellers/${txn.sellerId}`}>{seller?.name || txn.sellerId}</Link>
                  </td>
                  <td style={{ padding: '8px 12px' }}>{txn.rail}</td>
                  <td style={{ padding: '8px 12px' }}>${txn.amountUsd.toFixed(2)}</td>
                  <td style={{ padding: '8px 12px' }}><Label variant={statusVariant(txn.status)}>{txn.status}</Label></td>
                  <td style={{ padding: '8px 12px' }}>{txn.notes}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
