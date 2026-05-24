# Sustainable AI Power 2026

AI data center electricity demand, clean supply gaps, technology assessments, and under-pursued options as of mid-2026. Attribution: [R-sustainable-ai-power, 2026-05-22]; updated [R-ai-power-followup, 2026-05-24].

---

## Demand-Supply Gap

**US demand:** approximately 200 TWh in 2025, projected ~440 TWh by 2030 — a 130% increase over six years (IEA "Energy and AI," 2025). **EU demand:** ~70 TWh (2025) growing to 115-170 TWh by 2030 (IEA 2025; BNEF 2024).

**Clean supply constraint:** Average PJM interconnection wait has grown from under 2 years (2008) to over 8 years today (RMI; PJM TC1 filings). This produces a structural backlog that cannot clear in the 2025-2030 window.

**Resulting clean-power gap:** ~80-200 TWh (US) and ~30-60 TWh (EU) through 2030. Range is wide; IEA's 2016 forecasts overshot 2020 actuals by 2x, but 2025 actuals are tracking the high scenario. AI training workloads are structurally unlike prior data center demand classes, supporting the high-end.

**Announced vs. operating nuclear:** Hyperscalers have announced 10+ GW of nuclear PPAs since 2024 (Microsoft TMI restart 835 MW, Google Kairos 500 MW, Amazon X-energy, Meta 1-4 GW RFP). Applying the announced-vs-realized base rate from analogous infrastructure (LNG, offshore wind, gas pipelines: 10-25% reaches COD on schedule), the realistic operating figure by 2030 is **2-5 GW** — primarily the TMI restart (2027 delivery). Zero commercial SMRs are operating in the Western world as of mid-2026; all SMR FOAK delivery dates are 2030 or later (IAEA ARIS Catalogue, 2024).

Source: IEA "Energy and AI" 2025; S&P Global 2025; BNEF 2024; PJM TC1 data; RMI; IAEA ARIS. VERIFIED across multiple independent sources.

### AI Demand Trajectory: Deliberate Divergence (Preserve Both Positions)

+ NEW [R-ai-power-followup, 2026-05-24]: Two independent agents disagree on AI demand trajectory beyond 2030 with T1-sourced evidence from both sides; this synthesis preserves both positions rather than collapsing to a single point estimate.

**Tech-industry analyst position:** Continued high-growth (IEA Base Case, approximately 1,200 TWh globally by 2035) is the most likely outcome at 40–50% probability; plateau (IEA Headwinds, approximately 700 TWh by 2035) is a credible minority at 25–35%. Supporting evidence: Jevons paradox (per-token inference costs dropped ~100x from 2022–2025 while usage increased ~1,000x), $700B committed 2026 hyperscaler capex locking in demand infrastructure for 5–7 years, Epoch AI projecting frontier training runs requiring 4–16 GW individually by 2030.

**Reference-class analyst position:** Plateau-after-2032 has approximately 30–45% probability, tying or slightly exceeding continued 30% CAGR (25–40% probability). Historical sectoral surges above 25% CAGR almost never persist more than 5–8 years; AI may differ in Jevons elasticity but the structural deceleration pattern is load-bearing.

**Observable update signals:** Continued growth supported by sustained capex growth above 30% year-over-year in 2027–2028 and GPU utilization above 80%. Plateau supported by capex guidance cuts above 20% in any single quarter and GPU utilization below 60%. Current nuclear PPAs and PJM gas queue commitments implicitly assume continued high growth — both agents agree this framing carries demand-mismatch risk. [R-ai-power-followup, 2026-05-24]

---

## Hydrogen: 6-State Taxonomy

The hydrogen fuel cell question decomposes into five distinct situations with different verdicts.

**State 1 — Gray/blue hydrogen, deployed now.** Companies including Equinix, AT&T, Apple, and Google have deployed roughly 1% of US data center primary power via Bloom Energy SOFCs on gas-reformed hydrogen. Commercially operational, not under-pursued. Reduces criteria pollutants but retains ~80-90% of natural gas lifecycle GHG. Not a sustainability solution.

**State 2 — Green H₂ as primary power, 2026-2028.** Correctly deprioritized, not overlooked. Current green H₂ costs $4-8/kg (IEA Global Hydrogen Review, 2025). Fuel cell LCOE at these costs: $130-180/MWh — 2-3x behind-the-meter solar + 4-hour BESS at $60-80/MWh. Amazon reportedly abandoned Bloom Energy SOFC deployments. Microsoft's hydrogen test was a 48-hour proof-of-concept, not a production deployment. The $7.65B in announced fuel cell deals (late 2025/early 2026) was predominantly gas-reformed, not green. The non-pursuit reflects rational capital allocation.

**State 3 — Green H₂ as primary power, 2030-2032, at DOE Hub sites.**

⚠ REVISED [R-ai-power-followup, 2026-05-24]: Prior review assessed probability at 15-30% conditional on IRA 45V survival, hub buildout, and electrolyzer manufacturing scale. Revised down to **10-15% per hub**. The DOE Liftoff Report December 2024 update showed developer cost estimates rising to $5–7/kg — the wrong direction from the $1/kg Hydrogen Shot target. ScienceDirect 2025 EU dataset showed no clear cost reductions at large electrolyzer scale. Four conjunctive dependencies must all hold: 45V credit political survival, large-scale electrolyzer cost realization, hub buildout proceeding, and PEM 32.1% learning rate applying at utility scale. Gulf Coast HALO H2Hub remains the highest-probability geography. This is a monitored option, not a planning assumption.

**State 4 — Green H₂ for multi-day backup and seasonal firming.** The most genuinely under-pursued near-term application. The economics are not an LCOE competition — they are a capital cost comparison against diesel generators plus avoided-cost-of-lost-load for 48-168 hour outage scenarios. PEM fuel cell stack cost: ~$800-1,500/kW vs. $300-600/kW for diesel. EU ETS carbon exposure (~$65/ton CO₂ as of 2024) creates defensible NPV case for EU sites with significant backup requirements. Microsoft, Amazon, and Google all have hydrogen backup pilots that have not scaled to fleet replacement. This is the application the industry should be more seriously pursuing.

**State 5 — Green H₂ co-located with industrial offtake + data center PPAs.** The most structurally novel and underexplored configuration: a data center renewable PPA shared with an adjacent industrial hydrogen consumer (steel, ammonia, oil refining). Dual-offtake improves renewable generator load factor, creates localized clean H₂ without long-distance transport, and lets the data center claim associated carbon attributes. EU CBAM is creating structural demand pull for clean-H₂-based steel. No hyperscaler has announced this architecture publicly.

Source: IEA Global Hydrogen Review 2025; Hydrogen Power Economics 2025; arxiv:2502.12211; ScienceDirect EU PEM learning-rate dataset 2025; DOE Liftoff Report December 2024. VERIFIED for States 1-2; PENDING for States 3-5 (probabilistic assessments).

---

## Enhanced Geothermal Systems

**Technology:** Horizontal drilling approach pioneered by Fervo Energy, drawing on oil and gas industry tools. Capacity factor: 90-95% — the critical differentiator over solar (25-35%) and wind (35-45%). Produces firm, 24/7 carbon-free electricity without storage. Directly competitive with nuclear as baseload clean power.

**Status:** Fervo's Cape Station (Utah) targets 100 MW commercial operation in 2026 and 500 MW by 2028. Projected LCOE: $40-70/MWh (Fervo SEC filing, 2025; Fervo/UIPA Enhanced Geothermal Data Center Corridor, July 2025). 658 MW of PPAs signed including 320 MW with Southern California Edison and Google right-of-first-refusal on 3 GW. Google is the only hyperscaler with material contracted capacity.

**FOAK cost adjustment:** Applying the 80%-FOAK-overshoot base rate (Vogtle 4.8x, Hinkley Point C 2.5x, NuScale $58→$89/MWh before cancellation) produces a FOAK-adjusted LCOE range of **$70-140/MWh by 2028**. Even at $140/MWh, enhanced geothermal remains competitive with new nuclear ($100-200/MWh FOAK) and gas with CCS ($80-130/MWh). The relative ranking holds; the headline $40-70 figure does not survive base-rate adjustment.

**Critical falsification gate — Cape Station Phase I:** If the 100 MW Phase I project achieves capacity factor >80% and measured LCOE <$85/MWh within 12 months of commercial operation (ideally by end of 2027), Phase II (500 MW, 2028) becomes substantially more credible and rapid scaling follows. If Phase I underperforms thermally or triggers induced seismicity regulatory review, the technology reverts to the failed hot-dry-rock reference class (1970s-2000s US and European R&D that never reached commercial scale).

**Geographic advantage:** US Basin-and-Range geology (Nevada, Utah, Idaho, New Mexico, Oregon) provides the hot dry crystalline rock at accessible depths that Fervo's technology requires. This geology is largely absent in Europe outside Iceland and Italy. No rare earth or China supply chain exposure.

### Eavor Closed-Loop Geothermal

+ NEW [R-ai-power-followup, 2026-05-24]: Eavor closed-loop geothermal proved concept at Geretsried, Germany — first grid power December 2025, 4-loop system generating 8 MWe plus 64 MWth in combined-heat-and-power configuration. This is a meaningful technical milestone, but the 8 MWe per four-loop system reveals a significant scale challenge: reaching 100–500 MW firm power for a data center campus requires 50–250+ parallel systems and a coordinated drilling campaign that does not exist at that scale today.

**Timeline revision:** Eavor closed-loop is a **2035–2040 contributor** for US AI data center supply under optimistic assumptions, not a 2030–2035 lever. Open-loop EGS in the Basin and Range (Fervo-type, covered above) remains the nearer-term firm-power pathway for specific geographies. The DOE Enhanced Geothermal Earthshot target of $45/MWh by 2035 requires approximately 90% cost reduction from the 2022 baseline; DOE SunShot succeeded at a comparable task for solar PV, but no 2025–2026 on-track confirmation exists for the geothermal equivalent. [R-ai-power-followup, 2026-05-24]

Source: Fervo SEC filing 2025; Fervo/UIPA July 2025; DOE Enhanced Geothermal Earthshot. PENDING — Phase I is the evidence gate; current LCOE figures are pre-commercial. Eavor Geretsried first-grid-power December 2025 confirmed.

---

## Long-Duration Energy Storage

**Commercial gap:** LDES deployment is below 1 GWh globally as of 2024, against estimates of 100+ GW needed for meaningful renewable firming at hyperscaler scale. The sector suffers from a classic coordination failure: cannot reach cost targets without scale, and scale requires demonstrated cost competitiveness.

**Form Energy iron-air:**

⚠ REVISED [R-ai-power-followup, 2026-05-24]: The prior review cited Form Energy's $20/kWh target without flagging verification status. Three agents independently identified this figure as unverified via different analytical routes: (1) energy-market analyst via Lazard LCOS comparison — current iron-air at $35–50/kWh plus round-trip efficiency penalty yields blended LCOE of $90–115/MWh, not the sub-$80/MWh threshold implied by the $20/kWh target; (2) tech-industry analyst via source-type audit — the $20/kWh figure is a company manufacturing roadmap statement, not independently audited; (3) economics analyst via Google Minnesota deal-implied pricing — $33/kWh post-45X credits, approximately $77/kWh pre-credit. The **realistic 2030 range is $30–50/kWh installed** post-45X credits, which makes behind-the-meter economics viable but not at the optimistic blended LCOE projection. Sub-$80/MWh blended LCOE has 30–40% probability by 2028 and 50–65% probability by 2032 if Form Factory 1 scales and learning activates.

**Iron-air round-trip efficiency penalty:** Round-trip efficiency of 45–50% (versus lithium-ion at 85–90%) requires approximately 1.7–2x the solar PV capacity for equivalent net energy delivery, materially increasing land use and capital cost in any blended LCOE calculation. [R-ai-power-followup, 2026-05-24]

**Google Minnesota project:** 300 MW / 30 GWh for the 2030 timeframe; Georgia Power 15 MW / 1.5 GWh project announced 2026.

**Evidence gates:** Georgia Power 15 MW / 1.5 GWh project (first independent cost data point expected 2027–2028) gates interpretation of the Google Minnesota economics. The Google Minnesota project gates the broader hypothesis about 85–95% clean energy at hyperscaler scale.

**DOE LDES initiative:** Targets $0.05/kWh levelized storage cost. No large coordinated procurement mechanism exists to break the coordination trap, and the DOE program has not generated the equivalent of the loan guarantee structure that enabled early solar and wind scaling. The circular problem remains unresolved.

**Form Factory 1 supply constraint:** Weirton, WV, targeting 500 MW/year production — would consume approximately seven months of full-factory output for a single Google Minnesota installation. Fleet-scale hyperscaler deployment (10+ GW of LDES) requires Factory 2 and beyond, or competing iron-air manufacturers, neither of which exists as of 2026. [R-ai-power-followup, 2026-05-24]

Source: Lazard LCOS v7 2024; Form Energy public announcements; DOE LDES program documentation. PENDING — Form Energy targets are pre-scale projections; cross-agent convergence on $20/kWh unverified status from three independent analytical routes.

---

## Nuclear: SMR Scenarios and Category Disaggregation

+ NEW [R-ai-power-followup, 2026-05-24]: The follow-up review adds a Category A / Category B disaggregation that the prior review did not make explicit.

**Category A — LWR restarts and uprates (higher near-term probability):** Palisades approximately 800 MW targeting 2026 (slipped; 12–18 month schedule risk buffer applies), TMI/Crane approximately 835 MW, Duane Arnold 601 MW targeting 2029, uprate pipeline adding 2.5–5 GW through 2035. This represents the primary near-term nuclear clean-firm contribution: realistic **2–4 GW by 2030, growing to 3–5 GW by 2035**. Key risks: Palisades has already slipped from end-2025 to 2026+; Duane Arnold faces Beyond Nuclear intervention petition; NRC review queue creates simultaneous-processing pressure across 30+ uprate applications.

**Category B — Genuine new-build SMR and advanced reactor construction:** Energy-market analyst: 0.5–2 GW base case, 2–4 GW realistic-optimistic, 4–6 GW aggressive-optimistic by 2035, with the 5 GW threshold achievable only at aggressive-optimistic (approximately 20–30% probability). Reference-class analyst: 2–4 GW central estimate with 80% CI of [1 GW, 5 GW]. Cross-agent convergence on central case via independent routes.

**HALEU ceiling on aggressive-optimistic:** Centrus currently produces approximately 12 MT/year of HALEU at Piketon; combined HALEU demand for a 4–6 GW fleet across Natrium, Xe-100, Kairos KP-FHR, Oklo, and Holtec SMR-300 likely exceeds 30–50 MT/year. The 20–30% aggressive-scenario probability is conditional on HALEU supply expanding — a dependency not guaranteed by current investment trajectories. The 55x gap between current production (~900 kg/year for the first generation of designs) and fleet-scale need remains the binding constraint.

⚠ REVISED [R-ai-power-followup, 2026-05-24]: Korean APR-1400 analogy does not straightforwardly transfer to US SMR deployment. The Korean program achieved positive nth-of-a-kind learning via four conditions: design freeze across units, vertically integrated constructor-designer-operator, continuous domestic build cadence, and government-coordinated supply chain. US default multi-utility multi-state deployment structure lacks all four conditions. An alternative factory or module-level learning mechanism (rather than site-level) is what optimistic US SMR projections implicitly rely upon, but it is unproven; the burden of proof rests on demonstrating positive learning at any scale. Vogtle-style negative-or-flat learning is the historical reference class for US/EU large-reactor programs since 1995, with approximately 70–85% in that class. NuScale CFPP cancellation is the SMR-specific data point. [R-ai-power-followup, 2026-05-24]

Source: IAEA ARIS Catalogue 2024; DOE HALEU supply documentation; MIT CANES; NRC filing status as of 2026.

---

## Fusion Energy

+ NEW [R-ai-power-followup, 2026-05-24]: Fusion section not in prior review.

**Near-term (by 2040):** AI-allocated fusion capacity at **[0 GW, 12 GW] by 2040**, central estimate 1–3 GW, conditional on Commonwealth Fusion Systems ARC reaching commercial replication. CFS ARC (SPARC first plasma 2026, ARC targeting early 2030s, 400 MWe, Google 200 MW offtake signed) is the more credible near-term commercial path.

**Helion 2028 commitment:** 15–25% probability of on-time delivery. The appropriate reference class is ITER's 23+ year schedule slip against 2006 baseline and the physicist-survey record (time-to-commercial fusion estimates have barely changed across 30 years of surveys), not Helion-specific physics milestones.

**Long-term (by 2050):** AI-allocated fusion at **[0 GW, 60 GW]** by 2050, central estimate 10–25 GW. This is a potential marginal contributor, not a planning assumption for the 2025–2040 window.

**ITER irrelevance to AI power:** ITER revised timeline (operation 2034, D-T operation 2035) means it generates no electricity and is a research device — irrelevant to AI power before 2040.

**Planning implication:** Fusion should not appear as a planning assumption in infrastructure decisions for the 2025–2040 window. It is a tail-probability contributor by 2040 and a marginal contributor at central estimate by 2050. [R-ai-power-followup, 2026-05-24]

Source: CFS public disclosures; Helion/Microsoft agreement; ITER revised schedule 2024; physicist survey literature. PENDING — all fusion commercial timelines are pre-commercial projections.

---

## Workload Flexibility and Curtailment Absorption

**The immediately actionable lever** is not a generation technology. It is treating AI training workloads as flexible, interruptible load that can shift consumption to times and places where clean electricity is abundant and cheap.

**Curtailment data (2024):** Texas curtailed ~5-10 TWh wind and solar (ERCOT 2024); California curtailed ~3.4 TWh (CAISO); US total major-grid curtailment ~15-20 TWh (EIA). Renewable buildout is outpacing transmission capacity; curtailment is growing.

**Opportunity:** A 500 MW AI training campus co-located with high-curtailment grid zones (West Texas, Mojave) could potentially source 20-40% of annual training energy at near-zero marginal cost through interruptible-load tariff structures that ERCOT and CAISO already offer to industrial customers.

**Google precedent:** Running carbon-aware training operations since 2020, shifting workloads to lower-carbon grid hours; reported 2-3% efficiency loss for 30%+ emissions reduction. No other hyperscaler has deployed this approach at material scale.

**Economics:** GPU opportunity costs (depreciation + foregone revenue) exceed dollar-value of electricity savings at $50/ton carbon. Analysis reverses above $150-200/ton. Microsoft's internal carbon price (~$100/ton, highest among major tech) approaches this threshold.

**Scope limitation:** Inference workloads are latency-sensitive and cannot be temporally shifted. Large training runs incur 10-30% overhead from mid-job interruption (arxiv:2605.03751). For the training share (~60% of current AI electricity consumption, concentrated at fewer than 50 sites globally), this is a 0-2 year, near-zero-capital intervention that has been largely ignored.

✓ Confirmed by [R-ai-power-followup, 2026-05-24]: Flexible AI training load deferral identified as a near-term bridge mechanism, with 3–21% cost reduction per arxiv:2604.05376.

Source: ERCOT 2024; EIA; CAISO; Google CFE-365 reports; Phadke et al. LBNL 2024; arxiv:2605.03751. VERIFIED for curtailment data; Google approach VERIFIED from company reporting.

---

## Transmission Backbone

**Prior status (brief summary):** ~80-200 TWh clean-power gap partly attributable to transmission constraints; PJM interconnection queue backlog of 8+ years.

⚠ REVISED [R-ai-power-followup, 2026-05-24]: Transmission section materially updated.

**Realistic US interregional capacity addition by 2035: approximately 10–22 GW**, materially below the NERC ITCS-identified 35 GW minimum need. Historical pace since 2014: approximately 0.6 GW/year large-scale interregional transmission, versus 3.9 GW/year required to meet the NERC 35 GW target. Binding constraints are structural and co-equal: state-federal jurisdiction fragmentation, cost allocation disputes across RTO seams, eminent domain variability by state, NIMBY opposition.

**Key projects:** SunZia HVDC approximately 3 GW, Champlain Hudson Power Express approximately 1.25 GW, Grain Belt Express Phase 1 approximately 5 GW (DOE $4.9B loan terminated July 2025, pursuing private financing), TransWest Express approximately 3 GW, SOO Green approximately 2.1 GW. Optimistic total 14–15 GW, realistic 10–12 GW.

**MISO Tranche 2.1 — factual correction:** MISO Tranche 2.1 ($21.8B, 3,631 miles, approved December 2024, in-service 2032–2034) enables significant intra-MISO renewable capacity. This is intra-MISO capacity, NOT interregional RTO-to-RTO transfer, and does NOT count toward the NERC 35 GW interregional gap. MISO T2.1 is sometimes misattributed in discussion of interregional capacity expansion — it addresses a different metric.

**Reconductoring wildcard:** Reconductoring of existing lines could add 10–20 GW of effective interregional capacity without new right-of-way disputes, potentially raising the upper bound to 22–30 GW under optimistic assumptions. Does not change the core conclusion that the NERC 35 GW need will not be met by 2035. [R-ai-power-followup, 2026-05-24]

Source: NERC ITCS; MISO Tranche 2.1 approval documentation; individual project filings. VERIFIED for MISO T2.1 intra-regional characterization.

---

## Gas as the Bridge: The Uncomfortable Reality

**What is actually happening:** In PJM's TC1 interconnection queue, natural gas is the single largest source by application, with 106 GW of new gas generation in queue. Gas clears interconnection faster than any other source and can reach commercial operation within 2-3 years. Advanced nuclear and enhanced geothermal cannot deliver electrons at the speed AI data center buildout is proceeding.

**Hyperscaler commitment divergence:**
- **Google (CFE-365 standard):** 24/7 carbon-free hourly matching — every consumption hour matched to carbon-free generation in the same grid region. ~65% hourly matching achieved 2023; 100% target 2030. Contracted nuclear (TMI co-investor) and geothermal (Fervo). Has not publicly announced support for new gas plants.
- **Microsoft, Amazon, Meta (annual REC standard):** Annual totals balanced rather than hourly coverage — a structurally weaker commitment. Microsoft's 2025 sustainability report: energy use up 168%, emissions up 23.4% vs. 2019 baseline. Natural gas turbines are powering Stargate construction in West Texas. Under GHG Protocol's proposed hourly matching revisions (WattTime December 2025 analysis: would fail 65-75% of current corporate clean-energy claims), these commitments would not hold up.

**Historical base rate for bridge fuels:** US natural gas was framed as a 20-year bridge to clean energy in 2004-2008 policy documents. Gas generation has grown from ~20% to 40% of US electricity supply since then. Combined-cycle plants commissioned 2026-2030 carry 30-year operational lifespans (operating through 2056-2060). The "bridge" frame has an 85-95% entrenchment base rate historically; three of five agents (3/5 convergence point) treating gas as the realistic gap-filler for 5-10 GW that announced nuclear PPAs will not deliver on schedule.

**Methane leakage:** Satellite-based measurements (Alvarez et al., Science 2018; Lyon et al., 2021) put actual leakage at 2.3-3.7% vs. EPA inventory estimate of 1.5%. Energy Policy (January 2025): "two-thirds of the emissions reductions" from coal-to-gas switching "disappear" when methane leakage is properly accounted for.

**Market signal:** PJM December 2025 capacity auction cleared at $269.92/MW-day — an 800% year-over-year increase — sending a strong price signal for more gas construction.

✓ Confirmed by [R-ai-power-followup, 2026-05-24]: 85-95% bridge-fuel entrenchment base rate confirmed in direction. See next section for mechanism reframe.

Source: PJM TC1 published data; Microsoft 2025 sustainability report; Google CFE-365 reports; WattTime December 2025; Alvarez et al. Science 2018; Energy Policy January 2025; Brander M. et al. 2018; Bjørn A. et al. 2022. CONVERGED across independent agents on the commitment-divergence finding.

---

## The Gas Reality Reframe: Distributed Entrenchment

+ NEW [R-ai-power-followup, 2026-05-24]: This section is the central analytical contribution of the follow-up review. The prior review treated bridge-fuel entrenchment as operating primarily through utility-scale CCGT filling the AI power gap via the PJM TC1 106 GW queue. The follow-up establishes that this mechanism is physically constrained by OEM supply, and that the substitute mechanism — distributed RICE fleets and intensified existing-fleet utilization — is itself a form of fossil entrenchment that may be harder to unwind.

**OEM supply ceiling on central CCGT:** GE Vernova's Q1 2026 backlog reached 100 GW with CEO stating turbines are "sold out through 2030 by end of 2026" and approximately 10 GW of manufacturing capacity remaining through 2030. Siemens Energy holds a record 58 GW backlog (year-end 2025), with S&P Global confirming US gas-fired turbine wait times "as much as seven years." Mitsubishi Power backlog approaches 30 GW plus 20 GW in reservation agreements, with plans to double manufacturing capacity over two years. Combined three-OEM global manufacturing capacity of approximately 30–35 GW/year, expanding to approximately 40 GW/year by 2028, against combined backlogs of approximately 190 GW — representing more than five years of current production.

**PJM TC1 queue is not a delivery schedule:** Projects without already-reserved turbine slots face 5–7 year wait times from order placement. Combined with historical PJM queue-to-commercial-operation attrition of approximately 30–50%, realistic CCGT additions to the PJM system by 2030 from TC1 projects are materially lower than the 106 GW nominal — approximately 20–40% of nominal capacity at base case.

**Actual near-term bridge mechanisms:**
1. Distributed RICE engines (Wärtsilä, Caterpillar, Cummins, Bergen) — 12–24 month lead times versus 5–7 years for CCGT
2. Aeroderivative turbines — faster installation but still subject to GE Vernova's broader backlog pressure
3. Existing CCGT fleet running at higher capacity factors — no new turbine required, lowest-friction bridge
4. Flexible AI training load deferral — 3–21% cost reduction per arxiv:2604.05376

**Distributed generation is parallel gas entrenchment, not a clean-power pathway:** Reference-class analyst: US CHP has plateaued at approximately 7% of national capacity since 1990; US microgrids represent 0.4% of installed capacity; approximately 95% of announced 2024–2026 hyperscaler on-site capacity is gas-fired (Crusoe Stargate Abilene 1.2–2.1 GW gas-turbine, Pacifico GW Ranch Pecos 1 GW gas, Nscale Monarch WV 2 GW RICE-gas, Edged Energy Atlanta 168 MW diesel-gas; fuel-cell microgrid is exception case below 5% of aggregate MW). The distributed pathway absorbs an estimated 20–30% of hyperscaler new-build capacity 2026–2035 (80% CI [15%, 40%]).

**Cross-agent convergence (gold-standard finding):** Energy-market analyst via OEM supply economics and reference-class analyst via historical base-rate and project-mix decomposition independently arrived at the same conclusion: distributed RICE + existing fleet intensification is the actual bridge mechanism. Hyperscaler on-site generation announced as "22% growth" is parallel gas entrenchment, not a clean-power alternative.

**BTM gas: no PUC retirement pathway (reinforces stranded-asset risk):** RICE engines run at 40–48% thermal efficiency versus 55–62% for combined-cycle CCGT — more gas burned per MWh of AI output, higher emissions intensity per unit. A fleet of 500 × 10 MW RICE units distributed across many permitting jurisdictions is operationally harder to coordinate for retirement than 10 × 500 MW CCGT plants. Critically, BTM gas has no public utility commission pathway to retirement — PUC-regulated central CCGT can be retired through state rate-base proceedings; BTM gas has no equivalent regulatory mechanism. Existing fleet running harder extends operational life of units that would otherwise retire, creating stranded-asset exposure in the existing fleet rather than just new builds. The prior review's stranded-asset exposure ($200–400B by 2045 if decarbonization politics shift) is maintained and potentially increased by this mechanism shift. [R-ai-power-followup, 2026-05-24]

Source: GE Vernova Q1 2026 earnings; Siemens Energy backlog year-end 2025; Mitsubishi Power backlog; S&P Global; PJM TC1 data; reference-class analyst project-mix decomposition. CONVERGED across two independent analytical routes (gold-standard finding).

---

## Multi-Axis Sustainability: Water Matrix

Carbon is not the only binding constraint. Water is the binding constraint in the US Southwest.

| Technology | Operational water consumption |
|---|---|
| Wind onshore | ~0.001 L/kWh — negligible |
| Solar PV (dry-cooled) | ~0.01-0.05 L/kWh — minimal |
| Enhanced geothermal, closed-loop (Fervo-type) | ~0.1-0.4 L/kWh — low; closed-loop recycled |
| Natural gas CCGT | ~0.5-2.0 L/kWh |
| Nuclear, light water reactor | ~1.5-3.0 L/kWh |
| Gas + CCS | ~0.87-5.0 L/kWh (calibration gap across sources — see note) |
| Green hydrogen via electrolysis (full chain) | ~6-15 L/kWh delivered — highest of any clean option |

**Calibration gap note for gas + CCS:** NREL lifecycle harmonization (Meldrum et al., 2013, IOP; n=165 estimates), UNECE lifecycle assessment (2021), and USGS produce different mid-points across the 0.87-5.0 L/kWh range. Direction is clear — CCS adds substantial water load vs. unabated gas; magnitude is uncertain.

**Colorado River basin states** (Arizona, Nevada, Utah) have operated under Tier-1 and Tier-2 shortage declarations since 2021; May 2026 seven-state conservation agreement falls short of the structural deficit. Texas data center clusters face growing groundwater competition.

**Technology ranking flip under water stress:** For firm clean power at Western US sites, the ranking reverses — enhanced geothermal closed-loop and solar PV are the only ≥100 MW options with both low-carbon AND low-water profiles. Nuclear faces real water constraints in Texas and Arizona. Gas with CCS has among the worst water profiles of any generation option, undermining its positioning as a "clean bridge."

**Green hydrogen's hidden water disadvantage:** Electrolysis requires ~9 liters of water per kg of H₂, compounding to 6-15 L/kWh at current round-trip efficiencies. Economics and water arguments point in the same direction against green H₂ for primary power in water-stressed Western US locations.

Source: NREL Meldrum et al. (IOP, 2013); UNECE 2021; USGS; NREL TP-550-50900. VERIFIED for wind/solar/nuclear mid-points; gas+CCS PENDING (calibration gap flagged).

---

## Land Use

+ NEW [R-ai-power-followup, 2026-05-24]: Land use section not in prior review.

Land use is transitioning from manageable cost to binding political constraint at leading-edge data center locations in the 2025–2030 window, but it is not a national capacity cap.

**Locally binding, nationally non-binding:** Loudoun County, Virginia (March 2025, 7-2 bipartisan) eliminated by-right data center development, requiring special exception proceedings. Prince William County, Virginia had its Digital Gateway rezoning voided in March 2026. Maricopa County, Arizona introduced the first US data-center-specific ordinance. The European precedent (Dublin, Warsaw, Madrid following London-Frankfurt-Amsterdam restrictions on a 3–5 year lag) suggests this pattern spreads. Even if Loudoun-style restrictions reach 8–10 additional counties, 3,000+ US counties have not imposed restrictions — the constraint is locally binding at prime locations but nationally non-binding.

**NEPA timeline as real binding variable for generation siting:** The relevant binding variable is NEPA environmental review timelines (3–5 years for large utility-scale federal land projects), not BLM land quantity (19M+ acres designated open for utility solar). EU Projects of Common Interest fast-track comparison: 12–18 months for comparable projects versus 3–5 years US.

**BTM solar + LDES land constraint:** The hybrid configuration at hyperscaler campus scale requires 15,000–25,000 acres for the solar component, limiting the configuration to Sun Belt geographies (Texas, Arizona, Nevada, New Mexico, California desert). [R-ai-power-followup, 2026-05-24]

Source: Loudoun County Board proceedings March 2025; Prince William County rezoning record March 2026; BLM land designation database. VERIFIED for Loudoun and Prince William County actions.

---

## Materials Supply Chain Constraints

**HALEU (High-Assay Low-Enriched Uranium):** Required by advanced nuclear designs including Kairos, X-energy Xe-100, and TerraPower Natrium. Russia holds **100% of commercial HALEU production** as of 2026. Centrus produced ~900 kg in 2024 against projected demand exceeding 50 metric tons/year by 2035 — a 55x gap. Western investment of $4.2 billion (DOE $2.7B + Urenco + Orano) targets partial domestic production by 2027-2030, sufficient for 2-4 FOAK reactors. Fleet-scale deployment of HALEU-dependent designs before 2030 is physically impossible under current supply trajectories.

⚠ REVISED [R-ai-power-followup, 2026-05-24]: HALEU ceiling clarified as the binding constraint on Category B SMR aggressive-optimistic scenarios. Centrus approximately 12 MT/year at Piketon versus aggregate demand of approximately 30–50 MT/year for a 4–6 GW fleet across HALEU-dependent designs. The 20–30% aggressive-scenario probability from the energy-market analyst is conditional on HALEU supply expanding — an unresolved dependency not captured in the prior framing. [R-ai-power-followup, 2026-05-24]

**Green hydrogen electrolyzers:** China has built **85% of global alkaline electrolyzer manufacturing capacity** and holds dominant positions in all upstream supply chains (6 of the top 10 global electrolyzer manufacturers are Chinese; Asia Times/Pacific Forum; FCHEA). Chinese alkaline electrolyzers: $300-500/kW vs. $750-1,300/kW for Western equivalents. This is a cost and availability risk under IRA Section 45V domestic content provisions — not a physical supply cutoff risk in the near term. China has not restricted electrolyzer exports the way it has rare earth metals.

### Silver Constraint and Copper-Substitution Relief Valve

+ NEW [R-ai-power-followup, 2026-05-24]: Solar silver is an underappreciated emerging constraint. Photovoltaic demand could account for 29–41% of projected global silver supply by 2030 under static technology assumptions; total demand may exceed supply 30–38% at high solar deployment.

**Copper-metallization relief valve:** The copper-metallization substitution pathway (active development in HJT and TOPCon cell architectures; TOPCon at approximately 13 mg/W silver; if copper-metallization reaches 50% market share by 2030, silver demand from solar decreases by approximately 260 million ounces annually) is a documented relief valve that the raw silver constraint finding must not underweight. Under non-static technology assumptions, solar silver is a **5–15% cost-pressure constraint** on solar deployment trajectory, not a binding supply cap on AI power buildout. [R-ai-power-followup, 2026-05-24]

**PEM electrolyzer PFAS:**

⚠ REVISED [R-ai-power-followup, 2026-05-24]: Prior characterization as "problematic" should be revised. An October 2025 study via EPA Method 1633 detected no PFAS during normal PEM operation — this is the key finding that shifts the risk assessment. Manufacturing and disposal regulatory exposure is real under EU REACH 2.0, but industry-specific electrolyzer exemptions are politically expected given EU hydrogen strategy. Revised characterization: **"regulatory monitoring required — likely manageable via industry-specific exemptions."** [R-ai-power-followup, 2026-05-24]

**Battery supply-chain concentration risk is chemistry-specific:** NMC (cobalt-bearing): DRC supplies approximately 73–76% of global cobalt mine output and China holds approximately 80% of cobalt refining. LFP (cobalt-free): reduces but does not eliminate concentration risk; lithium imports 97% from Chile/Argentina, China holds processing dominance. Iron-air (Form Energy: iron, water, air): substantially escapes concentration risk and is the supply-chain-resilient choice, contingent on commercialization.

**Wind rare earth risk:** Rare earths for direct-drive wind (China holds approximately 85–90% of global rare-earth processing) are unaddressed by copper substitution (solar relief) or iron-air (battery relief). No documented relief valve for this risk.

Source: IEA/NEA Red Book; World Nuclear Association; DOE HALEU supply documentation; Asia Times/Pacific Forum; FCHEA; EPA Method 1633 (October 2025). VERIFIED for HALEU monopoly claim; China electrolyzer share VERIFIED; PFAS finding from EPA Method 1633 October 2025.

---

## Country-Comparative Positioning

**Advanced nuclear (HALEU-dependent):** US-advantaged. ADVANCE Act (2024) streamlines NRC licensing; IRA Sections 45U/45J provide production credits; DOE is primary HALEU investment vehicle. EU is slower (France exception: French nuclear revival policy active). Both face Russia-HALEU chokepoint equally.

**Enhanced geothermal:** US-advantaged. Basin-and-Range geology provides hot dry crystalline rock at accessible depths; largely absent in Europe outside Iceland and Italy. US oilfield services capacity is the critical technology-transfer enabler. No rare earth or China supply chain exposure.

**Green hydrogen electrolyzers:** EU regulatory framework (REPowerEU; EU Hydrogen Bank; IPCEI) is historically stronger than US. However, EU RED III Article 28's hourly-matching requirement for renewable fuel of non-biological origin certification forces EU green H₂ production to follow solar/wind generation curves at 25-40% capacity factor rather than 90%+ achievable with continuously-running electrolyzers. This makes EU green hydrogen more expensive than the policy architecture implies — the cost math is harder than it looks.

**Solar PV:** Both US and EU disadvantaged by China's 93-97% dominance of polysilicon and wafer manufacturing. IRA Section 45X credits driving First Solar/Qcells investment, but the 2027 IRA Section 48E ITC cliff (expires for wind/solar placed in service after December 31, 2027) creates a compressed 24-month window. Nuclear's Section 45U and hydrogen's Section 45V credits remain intact through this cliff.

Source: IEA/NEA; ADVANCE Act 2024; IRA Sections 45U/45J/45V/45X/48E; EU RED III Article 28; European Commission REPowerEU. VERIFIED for statutory details; advantage assessments are directional.

---

## Hyperscaler Procurement Tiers

Two distinct procurement standards exist, with materially different sustainability implications:

**Tier A — CFE-365 (Google):** 24/7 carbon-free electricity matching, hourly, in the same grid region as consumption. Currently ~65% hourly matching (2023); target 100% by 2030. Requires contracted nuclear and geothermal to cover non-solar/wind hours. The only major hyperscaler operating at this standard.

**Tier B — Annual REC matching (Microsoft, Amazon, Meta):** Annual total renewable energy certificates balance annual consumption totals. Does not ensure any given hour is covered by clean power. Under GHG Protocol proposed hourly matching revisions (WattTime December 2025), 65-75% of current corporate clean-energy claims under this standard would fail. Microsoft's operational behavior (168% energy increase, 23.4% emissions increase vs. 2019 baseline) is consistent with rapid data center buildout on gas-as-bridge with annual REC cover.

Implication for analysis: when hyperscalers claim "100% renewable energy," the claim is structurally ambiguous without knowing which tier applies. The Google commitment is substantially more constraining and credible than the MSFT/AMZN/Meta standard. [R-sustainable-ai-power, 2026-05-22]

Source: Google CFE-365 whitepaper and progress reports; Microsoft 2025 sustainability report; WattTime December 2025; GHG Protocol Scope 2 Guidance; Princeton ZERO Lab; Brander M. et al. 2018. CONVERGED on Tier A vs B distinction; specific claim rates PENDING full GHG Protocol revision publication.

---

## Google Minnesota: Utility-Structured, Not True BTM

⚠ REVISED [R-ai-power-followup, 2026-05-24]: The Google Minnesota project (300 MW/30 GWh Form Energy iron-air, 1,400 MW wind and 200 MW solar, approximately $1B capital commitment, 2028 installation scheduled) was mischaracterized in prior analysis as "behind-the-meter solar + LDES hybrid." This overstates self-sufficiency.

**Structural reality:** The project is structured through Xcel Energy's Clean Energy Accelerator regulatory framework, with Xcel managing grid integration. Google bears capital cost but energy flows through the utility framework. The Clean Energy Accelerator is a Minnesota-Xcel-specific regulatory instrument that does not exist in PJM, ERCOT, or CAISO. Replication in deregulated markets requires true BTM interconnection agreements and islanding-capable architecture — substantially more complex.

**Correct characterization:** "Utility-partnered LDES at hyperscaler anchor-tenant scale" rather than "true BTM." The configuration is significant as a model and an empirical gate for LDES economics; its replicability is jurisdiction-specific.

**LCOE correction:** At Lazard's $35–50/kWh iron-air plus the 45–50% round-trip efficiency penalty (requiring approximately 1.7–2× solar oversizing for equivalent net energy delivery), blended LCOE at 500 MW campus scale is approximately **$90–115/MWh**, not the optimistic $70–90/MWh range. Sub-$80/MWh requires Form Energy achieving its unverified $20/kWh manufacturing target. [R-ai-power-followup, 2026-05-24]

Source: Xcel Energy Clean Energy Accelerator regulatory filings; Form Energy/Google announcement; Lazard LCOS v7. Cross-agent convergence on LCOE from three independent analytical routes.

---

## Waste-Heat Recovery and District Heating

+ NEW [R-ai-power-followup, 2026-05-24]: Not in prior review.

**Technology status:** Waste-heat recovery is technically mature and operating at scale in Northern Europe. Stockholm Exergi's Open District Heating connects 30+ data centers to a 3,000 km network warming approximately 30,000 apartments annually. Microsoft-Fortum in Finland supplies approximately 40% of district heating demand for 250,000 people (live approximately 2026). EU Energy Efficiency Directive Article 23 (effective October 2025) mandates waste-heat assessment and cost-benefit analysis for all EU data centers above 1 MW.

**US adoption timeline — 2035–2045:** Three structural barriers are conjunctively binding on the 2030 horizon, not individually insurmountable but together making meaningful US scale-up implausible before 2035:

1. **Infrastructure absence:** US has approximately 660 district heating systems (IDEA database), covering roughly 2% of the built environment versus approximately 50% in Nordic countries and approximately 13% in Germany. The Stockholm 3,000 km network took 70+ years to build.

2. **Cooling architecture default:** US data centers default to air-cooled architectures. Waste heat recovery requires warm-water cooling loops operating at 40–60°C supply temperature. Retrofitting existing air-cooled facilities costs approximately $2–8M per MW.

3. **Regulatory and commercial framework:** Virginia HB323 (2026), the first US data center waste-heat reuse bill, directs convening a working group — a pre-feasibility step, not a deployment mandate. No US equivalent of EU EED Article 23 mandate exists.

**Realistic US path:** Industrial co-location (data center waste heat to industrial process heating, bypassing residential district heating buildout) is the realistic near-term US pathway. Minneapolis, Chicago, Boston, and NYC are the highest-probability geographies given existing heat network infrastructure. Revenue math: at Stockholm's approximately €190,000/MW annually on 50 MW thermal output, the offset is approximately $10–20/MWh equivalent — material for a European site with EU ETS carbon value, but substantially weaker in US absent carbon pricing. [R-ai-power-followup, 2026-05-24]

Source: Stockholm Exergi public data; Microsoft-Fortum Finland announcement; EU EED Article 23 text; IDEA database; Virginia HB323 (2026). VERIFIED for Stockholm and EU EED Article 23 mandate.

---

## Waste and End-of-Life Profiles

+ NEW [R-ai-power-followup, 2026-05-24]: End-of-life section not in prior review.

Waste and end-of-life profiles differ materially by technology on a 30-year planning horizon.

**Spent nuclear fuel:** Approximately 70,000–90,000 metric tons of heavy metal accumulated at US reactor sites, approximately 2,000 MTHM/year generation. Yucca Mountain NRC license in administrative indefinite suspension; Congressional action required. No interim consolidated storage facility operating. The 40-year dry-cask safety record is clean (no operational safety incidents), but regulatory complexity and cost are real 30-year liabilities for procurement planning.

**PEM electrolyzer PFAS:** See Materials section above — October 2025 EPA Method 1633 finding of no PFAS during normal operation revises risk downward. Manufacturing and disposal exposure real under EU REACH 2.0, but likely manageable via industry-specific exemptions.

**PV recycling:** EU WEEE Directive mandates 85% recovery and 80% recycling targets. US: Washington state-only mandatory take-back; no federal mandate. Approximately 24.93 million tonnes of US PV waste expected 2025–2050, representing approximately $189B in recoverable material value — sufficient private-sector incentive for recycling market development even without a federal mandate.

**GPU e-waste:** Global 22.3% recycling rate (UN GEM 2024). AI server refresh cycles compressing from traditional 5–7 years to 18–36 months, materially accelerating end-of-life volume at industry-wide level. Industry leaders (Oracle 99.6%, Microsoft 90.9%) have circular datacenter programs; 12% of data centers have zero e-waste programs.

**Iron-air end-of-life:** Iron oxide as primary reaction product, no hazardous materials, mature metal recycling stream — the most benign end-of-life profile among the storage technologies evaluated. [R-ai-power-followup, 2026-05-24]

Source: NRC dry-cask storage safety data; EU WEEE Directive; UN GEM 2024; Oracle/Microsoft circular economy reports. VERIFIED for EU WEEE targets; US PV waste projection PENDING independent verification.

---

## Sources (Abbreviated)

IEA "Energy and AI" 2025; IEA Global Hydrogen Review 2025; DOE Liftoff Report December 2024; BNEF New Energy Outlook 2024; Lazard LCOE v17 (June 2024); Lazard LCOS v7; Fervo Energy SEC filing 2025; Fervo/UIPA Enhanced Geothermal Data Center Corridor (July 2025); DOE Enhanced Geothermal Earthshot; DOE Hydrogen Hub documentation; NREL Meldrum et al. (IOP, 2013); UNECE 2021; USGS; PJM TC1 published data; ERCOT 2024; EIA; CAISO; IEA/NEA Uranium Red Book; World Nuclear Association; DOE HALEU supply chain documentation; IRA Sections 45U/45J/45V/45X/48E; EU RED III Article 28; EU CRMA; EU Energy Efficiency Directive Article 23; European Commission REPowerEU; IAEA ARIS Catalogue 2024; NERC ITCS; MISO Tranche 2.1 approval documentation; GE Vernova Q1 2026 earnings; Siemens Energy backlog year-end 2025; Mitsubishi Power backlog data; S&P Global gas turbine lead-time data; arxiv:2502.12211; ScienceDirect EU PEM electrolyzer learning-rate dataset 2025; Alvarez et al. (Science, 2018); Energy Policy (January 2025); GHG Protocol Scope 2 Guidance; WattTime December 2025; Google CFE-365 reports; Microsoft 2025 sustainability report; Phadke et al. LBNL 2024; arxiv:2605.03751; arxiv:2604.05376; RMI; Asia Times/Pacific Forum; FCHEA; ADVANCE Act 2024; EPA Method 1633 (October 2025); Stockholm Exergi public data; IDEA database; Virginia HB323 (2026); MIT CANES; CFS public disclosures; Helion/Microsoft agreement; ITER revised schedule 2024; UN GEM 2024; Loudoun County Board proceedings March 2025; Prince William County rezoning record March 2026; BLM land designation database; Epoch AI frontier training projections; Xcel Energy Clean Energy Accelerator regulatory filings.
