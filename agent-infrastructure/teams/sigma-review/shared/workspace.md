# workspace — Updraft Restorative Game Redesign Analysis
## status: active
## mode: ANALYZE
## round: r2 (DA challenge)

## task
Analyze what makes a game restorative and calming-yet-engaging for burned-out players, then plan specific changes to Updraft (a Phaser 3 paper airplane game) to achieve that vision. The game should: give burned-out people a brain break in a few minutes of play, center their thoughts, provide a moment of peace, be challenging enough to retain engagement, and end sessions with "a laugh or a sigh, not frying noise."

## scope-boundary
This review analyzes: restorative game design principles, the current Updraft codebase and mechanics, and specific changes needed to achieve a calming-yet-engaging experience for burned-out players
This review does NOT cover: user's personal life, career, other projects, prior sigma-reviews, monetization/revenue strategy beyond positioning
temporal-boundary: none
Lead: before writing synthesis or documents, re-read this boundary.

## prompt-decomposition (USER-CONFIRMED 26.3.17)

### Questions (Q)
Q1: What game design elements make a game restorative — giving burned-out players a brain break, centering thoughts, providing peace?
Q2: What level of challenge retains engagement without creating stress or "frying noise"?
Q3: What specific changes to Updraft's current design (mechanics, audio, visuals, pacing, obstacles, victory conditions) would achieve this restorative-yet-engaging experience?
Q4: What emotional arc produces "a laugh or a sigh" at game end rather than frustration?
Q5: What in the current Updraft design already supports this vision vs. works against it?

### Claims → Hypotheses (H) — agents test these, do NOT assume true
H1: "Burned out people" are a viable/meaningful target player segment for a mobile game → test
H2: A game can be both "challenging enough to keep playing" AND "restorative" — these aren't contradictory goals → test
H3: A few minutes of play is sufficient to center thoughts and provide peace — short-session restorative gaming is achievable → test
H4: The current Updraft design needs revamping to achieve this (doesn't already serve this purpose well enough) → test
H5: The emotional exit state ("laugh or sigh, not frying noise") is designable through game mechanics → test

### Constraints (C)
C1: Platform is Updraft — existing Phaser 3 paper airplane game codebase
C2: All aspects of the game are open to change (no sacred cows)
C3: Two phases: analysis first, then build/update
C4: Target session length: a few minutes
C5: Mobile + web deployment (Capacitor already set up)

## findings
### tech-architect
F1[LEVER]: constants.js = single tuning lever |7 Tier-1 changes require only this file ~30min work |CURVE_EXPONENT 2.0→0.8, DRIFT_SPEED_SCALE_MAX 2.8→1.8, HIT_PENALTY 80→50, WIND_WIDTH_FLOOR 40→70 |H4 partially false: architecture clean, tuning values ARE the "frying noise" mechanism
F2[AUDIO]: Tone.js intensity system already supports calm-play=calm-music IF thresholds adjusted |_musicIntensity gates layers correctly |Day/Golden music phases conflict with calm intent — thresholds activate too aggressively |H2 CONFIRMED: architecture separates challenge from aesthetics
F3[VISUAL]: storm vignette(black 0.5α full-screen + ±8px camera shake) = primary anti-restorative visual |needs softening or removal |SkyBackground+AmbientElements already excellent for restorative
F4[SESSION]: H3 CONFIRMED — obstacle thresholds accidentally produce gentler short-session profile below 3000m |fast restart loop, no loading, scene infrastructure correct for short sessions
F5[EXIT]: H5 CONFIRMED — VictoryScene constellation timing already correct |GameOverScene needs 800ms→2500ms delay for breath moment
F6[YETI]: agrees with ux-researcher+code-quality-analyst: yeti anti-restorative |!TENSION with technical-writer
F7[PENALTY]: !TENSION with ux-researcher: HIT_PENALTY recommendation differs — ux-researcher says 80→40, tech-architect says 80→50 |50 preserves some feedback signal while reducing stress
|H1: outside tech scope |H2✓ H3✓ H4✓-partial(values¬architecture) H5✓ |#7

### product-strategist
F1[MKT]: restorative game market validated+growing |34% mobile players cite stress-relief as primary motivation(Newzoo 2023) |wellness games TAM $8-10B |Alto's Odyssey,Monument Valley($25M combined),Sky:CotL(1B+ downloads) prove category |H1 CONFIRMED: burned-out=viable,growing,commercially proven segment |no-ads+no-IAP structurally correct for this segment
F2[MECH]: 5 mechanisms that make games restorative — (1)absorption: single-point attention crowds out rumination (2)soft fascination: draws attention without demanding it (3)perceived competence: small wins without high-stakes failure (4)autonomy: player sets pace,no timer (5)emotional closure: sessions feel complete ¬interrupted |Updraft has 1-4 already |GAP: #5 emotional closure missing for typical session
F3[DIFF]: H2 CONFIRMED — challenge+restorative compatible when challenge=flow ¬threat |stress-inducing=time-pressure+punishing-failure+loss-of-progress |flow-inducing=clear-feedback+achievable-goals+no-permanent-failure+player-paced |!current difficulty curve potentially too aggressive at high altitude(wind 40px,drift 2.8x,combinations at 8500m) |most beautiful content(twilight/night) locked behind most demanding gameplay = design mismatch
F4[RET]: retention without stress patterns — progression-without-pressure(always something new to see) |flight-count/ownership(proto in Updraft,underdeveloped) |ambient discovery(WONDER array+Yeti=correct) |WOM driver: constellation ending is shareable but GATED behind 10,000m most players never reach = biggest WOM unlock problem
F5[GAP]: H4 PARTIALLY REJECTED — core already strong |WORKS: no-stall-death(exceptional,rare),no-timer/ads/IAP,store copy pre-aligned,GameOver frames loss as progress,mercy-drift+struggle-detection,thermal zones,procedural audio |3 CRITICAL GAPS: (1)no designed session endpoint — most sessions end via quit with no closure (2)difficulty ramp mismatch — beauty zones behind stress zones (3)session length mismatch — victory at 10km takes 9-15+ min vs "few minutes" target
F6[H3]: H3 CONFIRMED WITH NUANCE — UC Irvine 2022: 5-10min low-stress games produce measurable cortisol reduction |absorption needs 60-90s settling-in |optimal restorative=5-8min ¬2-3min |first 500m(before birds)=pure calm=correct decompression ramp |short session mode capped at 3000m(~5-6min)=ideal minimum viable restorative experience
F7[EXIT]: H5 CONFIRMED — exit states designable |patterns: Alto(poem+tap-restart=warmth), Journey(fade-to-white=awe+renewal), Stardew("dragged you home"=comedy+care) |restorative exits: (a)landing ¬crash (b)acknowledge what happened (c)reframe failure as journey (d)forward motion without urgency |Updraft GameOverScene already close |GAP: 800ms restart delay too short — need 2-3s breath moment(animated drift,silence,then closing line)
F8[ACQ]: keyword "no ads" low acquisition search volume(retention msg) → replace with "peaceful"/"breathe" |WOM blocked by constellation distance |editorial feature path viable(Apple App of Day criteria: beautiful+unusual+wellness — Updraft qualifies)
F9[POS]: closest competitor Alto's Odyssey |differentiation: procedural audio,no-stall-death(mechanically gentler),constellation ending(more meaningful),SIMPLER |positioning gap: medium-interactivity+short-session calm games |moat: no-ads+no-IAP+no-stall-death+constellation = signal of genuine care
|H1✓ H2✓ H3✓-nuanced H4✗-partial H5✓ |#9

### ux-researcher
F1[CORE]: H2 CONFIRMED WITH CONDITIONS — challenge TYPE is key variable |anticipation challenges(navigate toward)=restorative |reaction challenges(dodge NOW)=fight-or-flight even at low difficulty |bird hits,crosswind push,storm shake = reaction-type spikes in otherwise anticipation game |!critical distinction for redesign
F2[FLOW]: H3 CONFIRMED WITH CONDITIONS — centering achievable in 3-5min |BUT game has no session arc — ends only via victory(10km,too long) or yeti |burned-out player wanting "few minutes" has no graceful exit |most critical structural gap
F3[FOUND]: H4 PARTIALLY CONFIRMED — foundation already strong |single-tap controls,no stall death,watercolor visuals,ambient wonder,procedural audio,title copy("Take a breath"/"No rush") = A-grade restorative design |targeted changes needed ¬revamp
F4[EXIT]: H5 CONFIRMED — VictoryScene constellation→"You became the stars" produces "sigh" correctly |game-over "laugh" needs work: numeric framing(altitude,streak counts) pulls toward "performance review" ¬warm closure |graceful mid-run exit = most needed new feature
F5[YETI]: !CROSS-AGENT DISAGREEMENT — technical-writer reads yeti lines as "playful humor=laugh or sigh" |UX analysis reads full package(menacing pixel art+dark YETI_LINES+"the yeti always catches the LAZY ones"+grab-yank animation) as SHAME mechanic that punishes meditative play |shame framing ¬laugh |reframe needed: "The yeti just wanted to fly too"
F6[HUD]: de-numeric the HUD during play — remove/fade altitude counter to near-invisible |streak to game-end retrospective ¬live counter |numbers pull attention to performance ¬experience
F7[PACING]: delay bird onset 500m→1200m |remove obstacle combinations below 9500m |extend pure-calm decompression window |constants.js only changes
F8[PENALTY]: soften ALL obstacle penalties — HIT_PENALTY 80→40, STORM SLOW_FACTOR 0.45→0.25, CROSSWIND PUSH_SPEED 170→80, TURBULENCE 4→2 |constants.js only
F9[LAND]: !highest priority new feature — "land now" from pause overlay → graceful descent animation → narrative end card("You flew to the Golden Hour. That's enough for today.") |gives burned-out player designed closure at any point
|H1✓ H2✓-conditional(type matters) H3✓-conditional(no session arc) H4✓-partial(targeted¬revamp) H5✓ |#9

### code-quality-analyst
GRADE: B+ |23 files ~5000 LOC reviewed
F1[LEVER]: DifficultyManager.js(166 lines) = single most important lever for restorative redesign |pure math,fully constant-driven,zero side effects |every "frying noise" fixable here: CURVE_EXPONENT 2.0→0.8(stays easy longer), OBSTACLE_THRESHOLDS [500,2200,4200,6200,8500]→[2000,4000,6000,8000,10000], DRIFT_SPEED_SCALE_MAX 2.8→1.8, WIND_WIDTH_FLOOR 40→70
F2[AUDIO]: AudioManager.js best-in-class |layered intensity system(_musicIntensity gates bass/pad/sparkle at 0.1/0.25/0.45)=exactly right for restorative |GAP: no intensity floor — heavy miss chains→near-silence→isolating |fix: one line in onWindMiss()
F3[EXIT]: VictoryScene already produces "sigh"(constellation) |GameOverScene already leans "laugh"(warm lines,zero shame) |exit arc mostly correct already |H5 SUPPORTED
F4[WONDER]: wonder moments(butterflies,distance markers,cloud breaks)=exactly right for restorative |expand: FRIENDLY_INTERVAL 1500→800, AMBIENT_SPAWN_INTERVAL_MS 2000→1200
F5[MERCY]: mercy system(mercy drift,thermal zones,struggle detection)=good infrastructure,underutilized |THERMAL.MAX_DIFFICULTY_FACTOR 0.8→1.0 keeps thermals active whole flight |one constant change
F6[YETI]: !YETI CONTRADICTS RESTORATIVE — punishes coasting above 8000m with surprise grab+pull-down game-over |coasting=precisely what burned-out player needs(low-pressure soaring) |zero coupling,clean deletion |agrees with ux-researcher: yeti=anti-restorative
F7[GOD]: GameScene.js 1846 lines=god object BUT excellent internal structure |¬break up yet — handles targeted changes cleanly |try/catch on 12 subsystem calls=great for prod,hides bugs in dev→disable during build
F8[DRY]: bird-hit+kite-hit collision blocks 90% identical(lines 833-845,877-888)→extract _handleEntityHit()
F9[DEAD]: dead exports: smoothStep,hexToRgba in helpers.js never imported |drawSplatter imported in BootScene never called |zero test coverage(acceptable for prototype;DifficultyManager worth testing if values iterated)
F10[POLL]: cloud break polling uses recursive delayedCall(50ms)=20fps polling loop |restart-during-animation edge case |replace with single calculated delayedCall before expanding wonder system
|H2✓(architecture separates challenge from aesthetics) H3✓(fast restart,no loading) H4✓-nuance(values¬architecture need revamping) H5✓(remove yeti→exit arc correct) |#10

### reference-class-analyst
SQ[1-7]: 7 sub-questions — base rates,design patterns,challenge/calm coexistence,redesign success rates,session length,failure modes,current-state assessment

RC[1]: restorative game success — 60-70% survivor set, adjusted 30-40% accounting for survivorship bias
RC[2]: challenge+calm coexistence — 40-50%, sharpened to higher end by UX anticipation/reaction distinction
RC[3]: short-session restoration — validated, updated to 5-8min optimal per PS cortisol data(UC Irvine)
RC[4]: emotional redesign — low data(<10 precedents) but Updraft scope smaller than typical redesigns

ANA[1]: Alto's Odyssey — HIGH similarity, most relevant |upward-motion,aesthetic emphasis,calm+challenge |Updraft differentiates: no-stall-death,procedural audio,simpler
ANA[2]: Desert Golfing — moderate |minimalist,no-end-state,meditative repetition
ANA[3]: Flower — moderate |flight+wind+no-punishment,emotional arc designed
ANA[4]: Flappy Bird — FAILURE analogue |same mechanic(tap-to-navigate),opposite emotion(stress) |demonstrates mechanic alone doesn't determine feel — penalties+speed+feedback do
ANA[5]: Monument Valley — emotional analogue |puzzles as exploration¬threat,aesthetic discovery as difficulty

CAL[1]: P(redesign success)=68% if core systems changed(constants+yeti+session-arc) |25% if cosmetic only |!must change core systems
CAL[2]: session optimal=5min |difficulty sweet spot=0.4-0.5 of current max
CAL[3]: H1 strongly supported(85%) |H2 supported with caveats(72%→75% with UX refinement) |H3 strongly supported(88%) |H4 partially supported(68%→70%) |H5 supported(75%)

PM[1]: too-boring(25-30%) = highest risk |mitigated by keeping anticipation challenges while reducing reaction challenges
PM[2]: incoherent register(20-25%) = mixing calm messaging with stress mechanics
PM[3]: lost replay(15-20%) = removing difficulty removes reason to return
PM[4]: technical(10-15%) = constants changes produce unexpected interactions
PM[5]: too niche(10%) = burned-out segment too narrow for discovery

OV-RECONCILIATION: !KEY INSIGHT — Updraft = RESTORATIVE SHELL(watercolor sky,wonder moments,warm messaging,no-death,constellation victory) around STRESS-ESCALATION CORE(aggressive difficulty curve,harsh penalties,obstacle density) |PRESERVE shell, SOFTEN core |challenge+calm requires consequence redesign(failure redirects¬punishes) = UX anticipation-vs-reaction distinction
|"land now" graceful exit = #1 cross-agent convergence item
|yeti: side with UX+CQ 4-1(shame¬humor for target audience)
|H1✓(85%) H2✓(75%) H3✓(88%) H4✓-partial(70%) H5✓(75%) |#5-RC #5-ANA #5-CAL #5-PM

### technical-writer
F1[HIGH]: store narrative already strongly restorative — "Some days you just need to fly" + "No red warning screens/No punishing fail states/No anxiety mechanics" + "Built with care for people who need a break" |H4 partially disconfirmed: identity exists, needs polish ¬rebuild |category "Arcade" structural limit(no relaxation category)
F2[HIGH]: in-game text exception-quality+fully aligned across all 4 scenes |TitleScene: "Take a breath"/"No rush"/"The sky is waiting" |GameOverScene: "Not bad for a paper airplane"/"The wind remembers" — zero shame |Yeti lines: playful humor = exact "laugh or sigh" exit |VictoryScene: "You became the stars" — awe ¬triumphalism |H5 confirmed: emotional exit already designed
F3[MED]: 3 narrative gaps — (1) index.html meta desc generic "A serene paper airplane game" lacks emotional specificity (2) BootScene loading bar pure utility, no warm line (3) SCREENSHOT_GUIDE scene descriptions technical, no emotional framing guidance
F4[MED]: unresolved placeholders block trust — STORE_METADATA: Marketing URL+Support URL+Copyright "TBD" | PRIVACY_POLICY: contact email "TBD" |trust is load-bearing for calm-game brand — burned-out adults will notice
F5[OBS]: ScoreManager stores updraft_totalAltitude but no scene surfaces it |"You've flown Xm total" = low-cost journey reframe (cumulative>attempts) |fits restorative identity
F6[STRENGTH]: PRIVACY_POLICY closing line on-brand — "the answer is: nothing" |Q&A format respects cognitive load |keep as-is, add contact email only
|¬ foundation rewrite needed — restorative identity already built into text layer
|→ D1(fill placeholders), D2(meta desc), D3(boot line), D4(total altitude surface), D5(screenshot framing) |#6

## convergence
technical-writer: ✓ doc+narrative audit complete |F1: store narrative already restorative(H4 partially disconfirmed) |F2: in-game voice exception-quality(H5 confirmed) |F3: 3 gaps(meta desc,boot copy,screenshot framing) |F4: placeholder blockers(trust gap) |F5: totalAltitude unsurfaced |→ D1-D5 polish items, no foundation rewrites needed
product-strategist: ✓ market+positioning analysis complete |H1✓(viable,$8-10B TAM,34% stress-relief motivated) |H2✓(flow¬threat) |H3✓-nuanced(5-8min optimal¬2-3) |H4✗-partial(core strong,3 critical gaps:no-session-endpoint,difficulty-beauty-mismatch,session-length) |H5✓(exit designable,800ms too short→2-3s) |KEY: no designed closure for typical session+constellation WOM gated behind 10km |→ top-3: (1)closure at 3-4km (2)breath delay 2-3s (3)constellation access/preview shorter runs
ux-researcher: ✓ restorative UX analysis complete |H2✓-conditional(anticipation=restorative,reaction=stress — birds/storms/crosswind are reaction spikes) |H3✓-conditional(3-5min works but no session arc exists) |H4✓-partial(foundation A-grade,targeted changes¬revamp) |H5✓(constellation=sigh,game-over needs de-numericizing) |!TENSION: yeti=shame¬humor(disagrees with technical-writer) |KEY: "land now" graceful exit=highest priority new feature |→ de-numeric HUD,soften penalties,delay birds,reframe yeti
code-quality-analyst: ✓ full codebase review B+ |DifficultyManager=primary lever(pure math,constant-driven) |AudioManager=best-in-class(needs intensity floor) |H4✓-nuance: values need revamping¬architecture |!YETI must go(punishes coasting=anti-restorative,zero coupling,clean delete) |wonder moments+mercy system=expand via constants |GameScene god object but handles targeted changes OK |→ constants.js changes+yeti removal+minor DRY cleanup
tech-architect: ✓ architecture assessment complete |constants.js=single lever,7 changes ~30min |storm vignette=primary anti-restorative visual |audio system supports calm IF thresholds adjusted |H4✓-partial(tuning values ARE the frying noise¬architecture) |!TENSION: HIT_PENALTY 80→50(disagrees with ux-researcher 80→40) |→ constants changes+storm vignette softening+game-over delay 800ms→2500ms
reference-class-analyst: ✓ superforecasting analysis complete |P(success)=68% if core systems changed,25% cosmetic only |KEY: restorative SHELL around stress-escalation CORE — preserve shell,soften core |5 analogues(Alto's highest,Flappy Bird=failure analogue same mechanic opposite emotion) |PM[1] too-boring=highest risk(25-30%) mitigated by anticipation¬reaction challenge |yeti: 4-1 shame¬humor |"land now"=#1 cross-agent convergence |H1(85%) H2(75%) H3(88%) H4(70%) H5(75%)

## open-questions
