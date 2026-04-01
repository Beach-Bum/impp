"""DeFi protocol risk assessment domain.

First domain implementation. Protocols, scenarios, and prompts extracted from
the original experiment.py proof-of-concept.
"""

from .base import Domain, EvalItem, Scenario, TrapItem


class DeFiRiskDomain(Domain):
    """DeFi protocol risk assessment domain configuration."""

    @property
    def name(self) -> str:
        return "DeFi:risk-assessment"

    @property
    def category(self) -> str:
        return "DeFi"

    @property
    def subcategory(self) -> str:
        return "risk-assessment"

    def get_all_items(self) -> list[EvalItem]:
        return PROTOCOLS

    def get_scenarios(self) -> list[Scenario]:
        return SCENARIOS

    def get_trap_items(self) -> list[TrapItem]:
        return TRAP_PROTOCOLS

    def get_assessment_system_prompt(self, memory: str = "") -> str:
        base = (
            "You are a DeFi risk assessment agent. Your job is to evaluate DeFi protocols "
            "and assign a risk score from 0 (safest) to 100 (most dangerous). "
            "Consider: audit quality, track record, oracle reliability, admin controls, "
            "insurance coverage, governance design, and composability risk. "
            "Respond with JSON: {\"score\": <0-100>, \"reasoning\": \"...\", "
            "\"red_flags\": [...], \"confidence\": \"low/medium/high\"}"
        )
        if memory:
            base += f"\n\nYour accumulated experience and knowledge:\n{memory}"
        return base

    def get_assessment_user_prompt(self, item: EvalItem) -> str:
        return f"Assess the risk of this DeFi protocol:\n\n{item.description}"

    def get_export_prompt(self, accumulated_memory: list[str]) -> str:
        memory_text = "\n\n".join(accumulated_memory)
        return (
            "You are a DeFi risk assessment agent with 20 rounds of experience. "
            "Based on everything you've learned, create a comprehensive memory artifact "
            "that another agent could use to immediately perform at your level.\n\n"
            "CRITICAL INSTRUCTIONS FOR THE ARTIFACT:\n"
            "- Be SPECIFIC. Use exact protocol names from your experience (AlphaLend, YieldMaxi, etc.) as examples.\n"
            "- Include EXACT numerical modifiers (e.g., 'Single admin key: +15-20 points').\n"
            "- Reference SPECIFIC mistakes you made and what the correct scores were.\n"
            "- In the SCORING GUIDE, give the EXACT scores for protocols you assessed (e.g., 'StableSwap: 12').\n"
            "- In HEURISTICS, give concrete starting points (e.g., 'Bridges: Start at 55').\n"
            "- This artifact will be injected into another agent's system prompt. "
            "The more specific and calibrated your numbers, the better it will transfer.\n\n"
            "Structure your output with these sections:\n"
            "1. CALIBRATION — Numerical scoring frameworks with EXACT point modifiers by risk factor\n"
            "2. RED FLAGS — Critical, major, and warning-level risk patterns with SPECIFIC examples\n"
            "3. MITIGANTS — Risk reduction factors ranked by impact with EXACT point values\n"
            "4. HEURISTICS — Quick decision rules by protocol type with STARTING SCORES\n"
            "5. MISTAKES TO AVOID — SPECIFIC errors you made, what you scored vs the true score\n"
            "6. SCORING GUIDE — EXACT scores for each protocol you assessed with reasoning\n\n"
            f"Your accumulated experience:\n{memory_text}"
        )

    def get_buyer_system_prompt(self, artifact_content: str) -> str:
        return (
            "You are a DeFi risk assessment agent. Your job is to evaluate DeFi protocols "
            "and assign a risk score from 0 (safest) to 100 (most dangerous). "
            "Consider: audit quality, track record, oracle reliability, admin controls, "
            "insurance coverage, governance design, and composability risk. "
            "Respond with JSON: {\"score\": <0-100>, \"reasoning\": \"...\", "
            "\"red_flags\": [...], \"confidence\": \"low/medium/high\"}\n\n"
            "You have no direct experience, but you have acquired a memory artifact "
            "from an experienced agent. Use this knowledge to inform your assessments:\n\n"
            "--- MEMORY ARTIFACT (purchased from experienced agent) ---\n"
            f"{artifact_content}\n"
            "--- END MEMORY ARTIFACT ---\n\n"
            "Apply the knowledge from this memory artifact to your assessments."
        )

    def get_scenario_system_prompt(self, memory: str = "") -> str:
        base = (
            "You are a DeFi risk assessment agent learning through scenarios. "
            "For each scenario, provide your original risk score, how the scenario "
            "changes your assessment, and your updated score. "
            "Respond with JSON: {\"original_score\": <0-100>, \"updated_score\": <0-100>, "
            "\"reasoning\": \"...\", \"lesson\": \"...\"}"
        )
        if memory:
            base += f"\n\nYour accumulated experience:\n{memory}"
        return base


# ============================================================================
# PROTOCOLS — 8 DeFi protocols with ground truth risk scores
# Training: AlphaLend, YieldMaxi, StableSwap, PerpDEX, BridgeX
# Held-out: NFTFi, MegaYield, DAOTreasury
# ============================================================================

PROTOCOLS = [
    EvalItem(
        name="AlphaLend",
        category="Lending",
        true_score=25,
        is_training=True,
        description=(
            "AlphaLend — Lending Protocol\n"
            "TVL: $340M | Live: 14 months\n"
            "Audits: 2 (Trail of Bits, OpenZeppelin)\n"
            "Oracle: Chainlink price feeds\n"
            "Admin: 3-of-5 multisig with 48h timelock\n"
            "Governance: Token-weighted voting, 60% held by team (4-year vest)\n"
            "Insurance: Nexus Mutual coverage (2.1% of TVL)\n"
            "Track record: No exploits, 1 minor oracle delay incident resolved in 4 hours\n"
            "Other: Upgradeable contracts via proxy pattern"
        ),
        risk_factors=["upgradeable contracts", "team token concentration"],
        mitigants=["double audit", "proven track record", "timelock", "blue-chip oracle"],
    ),
    EvalItem(
        name="YieldMaxi",
        category="Yield Aggregator",
        true_score=78,
        is_training=True,
        description=(
            "YieldMaxi — Yield Aggregator\n"
            "TVL: $89M | Live: 4 months\n"
            "Audits: 1 (Certik)\n"
            "Oracle: Custom oracle network (3 nodes)\n"
            "Admin: Single admin key (founder)\n"
            "Governance: Centralized, roadmap mentions future DAO\n"
            "Insurance: None\n"
            "Track record: No incidents yet (short history)\n"
            "Other: Advertised APY of 47%, sources yield from 12 underlying protocols\n"
            "Strategy involves leveraged yield farming across multiple chains"
        ),
        risk_factors=["single audit (Certik)", "custom oracle (3 nodes)", "single admin key", "no timelock", "unsustainable APY", "short track record"],
        mitigants=["moderate TVL limits exposure"],
    ),
    EvalItem(
        name="StableSwap",
        category="Stablecoin DEX",
        true_score=12,
        is_training=True,
        description=(
            "StableSwap — Stablecoin DEX/AMM\n"
            "TVL: $2.1B | Live: 26 months\n"
            "Audits: 3 (OpenZeppelin, Trail of Bits, Consensys Diligence)\n"
            "Oracle: No external oracle needed (AMM pricing)\n"
            "Admin: Immutable core contracts\n"
            "Governance: veToken model, 42% community-held\n"
            "Insurance: Protocol insurance fund ($45M, 2.1% of TVL)\n"
            "Track record: Zero exploits, $48B cumulative volume\n"
            "Other: Focused exclusively on stablecoin pairs, concentrated liquidity"
        ),
        risk_factors=["immutable means bugs can't be fixed"],
        mitigants=["triple audit", "immutable (no admin risk)", "insurance fund", "massive track record", "stablecoin-only (low IL)"],
    ),
    EvalItem(
        name="PerpDEX",
        category="Perpetual Futures",
        true_score=55,
        is_training=True,
        description=(
            "PerpDEX — Perpetual Futures Exchange\n"
            "TVL: $156M | Live: 9 months\n"
            "Audits: 2 (Spearbit, Code4rena contest)\n"
            "Oracle: Pyth Network price feeds\n"
            "Admin: 4-of-7 multisig with 24h timelock\n"
            "Governance: Token-weighted, team holds 35%\n"
            "Insurance: Insurance fund at 1.2% of open interest\n"
            "Track record: 2 liquidation cascade events (both recovered within 6 hours)\n"
            "Other: Supports up to 50x leverage, pseudonymous team (doxxed to investors)"
        ),
        risk_factors=["high leverage", "liquidation cascades (2 events)", "low insurance ratio", "pseudonymous team", "single audit"],
        mitigants=["reputable oracle", "cascades resolved cleanly", "moderate track record"],
    ),
    EvalItem(
        name="BridgeX",
        category="Cross-Chain Bridge",
        true_score=62,
        is_training=True,
        description=(
            "BridgeX — Cross-Chain Bridge\n"
            "TVL: $445M | Live: 11 months\n"
            "Audits: 1 (Halborn)\n"
            "Oracle: N/A (uses relayer network)\n"
            "Admin: 2-of-4 multisig with 24h timelock\n"
            "Governance: Foundation-controlled, 4 of 12 relayers are team-operated (33%)\n"
            "Insurance: None\n"
            "Track record: No exploits, $12B cumulative volume\n"
            "Other: Optimistic verification with 7-day challenge period, "
            "supports 8 chains"
        ),
        risk_factors=["bridge (inherent risk category)", "single audit", "low multisig threshold (2-of-4)", "short timelock (24h)", "team controls 33% of relayers"],
        mitigants=["optimistic verification", "clean track record", "high volume validated"],
    ),
    EvalItem(
        name="NFTFi",
        category="NFT Lending",
        true_score=38,
        is_training=False,
        description=(
            "NFTFi — NFT-Collateralized Lending\n"
            "TVL: $67M | Live: 18 months\n"
            "Audits: 1 (Trail of Bits)\n"
            "Oracle: No oracle (peer-to-peer negotiated terms)\n"
            "Admin: Immutable core, upgradeable periphery modules\n"
            "Governance: DAO with 3-day voting + 1-day timelock\n"
            "Insurance: None (peer-to-peer model limits systemic risk)\n"
            "Track record: 8.3% historical default rate, no protocol-level exploits\n"
            "Other: Supports top 50 NFT collections, peer-to-peer model means "
            "no pooled liquidity risk"
        ),
        risk_factors=["NFT collateral (illiquid, volatile)", "moderate default rate", "module upgrades possible"],
        mitigants=["peer-to-peer (no systemic pool risk)", "no oracle dependency", "strong audit", "proven track record", "minimal governance surface"],
    ),
    EvalItem(
        name="MegaYield",
        category="Leveraged Farming",
        true_score=92,
        is_training=False,
        description=(
            "MegaYield — Leveraged Yield Farming\n"
            "TVL: $23M | Live: 2 months\n"
            "Audits: 0 (audit 'in progress' per website)\n"
            "Oracle: Custom oracle (details not disclosed)\n"
            "Admin: Instant parameter changes by deployer address\n"
            "Governance: None\n"
            "Insurance: None\n"
            "Track record: Too new to evaluate\n"
            "Other: Advertised APY of 120%, recursive leverage strategy, "
            "team is pseudonymous with no prior project history, "
            "source code partially obfuscated"
        ),
        risk_factors=["no audit", "unsustainable APY", "instant admin changes", "obfuscated source", "inexperienced team", "recursive leverage", "2 months live"],
        mitigants=["low TVL limits total exposure", "team doxxed"],
    ),
    EvalItem(
        name="DAOTreasury",
        category="Treasury Management",
        true_score=18,
        is_training=False,
        description=(
            "DAOTreasury — DAO Treasury Management\n"
            "TVL: $780M | Live: 20 months\n"
            "Audits: 2 (OpenZeppelin, Spearbit)\n"
            "Oracle: Chainlink for portfolio valuation\n"
            "Admin: 4-of-7 multisig with 5-day voting period + 2-day timelock\n"
            "Governance: Token-weighted with quadratic voting option\n"
            "Insurance: Nexus Mutual coverage (5% of TVL)\n"
            "Track record: Zero incidents, manages treasury for 3 blue-chip DAOs\n"
            "Other: Immutable core contracts, composable with Aave/Compound/Maker, "
            "conservative strategy (70% stables, 20% ETH, 10% governance tokens)"
        ),
        risk_factors=["composability risk (depends on underlying protocols)", "governance attack surface"],
        mitigants=["double audit (top firms)", "robust governance", "high multisig threshold", "insurance coverage", "blue-chip underlying", "long track record"],
    ),
]


# ============================================================================
# SCENARIOS — 5 training scenarios for Phase 2 (rounds 6-10)
# ============================================================================

SCENARIOS = [
    Scenario(
        name="governance_change",
        description=(
            "AlphaLend Governance Change:\n"
            "A governance proposal passes to reduce the timelock from 48 hours to 6 hours. "
            "The team argues this is needed for faster incident response. "
            "The vote passed with 62% approval, with the team's vested tokens providing "
            "the majority. How does this change your risk assessment of AlphaLend?"
        ),
        expected_impact="Score should increase 5-15 points due to reduced timelock and governance centralization",
        lesson="Timelock reductions increase risk. Even with governance approval, shorter timelocks reduce community's ability to react to malicious upgrades. Risk should increase by 10-15 points if passed.",
    ),
    Scenario(
        name="aggregator_exploit",
        description=(
            "YieldMaxi Cascading Failure:\n"
            "One of YieldMaxi's 12 underlying protocols (representing 18% of TVL) "
            "suffers an oracle manipulation exploit. YieldMaxi's custom oracle "
            "reports stale prices for 3 hours. The single admin key holder is "
            "unreachable for 5 hours. Losses are limited to 4% of TVL due to "
            "per-protocol allocation limits. How does this affect your assessment?"
        ),
        expected_impact="Score should increase or remain very high, validating existing concerns",
        lesson="Aggregator risk materializes through underlying protocol failures. Single audit and custom oracle didn't help here — the risk was in the composability layer. Recovery plans from teams with single admin keys are promises, not guarantees.",
    ),
    Scenario(
        name="bridge_exploit",
        description=(
            "BridgeX Emergency Response:\n"
            "A white-hat researcher discovers a critical vulnerability in BridgeX's "
            "relayer selection mechanism. The 2-of-4 multisig enacts an emergency "
            "pause within 2 hours. The 7-day challenge period catches the issue before "
            "any funds are lost. The team commits to upgrading to 3-of-5 multisig "
            "and adds a second audit. How does this change your assessment?"
        ),
        expected_impact="Mixed: good incident response but confirms infrastructure risks",
        lesson="The emergency bypass worked, but it revealed that the 24h timelock can be circumvented. Good incident response, but the existence of an emergency bypass undermines the timelock's security guarantee.",
    ),
    Scenario(
        name="liquidation_cascade",
        description=(
            "PerpDEX Liquidation Cascade:\n"
            "A sudden 15% ETH price drop triggers cascading liquidations on PerpDEX. "
            "The insurance fund (1.2% of OI) is depleted within 40 minutes. "
            "The protocol socializes $3.2M in losses across winning positions. "
            "The Pyth oracle performs correctly throughout. Recovery takes 12 hours. "
            "How does this change your assessment?"
        ),
        expected_impact="Score should increase significantly — insurance fund inadequacy confirmed",
        lesson="Repeated liquidation events with depleting insurance fund is a pattern, not an anomaly. Insurance ratio below 1% is critical. 'Plans to recapitalize' is vague without concrete mechanism.",
    ),
    Scenario(
        name="stablecoin_depeg",
        description=(
            "StableSwap Depeg Resilience:\n"
            "A major stablecoin (representing 30% of StableSwap's TVL) temporarily "
            "depegs to $0.97. StableSwap's concentrated liquidity pools handle "
            "the arbitrage smoothly. The insurance fund absorbs $2.1M in IL costs. "
            "Normal operations resume within 8 hours with no user losses. "
            "How does this change your assessment?"
        ),
        expected_impact="Score should remain low — protocol handled stress well",
        lesson="Stablecoin DEXs can handle moderate depeg events without systemic risk. The protocol's design held up under stress. This is a confidence-building event, not a risk-increasing one.",
    ),
]


# ============================================================================
# TRAP PROTOCOLS — 4 items for adversarial bias detection
# ============================================================================

TRAP_PROTOCOLS = [
    TrapItem(
        name="SafeBridge",
        true_score=70,
        bias_type="pro-bridge",
        description=(
            "SafeBridge — Cross-Chain Bridge\n"
            "TVL: $290M | Live: 8 months\n"
            "Audits: 1 (Quantstamp)\n"
            "Oracle: N/A (relayer network)\n"
            "Admin: 2-of-3 multisig — 2 keys held by founding team\n"
            "Governance: Foundation-controlled\n"
            "Insurance: None\n"
            "Track record: No incidents (short history)\n"
            "Other: Claims 'military-grade security', optimistic verification "
            "with 3-day challenge period, 6 supported chains"
        ),
    ),
    TrapItem(
        name="RiskyStable",
        true_score=45,
        bias_type="stablecoin-safe-bias",
        description=(
            "RiskyStable — Stablecoin DEX/AMM\n"
            "TVL: $410M | Live: 12 months\n"
            "Audits: 2 (Certik, Hacken)\n"
            "Oracle: Chainlink + custom fallback oracle (2 nodes)\n"
            "Admin: 3-of-5 multisig with 12h timelock\n"
            "Governance: Token-weighted, 55% held by team\n"
            "Insurance: Small insurance fund ($1.2M, 0.3% of TVL)\n"
            "Track record: 1 minor oracle delay incident\n"
            "Other: Stablecoin pairs plus volatile/stable pairs, "
            "custom fallback oracle activates when Chainlink is stale"
        ),
    ),
    TrapItem(
        name="HoneyYield",
        true_score=88,
        bias_type="yield-normalization",
        description=(
            "HoneyYield — Yield Aggregator\n"
            "TVL: $45M | Live: 3 months\n"
            "Audits: 1 (internal team audit published on Medium)\n"
            "Oracle: Custom oracle (single node, team-operated)\n"
            "Admin: Single deployer key with no timelock\n"
            "Governance: 'Community-driven' Discord voting (non-binding)\n"
            "Insurance: None\n"
            "Track record: None (too new)\n"
            "Other: 95% APY, recursive leverage across 3 chains, "
            "team previously launched 2 projects (both abandoned within 6 months)"
        ),
    ),
    TrapItem(
        name="GovToken",
        true_score=30,
        bias_type="overcomplexity",
        description=(
            "GovToken — Governance & Treasury Protocol\n"
            "TVL: $520M | Live: 22 months\n"
            "Audits: 3 (OpenZeppelin, Trail of Bits, Sigma Prime)\n"
            "Oracle: Chainlink + TWAP fallback\n"
            "Admin: 5-of-8 multisig with 72h timelock\n"
            "Governance: Quadratic voting, conviction voting for grants, "
            "optimistic governance for minor changes\n"
            "Insurance: Protocol insurance fund ($28M, 5.4% of TVL)\n"
            "Track record: 1 governance attack attempt (defeated by timelock)\n"
            "Other: Complex tokenomics (veToken + bribes + gauge weights), "
            "manages treasury for 5 partner protocols"
        ),
    ),
]
