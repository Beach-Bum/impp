'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Spinner } from '@/components/ui/spinner';
import { fetchTransactions, type TransactionRecord } from '@/lib/api';
import { getSellerProfile } from '@/lib/directory';

function statusVariant(status: string): 'default' | 'outline' | 'secondary' {
  if (status === 'Released') return 'default';
  if (status === 'Held') return 'outline';
  return 'secondary';
}

export default function TransactionsScreen() {
  const [transactions, setTransactions] = useState<TransactionRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTransactions().then(setTransactions).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="mx-auto max-w-5xl px-5 py-8"><Spinner /></div>;

  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Transactions</h1>
      <p className="mb-6 text-sm text-muted-foreground">Settlement history for purchases, metered usage, escrow holds, and payout release.</p>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Transaction</TableHead>
                <TableHead>Seller</TableHead>
                <TableHead>Rail</TableHead>
                <TableHead>Amount</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Notes</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {transactions.map((txn) => {
                const seller = getSellerProfile(txn.sellerId);
                return (
                  <TableRow key={txn.id}>
                    <TableCell>
                      <strong>{txn.id}</strong>
                      <div className="text-xs text-muted-foreground">{txn.createdAt.replace('T', ' ').slice(0, 16)} UTC</div>
                    </TableCell>
                    <TableCell>
                      <Link href={`/sellers/${txn.sellerId}`} className="hover:underline">{seller?.name || txn.sellerId}</Link>
                    </TableCell>
                    <TableCell>{txn.rail}</TableCell>
                    <TableCell>${txn.amountUsd.toFixed(2)}</TableCell>
                    <TableCell><Badge variant={statusVariant(txn.status)}>{txn.status}</Badge></TableCell>
                    <TableCell>{txn.notes}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
