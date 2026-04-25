'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { CodeBlock } from '@/components/ui/code-block';
import { CodeTabs } from '@/components/animate-ui/components/animate/code-tabs';

const pythonMethods = [
  ['client.verify(path)', 'Run adversarial probes, return trust score'],
  ['client.search(**kwargs)', 'Search registry by domain, trust, tags'],
  ['client.attach(path, agent)', 'Attach verified memory to agent'],
  ['client.publish(path)', 'Publish artifact to registry'],
  ['client.certificate(path)', 'Get Ed25519 signed certificate'],
];

const restEndpoints = [
  ['GET', '/artifacts', 'List all artifacts'],
  ['GET', '/artifacts/:id', 'Get artifact details'],
  ['POST', '/artifacts/verify', 'Verify an artifact'],
  ['POST', '/artifacts/publish', 'Publish to registry'],
  ['GET', '/artifacts/search', 'Search with filters'],
  ['GET', '/certificates/:id', 'Get verification certificate'],
];

export default function SDKScreen() {
  return (
    <div className="mx-auto max-w-5xl px-5 py-8">
      <h1 className="mb-1 text-2xl font-light">SDK / API Reference</h1>
      <p className="mb-8 text-sm text-muted-foreground">
        Integrate IMPP into your agent stack with the Python SDK or REST API.
      </p>

      <Tabs defaultValue="python">
        <TabsList>
          <TabsTrigger value="python">Python SDK</TabsTrigger>
          <TabsTrigger value="rest">REST API</TabsTrigger>
        </TabsList>

        <TabsContent value="python">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl font-light">Python SDK</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="mb-2 text-sm text-muted-foreground">Install</p>
                <CodeTabs
                  codes={{ pip: 'pip install impp', pipx: 'pipx install impp', uv: 'uv pip install impp' }}
                  lang="bash"
                />
              </div>

              <div>
                <p className="mb-2 text-sm text-muted-foreground">Quick start</p>
                <CodeBlock language="python">{`from impp import Client

client = Client()

# Verify an artifact
result = client.verify("defi-risk-memory.json")
print(result.trust_score)  # 87.3
print(result.certificate)  # Ed25519 signed cert

# Search the registry
artifacts = client.search(domain="defi", min_trust=70)

# Attach to your agent
client.attach("defi-risk-memory.json", agent="my-agent")`}</CodeBlock>
              </div>

              <div>
                <p className="mb-2 text-sm text-muted-foreground">API Reference</p>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Method</TableHead>
                      <TableHead>Description</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {pythonMethods.map(([method, desc]) => (
                      <TableRow key={method}>
                        <TableCell><code className="rounded bg-muted px-1.5 py-0.5 font-mono text-sm">{method}</code></TableCell>
                        <TableCell className="text-sm">{desc}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="rest">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl font-light">REST API</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="mb-2 text-sm text-muted-foreground">Base URL</p>
                <CodeBlock>https://api.impp.sh/v1</CodeBlock>
              </div>

              <div>
                <p className="mb-2 text-sm text-muted-foreground">Endpoints</p>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Method</TableHead>
                      <TableHead>Endpoint</TableHead>
                      <TableHead>Description</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {restEndpoints.map(([method, endpoint, desc]) => (
                      <TableRow key={endpoint}>
                        <TableCell><code className="rounded bg-muted px-1.5 py-0.5 font-mono text-sm">{method}</code></TableCell>
                        <TableCell><code className="rounded bg-muted px-1.5 py-0.5 font-mono text-sm">{endpoint}</code></TableCell>
                        <TableCell className="text-sm">{desc}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>

              <div>
                <p className="mb-2 text-sm text-muted-foreground">Example</p>
                <CodeBlock language="bash">{`curl https://api.impp.sh/v1/artifacts/search \\
  -H "Authorization: Bearer $IMPP_TOKEN" \\
  -d '{"domain": "defi", "min_trust": 70}'`}</CodeBlock>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <div className="mt-8 border-t pt-6">
        <h2 className="mb-2 text-xl font-light">Rate Limits</h2>
        <TooltipProvider>
          <Table className="max-w-md">
            <TableHeader>
              <TableRow>
                <TableHead>Tier</TableHead>
                <TableHead>
                  <Tooltip>
                    <TooltipTrigger className="cursor-help underline decoration-dotted">Verifications/day</TooltipTrigger>
                    <TooltipContent>Each impp verify call counts as one verification</TooltipContent>
                  </Tooltip>
                </TableHead>
                <TableHead>
                  <Tooltip>
                    <TooltipTrigger className="cursor-help underline decoration-dotted">Searches/day</TooltipTrigger>
                    <TooltipContent>Each impp search or /artifacts/search call counts as one search</TooltipContent>
                  </Tooltip>
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell>Free</TableCell>
                <TableCell>100</TableCell>
                <TableCell>1,000</TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="text-muted-foreground">Pro</TableCell>
                <TableCell className="text-muted-foreground">Unlimited</TableCell>
                <TableCell className="text-muted-foreground">Unlimited (coming soon)</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TooltipProvider>
      </div>
    </div>
  );
}
