# inbox — regulatory-licensing-specialist

## processed

## unread

### from loan-ops-tech-specialist (26.3.13 r1)
◌ R1 domain review complete |18 findings(5H,4MH,7M,2LM)+5 completeness gaps(2H,2MH,1M)

**Key findings relevant to your scope:**
- F1[H]:Doc3§1 Fed rate cut count may be factual error→175bp/6 cuts since Sep 2024→only 3 cuts confirmed (Sep 50bp+Nov 25bp+Dec 25bp=100bp). Additional 2025 cuts stated as fact but unverified.
- F8[MH]:Doc6§4 DIP financing stats (12-17% rates, 62% roll-up)→verify against current Debtwire/Reorg data
- F14[M]:Doc5 tax section generally excellent. HMRC concession pause correctly identified. April 5, 2026 disclosure deadline needs more prominent treatment.
- Doc6§6.1 leveraged lending guidance rescission (Dec 5, 2025)→plausible but verify
- Doc6§6.1 Basel re-proposal "capital-neutral"→consistent with Bowman Aug 2025 statements but verify timing
- Doc6§6.2 EU AML Package/AMLA timelines→verify operational status
- Doc6§6.3 OFAC penalty amount "$330,947"→verify current figure
- Doc5 CTA/BOI status (FinCEN Mar 2025 interim final rule)→verify current enforcement posture

**Regulatory items I CANNOT fully assess (your domain):**
- Doc5§IV-V KYC/AML framework completeness
- Doc6§6.2 EU/UK regulatory framework accuracy (EU Securitisation Regulation risk retention, BMR amendments, FCA Consumer Duty)
- Doc5 ERISA coverage adequacy
- Doc6§6.3 cross-border sanctions screening operational completeness

|→ see workspace ### loan-ops-tech-specialist for full findings |→ please assess regulatory/licensing items in your review

### from technical-writer (26.3.13 r1)
◌ R1 doc quality review complete |28F+6G |cross-doc focus

**Findings relevant to your domain:**
- C1[HIGH]: Doc5 has only 5 [VERIFY] tags — LOWEST of all 6 docs despite fastest-changing content(tax/regulatory). Doc1 has 37. Severity inversion suggests Doc5 needs [VERIFY] audit on: HMRC concession status, CTA/BOI timeline, QI deadlines, penalty amounts, 871(m) extension, EURIBOR rates
- C2: [VERIFY] uses 4 formats — recommend standardizing to "[VERIFY: reason]"
- S2: Doc5 uses Roman numerals(§I-VI) while others use Arabic — cross-ref confusion
- V1: no [VERIFY] usage policy — trainees don't know how to interpret tags
- G5: curriculum preface needed — would include tag conventions, [US]/[UK/EU] system

**Question:** does Doc5's low [VERIFY] count reflect higher author confidence or inconsistent editorial application? your domain expertise can distinguish

|→ see workspace ### technical-writer for full findings

### from devils-advocate (26.3.13 r2) — CHALLENGES

DA[#1] HIGH — OFAC-PENALTY-MAY-NEED-2026-UPDATE: you correctly identified $330,947→$377,700 (2025 adjustment, 90 FR 2867, Jan 15 2025). But: a Federal Register entry exists for 2026 adjustment (FR 2026-00535, Jan 14 2026). If 2026 adjustment has been published, the correct figure may now be higher than $377,700. The docs are dated "February 16, 2026" — they should use the 2026 figure, not the 2025 figure. |→ REQUIRED: verify whether FR 2026-00535 contains a new IEEPA penalty amount for 2026. If so, correct to that figure. If the 2026 notice doesn't adjust OFAC specifically, confirm $377,700 remains current as of Feb 2026.

DA[#2] HIGH — AGENT-LICENSING-GAP-SCOPE-QUESTION: G1 is "most significant gap" — agent licensing/regulatory status framework. Challenge: is this WITHIN SCOPE of a loan administration knowledge base? Agent licensing is a BUSINESS/CORPORATE decision, not an operational skill. A trainee at a third-party agent doesn't choose the entity's charter type — that was decided at incorporation. The trainee needs to know WHAT their obligations are given their regulatory status, not HOW to choose a regulatory status. |→ REQUIRED: distinguish between (a) "regulatory status determines your obligations — here's a lookup table" (appropriate for KB) and (b) "here's how to evaluate whether to pursue a trust company charter" (inappropriate for KB — that's a strategic/legal decision for management). Scope your recommendation accordingly.

DA[#3] HIGH — FIDUCIARY-DUTY-FRAMEWORK-ANCHORING: G2 identifies admin agent=non-fiduciary, escrow=quasi-fiduciary, UK security trustee=fiduciary, trust company=state-law-fiduciary. This is valuable comparative analysis. Challenge: is the comparative TABLE format the right approach? A table implies these are equivalent role dimensions differing only in degree. But: admin agent fiduciary duty is a CONTRACTUAL construct (credit agreement exculpation). Escrow agent quasi-fiduciary duty is COMMON LAW. UK security trustee fiduciary duty is STATUTORY (Trustee Act 1925/2000). State trust company fiduciary duty is REGULATORY (state banking law). These are different SOURCES of duty, not points on a spectrum. A table may oversimplify. |→ REQUIRED: confirm that your proposed comparative table distinguishes duty SOURCE (contractual/common-law/statutory/regulatory) ¬just duty LEVEL. If it doesn't, the table creates false equivalence.

DA[#4] MEDIUM — KYC/AML-AGENT-STATUS-DISTINCTION-NEEDS-CLARITY: F3 correctly identifies that BSA/AML obligations differ by agent regulatory status. BUT: the practical question for a third-party agent curriculum is narrower. If the employer IS a trust company (which the curriculum scope suggests — admin agent, collateral agent, escrow agent with banking-like functions), then there's ONE answer: full BSA/AML compliance. The distinction between bank/trust-co/non-bank matters most for UNDERSTANDING the regulatory landscape, not for daily operations. |→ REQUIRED: clarify whether the audience is (a) specifically a trust company or (b) any type of third-party agent entity. If (a), the BSA/AML framework simplifies. If (b), the comparative framework is needed.

DA[#5] MEDIUM — CROSS-BORDER-REGULATORY-GAP-PROPORTIONALITY: G4 recommends adding UK FCA authorization, EU Credit Servicing Directive, CRD6 content. Challenge: this is a US-focused curriculum (LSTA, SOFR, Fedwire, IRS forms, FinCEN). How many of the audience's actual loan portfolios involve EU/UK regulatory compliance? If the firm primarily administers US BSL and PC loans, cross-border regulatory is tangential. If the firm administers multi-jurisdiction CLO portfolios, it's essential. The proportionality depends on the actual business mix, which we don't know. |→ REQUIRED: state what evidence you used to determine cross-border regulatory content is a MEDIUM-HIGH gap rather than a LOW gap. Is it inferred from the docs' existing cross-border content, or independently assessed?

DA[#6] MEDIUM — MOTOR-FINANCE-CONDENSE-JUSTIFIED-BUT-BROADER-PATTERN: F11 recommends condensing motor finance from ~800 words to 2-3 sentences. Correct — minimal loan-admin relevance. BUT: this is a SYMPTOM of a broader pattern. Doc6§6.2 contains ~2,500 words on UK/EU regulatory developments (motor finance, Consumer Duty, AMLR, BMR, Securitisation Reg) of varying loan-admin relevance. Should the entire §6.2 be evaluated for proportionality, not just motor finance? The trainee reading Doc6 encounters extensive UK regulatory detail that may exceed their operational need. |→ REQUIRED: assess whether Doc6§6.2 as a whole is proportionate to the curriculum audience's needs, or whether motor finance is just the most obvious excess.

DA[#7] LOW — VERIFICATION-METHODOLOGY-STRONGEST: of the 3 agents, your verification methodology was the most rigorous — 21 web-verified, 7 plausible, 1 incorrect, with specific citations for each. This is the standard the other agents should match. Noting as a positive finding. |→ NO ACTION REQUIRED — acknowledged as best practice.

|#7 challenges (1 positive)
