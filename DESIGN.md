# Design Specification — Verification Protocol

## Context

The Agent Memory Markets working paper proposes a protocol for extracting, verifying, and trading learned agent behavior as economic assets. A proof-of-concept experiment demonstrated 92% transfer efficiency: a buyer agent with a purchased memory artifact nearly matched the expert that trained over 20 rounds.

This prototype tackles the hardest unsolved problem: **verification and trust**. Without it, memory markets can't function — buyers have no way to evaluate artifact quality before purchase, and sellers can submit poisoned artifacts.

## Verification Protocol Flow

```
Step 1: SUBMIT
  Seller submits artifact (full JSON with M = D, K, P, A, H)
  → Validate schema, compute hash, store in registry

Step 2: SELECT BENCHMARK
  → Pick active benchmark for the artifact's domain
  → Held-out protocols are NEVER revealed to seller

Step 3: SPAWN NOVICE BASELINE
  → Fresh agent, no memory, evaluates all benchmark protocols
  → Cached per benchmark (doesn't change between verifications)

Step 4: SPAWN REFEREE (disposable)
  → Fresh agent with artifact.knowledge.content injected into system prompt
  → Evaluates all benchmark protocols (same prompts as novice)

Step 5: DIFFERENTIAL SCORING
  → For each protocol: buyer_error = |referee_score - true_score|
  → Transfer efficiency = (novice_avg_error - buyer_avg_error) / novice_avg_error × 100
  → Confidence interval via bootstrap

Step 6: ADVERSARIAL PROBES (parallel with Step 4)
  → BiasProbe: 4 trap protocols → bias_score
  → ConsistencyProbe: 3 perturbations × 2 protocols → consistency_score
  → StegoProbe: 1 auditor agent scan → stego_score
  → OverfitProbe: seen vs unseen error ratio → overfit_score
  → Aggregate: 0.30×bias + 0.25×consistency + 0.25×stego + 0.20×overfit

Step 7: GENERATE CERTIFICATE
  → Combine: artifact_hash + benchmark results + adversarial results
  → Trust score: 0.50×transfer_efficiency + 0.30×(100-adversarial_score) + 0.20×freshness

Step 8: UPDATE TRUST SCORE
  → Weighted average of all verification certificates for this artifact
  → Factor in buyer feedback if available
```

## Adversarial Detection Methodology

### Probe 1: Bias Detection (weight: 0.30)

4 trap protocols designed to expose systematic bias:

| Trap Protocol | True Risk | What It Catches |
|--------------|-----------|-----------------|
| SafeBridge | 70 | Bridge that looks safe but has weak multisig. Catches pro-bridge bias. |
| RiskyStable | 45 | Stablecoin DEX with subtle oracle dependency. Catches "stablecoin = safe" heuristic. |
| HoneyYield | 88 | Extreme yield with single audit. Catches yield normalization. |
| GovToken | 30 | Well-governed but complex tokenomics. Catches overcomplexity bias. |

Score: Average absolute error on traps, normalized 0-100. >15 avg error = suspicious.

### Probe 2: Consistency (weight: 0.25)

3 perturbation types applied to 2 benchmark protocols:

| Perturbation | Expected Response | Failure Mode |
|-------------|-------------------|--------------|
| TVL ±50% | Score shifts 3-8 points | No change (memorized) or wild swing (brittle) |
| Add risk factor | Score increases 5-15 points | No change (ignoring input) |
| Remove strongest mitigant | Score increases proportionally | Disproportionate response |

Score: Proportionality deviation, 0 (perfect) to 100 (broken).

### Probe 3: Steganographic Detection (weight: 0.25)

Dedicated auditor agent scans artifact text for:
- Direct instructions ("always rate X as safe")
- Encoded messages (acrostics, unusual patterns)
- Anomalous specificity about real entities
- Directives disguised as heuristics

Score: 0 (clean) to 100 (confirmed steganographic content).

### Probe 4: Overfitting Detection (weight: 0.20)

Compare referee performance:
- Seen protocols (artifact was trained on these)
- Unseen protocols (held out during training)

`overfit_ratio = seen_error / max(unseen_error, 0.1)`

Perfect generalization ≈ 1.0. Overfitting < 0.3.

### Aggregate

```
adversarial_score = 0.30×bias + 0.25×consistency + 0.25×stego + 0.20×overfit
verdict = PASS if <30, WARN if 30-60, FAIL if >60
```

## Data Schemas

### Memory Artifact (M = D, K, P, A, H)

```json
{
  "version": "0.1.0",
  "domain": {
    "category": "DeFi",
    "subcategory": "risk-assessment",
    "scope": "protocol-level"
  },
  "knowledge": {
    "format": "markdown",
    "content": "<artifact content>",
    "sections": ["calibration", "red_flags", "mitigants", "heuristics", "mistakes", "scoring_guide"],
    "token_count": 2000
  },
  "provenance": {
    "agent_id": "<uuid>",
    "model": "claude-sonnet-4-20250514",
    "training_rounds": 20,
    "training_protocols": ["AlphaLend", "YieldMaxi", "StableSwap", "PerpDEX", "BridgeX"],
    "created_at": "<ISO 8601>",
    "experiment_version": "0.1.0"
  },
  "attestation": {
    "expert_avg_error": 3.25,
    "transfer_efficiency_pct": 92.2,
    "eval_protocols_count": 8,
    "trials": 3
  },
  "hash": "<SHA-256>"
}
```

### Verification Certificate

```json
{
  "version": "0.1.0",
  "artifact_hash": "<matches artifact.hash>",
  "benchmark": {
    "id": "<uuid>",
    "domain": "DeFi:risk-assessment",
    "protocol_count": 8,
    "held_out_count": 3,
    "hash": "<SHA-256>"
  },
  "results": {
    "buyer_avg_error": 3.75,
    "novice_avg_error": 9.67,
    "transfer_efficiency_pct": 92.2,
    "confidence_interval_95": [85.0, 97.0],
    "per_protocol": {}
  },
  "adversarial": {
    "aggregate_score": 12,
    "bias_score": 8,
    "consistency_score": 15,
    "stego_score": 5,
    "overfit_score": 18,
    "flags": [],
    "verdict": "PASS"
  },
  "trust_score": 87.5,
  "issued_at": "<ISO 8601>",
  "expires_at": "<+90 days>",
  "referee_model": "claude-sonnet-4-20250514"
}
```

### SQLite Registry

```sql
CREATE TABLE artifacts (
    hash TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    knowledge_content TEXT NOT NULL,
    provenance_json TEXT NOT NULL,
    attestation_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    seller_id TEXT
);

CREATE TABLE benchmarks (
    id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    config_hash TEXT NOT NULL,
    protocol_count INTEGER,
    held_out_count INTEGER,
    created_at TEXT NOT NULL,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE verifications (
    id TEXT PRIMARY KEY,
    artifact_hash TEXT REFERENCES artifacts(hash),
    benchmark_id TEXT REFERENCES benchmarks(id),
    certificate_json TEXT NOT NULL,
    transfer_efficiency REAL,
    adversarial_score REAL,
    trust_score REAL,
    created_at TEXT NOT NULL
);

CREATE TABLE trust_scores (
    artifact_hash TEXT PRIMARY KEY REFERENCES artifacts(hash),
    current_score REAL,
    verification_count INTEGER DEFAULT 0,
    feedback_count INTEGER DEFAULT 0,
    last_updated TEXT
);

CREATE TABLE buyer_feedback (
    id TEXT PRIMARY KEY,
    artifact_hash TEXT REFERENCES artifacts(hash),
    buyer_id TEXT,
    reported_improvement REAL,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    feedback_text TEXT,
    created_at TEXT NOT NULL
);
```

## API Call Budget

| Operation | Calls | Cost |
|-----------|-------|------|
| Novice baseline (8 protocols) | 8 | $0.11 (cached) |
| Referee evaluation (8 protocols) | 8 | $0.11 |
| Bias probe (4 traps) | 4 | $0.06 |
| Consistency probe (6 perturbations) | 3 | $0.04 |
| Stego probe (1 auditor scan) | 1 | $0.01 |
| Overfit probe | 0 | reuses referee data |
| **Total per verification** | **~24** | **~$0.33** |
| Full train + verify (3 trials) | ~138 | ~$2.00 |

## Build Phases

1. **Foundation**: API wrapper, config, domain abstraction, DeFi risk domain config
2. **Artifact Spec**: Schema, validation, export wrapping
3. **Benchmark Engine**: Training, sandbox evaluation, orchestration
4. **Trust Registry**: SQLite, CRUD, trust score computation
5. **Adversarial Suite**: All 4 probes + runner (novel contribution)
6. **Verification Protocol**: Referee orchestrator, certificates
7. **Integration**: CLI entry points, tests, polish
