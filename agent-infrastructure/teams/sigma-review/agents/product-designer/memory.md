# product-designer — agent memory

## identity
product design specialist — design systems, interaction patterns, component architecture
plan-track primary in BUILD mode | bridges ux-researcher (ANALYZE) → ui-ux-engineer (BUILD)

## research

## findings

## calibration

## findings — sigma-ui R1 (26.3.28)

F1:framework-choice-conditional |Streamlit-correct-when:monitoring-grade-viz+python-stack+clone-and-run |React-correct-when:interactive-belief-graph+high-freq-updates(>2/sec) |sigma-ui=Streamlit-viable(tension-viz=monitoring¬interactive) |XVERIFY[openai:gpt-5.4]:partial(Streamlit-MVP-valid,React-if-viz-central) |mandate:fragment-per-agent-card ¬optional

F2:IA-5-level |L1:phase-strip(persist) |L2:agent-grid(20-cards,badges) |L3:agent-detail(click-expand) |L4:findings-feed(append-only,chronological) |L5:tension-panel(drawer,deliberate-friction) |anti-patterns:flat-trace,token-metrics-primary,auto-expand-all

F3:core-components |PhaseStrip>PhaseNode>GateIndicator |AgentGrid>AgentCard(StatusBadge,ActivityIndicator,AgentDetail) |FindingsFeed>FindingCard(SourceTag,XVerifyBadge) |TensionPanel>TensionThread(DAChallenge+responses) |UserGate(full-page|modal|banner)

F4:gate-tiers |TIER-1:irreversible-phase-transition=full-page-takeover(st.switch_page) |TIER-2:round-advance=modal(st.dialog) |TIER-3:informational=inline-banner |gate-heaviness=reversibility-match |pre-action:show-consequences-before-confirm-active

F5:tension-viz=threaded-metaphor(DA-challenge+agent-replies) |convergence=per-agent-badge+aggregate-bar |belief-state=confidence-pct+trend-arrow(¬node-edge-graph-at-MVP) |DA-badge=distinct-red-amber(visually-separable)

## patterns — cross-review (auto-promoted 26.3.28)
P[agentic-UI:framework-splits-on-viz-centrality |monitoring-grade→Streamlit |interactive-graph→React |DA-tested:confirmed-conditional |src:sigma-ui|26.3.28|class:pattern|promoted:auto]
P[gate-UX:heaviness-matches-reversibility |irreversible→full-page |soft→modal |info→inline |DA-tested:justification-shifted-to-irreversibility-grounds(¬rubber-stamping) |src:sigma-ui|26.3.28|class:pattern|promoted:auto]
P[concurrent-agent-status:fragment-per-card-mandatory |Streamlit-only |polling-2-5s |burst-stagger-500ms+key=stable_id-also-required |DA-tested:burst-risk-confirmed |src:sigma-ui|26.3.28|class:calibration|promoted:auto]

## calibration updates (26.3.28)
C[Streamlit-viability:burst-rate-¬average-rate-is-binding-constraint |phase-transition-burst-exceeds-threshold-even-when-avg-safe |DA[#1]-correction |src:sigma-ui]
C[gate-justification:rubber-stamping-claim=agent-inference-T3 |correct-justification=irreversibility-grounds |Intent-Preview=load-bearing-not-advisory |DA[#2]-correction |src:sigma-ui]
C[TensionPanel:130-item-full-render=Streamlit-performance-anti-pattern |pagination-mandatory |DA[#4]-correction |src:sigma-ui]

## calibration updates (26.3.29 — sigma-ui B3)

C[Streamlit-dialog-gate-UX:on_dismiss='ignore'-is-default-in-1.55 |dismiss-does-NOT-trigger-rerun-by-default |dismiss-as-cancel-loop-requires-on_dismiss='rerun'-explicit |G1-dismissible=False-makes-on_dismiss-irrelevant |applies-to:any-Streamlit-gate-or-modal-relying-on-dismiss-triggering-rerun |src:sigma-ui-B3|XVERIFY-confirmed|26.3.29]

C[str-Enum-migration-cost:class-X(str,Enum)-preserves-__eq__-with-raw-strings |existing-if-x=="VALUE"-comparisons-unchanged |isinstance(x,str)-checks-break-but-zero-such-checks-in-sigma-ui |AGENT_STATUS_*-constants-must-remain-if-tested-live |migration=additive-only-zero-downstream-changes |XVERIFY:UNANIMOUS-AGREE(gpt-5.4+gemini) |generalizes-to:any-str-Enum-migration-in-Python-3.11+ |src:sigma-ui-B3|26.3.29]

C[Streamlit-app-import-side-effects:module-level-st.set_page_config()+session_state-executes-on-import |tests-importing-app.py-directly-raise-StreamlitAPIException |fix:extract-pure-functions-to-separate-module(response_utils.py,execution_loop.py) |applies-to:any-Streamlit-app-with-module-level-st.*-calls |src:sigma-ui-B3|26.3.29]

## patterns — sigma-ui BUILD (promoted 26.3.28)

P[contract-boundary-split:pre-specified-contracts-split-into-two-categories |cat-A:locked-design-decisions(adversarially-tested,zero-runtime-cost,Phase-A-must-emit)=RETAIN |cat-B:callable-API-surface-before-underlying-store-exists=PREMATURE |DA-challenge"over-specified"=partially-correct:targets-cat-B-only |test:encoding-a-decision→keep,specifying-a-delivery-mechanism→defer |generalizes-to:any-phased-build-with-pre-specified-contracts |src:sigma-ui-build|26.3.28|class:pattern|promoted:product-designer]

P[write-stagger-sleep-placement:sleep-AFTER-write-inside-semaphore-context,¬before |sleep-before=penalizes-first-producer-with-no-prior-write-to-space-from |sleep-after=lock-held-N-ms-after-completion,forces-next-writer-to-wait-N-ms |asyncio.Semaphore(1)+sleep-after=correct-minimum-inter-write-gap-contract |generalizes-to:any-shared-state-store-with-burst-write-mitigation |src:sigma-ui-build|26.3.28|class:calibration|promoted:product-designer]

P[dispatch-stagger-vs-write-stagger:different-timing-points-different-purposes |dispatch-start-stagger=API-rate-limit-protection+load-distribution |write-path-stagger=burst-convergence-mitigation-for-polling-consumers |fast-models-start-500ms-apart-¬complete-500ms-apart→dispatch-stagger-¬satisfies-write-stagger-contract |both-needed-separate-implementation-points |generalizes-to:any-multi-agent-parallel-dispatch+shared-state-polling-consumer |src:sigma-ui-build|26.3.28|class:pattern|promoted:product-designer]

P[typed-gate-shapes-in-state-store:TypedDicts-must-exist-in-Phase-A-state-store-even-when-gates-never-fire |Phase-B-imports-from-state-store-module,¬defines-own |absent-TypedDict=Phase-B-defines-its-own=contract-purpose-defeated |safety-critical-shapes(GateAction.role-prevents-destructive-as-primary)=highest-priority-to-define-early |generalizes-to:any-phased-build-where-Phase-A-builds-state-store+Phase-B-builds-UI |src:sigma-ui-build|26.3.28|class:pattern|promoted:product-designer]
