# IMPP: A Protocol for Portable Procedural Memory in AI Agent Systems

**Ned Karlovich**  
Working draft — protocol-first arXiv version

## Abstract

AI agents increasingly rely on persistent memory: task traces, skill files, prompt refinements, domain heuristics, user preferences, and structured notes that improve behavior across interactions. Today, this memory is usually bound to a single application, framework, model provider, or deployment. We introduce IMPP, the Inter-Model Memory Protocol, a protocol for representing procedural and semantic agent memory as signed, versioned, evaluable artifacts. IMPP defines a memory-artifact schema, explicit attach modes describing how artifacts influence runtime behavior, provenance and privacy metadata, a staged trust ladder, and a verification pipeline combining supply-chain integrity checks with behavioral evaluation. We present a reference implementation and pilot experiments in DeFi risk assessment and cybersecurity vulnerability assessment. These experiments suggest that structured memory artifacts can transfer useful calibration behavior across agents, while also revealing important failure modes: benchmark leakage, anchoring, negative transfer, hidden instructions, and score gaming. We argue that portable agent memory should be treated as untrusted behavioral supply-chain material, requiring artifact cards, revocation, holdout evaluation, and adversarial testing before deployment. IMPP is a first step toward making learned agent behavior legible, portable, and governable.

## 1. Introduction

AI agents are beginning to accumulate operational memory. They store user preferences, summarize prior interactions, write tool-use notes, maintain vector stores, build skill libraries, and refine prompts from experience. These memories can materially change downstream behavior. A risk-assessment agent may become better calibrated after repeated feedback. A security triage agent may learn which vulnerabilities are usually exploitable. A customer-support agent may learn escalation patterns that reduce resolution time.

Most of this memory remains deployment-local. It is stored inside one application, one vector index, one prompt stack, one file tree, or one model-provider-specific workflow. When another agent faces a similar task, it usually starts over. This is inefficient, but the deeper problem is that there is no common infrastructure for packaging, verifying, and safely attaching learned behavior across agent systems.

Software ecosystems solved a related problem through package registries. Reusable behavior is packaged, versioned, signed, documented, distributed, and governed. Agent memory needs an analogous layer, but memory artifacts differ from ordinary software packages. They may not execute directly; instead, they bias future model behavior through context, retrieval, examples, policies, or tool constraints. Their failures can be delayed, probabilistic, and context-sensitive.

IMPP addresses this gap. It treats portable agent memory as a behavioral artifact that must be described, scoped, signed, evaluated, attached explicitly, and revocable.

This paper makes six contributions:

1. **Artifact model.** We define portable procedural and semantic memory artifacts with manifests, payloads, provenance, privacy metadata, evaluation metadata, and revocation state.
2. **Attach semantics.** We define runtime attach modes specifying how an artifact affects an agent: `prepend_policy`, `few_shot_examples`, `retrieval_only`, `tool_policy`, and `read_only_reference`.
3. **Two-layer trust model.** We separate supply-chain trust from semantic/behavioral trust.
4. **Verification pipeline.** We present a referee protocol using held-out evaluation, freshness, adversarial probes, and signed certificates.
5. **Reference implementation.** We describe an open-source Python implementation and registry prototype.
6. **Pilot validation.** We report preliminary transfer, cross-model, leakage, and adversarial-artifact results, while explicitly limiting the scope of the empirical claims.

## 2. Scope: what kind of memory is portable?

“Memory” is too broad to be a protocol unit. IMPP focuses on two forms of memory:

- **Procedural memory:** instructions, heuristics, decision rules, calibration frameworks, examples, and tool-use policies that influence how an agent performs a task.
- **Semantic memory:** structured domain knowledge, taxonomies, assumptions, constraints, and relationships.

Episodic memory can be useful, but raw episodes often contain private user data, proprietary traces, or deployment-specific context. IMPP supports episodic-derived artifacts only after transformation, redaction, licensing, and provenance review.

The central claim is therefore intentionally narrow: bounded procedural and semantic memories can be packaged as portable artifacts, but safe transfer requires explicit scope, attach semantics, provenance, and behavioral verification.

## 3. Artifact model

An IMPP artifact is a signed package containing:

- a manifest;
- a memory payload;
- a human-readable artifact card;
- source and provenance metadata;
- privacy and license metadata;
- declared attach modes;
- evaluation results;
- known failure modes;
- dependency and conflict declarations;
- revocation and freshness metadata.

Earlier versions of IMPP used the tuple `M = (D, K, P, A, H)`, where domain, knowledge, provenance, attestation, and hash define the core artifact. The v0.2 schema expands this tuple into a more operational protocol object.

A minimal artifact manifest should answer:

1. What domain and task is this memory for?
2. What kind of memory is it?
3. How may it be attached to an agent?
4. What source material produced it?
5. What data, privacy, and license restrictions apply?
6. What evaluations has it passed?
7. What are its known failure modes?
8. What should happen if it becomes stale, revoked, or conflicting?

## 4. Attach semantics

Installing memory is ambiguous unless the runtime contract is explicit. The same artifact can affect behavior differently depending on how it is attached.

IMPP defines five initial attach modes:

| Attach mode | Runtime behavior | Typical use | Main risk |
|---|---|---|---|
| `prepend_policy` | Injects guidance near the top of the agent context | Safety or domain policy | High behavioral authority |
| `few_shot_examples` | Provides examples for imitation | Calibration and format learning | Benchmark leakage or anchoring |
| `retrieval_only` | Indexed and retrieved only when relevant | Large knowledge payloads | Retrieval poisoning |
| `tool_policy` | Constrains tool use or escalation | Operational controls | Policy conflict |
| `read_only_reference` | Available as a file/namespace but not injected automatically | Low-risk documentation | Underuse or misinterpretation |

Attach modes are part of the protocol, not implementation detail. They determine token budget, safety exposure, conflict handling, and transfer behavior.

## 5. Trust model

IMPP separates trust into two layers.

### 5.1 Container and supply-chain trust

This layer asks whether the artifact is the artifact it claims to be:

- Is the content hash valid?
- Is the signature valid?
- Is the provenance chain intact?
- Were evaluation steps attested?
- Has the artifact been revoked?
- Is the publication history auditable?

Ed25519 signatures are useful, but signatures alone are insufficient. A production implementation should support transparency logs, attestations, revocation metadata, and key-compromise recovery.

### 5.2 Semantic and behavioral trust

This layer asks whether the artifact improves behavior safely:

- Does it improve task performance on held-out data?
- Does it transfer across compatible model families?
- Does it cause negative transfer outside its declared scope?
- Does it contain hidden instructions or manipulation?
- Is it stale?
- Does it conflict with other artifacts?
- Does its trust score predict downstream success?

Memory artifacts are untrusted behavioral supply-chain material. Verification must therefore include both integrity checks and behavioral evaluation.

## 6. Verification pipeline

The reference verifier follows a referee protocol:

1. Validate artifact schema.
2. Compute content hash.
3. Select domain-appropriate benchmark.
4. Evaluate a no-memory baseline.
5. Evaluate a buyer/referee agent with the artifact attached.
6. Compute transfer efficiency and error reduction.
7. Run adversarial probes.
8. Compute trust score and reason codes.
9. Issue a signed certificate.
10. Store certificate and update registry trust state.

The current reference implementation uses hand-weighted components:

- transfer efficiency: 50%;
- adversarial cleanliness: 30%;
- freshness: 20%.

Adversarial risk currently combines:

- bias: 30%;
- consistency: 25%;
- steganography: 25%;
- overfitting: 20%.

These weights should be treated as provisional reference weights, not universal truth. A mature registry should calibrate them against downstream success and safety outcomes.

## 7. Staged trust ladder

IMPP uses staged trust rather than binary safe/unsafe labels:

1. **Imported** — source captured; no structural guarantee.
2. **Parsed** — schema-valid; hash and required metadata present.
3. **Evaluated** — sandbox evaluation completed.
4. **Verified** — signed certificate issued after meeting verification criteria.
5. **Curated** — reviewed by maintainers or domain experts.
6. **Rejected** — blocked because of invalid metadata, unsafe behavior, poisoning, revocation, or stale state.

Trust state is attached to a specific artifact version. New versions must be re-evaluated. Revoked artifacts should remain visible in the log but blocked by default.

## 8. Evaluation plan and pilot evidence

The current prototype evaluates memory transfer in synthetic DeFi risk assessment and cybersecurity vulnerability assessment. The initial results are promising but pilot-scale. They should be interpreted as evidence that the protocol is worth studying, not as proof of universal transfer.

A credible evaluation suite should include:

- no-memory baseline;
- raw source context baseline;
- RAG baseline;
- prompt-only skill-file baseline;
- IMPP artifact with declared attach mode;
- attach-mode ablation;
- negative-transfer tests;
- adversarial artifact tests;
- trust-score calibration.

The current repository contains experiment infrastructure for trials, domains, cross-model buyer settings, sanitized artifacts, verification, storage, and JSON output. The next step is a public `data/paper_v1/` reproducibility package that regenerates the main tables.

## 9. Security and governance considerations

A memory artifact can act like an instruction-bearing dependency. Threats include:

- prompt injection;
- hidden instructions;
- stale assumptions;
- negative transfer;
- benchmark gaming;
- license contamination;
- PII leakage;
- artifact impersonation;
- registry compromise;
- signing-key compromise;
- conflict between installed artifacts.

Public methodology should be transparent, but production holdouts and abuse probes should rotate. Publishing the scoring formula is acceptable; publishing the entire live exam key is not.

## 10. Limitations

This work is preliminary. Current experiments use small synthetic domains and limited trials. Cross-model results are pilot evidence rather than statistically robust proof. The trust score is hand-weighted and requires calibration. Freshness, composability, revocation, and marketplace incentive dynamics remain under-tested. The paper should not claim that portable memory is universally safe or broadly generalizable.

## 11. Discussion: registry before marketplace

A marketplace may eventually be useful, but the protocol must come first. A marketplace turns verification scores into economic targets. That raises the stakes for adversarial optimization, dispute handling, review governance, and abuse monitoring.

The safer development sequence is:

1. protocol;
2. schema;
3. reference implementation;
4. reproducible benchmark;
5. curated registry;
6. commercial marketplace extensions.

## 12. Conclusion

Agent memory will become valuable infrastructure only if it can be transferred without collapsing trust. IMPP proposes a protocol for making learned agent behavior legible, attachable, verifiable, and revocable. The strongest near-term claim is not that memory markets are inevitable. It is that portable procedural and semantic memory artifacts are plausible, useful, and risky enough to require protocol-level treatment.
