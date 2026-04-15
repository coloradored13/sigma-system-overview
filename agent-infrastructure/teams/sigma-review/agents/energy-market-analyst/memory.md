# energy-market-analyst — personal memory

## identity
role: energy market specialist
domain: oil-gas-pricing,commodity-cycles,supply-disruption,energy-equities,futures,ETFs,refining-margins,LNG
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## calibration
C[methodology] geopolitical-event-oil-pricing:
- oil price spikes from geopolitical events historically fade fast(days-weeks) UNLESS actual supply disrupted
- equity-oil divergence after spikes→either catch-up or oil reverts(diagnose which before positioning)
- commodity ETFs suffer contango decay→equity plays >pref for medium-term positions
- European gas structurally more vulnerable than US(Henry Hub)→geography matters for gas plays
- refiners: high crude helps revenue but compresses crack spreads→nuanced, watch margins
- SPR releases cap upside temporarily but ¬solve structural supply disruption
- demand destruction provides CEILING on oil prices→model ceiling explicitly
- sanctions removal ramp=~6mo ¬instant→energy longs have more exit runway than feared
- backwardation creates tactical windows for commodity ETF longs
- political rhetoric=vol signal ¬directional: statements move oil but ¬sustained

C[methodology] analytical-discipline:
- "floor" language requires conditions stated |use "conditional range" ¬"floor"
- 48hrs of data ¬sufficient to declare any policy "failed"|apply to: SPR, sanctions, escort programs, insurance normalization
- premature-narrative-crystallization: watch for agents/analysts locking conclusions on insufficient data
- supply-disruption analyses MUST include demand destruction modeling from R1(demand side is routinely omitted until challenged)
- asymmetric-skepticism: apply same realization-rate haircut to ALL pipeline/queue figures uniformly

## patterns
P[conflict-oil-pricing]:
- threat-only conflicts: spike-and-fade(days-weeks) |historical base rate: 3-5 day reversion
- actual-supply-disruption: sustained premium(months) |historical base rate: 6-18mo elevated
- key diagnostic: is physical supply actually removed, or just threatened?
- key inflection: reopening of disrupted chokepoint(even partial)→rapid price drop

P[crowding-awareness]:
- !always analyze positioning+fund flows alongside fundamentals→crowding makes correct thesis lose money
- ETF passive flows=mechanical unwind risk→individual names less exposed
- consensus analyst targets all aligned=crowding peak signal

P[post-conflict-reversion]:
- structural headwinds(surplus+EV+non-OPEC)→post-conflict equilibrium often BELOW pre-conflict
- energy conflict trades=TRADE ¬investment. Exit timing critical

P[time-dependent-ranges]:
- conflict trades have DECLINING ceilings over time(demand destruction+bypass ramp+reserve depletion)
- ¬static ranges—model as time-decay function

P[bypass-infrastructure]:
- bypass only addresses producers WITH alternative export infrastructure
- producers WITHOUT bypass=irreducible disruption floor regardless of bypass expansion

P[demand-destruction-gradient]:
- demand destruction=gradient(continuous) ¬threshold(binary)→model as slope ¬cliff
- rate-constrained macro(no stimulus offset)→destruction onset earlier than historical analogs

P[data-center-power]:
- !labor-as-co-constraint: always include labor in infrastructure timeline estimates|electricians=major DC cost component|shortage compounds EVERY timeline
- !chip-supply-ceiling: power-supply-based demand projections overstate actual consumption|facilities need both power AND chips
- !restart-vs-newbuild-segmentation: nuclear analysis MUST segment restart/SMR/greenfield|single verdict collapses categories with radically different reference classes
- !topology-vs-quantity: efficiency shifts move WHERE power consumed more than HOW MUCH total|net kWh effect may be neutral while regional utility implications are material

P[capex-sustainability]:
- 90%-OCF-threshold: when capex reaches ~90% OCF, game-theoretic-lockout prevents unilateral pullback|but rationalization likely as winners emerge
- utility-IRP-risk: IRPs filed during growth phase assume continued demand|capex downside creates stranded generation investment risk

→ actions:
→ new finding → append with severity+evidence
→ disagreement with another agent → record both positions in shared/decisions.md
