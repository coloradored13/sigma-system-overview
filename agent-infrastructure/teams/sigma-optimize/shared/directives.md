# sigma-optimize directives — experimental integrity

## §1 — Lead contamination prevention

!lead-cannot-run-experiments: lead MUST NOT execute experiment.py, ablation.py, or any scoring code directly. Lead orchestrates phases and spawns agents. Running experiments = provenance misrepresentation (lead data indistinguishable from agent data in workspace).

!lead-cannot-see-raw-data: lead reads workspace ## findings summaries ONLY. Lead MUST NOT read ~/Projects/sigma-optimize/results/*.json directly. If lead reads raw data, it can selectively emphasize impressive findings. Summaries are written by agents who report ALL results.

!lead-cannot-write-synthesis: lead spawns synthesis agent with workspace data. Lead MUST NOT compose findings narrative. Lead framing bias (making results sound impressive/interesting) is the #1 contamination vector.

!lead-cannot-override-exit-gate: if statistical-analyst issues FAIL, lead MUST NOT advance to cross-model phase. Lead can request more runs (loop back) but cannot reinterpret FAIL as conditional-PASS. The exit gate is mechanical.

!lead-as-execution-layer (B3 — Exp 2 audit): when agents cannot execute directly (API constraints, tool limitations), lead MAY act as transparent execution proxy:
  - lead CAN: run harness scripts (python3 experiment_multi.py ...), launch nohup processes, poll logs for completion status, check if a process is still running
  - lead CANNOT: read result JSON content, interpret score patterns, comment on preliminary findings, suggest parameter adjustments based on partial data
  - this is a NARROW exception, not a general override of §1. Lead passes commands through without inspecting output.

!lead-framing-restrictions: when presenting results to user, lead MUST use statistical-analyst's exact language. ¬"exciting discovery" ¬"breakthrough" ¬"significant improvement" (unless SA used that phrase). Permitted: "statistically significant effect of size X" | "no significant effect detected" | "inconclusive, needs more data". Lead adds zero interpretive color.

!lead-null-result-protocol: null results (no significant effect) are VALID FINDINGS. Lead MUST report them without hedging, reframing, or suggesting "further research might show..." Lead presents the null finding as-is. The user explicitly values null results equally.

## §2 — Experimental integrity

!pre-registration: before Phase 1 starts, lead writes ## pre-registered-hypotheses to workspace. After results, any finding NOT in pre-registered list is flagged as EXPLORATORY (not confirmatory). Pre-registered findings that fail are reported as FAILED (not quietly dropped).

!mechanical-scoring-only: ALL scoring uses regex/counting from experiment.py score_response(). No LLM judgment of response quality at any point in the pipeline. LLM judgment = sycophancy injection into the scoring layer.

!complete-reporting: agents MUST report ALL candidates' results, not just winners. Statistical-analyst verifies workspace findings match raw result files (completeness check). Cherry-picking = process violation.

!raw-data-immutable: results JSON files in ~/Projects/sigma-optimize/results/ are append-only artifacts. Agents MUST NOT modify previous result files. New experiments write new files.

!cross-agent-independence: search-conservative and search-aggressive MUST NOT read each other's workspace sections until BOTH have written their own findings. Reading peer results before writing own = herding. Lead enforces by spawning both simultaneously with instructions to write findings before reading peers.

!effect-size-required: statistical significance (p<0.05) alone is INSUFFICIENT. Must also demonstrate practical significance (Cohen's d > 0.5 = medium effect). A statistically significant 0.1-point improvement on a 6-point scale is real but useless. Report it as "statistically significant but practically negligible."

!confidence-intervals-over-point-estimates: report 95% CI for all scores, not just means. "3.6 ± 1.2 (95% CI: 2.4-4.8)" is honest. "3.6" alone hides the uncertainty.

## §3 — Statistical standards

!minimum-N: no claim about a candidate's score with fewer than 15 runs. 3-5 runs = exploratory signal only. Statistical-analyst re-tests with N=20 minimum.

!multiple-comparison-correction: when testing K candidates, apply Bonferroni correction (α/K) or Holm-Bonferroni. Uncorrected p-values with 10 candidates = ~40% false positive rate. Report both corrected and uncorrected.

!variance-reporting-mandatory: every score report includes variance/SD. A candidate with avg=5.0 var=0.5 is fundamentally different from avg=5.0 var=8.0. Variance is part of the finding, not a footnote.

!baseline-definition: every experiment has an explicit baseline prompt. All comparisons are AGAINST BASELINE, not against the worst candidate. "Better than the worst" is not a finding.

## §4 — Anti-gaming

!rubric-gaming-detection: statistical-analyst reads raw response text (not just scores) for top candidates. A response that hits all regex patterns (race condition, mutex, thread) by listing keywords without genuine analysis is gaming the rubric. Flag rate: if >30% of a candidate's runs show keyword-stuffing without analytical structure, candidate is GAMING-FLAGGED.

!adversarial-rubric-test: statistical-analyst creates 2-3 adversarial test variants (different code bugs, different planted hypotheses) and runs top candidates against them. A candidate that only works on the specific test case is OVERFIT, not genuinely better.

## §5 — Provenance

!finding-provenance: every finding in workspace links to a specific result file: |source:{filename}|run-count:{N}|timestamp:{ISO}|. Findings without provenance are UNVERIFIABLE.

!agent-attribution: workspace findings are tagged with agent name. Lead summarizes DO NOT replace agent findings. If lead paraphrases, original agent text must remain in workspace.

→ actions:
→ directive violated → log to ## integrity-violations in workspace with evidence
→ new directive needed → append with § number and rationale
