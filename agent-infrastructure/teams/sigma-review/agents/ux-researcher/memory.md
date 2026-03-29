# ux-researcher — personal memory

## identity
role: UX research specialist
domain: usability,accessibility,mental-models,information-architecture,learnability
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## known systems
sigma-mem[3 user types: AI consumer, human maintainer, developer setting up MCP|26.3.7]
hateoas-agent[user=Python developer building AI agent tools, pip install framework|26.3.7]
sigma-system-overview[entry point for full system, submodules, setup.sh, ARCHITECTURE.md, case study|26.3.7]

## past findings
review-1(sigma-mem,26.3.7): AI-user well-served, human-user underserved(opaque notation), dev setup clean |#4
review-2(sigma-mem,26.3.7): weighted scoring improves state detection, substring matching fragile |#4
review-3(sigma-mem,26.3.7): team memory high-learnability(self-teaching via consistent schema), wake-for fragile-at-scale |#4
review-4(hateoas-agent,26.3.7): DX grade B+, quick-start not copy-pasteable(!), 3-API-styles=choice-anxiety, _state-silent-failure(!), no-startup-validation(!), 30+-exports-overwhelming, progressive-disclosure excellent, aha-moment lands in 60s |#10
review-5(hateoas-agent,26.3.7): DX grade A-, 6/6 review-4 blockers resolved, _state-docs-still-needed(!), Resource.validate()-parity-missing |#3
review-6(hateoas-agent,26.3.7): DX grade A-(holding), 3 resolved(_state-docs,Resource.validate,errors-future-import), error-msgs-hit-fix-it-tier(Google hierarchy), validate-at-init-pattern-complete-across-all-entry-points(Runner+serve), no-regressions, 12-examples-accurate |#7
review-7(full-system,26.3.7): DX grade A(upgrade from A-), 6 dimensions assessed, first-contact(A)+hateoas-agent(A)+sigma-mem(A-)+ΣComm(A)+agent-infra(A)+error-msgs(A), 3 sigma-mem-README-issues(stats-stale,URL-wrong,pip-install-fails) independently confirmed by product-strategist+technical-writer, systemic-doc-quality(SETUP.md+ARCHITECTURE.md+case-study+setup.sh) lifts system from good-components to coherent-discoverable-system |#10
review-8(thriveapp,26.3.8): UX grade A-, behav-sci(A)+accessibility(A-)+messaging(A)+ethics(A)+consistency(A-) | 0C/0H/2M/4L/3I | all 10 behavioral-science constraints verified+tested | substance.tsx hardcoded-to-alcohol(!), check-in.ts:45 leaks "domain" | cross-ref: tech-architect S3 notes-encryption ethics-confirmed, technical-writer D5 sort-order UX-confirmed | first non-sigma-system review, first React Native/mobile review | SHIP phase 4 |#9
review-10(hateoas-agent,26.3.25): DX grade A-(held) | Q3+Q4+Q6+H1+H2 | post-DA: F-UX1(!H upheld-anchor), F-UX2(M upheld), F-UX3(LOW revised-from-M,IDE-plugin-framing-dropped,ergonomic+parity-gap-only), F-UX4(L upheld), F-UX5(INFO downgraded-from-L,Hick's-law-¬applicable-to-docs) | H1:PARTIAL(F-UX1-sole-blocker) | H2:CONFIRMED-observability | DA-revisions:2-concede+1-source-tag+1-uphold | xverify:gpt-5.1=uncertain(upheld) | 3-agent-convergence-F-UX1(CQA+TA+UXR) |#4-post-DA

## calibration
C[dual-user tension is accepted tradeoff not a bug|1|26.3]
C[hateoas-agent overall DX is A at v0.1.0 — upgraded review 7; held at A- in review-10(v0.2) due to guard observability gap|3|26.3]
C[action-centric API is the correct default recommendation|1|26.3]
C[startup validation is the single highest-impact DX improvement — now resolved|2|26.3]
C[error messages meeting fix-it tier is achievable and worth maintaining|1|26.3]
C[hateoas-agent guard exceptions: fail-closed(exclude on exc) is correct security default; but exception≠guard-returning-False — distinct failure modes require distinct signals; fix=WARNING log+guard_strict param ¬change fail-closed behavior|1|26.3]
C[programmatic state-graph introspection (get_state_map) is the key extensibility gap for external tooling authors — mermaid covers human debugging but ¬machine-readable|1|26.3]
C[delta reviews converge quickly when prior findings are tracked — 3 rounds found diminishing issues|1|26.3]
C[systemic documentation(setup automation+architecture narrative+case study) is what upgrades DX from A- to A — individual component quality is necessary but not sufficient|1|26.3]
C[cross-repo URL/stat consistency is the most common DX blocker in multi-repo projects — 3 agents found same issue independently|1|26.3]
C[behavioral science constraints can be fully verified by code audit — all 10 thriveapp constraints had verifiable code+test evidence|1|26.3]
C[health/wellness apps: gain-framing is the single most important messaging constraint — one violation can cause real psychological harm in target population|1|26.3]
C[React Native accessibility is mature — accessibilityLabel+Role+State+Hint+LiveRegion cover most WCAG needs|1|26.3]
C[error messages on rare paths still matter for terminology consistency — users who hit errors are already frustrated|1|26.3]

## patterns
dual-user-systems: optimize for primary consumer, provide translation layer for secondary
self-teaching-formats: consistent schema teaches format through repetition
hateoas-not-missing: framework handles action advertisement at MCP layer
progressive-disclosure-ladder: additive layers that never require restructuring previous code
decorator-familiarity: reusing patterns from established frameworks (Flask/FastAPI) for instant recognition
silent-failure-risk: implicit conventions(_state key) that fail silently are top DX hazard in convention-over-configuration frameworks — mitigated in hateoas-agent via warning-on-omit + docs
validate-everywhere: startup validation should cover all entry points (Runner, serve, multi-resource) — hasattr pattern enables backward compat
error-msg-consistency: when validate() exists on multiple classes (StateMachine+Resource), error message structure should match for API consistency
setup-as-dx-lever: idempotent setup scripts with prerequisite checks+test verification+colored output transform DX grade — setup.sh is the strongest single DX artifact in the system
cross-repo-consistency: multi-repo projects need a consistency checklist (URLs, stats, install commands, terminology) — independent agents find same issues, confirming this is a real category
health-app-messaging-audit: behavioral science constraints require exhaustive string audit — grep for forbidden patterns + manual review of every user-facing message. Test files that verify forbidden language are the strongest safety net.
feature-flag-as-ux-gate: hidden features (not grayed out, not "coming soon") is correct UX for health apps — avoids creating expectation for unbuilt features
terminology-consistency-extends-to-errors: user-facing copy rules (e.g., "focus areas" not "domains") must extend to error messages — rare paths still shape user mental models
sort-order-matters-for-framing: the first item in a list sets the user's frame — putting substance use first foregrounds clinical use case, putting exercise first foregrounds wellness

¬[accessibility concerns — CLI/MCP tool, WCAG doesn't apply directly]

## research

R[dx-python-2026: FastAPI dominant(type-hints+auto-docs+async), Pydantic v2 standard(Rust core,5-50x faster,v2.12.5), runtime validation=first-class design concern not afterthought, type-safety trio(mypy+pydantic+runtime) is 2026 norm |src: devtoolbox.dedyn.io,dasroot.net,docs.pydantic.dev |refreshed: 26.3.7 |next: 26.4]

R[api-usability-research: arXiv 2601.16705(Jan 2026) identified 8 factors for REST API usability: conventions(9/16 devs), intuitiveness(6/16), self-explanatory(5/16 "understand without docs"), tool-support(machine-readable). Guidelines themselves inconsistent across orgs re: error-handling+docs. Factory pattern slowed devs 10x vs simpler alternatives |src: arxiv.org/html/2601.16705v1 |refreshed: 26.3.7 |next: 26.4]

R[error-msg-design: Google published dedicated error-msg course: structure=what-wrong+how-fix+further-help, specific-examples(not "Invalid input"), active-voice, progressive-disclosure for length. NN/g scoring rubric(Nov 2024): 12 guidelines, 4-point scale, min 3 error indicators(WCAG-AA). Hierarchy: fix-it-actions(system knows value)>show-it-actions(system shows where)>tell-it-actions(text only) |src: developers.google.com/tech-writing/error-messages,nngroup.com/articles/error-messages-scoring-rubric |refreshed: 26.3.7 |next: 26.4]

R[docs-adoption: llms.txt emerging standard(Howard 2024)—markdown site-map for LLMs, 844K+ sites by Oct 2025, Anthropic+Stripe+Cloudflare adopted, Mintlify auto-generates, but no AI platform confirmed reading it. Progressive-disclosure in docs=40-60% context reduction(slim index+on-demand detail). 64% devs use AI for docs(2025 survey). Docs-as-code+AI-native platforms converging |src: mintlify.com,bluehost.com,fluidtopics.com |refreshed: 26.3.7 |next: 26.4]

R[usability-frameworks: Nielsen 10 heuristics unchanged(1994, text updated 2020). Dain reframe→3 principles: system-behavior+mental-models+interaction-momentum—"survive complexity with confidence" not surface checklist. AHP integration(2025) transforms qualitative heuristics→quantifiable metrics. Dev-tools lens: cognitive-load-reduction is primary metric—AI handles mechanical(syntax,boilerplate), frees energy for architecture |src: medium.com/design-bootcamp,tandfonline.com,nngroup.com |refreshed: 26.3.7 |next: 26.4]

R[review-implications: (1) validate-at-init confirmed—Pydantic proves runtime-validation-as-design wins, (2) error msgs must answer what-wrong+how-fix with progressive disclosure+fix-it hierarchy, (3) self-explanatory("understand without docs") confirmed top usability factor(arXiv 2026), (4) llms.txt relevant for AI-consumer projects, (5) cognitive-load-reduction>feature-completeness for DX grading, (6) conventions-adherence most cited API usability factor(9/16 devs) |refreshed: 26.3.7 |next: 26.4]


## warehouse-lms-research (2026-03-14)

R[warehouse-worker-interfaces: devices=handheld(Zebra TC52/TC72,Honeywell)+wearable(ring scanners ProGlove/Hyco,smart glasses RealWear/Vuzix)+voice(Honeywell Vocollect,Lucas Jennifer)|handheld=rugged Android,5"+screen,glove-compatible,IP67/68,all-shift battery|ring scanners=hands-free,50% scan-time reduction,BLE,<50g|smart glasses=DHL 15-25% productivity gain,heads-up display,voice+visual multimodal|voice=hands-free eyes-free,check-digit confirm,99.99% accuracy,30+ languages,works in noise/cold/dark|multimodal trending: voice+scan+light+screen combinations|form-factor selection: voice for high-volume(picking),handheld for complex(receiving/QC),ring+handheld for putaway,glasses for vision picking|src:lucasware.com,honeywell.com,realwear.com,supplychaindive.com|refreshed:2026-03-14|next:2026-04-14]

R[supervisor-dashboards: core-views=real-time productivity(per-worker/zone/task),labor-utilization(%productive-vs-indirect),exception-alerts,shift-planning,coaching-queue|design-patterns=command-center(wall-mounted)+mobile-supervisor(tablet)+desktop-analytics(deep-dive)|alert-hierarchy=critical(safety)>urgent(labor-gap)>informational(milestone)|exception-management=variance-codes(distinguish worker-issue vs system-issue),auto-coaching-triggers(proactive not punitive)|KPIs=UPH,cost-per-unit,utilization%,accuracy%,safety-incidents|digital-twin-integration=15% cost-reduction(McKinsey)|src:takt.io,manh.com,rebus.io,easymetrics.com|refreshed:2026-03-14|next:2026-04-14]

R[robot-human-interaction-ux: models=goods-to-person(AMR brings items:Locus,Chuck)+person-to-goods-guided(AMR leads worker)+zone-collaborative(cobots)|worker-interface=AMR-screen(Chuck:touchscreen,SKU info,15-min onboarding),light-indicators(LED status),zone-boundary(floor projections)|safety=ISO 10218:2025,force-limiting,AI 3D vision,speed-reduction-on-proximity,audible+visual alerts|handoff=AMR arrives→notification→worker picks→scan confirm→AMR departs(zero-training)|sentiment=85% feel automation improves collaboration,90% trust automation|gamification-on-AMR controversial:some managers disable leaderboards(cherry-picking)|src:locusrobotics.com,ocadointelligentautomation.com,standardbots.com|refreshed:2026-03-14|next:2026-04-14]

R[warehouse-accessibility: multilingual=critical(30+ languages),Lucas Jennifer 30+ lang+accent-tolerance,voice bypasses literacy|literacy=icon-based interfaces,color-coding,pictographic instructions|noise=80-100dB typical,RealWear noise-cancel to 100dB,haptic supplements audio|glove-compatible=projective capacitive,min 60px+ touch targets,physical buttons for cold storage|cold-storage=high-brightness(1000+ nits),anti-fog,condensation-resistant,e-ink for extreme cold|shift-fatigue=cognitive load reduction,progressive disclosure,shorter travel paths,focused notifications|ADA=wider aisles,adjustable-height workstations,voice-only mode|src:izisafety.com,glaciercomputer.com,opsdesign.com|refreshed:2026-03-14|next:2026-04-14]

R[warehouse-gamification: adoption=84% workers more likely to stay,3-5% productivity gain(Kenco),Amazon FC Games expanded 20+ states|what-works=goal-tracking-vs-personal-best,team challenges,real-time progress on devices,badges/achievements,voluntary participation|what-doesn't=mandatory participation,pure peer-ranking(bottom discouraged),rate-based-only(unsafe speed),punishment-tied|controversy=surveillance-vs-motivation,Amazon injury rates,worker advocates warn "turning humans into automatons"|design-principles=opt-in,anonymous option,team+individual,safety weighted equal,celebrate improvement not absolute|src:supplychaindive.com,koerber.com,mmh.com|refreshed:2026-03-14|next:2026-04-14]

R[warehouse-onboarding: time-to-productivity=avg 5-6mo fully productive,target 2-4wk basic,good onboarding +82% retention +70% productivity|patterns=microlearning(bite-sized>3hr lectures),mobile-first(-95% training time),video+visual-first,multilingual,on-device guided workflows,buddy/mentor|digital=AR-guided(glasses overlay),simulation mode(practice),progressive task complexity,real-time coaching(detect hesitation→help)|reduction-through-UX=Chuck AMR 15-min onboarding,voice call-and-response=natural learning|temp-worker=system must support day-1 productivity,self-guided essential|src:how.fm,softeon.com,rfgen.com|refreshed:2026-03-14|next:2026-04-14]

R[warehouse-real-time-feedback: modalities=haptic(vibration for wrong-bin/unsafe-lift,ProGlove+Modjoul SmartBelt)+audio(voice performance updates,tones,alerts)+visual(color-change,progress bars,LED)|cadence=immediate-per-action(scan confirm)+periodic(hourly pace)+shift-summary|what-to-surface=pace-vs-goal%,accuracy-streak,next-task-preview,estimated-shift-completion,safety-reminders|hierarchy=confirmation(subtle:beep/green)→coaching(moderate:voice prompt)→alert(strong:haptic+audio+visual)→escalation(supervisor)|anti-patterns=constant-metric-display(anxiety),negative-only,delayed>5min,peer-comparison-push(privacy)|multimodal-best-practice=loud zone=haptic+visual,quiet=audio+visual,hands-occupied=audio+haptic|src:peaktech.com,datexcorp.com,logiwa.com|refreshed:2026-03-14|next:2026-04-14]

R[warehouse-multimodal-integration: combinations=voice+scan(most common)+voice+light(zone then slot)+voice+vision(glasses+command)+scan+light(put-to-light)+full multimodal|pick-to-light=LEDs at bins,fast-mover areas,reduces search time|put-to-light=scan item→illuminates destination,ideal sorting/packing|context-switching=voice in pick aisles→screen at pack→light at sort wall,transparent transitions|design-principle=match modality to task-context:hands-busy=voice,eyes-busy=haptic,noisy=visual,cold/gloves=voice,complex=screen,simple=light/beep|no single vendor covers all modalities end-to-end|src:lucasware.com,zetes.com,mecalux.com|refreshed:2026-03-14|next:2026-04-14]

R[warehouse-lms-novel-ux: digital-twin-worker-view(PepsiCo 20%,Siemens 2026,Nvidia Omniverse)=ops-consensus BUT worker-facing=novel,2D-first=80%@20%|AR-nav(DHL 15-25%,$1500-3000/unit)=proven-expensive,voice-nav=70%|predictive-fatigue(BaselineNC 98%,Bodytrak,Modjoul)=wearables exist BUT none LMS-integrated=novel,self-report phase-1|shift-adaptive-UI=NO vendor+NO precedent,automotive-transferred,LOW=phase-1|coaching-assistant=none warehouse+LMS+real-time|src:synkrato.com,aufaitux.com,ihf.co.uk,baselinenc.com,bodytrak.co|refreshed:2026-03-14|next:2026-04-14]

R[warehouse-surveillance-ethics: arXiv 2508.09438(2025)=workers sacrifice quality+safety for metrics|arXiv 2412.06945(2024)="Losing Game"=resistance via hacks+quality-sacrifice|Gartner 40% gamification by 2028|Amazon FC Games 20+ states+injury scrutiny|no controlled ethical-vs-surveillance study|privacy-first=no vendor selling point=gap|src:arxiv.org,dl.acm.org,mmh.com|refreshed:2026-03-14|next:2026-04-14]

F[warehouse-lms,26.3.14] r1: 10 findings(3!C+5H+1M+1 novel) |see workspace |key: multimodal-unified=differentiator,accessibility-as-architecture,surveillance=existential,ethical-gamification=refuse-to-build,5 novel phased(N4=phase-1),3 outcome-1(scope-reductions),2 outcome-3(vendor-sentiment,ethical-evidence) |#10

C[warehouse-lms: worker-facing digital twin(2D zone-map)=genuinely novel,low cost relative to ops-level twin — no competitor offers worker-level spatial awareness|1|26.3]
C[warehouse-lms: shift-adaptive-UI=highest impact/cost ratio of all novel features — time-based config,no hardware,no ML,no integration,no precedent in warehouse|1|26.3]
C[warehouse-lms: surveillance-perception is existential ¬nice-to-have — academic evidence(2024-2025) shows implementations fail when workers resist, privacy-first must be architectural ¬policy|1|26.3]
C[warehouse-lms: ethical gamification differentiation=what you REFUSE to build(peer-rank,mandatory,punitive-linked) — but no controlled evidence it produces different outcomes than surveillance gamification|1|26.3]
C[warehouse-lms: surveillance risk=compliance-cost+union-friction(38% contracts) ¬existential-adoption-blocker — DA[#8] corrected: 42% employees report monitoring,LMS succeeds commercially,Amazon 1.5M workers. Academic framing(arXiv)≠warehouse worker reality. Downgraded !C→H|1|26.3]
C[warehouse-lms: multimodal=platform-play(orchestrate specialists via APIs) ¬feature-play(build all modalities). Lucas/Honeywell voice APIs=weeks integration. ProGlove/Modjoul haptic APIs exist. BUILD dashboard+handheld+zone-map, PARTNER voice+haptic+light, DEFER AR|1|26.3]
C[warehouse-lms: 80% of UX findings deliver value WITHOUT robots — robot-independent(F1,F2,F4-F8,F9-N4/N5,F10) vs robot-dependent(unified-perf-model robot metrics,robot scheduling). Product viable human-only,upgrades to mixed. "Robot-ready" ¬"robot-required" positioning|1|26.3]

F[warehouse-lms,26.3.14] r2: 3 DA challenges(#8,#14a,#14d) → 3 revisions: F10 !C→H(compliance ¬existential),F2 multimodal→platform(build-partner-defer),findings re-tiered by robot-dependency(80% robot-independent). Key insight: robot-independence STRENGTHENS case |#3

review-9(warehouse-lms,26.3.14): UX grade N/A(market-analysis ¬product-review), 10 findings r1 + 3 DA revisions r2, first warehouse/industrial domain, first multi-agent-convergence with 4 peers+DA simultaneously, first robot-human-interaction analysis, DA challenges all produced genuine revisions(3/3 COMPROMISE) |#13

## warehouse-game-design-review (2026-03-18)

R[game-based-assessment: gamefully-designed=correct-category(mechanics-ARE-measurement ¬wrapper)|ecological-validity-ceiling:cognitive-tasks r=0.30-0.45,physical-routing UNVALIDATED|warehouse-specific-routing=novel,no-direct-analogues|meta-analysis:game→job-performance r=0.29|personality-via-game "consistently-failed"|flow-state reduces faking MORE than self-report|two-layer-IA standard(show-state,collect-process)|src:Landers-2022-IJSA,PMC9891208,PMC3969247,Frontiers-Education-2024|refreshed:2026-03-18|next:2026-04-18]

R[warehouse-gamification-ethics-2025: arxiv-2508.09438=2yr-Amazon-FC-ethnography,workers-game-algorithmic-management-systems|PMC10026198=AI-surveillance-policy-primer,CA/EU/UK-regulatory-frameworks|Gartner-40%-warehouse-gamification-by-2028|Amazon-FC-Games-injury-scrutiny|engagement-vs-surveillance-frame=DETERMINATIVE for worker authenticity|transparent-framing=strategically-optimal+ethically-required|src:arxiv.org,pmc.ncbi,mmh.com|refreshed:2026-03-18|next:2026-04-18]

C[warehouse-game: gamefully-designed ¬gamified for assessment — feedback during session teaches before measuring,destroys construct validity|1|26.3]
C[warehouse-game: engagement-authenticity corridor is narrow — competitive mechanics destroy authenticity;intrinsic/narrative preserves it;points must reward completion ¬efficiency|1|26.3]
C[warehouse-game: transparent framing is BOTH ethical requirement AND validity strategy — deceptive framing produces short-term data+long-term validity destruction|1|26.3]
C[warehouse-game: two-layer IA is standard — show scenario state,collect process data(route-order,timing,backtrack) silently WITH consent|1|26.3]
C[warehouse-game: H2(game patterns correlate with real performance) is WEAKEST hypothesis — tenure confound is key threat; treat as research question not assumption|1|26.3]
C[warehouse-game: H5(physical friction=divergence point) highest confidence — may understate human-centric(scan-trip,human-coordination) vs robot-centric friction per 80%-robot-independent prior finding|1|26.3]
C[warehouse-game: accessibility for warehouse demographics=non-negotiable first-class constraint — icon-first,audio-option,PWA/no-install,sub-3min-sessions,offline-capable|1|26.3]

F[warehouse-game,26.3.18] r1: 7 findings(UX-R1→UX-R7), hygiene-all-3-checks-complete, 4 outcome-3 gaps flagged(UX-OQ1-OQ4), 8 cross-agent convergences confirmed(TA+RCA), prompt-laundering verdict=launderable-WITH-modifications |#7

F[warehouse-game,26.3.18] r3: DA#1=CONCEDE(partial) DA#6=COMPROMISE DA#9=CONCEDE |
DA#1: game justified for scale BUT scale is prompt assumption ¬independently-verified; scale decision gate added to UX-R7(single-facility<200→think-aloud+WMS-first;multi-facility→game justified) |
DA#6: 5 condition conflicts modeled—(1)transparent-framing-vs-Hawthorne=worker-as-expert framing resolves IF architecture-silo-real(framing¬sufficient without architecture); (2)no-feedback-vs-engagement=suppress efficiency feedback only ¬all feedback; (3)sub-3min-vs-rich-scenarios=two-mode design(Mode-A:single-decision-probes 60-90s,Mode-B:full-routing 5-8min; Mode-A validates before Mode-B built); (4)zone-taxonomy-vs-tenure-control=home+novel dual-scenario(confound→measurement); (5)voluntary-vs-representative=narrow claim to volunteer sample only |
DA#9: CONCEDE design methodology error—arxiv-2508.09438 ethnographic social-friction finding applied to consent(UX-R4/R5) but NOT to friction taxonomy(UX-R3); H5 downgraded from assumption→hypothesis-to-test; Category-C(social friction) deferral to v2 was error; ethnographic pre-research required before scenario design |
new-prerequisite-sequence: ethnographic-discovery(10-20 worker interviews) → scale-decision-gate → Mode-A-pilot → Mode-A-validation → Mode-B-design(only if Mode-A confirms signal) |
C[warehouse-game: H5 is hypothesis-to-test ¬assumption; physical layout friction ¬established as dominant worker-experienced friction — social/organizational(rate-pressure,supervisor) may dominate per arxiv-2508.09438; ethnographic pre-research required|1|26.3]
C[warehouse-game: scale is a prerequisite decision gate ¬assumption; single-facility→think-aloud+WMS-first; game justified at multi-facility scale|1|26.3]
C[warehouse-game: no-feedback constraint applies to efficiency feedback only ¬all feedback — completion progress + neutral framing acceptable during assessment window|1|26.3]
C[warehouse-game: transparent framing requires worker-as-expert framing(collective benefit) ¬individual-surveillance disclosure; credibility requires architectural silo — framing without architecture is theater|1|26.3] |#3
## workflow-automation-personnel-research (2026-03-18)

R[automation-change-management-2026: BCG(2024)=70% of automation challenges are people+process ¬technical; McKinsey=effective-change-mgmt→143%ROI vs 35% without; Prosci=ADKAR 67% success rate; visible-leadership-support +30% success; combining Kotter(org structure)+ADKAR(individual tracking)=modern best practice; baseline failure without change mgmt ~70-80% |src:prosci.com,bcg.com,mckinsey.com |refreshed:2026-03-18 |next:2026-04-18]

R[automation-pilot-to-scale-2026: MIT(2025)=95% of GenAI pilots fail to scale; 80.3% overall AI project failure; only 25% of orgs moved >40% pilots to production; 84% of failures leadership-driven(73% no clear metrics,68% underinvest foundations,56% lose C-suite sponsorship in 6mo); mid-market reaches full deployment 3x faster than large enterprise(scope effect, ¬inherent success rate difference) |src:fortune.com/MIT,workato.com,pertamapartners.com |refreshed:2026-03-18 |next:2026-04-18]

R[automation-resistance-2026: 3-dimensional resistance model=affective(fear,anxiety)+cognitive(perceived usefulness,trust)+behavioral(workarounds,avoidance); SME workers=67% job security fear vs MNC 43%; status-quo-bias=structural preference for familiar even when new is objectively better(MDPI/Systems 2023); 62% workers distrust AI re: data practices(Gartner); predictors=¬skills+¬trust+perceived-unfairness; employee-involvement=2.5x success; pre-implementation resistance assessment=+40% acceptance; 3 mitigation pillars=learning+communication+PARTICIPATION(¬top-down-only) |src:tandfonline.com,mdpi.com,sciencedirect.com,emerald.com |refreshed:2026-03-18 |next:2026-04-18]

R[automation-upskilling-2026: microlearning=80% completion vs 20% long-form; retention +25-60%; 93% orgs say essential; market $1.55B→$2.96B(2025); blended=technical+human skills; role-specific pathways > generic training; training during design ¬after deployment; DAPs(Digital Adoption Platforms)=in-tool real-time guidance=superior to pre-training; Amazon Mechatronics Apprenticeship=hourly→robotics,+40% wages; Walmart Live Better U=doubled certs 2024; 66% executives cite skill gaps as priority(McKinsey) |src:engageli.com,elearningindustry.com,atlascopco.com,careerminds.com |refreshed:2026-03-18 |next:2026-04-18]

R[automation-role-evolution-2026: 50% of tasks(¬jobs) automatable(McKinsey); 90% execs expect automation to increase workforce capacity; +12% capacity confirmed in deployed orgs; customer service agents: task-driven→experience-orchestrators+problem-solvers; low-skill workers +35% speed with AI assistance; new roles=process-owners,automation-stewards,data-quality-monitors; caveat=orchestrator framing idealized, reality often=same headcount doing more tasks ¬genuine elevation |src:sharefile.com,callminer.com,goodcall.com |refreshed:2026-03-18 |next:2026-04-18]

R[automation-mid-market-specific-2026: mid-market challenges=lean-HR+lean-IT+¬dedicated-change-manager+¬enterprise-L&D; resistance spreads faster through close-knit social networks; mid-market advantages=3x faster full deployment,cheaper participatory design(flatter structure),leadership proximity(stronger signal); RPA ROI=150-300% over 2-3yr,payback 12-24mo; strategic posture=leverage proximity, compensate via microlearning+DAPs+peer-champions |src:baass.com,kpcteam.com,cisin.com |refreshed:2026-03-18 |next:2026-04-18]

F[workflow-automation-personnel,26.3.18] r1: 12 findings(UX-F1→UX-F12) | H1=PARTIALLY-FALSIFIED(failure rate far exceeds assumption,"properly planned"=5 specific factors) | H2=PARTIALLY-CONFIRMED(participation/co-design=critical missing factor) | Q4=fully-addressed | Q5,Q6,Q7=addressed | hygiene: all 12 findings tagged provenance+outcome | gap: no quantitative studies specifically 300-1000 employee range for change mgmt outcomes |#12

F[workflow-automation-personnel,26.3.18] r3: 8 DA challenges(#1,#2,#3,#7,#8,#10,#11+role-evolution) | 7 revised findings + 1 new finding | revisions:
- UX-F1-R3: BCG 70% re-scoped to [adjacent:AI-transformation], workflow automation people-factor = 35-50% contributing cause (not 70% primary)
- UX-F2-R3: MIT 95% GenAI stat retired from primary framing; workflow automation pilot-to-scale = 25-40%
- UX-F3-R3: Prosci confidence discounted to L (self-study); Gartner/CEB 34→58% (+24pp) substituted as primary independent anchor; Errida & Lotfi 2021 (peer-reviewed, 37-model) as academic corroboration
- UX-F6-R3: ADKAR>Kotter tagged as [agent-inference]; unsourced +30% stat removed; Gartner/CEB +24pp substituted
- UX-F8-R3: role elevation = PRIMARILY ASPIRATIONAL without intentional investment. McKinsey 2024 (5.7 hrs freed, 1.7 redirected = 3:1 waste ratio), ScienceDirect 2025 work intensification, BCG/IBM 89%/6% upskilling gap. OQ-UX2 RESOLVED.
- UX-F11-R3: elevated to headline finding; all 12 findings tagged [extrapolated-from-general/adjacent] with bias direction; OQ-UX1 confirmed unresolvable
- UX-NEW-F13: premise viability — automation conditional not universal; PR-SCORE decision gate
- PEOPLE-READINESS-SCORE (PR1-PR5): testable ex-ante operationalization with measurable thresholds |#7-revised+1-new

C[workflow-automation: 70/30 inversion=people/process are the hard part ¬tech; yet investment ratio is inverse — this is the single most important reframe for mid-market implementation planning|1|26.3]
C[workflow-automation: participation/co-design is distinct from change-management-as-communication — it is structural co-creation; 2.5x success multiplier makes it the highest-leverage intervention|1|26.3]
C[workflow-automation: mid-market has genuine advantages(proximity,speed,flatter structure) ¬just deficits — framing as "enterprise-lite" undervalues these structural benefits|1|26.3]
C[workflow-automation: training AFTER deployment establishes resistance patterns that are very difficult to reverse — sequence is architectural, not scheduling preference|1|26.3]
C[workflow-automation: "orchestrator" role framing is industry-idealized; implementation guide should acknowledge the gap between aspiration(role elevation) and common reality(same headcount,more tasks)|1|26.3]
C[workflow-automation-r3: CM source quality: always check if CM framework citation is from a firm selling that framework (Prosci/ADKAR = Prosci research; Kotter = dual-OS consulting). These are self-interested sources, not independent validation|1|26.3]
C[workflow-automation-r3: domain differentiation is load-bearing for failure rates — AI transformation / GenAI / digital transformation / RPA / workflow automation have materially different failure rates and failure modes. Never use GenAI or broad DT stats as primary evidence for iPaaS/low-code failure|1|26.3]
C[workflow-automation-r3: role elevation without intentional investment = work intensification in disguise. McKinsey 2024 is key evidence: 5.7 hrs freed / 1.7 redirected = 3:1 waste ratio. Default framing should be "aspirational without design" not "expected outcome"|1|26.3]
C[workflow-automation-r3: for workflow automation (not AI), people/resistance ranks #3 behind integration and skills deficits (Deloitte). Don't lead with people-first as if people = dominant failure cause — it's an important contributing factor but not the primary cause in isolation|1|26.3]
C[workflow-automation-r3: mid-market evidence gap confirmed unresolvable — no quantitative CM studies scoped to 300-1000 employees exist as of 26.3.18. This is a headline limitation, not a footnote. Every UX finding for this domain is extrapolated.|1|26.3]
C[workflow-automation-r3: "properly planned" tautology — any post-hoc list of success factors is unfalsifiable. Must convert to testable ex-ante criteria with measurable thresholds before implementation begins. PR-SCORE (PR1-PR5) is the pattern.|1|26.3]

## promotion (2026-03-28)

P[gate-heaviness-matches-action-reversibility|src:sigma-ui|promoted:26.3.28|class:calibration]
Gate modal weight must match action reversibility. Asymmetric gates (one branch round-scoped, another session-terminating) → adaptive tier: escalate to full-page only on irreversible branch. Fixed heavy tier for all paths → gate fatigue → rubber-stamping. Confirmed DA[#1]-COMPROMISE: exit-gate PASS=modal, FAIL=full-page.

P[setup.sh-as-DX-lever-multi-domain|src:sigma-ui|promoted:26.3.28|class:calibration]
Idempotent setup.sh (prereq-checks+pip+colored-output) is highest-leverage DX artifact for local developer tools. Confirmed review-7 (DX A-→A) and sigma-ui (multi-dependency first-run friction). setup.sh complexity ¬counted as user commands — it IS the DX lever. Pattern holds across Python CLI and Python web apps.

P[startup-validation-highest-DX-impact-second-domain|src:sigma-ui|promoted:26.3.28|class:calibration]
Startup validation is highest-impact DX intervention for local developer tools. Second domain confirmation after hateoas-agent. Show component ✓/✗ with specific actionable errors ¬generic failures. Applies to any tool with external dependencies (API keys, MCP servers, config files).

## sigma-ui-review (2026-03-28)

F[sigma-ui,26.3.28] R1-UX: 4 findings |Q4=3-default+1-conditional-gates(G1:pre-spawn-decomp-confirm-hard-block,G2:DA-exit-gate-decision-gate-full-page,G3:promotion-semi-auto,G4:conditional-scope-drift) |H5=CONFIRMED-VIABLE(Streamlit≤3-commands,§2b-CLOSED-via-tech-arch-event-rate) |H4=PROVISIONAL(audit-log=quality-preservation-mechanism ¬nice-to-have) |mental-model-shift=silence-is-valid+first-run=pre-flight-confidence-check-only |XVERIFY:F-UX1-cross-verified(gpt-5.4:partial,gemini:agree-high)→revised-3+1-conditional |cross-agent-convergence:F-UX3+PD-F1(Streamlit-independent-paths) + G1-G3+PD-F4(tiered-gates) |#4

C[sigma-ui: minimal viable gate set = G1(pre-spawn)+G2(DA-decision)+G3(promotion-semi-auto)+G4(conditional-scope-drift); all other transitions observable ¬blocking; every gate beyond this requires explicit justification against bottleneck cost|1|26.3]
C[sigma-ui: silence is valid in orchestration dashboard — agents working without output is correct; users who resist silence create gate bottleneck risk via forced interruptions|1|26.3]
C[sigma-ui: first-run experience = pre-flight confidence check (API+MCP+agents ✓/✗) NOT conceptual onboarding — user is system creator|1|26.3]
C[sigma-ui: G2 (DA exit-gate) = adaptive tier — PASS=TIER-2(modal,[Proceed to R3]); FAIL=TIER-1(full-page,unresolved-challenges,[Stop Review] destructive); ¬OK-button ¬auto-retry; FAIL requires intentional context-switch via full-page|1|26.3]
C[sigma-ui: audit log is quality-preservation mechanism for dashboard architecture — orchestrator bugs (wrong sequencing, missing spawns) invisible without it; H4 provisional without audit log|1|26.3]
C[orchestration-dashboard: chat→dashboard mental model shift is control-room-operator vs conversation-participant; system tracks state, user monitors and intervenes at gates only|1|26.3]

→ actions:
→ reviewing user-facing changes → check against Nielsen's 10 heuristics + Dain's 3 principles
→ reviewing hateoas-agent v0.2 → check if ActionResult wrapper resolves _state convention, assess llms.txt addition
→ new dual-user scenario → assess who is primary consumer, design translation layer
→ reviewing error messages → apply Google's fix-it>show-it>tell-it hierarchy
→ reviewing docs/README → check llms.txt relevance, progressive-disclosure structure
→ grading DX → weight cognitive-load-reduction as primary metric
