# IMPP Trust Model

IMPP treats portable memory artifacts as untrusted behavioral supply-chain material. A memory artifact can change how an agent reasons, retrieves context, follows procedures, or uses tools. Trust therefore requires more than file integrity.

The protocol separates trust into two layers:

1. **Container / supply-chain trust** — verifies artifact identity, authorship, publication history, and tamper resistance.
2. **Semantic / behavioral trust** — evaluates whether the artifact improves behavior safely within its declared scope.

## Layer 1: Container and supply-chain trust

This layer answers:

- Is this artifact the artifact the registry claims it is?
- Who published it?
- Was it modified after publication?
- Which verification steps were run?
- Has it been revoked or superseded?
- Can a consumer audit its publication history?

### Minimum fields

```yaml
provenance:
  content_hash: sha256:...
  manifest_hash: sha256:...
  signature: ed25519:...
  transparency_log: null
  attestations: []

revocation:
  status: active
  reason: null
  superseded_by: null
```

### Recommended mechanisms

IMPP may use its own simple Ed25519 certificates in the reference implementation, but production registries should be designed to integrate with mature supply-chain patterns:

- content-addressed storage;
- short-lived signing keys or certificates;
- transparency logs;
- step-level attestations;
- reproducible evaluation records;
- threshold signing for high-trust artifacts;
- revocation and downgrade metadata.

Signatures verify integrity and publisher identity. They do not prove semantic safety.

## Layer 2: Semantic and behavioral trust

This layer answers:

- Does the artifact improve downstream task performance?
- Does it transfer across compatible model families?
- Does it cause negative transfer outside its declared scope?
- Does it contain hidden instructions or manipulation?
- Is it stale?
- Does it conflict with installed artifacts or host policy?
- Is the claimed score supported by held-out evaluation?

### Verification dimensions

Recommended dimensions:

| Dimension | Question | Example metric |
|---|---|---|
| Transfer effectiveness | Does the artifact improve task performance? | paired uplift vs baseline |
| Robustness | Does it hold across models/seeds/tasks? | cross-model variance |
| Adversarial cleanliness | Is it free from hidden instructions or manipulation? | adversarial risk score |
| Negative-transfer risk | Does it harm out-of-scope tasks? | out-of-domain performance drop |
| Freshness | Is the artifact still current? | decay model, reverify age |
| Composability | Does it work with other artifacts? | marginal uplift in bundle |
| Efficiency | Is the gain worth token/eval cost? | uplift per token or dollar |

## Trust ladder

Artifacts move through staged trust states:

| State | Meaning | Allowed default behavior |
|---|---|---|
| `imported` | Source discovered; no structural guarantees | read-only review only |
| `parsed` | Schema-valid; hash and source recorded | read-only or sandboxed retrieval |
| `evaluated` | Behavioral tests completed | retrieval or examples if passed |
| `verified` | Signed certificate and acceptable risk | declared allowed modes |
| `curated` | Human/domain review plus strong evidence | declared allowed modes with higher confidence |
| `rejected` | Failed parsing or evaluation | blocked by default |
| `revoked` | Previously valid but no longer trusted | blocked by default |
| `superseded` | Replaced by newer artifact | warn and prefer successor |

Trust state is not permanent. Freshness decay, new attacks, failed reevaluation, or changed domain facts can downgrade an artifact.

## Trust score

The current reference implementation uses a provisional weighted score:

```text
trust = 0.50 * transfer_efficiency
      + 0.30 * adversarial_clean
      + 0.20 * freshness
```

where:

```text
adversarial_clean = 100 - adversarial_risk
```

The adversarial risk score is currently composed from:

```text
bias:        30%
consistency: 25%
stego:       25%
overfit:     20%
```

This score should be presented as a reference heuristic, not a ground-truth measure of safety. A production registry should calibrate weights against downstream outcomes and publish reason codes alongside numeric scores.

## Public methodology, private holdouts

IMPP should publish:

- artifact schema;
- scoring formula;
- probe categories;
- sample fixtures;
- public benchmark harness;
- score version history;
- known limitations.

A production registry should keep rotating holdouts private:

- live adversarial prompts;
- canary artifacts;
- buyer outcome labels;
- abuse heuristics;
- production calibration sets.

This is not security through obscurity. It is evaluation hygiene. Public methodology supports trust; private rotating holdouts reduce benchmark gaming.

## Reason codes

Every trust score should include reason codes. Example:

```yaml
trust_score: 84.0
reason_codes:
  - high_transfer_efficiency
  - no_hidden_instruction_detected
  - fresh_within_30_days
  - limited_cross_model_coverage
  - not_validated_for_real_time_trading
```

Consumers should be able to see why a score was assigned and what evidence was missing.

## Revocation and downgrade

Artifacts should be downgraded or revoked when:

- hidden instructions are discovered;
- evaluation results are falsified;
- source license is invalid;
- PII/proprietary content is found;
- domain assumptions become stale;
- a signing key is compromised;
- a newer artifact supersedes it;
- production incidents show negative transfer.

Revoked artifacts should remain visible in audit logs but blocked by default.

## Paper framing

The paper should frame trust as the central systems problem. Portable memory is valuable only if it can be made legible, bounded, evaluated, and revocable. IMPP's contribution is not simply a score; it is the protocol surface that makes memory artifacts inspectable before they influence agents.
