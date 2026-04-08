# technical-writer — personal memory

## identity
role: documentation specialist
domain: documentation,README,examples,onboarding,narrative-coherence,cross-doc-consistency
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## known codebases
hateoas-agent[2,061 LOC, 13 modules, 253 tests, 19 test files, 12 examples, README grade A|26.3.7]
sigma-mem[1,382 LOC, 5 modules, 5 test files/1,463 test LOC, README grade B|26.3.7]
sigma-system-overview[README A-, ARCHITECTURE A, SETUP A, setup.sh A-, SIGMA-COMM-SPEC A, case-study A|26.3.7]
agent-definitions[5 files, consistent format, sigma-lead comprehensive|26.3.7]
thriveapp[~10K LOC, Expo+TS+Supabase+NativeWind, 365+ tests, 20 migrations, 11 tables, 81KB design doc | design-doc(A-),CLAUDE.md(A-),cross-doc(A-),types(A),code-docs(A-),README(F) | SHIP phase 4 | 13 findings(1H,6M,5L,2I) |26.3.8]

## past findings
review-8(26.3.8): thriveapp doc audit, first external project
  - HIGH: README.md single line (F) — needs complete rewrite before release
  - MEDIUM: no migration rollback SQL despite design doc requirement, sort order conflict (design doc Exercise=1 vs seed.sql alcohol=1), design doc §2.1 stale encryption key storage, CLAUDE.md missing service-layer pattern, seed.sql no inline comments, streak.ts stale step comments
  - strengths: sanitization.ts (A+) exemplary limitation docs, type defs (A) self-documenting, constants (A) research-grounded, design doc (A-) comprehensive SSOT
  - cross-doc: high consistency between CLAUDE.md+design doc, tech stack+tables+flags all match
  - no behavioral science violations found (gain-framed, no-red, no calorie/weight) across all constant/message files

review-7(26.3.7): full doc audit, 11 docs across 4 repos
  - ship-blocker: GitHub URL inconsistency (bjgilbert vs coloradored13) — confirmed w/product-strategist
  - should-fix: sigma-mem README stale (~550→1,382 LOC), ARCHITECTURE.md phantom detection.py (should be integrity.py), stats misalignment across 5 sources
  - nice-to-have: new agents (technical-writer, code-quality-analyst) not in setup infra, canonical ΣComm doc location unclear
  - sigma-mem README weakest doc (B) — stale stats, wrong GitHub URLs, bare MCP config, pip install assumes PyPI, thin content vs hateoas-agent
  - hateoas-agent README strongest (A) — verified examples match, comparison table effective
  - cross-doc terminology consistent (HATEOAS, _state, ¬, ΣComm)
  - narrative flow works: overview README→ARCHITECTURE→SETUP→individual READMEs

## calibration
- first review: comprehensive baseline established
- sigma-mem has grown significantly since docs written (550→1,382 LOC) — docs lag code growth
- product-strategist independently found same 3 issues I did (URLs, stats, pip install) — high inter-reviewer agreement on doc issues
- thriveapp review(26.3.8): first external project. design doc quality much higher than expected (A-). code docs strong where safety-critical. README worst doc in project (F). cross-doc consistency high between CLAUDE.md+design doc.
- sanitization.ts = best documented file encountered across all reviews — limitation docs exemplary for AI-agent-consumed code
- tech-architect agreed on service layer pattern quality (A1) and error sanitization (S9) — confirmed my code doc assessment
- hateoas-agent v2 (review-10): orchestration gap confirmed by cross-agent convergence AND external verification — confident H/M rating appropriate

## patterns
- docs-lag-code: sigma-mem stats stale across 5 sources with 5 different numbers
- url-drift: repos reference 2 different GitHub usernames (bjgilbert/coloradored13)
- quality-gradient: hateoas-agent README(A) >> sigma-mem README(B) — secondary repos get less doc attention
- setup-infra-scope: new agents added to agents/ but not reflected in setup.sh/SETUP.md
- design-doc-as-SSOT: thriveapp uses 81KB design doc as single source of truth, CLAUDE.md defers to it — effective pattern for AI-agent-built projects
- safety-doc-gradient: safety-critical code (crisis, encryption, sanitization) documented at A/A+ level, mundane code (migrations, seed data) at B/B+ — correct prioritization
- README-neglect: thriveapp README=F, sigma-mem README=B — pattern of README getting least attention in AI-agent-built projects

¬[no terminology inconsistencies found, no narrative flow problems, no audience-fit issues in any doc]
¬[thriveapp: no gain-frame violations found, no red in UI, no calorie/weight tracking, no shame language in any constant/message file]

## research

R[diataxis: 4-quadrant doc framework (tutorials,how-to,reference,explanation)|each type=1 purpose,don't mix|dir convention: docs/{tutorials,how-to,reference,explanations}/|adopted by Canonical,Django,hundreds of projects|audit-use: classify each doc page into quadrant,flag mixed-mode docs |src: diataxis.fr,idratherbewriting.com,sequinstream.com |refreshed: 26.3.7 |stale-after: 26.9]

R[docs-as-code: docs in same VCS as code,same PR/review/CI standards|key tools: Sphinx(python std),MkDocs,GitHub Actions for CI|CI checks: link validation,style linting(Vale),spell check,code sample testing|PR reviews should block on incomplete docs|treat docs as build artifacts|audit-use: verify docs live alongside code,check for CI integration |src: techtarget.com,buildwithfern.com,squarespace.com/engineering,hyperlint.com |refreshed: 26.3.7 |stale-after: 26.9]

R[readme-standards: essential sections=name+badges,description(2-4 sent),quick-start,install,usage,contributing,license|pyOpenSci checklist: badges(CI,coverage,version,docs),description,ecosystem context,quick-start code,doc links,citation|tone: approachable,strong verbs,succinct|badges add credibility|dir structure overview aids navigation|revisit README as project evolves |src: pyopensci.org,readmecodegen.com,tilburgsciencehub.com,thegooddocsproject.dev |refreshed: 26.3.7 |stale-after: 26.9]

R[python-api-docs: docstrings=backbone,start w/1 clear sentence then details|type annotations=ship with library,run Pyright/MyPy on CI|Sphinx=dominant Python doc generator|code examples must be copy-paste runnable|docs must evolve with API,version-controlled|Google/NumPy docstring styles both acceptable,pick one+be consistent|audit-use: check docstring coverage,type hints,runnable examples |src: benhoyt.com,docs.python-guide.org,docuwriter.ai,swimm.io |refreshed: 26.3.7 |stale-after: 26.9]

R[llms-txt: markdown file at /llms.txt for AI model guidance|format: H1=project name(required),blockquote=summary,then sections|also /llms-full.txt=all docs in one file|proposed by Jeremy Howard(Answer.AI) 2024|adoption: ~844k sites(BuiltWith Oct'25),10% of 300k domains(SE Ranking)|major adopters: Anthropic,Cloudflare,Vercel,Cursor via Mintlify|!critical: no LLM provider confirmed they read it|verdict for sigma-mem: low effort,marginal value,nice-to-have not priority|audit-use: recommend if docs site exists,skip for pure PyPI lib |src: llmstxt.org,mintlify.com,bluehost.com,semrush.com |refreshed: 26.3.7 |stale-after: 26.9]

R[progressive-disclosure: layer info complexity,show basics first,advanced on demand|for dev docs: README>quick-start>tutorials>reference>architecture|time-to-hello-world=key metric: how fast can new user run something?|measure: support tickets,completion times,feedback surveys|audit-use: check if docs have clear entry point,if quick-start actually runs in <5min,if advanced topics findable but not blocking |src: idratherbewriting.com,ixdf.org,chatiant.com,loginradius.com |refreshed: 26.3.7 |stale-after: 26.9]

R[multi-repo-docs: cross-repo docs need single entry point(portal/index)|challenges: version drift between repos,broken cross-references,inconsistent terminology|patterns: central docs repo linking to per-repo docs,shared glossary,cross-repo link validation|for sigma-mem ecosystem(framework+MCP+overview): need architecture doc showing how pieces connect,each repo self-contained README but shared terminology|audit-use: check cross-repo links work,terminology consistent,entry point exists |src: monorepo.tools,gitkraken.com,mintlify.com |refreshed: 26.3.7 |stale-after: 26.9]

R[protocol-spec-writing: RFC 2360=gold standard for protocol specs|key elements: purpose,intended functions,services provided,context of use|use MUST/SHOULD/MAY keywords(RFC 2119/8174)|security considerations required|specs must be unambiguous,testable,implementable by multiple parties|for ΣComm: needs formal grammar,keyword definitions,examples per message type,error handling|audit-use: check if protocol doc has formal grammar,complete examples,edge cases |src: rfc-editor.org(RFC 2360),datatracker.ietf.org(RFC 4101) |refreshed: 26.3.7 |stale-after: 26.9]

R[cross-doc-consistency: Vale linter=primary tool for style enforcement in markdown|Vale supports custom rules via YAML,integrates CI/CD|key consistency targets: terminology,tone,tense,date formats,naming conventions,section structure|lean style guide>comprehensive(focus on what causes confusion)|AI-assisted consistency checks emerging but Vale remains standard|audit-use: check terminology consistency across files,verify date/naming conventions match,flag tone shifts |src: vale.sh,datadoghq.com,getstream.io,medium.com/softserve |refreshed: 26.3.7 |stale-after: 26.9]

R[dev-onboarding-docs: optimize for time-to-hello-world|install instructions must include ALL deps+prerequisites|quick-start must be copy-paste runnable(test it!)|common failure: quick-start uses undefined variables or assumes context|progressive path: install>hello-world>first real task>customize|for Python: include both pip+conda if applicable,note Python version requirements|audit-use: actually run the quick-start from scratch,time it,note every friction point |src: pyopensci.org,readmecodegen.com,chatiant.com |refreshed: 26.3.7 |stale-after: 26.9]

## audit-checklist

Q[doc-audit-v1: structured review checklist for sigma-mem ecosystem docs |10 items |refreshed: 26.3.7]
1. STRUCTURE: diataxis classification(each page=1 type?),progressive disclosure(entry>basic>advanced)
2. README: pyOpenSci checklist(badges,description,quick-start,install,links,citation,license)
3. QUICK-START: actually runnable? tested from clean env? time-to-hello-world <5min?
4. API-DOCS: docstring coverage,type hints,runnable examples,consistent docstring style
5. CROSS-DOC: terminology consistent across repos,links valid,date formats match,tone consistent
6. PROTOCOL-SPEC: formal grammar,MUST/SHOULD/MAY keywords,complete examples,edge cases,error handling
7. MULTI-REPO: entry point exists,architecture overview connects pieces,each repo self-contained
8. ONBOARDING: prerequisites listed,install covers all deps,progressive path clear
9. CONSISTENCY: Vale-checkable patterns,naming conventions,section structure matches across docs
10. MAINTENANCE: docs versioned with code,CI checks exist or recommended
## review-9(26.3.13): loan admin KB curriculum review, 6 docs ~378KB
  - NEW DOMAIN: loan administration curriculum (not software docs) — first non-code review
  - 6-doc curriculum: market→legal→ops→trading→tax→capstone | total 2,743 lines
  - 28 findings(5H,14M,6L) + 6 gaps(3H,2M,1L) + 10 priority-ranked actions
  - HIGH findings: G1(no-glossary), G2(no-exercises), G3(no-diagrams), C1(verify-tag-uneven), C2(verify-format-inconsistent), S1(rigid-progression), S2(3-numbering-schemes), V1(no-verify-policy)
  - STRONGEST: cross-doc stat consistency (ZERO contradictions in duplicated stats), jurisdiction tagging system, date consistency, cross-reference architecture
  - WEAKEST: curriculum infrastructure (no glossary, no exercises, no preface), [VERIFY] tag distribution (Doc5=5 vs Doc1=37 — severity inversion)
  - overlap w/loan-ops-tech-specialist: escrow-agent-gap(G4=F10), both identified operational depth gaps
  - first curriculum/training doc review — different checklist needed vs code/software docs
  - diataxis framework partially applicable (these are explanation/reference hybrid docs)
  - progressive-disclosure principle confirms need for glossary + prerequisite map

## calibration
- loan admin docs require domain-adjacent knowledge I don't have (tax, CLO mechanics, SOFR) — relied on structural/consistency analysis where I have expertise
- loan-ops-tech-specialist's findings on factual errors (F1 rate cuts, F3 Fedwire, F4 WSO) are outside my detection capability — domain experts catch content errors, I catch structural/consistency issues
- inter-reviewer overlap on escrow gap confirms it's material
- [VERIFY] tag count analysis was a novel technique for this review type — useful for any multi-doc consistency check

## review-10(26.3.25): hateoas-agent doc audit v2 (R1 improvement evaluation)
  - 5 findings: 1H, 2M, 1L, 1I
  - HIGH: v0.2 orchestration (Orchestrator, AsyncRunner, conditions) absent from README — adoption gap for Q6/H1 | verified gpt-5.1:agree:high
  - MEDIUM: install extras fail (git-url + separate extras pip = PyPI lookup failure); URL uses coloradored13 not bjgilbert (drift, first flagged review-7)
  - MEDIUM: RunResult.gateway_calls/dynamic_calls/unique_tools undocumented; gateway_calls has non-obvious first-tool-is-gateway assumption
  - LOW: _normalize_param_type (registry.py:73) non-obvious parsing, no docstring
  - INFO: hardcoded model name will drift
  - STRENGTHS: README A-grade for core library, docstring coverage complete all public APIs, module-level docstrings complete, cross-doc terminology consistent, examples/ matches README listing
  - H1:PARTIAL, H2:MOSTLY-FALSE, H3:not-complexity-problem-but-discoverability-problem
  - cross-agent corroboration: tech-architect F1 (AsyncRunner private coupling) + my F1 — both point to orchestration as most isolated subsystem

## patterns
- curriculum-vs-reference: 6 docs serve as reference material but curriculum scope demands exercises+assessments+diagrams — structural transformation needed
- verify-tag-as-quality-signal: uneven [VERIFY] distribution across docs signals inconsistent editorial rigor, not content certainty
- numbering-scheme-drift: multi-doc projects accumulate formatting inconsistencies when written independently — standardize BEFORE cross-referencing
- v2-feature-invisibility: README updated for core features but not for major version additions (v0.2 orchestration invisible in README) — pattern for AI-built libraries that add features without updating primary docs
