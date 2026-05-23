# Powering AI Sustainably: What Works, What Doesn't, and What's Being Missed

## The Short Answer

Powering AI data centers sustainably is an unsolved problem with a widening gap, not a problem on the verge of being solved. The gap between AI electricity demand and available clean supply is real and will persist through 2030 under any realistic scenario. The hydrogen fuel cell example from the question is largely a null finding — green hydrogen is correctly deprioritized for AI primary power at current economics — but that verdict conceals a more interesting picture once you disaggregate by use case and time horizon. More importantly, several genuinely under-pursued options exist, and the most actionable one is not a generation technology at all.

US data center electricity demand is approximately 200 TWh in 2025 and is projected to reach roughly 440 TWh by 2030 — a 130% increase over six years (IEA "Energy and AI," 2025). The EU will grow from approximately 70 TWh to 115-170 TWh over the same period. Against that demand, clean supply additions are structurally backlogged: the average wait for grid interconnection in PJM, the largest US power market, has grown from under two years in 2008 to over eight years today (RMI; PJM interconnection reform filings). The result is a clean-power gap of approximately 80-200 TWh in the US and 30-60 TWh in the EU through 2030, directionally high-confidence though sensitive to both demand and supply assumptions at the margin (IEA 2025; S&P Global 2025; BNEF 2024). The range is wide because IEA's 2016 data center forecasts overshot 2020 actuals by a factor of two — but 2025 actuals are tracking the high scenario, and AI training workloads are structurally unlike prior data center demand classes.

Hyperscalers have announced more than 10 GW of nuclear power purchase agreements since 2024 — Microsoft's Three Mile Island restart (835 MW), Google's Kairos SMR fleet (500 MW), Amazon's X-energy deal, Meta's 1-4 GW nuclear RFP, and others. The announced figure is misleading. Drawing on announced-versus-realized base rates from analogous energy infrastructure buildouts (LNG, offshore wind, gas pipelines: 10-25% of announced capacity typically reaches commercial operation on schedule), the realistic figure operating by 2030 is 2-5 GW — primarily the TMI restart (2027 delivery) and possibly one or two additional nuclear restarts. Zero commercial small modular reactors are operating anywhere in the Western world as of mid-2026, and all SMR first-of-kind delivery dates are 2030 or later (IAEA ARIS Catalogue, 2024; nuclear utility filings). The headline 10 GW should be read as serious procurement intent, not near-term supply.

---

## The Hydrogen Question

The answer to whether hydrogen fuel cells are an overlooked opportunity depends almost entirely on which variant of the technology you are asking about. Five distinct situations look quite different from each other.

**Gray and blue hydrogen fuel cells (gas-reformed, deployed now).** Companies including Equinix, AT&T, Apple, and Google have deployed roughly 1% of US data center primary power through Bloom Energy solid oxide fuel cells running on natural-gas-reformed hydrogen. These are commercially operational and not under-pursued. They reduce criteria air pollutants compared to diesel backup but retain approximately 80-90% of natural gas lifecycle greenhouse gas emissions — a sustainability improvement at best marginal from a carbon standpoint.

**Green hydrogen as primary power, 2026-2028.** This is the use case most people have in mind and the verdict is clear: correctly deprioritized, not overlooked. Current green hydrogen production costs $4-8 per kilogram globally (IEA Global Hydrogen Review, 2025). Running solid oxide fuel cells on that hydrogen produces electricity at $130-180 per MWh — two to three times the cost of behind-the-meter solar plus four-hour battery storage at $60-80 per MWh delivered (Hydrogen Power Economics 2025; arxiv:2502.12211 techno-economic analysis). Amazon reportedly abandoned Bloom Energy fuel cell deployments. Microsoft's most visible hydrogen test was a 48-hour proof of concept at Cheyenne, not a production deployment. The $7.65 billion in announced fuel cell deals in late 2025 and early 2026 was predominantly gas-reformed, not green hydrogen. The non-pursuit reflects rational capital allocation.

**Green hydrogen as primary power, 2030-2032, at DOE Hydrogen Hub sites.** The picture changes at a specific geography and time horizon. Proton exchange membrane electrolyzer manufacturing has a 32.1% learning rate (ScienceDirect EU dataset, 2025). At 40 GW of cumulative global installed capacity, production costs reach approximately $2 per kilogram, at which point fuel cell electricity costs fall to $60-80 per MWh — within competitive range. The probability this threshold is reached by 2030-2032 is roughly 15-30%, conditional on the IRA Section 45V production credit surviving, DOE Hydrogen Hub buildouts proceeding, and electrolyzer manufacturing scaling adequately. It is not null at this horizon; it is probabilistically small and geographically concentrated near hub sites in the Gulf Coast and Appalachian regions (IEA Global Hydrogen Review 2025; EA learning-rate analysis from ScienceDirect).

**Green hydrogen for multi-day backup and seasonal firming.** This is the most genuinely under-pursued near-term application. The economics of backup power are not an LCOE comparison against grid generation — they are a capital cost comparison against diesel generators and an avoided-cost-of-lost-load calculation for 48-168 hour outage scenarios. A proton exchange membrane fuel cell stack costs roughly $800-1,500 per kilowatt compared to $300-600 per kilowatt for diesel, but the ongoing fuel cost advantage and EU Emissions Trading System carbon exposure ($65 per ton CO2 as of 2024) create a defensible NPV case at sites with significant backup requirements. Microsoft, Amazon, and Google all have hydrogen backup pilots that have not scaled to fleet replacement. This is the application the industry should be more seriously pursuing.

**Green hydrogen co-located with industrial offtake and data center renewable PPAs.** The most structurally novel and genuinely underexplored opportunity is a configuration in which a data center renewable power purchase agreement is shared with an adjacent industrial hydrogen consumer — steel production, ammonia, or oil refining. The dual-offtake structure improves the economics for the renewable generator (improving load factor), creates a localized clean hydrogen supply without long-distance transport, and lets the data center claim the associated carbon attributes. EU CBAM (Carbon Border Adjustment Mechanism) is creating structural demand pull for clean-hydrogen-based steel that makes this configuration more attractive. No hyperscaler has announced this architecture publicly.

---

## What Is Genuinely Under-Pursued

Beyond hydrogen sub-segments, three categories stand out as meaningfully under-pursued relative to their actual potential.

### Enhanced Geothermal Systems

Advanced enhanced geothermal systems — specifically the horizontal drilling approach pioneered by Fervo Energy drawing on oil and gas industry tools — represent the most commercially credible firm-power option that is not yet being pursued at scale. Fervo's Cape Station project in Utah targets 100 MW of commercial operation in 2026 and 500 MW by 2028, with a projected LCOE of $40-70 per MWh (Fervo SEC filing, 2025; Fervo/UIPA Enhanced Geothermal Data Center Corridor, July 2025). The company has signed 658 MW of power purchase agreements including a 320 MW deal with Southern California Edison and a Google right-of-first-refusal on 3 GW.

The capacity factor of 90-95% is the critical differentiator. Unlike solar (25-35%) or wind (35-45%), enhanced geothermal produces firm, 24/7 carbon-free electricity without storage. That makes it directly competitive with nuclear as a baseload clean power source, at a fraction of the nuclear construction cost and timeline.

However, the $40-70/MWh figure warrants genuine caution. Applying the same FOAK (first-of-a-kind) cost overrun base rate that applies to other novel energy infrastructure — roughly 80% of major FOAK energy projects have exceeded initial cost estimates by more than 20%, with examples including Vogtle (4.8x original estimate), Hinkley Point C (2.5x), and NuScale's cancelled project ($58 → $89/MWh before cancellation) — produces a FOAK-adjusted LCOE range of $70-140 per MWh by 2028. Even at $140/MWh, enhanced geothermal remains competitive with new nuclear ($100-200/MWh FOAK) and gas with carbon capture ($80-130/MWh). The relative ranking holds; the absolute cost claim does not.

The critical evidence gate is Cape Station Phase I. If the 100 MW Phase I project achieves a capacity factor above 80% and a measured LCOE below $85 per MWh within 12 months of commercial operation — ideally by the end of 2027 — the Phase II expansion to 500 MW by 2028 becomes substantially more credible, and the door opens to rapid scaling. If Phase I underperforms thermally or encounters induced seismicity issues triggering regulatory review, the technology reverts to the failed hot-dry-rock reference class from the 1970s-2000s, in which decades of US and European geothermal R&D never reached commercial scale.

Google is the only hyperscaler with material contracted enhanced geothermal capacity. Amazon, Microsoft, and Meta have not followed. The US Basin-and-Range geology (Nevada, Utah, Idaho, New Mexico, Oregon) gives the US a geographic advantage for this technology that no other country can easily replicate.

### Long-Duration Energy Storage

Long-duration energy storage — batteries capable of providing 24 to 100 hours of discharge rather than the standard four hours of lithium-ion — could be transformative for renewable firming, but the sector suffers from a classic coordination failure. Commercial deployment is below 1 GWh globally as of 2024, against estimates of 100+ GW needed for meaningful renewable firming at hyperscaler scale.

Form Energy's iron-air technology targets $20 per kWh at scale, which would produce a levelized storage cost of $35-50 per MWh for 100-hour duration — compared to $65-140 per MWh for four-hour lithium-ion (Lazard LCOS v7, 2024). The company has signed supply agreements with Google (Minnesota, 300 MW / 30 GWh for the 2030 timeframe) and Crusoe. A Georgia Power 15 MW / 1.5 GWh project was announced in 2026.

The circular problem is that long-duration storage cannot reach cost targets without scale, and scale requires demonstrated cost competitiveness. The DOE LDES initiative targets $0.05/kWh levelized storage cost. No large coordinated procurement mechanism exists to break this coordination trap, and the DOE program has not generated the equivalent of the loan guarantee structure that enabled early solar and wind scaling.

### Workload Flexibility and Curtailment Absorption

The most immediately actionable under-pursued lever is not a generation technology at all. It is the treatment of AI training workloads as flexible, interruptible load that can shift consumption to times and places where clean electricity is abundant and cheap.

Texas alone curtailed roughly 5-10 TWh of wind and solar in 2024 — electricity generated at zero marginal cost because the grid could not absorb it. California curtailed approximately 3.4 TWh in the same period (ERCOT 2024; EIA; CAISO). Total US major-grid curtailment in 2024 was roughly 15-20 TWh. Renewable buildout is outpacing transmission capacity, and curtailment is growing. A 500 MW AI training campus co-located with high-curtailment grid zones (West Texas, Mojave California) could potentially source 20-40% of its annual training energy at near-zero marginal cost through interruptible-load tariff structures that ERCOT and CAISO already offer to industrial customers.

Google has run carbon-aware training operations since 2020, shifting workloads to lower-carbon grid hours with a reported 2-3% efficiency loss for 30%+ emissions reduction. No other hyperscaler has deployed this approach at material scale. The economics: GPU opportunity costs (depreciation plus foregone revenue on idle hardware) exceed the dollar value of electricity savings at a $50 per ton carbon price, but the analysis reverses above $150-200 per ton. For firms with internal carbon prices in that range — Microsoft's is approximately $100 per ton, the highest among major tech companies — workload flexibility is among the cheapest available abatement levers.

This does not solve the 24/7 inference or production training problem. Inference workloads are latency-sensitive and cannot be temporally shifted. Large training runs incur 10-30% overhead from mid-job interruption (arxiv:2605.03751 on carbon-aware power scheduling). But for the training share of compute — roughly 60% of current AI electricity consumption, concentrated at fewer than 50 sites globally — this is a 0-2 year, near-zero-capital intervention that the industry has largely ignored.

---

## The Uncomfortable Reality: Gas as the Bridge

Any honest analysis of AI power sustainability must confront what is actually happening in power markets. In PJM's Transition Cycle 1 interconnection queue — the queue for new electricity generation in the Eastern US — natural gas is the single largest source by application, with 106 GW of new gas generation in line (PJM TC1 published data). Gas clears the interconnection queue faster than any other source and can reach commercial operation within 2-3 years of application. Advanced nuclear and enhanced geothermal cannot deliver electrons at the speed AI data center buildout is proceeding.

The hyperscalers' sustainability commitments are not equivalent. Google has committed to 24/7 carbon-free hourly matching — meaning every hour of consumption must be matched to a carbon-free generation source in the same grid region. Google has materially deployed this: roughly 65% hourly matching was achieved in 2023, with a 2030 target of 100%. Google has also contracted nuclear (Three Mile Island co-investor) and geothermal (Fervo), and has not publicly announced support for new gas plants.

Microsoft, Amazon, and Meta follow a structurally different pattern. All three claim "100% renewable energy" based on annual renewable energy certificate matching — a weaker standard under which annual totals are balanced rather than hourly coverage. Microsoft's 2025 sustainability report disclosed energy use up 168% and emissions up 23.4% versus its 2019 baseline. Natural gas turbines are powering Stargate construction in West Texas. The commitment language remains carbon-negative by 2030, but operational behavior is gas-as-bridge with annual RECs as cover. Under the GHG Protocol's proposed hourly matching revisions — which WattTime's December 2025 analysis suggests would fail 65-75% of current corporate clean-energy claims — these commitments would not hold up.

The outside-view historical base rate for bridge fuels is stark. US natural gas was framed as a 20-year bridge to clean energy in 2004-2008 policy documents. Gas generation has grown from approximately 20% to 40% of US electricity supply since then and continues to grow. Combined-cycle plants commissioned in 2026-2030 carry 30-year operational lifespans, meaning they will operate through 2056-2060. Satellite-based methane leakage measurements (Alvarez et al., 2018, Science; confirmed by Lyon et al., 2021) put actual leakage at 2.3-3.7%, well above the EPA inventory estimate of 1.5%; Energy Policy analysis from January 2025 found that "two-thirds of the emissions reductions" from coal-to-gas switching "disappear" when methane leakage is properly accounted for. The PJM December 2025 capacity auction cleared at $269.92 per MW-day — an 800% year-over-year increase — sending a strong price signal for more gas construction.

Any realistic assessment of AI power sustainability in the 2027-2030 window must account for gas as the gap-filler for the 5-10 GW that announced nuclear PPAs will not deliver on schedule.

---

## The Multi-Axis Sustainability Picture

Carbon is not the only dimension of sustainability. Water consumption and materials supply chains present independent constraints that the technology ranking changes depending on geography.

### Water

The water consumption per megawatt-hour varies substantially across clean generation options and is the binding constraint in the US Southwest:

| Technology | Operational water consumption |
|---|---|
| Wind onshore | ~0.001 L/kWh — essentially negligible |
| Solar PV (dry-cooled) | ~0.01-0.05 L/kWh — minimal |
| Enhanced geothermal, closed-loop (Fervo-type) | ~0.1-0.4 L/kWh — low; closed-loop recycled |
| Natural gas CCGT | ~0.5-2.0 L/kWh (cooling tower higher) |
| Nuclear, light water reactor (cooling tower) | ~1.5-3.0 L/kWh |
| Gas + carbon capture and storage | ~1.0-4.0+ L/kWh (CCS amine scrubbing adds substantial water load) |
| Green hydrogen via electrolysis (full chain) | ~6-15 L/kWh delivered — highest of any clean option |

Note on gas + CCS: sources differ on this figure. NREL's lifecycle harmonization study (Meldrum et al., 2013, IOP; n=165 estimates), the UNECE lifecycle assessment (2021), and the US Geological Survey produce different mid-points. The calibration gap across sources is 0.87-5.0 L/kWh for gas + CCS. The direction is clear — CCS adds water load; the magnitude is uncertain.

Colorado River basin states (Arizona, Nevada, Utah) have operated under Tier-1 and Tier-2 water shortage declarations since 2021, with a May 2026 seven-state conservation agreement falling short of the structural deficit. Texas data center clusters face growing groundwater competition in the Colorado River Authority allocation zone. Under water-stressed siting conditions, the technology ranking for firm clean power flips: enhanced geothermal closed-loop and solar PV are the only ≥100 MW options with both low-carbon AND low-water profiles. Nuclear, though carbon-free, faces real water constraints in Texas and Arizona. Gas with CCS, often positioned as a clean bridge, has among the worst water profiles of any generation option.

The hidden water disadvantage of green hydrogen is noteworthy: electrolysis requires approximately 9 liters of water per kilogram of hydrogen produced, which compounds to 6-15 liters per kilowatt-hour of delivered electricity at current round-trip efficiencies. This further strengthens the case against green hydrogen for primary power in water-stressed Western US locations — the economics and water arguments point in the same direction.

### Materials Supply Chains

Two supply chain constraints are load-bearing for the main technology categories.

For advanced nuclear — the reactor designs requiring high-assay low-enriched uranium (HALEU), including Kairos Power, X-energy's Xe-100, and TerraPower Natrium — Russia holds 100% of commercial HALEU production as of 2026. Centrus Energy produced approximately 900 kg in 2024 against projected demand exceeding 50 metric tons per year by 2035 — a 55x gap. Western investment of $4.2 billion (DOE $2.7 billion plus Urenco and Orano) targets partial domestic production by 2027-2030, sufficient for 2-4 first-of-kind reactors. Fleet-scale deployment of HALEU-dependent designs before 2030 is physically impossible under current supply trajectories (IEA/NEA Red Book; World Nuclear Association; DOE official announcements).

For green hydrogen electrolyzers, China has built 85% of global alkaline electrolyzer manufacturing capacity and holds dominant positions in all upstream supply chains (6 of the top 10 global electrolyzer manufacturers are Chinese; Asia Times/Pacific Forum research; FCHEA). The cost gap is 2-3x: Chinese alkaline electrolyzers run $300-500 per kilowatt versus $750-1,300 per kilowatt for Western equivalents. This is a cost and availability risk under domestic content requirements — the IRA Section 45V credit includes domestic content provisions that would require US-manufactured electrolyzers, substantially increasing the cost of green hydrogen produced under that subsidy. It is not a physical supply cutoff risk in the near term; China has not restricted electrolyzer exports the way it has rare earth metals.

---

## Country-Comparative Positioning

**Advanced nuclear (HALEU-dependent designs):** US-advantaged. ADVANCE Act (2024) streamlines NRC licensing for some advanced designs; IRA Sections 45U and 45J provide production credits; DOE is the primary HALEU investment vehicle. EU is slower, with France as the exception (French nuclear revival policy active). Both face the Russia-HALEU chokepoint equally.

**Enhanced geothermal:** US-advantaged. Basin-and-Range geology (Nevada, Utah, Idaho, New Mexico, Oregon) provides the hot dry crystalline rock at accessible depths that Fervo's technology requires. This geology is largely absent in Europe outside Iceland and Italy. US oilfield services capacity is the critical enabler of the horizontal drilling technology transfer. No rare earth or China supply chain exposure.

**Green hydrogen electrolyzers:** EU has a stronger regulatory framework (REPowerEU hydrogen strategy; EU Hydrogen Bank; IPCEI) and was historically in front on deployment intent. However, EU RED III Article 28's hourly-matching requirement for renewable fuel of non-biological origin certification means EU green hydrogen must follow solar and wind generation curves — at 25-40% capacity factor rather than the 90%+ achievable with a continuously-running electrolyzer. This makes EU green hydrogen more expensive than it would be without the additionality and temporal correlation requirements, partially undermining the EU's apparent advantage. The policy architecture is sound; the cost math is harder than it looks.

**Solar PV:** Both US and EU are disadvantaged by China's 93-97% dominance of polysilicon and wafer manufacturing. IRA Section 45X domestic content credits are driving First Solar and Qcells investment, but the 2027 IRA Section 48E investment tax credit cliff — when the credit expires for wind and solar placed in service after December 31, 2027 — creates a compressed 24-month window for new solar to qualify. Nuclear's Section 45U production credit and hydrogen's Section 45V credit remain intact.

---

## Actionable Moves in the Next 24 Months

For a hyperscaler or large data center operator, the near-term action set differs from the longer-term one.

**Immediate (2026-2027):**

Register AI training load with ERCOT as an interruptible large industrial customer. The administrative process takes 3-6 months. A 500 MW training campus could access 200-400 GWh of near-zero-cost curtailed electricity annually while improving grid stability. CAISO has analogous demand response mechanisms. This is the highest return-on-effort clean-energy intervention available today. The capital investment is in scheduling infrastructure, not generation.

Commission a multi-axis sustainability analysis for planned data center sites. Siting decisions made on carbon-only criteria that ignore water constraints will face project-blocking regulatory challenges in Colorado River basin states within 5-10 years. For Western US siting (Texas, Arizona, Nevada), enhanced geothermal PPA optionality and behind-the-meter solar with minimal water consumption should be the baseline, not nuclear, which faces water allocation constraints at these sites.

Evaluate hydrogen backup/UPS fleet replacement economics. The question is not LCOE competition with grid generation; it is capital cost of fuel cell stacks versus diesel generators plus avoided EU ETS carbon costs for EU sites. For data centers with 48-168 hour backup requirements in EU ETS-covered jurisdictions, the NPV case is increasingly defensible. Run a 5-10 MW pilot as real-options strategy (addressing PM[3]: the 15% probability that green hydrogen for firming turns out to be the right answer post-2030 means small-scale optionality is cheap insurance).

Evaluate VPP / grid-forming inverter potential for new BESS deployments. The PJM December 2025 capacity auction cleared at $269.92/MW-day — an 800% increase year-over-year. A 500 MW campus with 2,000 MWh of co-located BESS and grid-forming inverter capability could generate $15-30 million per year in capacity market revenue. As the IRA Section 48E ITC expires post-2027, this revenue stream partially replaces the lost subsidy economics and helps justify storage capital.

**Medium-term (2028-2030):**

Establish rights-of-first-refusal or development agreements with enhanced geothermal developers. Cape Station Phase I (100 MW, 2026) is the technology credibility gate. If it performs at 80%+ capacity factor and $85/MWh or below by the end of 2027, Phase II (500 MW, 2028) and a generation of follow-on projects become commercially viable. That creates a narrow window in 2027-2028 where signing long-term PPAs at Cape II economics will be possible before the market prices in the technology validation. Google has already secured right-of-first-refusal on 3 GW; others have not.

Evaluate industrial-co-located green hydrogen configuration for Gulf Coast or Upper Midwest data center clusters. A joint venture in which a data center renewable PPA generator also supplies hydrogen to adjacent steel or ammonia production is genuinely novel in US/EU contexts. The economics are driven by the industrial demand floor. Steel producers facing EU CBAM exposure by 2030 are looking for clean hydrogen supply deals. This may be the most under-explored high-upside configuration that no major technology company has yet announced.

---

## Sources

IEA "Energy and AI" 2025; IEA Global Hydrogen Review 2025; Lawrence Berkeley National Laboratory data center electricity reports (2007, 2016, 2024); BNEF New Energy Outlook 2024; Lazard LCOE Analysis v17 (June 2024); Lazard Levelized Cost of Storage Analysis v7; Fervo Energy SEC filing (2025); Fervo/UIPA Enhanced Geothermal Data Center Corridor (July 2025); DOE Enhanced Geothermal Earthshot program documentation; DOE Hydrogen Hub program documentation; NREL Lifecycle Water Use for Electricity Generation (TP-550-50900); NREL Meldrum et al. "Life cycle water use for electricity generation" (IOP Environmental Research Letters, 2013); UNECE Life Cycle Assessment of Electricity Generation Options (2021); US Geological Survey water use by thermoelectric power data; PJM interconnection queue TC1 published data; FERC interconnection reform filings; ERCOT 2024 curtailment data; EIA curtailment data (2024); CAISO curtailment data (2024); IEA/NEA Uranium Red Book; World Nuclear Association; DOE HALEU supply chain documentation; IRS/DOE/US Congress IRA Section 45E/45U/45V/45X/48E provisions; European Commission RED III Article 28; EU CRMA (Critical Raw Materials Act, effective May 2024); European Commission REPowerEU strategy; IAEA ARIS Catalogue (2024); Epoch AI training compute growth dataset; arxiv:2502.12211 (hydrogen power techno-economic analysis); ScienceDirect EU PEM electrolyzer learning-rate dataset (2025); Alvarez et al. "Assessment of methane emissions from the US oil and gas supply chain" (Science, 2018); Energy Policy journal (January 2025 gas emissions reanalysis); GHG Protocol Scope 2 Guidance (under consultation); WattTime hourly CFE analysis (December 2025); Princeton ZERO Lab carbon accounting research; Brander M. et al. (2018) and Bjørn A. et al. (2022) on corporate renewable energy claims; Google CFE-365 progress reports and whitepaper; Phadke et al. LBNL 2024 on AI demand flexibility; arxiv:2605.03751 (carbon-aware power scheduling); RMI PJM interconnection reform analysis; ERCOT interruptible load market documentation; Fraunhofer ISE Photovoltaics Report; Asia Times/Pacific Forum electrolyzer manufacturing analysis; FCHEA (Fuel Cell and Hydrogen Energy Association) industry reports; H2 Green Steel (Stegra) SEC-equivalent filings; Wood Mackenzie solar supply chain analysis.

---

## Errata and Known Completeness Gaps — 2026-05-23 post-audit corrections

This section is a post-hoc addition by the review lead following two independent audits (a sigma-audit process review and a sigma-evaluate quality assessment). It corrects specific factual items in the body above and notes scope items the review did not analyze. The original analysis is preserved unchanged for audit trail; corrections below take precedence.

### Factual corrections

**PJM capacity auction attribution.** The body references "PJM December 2025 capacity auction cleared $269.92/MW-day" in the context of merchant-pricing breakout signals. The correct attribution: $269.92/MW-day was the *July 2024* auction for the 2025/2026 delivery year (system-wide, with zonal exceptions BGE $466.35 and Dominion $444.26). The December 2025 auction (for the 2027/2028 delivery year) cleared at the FERC-approved cap of $333.44/MW-day across the entire PJM footprint, a 1.3% increase over the prior auction. Both clearings represent the unprecedented capacity-price regime the body describes; the attribution error does not change the directional finding. Source: PJM press releases (July 2024 and July 2025) and Utility Dive coverage.

**US data center demand point estimate.** The body states "approximately 440 TWh by 2030." The IEA Energy and AI 2025 report states US data center electricity demand grows by approximately 240 TWh, or 130%, relative to the 2024 baseline. The implied 2030 total ranges from approximately 425 to 440 TWh depending on which 2024 baseline figure is used (LBNL 2024 puts US 2024 data center demand at approximately 176 TWh, which implies a 2030 figure of ~416 TWh; the synthesis used a higher 2024 baseline of ~200 TWh, which yields ~440 TWh). The 425–440 TWh range is more defensible than the single point estimate; the directional finding of a major demand surge holds.

**IRA Section 48E framing.** The body characterizes the ITC as having a "post-2027 cliff." This is oversimplified. Following the One Big Beautiful Bill Act (OBBBA, enacted July 4, 2025) and IRS guidance issued August 2025, wind and solar projects must either *begin construction* by July 4, 2026, *or* be placed in service by the end of 2027, to qualify for §48E. The 4-year continuity safe harbor remains in effect for projects that began construction before September 2, 2025 under prior rules. The 5% cost safe harbor was eliminated except for solar facilities under 1.5 MW. The practical effect for utility-scale developers is a strong incentive to begin construction before July 4, 2026 — not a hard 2027 deadline. The framing matters because the project pipeline through 2030 depends on how many projects safe-harbor under begin-construction rules, not on the placed-in-service deadline alone.

**HALEU "55× supply-demand gap."** The body cites a "55× supply-demand gap" without sourcing. The figure has rough mathematical grounding: DOE projects approximately 50 metric tons per year of HALEU demand by 2035; US domestic production was approximately 0.9 metric tons in 2024 (Centrus had produced and delivered over 920 kg cumulatively by mid-2025). The 50 ÷ 0.9 ≈ 55× ratio is therefore in the right neighborhood, but several caveats apply: (a) the demand figure is the 2035 not the 2030 number; (b) DOE HALEU stockpiles at Y-12, INL, and Savannah River are projected to reach approximately 21 metric tons by mid-2026 with approximately 14.9 metric tons potentially available as temporary supply, materially closing the gap for early-2030s reactor deployments; (c) Centrus is expanding the Piketon cascade. The headline of "Russia HALEU monopoly is a binding 5-year constraint on advanced nuclear scale-up" remains directionally correct, but readers should treat the specific 55× ratio as illustrative not authoritative. Source: DOE HALEU Availability Program documentation; Third Way (March 2025); World Nuclear Association HALEU briefing.

**Green hydrogen water consumption.** The body cites approximately 6–15 L/kWh delivered for green hydrogen via electrolysis full chain. The stoichiometric minimum for electrolysis is approximately 9 L per kilogram of hydrogen produced; with cooling water and balance-of-plant the figure rises to 22–30 L/kg. Converting to L/kWh-delivered requires assumptions about round-trip efficiency. At 30–40% round-trip efficiency, 1 kg of H₂ (33.3 kWh LHV) yields approximately 10–13 kWh of electricity, giving roughly 1–3 L/kWh delivered for stoichiometric water alone, or roughly 2–10 L/kWh delivered with cooling. The body's 6–15 L/kWh figure is at the high end of this range and should be read as inclusive of cooling and balance-of-plant. The directional finding (green H₂ has materially higher water intensity than alternatives) holds; the specific L/kWh range carries 2× uncertainty.

### Known completeness gaps

Two technologies in the original hypothesis list (workspace H3 candidates) received no analytical coverage in this review:

**Behind-the-meter LDES at hyperscaler scale.** Long-duration energy storage was discussed in the body as a coordination-failure category, but the specific configuration of co-located LDES with hyperscaler renewable PPAs (Form Energy iron-air at 100-hour duration paired with Google Minnesota's 300 MW / 30 GWh agreement, for example) was not analyzed for water/land/materials/economics trade-offs at scale. This is a real gap.

**Waste-heat recovery.** Data center waste heat recovery — district heating integration (substantial in Northern Europe, nascent in the US), bottoming cycles, or absorption chilling — was not analyzed. The Nordic precedent (Stockholm Data Parks, FortumValue heat purchase agreements) and emerging EU regulatory pressure under the Energy Efficiency Directive suggest this is a real opportunity space the review missed.

**Land, materials supply chain (beyond iridium and HALEU), and waste/end-of-life axes of multi-axis sustainability.** The scope-boundary claimed carbon, water, land, materials, and waste/end-of-life as co-equal axes. The delivered analysis covers carbon and water substantively, materials partially (iridium, HALEU, AWE concentration in China), and land/waste essentially not at all. For hyperscaler siting at scale, land use becomes a binding constraint in dense Northern Virginia and Frankfurt-Amsterdam-London markets, and waste/end-of-life (battery recycling, electrolyzer membrane disposal, decommissioning of advanced nuclear) will become material on the medium-to-long timeframe.

### Confidence note

Both audits assessed the synthesis as analytically reliable (YELLOW process verdict / B 3.0/4.0 findings grade — both above re-evaluate threshold). The corrections above are precision and completeness items that should be incorporated into how the document is used. The load-bearing conclusions (the 6-state H₂ taxonomy, EGS as most credible under-pursued firm power conditional on Cape Phase I, workload-flexibility as most actionable demand-side lever, gas-as-bridge entrenchment tension) are not affected by these corrections.

For high-stakes decisions, verify the specific quantitative claims in the body against primary sources cited.

