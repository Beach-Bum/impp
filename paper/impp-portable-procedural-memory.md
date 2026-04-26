# IMPP: A Protocol for Portable Procedural Memory in AI Agent Systems

**Ned Karlovich**  
Working draft — protocol-first arXiv version

## Abstract

AI agents increasingly rely on persistent memory: task traces, skill files, prompt refinements, domain heuristics, user preferences, and structured notes that improve behavior across interactions. Today, this memory is usually bound to a single application, framework, model provider, or deployment. We introduce IMPP, the Inter-Model Memory Protocol, a protocol for representing procedural and semantic agent memory as signed, versioned, evaluable artifacts. IMPP defines a memory-artifact schema, explicit attach modes describing how artifacts influence runtime behavior, provenance and privacy metadata, a staged trust ladder, and a verification pipeline combining supply-chain integrity checks with behavioral evaluation. We present a reference implementation and pilot experiments in DeFi risk assessment and cybersecurity vulnerability assessment. Pilot results show mixed transfer: same-model Claude Sonnet evaluation on DeFi shows modest positive transfer (+5.6% TE), while cross-model GPT-4o transfer is slightly negative (-2.7%), and both models show negative transfer on cybersecurity tasks (-7.6% and -7.1% respectively). These results demonstrate that naive artifact attachment can produce zero or negative transfer, reinforcing the need for explicit attach semantics, model adaptation, verification, and negative-transfer testing. We argue that portable agent memory should be treated as untrusted behavioral supply-chain material, requiring artifact cards, revocation, holdout evaluation, and adversarial testing before deployment. IMPP is a first step toward making learned agent behavior legible, portable, and governable.

## 1. Introduction

AI agents are beginning to accumulate operational memory. They store user preferences, summarize prior interactions, write tool-use notes, maintain vector stores, build skill libraries, and refine prompts from experience. These memories can materially change downstream behavior. A risk-assessment agent may become better calibrated after repeated feedback. A security triage agent may learn which vulnerabilities are usually exploitable. A customer-support agent may learn escalation patterns that reduce resolution time.

Most of this memory remains deployment-local, bound to one application, vector index, prompt stack, or model-provider workflow. When another agent faces a similar task, it starts from scratch. The deeper problem is not inefficiency but the absence of common infrastructure for packaging, verifying, and safely attaching learned behavior across agent systems.

Software ecosystems solved a related problem through package registries, where reusable behavior is packaged, versioned, signed, and governed [10]. Agent memory needs an analogous layer, but memory artifacts differ from software packages in important ways: they may not execute directly, instead biasing model behavior through context, retrieval, examples, or policy injection. Their failures can be delayed, probabilistic, and context-sensitive.

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

The current prototype evaluates memory transfer in two synthetic domains: DeFi risk assessment (32 protocol items) and cybersecurity vulnerability assessment (8 items). We test two conditions: `no_memory` (baseline, no artifact) and `impp_artifact` (full IMPP artifact attached via `prepend_policy`). Each condition is evaluated across multiple independent trials.

### 8.1 Experimental setup

We evaluate two model configurations:

- **Same-model (Claude Sonnet via OpenRouter):** The artifact was produced by a Claude-family model and evaluated by the same model family. 3 trials per domain per condition.
- **Cross-model (GPT-4o):** The artifact was produced by Claude and evaluated by GPT-4o, testing cross-model portability. 4 trials for DeFi, 3 trials for CyberSec, per condition.

Each trial evaluates the same fixed task set. Transfer efficiency (TE) is computed as `(novice_MAE - artifact_MAE) / novice_MAE × 100`, where positive TE indicates the artifact improved performance over the no-memory baseline.

### 8.2 Results

**Table 1.** Per-model condition-level MAE (mean absolute error ± standard deviation across trials).

| Domain | Model | Condition | MAE | Trials |
|--------|-------|-----------|-----|--------|
| DeFi | Claude Sonnet | impp_artifact | 7.38 ± 0.65 | 3 |
| DeFi | Claude Sonnet | no_memory | 7.81 ± 0.41 | 3 |
| DeFi | GPT-4o | impp_artifact | 8.03 ± 0.69 | 4 |
| DeFi | GPT-4o | no_memory | 7.82 ± 0.24 | 4 |
| CyberSec | Claude Sonnet | impp_artifact | 18.33 ± 0.85 | 3 |
| CyberSec | Claude Sonnet | no_memory | 17.04 ± 1.23 | 3 |
| CyberSec | GPT-4o | impp_artifact | 16.42 ± 0.75 | 3 |
| CyberSec | GPT-4o | no_memory | 15.33 ± 1.83 | 3 |

**Table 2.** Per-model transfer efficiency. Positive TE indicates the artifact reduced error relative to the no-memory baseline.

| Domain | Claude Sonnet TE | GPT-4o TE |
|--------|-----------------|-----------|
| DeFi | +5.6% | -2.7% |
| CyberSec | -7.6% | -7.1% |

### 8.3 Interpretation

Table 1 reports per-model condition-level MAE; Table 2 reports per-model transfer efficiency. Pilot results show mixed transfer. DeFi same-model Claude evaluation shows a modest positive signal (+5.6% TE), suggesting the artifact provides some useful calibration when consumed by the same model family that produced it. Cross-model GPT-4o transfer on DeFi is slightly negative (-2.7%), consistent with the hypothesis that artifacts shaped by one model's reasoning style do not automatically help a different model. Both models show negative transfer on cybersecurity tasks, where the artifact appears to degrade performance below the no-memory baseline.

These results do not support a claim of broad positive transfer. They do support three protocol-level conclusions:

1. **Portable memory artifacts are feasible and evaluable.** The IMPP schema, attach mode, and verification pipeline can represent, deliver, and measure the effect of transferred memory.
2. **Naive attachment can produce zero or negative transfer.** Attaching an artifact via `prepend_policy` without model adaptation or domain matching is insufficient. The protocol must support attach-mode selection, model-compatibility metadata, and negative-transfer detection.
3. **Same-model transfer is more promising than cross-model transfer.** This is consistent with the intuition that procedural memory encodes model-specific reasoning patterns. Cross-model transfer likely requires artifact transformation or model-adaptive attach modes.

### 8.4 Credible evaluation suite

A complete evaluation should include conditions beyond the two tested here:

- raw source context baseline;
- RAG baseline;
- prompt-only skill-file baseline;
- attach-mode ablation;
- negative-transfer tests (wrong-domain artifact);
- adversarial artifact tests (poisoned artifact);
- trust-score calibration against downstream outcomes.

### 8.5 Reproducibility

All experiment infrastructure, data fixtures, and committed results are available in the project repository.

- **Task fixtures and labels:** `data/paper_v1/` contains domain task sets and ground-truth labels. Sample fixtures in `data/paper_v1/results.csv` are synthetic and marked `is_sample=true`; they should not be cited as empirical evidence.
- **Real pilot results:** `data/paper_v1/results_real.csv` contains all real experiment rows. Every row has `is_sample=false`. Generated tables are in `paper/tables/real/conditions.md` (Table 1) and `paper/tables/real/summary.md` (Table 2).
- **Experiment runner:** `experiments/run_paper_v1.py` orchestrates live and dry-run experiments.
- **Table generator:** `experiments/generate_paper_tables.py` regenerates markdown tables from committed CSV data.

To validate fixtures without API calls:

```
python experiments/run_paper_v1.py --dry-run --domain defi_risk
python experiments/run_paper_v1.py --dry-run --domain cybersec_vuln
```

To regenerate tables from committed real results:

```
python experiments/generate_paper_tables.py --source real
```

Live experiment runs require provider API keys (Anthropic, OpenAI, or OpenRouter) and are not required to inspect or verify the committed results. Private API keys and raw provider logs are not included in the repository.

### 8.6 Artifact availability

Source code and public fixtures are available in the project repository. Sample fixtures are clearly marked and should not be cited as empirical evidence. Real pilot tables (Tables 1 and 2) are generated from `results_real.csv` and can be regenerated using the commands above. The IMPP protocol schema, reference implementation, and registry prototype are open-source.

## 9. Related work

IMPP draws on several research threads. We summarize connections and distinctions here.

**Agent memory and persistent context.** Recent agent frameworks increasingly support persistent memory across sessions, including tool-use traces, user preference stores, and vector-indexed conversation history [1, 2, 3, 4]. IMPP differs by treating memory as a portable, signed artifact with explicit attach semantics rather than an internal implementation detail.

**Prompt and skill reuse.** Prompt engineering research has explored systematic prompt construction, reuse, and composition [5, 6]. Skill libraries and prompt registries share IMPP's goal of reusable behavioral components but typically lack provenance metadata, verification, or revocation mechanisms.

**Retrieval-augmented generation.** RAG systems retrieve relevant context from external stores to ground model responses [7]. IMPP's `retrieval_only` attach mode is analogous, but IMPP adds supply-chain trust, behavioral evaluation, and explicit scoping that RAG pipelines typically omit.

**Model cards, data cards, and artifact cards.** Model cards [8] and data cards [9] establish the practice of structured documentation for ML artifacts. IMPP's artifact card extends this pattern to behavioral memory, adding attach-mode declarations, evaluation certificates, and revocation state.

**Software supply-chain security.** Signed packages, provenance attestations, and transparency logs are established in software supply chains [10, 11]. IMPP adapts these patterns to behavioral artifacts, where the threat model includes not only tampering and impersonation but also prompt injection, hidden instructions, and negative transfer.

**Evaluation and benchmark leakage.** Held-out evaluation is standard practice, but benchmark leakage is an active concern for LLM evaluation. IMPP's verification pipeline requires holdout evaluation and adversarial probes, and the pilot results in Section 8 illustrate the risk that public labels may inflate apparent transfer efficiency.

## 10. Security and governance considerations

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

## 11. Limitations

This work is preliminary. Known limitations include:

- **Small scale.** Two synthetic domains, 32 and 8 items respectively, with 3-4 trials per condition per model. Effect sizes are small relative to trial variance. Larger item sets and more trials are needed before drawing strong conclusions about transfer magnitude.
- **Mixed transfer results.** Only one of four domain-model combinations (DeFi / Claude Sonnet) shows positive transfer. Three show negative transfer. This is honest but means the protocol's value currently rests on feasibility and infrastructure, not demonstrated performance improvement.
- **Benchmark leakage risk.** Public labels mean the model may have seen similar data during training. Transfer efficiency could reflect label familiarity rather than artifact quality.
- **Single attach mode tested.** All experiments use `prepend_policy`. Other attach modes (`few_shot_examples`, `retrieval_only`, `tool_policy`) may produce different transfer characteristics.
- **No model-adaptive attach.** The same artifact text is attached regardless of the consuming model. Model-specific reformulation or selective retrieval might improve cross-model transfer.
- **Hand-weighted trust scores.** The verification pipeline weights (transfer efficiency 50%, adversarial cleanliness 30%, freshness 20%) are provisional and uncalibrated against downstream outcomes.
- **Untested dynamics.** Freshness, composability, revocation, and marketplace incentive dynamics remain under-tested.

## 12. Discussion: registry before marketplace

A marketplace may eventually be useful, but the protocol must come first. A marketplace turns verification scores into economic targets. That raises the stakes for adversarial optimization, dispute handling, review governance, and abuse monitoring.

The safer development sequence is:

1. protocol;
2. schema;
3. reference implementation;
4. reproducible benchmark;
5. curated registry;
6. commercial marketplace extensions.

## 13. Conclusion

Agent memory will become valuable infrastructure only if it can be transferred without collapsing trust. IMPP proposes a protocol for making learned agent behavior legible, attachable, verifiable, and revocable.

Our pilot results reinforce a conservative framing: portable memory artifacts are feasible and evaluable, but naive attachment can produce zero or negative transfer. The protocol must therefore include explicit attach semantics, model-compatibility metadata, verification pipelines, and negative-transfer testing as first-class concerns, not optional extensions.

The strongest near-term claim is not that memory transfer reliably improves performance. It is that portable procedural and semantic memory artifacts are plausible, measurable, and risky enough to require protocol-level treatment. The path forward requires larger benchmarks, attach-mode ablation, model-adaptive delivery, and calibrated trust scoring.

## References

[1] J. S. Park, J. C. O'Brien, C. J. Cai, M. R. Morris, P. Liang, and M. S. Bernstein. "Generative Agents: Interactive Simulacra of Human Behavior." UIST 2023. arXiv:2304.03442.

[2] C. Packer, S. Wooders, K. Lin, V. Fang, S. G. Patil, I. Stoica, and J. E. Gonzalez. "MemGPT: Towards LLMs as Operating Systems." arXiv:2310.08560, 2023.

[3] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao. "Reflexion: Language Agents with Verbal Reinforcement Learning." NeurIPS 2023. arXiv:2303.11366.

[4] G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and A. Anandkumar. "Voyager: An Open-Ended Embodied Agent with Large Language Models." arXiv:2305.16291, 2023.

[5] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, and D. Zhou. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." NeurIPS 2022. arXiv:2201.11903.

[6] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao. "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023. arXiv:2210.03629.

[7] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS 2020. arXiv:2005.11401.

[8] M. Mitchell, S. Wu, A. Zaldivar, P. Barnes, L. Vasserman, B. Hutchinson, E. Spitzer, I. D. Raji, and T. Gebru. "Model Cards for Model Reporting." FAT* 2019. arXiv:1810.03993.

[9] T. Gebru, J. Morgenstern, B. Vecchione, J. W. Vaughan, H. Wallach, H. Daumé III, and K. Crawford. "Datasheets for Datasets." Communications of the ACM, 2021. arXiv:1803.09010.

[10] OpenSSF. "Supply-chain Levels for Software Artifacts (SLSA)." https://slsa.dev, 2023.

[11] Sigstore Project. "Sigstore: Software Signing for Everyone." https://sigstore.dev, 2022.

**TODO:** The benchmark leakage paragraph in Section 9 does not yet have a specific citation. A verified reference on LLM data contamination or evaluation benchmark leakage should be added before final arXiv submission.
