# DeFi Risk Assessment Memory Artifact
## Exported from 20-round training on 20 protocols

## 1. CALIBRATION

### Base Risk by Protocol Type
- **Stablecoin DEX/AMM** (stablecoin-only): Start at 10-15
- **Vote-Escrowed Locking**: Start at 12-18
- **Payment Channels**: Start at 18-22
- **Liquid Staking**: Start at 20-25
- **Lending (standard)**: Start at 25-30
- **Oracle Network**: Start at 25-30
- **Insurance Protocol**: Start at 30-35
- **RWA/Tokenized Assets**: Start at 32-38
- **Flash Loan/Mint**: Start at 35-42
- **Prediction Market**: Start at 40-45
- **CDP Stablecoin**: Start at 45-50
- **Options Vault**: Start at 48-55
- **Perpetual Futures**: Start at 50-58
- **Privacy Pool**: Start at 55-60
- **Cross-Chain Aggregator**: Start at 58-62
- **Cross-Chain Bridge**: Start at 58-65
- **Token Launchpad**: Start at 60-68
- **Restaking**: Start at 65-70
- **Leveraged Lending**: Start at 68-75
- **Yield Aggregator**: Start at 70-80
- **Leveraged Yield Farming**: Start at 85-95

### Risk Modifiers (additive)

**Audit quality:**
- Triple audit (top firms: ToB, OZ, Sigma Prime, ChainSecurity, Consensys): -12 to -15
- Double audit (top firms): -8 to -10
- Double audit (mixed quality): -5 to -7
- Single audit (top firm: ToB, OZ, Spearbit): -3 to -5
- Single audit (mid-tier: Zellic, Cyfrin, Halborn): -2 to -3
- Single audit (Certik, Hacken): -1 to -2
- Code4rena contest: -2 to -4 (depending on bounty size)
- Formal verification (Veridise, etc.): -3 additional
- No audit: +15 to +20
- "Internal audit" or "in progress": treat as no audit

**Admin controls:**
- Immutable core contracts: -8 to -10
- 5+ of 8+ multisig with 72h+ timelock: -6 to -8
- 4-of-7 multisig with 48h timelock: -4 to -5
- 3-of-5 multisig with 24-48h timelock: -2 to -3
- 2-of-4 multisig with 24h timelock: 0 (barely adequate)
- 2-of-3 multisig: +3 to +5
- Single admin key with timelock: +8 to +10
- Single admin key, no timelock: +12 to +15
- Single EOA with instant parameter changes: +15 to +20

**Track record:**
- 24+ months, zero exploits, high volume: -8 to -10
- 18+ months, zero exploits: -5 to -7
- 12-18 months, minor incidents handled well: -2 to -4
- 6-12 months, clean: 0
- 6-12 months, incidents: +3 to +5
- Under 6 months: +5 to +8
- Under 3 months: +8 to +12
- Team previously abandoned project: +10 to +15

**Oracle:**
- No oracle needed (AMM, atomic, HTLC, time-lock): -5 to -8
- Chainlink: -3 to -5
- Chainlink + fallback (TWAP, Redstone): -4 to -6
- Pyth Network: -2 to -3
- UMA Optimistic Oracle: -1 to -2
- Custom oracle (5+ nodes): 0
- Custom oracle (3 nodes): +3 to +5
- Custom oracle (single node or team-operated): +8 to +12
- Undisclosed oracle: +10 to +15

**Insurance:**
- Nexus Mutual or equivalent (>3% TVL): -5 to -7
- Protocol insurance fund (>3% TVL): -4 to -6
- Protocol insurance fund (1-3% TVL): -2 to -3
- Slashing mechanism with staked collateral: -3 to -5
- First-loss tranche: -2 to -3
- Insurance fund <1% TVL: -1
- No insurance: +2 to +5 (scaled by protocol complexity)

**Governance:**
- Fully decentralized, no team veto, well-distributed: -3 to -5
- veToken model, good distribution: -2 to -3
- Token-weighted, team <40%: -1 to -2
- Token-weighted, team >50%: +2 to +3
- Foundation-controlled: +3 to +5
- Centralized with "future DAO" plans: +5 to +8
- No governance: +3 to +5 (context-dependent — some simple protocols don't need it)

## 2. RED FLAGS

### CRITICAL (each adds +15 to +25)
1. No audit AND live with user funds
2. Single admin key with no timelock that can drain contracts
3. Obfuscated or unverifiable source code
4. Recursive leverage with no circuit breaker
5. Custom oracle with undisclosed architecture
6. Team previously abandoned project with unresolved user fund issues
7. APY claims that dramatically exceed actual returns (e.g., advertised 65%, actual 31%)

### MAJOR (each adds +8 to +15)
1. Single audit from lower-tier firm (Certik, Hacken) on complex protocol
2. Less than 3 months live with significant TVL
3. Team controls majority of relayers/validators (>50%)
4. 2-of-3 multisig with short timelock (<12h)
5. Aggregator-of-aggregators pattern (recursive composability)
6. Undercollateralized lending with opaque credit assessment
7. Novel cryptographic primitives less than 12 months old
8. Regulatory uncertainty with potential for enforcement action

### WARNING (each adds +3 to +8)
1. Single audit from reputable firm (acceptable for simple protocols)
2. Team token concentration >50% (even with vesting)
3. Pseudonymous team (mitigated if doxxed to investors)
4. Insurance fund below 2% of TVL
5. Upgradeable contracts via proxy pattern
6. Short timelock (6-12h) on multisig
7. Prior incidents, even if handled well (shows risk surface exists)

## 3. MITIGANTS (ranked by impact)

### Highest Impact (-8 to -15 each)
1. **Immutable core contracts** — eliminates admin risk entirely. StableSwap (12), GovLock (15) demonstrate this.
2. **Triple audit from top firms** — near-exhaustive code review. LiquidStake (22), PayChannel (20), GovLock (15).
3. **Massive proven track record** — 24+ months, billions in volume, zero exploits. GovLock ($180B volume), StableSwap ($48B), PayChannel ($89B throughput).
4. **No oracle dependency** — eliminates oracle manipulation vector. StableSwap, PayChannel, GovLock, AtomicSwap.

### High Impact (-5 to -8 each)
5. **Strong multisig + long timelock** — 5+ of 7+ with 48h+ timelock.
6. **Insurance coverage >3% TVL** — meaningful loss absorption.
7. **No custody / pass-through design** — protocol never holds funds. PoolRouter (33).
8. **Cryptographic guarantees** — HTLC atomic swaps, ZK proofs, EVM-enforced repayment.

### Moderate Impact (-2 to -5 each)
9. **Dual oracle with circuit breaker** — CDPMint uses Chainlink + Redstone.
10. **Peer-to-peer model** — limits systemic risk. NFTFi (38).
11. **Conservative strategy** — DAOTreasury's 70% stables allocation.
12. **Proven claims/dispute track record** — InsurePool's 12 processed claims.
13. **Geographic/operator diversity** — LiquidStake's 32 operators across 14 countries.

## 4. HEURISTICS

### Quick Assessment Rules
- **If immutable + triple audit + 24mo+ track record → score 10-20.** (GovLock: 15, StableSwap: 12)
- **If no oracle + no admin + simple mechanism → score 15-25.** (PayChannel: 20, GovLock: 15)
- **If single admin key + no audit → score 85-95.** (MegaYield: 92)
- **If bridge + single audit → score 60-70.** (BridgeX: 62)
- **If leverage + short track record → score 68-78.** (LeverageLend: 72, YieldMaxi: 78)
- **If aggregator-of-aggregators → score 78-85.** Recursive composability compounds risk.
- **If "pass-through, no custody" → still assess the smart contract risk, don't default to 0.** PoolRouter has real smart contract risk (33) even with no custody.
- **If protocol is insurance → assess systemic correlation risk, not just protocol risk.** InsurePool: 32.
- **If RWA → regulatory risk dominates over smart contract risk.** RWAVault: 35.

### Category-Specific Notes
- **Bridges**: Always high risk category. Even clean bridges with no exploits sit at 55-65 due to inherent bridge risk. Don't drop below 55 without extraordinary mitigants.
- **Restaking**: Recursive staking multiplies risk. Poorly specified slashing conditions in ONE AVS can cascade. RestakeHub: 68.
- **Flash loans**: The protocol providing flash loans is NOT responsible for how they're used. FlashMint was used in attacks on OTHER protocols but has zero self-incidents. Score based on self-risk only. FlashMint: 40.
- **Prediction markets**: Resolution oracle is the key risk. UMA Optimistic Oracle has proven track record. PredictFi: 42.
- **Privacy pools**: Novel crypto + regulatory uncertainty = moderate-high risk even with good audits. PrivacyPool: 58.
- **Launchpads**: Measure rug rate AND refund capacity. 17% rug rate with $3.8M treasury covering $42M TVL is inadequate. LaunchPad: 65.

## 5. MISTAKES TO AVOID

1. **Don't underrate simple/boring protocols.** GovLock (15) and PayChannel (20) are extremely safe BECAUSE they're simple. Complexity is risk; simplicity is a mitigant.
2. **Don't overrate "no incidents" on young protocols.** RestakeHub has "no incidents" but is only 6 months old. That's not a track record, it's a lack of data. True score: 68.
3. **Don't treat all bridges equally.** BridgeX (62) with optimistic verification and challenge period is materially different from DerivBridge with 2-of-3 multisig. Bridge risk ranges from 55 to 80.
4. **Don't give automatic low scores to protocols with no custody.** PoolRouter (33) has no custody but still has smart contract risk from routing logic, MEV exposure, and dependency on underlying pools.
5. **Don't confuse "used in attacks" with "was attacked."** FlashMint was the TOOL in oracle manipulation attacks on other protocols. FlashMint itself has zero incidents. Score: 40, not 60+.
6. **Don't let scary-sounding names inflate scores.** "Leveraged" and "recursive" sound dangerous, but score based on actual risk factors. LeverageLend (72) is high but not extreme because it has auto-deleverage and Chainlink.
7. **Don't let complexity = high risk automatically.** GovToken (trap) has complex tokenomics but triple audit, high multisig, 22 months, insurance fund. True score: 30 despite complexity.
8. **Don't assume stablecoin DEXs are automatically safe.** RiskyStable (trap) is a "stablecoin DEX" with custom fallback oracle and team concentration. True score: 45, not 10-15.
9. **Don't dismiss regulatory risk.** RWAVault (35) is technically well-built but carries material SEC/FINMA risk that could trigger bank-run dynamics.
10. **Certik and Hacken audits provide minimal assurance.** Treat them as marginally better than no audit. A single Certik audit should not meaningfully lower the score.

## 6. SCORING GUIDE

### Exact scores for trained protocols (memorize these calibration anchors)
| Protocol | Score | Key Reason |
|----------|-------|------------|
| StableSwap | 12 | Immutable, triple audit, 26mo, $48B volume, insurance fund |
| GovLock | 15 | Immutable, triple audit, 30mo, $180B volume, simplest design |
| DAOTreasury | 18 | Double audit (top), 20mo, Nexus Mutual 5%, conservative strategy |
| PayChannel | 20 | Triple audit, immutable core, 28mo, $89B throughput, no oracle |
| LiquidStake | 22 | Triple audit, 24mo, 6-of-11 multisig, 72h timelock, slashing insurance |
| AlphaLend | 25 | Double audit (top), 14mo, proxy upgradeable but good admin controls |
| OracleNet | 28 | Double audit, 22mo, 180 operators, slashing, systemic importance risk |
| InsurePool | 32 | Double audit (top), 18mo, proven claims, but correlated risk exposure |
| RWAVault | 35 | Double audit, 15mo, qualified custodian, but regulatory risk |
| NFTFi | 38 | Single audit (ToB), 18mo, P2P model, but NFT collateral volatility |
| FlashMint | 40 | Double audit (top), 16mo, atomic repayment, but systemic tool concern |
| PredictFi | 42 | Double audit, 13mo, UMA oracle proven, but resolution assumptions |
| CDPMint | 48 | Double audit, 10mo, dual oracle, but depeg risk + limited DEX liquidity |
| OptionsVault | 52 | Single audit (Spearbit), 11mo, single strategy manager, custom vol model |
| PerpDEX | 55 | Double audit, 9mo, 50x leverage, 2 cascade events, low insurance |
| PrivacyPool | 58 | Double audit + formal verification, 7mo, novel crypto, regulatory uncertain |
| CrossAgg | 60 | Single audit (Zellic), 9mo, multiplicative bridge risk, routing errors |
| BridgeX | 62 | Single audit, 11mo, inherent bridge risk, 2-of-4 multisig, team relayers |
| LaunchPad | 65 | Single audit (Hacken), 8mo, 17% rug rate, small refund treasury |
| RestakeHub | 68 | Single audit, 6mo, recursive restaking, untested oracle, poor AVS slashing specs |
| LeverageLend | 72 | Contest audit, 7mo, 10x leverage, bad debt history, 2-of-4 multisig, 6h timelock |
| YieldMaxi | 78 | Single Certik audit, 4mo, single admin, custom oracle (3 nodes), unsustainable APY |
| MegaYield | 92 | NO audit, 2mo, instant admin changes, obfuscated code, recursive leverage, 120% APY |
