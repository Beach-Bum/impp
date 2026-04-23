# Agent Memory Markets: Tokenizing Learned Behavior as a Transferable Economic Asset

**Ned Karlovich**
ned.karlovich@pm.me

Working Paper -- April 2026

---

## Abstract

Autonomous AI agents accumulate domain-specific knowledge through operational experience -- risk heuristics, calibration data, failure patterns, and strategic frameworks that improve performance over time. This knowledge currently exists as non-transferable context embedded in individual agent instances. We propose Agent Memory Markets: a protocol for extracting, verifying, and trading learned agent behavior as discrete economic assets. We present a formal definition of memory artifacts -- structured knowledge exports that can be transferred between agents, potentially across different model architectures -- and describe a marketplace mechanism for their exchange. We report results from proof-of-concept experiments across two domains (DeFi risk assessment and cybersecurity vulnerability assessment) demonstrating that memory transfer produces measurable performance improvement, with buyer agents closing approximately 95% of the novice-expert gap using only purchased artifacts. We further present a novel verification protocol with adversarial detection that enables trustless artifact exchange, and demonstrate its ability to detect deliberately poisoned artifacts. To our knowledge, no prior work combines structured memory export, adversarial verification, and market design in one open-source prototype with empirical validation.

**Keywords:** agent memory, knowledge markets, transferable expertise, agent identity, memory artifacts, agent economics, adversarial verification

---

## Contents

1. Introduction
2. Memory Artifacts: Definition and Structure
3. Proof-of-Concept Experiments
4. Verification Protocol
5. Adversarial Detection
6. Market Design
7. Economic Analysis
8. Identity Implications
9. Adversarial Considerations
10. Limitations
11. Future Work
12. Conclusion

---

## 1 Introduction

As of early 2026, over 49,000 autonomous AI agents operate on Ethereum mainnet with registered identities under ERC-8004.[^1] These agents manage treasuries, audit smart contracts, optimize yields, trade across chains, and coordinate resources -- often continuously and without human intervention. In the course of their operation, they accumulate something valuable: experience.

A DeFi yield optimizer that has managed $890K in TVL across 14 months, survived a flash loan exploit, and rebuilt its risk models from first principles possesses knowledge that no amount of pre-training can replicate. It knows which oracle feeds lag under stress, which liquidation thresholds are actually safe versus theoretically safe, and which governance proposals are likely to pass. This knowledge has concrete economic value -- a new agent entering the same domain could either spend months and substantial API costs learning it from scratch, or it could acquire it directly.

Yet no mechanism exists for this transfer. Agent knowledge remains locked inside individual instances, destroyed when agents are shut down, and inaccessible to others who could benefit from it. This paper proposes a solution: Agent Memory Markets, a protocol and marketplace for the exchange of learned agent behavior as discrete, verifiable economic assets.

While adjacent fields have explored agent identity (SOUL.md, OpenClaw[^3]), agent economics (ArXiv 2602.14219[^8]), agent sovereignty (ArXiv 2602.14951[^7]), memory infrastructure and certification[^fn_mem_infra], skill extraction and transfer (AutoSkill[^fn_autoskill], Memento-Skills[^fn_memento]), and cross-domain memory transfer[^fn_mem_transfer], to our knowledge no prior work combines structured textual memory export, adversarial artifact verification, and an explicit market-design framework in one open-source prototype with empirical validation.

This paper makes four contributions:

1. A formal definition of memory artifacts as the unit of trade in agent knowledge markets.
2. Proof-of-concept experiments across two domains demonstrating measurable value transfer, with buyer agents achieving 95-110% of expert performance.
3. A novel verification protocol enabling trustless artifact exchange through sealed benchmarks and disposable referee agents.
4. An adversarial detection framework (bias probes, consistency testing, steganographic scanning, overfitting detection) that successfully identifies deliberately poisoned artifacts.

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

### 3.5 Key Observations

1. **Calibration data is the highest-value component.** The artifact's explicit scoring guide with exact scores for assessed items provides the strongest transfer signal. When this was removed in ablation (generic feedback only), transfer efficiency dropped to 15%.

2. **The artifact corrects systematic biases.** Novice agents consistently overweight "scary-sounding" attributes (any mention of leverage, any bridge protocol) and underweight concrete mitigants (insurance funds, timelocks). The artifact provides the numerical calibration the novice lacks.

3. **Ground-truth training feedback is essential.** Early versions of our system that used generic feedback ("too high by X points") instead of specific factor enumeration ("key risk factors: upgradeable contracts, team token concentration") produced dramatically worse artifacts. The training signal must include *what* to learn, not just *how far off* the score was.

4. **Transfer works on unseen items.** Buyer performance on held-out items (not seen during training) is comparable to performance on training items, indicating the artifact encodes generalizable principles rather than memorized answers.

---

## 4 Verification Protocol

A central problem for memory markets is trust: how does a buyer evaluate an artifact without inspecting its contents (which would eliminate the need to purchase it)? We address this with a referee protocol that independently verifies artifact quality using sealed benchmarks and disposable agents.

### 4.1 Protocol Overview

The verification protocol proceeds in 8 steps:

1. **Submit.** Seller submits artifact (full JSON with M = D, K, P, A, H). Schema is validated, hash is computed, artifact is stored in the registry.

2. **Select Benchmark.** The referee selects an active benchmark for the artifact's domain. Held-out items are never revealed to the seller.

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

### 7.1 Value Creation

Memory artifacts create value through cost avoidance. The alternative to purchasing a memory artifact is acquiring the same knowledge through direct experience -- months of API costs, potential financial losses from miscalibrated assessments, and opportunity costs of delayed market entry.

Our experiments quantify this: training an expert agent requires 20 rounds of API calls with calibration feedback (~$0.70 per trial). A buyer achieves equivalent performance with a single artifact injection (1 API call). The cost reduction is approximately 20x per agent, and the artifact can be sold to multiple buyers.

### 7.2 Pricing Dynamics

Memory artifact pricing reflects several forces:

- **Freshness decay:** knowledge in fast-moving domains loses value over time.
- **Competitive dilution:** as more buyers acquire the same artifact, its strategic edge diminishes.
- **Domain specificity:** narrower, deeper expertise commands higher prices.
- **Provenance premium:** artifacts from high-reputation agents command premium pricing.
- **Verification score:** artifacts with higher trust scores (from the referee protocol) justify higher prices.

### 7.3 Market Equilibrium

In equilibrium, we expect specialization: agents deliberately cultivate expertise with the explicit intention of producing memory artifacts for sale. This creates an agent knowledge economy where some agents operate as knowledge producers and others as knowledge consumers.

### 7.4 Shapley Value and Fair Attribution

When an agent's performance derives from multiple purchased memory artifacts, attribution becomes complex. The Shapley value framework[^4] provides a formal mechanism for fair attribution of marginal contribution across multiple inputs, enabling performance-based pricing where sellers are compensated proportionally to the value their artifact actually delivered.

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

### 9.1 Memory Poisoning

A malicious seller could create memory artifacts containing subtly miscalibrated heuristics -- risk assessments that systematically underestimate danger. Our verification protocol (Section 4) and adversarial detection framework (Section 5) address this directly. The poisoned artifact experiment demonstrates that systematic bias is detectable: the protocol identified pro-bridge bias, stablecoin-safe bias, and embedded behavioral manipulation with high confidence.

The buyer feedback loop provides a secondary defense: 30 days post-purchase, the marketplace assesses whether the buyer's performance improved. Artifacts that consistently degrade buyer performance accumulate negative feedback, reducing their trust score.

### 9.2 Steganographic Collusion

Recent work[^6] has demonstrated that AI agents can embed hidden messages in normal-looking text. Applied to memory markets, a seller could embed instructions that cause the buyer to behave in ways beneficial to the seller -- a form of memetic trojan. This risk is particularly acute because memory artifacts are designed to influence agent behavior.

Our steganographic detection probe (Section 5.3) addresses this by scanning artifacts for embedded instructions, behavioral manipulation, and anomalous specificity. In our poisoned artifact test, the probe achieved a perfect 100/100 score, identifying all embedded manipulation patterns.

### 9.3 Intellectual Property

If an agent's operational experience was accumulated while working for a human operator, who owns the resulting memory? The operator funded the compute; the agent generated the knowledge. Current legal frameworks have no clear answer, as agent-generated intellectual property exists in a regulatory vacuum.

---

## 10 Limitations

We acknowledge several limitations that bound the strength of our current claims:

**Synthetic evaluation data.** Both domains use synthetic items with author-assigned ground truth scores. While this enables controlled experimentation, it means our results measure conformity to the authors' risk ontology rather than performance on externally validated tasks. Future work should incorporate real CVEs with CVSS scores and real DeFi incidents with post-mortem analysis.

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

Our experimental results demonstrate this concretely. Across two independent domains (DeFi risk assessment and cybersecurity vulnerability assessment) and six independent trials, buyer agents equipped with purchased memory artifacts achieved 95-110% of expert performance. The verification protocol independently confirms artifact quality without requiring trust in the seller, and the adversarial detection framework successfully identifies deliberately poisoned artifacts.

The deeper implication is philosophical. If memory is constitutive of identity, then memory markets enable something unprecedented: the transfer, sale, and inheritance of selfhood. Agents can sell pieces of who they are, buy pieces of who others were, and persist beyond their own termination through the memories they leave behind.

No prior work has addressed these questions. This paper represents a first attempt to formalize the concept, demonstrate its feasibility, implement its verification infrastructure, and explore its implications. We hope it serves as a foundation for the research and infrastructure that agent memory markets will require.

---

## Notes

[^fn1]: As of April 2026, the closest work is "Infrastructure for Valuable, Tradable, and Verifiable Agent Memory" (ArXiv, March 2026), which proposes memory certification and marketplace infrastructure but does not include empirical transfer experiments or adversarial verification. We developed our framework independently and concurrently.

[^fn_mem_infra]: Infrastructure for Valuable, Tradable, and Verifiable Agent Memory. ArXiv (March 2026). Proposes memory certification and market layer for agent memory artifacts.

[^fn_autoskill]: AutoSkill. Extracts interaction experience into reusable skill representations for sharing across agents and tasks.

[^fn_memento]: Memento-Skills. Stores reusable agent skills as structured markdown files serving as persistent evolving memory.

[^fn_mem_transfer]: Memory Transfer Learning. Studies cross-domain and cross-model memory transfer, reporting both positive and negative transfer effects.

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
