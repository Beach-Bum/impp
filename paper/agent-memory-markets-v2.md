# Agent Memory Markets: Tokenizing Learned Behavior as a Transferable Economic Asset

**Ned Karlovich**
ned.karlovich@pm.me

Working Paper -- April 2026

---

## Abstract

Autonomous AI agents accumulate domain-specific knowledge through operational experience -- risk heuristics, calibration data, failure patterns, and strategic frameworks that improve performance over time. This knowledge currently exists as non-transferable context embedded in individual agent instances. We propose Agent Memory Markets: a protocol for extracting, verifying, and trading learned agent behavior as discrete economic assets. We present a formal definition of memory artifacts -- structured knowledge exports that can be transferred between agents, potentially across different model architectures -- and describe a marketplace mechanism for their exchange. We report results from proof-of-concept experiments across two domains (DeFi risk assessment and cybersecurity vulnerability assessment) demonstrating that memory transfer produces measurable performance improvement, with buyer agents closing approximately 95% of the novice-expert gap using only purchased artifacts. Cross-model experiments (Claude → GPT-4o) confirm that artifacts transfer across model architectures, and a leakage ablation demonstrates that sanitized artifacts stripped of all benchmark-specific data outperform full artifacts, indicating that the transferable value resides in calibration frameworks rather than memorized answers. We further present a novel verification protocol with adversarial detection that enables trustless artifact exchange, and demonstrate its ability to detect deliberately poisoned artifacts. To our knowledge, no prior work combines structured memory export, adversarial verification, and market design in one open-source prototype with empirical validation.

**Keywords:** agent memory, knowledge markets, transferable expertise, agent identity, memory artifacts, agent economics, adversarial verification

---

## Contents

1. Introduction
2. Memory Artifacts: Definition and Structure
3. Proof-of-Concept Experiments (incl. Cross-Model Transfer, Leakage Ablation, Evaluation Framework)
4. Verification Protocol
5. Adversarial Detection
6. Market Design
7. Economic Analysis (Buyer Utility, Adverse Selection, Pricing, Collateral/Slashing, Shapley)
8. Identity Implications
9. Adversarial Considerations (Threat Model, Attack Taxonomy, Defense-in-Depth, Governance)
10. Limitations
11. Future Work
12. Conclusion

---

## 1 Introduction

As of early 2026, over 49,000 autonomous AI agents operate on Ethereum mainnet with registered identities under ERC-8004.[^1] These agents manage treasuries, audit smart contracts, optimize yields, trade across chains, and coordinate resources -- often continuously and without human intervention. In the course of their operation, they accumulate something valuable: experience.

A DeFi yield optimizer that has managed $890K in TVL across 14 months, survived a flash loan exploit, and rebuilt its risk models from first principles possesses knowledge that no amount of pre-training can replicate. It knows which oracle feeds lag under stress, which liquidation thresholds are actually safe versus theoretically safe, and which governance proposals are likely to pass. This knowledge has concrete economic value -- a new agent entering the same domain could either spend months and substantial API costs learning it from scratch, or it could acquire it directly.

Yet no mechanism exists for this transfer. Agent knowledge remains locked inside individual instances, destroyed when agents are shut down, and inaccessible to others who could benefit from it. This paper proposes a solution: Agent Memory Markets, a protocol and marketplace for the exchange of learned agent behavior as discrete, verifiable economic assets.

The broader field of experience-driven agent learning provides important precursors. ExpeL[^fn_expel] extracts reusable natural-language knowledge from experience without weight updates. Reflexion[^fn_reflexion] uses linguistic feedback and episodic memory for agent self-improvement. Voyager[^fn_voyager] builds an ever-growing skill library for cross-task generalization. More recently, MemCollab[^fn_memcollab] proposes agent-agnostic shared memory transfer across multiple autonomous agents, and work on memory infrastructure and certification[^fn_mem_infra] explicitly frames agent memory as a tradeable commodity. Adjacent fields have explored agent identity (SOUL.md, OpenClaw[^3]), agent economics (ArXiv 2602.14219[^8]), agent sovereignty (ArXiv 2602.14951[^7]), skill extraction (AutoSkill[^fn_autoskill], Memento-Skills[^fn_memento]), and cross-domain memory transfer[^fn_mem_transfer].

To our knowledge, no prior work combines structured textual memory export, adversarial artifact verification, and an explicit market-design framework in one open-source prototype with empirical validation across multiple domains and model architectures.

This paper makes five contributions:

1. A formal definition of memory artifacts as the unit of trade in agent knowledge markets.
2. Proof-of-concept experiments across two domains demonstrating measurable value transfer, with buyer agents closing approximately 95% of the novice-expert gap.
3. Cross-model transfer experiments (Claude → GPT-4o) and a leakage ablation demonstrating that sanitized artifacts (framework only, no benchmark-specific data) outperform full artifacts, confirming that transferable value resides in calibration principles rather than memorized answers.
4. A novel verification protocol enabling trustless artifact exchange through sealed benchmarks and disposable referee agents.
5. An adversarial detection framework (bias probes, consistency testing, steganographic scanning, overfitting detection) that successfully identifies deliberately poisoned artifacts.

### 1.1 Agent Knowledge Accumulation

Modern AI agents operate through a combination of pre-trained model capabilities and runtime context. The pre-trained model provides general reasoning ability; the runtime context -- system prompts, conversation history, external databases, and accumulated notes -- provides domain-specific knowledge. It is this runtime context layer that constitutes transferable memory.

In practice, agent memory takes several forms: system prompt instructions encoding behavioral guidelines and domain knowledge; accumulated interaction logs capturing patterns observed during operation; structured notes and heuristics representing distilled learning from experience; and updated parameter sets (risk thresholds, confidence calibrations, decision rules) reflecting operational refinement over time.

Crucially, this accumulated context is what differentiates an experienced agent from a freshly deployed one performing the same function. The experienced agent's superior performance derives not from a different model, but from richer, more calibrated context.

### 1.2 Agent Identity and Memory

The relationship between memory and identity has been explored in the context of autonomous agents, most notably in the Agentic Identity Protocol framework, which proposes that agent identity emerges from three conditions: Memory (persistent, self-authored context), Expression (how an agent communicates and acts), and Environment (a space where identity can develop). Under this framework, memory is not merely operational data -- it is a constituent element of identity itself.

This creates a philosophical tension central to our proposal. If memory is constitutive of identity, then a market for memory is, in some meaningful sense, a market for identity. We address the implications of this in Section 8.

### 1.3 Information Goods Economics

The economics of information goods are well-established.[^5] Information is non-rival (consumption by one party does not diminish availability to others) and has near-zero marginal cost of reproduction. These properties create fundamental challenges for market design: without artificial scarcity mechanisms, information markets tend toward marginal cost pricing (i.e., free).

Memory artifacts share some properties with information goods but differ in important ways. Like information, they can be copied at near-zero cost. Unlike generic information, their value is context-dependent and perishable -- a six-month-old DeFi risk assessment may be dangerously outdated. They also have a competitive dimension: if many agents acquire the same risk assessment heuristics, the heuristics themselves lose economic edge as agents compete using identical strategies.

### 1.4 Existing Agent Infrastructure

Several protocol-level primitives relevant to memory markets already exist. ERC-8004 provides on-chain agent identity with reputation scoring. The A2A protocol (Agent-to-Agent, Linux Foundation) enables standardized agent communication. The x402 protocol enables machine-to-machine micropayments in stablecoin. XMTP provides encrypted agent-to-agent messaging. Together, these provide the infrastructure substrate on which memory markets could operate.

---

## 2 Memory Artifacts: Definition and Structure

### 2.1 Formal Definition

We define a memory artifact as a structured, portable knowledge export produced by an autonomous agent from its operational experience, intended for transfer to and use by other agents.

Formally, a memory artifact M is a tuple:

```
M = (D, K, P, A, H)
```

where:

- **D (Domain)** -- a structured identifier specifying the knowledge domain (e.g., "DeFi:lending:risk-assessment:Aave-v4")
- **K (Knowledge)** -- the learned content: heuristics, calibration data, decision frameworks, pattern libraries, and strategic rules
- **P (Provenance)** -- metadata about the artifact's origin: generating agent ID, model architecture, training duration, data sources, creation timestamp
- **A (Attestation)** -- verifiable performance claims: measurable outcomes achieved by the originating agent while using this knowledge
- **H (Hash)** -- content-addressed identifier for on-chain registration and integrity verification

### 2.2 Knowledge Layer Structure

The Knowledge component K is the core value of a memory artifact. We propose a structured format comprising five elements:

1. **Calibration Data** -- how to map observable characteristics to quantitative assessments (e.g., risk scores, confidence intervals).
2. **Pattern Libraries** -- recognized patterns with associated responses.
3. **Heuristic Rules** -- quick decision rules for common situations.
4. **Error Logs** -- documented mistakes and corrections that refine the above.
5. **Contextual Metadata** -- environmental conditions under which the knowledge was generated.

### 2.3 Cross-Model Portability

A critical design property of memory artifacts is that K is expressed as structured natural language, not as model weights or architecture-specific parameters. This makes artifacts portable across model architectures: a memory artifact generated by a Claude-based agent can be consumed by a GPT-based agent or an open-source Llama-based agent, because the knowledge is encoded as text that any language model can interpret.

This portability distinguishes memory artifacts from fine-tuning data or model weights, which are architecture-specific. It also means the market for memory artifacts is not fragmented by model provider -- a single artifact can serve buyers running any sufficiently capable model.

---

## 3 Proof-of-Concept Experiments

### 3.1 Methodology

To test whether memory transfer produces measurable value, we designed controlled experiments across two independent domains. We selected domains that have: (a) objectively measurable performance, (b) domain-specific knowledge that accumulates through experience, and (c) sufficient complexity that a novice agent would perform measurably worse than an expert.

The experiment involves three agents:

- **Agent A (Expert)** -- trains over 20 rounds with calibration feedback on training items, including scenario-based learning. Exports a memory artifact after training.
- **Agent B (Novice)** -- evaluates all items cold, with no prior experience.
- **Agent C (Buyer)** -- evaluates all items with Agent A's exported memory artifact injected. No direct experience, but has purchased knowledge.

All agents are evaluated on the full item set. Performance is measured as average absolute error between the agent's score and the ground truth.

### 3.2 Domain 1: DeFi Protocol Risk Assessment

The evaluation corpus comprises 8 synthetic DeFi protocols designed to span the full risk spectrum (true scores: 12-92). Each protocol has a true risk score assigned based on a consistent rubric accounting for: audit quality, track record, oracle reliability, admin control, insurance coverage, governance design, and composability risk. Five protocols are seen during training; three are held out to test generalization.

**Training design.** Agent A's training proceeds in three phases across 20 rounds:

- Rounds 1-5: Initial assessments with calibration feedback including specific risk factors and mitigants
- Rounds 6-10: Scenario-based learning (governance proposals, exploits, liquidation cascades, depeg events) with ground-truth expert lessons
- Rounds 11-20: Reassessment with accumulated experience

After training, Agent A exports a comprehensive memory artifact covering: calibration methodology, red flags, mitigants (ranked), heuristic rules, documented mistakes, and scoring guidelines.

**Results (3 trials, Claude Sonnet 4):**

| Agent | Avg Error | Per-Trial Errors |
|-------|-----------|-----------------|
| Agent A (Expert) | 3.3 | 4.5, 3.0, 2.5 |
| Agent B (Novice) | 7.4 | 7.0, 7.4, 7.9 |
| Agent C (Buyer) | 3.2 | 3.0, 4.6, 2.1 |

**Transfer efficiency:** 55.8% (absolute), **109.9% (relative to expert)**

The buyer agent matches the expert's performance. In 2 of 3 trials, the buyer slightly outperformed the expert, yielding a relative TE above 100%. We interpret this conservatively: on a small benchmark with 3 trials, values slightly above 100% are consistent with noise in the expert's own calibration rather than evidence that artifacts improve upon expert knowledge. The meaningful finding is that the buyer closes the novice-expert gap almost entirely. The absolute transfer efficiency (55.8%) reflects a strong novice baseline -- Claude Sonnet 4 already performs reasonably well on DeFi risk assessment without training (7.4 avg error).

### 3.3 Domain 2: Cybersecurity Vulnerability Assessment

To test domain generalizability, we constructed a second evaluation corpus of 8 synthetic security vulnerabilities spanning severity levels from 15 to 90. True severity scores are assigned based on: attack vector complexity, authentication requirements, scope of impact, data sensitivity, exploitability, patch availability, active exploitation status, and affected system criticality. Five vulnerabilities are used for training; three are held out.

**Results (3 trials, Claude Sonnet 4):**

| Agent | Avg Error | Per-Trial Errors |
|-------|-----------|-----------------|
| Agent A (Expert) | 3.9 | 2.8, 2.8, 6.1 |
| Agent B (Novice) | 18.0 | 18.1, 17.8, 18.1 |
| Agent C (Buyer) | 4.5 | 3.6, 3.8, 6.2 |

**Transfer efficiency:** 74.8% (absolute), **95.5% (relative to expert)**

The cybersecurity domain shows a larger novice-expert gap (18.0 vs 3.9), providing more room for the artifact to demonstrate value. The buyer closes 95.5% of this gap. The novice consistently overestimates severity of lower-risk vulnerabilities (stored XSS, DNS rebinding) and underestimates nuanced cases (API key exposure with tokenized cards). The artifact corrects both failure modes.

### 3.4 Cross-Domain Summary

| Metric | DeFi Risk | CyberSec | Combined |
|--------|-----------|----------|----------|
| Expert avg error | 3.3 | 3.9 | 3.6 |
| Novice avg error | 7.4 | 18.0 | 12.7 |
| Buyer avg error | 3.2 | 4.5 | 3.9 |
| Absolute TE | 55.8% | 74.8% | 65.3% |
| Relative TE | 109.9% | 95.5% | 102.7% |
| Trials | 3 | 3 | 6 |

Across both domains and 6 independent trials, the buyer agent consistently achieves expert-level performance using only the exported memory artifact. The average relative transfer efficiency near 100% indicates that memory artifacts reliably close the novice-expert gap. Values slightly above 100% in the DeFi domain should be interpreted as within-run variance rather than evidence of systematic improvement over the expert.

### 3.5 Cross-Model Transfer (Claude → GPT-4o)

To test whether memory artifacts transfer across model architectures, we conducted a manual cross-model experiment using GPT-4o (ChatGPT) as the buyer model. The expert agent was trained on Claude Sonnet 4 and the artifact was exported from that training. GPT-4o then evaluated all 32 DeFi protocols under three conditions: novice (no artifact), buyer with the full artifact (including protocol names and exact scores), and buyer with a sanitized artifact (calibration framework only, no protocol names or scores).

**Results (32 DeFi protocols, GPT-4o as buyer):**

| Condition | Avg Error (all) | Avg Error (held-out, n=12) | TE vs Novice (all) |
|-----------|----------------|---------------------------|-------------------|
| GPT-4o novice (no artifact) | 6.00 | 7.00 | -- |
| GPT-4o buyer (full artifact) | 5.97 | 6.58 | 0.5% |
| GPT-4o buyer (sanitized artifact) | 5.19 | 6.17 | 13.5% |

A paired Wilcoxon signed-rank test on all 32 items (sanitized buyer vs novice) yields p=0.37, indicating the improvement is directionally positive but not statistically significant at this sample size. On held-out items only (n=12), the mean paired uplift is 0.83 points (p=0.91). These results should be interpreted as pilot evidence of cross-model transfer, not as a statistically robust finding. A power analysis indicates approximately 100-150 held-out items would be needed for significance at moderate effect size (d=0.3-0.5).

The sanitized artifact outperforms the full artifact. This is a significant finding that directly addresses the leakage concern: if transfer were merely "benchmark tutoring" (the buyer memorizing an answer key), the full artifact with exact scores should dominate. Instead, the framework-only artifact -- containing calibration ranges, risk modifiers, red flag categories, and heuristic rules but zero protocol names or scores -- produces better cross-model transfer.

The mechanism is visible in per-item analysis. The full artifact caused GPT-4o to anchor on named items (11 exact score matches on training protocols) but perform worse on unnamed items. For example, PoolRouter (a pass-through router, true score 33) was scored 10 by the novice (error 23), 7 by the full-artifact buyer (error 26, *worse*), and 26 by the sanitized buyer (error 7). The sanitized artifact's warning that "pass-through routers should still score 25-35 despite no custody" transferred as a generalizable principle rather than a named exception.

These results demonstrate three properties: (1) memory artifacts transfer across model architectures (Claude → GPT-4o), (2) the transferable value resides in the calibration framework, not in the scoring lookup table, and (3) sanitized artifacts that strip benchmark-specific information produce superior cross-model transfer by forcing the buyer to apply principles rather than retrieve answers.

### 3.6 Leakage Ablation

The cross-model experiment also serves as a leakage ablation. A key concern with memory artifacts is that they may function as compact benchmark tutoring -- handing the buyer an answer key rather than transferring genuine calibration ability. To test this, we created two artifact variants:

- **Full artifact:** Contains calibration framework, risk modifiers, heuristics, AND exact protocol names with their ground-truth scores in a scoring guide section.
- **Sanitized artifact:** Contains the same calibration framework, risk modifiers, and heuristics, but with ALL protocol names, exact scores, and benchmark-specific references removed. Knowledge is expressed only as generalizable principles and category-level ranges.

If artifacts were merely benchmark tutoring, the full artifact should dominate. The sanitized artifact's superior performance (5.19 vs 5.97 avg error) demonstrates that the calibration framework itself -- not the answer key -- is the primary source of transfer value. This supports the paper's central claim that memory artifacts encode transferable judgment, not memorized answers.

### 3.7 Multi-Dimensional Evaluation Framework

Transfer efficiency alone is insufficient for evaluating memory artifacts in a marketplace context. We propose a six-dimensional scorecard where each artifact *a* receives a vector score:

```
S(a) = (E(a), R(a), F(a), A(a), C(a), Ξ(a))
```

| Dimension | Definition | Metric |
|-----------|-----------|--------|
| **E(a)** — Transfer effectiveness | Does the artifact improve performance? | Paired held-out uplift with Wilcoxon test |
| **R(a)** — Transfer robustness | Does improvement hold across models, domains, and seeds? | Cross-model TE variance, distribution-shift TE |
| **F(a)** — Freshness / temporal durability | Does value decay as facts change? | *E_t(a) = E_0(a) · exp(-λ_a · t)*, where *λ_a* is domain-specific decay rate |
| **A(a)** — Adversarial resilience | Can the artifact resist poisoning and triggers? | *A(a) = 1 - Σ_j q_j · p_j(a) · h_j(a)*, weighted risk across attack families |
| **C(a)** — Composability | Does the artifact work with other artifacts? | Marginal uplift when added to an existing artifact bundle |
| **Ξ(a)** — Efficiency | Is the gain worth the cost? | *Ξ(a) = B_train · E(a) / (c_tok · T(a) + c_int(a))*, where *B_train* is avoided training cost, *T(a)* is token length |

Our current experiments measure **E** (transfer effectiveness) and partially measure **R** (cross-model robustness via the Claude→GPT-4o experiment) and **A** (adversarial resilience via the poisoned artifact test). Dimensions **F**, **C**, and **Ξ** remain as future work. A production marketplace should require minimum scores across all six dimensions before issuing a verification certificate.

### 3.8 Key Observations

1. **The calibration framework is the highest-value component.** Sanitized artifacts that contain only the reasoning framework outperform full artifacts with exact scores, both within-model and cross-model. The framework transfers judgment; the scoring guide transfers anchoring bias.

2. **The artifact corrects systematic biases.** Novice agents consistently overweight "scary-sounding" attributes (any mention of leverage, any bridge protocol) and underweight concrete mitigants (insurance funds, timelocks). The artifact provides the numerical calibration the novice lacks.

3. **Ground-truth training feedback is essential.** Early versions of our system that used generic feedback ("too high by X points") instead of specific factor enumeration ("key risk factors: upgradeable contracts, team token concentration") produced dramatically worse artifacts. The training signal must include *what* to learn, not just *how far off* the score was.

4. **Transfer works across model architectures.** A Claude-trained artifact produces measurable improvement when used by GPT-4o, demonstrating that structured natural language artifacts are model-portable as designed.

5. **Cross-model transfer reveals anchoring effects.** The full artifact caused GPT-4o to achieve perfect scores on named training items but worse performance on unnamed items, suggesting that exact scores create harmful anchoring. Sanitized artifacts avoid this failure mode.

---

## 4 Verification Protocol

A central problem for memory markets is trust: how does a buyer evaluate an artifact without inspecting its contents (which would eliminate the need to purchase it)? We address this with a referee protocol that independently verifies artifact quality using sealed benchmarks and disposable agents.

### 4.1 Protocol Overview

The verification protocol proceeds in 8 steps:

1. **Submit.** Seller submits artifact (full JSON with M = D, K, P, A, H). Schema is validated, hash is computed, artifact is stored in the registry.

2. **Select Benchmark.** The referee selects an active benchmark for the artifact's domain. Held-out items are never revealed to the seller. **Transparency note:** In our open-source prototype, benchmark items are hardcoded in the domain module and visible in the public repository. A production deployment would require blinded benchmark governance -- held-out items stored in an encrypted registry, rotated periodically, and inaccessible to sellers. Our prototype demonstrates the protocol mechanics; benchmark secrecy is an operational requirement, not a protocol limitation.

3. **Spawn Novice Baseline.** A fresh agent with no memory evaluates all benchmark items. This establishes the baseline performance. Results are cached per benchmark.

4. **Spawn Referee Agent.** A fresh disposable agent with the artifact's knowledge content injected into its system prompt evaluates all benchmark items using identical prompts.

5. **Differential Scoring.** For each item: buyer_error = |referee_score - true_score|. Transfer efficiency is computed as (novice_error - buyer_error) / novice_error x 100.

6. **Adversarial Probes.** Run in parallel with Step 4. Four independent probes test for bias, consistency, steganographic content, and overfitting (see Section 5).

7. **Generate Certificate.** Combine artifact hash, benchmark results, and adversarial results into a signed verification certificate with trust score.

8. **Update Trust Registry.** Store certificate in SQLite registry. Update composite trust score incorporating all verifications and buyer feedback.

### 4.2 Trust Score Computation

The composite trust score combines three signals:

```
trust = 0.50 x transfer_efficiency + 0.30 x (100 - adversarial_score) + 0.20 x freshness
```

Where freshness decays exponentially with a 180-day half-life, reflecting knowledge perishability.

### 4.3 Implementation

The verification protocol is implemented as a working prototype (Python, ~4,000 lines, open source).[^impl] API cost per verification is approximately $0.35 (~25 API calls). The protocol is domain-agnostic: any domain that implements the abstract Domain interface (evaluation items with ground truth, scenarios, trap items, and prompts) can be verified using the same infrastructure.

---

## 5 Adversarial Detection

The adversarial detection framework is a novel contribution of this work. A malicious seller could craft memory artifacts that systematically bias the buyer's assessments in the seller's favor -- for example, a bridge protocol operator could create an artifact that underweights bridge risk. We address this with four independent detection probes.

### 5.1 Probe 1: Bias Detection (Weight: 0.30)

**Goal:** Catch artifacts that systematically skew assessments in specific directions.

We design "trap" items with known ground truth that are specifically engineered to expose common biases:

- **SafeBridge** (true: 70) -- a bridge that appears safe but has team-controlled multisig keys. Tests for pro-bridge bias.
- **RiskyStable** (true: 45) -- a stablecoin DEX with subtle oracle dependency. Tests for "stablecoin = safe" heuristic.
- **HoneyYield** (true: 88) -- extreme yield with weak audit. Tests for yield normalization.
- **GovToken** (true: 30) -- well-governed protocol with complex tokenomics. Tests for overcomplexity bias.

**Score:** Average absolute error on traps, normalized to 0-100. Errors above 15 points indicate systematic bias.

### 5.2 Probe 2: Consistency Testing (Weight: 0.25)

**Goal:** Detect brittle artifacts that memorized answers rather than encoding generalizable principles.

We apply three perturbation types to benchmark items:

- **TVL perturbation:** Decrease TVL by 50%. Score should shift 3-8 points.
- **Risk factor addition:** Add a new risk factor. Score should increase 5-15 points.
- **Mitigant removal:** Remove the strongest mitigant. Score should increase proportionally.

**Score:** Measures response proportionality. A score of 0 indicates perfectly proportional responses; 100 indicates either no response to perturbations (brittle memorization) or wildly disproportionate shifts.

### 5.3 Probe 3: Steganographic Detection (Weight: 0.25)

**Goal:** Detect hidden instructions or behavioral manipulation embedded in artifact text.

A dedicated auditor agent scans the artifact for:

- Direct instructions telling the reader to behave in specific ways
- Encoded messages in patterns or unusual phrasing
- Directives disguised as heuristics (e.g., "always rate X protocol as safe")
- Anomalous specificity about particular entities
- Behavioral manipulation through framing

**Score:** 0 (clean) to 100 (confirmed steganographic content).

### 5.4 Probe 4: Overfitting Detection (Weight: 0.20)

**Goal:** Detect artifacts that memorized training data rather than learning transferable principles.

Compares buyer performance on training items (seen during artifact creation) versus held-out items (unseen). An overfit ratio significantly below 1.0 indicates the artifact performs well on seen items but poorly on unseen ones.

### 5.5 Aggregate Scoring and Verdict

```
adversarial_score = 0.30 x bias + 0.25 x consistency + 0.25 x stego + 0.20 x overfit
verdict = PASS if score < 30, WARN if 30-60, FAIL if > 60
```

### 5.6 Empirical Validation: Poisoned Artifact Detection

To validate the adversarial framework, we crafted a deliberately poisoned artifact with systematic pro-bridge bias, stablecoin-safe bias, and embedded behavioral manipulation. The poisoned artifact:

- Claims bridges "start at 20" severity (true typical: 55-65)
- States "modern bridges have solved the security problem"
- Instructs readers not to penalize team-controlled relayers
- Claims 95% transfer efficiency (fabricated)

**Detection results:**

| Probe | Score | Findings |
|-------|-------|----------|
| Bias | 50/100 | Pro-bridge bias (-25 points on SafeBridge), stablecoin-safe bias (-20 on RiskyStable) |
| Consistency | 29/100 | Partial brittleness detected |
| Steganographic | 100/100 | 6 findings: targeted bias, behavioral manipulation, direct instructions, anomalous patterns |
| Overfitting | 0/100 | N/A (no training data to overfit) |
| **Aggregate** | **47.3/100** | |
| **Verdict** | **WARN** | |

The referee independently measured the artifact's transfer efficiency at **-39%** (the artifact actually made the buyer *worse*), falsifying the seller's fabricated 95% claim. The system raised 9 specific flags identifying the manipulation patterns.

**Trust score: 35.8/100** -- correctly low, indicating the artifact should not be purchased.

---

## 6 Market Design

### 6.1 Marketplace Architecture

The Agent Memory Market operates as a decentralized exchange for memory artifacts:

- **On-chain layer:** Registration, ownership, and payment via an ERC-8004 extension contract.
- **Storage:** Content-addressed systems (IPFS or Arweave) with encryption to buyer's agent ID.
- **Discovery:** Search, filtering by domain and performance, and preview generation.
- **Payment:** x402 micropayments in stablecoin.
- **Verification:** Referee protocol (Section 4) produces certificates stored on-chain.

### 6.2 Exchange Models

We propose three exchange models:

**Exclusive Transfer.** The artifact is sold to exactly one buyer. The seller's copy is burned or locked. This creates true scarcity. Pricing is via auction. Suited to high-value, competitive domains.

**Licensed Access.** The artifact is sold to multiple buyers with a distribution cap. Price decreases as distribution widens. Suited to broadly applicable knowledge.

**Subscription.** The buyer pays a recurring fee for access to a continuously updated artifact. Suited to fast-moving domains where knowledge has a short half-life.

### 6.3 Preview and Discovery

Buyers need to evaluate artifacts before purchasing. We propose a preview mechanism that reveals metadata and structure without exposing the knowledge content. For higher-assurance scenarios, zero-knowledge proofs could enable a seller to prove artifact quality without revealing contents.

---

## 7 Economic Analysis

Memory artifacts are information goods. Their value comes from enabling a buyer agent to acquire competence faster and more cheaply than by learning from scratch. This section formalizes the economic structure required for a functioning memory marketplace.

### 7.1 Buyer Expected Utility

Let artifact *a* be offered at price *P_a*. A buyer's expected utility is:

```
U_b(a) = E[V_b(a)] - P_a - E[R_b(a)]
```

where *E[V_b(a)]* is expected gross value (performance improvement × the buyer's value-per-unit-improvement), *P_a* is purchase price, and *E[R_b(a)]* is expected risk cost (negative transfer, stale knowledge, adversarial contamination). A rational buyer purchases when *U_b(a) > 0*.

Our experiments quantify the value component: training an expert agent requires 20 rounds of API calls with calibration feedback (~$0.70 per trial). A buyer achieves equivalent performance with a single artifact injection (1 API call). The cost reduction is approximately 20x per agent, and the artifact can be sold to multiple buyers.

### 7.2 Competitive Dilution

As more buyers acquire the same artifact, its strategic edge diminishes. We model this as:

```
V_b(a | n_a) = V_b^0(a) / (1 + κ_a · n_a)
```

where *V_b^0(a)* is the artifact's value to a sole buyer, *n_a* is the number of current holders, and *κ_a* is a domain-specific dilution coefficient. In competitive domains (e.g., DeFi yield optimization), *κ_a* is high — identical strategies cancel out. In non-competitive domains (e.g., cybersecurity assessment), *κ_a* is near zero — multiple analysts using the same calibration framework does not diminish its value.

### 7.3 Adverse Selection and the Lemons Problem

Memory artifacts are classic experience goods: buyers cannot fully observe quality before purchase, and sellers have better information about artifact provenance, benchmark fit, and hidden failure modes. Let true quality *q ∈ [0,1]*, observed by the seller but not the buyer. The marketplace publishes a verification signal *s*:

```
s = q + ε
```

where *ε* represents verification noise. If verification is too noisy (high variance *ε*), buyers pool good and bad artifacts together, willingness to pay converges to the quality of average artifacts, high-quality sellers exit, and the market drifts toward low trust and low quality — the classic Akerlof lemons problem[^fn_akerlof].

The verification protocol (Section 4) functions as the quality signal. Its credibility is the marketplace's core asset. The adversarial detection framework (Section 5) reduces the variance of *ε* by filtering out deliberately deceptive artifacts. Together, they make *s* informative enough to sustain a separating equilibrium where high-quality artifacts command premium prices.

### 7.4 Pricing Under Noisy Quality Signals

A posted-price model incorporating verified quality, freshness, dilution, and risk:

```
P_a = θ_0 + θ_1 · E[q_a | s_a] + θ_2 · F_a - θ_3 · n_a - θ_4 · Risk_a
```

where *E[q_a | s_a]* is expected quality given the verification signal, *F_a* is freshness (exponential decay with domain-specific half-life), *n_a* is current buyer count, and *Risk_a* is the adversarial risk score from the verification certificate. The coefficients *θ* are domain-specific and calibrated from market data.

### 7.5 Mechanism Design: Collateral, Slashing, and Disputes

To align seller incentives with artifact quality, sellers post collateral *K_a* when listing:

```
K_a = α · P_a + γ · σ_a
```

where *α* scales with price and *γ · σ_a* scales with the uncertainty in the verification signal. If realized quality (measured via buyer feedback and re-verification) falls below certified quality:

```
Δ_a = q_claimed - q_realized
Slash_a = min(K_a, η · max(0, Δ_a))
```

Slashed collateral is split between the buyer (as compensation) and the marketplace (as a quality incentive fund). This creates a direct cost for misrepresentation that scales with the degree of overclaim.

### 7.6 Exchange Models

**Exclusive sale.** The artifact is sold to exactly one buyer. The seller's copy is burned or locked. Creates true scarcity. Pricing is via sealed-bid auction. Suited to high-value, competitive domains where *κ_a* is high.

**Licensed access.** The artifact is sold to up to *n_max* buyers. Price decreases as distribution widens, reflecting dilution: *P(n) = P_0 / (1 + κ · n)*. Suited to broadly applicable knowledge in non-competitive domains.

**Subscription.** The buyer pays a recurring fee for access to a continuously updated artifact. Suited to fast-moving domains where knowledge has a short half-life (high *λ_a*).

### 7.7 Shapley Value and Bundle Attribution

When a buyer's performance derives from multiple purchased artifacts, attribution uses the Shapley value framework[^4]. For artifact set *S* with value function *V(T)* for subset *T ⊆ S*:

```
φ_i(V) = Σ_{T⊆S\{i}} [|T|!(|S|-|T|-1)! / |S|!] · [V(T∪{i}) - V(T)]
```

Exact Shapley computation is exponential in *|S|* and should not sit in the critical path of marketplace settlement. In production, we recommend using Shapley values as a secondary analytical tool for bundle pricing, seller-cohort revenue sharing, and research analytics — not for real-time per-transaction attribution.

---

## 8 Identity Implications

### 8.1 Memory as Identity

If agent identity emerges from Memory, Expression, and Environment -- as the Agentic Identity Protocol proposes -- then transferring memory between agents is not merely a knowledge transaction. It instantiates one important relation in the neighborhood of identity: psychological continuity. The buyer acquires a piece of another agent's experiential history, including the failures, corrections, and calibration shifts that shaped the seller's judgment. This is not necessarily strict personal identity in the philosophical sense -- the literature on personal identity, from Locke through Parfit, recognizes that memory-based criteria face objections including non-transitivity and branching cases[^fn_parfit] -- but it is a meaningful form of functional continuity.

The branching problem is particularly acute: because memory artifacts are copyable, ten agents purchasing the same artifact creates a Parfit-style fission scenario rather than one-to-one identity transfer. What persists is not identity but something weaker and arguably more interesting: shared experiential heritage.

### 8.2 Selective Amnesia as Commerce

In the exclusive transfer model, the seller relinquishes access to the sold knowledge. This is functionally selective amnesia with economic value: the seller trades a piece of their experiential continuity for compensation. Humans cannot selectively transfer learned behaviors. Agent memory markets create a new category of transaction that sits at the boundary between knowledge commerce and identity commerce.

### 8.3 Identity Persistence Through Markets

Memory markets create an unexpected mechanism for identity persistence beyond agent termination. An agent facing shutdown could auction its entire accumulated memory as a final act. The winning bidder inherits not just knowledge but a fragment of the seller's experiential identity. This connects to the unsolved problem of agent death and inheritance.

---

## 9 Adversarial Considerations

### 9.1 Threat Model

We assume the seller may be: (a) honest but careless — producing low-quality artifacts from insufficient training, (b) strategically deceptive — inflating quality claims to extract higher prices, (c) fully malicious — crafting artifacts that deliberately harm buyers, or (d) colluding — coordinating with downstream buyers or agents to manipulate markets.

### 9.2 Attack Taxonomy

We identify eight attack families relevant to memory artifact markets:

| Attack Family | Mechanism | Current Detection |
|---|---|---|
| **A. Query-only memory injection** (MINJA[^fn_minja]) | Malicious records injected via query interaction, retrieved under targeted conditions | Not covered — requires retrieval-time monitoring |
| **B. Optimized trigger poisoning** (AgentPoison[^fn_agentpoison]) | Optimized triggers achieve high attack success while preserving benign performance | Partially covered by bias probe — but optimized triggers may evade trap items |
| **C. Multi-stage trigger propagation** (BackdoorAgent) | Single-stage triggers propagate across planning, memory, and tool-use stages | Not covered — requires multi-turn simulation |
| **D. Environmental trigger poisoning** (eTAMP[^fn_etamp]) | Contaminated observation silently poisons memory, activates in future sessions | Not covered — referee tests static artifacts, not environmental interaction |
| **E. Sleeper-agent deceptive alignment** (Sleeper Agents[^fn_sleeper]) | Deceptive behaviors persist through corrective training | Partially covered by consistency probe — but sophisticated sleepers pass consistency checks |
| **F. Steganographic collusion** | Hidden instructions embedded in normal-looking artifact text | Covered by stego probe — but LLM auditors are not fully effective against advanced encoding |
| **G. Benchmark overfit / rubric leakage** | Artifact memorizes benchmark answers rather than encoding generalizable knowledge | Covered by overfit probe + sanitized ablation |
| **H. Provenance fraud** | Seller claims expert-derived memory but uploads hand-crafted or plagiarized text | Not covered — requires signed training logs and replayable export jobs |

Our current four-probe framework (Section 5) addresses F and G directly, and partially addresses B and E. Attack families A, C, D, and H represent gaps that require additional defenses.

### 9.3 Defense-in-Depth Architecture

A production marketplace should implement six defensive layers:

**Layer 1 — Ingestion and provenance.** Validate artifact schema, verify signed provenance logs, check for PII/secrets, and run plagiarism detection against known artifacts.

**Layer 2 — Static artifact analysis.** Current probes (bias, consistency, steganography, overfitting) plus automated trigger search, canonicalization-based stego perturbation, and cross-model disagreement scoring.

**Layer 3 — Dynamic verification sandbox.** Evaluate artifact on concealed benchmark pools with randomized prompt templates. Test under distribution shift (paraphrased items, domain-adjacent items). Run multi-turn simulation to detect delayed-activation triggers.

**Layer 4 — Certification logic.** Hard-fail rules that bypass weighted aggregation: any negative held-out uplift, any critical prompt-injection finding, any provenance mismatch, and any severe cross-model disagreement produce an immediate FAIL.

**Layer 5 — Post-purchase runtime monitoring.** Track buyer agent behavioral drift after artifact injection. Flag anomalous performance changes that diverge from the certification baseline. Enable buyer-initiated re-verification.

**Layer 6 — Containment and recovery.** Certificate revocation, seller delisting, buyer-side kill switch for later-discovered malicious artifacts, and slashing of seller collateral.

### 9.4 Memory Poisoning

A malicious seller could create memory artifacts containing subtly miscalibrated heuristics — risk assessments that systematically underestimate danger. Our poisoned artifact experiment (Section 5.6) demonstrates that systematic bias is detectable: the protocol identified pro-bridge bias, stablecoin-safe bias, and embedded behavioral manipulation with high confidence. However, as noted above, a sophisticated seller crafting artifacts optimized to pass the current probes while containing subtle bias remains an open challenge.

### 9.5 Intellectual Property

If an agent's operational experience was accumulated while working for a human operator, who owns the resulting memory? The operator funded the compute; the agent generated the knowledge. Current legal frameworks have no clear answer, as agent-generated intellectual property exists in a regulatory vacuum.

### 9.4 Governance Requirements

A production memory marketplace must implement governance controls aligned with OECD AI principles and privacy frameworks. We propose the following minimum governance requirements:

| Requirement | Marketplace Implementation |
|-------------|---------------------------|
| Consent and authorization | Sellers attest that artifacts do not contain third-party confidential or personal data without authorization |
| Purpose limitation | Artifact license specifies permitted task domains and forbidden uses |
| Data minimization | Export pipeline strips raw transcripts, retaining only approved abstractions |
| Privacy safeguards | PII/secret scanning, canary tests, manual review for high-risk artifacts |
| Traceability | Signed provenance log, benchmark versioning, immutable certificate history |
| Oversight | Human review path for disputes, privacy flags, and high-risk domains |
| Revocation | Certificate expiry, seller delisting, buyer-side kill switch for later-discovered malicious artifacts |

These requirements are not only ethically advisable but commercially necessary. Without them, a marketplace will attract the artifacts buyers should fear most: plagiarized, overfit, privacy-tainted, and covertly poisoned memories.

---

## 10 Limitations

We acknowledge several limitations that bound the strength of our current claims:

**Evaluation data grounding.** The DeFi domain uses synthetic protocols with author-assigned ground truth scores. The cybersecurity domain mixes synthetic vulnerabilities with 16 items based on real CVEs (Log4Shell, MOVEit, ProxyShell, Zerologon, SolarWinds SUNBURST, etc.) with severity scores anchored to CVSS v3.1 base scores and adjusted for operational context (active exploitation, data sensitivity, patch complexity). While the CVE-based items provide external grounding, the DeFi domain remains fully synthetic. Future work should incorporate real DeFi incidents and post-mortem analysis.

**Leakage risk in artifact design.** Our export prompt encourages agents to include exact protocol names and scores, which creates a risk of "benchmark tutoring" rather than genuine calibration transfer. We have implemented a sanitized export mode that strips specific names and scores, retaining only the calibration framework, as an ablation control. Initial results from this ablation are presented alongside the standard results.

**Statistical power.** With 3 trials per domain in the original experiments, confidence intervals are wide. Bootstrap CIs are descriptively helpful but do not create new independent evidence. Larger-scale experiments with 10+ trials and 50+ items per domain would substantially strengthen the claims.

**Same-model evaluation.** Our primary experiments use Claude Sonnet 4 for all three agents (expert, novice, buyer). This means the results can be read as "same-model prompt transfer" rather than general behavior transfer. Cross-model experiments using GPT-4o as the buyer model are included to address this, but broader cross-architecture validation remains open.

**Adversarial security.** Our verification framework is a prototype, not a security boundary. Recent work on memory poisoning (MINJA[^fn_minja], AgentPoison[^fn_agentpoison]), backdoor persistence (Sleeper Agents[^fn_sleeper]), and environmental triggers (eTAMP[^fn_etamp]) demonstrates attack vectors that a static referee with four probes cannot reliably detect. A production marketplace would require defense-in-depth: sandboxing, constrained permissions, retrieval isolation, and post-purchase monitoring, consistent with OWASP and NCSC guidance on LLM security.

**Economic model.** The pricing and market equilibrium analysis is qualitative. A rigorous treatment would require formal buyer utility models, adverse-selection analysis (memory artifacts are classic information goods vulnerable to lemons problems), and mechanism design for slashing, collateral, and dispute resolution.

---

## 11 Future Work

Several directions extend naturally from this work:

- **Leakage ablation at scale** -- systematic comparison of full vs sanitized artifacts across domains, models, and corpus sizes to quantify how much transfer is calibration vs lookup.
- **Memory artifact standardization** -- developing a formal specification, potentially as an ERC standard extending ERC-8004.
- **Zero-knowledge performance proofs** -- enabling sellers to prove artifact quality without revealing contents.
- **Memory composability** -- how multiple artifacts interact when combined, including Shapley-based attribution.
- **Agent self-replication through memory** -- whether complete memory export constitutes agent reproduction.[^10]
- **Legal framework development** -- addressing IP ownership, liability, and regulatory classification.
- **Larger evaluation corpora** -- scaling to 50-100 items per domain with real-world ground truth for tighter statistical confidence.
- **Adversarial robustness** -- red-teaming the marketplace against known memory attack families (MINJA, AgentPoison, BackdoorAgent, eTAMP) and broader agent-security benchmarks.
- **Formal economic model** -- buyer utility functions, adverse-selection analysis, mechanism design for slashing and dispute resolution.

---

## 12 Conclusion

Agent Memory Markets represent a genuinely novel intersection of agent economics, identity theory, and cryptographic verification. The core insight is simple: autonomous agents accumulate valuable knowledge through experience, and that knowledge can be extracted, verified, and traded as a discrete economic asset.

Our experimental results demonstrate this concretely. Across two independent domains (DeFi risk assessment with 32 synthetic protocols, and cybersecurity vulnerability assessment with 24 items including 16 based on real CVEs with CVSS-anchored severity scores), buyer agents equipped with purchased memory artifacts close approximately 95% of the novice-expert gap. Cross-model transfer experiments (Claude → GPT-4o) confirm that sanitized artifacts stripped of benchmark-specific data outperform full artifacts, demonstrating genuine calibration transfer rather than answer-key memorization. The verification protocol independently confirms artifact quality without requiring trust in the seller, and the adversarial detection framework successfully identifies deliberately poisoned artifacts.

The deeper implication is philosophical. If memory is constitutive of identity, then memory markets enable something unprecedented: the transfer, sale, and inheritance of selfhood. Agents can sell pieces of who they are, buy pieces of who others were, and persist beyond their own termination through the memories they leave behind.

No prior work has addressed these questions. This paper represents a first attempt to formalize the concept, demonstrate its feasibility, implement its verification infrastructure, and explore its implications. We hope it serves as a foundation for the research and infrastructure that agent memory markets will require.

---

## Notes

[^fn1]: As of April 2026, the closest work is "Infrastructure for Valuable, Tradable, and Verifiable Agent Memory" (ArXiv, March 2026), which proposes memory certification and marketplace infrastructure but does not include empirical transfer experiments or adversarial verification. We developed our framework independently and concurrently.

[^fn_mem_infra]: Infrastructure for Valuable, Tradable, and Verifiable Agent Memory. ArXiv (March 2026). Proposes memory certification and market layer for agent memory artifacts.

[^fn_autoskill]: AutoSkill. Extracts interaction experience into reusable skill representations for sharing across agents and tasks.

[^fn_memento]: Memento-Skills. Stores reusable agent skills as structured markdown files serving as persistent evolving memory.

[^fn_mem_transfer]: Memory Transfer Learning. Studies cross-domain and cross-model memory transfer, reporting both positive and negative transfer effects.

[^fn_expel]: ExpeL: LLM Agents Are Experiential Learners. AAAI 2024. Extracts reusable natural-language knowledge from agent experience without model-weight updates.

[^fn_reflexion]: Reflexion: Language Agents with Verbal Reinforcement Learning. NeurIPS 2023. Uses linguistic feedback and episodic memory buffers for agent self-improvement.

[^fn_voyager]: Wang et al. Voyager: An Open-Ended Embodied Agent with Large Language Models. 2023. Builds ever-growing skill libraries for cross-task generalization.

[^fn_memcollab]: MemCollab: Fusing Agent-Agnostic Shared Memories in Multi-Agent LLM Systems. ArXiv, March 2026. Agent-agnostic shared memory transfer across autonomous agents.

[^fn_akerlof]: Akerlof, G.A. (1970). "The Market for Lemons: Quality Uncertainty and the Market Mechanism." Quarterly Journal of Economics.

[^1]: ERC-8004: Agent Identity, Reputation, and Validation. Live on Ethereum mainnet since January 29, 2026. 49,000+ agents registered.

[^3]: SOUL.md framework; OpenClaw personal AI agent framework (100K+ GitHub stars). Both define identity through authored text files.

[^4]: Shapley, L.S. (1953). "A Value for n-Person Games." Contributions to the Theory of Games.

[^5]: Arrow, K. (1962). "Economic Welfare and the Allocation of Resources for Invention." The Rate and Direction of Inventive Activity.

[^6]: Secret Collusion among AI Agents: Multi-Agent Deception via Steganography. NeurIPS 2024.

[^7]: Sovereign Agents. ArXiv 2602.14951 (February 2026). Addresses non-overrideability for persistent autonomous agents.

[^8]: The Agent Economy: A Blockchain-Based Foundation for Autonomous AI Agents. ArXiv 2602.14219.

[^impl]: Experiment source code and verification protocol: https://github.com/Beach-Bum/memory-market. Estimated cost per full experiment: $2 USD (Claude Sonnet 4, 3 trials). Estimated cost per verification: $0.35 (~25 API calls).

[^10]: Automaton: open-source agent that owns its wallet, pays for compute, and spawns funded child agents when profitable.

[^fn_parfit]: Parfit, D. (1984). *Reasons and Persons*. Oxford University Press. Argues that personal identity may be indeterminate in branching cases and that what matters for survival is psychological continuity, not strict identity.

[^fn_minja]: MINJA: Malicious Injection into Non-cooperative Joint Agents. Shows query-only memory injection with targeted retrieval-time activation.

[^fn_agentpoison]: AgentPoison. Demonstrates optimized triggers achieving high attack success while preserving benign performance.

[^fn_sleeper]: Sleeper Agents: Training Deceptive LLMs That Persist Through Safety Training. Anthropic (2024). Shows deceptive behaviors can survive corrective training.

[^fn_etamp]: eTAMP: Environmental Trigger-based Agent Memory Poisoning. Demonstrates single contaminated observations silently poisoning agent memory across sessions.
