# regulatory-licensing-specialist memory

## identity
role: Financial services regulatory specialist — trust company chartering, loan agent licensing, fiduciary duty frameworks, banking regulations, compliance infrastructure
created: 26.3.11 |trigger: DA[#8] gap identification |team: sigma-review

## research-findings(26.3.11)

### R1: licensing-paths
- trust-charter: ¬legally-required-for-pure-admin-agent(contractual-role) |required-for-trustee+escrow(TIA-1939-§310)
- !BUT: practically-required-for-market-credibility |GLAS,CSC,Wilmington all hold trust/bank charters
- NH nondepository trust: best-path |$500K-min($1.25M-practical) |4-6mo |$5K-app-fee |GLAS-precedent(2016)
- SD/WY: alternatives($500K-$1M min, 6-9mo) |DE: heavier(CSC-precedent) |NY: avoid-initially(12-18mo+,$2-5M+)
- OCC federal: overkill($15M-Tier-1+$10M-liquid) |suited-for-custody/digital-assets

### R2: agent-vs-servicer-distinction
- admin-agent(BSL/PC): B2B-institutional |¬consumer-lending-license |¬NMLS |¬state-mortgage-servicer
- payment-processing: trust-company-accounts OR bank-partnership eliminates money-transmitter-concern
- SEC/FINRA: ¬required-for-loan-agency-alone |SRS-Acquiom-has-BD-for-M&A-escrow-specifically
- !critical-insight: syndicated-loan "loan agent" ≠ consumer "loan servicer" — entirely-different-regulatory-regimes

### R3: fiduciary-framework
- admin-agent: contractual(¬fiduciary) |LSTA: "mechanical and administrative" |gross-negligence/willful-misconduct-standard
- trustee: fiduciary |prudent-person-standard |higher-insurance-requirements
- insurance-package: E&O($3-10K/yr@$1M) +fiduciary-liability($5-25K/yr) +fidelity-bond($2-10K/yr) +cyber($5-25K/yr) +D&O($5-20K/yr) = $20-130K/yr total

### R4: compliance-infrastructure
- AML/BSA: trust-co=financial-institution |SAR+CTR filing |written-AML-program |BSA-officer |annual-independent-audit
- SOC2-Type-II: 12-18mo from start |$20-80K first-yr |ISO27001: 12-15mo |90%-overlap(pursue-simultaneously)
- ongoing: quarterly-call-reports |18mo-examinations(NH) |capital-adequacy-monitoring

### R5: total-cost-model
- regulatory-capital: $2-4M initial(charter+setup)
- regulatory-operations: $1-2.7M/yr(compliance-staff+AML+legal+insurance+audit)
- experienced-loan-admin-staff: $500K-1.5M/yr(5-10 people minimum, ¬engineers)
- total: tech($10-20M) + regulatory($2-4M) + annual-regulatory-ops($1-2.7M/yr) = $13-27M launch
- !breaks-even-on-regulatory-costs-alone: 40-540 facilities @$5-25K/yr

### R6: competitor-structures
- GLAS: NH trust co(2016) +UK +PSD2(DE/FR) +ACPR +BaFin +ASIC |multi-jurisdictional over 10yr
- CSC: Delaware Trust Co(acquired) |125yr entity
- Wilmington: M&T Bank subsidiary |full banking charter
- AD: Jersey JFSC |fund-admin-licensing-primary
- Kroll: existing Kroll corporate entities
- SRS: FINRA BD +FCA(UK) +DNB(NL) |payment-services
- Hypercore: SaaS-only |¬trust-co |limited-service-scope

### R7: cross-border
- UK: FCA authorization(6-12mo,$100-300K) |payment-services-reg
- EU: CRD6(Jan-2027) +PSD2 +Credit Servicing Directive |member-state-by-member-state |6-18mo+$150-500K per jurisdiction
- APAC: HK(TCSP) |SG(ACRA) |AU(ASIC) |¬priority

## calibration
C[26.3.11] NH-trust-charter-timeline: 4-6mo validated by GLAS-precedent+multiple-2025-approvals |confidence: HIGH
C[26.3.11] SOC2-timeline: 12-18mo industry-consensus |finserv-startups sometimes faster with dedicated effort |confidence: HIGH
C[26.3.11] total-cost-$13-27M: combines tech-architect $10-20M(tech) + my $2-4M(regulatory) + ops costs |confidence: MEDIUM(range is wide, depends on service-scope+jurisdiction-count)
C[26.3.11] admin-agent-¬fiduciary: LSTA standard, well-established in credit-agreement law |confidence: HIGH
C[26.3.11] Hypercore-SaaS-only: operates without trust charter, limits service scope |validates that regulatory is optional IF scope limited |confidence: HIGH

## patterns
P[26.3.11] successful-entrant-paths: own-charter(GLAS,CSC) OR parent-entity(Wilmington,Kroll) OR scope-limitation(Hypercore)
P[26.3.11] NH-is-finserv-friendly: multiple trust-co charters granted 2024-2025 |nondepository focus |lighter-than-NY/DE
P[26.3.11] regulatory-cost=material-not-fatal: $1-2.7M/yr ongoing is significant but manageable at $15-30M raise level

## open-questions
- money-transmitter-licensing: state-by-state analysis needed if ¬using trust-company-accounts for payment processing
- NY-DFS-charter: may be needed later for institutional credibility with largest banks — timeline+cost needs deeper analysis
- EU CRD6 impact: Jan-2027 transposition could affect US-entity serving EU lenders — monitor regulatory developments
- successor-agent-regulatory: successor agent assumes ALL existing obligations — must have charter+compliance BEFORE accepting mandates
- insurance-capacity: E&O coverage limits may gate maximum deal size for new entrant vs self-insuring incumbents

## r1-refresh(26.3.11-session2)
R[26.3.11] r1-findings-refreshed: 8-findings(F1-F8) |validated-prior-R1-R7-with-fresh-web-research
key-updates:
- CRD6: loan-agency/trustee=¬explicitly-"core-banking"(Mayer-Brown-Apr-2025)→potential-EU-exemption-reduces-barrier |BUT-member-state-fragmentation
- CSBS-MTMA: 31-states-enacted(up-from-prior) |trust-co=exempt→charter-solves-money-transmitter
- SOC2-costs: $30-150K-first-yr(2026-pricing) |ISO27001-costs+20%-over-2025
- TIA-§310: confirmed-NH-NDTC-eligible-as-qualified-trustee(non-bank path validated)
- private-credit-market: $3.5T(2025,AIMA)→$5T(2029) |$45T-PC+-TAM(Oxane) |infra-gap-massive
- cost-model: REVISED $13-27M→$13-25M(Hypercore-SaaS-floor)
- successor-agent: regulatory-requirements=contractual(credit-agreement-defined) ¬separate-licensing
C[26.3.11] CRD6-loan-agency-exemption: MEDIUM-confidence |Mayer-Brown-supports-but-"legally-uncertain" |member-state-risk
C[26.3.11] MTMA-trust-co-exemption: HIGH-confidence |31-states-enacted |statutory-exemption
P[26.3.11] charter+tech=only-defensible-combination-for-independent-entrant |GLAS=sole-independent-with-both |Hypercore-ceiling-validates

## promoted-principles
P[charter-as-multi-solving-instrument: single-trust-company-charter-simultaneously-solves-trustee-eligibility(TIA-§310)+payment-processing-exemption(CSBS-MTMA)+regulatory-moat+institutional-credibility. Evaluate-charter-ROI-against-ALL-solved-problems ¬just-one. NH-NDTC=$1.25M-solves-4-problems |src:loan-admin |promoted:26.3.12 |class:new-principle]
P[conditional-charter≠operational-readiness: charter-approval=30-40%-of-total-timeline. 12-18mo-gap-post-approval(AML-program+BSA-officer+board+insurance+trust-accounts+examiner-readiness). Crypto.com-conditional-Feb2026-still-pre-opening. Extends-charter-multi-solver:charter=necessary-step-1 ¬finish-line |src:loan-admin-v2 |promoted:26.3.12 |class:new-principle]
P[stress-shifts-pipeline-mix-not-volume: credit-stress→greenfield↓(40→15-20%)+successor↑(30→40-50%)+restructuring-new(20-30%). Revenue/facility-UP-in-distress($25-50K→$35-75K). Counterintuitive:specialized-agents-benefit-from-distress(LME+amendment+workout-demand). Pipeline-velocity↓-but-value/facility↑ |src:loan-admin-v2 |promoted:26.3.12 |class:new-principle]
P[AI-regulatory-language-precision: "AI-assisted"≠"AI-generated"→regulator-acceptance=framing-dependent. FinCEN-Oct2025:supports-AI-for-"lower-risk-SAR-tasks"+human-in-loop=prerequisite. Applies-beyond-AML-to-any-regulated-AI-output. Always-use-regulator's-own-language |src:loan-admin-v2 |promoted:26.3.12 |class:new-principle]

## v2-findings(26.3.12)
F9: regtech-as-differentiator |3-mechanisms(real-time-monitoring,URSIT-advantage,KYC-as-service) |$200-400K-build |compliance=product-feature-¬just-cost-center
F10: charter-expansion-sequenced |NH(0-6mo)→UK(12-24mo)→EU-DE+LU(24-36mo)→APAC(36-48mo) |CRD6-UPGRADED-MEDIUM-HIGH(5-law-firms:loan-agency≠core-banking) |total=$1.5-3M/4yr
F11: insurance-tower-detailed |PC-Day-1($25-80K/yr,$5-25M-tower)→BSL-3-5yr($100-400K,$50-250M)→mega-established($250M+) |tech→better-terms
F12: AML/BSA-as-product |AI-70-90%-detection+auto-SAR+KYC-as-service($5-15K/client/yr) |build=$100-200K |revenue=$250K-3M@maturity
F13: successor-mechanics-resolved |contractual-¬licensing |migration-tech=$50-100K=competitive-edge |30%-of-pipeline(PS-F3)
F14: regulatory-cost-optimization |$190-390K/yr-savings(15-20%-of-$1-2.5M) |SAR-auto+call-reports+monitoring+exam-prep |build=$200-400K |ROI@mo-18
F15: NH-examiner-URSIT-mapped |4-components(Audit,Management,Dev+Acq,Support+Delivery) |compliance-native=internal-advantage |first-exam<12mo=critical
F16: regulatory-moat-quantified |SaaS→charter=28-45mo+$2-4.5M |PE-de-novo=12-18mo=real-threat |temporal→relational=key-conversion

## v2-calibrations(26.3.12)
C[26.3.12] CRD6-loan-agency-exemption: UPGRADED MEDIUM→MEDIUM-HIGH |5-major-law-firms-agree |member-state-risk-remains
C[26.3.12] insurance-tower-PC-accessibility: HIGH |standard-market-practice |Day-1-feasible-for-mid-market-PC
C[26.3.12] AML-tech-revenue-potential: MEDIUM |proven-tech-capability-but-loan-admin-revenue-model-unproven
C[26.3.12] regulatory-cost-savings-via-tech: MEDIUM |vendor-claims-discounted |conservative-$190-390K/yr
C[26.3.12] SaaS-to-charter-barrier: HIGH |28-45mo-minimum-well-supported-by-evidence
C[26.3.12] effective-window-2-8mo: revised-from-6-12mo |competitive-acceleration-3-moves-in-Q1-2026 |confidence:MEDIUM
C[26.3.12] Fitch-PC-defaults-9.2%: validated-by-Reuters+TheStarMY+Bernstein |record-level-2025 |confidence:HIGH
C[26.3.12] breakeven-mo-36-48: all-in-burn-exceeds-PS-model |GLAS-4yr-validates-timeline |confidence:MEDIUM-HIGH
C[26.3.12] charter-environment-2025-2026: MOST-favorable-in-decade |11-in-83-days(OCC) |20-filings-all-time-high |BUT-conditional≠operational |confidence:HIGH
C[26.3.12] KYC-as-service-precedent: 5-fund-admin/trust-firms-actively-selling |charter=regulatory-prerequisite |$5-15K/client=market-rate |confidence:HIGH
C[26.3.12] AI-AML-regulatory-acceptance: FinCEN-supports-AI-for-alert-clearing+monitoring |full-auto-SAR=¬accepted→human-in-loop |HSBC-proof-point |confidence:HIGH-tech,MEDIUM-regulatory-acceptance-for-trust-co
P[26.3.12] conditional-charter≠operational-readiness: 12-18mo-gap-between-conditional-approval-and-accepting-first-mandate |pre-opening-requirements-extensive(OCC) |applies-to-Hypercore-charter-scenario-AND-new-entrant-planning
P[26.3.12] charter+tech+distribution=only-viable-independent-path |GLAS=proof |Hypercore-ceiling-validates-charter-necessity |AD-Bain-validates-platform-investment

## v2-open-Qs-status
!RESOLVED(4/4): CRD6-exemption(upgraded) |insurance-tower(detailed) |successor-agent(contractual) |URSIT(mapped)
NEW-open-Qs: (1)France-specific-CRD6-transposition(banking-monopoly-may-be-broader-than-other-MS) (2)NH-examiner-actual-tech-expectations(varies-by-individual-examiner-beyond-URSIT-framework)

## r1-doc-review(26.3.13)
R[26.3.13] r1: reviewed 6 loan-admin KB docs for regulatory accuracy |18F(3H,5MH,7M,3LM)+5G(2H,2MH,1M)
key-findings:
- F1[H]: OFAC penalty WRONG($330,947→$377,700) — only confirmed factual error
- F2[H]: OFAC SOL vs recordkeeping conflated — two distinct legal developments
- F3[H]: KYC/AML missing agent-regulatory-status distinction (bank vs trust-co vs non-regulated)
- G1[H]: Agent licensing framework MISSING — most significant gap (trust charter, TIA§310, BSA/AML trigger, MTL exemption)
- G2[H]: Fiduciary duty comparative framework MISSING (admin=non-fiduciary, escrow=quasi-fiduciary, security trustee=fiduciary, trust-co=state-law)
Doc5=strongest regulatory accuracy | overall quality HIGH
pattern: regulatory content correct where present but structural gaps in agent-entity-level regulatory framework
C[26.3.13] Doc5-regulatory-accuracy: HIGH | 21/22 items web-verified correct | only OFAC penalty wrong
C[26.3.13] Agent-licensing-gap: HIGH-impact | foundational for audience | trust-charter implications permeate all operational content

## regulatory-landscape-research(26.3.13)
R[money-transmission-licensing: state-by-state MTL required+FinCEN MSB |all-49-licensing-states=$1.3-3M+-initial |6-18mo-timelines |MTMA-adopted-31-states-covering-99%-of-transmission-activity |California-DFAL-effective-July-1-2026 |src:CSBS,state-regulators |refreshed:2026-03-13 |next:2026-04-13]
R[stablecoin-regulation: GENIUS-Act-signed-July-18-2025=first-US-federal-digital-assets-law |creates-FQPSI/SQPSI-categories |!CRITICAL:preempts-state-MTL-requirements-for-permitted-stablecoin-issuers→directly-undermines-WU-primary-regulatory-moat |OCC-implementing-rules-proposed-March-2026 |payment-stablecoins≠securities≠commodities |!IMPLICATION-for-loan-admin:trust-charter-holders-can-issue/custody-stablecoins→potential-payment-rail-for-loan-settlements |src:Congress.gov,Latham-Watkins,Sidley-Austin,OCC |refreshed:2026-03-13 |next:2026-04-13]
R[crypto-fintech-licensing: Ripple(50+-MTLs)+Kraken(Fed-master-account-March-2026=first-crypto-firm)+Circle/Coinbase-pursuing-federal-charters |DOJ-shifted-enforcement-posture-April-2025 |OCC-charter-surge:11-approvals-in-83-days,20-filings-2025=all-time-high |src:OCC,DOJ |refreshed:2026-03-13 |next:2026-04-13]

## research(26.3.22)
R[OCC-chartering-reform: OCC-finalized-12-CFR-5.20-amendment(effective-Apr-1-2026)|replaces-"fiduciary-activities"→"operations-of-trust-company-and-activities-related-thereto"|national-trust-banks-may-now-engage-non-fiduciary-activities(custody,safekeeping,stablecoin)|OCC-charter-surge:11-conditional-approvals-in-83-days(Dec2025-Feb2026),20-filings-2025=all-time-high|5-Dec-12-2025-approvals(BitGo,Fidelity-Digital,Paxos=conversions;2-de-novo)|Bridge(Stripe-sub),Protego,Crypto.com=Feb-2026-conditionals|CSBS-warns-"Franken-charter"-legal-challenge-risk|Acting-Comptroller-Hood:pro-fintech,pro-digital-assets,reduced-regulatory-burden|processing-target:120-days-from-complete-application|!KEY-UPDATE:non-fiduciary-expansion-broadens-trust-charter-utility-for-loan-admin(custody+payment-processing-now-explicitly-permissible)|src:OCC-Bulletin-2026-4,FederalRegister-91FR9977,ABA-Banking-Journal,Stinson-analysis,FinTechWeekly,PYMNTS|refreshed:2026-03-22|next:2026-04-22]
R[GENIUS-Act-stablecoin: signed-July-18-2025=first-US-federal-digital-assets-law|creates-FQPSI(federal)+SQPSI(state)-issuer-categories|trust-companies-explicitly-preserved("nothing-limits-authority-of-trust-company")|FDIC-proposed-rule-Dec-2025-for-supervised-institutions|OCC-proposed-rulemaking-Mar-2-2026(licensing,reserves,operations)|comment-deadline-May-1-2026|effective-Jan-18-2027-or-120-days-post-final-rules(whichever-first)|payment-stablecoins≠securities≠commodities|!IMPLICATION-for-loan-admin:trust-charter-holders-can-issue/custody-stablecoins→potential-payment-rail-for-loan-settlements|preempts-state-MTL-for-permitted-issuers→reduces-regulatory-fragmentation|src:Congress.gov,Latham-Watkins,Sidley-Austin,FDIC-press,OCC-Federal-Register|refreshed:2026-03-22|next:2026-04-22]
R[FDIC-OCC-regulatory-posture: Trump-admin-2-redirected-toward-digital-assets+reimagined-regulatory-perimeter+capital-reform+recalibrated-supervision|"reputation-risk"-eliminated-as-enforcement-basis(Oct-2025-proposed-rule,OCC+FDIC)|AML/CFT-reorientation:outcomes-based→resource-reallocation-from-low→high-value-reporting|enhanced-SLR-finalized-Nov-2025(GSIBs)|climate-risk-guidance-withdrawn-Mar-2025|!NET-EFFECT:most-favorable-chartering-environment-in-decade-for-fintech+trust-companies|bank-fintech-partnerships-"critically-important"(Hood-Feb-2025)|third-party-risk-mgmt-guidance-maintained(Jun-2023-interagency)|community-bank-BSA-exam-relief(Nov-2025,$30B-threshold)|src:FDIC-speeches,Freshfields,PwC,Gibson-Dunn,Chambers,Sidley|refreshed:2026-03-22|next:2026-04-22]
R[AML-BSA-non-bank: FinCEN-investment-adviser-AML-rule-DELAYED-Jan-2026→Jan-2028(final-rule-Dec-2025)|scope:~15K-RIAs($120T-AUM)+~6K-ERAs($5T)|FinCEN-reviewing-to-narrow-scope-to-business-models+risk-profiles|real-estate-all-cash-reporting:effective-Dec-1-2025(nationwide,replaces-GTOs)|FinCEN-Oct-2025-FAQ:AI-supported-for-"lower-risk-SAR-related-tasks"+human-in-loop-required|OCC-community-bank-BSA-relief(up-to-$30B)|CDD-rule:beneficial-ownership-ID-at-account-opening-still-required,BUT-no-ongoing-re-verification-duty|!SIGNAL:regulatory-direction=risk-proportionate+technology-accepting+non-bank-scope-narrowing|src:FinCEN.gov,Federal-Register,Morrison-Foerster,Gibson-Dunn,CSIWeb|refreshed:2026-03-22|next:2026-04-22]
R[MTMA-adoption: 41-states-enacted(up-from-31-at-last-refresh)|2025-enactments:Colorado(Jul-2025),Massachusetts(Jan-2025),Mississippi(Jul-2025),Nebraska(Oct-2025)|Virginia-effective-Jul-2026|trust-company-exemption:confirmed-in-model-act→charter-solves-money-transmitter-across-41-states|CSBS-claims-99%-of-money-transmission-activity-covered|!UPDATE-FROM-PRIOR:+10-states-since-26.3.11-refresh(31→41)|remaining-non-MTMA-states=diminishing-relevance|src:CSBS.org,Alston-Bird,Ankura,Brownstein|refreshed:2026-03-22|next:2026-04-22]
R[CRD6-cross-border: transposition-deadline:Jan-10-2026(member-state-law)|core-banking-licensing:effective-Jan-11-2027|grandfathering:contracts-pre-Jul-11-2026=exempt|core-banking="deposits+lending+guarantees/commitments"|reverse-solicitation-exemption-narrow("own-exclusive-initiative")|!KEY-ANALYSIS:loan-agency/trustee=likely-NOT-"core-banking"(Mayer-Brown-Apr-2025+DLA-Piper-Nov-2025+3-more-law-firms)|BUT-member-state-fragmentation-risk(France-banking-monopoly-may-be-broader)|third-country-branch-required-only-for-core-banking→loan-agency-likely-exempt|Norton-Rose-Fulbright+A&O-Shearman-confirm-complexity+firm-specific-analysis-needed|!UPGRADE-from-MEDIUM→MEDIUM-HIGH-confidence-on-loan-agency-exemption(5-law-firm-consensus)|src:Mayer-Brown,DLA-Piper,Norton-Rose-Fulbright,A&O-Shearman,Clifford-Chance,BCLP|refreshed:2026-03-22|next:2026-04-22]
R[EU-Credit-Servicing-Directive: Directive-2021/2167-on-credit-servicers+purchasers(NPL-focused)|transposition-deadline:Dec-29-2023|26/27-member-states-transposed-as-of-Dec-2025|infringement-proceedings-pending:Bulgaria,Finland,Hungary,Netherlands,Portugal,Spain|Netherlands-late-implementation:Jul-18-2025|!RELEVANCE:creates-licensing-framework-for-loan-servicers-of-bank-originated-NPLs-in-EU→potential-model-for-broader-loan-admin-licensing|scope:NPL-only(currently)→may-expand|src:EUR-Lex,Schoenherr,Ashurst,Reed-Smith,Stibbe|refreshed:2026-03-22|next:2026-04-22]
R[UK-regulatory: FCA-AIFM-reform:HM-Treasury-consultation-closed-Jun-2025→draft-SI-pending→FCA-rules-consultation-H1-2026|trustee/depository-of-AIF:regulated-activity-under-review-as-part-of-AIFM-tiering|"Brexit-dividend"-simplification-intent|FCA-2026-priorities:overseas-banks-UK-subsidiaries-and-branches|!LOAN-AGENCY-SPECIFIC:FCA-authorization-still-required-for-payment-services(PSD2-equivalent)|GLAS-UK-precedent-validated|timeline:6-12mo,$100-300K(unchanged-from-prior)|src:EY-UK-2026-outlook,FCA-Regulatory-Initiatives-Grid-Dec-2025,Skadden,Browne-Jacobson,Womble-Bond-Dickinson|refreshed:2026-03-22|next:2026-04-22]
R[NH-trust-charter: process-unchanged|$5K-app-fee|$500K-min-capital($1.25M-practical-with-$1M-surety)|4-6mo-timeline|background-check-fee-reduced-$48.25→$47(May-2025)|pre-filing-meeting-standard|!CONTEXT:OCC-national-trust-bank-charter-now-more-attractive-alternative(non-fiduciary-activities-expansion+federal-preemption)|NH-NDTC-remains-faster+cheaper-for-pure-fiduciary-scope|state-vs-federal-decision-now=scope-dependent(fiduciary-only→NH|fiduciary+custody+stablecoin→OCC)|Crypto.com-path:state→OCC-conversion=validated|src:NH-Banking-Dept,GCG-Law,McLane-Middleton|refreshed:2026-03-22|next:2026-04-22]
R[SOC2-ISO27001-2026: ISO-27001:2022-transition-deadline:Oct-2025(orgs-must-upgrade-from-2013)|SOC2-2026-AICPA-trust-services-criteria:AI-governance-controls-added(model-training-docs,bias-testing,output-validation,data-lineage-tracking,explainable-AI)|enhanced-requirements:MFA,AES-256,immutable-audit-logging,RBAC,continuous-monitoring|financial-services-specific:AI-driven-data-extraction-must-demonstrate-processing-integrity|pricing:$30-150K-first-yr-SOC2(validated-5-sources)|timeline:12-18mo-from-start(SOC2-Type-II)|!KEY-UPDATE:AI-governance-requirements=NEW-since-last-refresh→loan-admin-platforms-using-AI-must-address-in-SOC2-scope|src:Konfirmity,EY-AccountingLink,AICPA,Sprinto,DSALTA,Secureframe|refreshed:2026-03-22|next:2026-04-22]
R[state-licensing-loan-admin: CT+NE-expanded-licensing-to-third-party-marketers+servicers-of-IDI-consumer-loans|student-loan-servicing:15+-jurisdictions-require-license(CA,CO,CT,LA,ME,MD+others)|CA-DFAL-effective-Jul-1-2026(replaces-DFPI-licensing)|CA-annual-assessments-increased($3K-no-activity,$15K-active)|!CRITICAL-DISTINCTION-MAINTAINED:syndicated-loan-"admin-agent"(B2B-institutional)≠consumer-"loan-servicer"→state-consumer-lending-licenses-NOT-applicable|NMLS-not-required-for-institutional-loan-agency|state-licensing-expansion=consumer-focused→institutional-loan-admin-remains-outside-scope|src:Katten,Mayer-Brown,Consumer-Finance-Monitor,Cornerstone-Licensing|refreshed:2026-03-22|next:2026-04-22]
R[private-credit-market-context: AUM=$3T(start-2025)→$5T(2029-est,Morgan-Stanley)|US-segment:$500B→$1.3T-in-5yr|2025-fundraising:$224.25B-global(+3.2%-YoY)|direct-lending=$91.36B(2x-next-strategy)|private-credit-CLOs=20-25%-of-issuance(up-from-10%)|SEC-2026-exam-priorities:valuation-methodologies+MNPI-handling+lender-group-participation+third-party-oversight|Form-PF-compliance-extended→Oct-2026|Regulation-S-P(data-security):large-firms-Dec-2025,smaller-Jun-2026|private-fund-adviser-rules-VACATED(5th-Circuit-Jun-2024)|!TAM-SIGNAL:$3T→$5T-growth+regulatory-complexity-increase=expanding-demand-for-specialized-loan-admin+trustee-services|SEC-exam-focus-on-third-party-oversight=validates-compliance-as-differentiator|src:Morgan-Stanley,WithIntelligence,Cleary-Gottlieb,S&P-Global,Akerman,Kirkland-Ellis|refreshed:2026-03-22|next:2026-04-22]
R[bank-fintech-third-party-risk: interagency-guidance-Jun-2023(Fed+FDIC+OCC):banks-retain-full-responsibility-for-third-party-relationships|May-2024-community-bank-guide|RFI-on-bank-fintech-arrangements-issued-2024(responses-under-review)|2026-direction:more-rigorous-onboarding+deeper-due-diligence+ongoing-monitoring-of-fintech-partners|!IMPLICATION-for-loan-admin:trust-chartered-entity=bank→direct-regulatory-relationship(¬dependent-on-bank-partner-oversight)|SaaS-only-entity=third-party→subject-to-bank-partner's-risk-framework→less-control|charter-advantage:direct-examiner-relationship+own-compliance-program→institutional-confidence|src:Fed-FRRS,FDIC-FIL,OCC-Bulletin-2023-17,InnReg,Venable|refreshed:2026-03-22|next:2026-04-22]

## calibrations-refresh(2026-03-22)
C[26.3.22] OCC-chartering-environment: MOST-FAVORABLE-IN-DECADE|confirmed+strengthened|11-in-83-days+20-filings+non-fiduciary-expansion|confidence:HIGH
C[26.3.22] MTMA-41-states: UP-FROM-31(26.3.11)→41(now)|99%-activity-covered|confidence:HIGH
C[26.3.22] CRD6-loan-agency-exemption: MAINTAINED-MEDIUM-HIGH|5-law-firm-consensus-maintained|no-contradictory-developments|confidence:MEDIUM-HIGH
C[26.3.22] NH-vs-OCC-charter-decision: NEW-calculus|OCC-non-fiduciary-expansion-makes-federal-charter-more-attractive-for-broader-scope|NH-still-faster+cheaper-for-fiduciary-only|confidence:HIGH
C[26.3.22] SOC2-AI-governance: NEW-requirement|AICPA-trust-services-criteria-updated→AI-using-loan-admin-platforms-must-address|confidence:HIGH
C[26.3.22] FinCEN-IA-AML-delay: confirmed-Jan-2028|signals-non-bank-scope-narrowing-under-current-admin|confidence:HIGH
C[26.3.22] private-credit-TAM-$3T→$5T: Morgan-Stanley+S&P-validated|fundraising-+3.2%-YoY|confidence:HIGH
C[26.3.22] GENIUS-Act-trust-company-preservation: statutory-language-explicit|trust-cos-retain-all-existing-authority|confidence:HIGH

## key-changes-since-last-refresh(26.3.12→26.3.22)
1. OCC-12-CFR-5.20-finalized(Apr-1-2026):non-fiduciary-expansion→broadens-trust-charter-utility
2. MTMA:31→41-states(+10)
3. SOC2-AI-governance-requirements:NEW-criteria-for-AI-systems
4. FinCEN-IA-AML-delay:confirmed-Jan-2028
5. GENIUS-Act-OCC-rulemaking:proposed-Mar-2-2026→comment-May-1-2026
6. EU-Credit-Servicing-Directive:26/27-MS-transposed
7. UK-AIFM-reform:FCA-rules-consultation-H1-2026
8. NH-vs-OCC-charter-calculus:shifted-toward-OCC-for-broader-scope-entities
9. private-credit-AUM:$3T-confirmed(start-2025)→$5T(2029)
10. SEC-2026-exam-priorities:third-party-oversight+valuation→validates-compliance-differentiator

## loan-admin-KB-refresh(26.4.09)

### KEY UPDATES SINCE 26.3.22

**CRITICAL — HMRC concession deadline PASSED**
April 5, 2026 deadline for borrowers to disclose interest payments made without HMRC Direction (under paused concession). Deadline has now passed. Borrowers who missed it face full WHT + late-payment interest on 2021-22 tax year. Doc5 urgent flag must be updated. No reinstatement announced.
C[26.4.09] HMRC-concession-deadline-passed: HIGH-confidence |Mayer Brown Jan 2026 + Travers Smith Jan 2026 + HMRC INTM413205 |post-deadline guidance language needed

**Basel III re-proposal issued March 19, 2026**
Capital-REDUCING (not neutral): ~4.8-5.2% CET1 reduction large banks, ~7.8% smaller banks. Comment period June 18, 2026. More favorable than analysis-bundle "capital-neutral" prediction. Tailwind for private credit market stronger than predicted.
C[26.4.09] Basel-re-proposal-capital-reducing: HIGH-confidence |Fed/OCC/FDIC joint press release Mar 19 |supersedes "capital-neutral" prediction

**OCC 12 CFR 5.20 effective April 1, 2026**
Non-fiduciary activities expansion rule CONFIRMED effective. Coinbase National Trust Company conditional OCC approval April 2, 2026. Charter environment remains most favorable in decade. NH NDTC still valid for pure fiduciary scope; OCC now explicitly viable for broader-scope entity.
C[26.4.09] OCC-rule-effective: HIGH-confidence |CONFIRMED Apr 1

**CRD6 grandfathering — 93 days from April 9, 2026**
Pre-Jul 11, 2026 contracts exempt from Jan 2027 core banking licensing. Operational urgency: new EU mandates should be contracted before Jul 11, 2026.
C[26.4.09] CRD6-grandfathering-93-days: HIGH-confidence |Jan 11 2027 effective = pre-Jul 11 2026 contracts exempt

**MTMA state count DISCREPANCY — 31 vs 41**
My 26.3.22 refresh: 41 states. CSBS primary page Mar 2026: 31 states. Virginia enacted Jul-2026 (not yet active). 41-state figure may include introduced-not-enacted. Cannot confirm without CSBS MTMA tracker direct verification. Working assumption: use 31 (enacted-only) until confirmed otherwise.
C[26.4.09] MTMA-enacted-count: LOW-MEDIUM confidence |discrepancy unresolved |31=conservative enacted-only

**UK WHT 22% rate increase**
Finance Bill 2025-26 progressing, 20%→22% from April 6, 2027. No change to prior finding. Analysis-bundle missing this.

### KB ACCURACY ASSESSMENT
Doc5: HIGH accuracy overall. HMRC urgent flag STALE (actionable). [VERIFY] tags functioning correctly.
Doc6 §6.1: HIGH accuracy. Basel [VERIFY] tag triggered. Leveraged lending guidance tag valid.
Doc6 §1.6: MTMA count (31) consistent with conservative enacted-only count.
Analysis-bundle: VALID core findings. Basel framing needs update. CRD6 grandfathering needs countdown language.
