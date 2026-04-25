# IMPP Import Pipeline & Staged Trust Spec

> Draft spec for bootstrapping the registry with real artifacts from open sources,
> using honest staged trust levels instead of pretending everything is verified.

## 1. Artifact Schema

Every artifact in the registry conforms to this normalized schema, regardless of source.

```json
{
  "id": "sha256-content-hash",
  "name": "org/artifact-name",
  "version": "1.0.0",
  "description": "Brief description of what this artifact teaches an agent",
  "domain": "defi|cybersec|engineering|research|legal|medical|general",
  "format": "jsonl|json|yaml|markdown|embeddings|mixed",
  "trust_state": "imported|parsed|evaluated|verified|curated",
  "source": {
    "type": "github|huggingface|academic|manual",
    "url": "https://github.com/org/repo",
    "license": "MIT|Apache-2.0|CC-BY-4.0|...",
    "author": "original author or org",
    "discovered_at": "2026-04-25T00:00:00Z",
    "commit_hash": "abc123...",
    "file_hashes": {
      "artifact.json": "sha256:...",
      "embeddings.npy": "sha256:..."
    }
  },
  "provenance": {
    "model_family": "gpt-4|claude|llama|unknown",
    "training_method": "expert-iteration|rl|distillation|manual|unknown",
    "training_rounds": null,
    "corpus_size": null,
    "created_at": null
  },
  "evaluation": {
    "trust_score": null,
    "transfer_efficiency": null,
    "adversarial_score": null,
    "negative_transfer_risk": null,
    "freshness_days": null,
    "evaluated_at": null,
    "evaluator_version": null
  },
  "certificate": {
    "signature": null,
    "public_key": null,
    "issued_at": null,
    "expires_at": null
  },
  "metadata": {
    "token_count": null,
    "file_count": 1,
    "size_bytes": 0,
    "tags": [],
    "dependencies": []
  }
}
```

Fields are nullable — they get filled as the artifact progresses through trust states.

## 2. Trust State Machine

```
  ┌──────────┐     ┌────────┐     ┌───────────┐     ┌──────────┐     ┌─────────┐
  │ Imported │ ──> │ Parsed │ ──> │ Evaluated │ ──> │ Verified │ ──> │ Curated │
  └──────────┘     └────────┘     └───────────┘     └──────────┘     └─────────┘
       │                │               │                 │
       └── rejected ────┴── rejected ───┴── rejected ─────┘
```

### States

| State | Entry Condition | What's Known | Badge Color |
|-------|----------------|--------------|-------------|
| **Imported** | Discovered by crawler | Source URL, license, format guess | Gray |
| **Parsed** | Schema validation passes | Full schema populated, content hash, dedup check | Blue |
| **Evaluated** | Sandbox pipeline completes | Trust score, transfer efficiency, adversarial score | Yellow |
| **Verified** | Score >= 60, Ed25519 signed | Certificate issued, provenance validated | Green |
| **Curated** | Manual review + score >= 80 | Human-reviewed, reference quality | Gold |

### Rejection

Artifacts can be rejected at any stage:
- **Imported → rejected**: Invalid license, binary blob, empty content, duplicate
- **Parsed → rejected**: Schema validation failure, unsupported format, corrupt data
- **Evaluated → rejected**: Trust score < 40, high adversarial risk, detected poisoning
- **Verified → rejected**: Certificate revoked, freshness decay below threshold

Rejected artifacts stay in the DB with `trust_state: "rejected"` and a `rejection_reason`.

### Transitions

```python
VALID_TRANSITIONS = {
    "imported": ["parsed", "rejected"],
    "parsed": ["evaluated", "rejected"],
    "evaluated": ["verified", "rejected"],
    "verified": ["curated", "rejected"],
    "curated": [],  # terminal state
    "rejected": ["imported"],  # can re-import after fixes
}
```

## 3. Source Adapters

Each source gets an adapter that implements the discovery and normalization interface.

### Interface

```python
class SourceAdapter(Protocol):
    name: str  # "github", "huggingface", "academic"

    async def discover(self, query: DiscoveryQuery) -> list[CandidateArtifact]:
        """Find candidate artifacts from this source."""
        ...

    async def fetch(self, candidate: CandidateArtifact) -> RawArtifact:
        """Download the raw artifact content."""
        ...

    async def normalize(self, raw: RawArtifact) -> ArtifactRecord:
        """Convert to registry schema. Sets trust_state='parsed'."""
        ...
```

### GitHub Adapter

Discovery targets:
- Repos with topics: `agent-memory`, `llm-memory`, `prompt-library`, `rag-knowledge`, `ai-benchmark`
- Repos matching patterns: `*-memory-*`, `*-knowledge-*`, `*-agent-config*`
- Files: `*.jsonl`, `*.json` in repos with AI/LLM topics
- README-described prompt collections, evaluation datasets, agent configs

Normalization:
- Extract license from repo metadata
- Map repo topics to IMPP domains
- Hash file contents for fingerprint
- Parse JSONL/JSON structure to determine format
- Extract author from repo owner

Rate limits: GitHub API (5000/hr authenticated), respect robots.txt.

### Hugging Face Adapter

Discovery targets:
- Datasets tagged: `agent`, `memory`, `knowledge`, `benchmark`, `evaluation`
- Models with structured knowledge exports
- Spaces that produce structured outputs

Normalization:
- License from dataset card
- Domain from tags
- Format detection (JSONL, Parquet → JSONL, JSON)
- Author from org/user

### Academic Adapter

Discovery targets:
- Papers with code repos (Papers With Code API)
- ArXiv papers in cs.AI, cs.CL, cs.MA with linked repos
- Repos from known research groups (FAIR, DeepMind, Anthropic, etc.)

Normalization:
- License from repo (default: check paper terms)
- Domain from paper categories
- Higher base trust weight for academic provenance
- Citation count as quality signal

## 4. Import Pipeline

### Pipeline Steps

```
discover → fetch → normalize → fingerprint → deduplicate → evaluate → sign → publish
```

### Implementation Plan

```
amm/
├── importer/
│   ├── __init__.py
│   ├── pipeline.py          # Main pipeline orchestrator
│   ├── discovery.py          # Discovery coordinator
│   ├── normalization.py      # Schema normalization
│   ├── fingerprint.py        # Content hashing + dedup
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── github.py         # GitHub source adapter
│   │   ├── huggingface.py    # HuggingFace source adapter
│   │   └── academic.py       # Academic repos adapter
│   └── queue.py              # Evaluation queue management
```

### Pipeline Orchestrator

```python
class ImportPipeline:
    def __init__(self, adapters: list[SourceAdapter], db: RegistryDB):
        self.adapters = adapters
        self.db = db

    async def run(self, query: DiscoveryQuery) -> ImportReport:
        report = ImportReport()

        for adapter in self.adapters:
            # 1. Discover
            candidates = await adapter.discover(query)
            report.discovered += len(candidates)

            for candidate in candidates:
                # 2. Fetch
                raw = await adapter.fetch(candidate)

                # 3. Normalize (Imported → Parsed)
                artifact = await adapter.normalize(raw)

                # 4. Fingerprint + Deduplicate
                artifact.id = content_hash(artifact)
                if self.db.exists(artifact.id):
                    report.duplicates += 1
                    continue

                # 5. Store as "parsed"
                artifact.trust_state = "parsed"
                self.db.insert(artifact)
                report.parsed += 1

                # 6. Queue for evaluation
                await self.queue.enqueue(artifact.id)
                report.queued += 1

        return report
```

### Evaluation Queue

Evaluation is async and potentially expensive (needs LLM calls for transfer scoring).

```python
class EvaluationQueue:
    async def process_next(self) -> EvalResult:
        artifact_id = await self.dequeue()
        artifact = self.db.get(artifact_id)

        # Run IMPP verification pipeline
        result = await self.verifier.evaluate(artifact)

        if result.trust_score >= 60:
            # Sign and promote to "verified"
            cert = self.signer.sign(artifact, result)
            artifact.trust_state = "verified"
            artifact.certificate = cert
        elif result.trust_score >= 40:
            # Keep as "evaluated" but not verified
            artifact.trust_state = "evaluated"
        else:
            artifact.trust_state = "rejected"
            artifact.rejection_reason = result.failure_reason

        artifact.evaluation = result.to_dict()
        self.db.update(artifact)
        return result
```

### CLI Integration

```bash
# Discover and import from GitHub
$ impp import --source github --query "agent memory" --domain defi --limit 50

# Import from HuggingFace
$ impp import --source huggingface --tags "agent,memory,benchmark"

# Process evaluation queue
$ impp evaluate --batch 10

# View import report
$ impp import --status
  Imported: 200
  Parsed: 183
  Evaluated: 47
  Verified: 18
  Curated: 6
  Rejected: 17
```

## 5. Public Badges & Scorecards

### Trust Badges (UI)

```
┌─────────────────────────────────────────────┐
│  ● Imported   (gray)    — Source discovered  │
│  ● Parsed     (blue)    — Schema valid       │
│  ● Evaluated  (yellow)  — Sandbox tested     │
│  ● Verified   (green)   — Ed25519 signed     │
│  ★ Curated    (gold)    — Reference quality  │
└─────────────────────────────────────────────┘
```

### Landing Page Counts

Replace the current "56 verified" with staged counts:

```
IMPP is the agent memory registry. It aggregates 247 artifacts:
18 verified · 47 evaluated · 183 parsed — from GitHub, Hugging Face, and academic sources.
```

### Leaderboard Integration

- Filter by trust state (dropdown: All / Verified+ / Evaluated+ / Parsed+)
- Sort by trust score within each state
- Badge color on each row
- Source icon (GitHub, HF, academic, manual)

### Package Detail (Asset Screen)

- Trust state badge prominently displayed
- Source provenance card: where it came from, license, original author
- Evaluation scorecard (if evaluated+)
- Certificate info (if verified+)
- Curation notes (if curated)

## 6. Database Changes

### New Supabase columns on `artifacts` table

```sql
ALTER TABLE artifacts ADD COLUMN trust_state TEXT DEFAULT 'imported'
  CHECK (trust_state IN ('imported', 'parsed', 'evaluated', 'verified', 'curated', 'rejected'));
ALTER TABLE artifacts ADD COLUMN source_type TEXT;
ALTER TABLE artifacts ADD COLUMN source_url TEXT;
ALTER TABLE artifacts ADD COLUMN source_license TEXT;
ALTER TABLE artifacts ADD COLUMN source_author TEXT;
ALTER TABLE artifacts ADD COLUMN discovered_at TIMESTAMPTZ;
ALTER TABLE artifacts ADD COLUMN rejection_reason TEXT;
ALTER TABLE artifacts ADD COLUMN content_hash TEXT UNIQUE;
ALTER TABLE artifacts ADD COLUMN file_hashes JSONB;
ALTER TABLE artifacts ADD COLUMN provenance JSONB;
```

### New `import_runs` table

```sql
CREATE TABLE import_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_type TEXT NOT NULL,
  query TEXT,
  discovered INTEGER DEFAULT 0,
  parsed INTEGER DEFAULT 0,
  duplicates INTEGER DEFAULT 0,
  queued INTEGER DEFAULT 0,
  started_at TIMESTAMPTZ DEFAULT now(),
  completed_at TIMESTAMPTZ,
  status TEXT DEFAULT 'running'
);
```

## 7. Priorities

### Phase 1: Schema + GitHub adapter
- Artifact schema finalized
- Trust state machine in DB
- GitHub adapter (discover + normalize + fingerprint)
- CLI: `impp import --source github`
- UI: trust state badges on leaderboard

### Phase 2: Evaluation pipeline
- Wire import pipeline to existing verification engine
- Evaluation queue with async processing
- CLI: `impp evaluate --batch N`
- UI: staged counts on landing page

### Phase 3: More sources + curation
- HuggingFace adapter
- Academic adapter
- Manual curation workflow
- UI: source provenance cards, curation notes

### Phase 4: Scale
- Scheduled crawls (cron)
- Dedup across sources (same artifact in GitHub + HF)
- Freshness re-evaluation
- Community submissions
