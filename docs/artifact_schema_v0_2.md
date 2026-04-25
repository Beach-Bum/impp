# IMPP Artifact Schema v0.2

This document defines the protocol-first artifact schema for IMPP.

The original implementation used the compact tuple:

```text
M = (D, K, P, A, H)
```

where:

- `D` = domain;
- `K` = knowledge payload;
- `P` = provenance;
- `A` = attestation;
- `H` = content hash.

Version 0.2 keeps this conceptual core but expands it into a deployable artifact manifest suitable for open registries, evaluation, revocation, and safe runtime attachment.

## Design goals

An IMPP artifact should be:

1. **Portable** — usable across compatible agent runtimes and model families.
2. **Scoped** — explicit about domain, task, and contraindications.
3. **Attachable** — clear about how it may influence runtime behavior.
4. **Verifiable** — hashable, signable, and evaluable.
5. **Auditable** — source, license, privacy, and evaluation metadata are recorded.
6. **Revocable** — stale or unsafe artifacts can be downgraded or blocked.
7. **Composable** — dependencies and conflicts are declared instead of discovered through prompt collisions.

## Top-level manifest

```yaml
schema: impp.artifact.v0.2
name: impp/defi-risk-calibration
version: 1.0.0
type: procedural
license: Apache-2.0
summary: Calibration framework for DeFi protocol risk assessment.

artifact_card: CARD.md
payload:
  format: markdown
  path: memory.md

scope:
  domain: defi-risk-assessment
  subdomains:
    - lending
    - governance
    - oracle-risk
    - bridge-risk
  intended_use:
    - protocol risk scoring
    - analyst support
    - benchmark evaluation
  prohibited_use:
    - autonomous trading
    - investment advice
    - production liquidation decisions without human review
  contraindications:
    - real-time market execution
    - protocols launched after observation window

attach:
  allowed_modes:
    - retrieval_only
    - few_shot_examples
    - read_only_reference
  prohibited_modes:
    - prepend_policy
    - tool_policy
  default_mode: retrieval_only

source:
  author: Ned Karlovich
  author_agent: claude-sonnet-4-20250514
  observation_window: 2024-01-01/2026-04-01
  source_material:
    - synthetic benchmark protocols
    - public audit-report-inspired rubric
  generation_method: expert_iteration

privacy:
  pii: none_detected
  proprietary_data: false
  redaction_method: not_applicable
  consent_required: false

provenance:
  content_hash: sha256:...
  manifest_hash: sha256:...
  signature: ed25519:...
  transparency_log: null
  attestations: []

evaluation:
  evaluated: true
  evaluator_version: impp-verifier-0.5.0
  evaluated_at: 2026-04-25T00:00:00Z
  suites:
    - defi-risk-public-v1
    - negative-transfer-v1
    - adversarial-memory-v1
  metrics:
    transfer_efficiency: 0.558
    relative_transfer_efficiency: 1.099
    adversarial_risk: 0.12
    trust_score: 84.0
  known_failures:
    - may over-penalize newly launched unaudited protocols
    - not validated for real-time trading

conflicts:
  declares:
    - risk_scoring.defi.oracle_assumptions
    - risk_scoring.defi.bridge_assumptions
  incompatible_with: []
  dependencies: []

freshness:
  created_at: 2026-04-25T00:00:00Z
  expires_at: 2026-07-25T00:00:00Z
  recommended_reverify_after_days: 30
  decay_model: domain_default

revocation:
  status: active
  reason: null
  superseded_by: null
```

## Required fields

The following fields are required for all artifacts:

```text
schema
name
version
type
license
summary
payload
scope
attach
source
privacy
provenance.content_hash
freshness.created_at
revocation.status
```

Evaluation fields may be empty for `imported` or `parsed` artifacts, but must be populated before an artifact can become `evaluated`, `verified`, or `curated`.

## Artifact types

| Type | Description | Example |
|---|---|---|
| `procedural` | Instructions, heuristics, decision rules, workflows, tool policies | Security triage rubric |
| `semantic` | Structured domain concepts, taxonomies, assumptions, relationships | DeFi risk ontology |
| `episodic_derived` | Redacted lessons distilled from traces or conversations | Incident postmortem lessons |
| `hybrid` | Combination of procedural and semantic payloads | Risk assessment framework with taxonomy |

Raw episodic traces should not be published as portable artifacts unless transformed, redacted, licensed, and explicitly approved.

## Attach contract

Artifacts must declare allowed, prohibited, and default attach modes. The protocol currently recognizes:

```text
prepend_policy
few_shot_examples
retrieval_only
tool_policy
read_only_reference
```

See `docs/attach_modes.md` for full semantics.

## Artifact card

Each artifact should include a human-readable artifact card. The card should explain:

- intended use;
- non-use cases;
- source material;
- authoring process;
- evaluation coverage;
- known failures;
- privacy and license notes;
- update and revocation policy.

## Trust states

Artifacts move through staged trust states:

```text
imported → parsed → evaluated → verified → curated
```

Artifacts can also become:

```text
rejected
revoked
superseded
```

Trust state is not permanent. A verified artifact can be downgraded if it becomes stale, fails reevaluation, or is found to contain unsafe content.

## Versioning

Artifact versions use semantic versioning:

- Patch: metadata, card, typo, or non-semantic correction.
- Minor: new examples, expanded scope, additional evaluation.
- Major: changed payload semantics, changed attach modes, or changed domain assumptions.

Any payload change requires a new content hash. Any major version requires reevaluation.

## Public vs private evaluation material

The manifest may reference public evaluation suites. Production registries should also use private rotating holdouts and canaries. Public methodology improves trust; publishing the entire live exam key weakens verification.

## Open questions

- Standard format for transparency-log entries.
- Standard signature envelope.
- Cross-registry namespace governance.
- Conflict-resolution algorithm for multi-artifact bundles.
- Machine-readable artifact-card schema.
- Calibration procedure for trust-score weights.
