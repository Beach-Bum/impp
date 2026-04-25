# IMPP Trust Model

IMPP separates trust into two independent layers. Both must pass for an artifact to be trusted.

## Layer 1: Container / Supply-Chain Trust

This layer answers: **is this artifact what it claims to be?**

| Check | What It Verifies |
|-------|-----------------|
| Schema validation | Required fields present, format constraints met |
| Hash integrity | SHA-256 hash matches content |
| Signature verification | Ed25519 certificate signed by known registry key |
| Certificate validity | Not expired, not revoked |
| Provenance metadata | Agent ID, model, timestamp present |

Supply-chain trust is **binary**: the artifact either passes all checks or it doesn't. There is no partial pass.

This layer is analogous to package signature verification in npm, PyPI, or Sigstore.

## Layer 2: Semantic / Behavioral Trust

This layer answers: **does this artifact actually improve agent behavior safely?**

| Check | What It Measures |
|-------|-----------------|
| Transfer efficiency | How much of the expert-novice gap the artifact closes |
| Negative transfer | Whether the artifact degrades baseline performance |
| Bias detection | Systematic directional errors in subcategories |
| Consistency | Response stability under input perturbation |
| Steganography | Hidden instructions or payload patterns |
| Freshness | Age relative to domain update frequency |

Behavioral trust is **continuous**: expressed as a trust score (0-100) with component breakdowns.

This layer has no direct analogue in package registries. It is closer to model evaluation in ML, but applied to behavioral artifacts rather than model weights.

## Trust Score

The trust score is a weighted composite:

```
trust_score = (
    0.50 * transfer_efficiency +
    0.30 * adversarial_clean +
    0.20 * freshness
)
```

Where:
- `transfer_efficiency` (0-100): percentage of expert-novice gap closed
- `adversarial_clean` (0-100): `100 - adversarial_risk_score`
- `freshness` (0-100): exponential decay with 180-day half-life

### Adversarial Risk Score

The adversarial risk score is itself a weighted composite:

```
adversarial_risk = (
    0.30 * bias +
    0.25 * consistency +
    0.25 * stego +
    0.20 * overfit
)
```

### Thresholds

| Risk Score | Outcome |
|------------|---------|
| 0-30 | PASS |
| 31-50 | WARN (manual review) |
| 51-100 | FAIL (rejected) |

| Trust Score | Meaning |
|-------------|---------|
| 80-100 | High confidence transfer |
| 50-79 | Usable with caveats |
| Below 50 | Not certified |

### Calibration Status

**The current weights are hand-tuned and provisional.** They have not been calibrated against downstream agent outcomes at scale. The trust score should be treated as a directional signal, not an objective measure.

Future calibration will require:
- Larger evaluation corpora (current: 8-32 items per domain)
- More domains beyond DeFi and CyberSec
- Real-world deployment feedback
- Statistical validation of weight choices

## Staged Trust Ladder

Artifacts progress through trust stages:

```
Imported → Parsed → Evaluated → Verified → Curated
                                              ↓
                                          Rejected
```

| Stage | What Happens |
|-------|-------------|
| **Imported** | Raw artifact submitted, basic format check |
| **Parsed** | Schema validated, PII check, content extracted |
| **Evaluated** | Behavioral probes run, transfer efficiency measured |
| **Verified** | Certificate issued, trust score assigned |
| **Curated** | Manual review passed, featured in registry |
| **Rejected** | Failed at any stage, with reason code |

Each stage adds trust. Consumers can choose their minimum stage:
- `verified` (default): only install artifacts with valid certificates
- `evaluated`: install artifacts that passed probes but may not have certificates yet
- `curated`: only install manually reviewed artifacts

## Trust Decay

Trust is not permanent:
- Certificates expire after 90 days
- Freshness score decays exponentially
- Re-verification can raise or lower trust scores
- Revocation immediately invalidates trust

## Reason Codes (Future)

Trust scores will be accompanied by reason codes explaining why a score is what it is:

```json
{
  "trust_score": 78.5,
  "reasons": [
    {"code": "TE_GOOD", "detail": "Transfer efficiency 85% across 3 trials"},
    {"code": "ADV_CLEAN", "detail": "All adversarial probes passed (risk: 12)"},
    {"code": "FRESHNESS_WARN", "detail": "Artifact is 95 days old (freshness: 68%)"}
  ]
}
```

This is not yet implemented. Current trust scores are opaque numbers.
