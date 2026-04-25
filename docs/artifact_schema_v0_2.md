# IMPP Artifact Schema v0.2

This document describes the changes from v0.1 to v0.2 of the IMPP artifact schema.

## Changes from v0.1

v0.1 defined `M = (D, K, P, A, H)` with minimal fields. v0.2 extends the schema with fields required for a credible protocol paper.

### New Top-Level Fields

| Field | Type | Purpose |
|-------|------|---------|
| `artifact_type` | enum | Classifies the memory type: `procedural`, `semantic`, `episodic_derived`, `hybrid` |
| `attach` | object | Runtime attach mode configuration |
| `card` | object | Artifact card (intended use, contraindications, known failures) |
| `privacy` | object | PII and jurisdiction metadata |
| `conflicts` | array | Declared conflicts with other artifacts |
| `revocation` | object | Revocation status and reason |

### Extended Provenance

| Field | Type | Purpose |
|-------|------|---------|
| `provenance.license` | enum | `MIT`, `Apache-2.0`, `CC-BY-4.0`, `CC-BY-SA-4.0`, `CC-BY-NC-4.0`, `proprietary` |
| `provenance.license_url` | uri | URL to full license text |
| `provenance.source_material` | array | Structured source references with per-source licensing |

### Extended Attestation

| Field | Type | Purpose |
|-------|------|---------|
| `attestation.evaluation_suite` | object | Metadata about the evaluation benchmark used |

### Attach Mode Configuration

```json
{
  "attach": {
    "supported_modes": ["prepend_policy", "retrieval_only"],
    "default_mode": "prepend_policy",
    "prohibited_modes": ["tool_policy"]
  }
}
```

### Artifact Card

```json
{
  "card": {
    "intended_use": "DeFi protocol risk scoring for lending and bridge categories",
    "contraindications": ["Not suitable for NFT valuation", "Not tested on L2-specific protocols"],
    "known_failures": ["Underestimates risk for protocols with less than 30 days of history"],
    "limitations": "Trained on synthetic protocol profiles, not real-world DeFi data"
  }
}
```

### Privacy Metadata

```json
{
  "privacy": {
    "contains_pii": false,
    "pii_redacted": false,
    "data_jurisdiction": "EU"
  }
}
```

### Conflict Declarations

```json
{
  "conflicts": [
    {
      "artifact": "defi-risk-v1",
      "reason": "Superseded — v2 uses updated risk weights that contradict v1 calibration"
    }
  ]
}
```

## JSON Schema

The formal JSON Schema is at [`schemas/impp.artifact.v0.2.schema.json`](../schemas/impp.artifact.v0.2.schema.json).

## Migration

v0.1 artifacts are forward-compatible: all new fields are optional. The only breaking change is `impp_version` moving from `"0.5"` to `"0.2"` (note: the original v0.1 used `"0.5"` as the version string — this was a misnomer that is corrected in v0.2).

To upgrade a v0.1 artifact:
1. Set `impp_version` to `"0.2"`
2. Add `artifact_type` (recommended)
3. Add `provenance.license` (recommended)
4. Add `attach.supported_modes` (recommended)
5. All other new fields are optional
