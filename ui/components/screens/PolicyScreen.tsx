'use client';

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export default function PolicyScreen() {
  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">Policy center</h1>
      <p className="mb-6 text-sm text-muted-foreground">Control budgets, risk gates, and allowed runtime scopes.</p>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Current policy snapshot</CardTitle></CardHeader>
          <CardContent>
            <div className="mb-2 flex flex-wrap gap-1">
              <Badge variant="secondary">Auto-buy cap: $2,000</Badge>
              <Badge variant="outline">Human approval above Medium</Badge>
              <Badge variant="destructive">Auto-revoke: neg transfer &gt; 5%</Badge>
            </div>
            <p className="mt-2 text-sm leading-relaxed">Runtime scope: Retrieval only / no tool autonomy</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle className="text-xl font-light">Controls</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label>Auto-buy cap</Label>
              <Input defaultValue="2000" type="number" className="mt-1" />
            </div>
            <div>
              <Label>Allowed runtime scope</Label>
              <Select defaultValue="retrieval">
                <SelectTrigger className="mt-1"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="retrieval">Retrieval only / no tool autonomy</SelectItem>
                  <SelectItem value="guarded">Retrieval + guarded tools</SelectItem>
                  <SelectItem value="full">Full autonomy</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex gap-2 pt-2">
              <Button>Save policy</Button>
              <Button variant="destructive">Reset changes</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
