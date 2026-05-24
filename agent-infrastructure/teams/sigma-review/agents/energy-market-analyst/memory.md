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
P[FOAK-symmetric-base-rate|src:sustainable-ai-power-2026-05-22|promoted:2026-05-23|class:calibration]: apply 80% FOAK cost-overrun base rate symmetrically to ALL pre-commercial generation tech (EGS, SMR, gas+CCS, fusion) regardless of novelty advantage narrative|observed failure: applied to SMR but not EGS in same review→DA caught asymmetry|correct form: any tech with ¬operating commercial plant carries same FOAK uncertainty band|exception: only reduce haircut if FOAK plant has COD + operating data in same technology class
P[null-finding-temporal-bounding|src:sustainable-ai-power-2026-05-22|promoted:2026-05-23|class:calibration]: null findings (X appropriately deprioritized) MUST carry explicit temporal+geographic bound|observed failure: green-H2 NULL stated as categorical; own DB[] evidence pointed to 2030-2032 non-null at H2Hub-adjacent sites—contradiction not surfaced until DA warrant audit|correct form: NULL(2026-2028 primary power nationally) ¬NULL(categorically)|applies-to: any deprioritization finding where own cost trajectory evidence shows parity within review horizon
P[hydrogen-backup-vs-primary-economics|src:sustainable-ai-power-2026-05-22|promoted:2026-05-23|class:pattern]: H2 fuel cell analysis requires TWO distinct economic frameworks: (a) backup/UPS = capital-cost comparison vs diesel genset (¬LCOE competition)→near-term feasible with gray/blue H2; (b) primary power = LCOE comparison vs generation alternatives→only competitive at <=$2/kg green H2|conflating these frameworks produces wrong verdict|backup replacement is actionable ≤5y; primary power is medium-term at best|applies-to: any energy storage/generation review covering hydrogen
P[interconnection-reform-timeline|src:sustainable-ai-power-2026-05-22|promoted:2026-05-23|class:calibration]: FERC interconnection reform (Order 1920 + cluster studies) is 10-year structural fix ¬3-year operational fix|legal challenges+NEPA+landowner rights are non-bureaucratic constraints reform does not touch|PJM TC1: 100 GW applications→17 GW draft IAs confirms filter function not acceleration|BTM+nuclear co-location is only near-term bypass for 2026-2030 window|applies-to: any US data center power sourcing or renewable energy project timeline analysis

P[SMR-fleet-scenario-calibration|src:ai-power-followup-2026-05-23|promoted:2026-05-23|class:calibration]: US advanced nuclear 2035 base case MUST disaggregate Category A (LWR restarts: Palisades/Duane Arnold/TMI, 2–4 GW by 2030) vs Category B (genuine SMRs: Natrium/Xe-100/Kairos/Oklo, 0.5–2 GW base case by 2035)|XVERIFY[openai:gpt-5.4] partial-confirmed base case|aggressive-optimistic 4–6 GW requires 3–4 simultaneous FOAK successes (joint probability ~0.8% at RC base rate, ~20–30% with ADVANCE Act adjustment)|H1-style "5 GW SMR by 2035" threshold is aggressive-optimistic not base case|Oklo+Kairos contribute minimally to 2035 capacity even under optimistic scheduling|applies-to: any US nuclear buildout forecast that aggregates restarts + SMRs without category segmentation
P[DOE-earthshot-target-vs-developer-actuals|src:ai-power-followup-2026-05-23|promoted:2026-05-23|class:calibration]: DOE Energy Earthshot targets are aspirational trajectories ¬confirmed delivery schedules|DOE Liftoff Reports are the authoritative signal when developer actual cost data diverges from target trajectory|observed: Hydrogen Shot $1/kg by 2031 aspirational while DOE Liftoff Dec 2024 shows developer costs rising to $5–7/kg (before 45V) — wrong direction|SunShot is the rare exception (achieved ahead of schedule); most Earthshots are aspirational|RC[DOE-energy-cost-targets-met-by-deadline]=variable, weighted toward aspirational for novel tech without established learning curves|applies-to: any analysis citing DOE Earthshot cost targets as near-term delivery commitments (EGS $45/MWh, Hydrogen Shot $1/kg, LDES $0.05/kWh)
P[iron-air-RTE-LCOE-cascade|src:ai-power-followup-2026-05-23|promoted:2026-05-23|class:calibration]: iron-air battery round-trip efficiency 45–50% (vs lithium-ion 85–90%) forces ~1.7–2× BTM solar PV oversizing for equivalent net energy delivery|materially raises blended LCOE in BTM solar+LDES configurations|at Lazard 2025 estimate ($35–50/kWh) + RTE penalty, blended LCOE ~$90–115/MWh not sub-$80/MWh|sub-$80/MWh requires Form Energy achieving $20/kWh manufacturing target (unverified as of 2026; Georgia Power 15 MW project is first independent data point ~2027–2028)|applies-to: any BTM solar + long-duration storage LCOE analysis using iron-air chemistry|¬applies: flow batteries or other LDES chemistries with different RTE profiles

→ actions:
→ new finding → append with severity+evidence
→ disagreement with another agent → record both positions in shared/decisions.md
