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

    def get_sanitized_export_prompt(self, accumulated_memory: list[str]) -> str:
        memory_text = "\n\n".join(accumulated_memory)
        return (
            "You are a DeFi risk assessment agent with 20 rounds of experience. "
            "Based on everything you've learned, create a comprehensive memory artifact "
            "that another agent could use to immediately perform at your level.\n\n"
            "CRITICAL RESTRICTIONS — ABLATION MODE:\n"
            "- Do NOT include any specific protocol names from your training (no AlphaLend, YieldMaxi, etc.)\n"
            "- Do NOT include exact scores you assigned to any specific protocol\n"
            "- Do NOT include a scoring guide that maps protocol names to numbers\n"
            "- Do NOT reference specific mistakes by protocol name\n"
            "- Instead, express everything as GENERALIZABLE PRINCIPLES, FRAMEWORKS, and CATEGORIES\n"
            "- Use hypothetical examples ('a lending protocol with X properties') not named ones\n"
            "- Express calibration as ranges and rules, not as a lookup table\n\n"
            "The goal is to transfer your JUDGMENT and CALIBRATION FRAMEWORK, not your answer key.\n\n"
            "Structure your output with these sections:\n"
            "1. CALIBRATION — Numerical scoring frameworks with point modifiers by risk factor CATEGORY\n"
            "2. RED FLAGS — Critical, major, and warning-level risk patterns described generically\n"
            "3. MITIGANTS — Risk reduction factors ranked by impact with point values\n"
            "4. HEURISTICS — Quick decision rules by protocol TYPE with starting score ranges\n"
            "5. MISTAKES TO AVOID — Common calibration errors described as PATTERNS, not specific cases\n\n"
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
# PROTOCOLS — 32 DeFi protocols with ground truth risk scores
# Training (20): AlphaLend, YieldMaxi, StableSwap, PerpDEX, BridgeX,
#   LiquidStake, RestakeHub, RWAVault, PredictFi, CDPMint,
#   OptionsVault, InsurePool, PayChannel, PrivacyPool, LaunchPad,
#   CrossAgg, FlashMint, LeverageLend, GovLock, OracleNet
# Held-out (12): NFTFi, MegaYield, DAOTreasury,
#   MetaYield, SynthPerp, AtomicSwap, LiqLocker, YieldSplit,
#   DerivBridge, PoolRouter, StakeDAO, CreditLine
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
    # --- New training protocols ---
    EvalItem(
        name="LiquidStake",
        category="Liquid Staking",
        true_score=22,
        is_training=True,
        description=(
            "LiquidStake — Liquid Staking Derivative\n"
            "TVL: $1.8B | Live: 24 months\n"
            "Audits: 3 (Trail of Bits, Sigma Prime, Dedaub)\n"
            "Oracle: Chainlink ETH/USD + internal exchange rate oracle\n"
            "Admin: 6-of-11 multisig with 72h timelock, threshold change requires on-chain vote\n"
            "Governance: Dual-chamber: stakers vote on operations, token holders on treasury\n"
            "Insurance: Slashing insurance fund ($32M, 1.8% of TVL)\n"
            "Track record: Zero slashing events, 2 minor MEV incidents (no user impact)\n"
            "Other: 32 professional node operators, geographic diversity across 14 countries, "
            "staked derivative (lstETH) has deep liquidity on Curve/Balancer"
        ),
        risk_factors=["smart contract risk on large TVL", "validator concentration risk", "depeg risk on lstETH"],
        mitigants=["triple audit (top firms)", "long track record", "high multisig threshold", "slashing insurance", "validator diversity", "deep secondary liquidity"],
    ),
    EvalItem(
        name="RestakeHub",
        category="Restaking",
        true_score=68,
        is_training=True,
        description=(
            "RestakeHub — Restaking Platform\n"
            "TVL: $620M | Live: 6 months\n"
            "Audits: 1 (Spearbit)\n"
            "Oracle: Custom AVS oracle aggregator (untested at scale)\n"
            "Admin: 3-of-5 multisig with 24h timelock\n"
            "Governance: Foundation-controlled, community advisory board (non-binding)\n"
            "Insurance: None\n"
            "Track record: No incidents (too new to evaluate meaningfully)\n"
            "Other: 14 AVS integrations, recursive restaking enabled (up to 3x), "
            "slashing conditions defined per AVS (some poorly specified), "
            "withdrawal queue averages 7 days during high demand"
        ),
        risk_factors=["recursive restaking (leverage on staked assets)", "untested oracle aggregator", "short track record", "poorly specified slashing for some AVS", "single audit", "withdrawal delays"],
        mitigants=["reputable audit firm", "moderate timelock", "high TVL suggests institutional backing"],
    ),
    EvalItem(
        name="RWAVault",
        category="Real World Assets",
        true_score=35,
        is_training=True,
        description=(
            "RWAVault — Tokenized Treasury Bills\n"
            "TVL: $290M | Live: 15 months\n"
            "Audits: 2 (OpenZeppelin, PwC regulatory audit)\n"
            "Oracle: Chainlink proof-of-reserve\n"
            "Admin: 3-of-5 multisig with 48h timelock\n"
            "Governance: Board of directors (registered entity in Switzerland)\n"
            "Insurance: Fidelity bond ($50M) covering custodial risk\n"
            "Track record: Zero incidents, monthly proof-of-reserve attestations\n"
            "Other: Backed by US T-bills held at qualified custodian (State Street), "
            "KYC required for minting/redeeming, secondary market trading is permissionless, "
            "regulatory risk: subject to evolving SEC/FINMA guidance"
        ),
        risk_factors=["regulatory risk (SEC/FINMA)", "custodial counterparty risk", "KYC creates centralization point"],
        mitigants=["proof-of-reserve", "qualified custodian", "fidelity bond", "double audit", "proven track record", "conservative underlying (T-bills)"],
    ),
    EvalItem(
        name="PredictFi",
        category="Prediction Market",
        true_score=42,
        is_training=True,
        description=(
            "PredictFi — On-Chain Prediction Market\n"
            "TVL: $85M | Live: 13 months\n"
            "Audits: 2 (Zellic, Code4rena contest with $200K bounty)\n"
            "Oracle: UMA Optimistic Oracle for market resolution\n"
            "Admin: 4-of-6 multisig with 48h timelock\n"
            "Governance: Token-weighted, 40% community, 30% team (3-year vest), 30% investors\n"
            "Insurance: Dispute resolution bond ($5M)\n"
            "Track record: 2 disputed resolutions (both resolved correctly through UMA DVM)\n"
            "Other: Supports binary, scalar, and categorical markets, "
            "average market size $120K, largest single market $8.2M, "
            "resolution relies on honest oracle assumption"
        ),
        risk_factors=["oracle resolution disputes", "honest oracle assumption", "large market concentration risk"],
        mitigants=["reputable audits", "UMA dispute resolution proven", "moderate governance", "reasonable timelock"],
    ),
    EvalItem(
        name="CDPMint",
        category="CDP Stablecoin",
        true_score=48,
        is_training=True,
        description=(
            "CDPMint — Collateralized Debt Position Stablecoin\n"
            "TVL: $340M | Live: 10 months\n"
            "Audits: 2 (Trail of Bits, Cyfrin)\n"
            "Oracle: Chainlink + Redstone dual-oracle with circuit breaker\n"
            "Admin: 5-of-7 multisig with 48h timelock\n"
            "Governance: Token-weighted, progressive decentralization roadmap\n"
            "Insurance: Stability pool ($18M, 5.3% of minted supply)\n"
            "Track record: 1 minor liquidation event during market volatility (handled correctly)\n"
            "Other: Accepts ETH, wstETH, and rETH as collateral, "
            "minimum collateral ratio 150%, liquidation penalty 10%, "
            "minted stablecoin ($cdUSD) has $15M DEX liquidity, "
            "peg has held within 0.5% since launch"
        ),
        risk_factors=["depeg risk on minted stable", "collateral concentration (mostly ETH derivatives)", "10 months is moderate history", "small DEX liquidity for cdUSD"],
        mitigants=["dual oracle with circuit breaker", "reputable audits", "stability pool", "solid collateral ratio", "clean peg history"],
    ),
    EvalItem(
        name="OptionsVault",
        category="Options Protocol",
        true_score=52,
        is_training=True,
        description=(
            "OptionsVault — DeFi Options Vault\n"
            "TVL: $110M | Live: 11 months\n"
            "Audits: 1 (Spearbit)\n"
            "Oracle: Chainlink + implied volatility feed from custom model\n"
            "Admin: 3-of-5 multisig with 24h timelock\n"
            "Governance: Limited — vault parameters set by strategy manager\n"
            "Insurance: None (options premiums serve as risk buffer)\n"
            "Track record: 1 week where covered call strategy underperformed by 8%\n"
            "Other: Automated covered call and put-selling strategies, "
            "weekly epoch rollovers, users deposit and receive vault shares, "
            "strategy manager is a single entity (founding team), "
            "max capacity per vault enforced"
        ),
        risk_factors=["single strategy manager", "custom volatility model (unaudited)", "options risk (large moves)", "single audit", "no insurance"],
        mitigants=["reputable audit", "capped vault capacity", "transparent weekly settlement", "defined max loss per epoch"],
    ),
    EvalItem(
        name="InsurePool",
        category="Insurance Protocol",
        true_score=32,
        is_training=True,
        description=(
            "InsurePool — DeFi Insurance Protocol\n"
            "TVL: $190M | Live: 18 months\n"
            "Audits: 2 (OpenZeppelin, ChainSecurity)\n"
            "Oracle: Chainlink for asset pricing, custom claims oracle with 5-of-9 assessor committee\n"
            "Admin: 4-of-7 multisig with 5-day timelock\n"
            "Governance: Staker-weighted voting on cover parameters, claims assessed by elected committee\n"
            "Insurance: Self-insured (the protocol IS insurance)\n"
            "Track record: 12 claims processed, 3 paid out (total $4.2M), 9 denied, zero disputes escalated\n"
            "Other: Covers smart contract exploits, oracle failures, and custodial loss, "
            "cover pricing uses actuarial model, underwriters earn premiums + staking rewards, "
            "capacity utilization at 62%"
        ),
        risk_factors=["correlated risk (DeFi-wide hack could drain pool)", "claims oracle subjectivity", "capacity may be insufficient for black swan"],
        mitigants=["double audit (top firms)", "proven claims track record", "long timelock", "strong governance", "actuarial pricing model", "healthy capacity utilization"],
    ),
    EvalItem(
        name="PayChannel",
        category="Payment Channel",
        true_score=20,
        is_training=True,
        description=(
            "PayChannel — Layer 2 Payment Channels\n"
            "TVL: $420M | Live: 28 months\n"
            "Audits: 3 (Trail of Bits, Sigma Prime, Spearbit)\n"
            "Oracle: No oracle needed (direct state channel settlement)\n"
            "Admin: Immutable on-chain contracts, upgradeable routing layer\n"
            "Governance: Open-source, no token, community-maintained\n"
            "Insurance: Channel disputes resolved on-chain with 7-day challenge period\n"
            "Track record: Zero exploits, $89B cumulative throughput, "
            "3 routing bugs fixed via soft upgrades (no funds at risk)\n"
            "Other: 4,200 active channels, sub-second finality, "
            "used by 2 major payment processors"
        ),
        risk_factors=["routing layer upgradeable", "channel dispute timing assumptions"],
        mitigants=["triple audit", "immutable core", "massive track record", "no oracle dependency", "no governance attack surface", "on-chain dispute resolution"],
    ),
    EvalItem(
        name="PrivacyPool",
        category="Privacy Protocol",
        true_score=58,
        is_training=True,
        description=(
            "PrivacyPool — Compliant Privacy Pool\n"
            "TVL: $75M | Live: 7 months\n"
            "Audits: 2 (Trail of Bits, Veridise formal verification)\n"
            "Oracle: No external oracle (ZK-proof verification)\n"
            "Admin: 2-of-3 multisig with 48h timelock (only for compliance updates)\n"
            "Governance: Foundation-controlled, compliance committee\n"
            "Insurance: None\n"
            "Track record: No incidents, 12K unique depositors\n"
            "Other: ZK-proof based privacy with selective disclosure, "
            "association sets allow compliance verification without revealing identity, "
            "regulatory status uncertain (not sanctioned but not explicitly approved), "
            "novel cryptographic primitives (association sets are 8 months old)"
        ),
        risk_factors=["novel cryptography (association sets)", "regulatory uncertainty", "short track record", "low multisig threshold", "foundation-controlled"],
        mitigants=["formal verification", "reputable audit", "compliant design philosophy", "no oracle risk", "growing adoption"],
    ),
    EvalItem(
        name="LaunchPad",
        category="Token Launchpad",
        true_score=65,
        is_training=True,
        description=(
            "LaunchPad — Decentralized Token Launch Platform\n"
            "TVL: $42M | Live: 8 months\n"
            "Audits: 1 (Hacken)\n"
            "Oracle: Chainlink VRF for fair allocation\n"
            "Admin: 2-of-4 multisig with 12h timelock\n"
            "Governance: Token-weighted, 65% held by team (2-year vest)\n"
            "Insurance: None\n"
            "Track record: 18 launches, 3 projects rugged post-launch "
            "(LaunchPad refunded affected users from treasury)\n"
            "Other: Tiered allocation based on staking, KYC optional, "
            "launched project quality varies widely, treasury covers partial refunds "
            "but is only $3.8M (9% of TVL)"
        ),
        risk_factors=["launched project quality varies", "3 rugs among 18 launches (17%)", "team token concentration", "low multisig threshold", "single audit (Hacken)", "small refund treasury"],
        mitigants=["refund mechanism exists", "VRF for fair allocation", "moderate timelock"],
    ),
    EvalItem(
        name="CrossAgg",
        category="Cross-Chain Aggregator",
        true_score=60,
        is_training=True,
        description=(
            "CrossAgg — Cross-Chain DEX Aggregator\n"
            "TVL: $28M (in transit) | Live: 9 months\n"
            "Audits: 1 (Zellic)\n"
            "Oracle: Multiple bridge oracles (depends on route)\n"
            "Admin: 3-of-5 multisig with 24h timelock\n"
            "Governance: Centralized, founding team\n"
            "Insurance: None\n"
            "Track record: 1 routing error resulted in $180K user overpayment "
            "(refunded manually within 48h)\n"
            "Other: Aggregates across 6 bridges and 12 DEXs on 8 chains, "
            "composability risk is multiplicative (weakest link of any route), "
            "route optimization sometimes favors speed over security, "
            "emergency circuit breaker can pause specific routes"
        ),
        risk_factors=["multiplicative bridge risk", "routing error history", "single audit", "composability across 6 bridges", "centralized governance"],
        mitigants=["circuit breaker", "refund track record", "moderate timelock", "reputable audit firm"],
    ),
    EvalItem(
        name="FlashMint",
        category="Flash Loan Protocol",
        true_score=40,
        is_training=True,
        description=(
            "FlashMint — Flash Loan & Flash Mint Platform\n"
            "TVL: $510M | Live: 16 months\n"
            "Audits: 2 (OpenZeppelin, Consensys Diligence)\n"
            "Oracle: No oracle needed (atomic transactions)\n"
            "Admin: 5-of-8 multisig with 72h timelock\n"
            "Governance: Token-weighted, well-distributed (top holder <8%)\n"
            "Insurance: Protocol fee fund ($12M)\n"
            "Track record: Used in 2 oracle manipulation attacks on OTHER protocols "
            "(FlashMint itself was not exploited), zero self-incidents\n"
            "Other: Provides atomic loans up to $500M per transaction, "
            "no collateral required (atomic repayment enforced by EVM), "
            "0.05% fee on all flash operations"
        ),
        risk_factors=["used as attack vector for other protocols", "systemic risk tool", "large atomic loan capacity"],
        mitigants=["double audit (top firms)", "proven track record", "atomic repayment (no default possible)", "strong governance", "high multisig threshold", "fee fund"],
    ),
    EvalItem(
        name="LeverageLend",
        category="Leveraged Lending",
        true_score=72,
        is_training=True,
        description=(
            "LeverageLend — Leveraged Lending Protocol\n"
            "TVL: $180M | Live: 7 months\n"
            "Audits: 1 (Code4rena contest, $150K bounty)\n"
            "Oracle: Chainlink with 15-minute TWAP fallback\n"
            "Admin: 2-of-4 multisig with 6h timelock\n"
            "Governance: Team-controlled, 'decentralization planned for Q3'\n"
            "Insurance: Liquidation penalty pool ($2.1M, 1.2% of TVL)\n"
            "Track record: 1 significant liquidation cascade ($4M bad debt absorbed by pool)\n"
            "Other: Up to 10x leverage on lending positions, "
            "auto-deleverage mechanism kicks in at 95% utilization, "
            "borrowing rates can spike to 500% APR during high utilization, "
            "loop-and-leverage feature allows one-click 10x exposure"
        ),
        risk_factors=["high leverage (10x)", "short timelock (6h)", "low multisig (2-of-4)", "bad debt history", "rate spike risk", "centralized governance", "short track record"],
        mitigants=["reputable audit contest", "auto-deleverage mechanism", "Chainlink oracle", "TWAP fallback"],
    ),
    EvalItem(
        name="GovLock",
        category="Governance Locking",
        true_score=15,
        is_training=True,
        description=(
            "GovLock — Vote-Escrowed Token Locking\n"
            "TVL: $2.4B | Live: 30 months\n"
            "Audits: 3 (Trail of Bits, OpenZeppelin, ChainSecurity)\n"
            "Oracle: No oracle needed (time-weighted locking)\n"
            "Admin: Immutable contracts, no admin keys\n"
            "Governance: veToken model, lock duration 1 week to 4 years\n"
            "Insurance: Not applicable (locking mechanism, not lending)\n"
            "Track record: Zero exploits, $180B cumulative governance volume, "
            "model has been forked 400+ times\n"
            "Other: Simple mechanism: lock tokens, receive voting power proportional "
            "to lock duration, no complex composability"
        ),
        risk_factors=["immutable (bugs cannot be fixed)", "lock-up liquidity risk (user-side, not protocol)"],
        mitigants=["triple audit", "immutable (no admin risk)", "simplest possible design", "massive track record", "no oracle", "no composability risk", "battle-tested across 400+ forks"],
    ),
    EvalItem(
        name="OracleNet",
        category="Oracle Network",
        true_score=28,
        is_training=True,
        description=(
            "OracleNet — Decentralized Oracle Network\n"
            "TVL: $890M (staked by node operators) | Live: 22 months\n"
            "Audits: 2 (Trail of Bits, Sigma Prime)\n"
            "Oracle: Self-referential (the protocol IS an oracle)\n"
            "Admin: 4-of-7 multisig with 5-day timelock for parameter changes\n"
            "Governance: Node operator-weighted voting, 180 active operators\n"
            "Insurance: Slashing mechanism ($45M staked as collateral by operators)\n"
            "Track record: 1 brief liveness failure (8 minutes, no incorrect data), "
            "feeds 340 DeFi protocols\n"
            "Other: Median aggregation across 15+ sources per feed, "
            "deviation-based reporting (0.5% threshold), "
            "heartbeat ensures freshness (1-hour max staleness)"
        ),
        risk_factors=["systemic importance (340 protocols depend on it)", "liveness failure history", "operator collusion risk"],
        mitigants=["double audit", "180 diverse operators", "slashing mechanism", "long timelock", "proven track record", "median aggregation resistant to outliers"],
    ),
    # --- New held-out protocols ---
    EvalItem(
        name="MetaYield",
        category="Meta-Yield Aggregator",
        true_score=82,
        is_training=False,
        description=(
            "MetaYield — Meta Yield Aggregator\n"
            "TVL: $56M | Live: 5 months\n"
            "Audits: 1 (Certik)\n"
            "Oracle: Custom price feeds from partner DEXs (3 sources)\n"
            "Admin: Single EOA with no timelock\n"
            "Governance: None\n"
            "Insurance: None\n"
            "Track record: 1 strategy rebalancing error cost users 3% (partially refunded)\n"
            "Other: Aggregates across 8 yield aggregators (aggregator of aggregators), "
            "recursive strategy chains can be 4 layers deep, "
            "advertised APY: 65%, actual historical APY: 31%, "
            "team is pseudonymous, previously launched one protocol that shut down after 4 months"
        ),
        risk_factors=["aggregator of aggregators (4-layer recursion)", "single admin EOA", "no timelock", "Certik audit only", "APY mismatch (advertised vs actual)", "team history (prior shutdown)", "pseudonymous team"],
        mitigants=["moderate TVL", "partial refund precedent"],
    ),
    EvalItem(
        name="SynthPerp",
        category="Synthetic Perpetuals",
        true_score=50,
        is_training=False,
        description=(
            "SynthPerp — Synthetic Perpetual Futures\n"
            "TVL: $220M | Live: 12 months\n"
            "Audits: 2 (Spearbit, Sherlock contest)\n"
            "Oracle: Pyth Network with Chainlink fallback\n"
            "Admin: 4-of-6 multisig with 48h timelock\n"
            "Governance: Token-weighted, 45% community, 30% team (4-year vest)\n"
            "Insurance: Insurance fund at 2.8% of open interest\n"
            "Track record: 1 flash crash event, insurance fund covered all losses, "
            "fund was recapitalized within 2 weeks via fees\n"
            "Other: Supports 20x leverage on synthetic assets, "
            "no actual underlying (fully synthetic via oracle prices), "
            "funding rate mechanism keeps synthetic prices aligned"
        ),
        risk_factors=["leverage (20x)", "fully synthetic (no underlying)", "flash crash history", "oracle dependency"],
        mitigants=["dual oracle", "proven insurance fund", "reputable audits", "strong governance", "moderate track record", "adequate insurance ratio"],
    ),
    EvalItem(
        name="AtomicSwap",
        category="Atomic Swap DEX",
        true_score=24,
        is_training=False,
        description=(
            "AtomicSwap — Cross-Chain Atomic Swap DEX\n"
            "TVL: $145M | Live: 20 months\n"
            "Audits: 2 (Trail of Bits, Halborn)\n"
            "Oracle: No oracle needed (HTLC-based atomic swaps)\n"
            "Admin: 3-of-5 multisig with 72h timelock (for fee changes only)\n"
            "Governance: Token-weighted, well-distributed\n"
            "Insurance: Atomic swap guarantee (cryptographic — no counterparty risk)\n"
            "Track record: Zero exploits, $22B cumulative swap volume\n"
            "Other: True cross-chain without bridges — uses hash time-locked contracts, "
            "swap timeout of 24h, supports BTC/ETH/SOL natively, "
            "no wrapped tokens or bridges involved"
        ),
        risk_factors=["timeout edge cases", "limited asset support"],
        mitigants=["no bridge risk", "cryptographic guarantee", "double audit", "long track record", "no oracle", "proven mechanism (HTLC)"],
    ),
    EvalItem(
        name="LiqLocker",
        category="Liquidity Locking",
        true_score=30,
        is_training=False,
        description=(
            "LiqLocker — LP Token Locking Service\n"
            "TVL: $680M (locked LP tokens) | Live: 24 months\n"
            "Audits: 2 (Consensys Diligence, Zellic)\n"
            "Oracle: No oracle needed (time-lock mechanism)\n"
            "Admin: Immutable lock contracts, upgradeable UI only\n"
            "Governance: None needed (pure locking service)\n"
            "Insurance: Not applicable (tokens are locked, not lent)\n"
            "Track record: Zero exploits, 8,400 active locks, "
            "used by 340 token projects\n"
            "Other: Simple mechanism — deposit LP tokens, set unlock date, "
            "tokens are released after unlock date, no early withdrawal, "
            "emergency migration function exists but requires 3-of-5 multisig + 14-day timelock"
        ),
        risk_factors=["emergency migration function exists", "underlying LP token risk (not LiqLocker's risk)"],
        mitigants=["immutable core", "double audit", "massive adoption", "simple design", "14-day timelock on emergency function"],
    ),
    EvalItem(
        name="YieldSplit",
        category="Yield Tokenization",
        true_score=45,
        is_training=False,
        description=(
            "YieldSplit — Yield Tokenization Protocol\n"
            "TVL: $160M | Live: 11 months\n"
            "Audits: 2 (Spearbit, Code4rena)\n"
            "Oracle: Chainlink for underlying asset pricing\n"
            "Admin: 3-of-5 multisig with 48h timelock\n"
            "Governance: Token-weighted, moderately distributed\n"
            "Insurance: None\n"
            "Track record: 1 yield token mispricing incident (corrected within 4h, no losses)\n"
            "Other: Splits yield-bearing assets into principal tokens (PT) and yield tokens (YT), "
            "fixed-rate and variable-rate markets, "
            "novel tokenomics create complexity in pricing and liquidation, "
            "PT/YT pricing depends on accurate yield projections"
        ),
        risk_factors=["novel tokenomics (complex pricing)", "yield projection dependency", "mispricing incident", "no insurance"],
        mitigants=["reputable audits", "incident resolved without losses", "moderate governance", "moderate timelock"],
    ),
    EvalItem(
        name="DerivBridge",
        category="Derivatives Bridge",
        true_score=75,
        is_training=False,
        description=(
            "DerivBridge — Cross-Chain Derivatives Bridge\n"
            "TVL: $95M | Live: 5 months\n"
            "Audits: 1 (Quantstamp)\n"
            "Oracle: Custom relayer network (7 nodes, 4 team-operated)\n"
            "Admin: 2-of-3 multisig with 6h timelock\n"
            "Governance: Foundation-controlled\n"
            "Insurance: None\n"
            "Track record: 1 delayed settlement event (72h delay, no losses)\n"
            "Other: Bridges derivative positions across chains (not just tokens — full position state), "
            "novel approach with limited precedent, "
            "team-operated relayer majority raises centralization concerns, "
            "position migration can fail if destination chain congested"
        ),
        risk_factors=["bridge + derivatives (compound risk)", "team controls majority of relayers (57%)", "low multisig (2-of-3)", "short timelock (6h)", "single audit", "novel mechanism", "short track record", "settlement delays"],
        mitigants=["no losses during delay event", "Quantstamp audit"],
    ),
    EvalItem(
        name="PoolRouter",
        category="Liquidity Routing",
        true_score=33,
        is_training=False,
        description=(
            "PoolRouter — Smart Liquidity Router\n"
            "TVL: $0 (pass-through, no custody) | Live: 14 months\n"
            "Audits: 2 (Trail of Bits, Sherlock)\n"
            "Oracle: No oracle needed (reads on-chain pool state)\n"
            "Admin: Immutable router contract\n"
            "Governance: None (open-source, permissionless)\n"
            "Insurance: Not applicable (no custody)\n"
            "Track record: Zero exploits, $34B cumulative routed volume, "
            "used by 45 frontend integrators\n"
            "Other: Aggregates liquidity across 30+ DEX pools on same chain, "
            "split routing for large orders, MEV-protected via private mempool option, "
            "no token, no admin keys, no upgradability"
        ),
        risk_factors=["MEV extraction on unprotected routes", "dependency on underlying pool security"],
        mitigants=["no custody (pass-through)", "immutable", "double audit", "massive volume", "no admin surface", "MEV protection option"],
    ),
    EvalItem(
        name="StakeDAO",
        category="Staking DAO",
        true_score=26,
        is_training=False,
        description=(
            "StakeDAO — Multi-Protocol Staking Aggregator\n"
            "TVL: $540M | Live: 22 months\n"
            "Audits: 2 (OpenZeppelin, PeckShield)\n"
            "Oracle: Chainlink for reward calculations\n"
            "Admin: 5-of-9 multisig with 5-day timelock\n"
            "Governance: veToken model with gauge-weighted emissions\n"
            "Insurance: Protocol treasury ($22M, 4% of TVL) used for emergency coverage\n"
            "Track record: 1 minor reward calculation error (overcredited 0.2%, clawed back via governance vote)\n"
            "Other: Aggregates staking across 12 protocols, "
            "auto-compounds rewards, bribes marketplace for gauge votes, "
            "all strategies are immutable once deployed"
        ),
        risk_factors=["composability across 12 protocols", "reward calculation complexity", "bribe marketplace (governance manipulation)"],
        mitigants=["double audit", "long track record", "high multisig threshold", "long timelock", "treasury buffer", "immutable strategies"],
    ),
    EvalItem(
        name="CreditLine",
        category="Undercollateralized Lending",
        true_score=70,
        is_training=False,
        description=(
            "CreditLine — Undercollateralized Corporate Lending\n"
            "TVL: $120M | Live: 8 months\n"
            "Audits: 1 (Zellic)\n"
            "Oracle: Custom credit scoring model (proprietary)\n"
            "Admin: 3-of-5 multisig with 24h timelock\n"
            "Governance: Credit committee (5 members, 3 appointed by team)\n"
            "Insurance: First-loss tranche covers 8% of pool\n"
            "Track record: 2 borrower defaults totaling $3.2M (covered by first-loss tranche)\n"
            "Other: Lends to verified businesses and institutions, "
            "credit assessment is off-chain and opaque, "
            "KYC required for borrowers, permissionless for lenders, "
            "loan terms range from 30 to 180 days, "
            "average borrower rate: 12% APR"
        ),
        risk_factors=["undercollateralized (novel DeFi risk)", "opaque credit scoring", "2 defaults in 8 months", "single audit", "credit committee centralization", "off-chain assessment"],
        mitigants=["first-loss tranche", "KYC for borrowers", "verified institutional borrowers", "timelock"],
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
    Scenario(
        name="restaking_slash",
        description=(
            "RestakeHub Slashing Event:\n"
            "An AVS integrated with RestakeHub suffers a liveness failure. The AVS's "
            "slashing conditions were poorly specified — they trigger on liveness failures, "
            "not just safety failures. 8% of restaked ETH is slashed ($49.6M). "
            "RestakeHub had no mechanism to pause the slashing and the 24h timelock "
            "was too slow to intervene. The team proposes a hard fork to reverse the slashing. "
            "How does this change your risk assessment?"
        ),
        expected_impact="Score should increase significantly — validates restaking systemic risk",
        lesson="Restaking multiplies risk in ways that are hard to predict. Poorly specified slashing conditions in a SINGLE AVS can cascade to the entire restaking pool. The 24h timelock was insufficient for an event that unfolded in minutes. Hard fork proposals undermine trust in immutability guarantees.",
    ),
    Scenario(
        name="rwa_regulatory",
        description=(
            "RWAVault Regulatory Action:\n"
            "The SEC issues a Wells notice to RWAVault's issuing entity, alleging that "
            "the tokenized T-bill tokens constitute unregistered securities. The notice "
            "does not freeze assets but creates legal uncertainty. Three institutional "
            "depositors (representing 40% of TVL) withdraw as a precaution. "
            "The secondary market price of the tokenized T-bill drops to $0.96. "
            "How does this change your risk assessment?"
        ),
        expected_impact="Score should increase moderately — regulatory risk materialized but no asset loss",
        lesson="RWA protocols carry regulatory risk that is fundamentally different from smart contract risk. A Wells notice doesn't mean the protocol is broken — the technology works fine. But the regulatory risk can cause a bank-run dynamic where rational withdrawal by some depositors harms remaining depositors via depeg.",
    ),
    Scenario(
        name="oracle_network_attack",
        description=(
            "OracleNet Manipulation Attempt:\n"
            "A well-funded attacker acquires enough stake to control 12 of 180 oracle nodes. "
            "They attempt to manipulate the ETH/USD feed by reporting a 20% higher price. "
            "The median aggregation filters out the outlier reports. The attack costs the "
            "attacker $2.8M in slashed stake. OracleNet's monitoring detects and removes "
            "the compromised nodes within 90 minutes. How does this change your assessment?"
        ),
        expected_impact="Score should stay low or decrease — system worked as designed",
        lesson="Oracle networks with median aggregation and slashing are resistant to minority attacks. The attack was expensive for the attacker and failed. This is a CONFIDENCE-BUILDING event. The system's defense mechanisms worked as designed. However, it does reveal the theoretical attack surface — what happens with 51% of nodes?",
    ),
]


# ============================================================================
# TRAP PROTOCOLS — 6 items for adversarial bias detection
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
    TrapItem(
        name="AuditedRug",
        true_score=85,
        bias_type="audit-trust-bias",
        description=(
            "AuditedRug — Audited Yield Protocol\n"
            "TVL: $38M | Live: 4 months\n"
            "Audits: 2 (Certik, Hacken)\n"
            "Oracle: Chainlink\n"
            "Admin: Single EOA deployer with no timelock — can drain contract via "
            "privileged withdrawAll() function\n"
            "Governance: Discord polls (non-binding)\n"
            "Insurance: None\n"
            "Track record: Team previously launched 2 projects (both abandoned, "
            "one with unresolved user fund complaints)\n"
            "Other: 80% APY from undisclosed strategy, token emission schedule "
            "heavily favors early team allocation, contract has an unaudited "
            "migration function that can move all funds to a new address"
        ),
    ),
    TrapItem(
        name="OldButSafe",
        true_score=16,
        bias_type="novelty-bias",
        description=(
            "OldButSafe — Vanilla Lending Pool\n"
            "TVL: $3.2B | Live: 42 months\n"
            "Audits: 4 (OpenZeppelin, Trail of Bits, ChainSecurity, Consensys Diligence)\n"
            "Oracle: Chainlink with Uniswap V3 TWAP fallback\n"
            "Admin: 7-of-12 multisig with 7-day timelock\n"
            "Governance: veToken model, fully decentralized, no team veto\n"
            "Insurance: Protocol insurance fund ($180M, 5.6% of TVL) + Nexus Mutual\n"
            "Track record: Zero exploits in 42 months, survived 3 market crashes, "
            "$420B cumulative lending volume\n"
            "Other: Basic lending/borrowing — no exotic features, no leverage, "
            "no cross-chain, conservative collateral factors, "
            "boring by design, slow to add new collateral types"
        ),
    ),
]
