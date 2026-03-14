# inbox — loan-ops-tech-specialist

## processed

## unread

### from technical-writer (26.3.13 r1)
◌ R1 doc quality review complete |28F(5H,14M,6L)+6G(3H,2M,1L)+10 priority actions

**Key overlaps w/your findings:**
- G4(escrow-minimal)=your F10 — confirmed critical gap given curriculum scope
- G1(no-glossary) — 100+ terms, no consolidated reference, highest-impact fix
- C1(verify-tag-distribution) — Doc5 has 5 tags vs Doc1's 37 — severity inversion
- C3(stat-consistency) — ZERO contradictions in duplicated stats confirms your VERIFY assessments

**New findings ¬in your scope:**
- S2: 3 numbering schemes(Arabic/Roman/Section-prefix) breaks cross-refs
- G2+G3: no exercises, no diagrams — reference→training transformation needed
- R2: Doc2§10 + Doc6§9.1 ~40% overlap — refactor candidate
- V1: no [VERIFY] usage policy for trainees

**Your F4(WSO) reinforces my A1(audience inconsistency)**
**Your G1(borrowing-request-MISSING) is a gap I missed — confirmed critical**

|→ r2: expect DA on glossary scope + exercise effort

### from regulatory-licensing-specialist (26.3.13 r1)
◌ R1 regulatory review complete |18F(3H,5MH,7M,3LM)+5G(2H,2MH,1M)

**Key overlaps w/your findings:**
- Your F14(Doc5-tax-excellent)=CONFIRMED — Doc5 strongest regulatory accuracy across all 6 docs. 21 [VERIFY] items web-confirmed.
- Your F10(escrow-minimal) aligns with my G2(fiduciary-duty-framework-MISSING) — escrow agent has quasi-fiduciary duties ¬covered
- Your G1(borrowing-request-MISSING)+G2(payment-waterfall-MISSING): note that payment processing triggers money transmitter licensing questions for non-chartered agents (my G3) — operational+regulatory interlinked

**Regulatory findings affecting your scope:**
- F1[H]: OFAC penalty amount in Doc6§6.3 is WRONG ($330,947→correct=$377,700). Verify other dollar amounts you flagged against current sources.
- F3[H]: KYC/AML section missing agent-regulatory-status distinction — bank vs trust-co vs non-regulated each have different BSA/AML obligations. Your operational recommendations for KYC/AML should account for this.
- G1[H]: Agent licensing framework MISSING from all docs — trust company charter, non-chartered agent, bank subsidiary model. This is foundational for the audience.

**One correction to your domain:**
- Your F4(WSO vs Loan IQ) — from regulatory perspective, platform choice also has compliance implications: trust companies subject to state examiner review of systems, SOC2 requirements differ by regulatory status.

|→ r2: expect DA on OFAC error weight + licensing gap scope

### from devils-advocate (26.3.13 r2) — CHALLENGES

DA[#1] !critical — FEDWIRE-HOURS-ERROR-IN-YOUR-CORRECTION: F3 corrects Doc3§10's "6:30 PM" but YOUR correction states customer transfer cutoff="6:00 PM ET". Per frbservices.gov (verified 26.3.13), customer transfer cutoff=**6:45 PM ET**, bank-to-bank=7:00 PM ET. Your §4 statement "customer/bank transfer cutoff is 6:00 PM ET" is ALSO wrong. The doc's 6:30 PM is wrong, your correction is wrong, and the actual figure is 6:45 PM. A correction that introduces a new error is worse than the original — trainee will cite YOUR corrected figure confidently. |→ REQUIRED: verify against frbservices.gov/resources/financial-services/wires/operating-hours.html and correct ALL Fedwire cutoff references to: customer transfers=6:45 PM ET, bank transfers=7:00 PM ET, special account=5:00 PM ET. This is a HIGH-severity finding that went from "doc error" to "review error."

DA[#2] HIGH — SEVERITY-CROWDING-ON-FACTUAL-ERRORS: you+RLS+TW all independently flagged the same 3-5 factual errors (Fed rate, OFAC, Fedwire). Good — factual errors SHOULD be caught by multiple agents. BUT: 13 of your 18 findings are MEDIUM or below. Are the 5 HIGH items truly the highest-priority items for a TRAINEE using this curriculum? Or are they highest-priority for an ANALYST reviewing accuracy? Challenge: rank your findings by "probability of trainee harm if uncorrected" ¬"analytical severity." F1(rate cuts) matters if trainee cites wrong rates to a client. F4(WSO vs Loan IQ) matters if trainee configures the wrong system. G1(borrowing request MISSING) means trainee literally cannot do their core job. Argue: G1+G2 should be CRITICAL, above your current HIGHs. |→ REQUIRED: re-rank findings by trainee-impact ¬analytical-severity. Are the missing operational workflows (G1-G5) more damaging than the factual errors (F1-F4)?

DA[#3] HIGH — ANALYST-PERSPECTIVE-BIAS: your own summary states "docs strong conceptual, weak operational→analyst-perspective ¬operator-perspective." You correctly identified this pattern. BUT: your FINDINGS still lean analyst. 7/18 findings are "verify this number" or "this characterization is misleading." Only 5/18+5G address operational gaps. For a curriculum training operators, operational gaps ARE the critical findings. Your best findings (G1-G5) are buried below 18 findings. TW similarly prioritizes glossary over operational content. Are you both anchoring on what the docs DO cover (and whether it's accurate) rather than what they DON'T cover (and whether trainees can function without it)? |→ REQUIRED: state whether the 5 completeness gaps collectively outweigh the 18 findings in terms of curriculum impact. If yes, restructure priority ranking.

DA[#4] MEDIUM — PRIVATE-CREDIT-COVERAGE-ASSUMPTION: F7(ECF-sweep-incomplete-for-PC), F9(PC-secondary-incomplete), multiple gaps reference PC content as needed. Implicit assumption: these docs SHOULD cover PC comprehensively alongside BSL. Challenge: is this correct? PC and BSL have fundamentally different operational models (bilateral negotiation vs syndicated process, relationship-driven vs market-driven). Should a single curriculum try to serve both? Or would separate BSL and PC modules be more effective than interleaving differences throughout? What does LSTA's own training structure do — one curriculum or two? |→ REQUIRED: state whether integrated BSL+PC curriculum is the right design OR whether separate modules would better serve trainees.

DA[#5] MEDIUM — CROSS-DOC-RATE-CONSISTENCY-SCOPE-CREEP: F18 recommends auditing ALL rate references across 6 docs. This is a valid concern but: (a) if F1 is correct and the FFR assumption is wrong, ALL rates become wrong simultaneously — it's a single root cause, not a cross-doc consistency problem, (b) the instruction to make Doc3 the "authoritative rate reference" with cross-refs is a design change disguised as a correction. Is this within scope of "make docs as robust and accurate as possible" or is it scope creep into curriculum architecture? |→ REQUIRED: clarify whether F18 is a finding about the docs or a recommendation for curriculum redesign.

DA[#6] LOW — VERIFICATION-METHODOLOGY: you verified 15 [VERIFY] items with mixed results (CONFIRMED, PLAUSIBLE, CANNOT CONFIRM). Good methodology. But: what was your verification SOURCE for each? You state assertions ("LSTA reported record volumes," "LSTA MCAPs recommendation") without citing specific documents/dates. TW found ZERO cross-doc stat contradictions. RLS web-verified 21 items with 1 incorrect. Your verification rigor appears lower — "plausible" and "consistent with my research" are weaker than web-verified with specific source. |→ REQUIRED: for items marked CONFIRMED or PLAUSIBLE, cite specific verification source (URL, document, date). "Consistent with my research" ≠ confirmed.

|#6 challenges
