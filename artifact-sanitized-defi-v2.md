# DeFi Risk Assessment Memory Artifact (Sanitized)
## Generalizable calibration framework — no protocol names or exact scores

## 1. CALIBRATION

### Base Risk by Protocol Type
- **Stablecoin DEX/AMM** (stablecoin-only pairs, AMM pricing): Start at 10-15
- **Vote-Escrowed Token Locking** (simple lock-and-vote, no composability): Start at 12-18
- **Layer 2 Payment Channels** (state channels, atomic settlement): Start at 18-22
- **Liquid Staking Derivatives** (professional operators, derivative token): Start at 20-25
- **Standard Lending** (collateralized, oracle-priced): Start at 25-30
- **Decentralized Oracle Networks** (data aggregation, node staking): Start at 25-30
- **DeFi Insurance** (underwriting pools, claims processing): Start at 30-35
- **Tokenized Real World Assets** (off-chain backing, custodial): Start at 32-38
- **Flash Loan Platforms** (atomic, no collateral): Start at 35-42
- **Prediction Markets** (resolution oracle dependent): Start at 40-45
- **CDP Stablecoins** (collateral-backed, liquidation risk): Start at 45-50
- **Options Vaults** (automated strategies, vol exposure): Start at 48-55
- **Perpetual Futures** (leverage, funding rates): Start at 50-58
- **Privacy Protocols** (novel crypto, regulatory risk): Start at 55-60
- **Cross-Chain DEX Aggregators** (multi-bridge routing): Start at 58-62
- **Cross-Chain Bridges** (relayer/validator sets): Start at 58-65
- **Token Launchpads** (project quality variance): Start at 60-68
- **Restaking Platforms** (recursive staking, AVS risk): Start at 65-70
- **Leveraged Lending** (looped leverage, liquidation cascades): Start at 68-75
- **Yield Aggregators** (composability across protocols): Start at 70-80
- **Leveraged Yield Farming** (recursive leverage, multi-chain): Start at 85-95

### Risk Modifiers (additive)

**Audit quality:**
- Triple audit from top-tier firms (Trail of Bits, OpenZeppelin, Sigma Prime, ChainSecurity, Consensys Diligence): -12 to -15
- Double audit from top-tier firms: -8 to -10
- Double audit mixed quality: -5 to -7
- Single audit from top firm (Trail of Bits, OpenZeppelin, Spearbit): -3 to -5
- Single audit from mid-tier firm (Zellic, Cyfrin, Halborn): -2 to -3
- Single audit from lower-tier firm (Certik, Hacken): -1 to -2. Treat these as marginally better than no audit.
- Competitive audit contest (Code4rena, Sherlock): -2 to -4 depending on bounty size
- Formal verification: -3 additional
- No audit: +15 to +20
- "Internal audit" or "audit in progress": treat as no audit

**Admin controls:**
- Immutable core contracts (no admin keys at all): -8 to -10
- High multisig (5+ of 8+) with long timelock (72h+): -6 to -8
- Moderate multisig (4-of-7) with 48h timelock: -4 to -5
- Standard multisig (3-of-5) with 24-48h timelock: -2 to -3
- Low multisig (2-of-4) with 24h timelock: 0 (barely adequate)
- Very low multisig (2-of-3): +3 to +5
- Single admin key with timelock: +8 to +10
- Single admin key, no timelock: +12 to +15
- Single EOA with instant parameter changes or privileged withdraw functions: +15 to +20

**Track record:**
- 24+ months, zero exploits, high cumulative volume: -8 to -10
- 18+ months, zero exploits: -5 to -7
- 12-18 months, minor incidents handled cleanly: -2 to -4
- 6-12 months, clean: 0
- 6-12 months with incidents: +3 to +5
- Under 6 months: +5 to +8
- Under 3 months: +8 to +12
- Team previously abandoned a project: +10 to +15

**Oracle dependency:**
- No oracle needed (AMM pricing, atomic transactions, time-locks, HTLCs): -5 to -8
- Chainlink: -3 to -5
- Dual oracle with circuit breaker (e.g., Chainlink + fallback): -4 to -6
- Pyth Network: -2 to -3
- UMA Optimistic Oracle: -1 to -2
- Custom oracle with 5+ independent nodes: 0
- Custom oracle with 3 nodes: +3 to +5
- Custom oracle, single node or team-operated majority: +8 to +12
- Undisclosed oracle architecture: +10 to +15

**Insurance/loss absorption:**
- External coverage (Nexus Mutual or equivalent) at >3% TVL: -5 to -7
- Protocol insurance fund >3% TVL: -4 to -6
- Protocol insurance fund 1-3% TVL: -2 to -3
- Slashing mechanism with meaningful staked collateral: -3 to -5
- First-loss tranche: -2 to -3
- Insurance fund <1% TVL: -1
- No insurance on complex protocol: +2 to +5

**Governance:**
- Fully decentralized, no team veto, well-distributed token: -3 to -5
- veToken model, healthy distribution: -2 to -3
- Token-weighted, team <40%: -1 to -2
- Token-weighted, team >50%: +2 to +3
- Foundation-controlled with advisory board: +3 to +5
- Centralized with vague decentralization plans: +5 to +8
- No governance mechanism at all: +3 to +5 (context-dependent)

## 2. RED FLAGS

### CRITICAL (each adds +15 to +25)
1. No audit with live user funds
2. Single admin key that can drain contracts via privileged function
3. Obfuscated or unverifiable source code
4. Recursive leverage with no circuit breaker or auto-deleverage
5. Custom oracle with undisclosed architecture
6. Team previously abandoned project with unresolved user fund complaints
7. Large discrepancy between advertised and actual APY (e.g., claiming 65% when historical is 31%)

### MAJOR (each adds +8 to +15)
1. Single audit from lower-tier firm on a complex protocol
2. Less than 3 months live with significant TVL
3. Team controls majority of validators/relayers (>50%)
4. Very low multisig (2-of-3) with short timelock (<12h)
5. Aggregator-of-aggregators pattern (recursive composability 3+ layers deep)
6. Undercollateralized lending with opaque/proprietary credit assessment
7. Novel cryptographic primitives less than 12 months old in production
8. Regulatory uncertainty with potential for enforcement action

### WARNING (each adds +3 to +8)
1. Single audit from reputable firm (acceptable for simple protocols, insufficient for complex ones)
2. Team token concentration >50% even with vesting
3. Pseudonymous team (partially mitigated if doxxed to investors)
4. Insurance fund below 2% of TVL
5. Upgradeable contracts via proxy pattern
6. Short timelock (6-12h) on multisig
7. Prior incidents, even if handled well — demonstrates the risk surface exists

## 3. MITIGANTS (ranked by impact)

### Highest Impact (-8 to -15 each)
1. **Immutable core contracts** — eliminates admin risk entirely. Protocols scoring lowest in my experience share this property.
2. **Triple audit from top firms** — near-exhaustive code review provides strongest assurance.
3. **Massive proven track record** — 24+ months with billions in cumulative volume and zero exploits. Time-tested at scale.
4. **No oracle dependency** — eliminates the entire oracle manipulation attack vector.

### High Impact (-5 to -8 each)
5. **Strong multisig + long timelock** — 5+ of 7+ signers with 48h+ delay.
6. **Insurance coverage >3% TVL** — meaningful loss absorption capacity.
7. **No custody / pass-through design** — protocol never holds funds, but still has smart contract risk from routing/logic.
8. **Cryptographic guarantees** — hash time-locked contracts, ZK proofs, EVM-enforced atomic repayment.

### Moderate Impact (-2 to -5 each)
9. **Dual oracle with circuit breaker** — fallback + pause mechanism.
10. **Peer-to-peer model** — limits systemic pooled risk.
11. **Conservative allocation strategy** — heavy stablecoin allocation reduces exposure.
12. **Proven claims/dispute track record** — for insurance protocols, a history of processing claims correctly.
13. **Geographic/operator diversity** — decentralized across many jurisdictions reduces coordinated failure risk.

## 4. HEURISTICS

### Quick Assessment Rules
- **If immutable + triple audit + 24mo+ track record → 10-20.** The safest protocols combine all three.
- **If no oracle + no admin + simple mechanism → 15-25.** Simplicity is a powerful mitigant.
- **If single admin key + no audit → 85-95.** Maximum admin risk + no code assurance.
- **If bridge + single audit → 60-70.** Bridges are inherently high risk; single audit is insufficient.
- **If leverage + short track record → 68-78.** Leverage amplifies all other risks.
- **If aggregator-of-aggregators → 78-85.** Each composability layer multiplies risk.

### Common Calibration Errors
- **Don't underrate simple/boring protocols.** The simplest mechanisms (token locking, payment channels, basic AMMs) should score lowest. Simplicity IS the mitigant. Boring = safe.
- **Don't overrate "no incidents" on protocols under 6 months old.** Short history is absence of data, not evidence of safety.
- **Don't treat all bridges equally.** Bridges with optimistic verification and challenge periods are materially safer than those with low multisig and team-controlled relayers. Range: 55-80.
- **Don't give automatic low scores to pass-through protocols.** Even with no custody, routing logic and MEV exposure create real smart contract risk. Score 25-35, not 0-10.
- **Don't confuse "used in attacks on other protocols" with "was attacked."** Flash loan platforms that were tools in oracle attacks on OTHER protocols have zero self-incidents. Score the protocol's own risk.
- **Don't let complexity automatically inflate scores.** A protocol with complex tokenomics but triple audit, high multisig, long track record, and insurance can still score 25-35.
- **Don't assume stablecoin protocols are automatically safe.** A "stablecoin DEX" with custom fallback oracle and team concentration can score 40-50, not 10-15.
- **Certik and Hacken audits provide minimal assurance.** Treat as marginally better than no audit. Do not meaningfully lower score for these.
- **Regulatory risk is real risk.** Tokenized assets with evolving regulatory exposure carry material non-technical risk that can trigger bank-run dynamics.
- **Insurance protocols carry correlated risk.** A DeFi-wide event could drain the pool. Score higher than the protocol's own technical quality suggests.

## 5. MISTAKES TO AVOID

### Systematic Biases I Corrected During Training
1. **Overweighting scary-sounding features.** Terms like "leverage," "recursive," and "bridge" sound dangerous but must be scored on actual risk factors, not terminology. A leveraged lending protocol with auto-deleverage, Chainlink oracle, and contest audit is 70-75, not 85+.
2. **Underweighting admin key risk.** Single admin key with no timelock is one of the highest-impact risk factors. It should add +12 to +20 regardless of other qualities.
3. **Bridge bias.** I initially underrated bridges. Even clean bridges with good track records should not score below 55 due to inherent architectural risk.
4. **Oracle dismissal.** Custom oracles with few nodes (2-3) are far more dangerous than I initially assessed. Custom oracle with 3 nodes should add +3 to +5 minimum.
5. **False safety from stablecoin label.** The word "stablecoin" in a protocol name does not make it safe. Always check the oracle, admin controls, and governance independently.
6. **Ignoring what insurance actually covers.** An insurance fund at 1.2% of TVL or open interest is nearly meaningless in a stress event. Adequate insurance starts at 3%+.
7. **Discounting regulatory risk.** For real-world-asset protocols, regulatory action can be more damaging than a smart contract exploit because it triggers coordinated withdrawal.
8. **Treating track record linearly.** The difference between 2 months and 12 months is enormous. The difference between 24 months and 30 months is marginal. Front-load the track record discount.
