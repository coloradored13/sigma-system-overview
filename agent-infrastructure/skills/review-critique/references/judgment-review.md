# Judgment-Based Review

Evaluation requiring contextual judgment — weighing tradeoffs, assessing risk, making recommendations. No single checklist applies; the reviewer synthesizes multiple factors to reach a conclusion.

**Use for:** contract review, risk assessment, vendor evaluation, NDA triage, ticket triage, escalation assessment, performance reviews, due diligence, "should we do this" decisions.

---

## Risk Assessment Framework

### Risk Matrix

| | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| **High Likelihood** | Medium | High | Critical |
| **Medium Likelihood** | Low | Medium | High |
| **Low Likelihood** | Low | Low | Medium |

### Risk Categories
- **Operational**: Process failures, staffing gaps, system outages
- **Financial**: Budget overruns, vendor cost increases, revenue impact
- **Compliance**: Regulatory violations, audit findings, policy breaches
- **Strategic**: Market changes, competitive threats, technology shifts
- **Reputational**: Customer impact, public perception, partner relationships
- **Security**: Data breaches, access control failures, third-party vulnerabilities

### Risk Register Format
For each risk:
- **Description**: What could happen
- **Likelihood**: High / Medium / Low (with evidence for the rating)
- **Impact**: High / Medium / Low (quantify if possible)
- **Risk Level**: Derived from matrix
- **Mitigation**: Specific action to reduce likelihood or impact
- **Owner**: Who manages this risk
- **Status**: Open / Mitigated / Accepted / Closed

---

---

## Pre-Mortem Framework

A pre-mortem inverts the normal review. Instead of "is this good now?" it asks: **"It's 6 months from now and this failed. Why?"**

More specific and actionable than generic risk assessment because it forces narrative — you're not listing abstract risks, you're telling a plausible failure story.

### When to Use
- Before committing to a plan, roadmap, or architecture
- Before shipping code to production
- Before signing a contract or making a hire
- Before any decision that's expensive to reverse
- When someone says "what could go wrong" or "what am I missing"

### How to Run

**1. Set the scene.** "It's [6 months / 1 year / end of quarter]. This [plan/project/decision] has failed. Not a minor setback — a clear failure."

**2. Write the incident report.** For each plausible failure mode:
- **What happened:** The specific failure event
- **Why it happened:** Root cause — not "bad luck" but a structural vulnerability that existed from the start
- **Warning signs we missed:** What was visible now that we ignored or rationalized
- **Who was affected:** Stakeholders, users, team, business
- **What would have prevented it:** The action we could have taken today

**3. Focus on plausible, not possible.** "An asteroid hits the data center" is possible but useless. "The key engineer quits and nobody else understands the payment waterfall code" is plausible and actionable.

**4. Prioritize by reversibility × likelihood.** Failures that are both likely AND hard to reverse get the most attention.

### Pre-Mortem for Code (Honnibal Pattern)
When applied to code or architecture, look specifically for:
- **Implicit ordering dependencies** — code that works only because things happen to run in a certain order
- **Shared mutable state** — data that multiple components read/write without coordination
- **Coincidental correctness** — tests pass but for the wrong reason
- **Load-bearing defaults** — configuration that's never been changed because the default happens to work
- **Invisible invariants** — assumptions that aren't documented or enforced, just true by accident

For each: imagine a reasonable developer making a reasonable change 6 months from now. How does it break?

### Output Format
```
## Pre-Mortem: [what's being reviewed]

### Failure Mode 1: [name]
What happened: [specific failure event]
Root cause: [structural vulnerability]
Warning signs: [what we can see now]
Prevention: [action to take today]
Reversibility: [easy / moderate / hard to recover from]
Likelihood: [low / medium / high]

### Failure Mode 2: ...
```

---

## Contract Review Framework

### Red Flag Scan (Read First)
- Unlimited liability or uncapped indemnification
- Unilateral modification rights
- Auto-renewal with short opt-out windows
- Non-compete or exclusivity clauses
- Assignment restrictions that limit flexibility
- IP ownership clauses (who owns work product?)
- Governing law / jurisdiction in unfavorable venue
- Broad termination-for-convenience by one party only
- Data ownership and portability on termination

### Key Provisions to Evaluate
- **Term and termination**: Length, renewal mechanics, exit costs
- **Scope**: What's included, what's excluded, change order process
- **Pricing**: Fixed vs. variable, escalation provisions, most-favored-customer
- **SLAs and remedies**: Uptime commitments, credit mechanisms, cure periods
- **Liability**: Caps, carve-outs, indemnification scope
- **Confidentiality**: Scope, duration, permitted disclosures
- **Insurance**: Required coverage types and minimums
- **Representations and warranties**: What each party is asserting as true

### Contract Review Output
For each provision reviewed:
- **What it says** (plain-language summary)
- **Whether it's standard** (market-normal, borrower-favorable, or lender-favorable)
- **Risk if left unchanged** (what could go wrong)
- **Suggested edit** (if needed)

**Note:** For loan credit agreement review, load the `loan-agency` skill — it covers sacred rights, erroneous payment provisions, LME blockers, amendment mechanics, and LSTA/LMA documentation differences.

**Note:** Contract review provides analytical framework, not legal advice. Material provisions should be reviewed by qualified counsel.

---

## Vendor Evaluation Framework

### Evaluation Dimensions

| Dimension | Weight (adjust per context) | What to Assess |
|---|---|---|
| Capability fit | High | Does it solve the actual problem? Feature gaps? |
| Total cost of ownership | High | License + implementation + training + support + exit |
| Security & compliance | High | SOC 2, data residency, encryption, access controls |
| Vendor stability | Medium | Financial health, funding, customer count, churn |
| Integration | Medium | API quality, existing integrations, migration effort |
| Support quality | Medium | Response time, escalation path, documentation |
| Lock-in risk | Medium | Data portability, contract flexibility, switching cost |

### Decision Framework
- **Single vendor**: Score on all dimensions, compare against minimum thresholds
- **Vendor comparison**: Score both on same dimensions, weight by priority, present tradeoffs clearly
- **Renewal decision**: Add incumbent advantage (switching cost, institutional knowledge) as a factor

---

## Ticket Triage Framework

### Priority Assignment

| Priority | Criteria | Response Target |
|---|---|---|
| **P1 — Critical** | Service down, data loss, security breach, revenue-blocking for multiple users | Immediate (< 1 hour) |
| **P2 — High** | Major feature broken, significant user impact, workaround exists but painful | Same business day |
| **P3 — Medium** | Feature degraded, minor user impact, reasonable workaround exists | 1-2 business days |
| **P4 — Low** | Cosmetic, feature request, documentation gap, minor inconvenience | Next sprint / backlog |

### Triage Workflow
1. **Parse**: What is the customer actually experiencing? Separate symptoms from root cause.
2. **Categorize**: Bug, how-to, feature request, billing, account, integration, security, data, performance
3. **Prioritize**: Assign P1-P4 using the matrix above
4. **Check for duplicates**: Is this a known issue? Existing ticket?
5. **Route**: Which team or person handles this category?
6. **Respond**: Acknowledge receipt, set expectation, provide workaround if available

### Escalation Triggers
- Customer explicitly requests escalation
- Issue persists past SLA
- Multiple customers reporting the same issue
- Security or data integrity concern
- Executive or key account involved

---

## Performance Review Framework

### Self-Assessment Structure
For each accomplishment:
- **Situation**: Context and challenge
- **Contribution**: What you specifically did
- **Impact**: Measurable result

### Manager Review Structure
- **Strengths**: Specific behavioral examples, not adjectives ("Led the migration project through two scope changes while maintaining the original deadline" not "hardworking")
- **Development areas**: Specific, actionable, with support offered
- **Goals assessment**: Met / Exceeded / Missed with evidence
- **Overall trajectory**: Growing, meeting expectations, needs improvement

### Feedback Quality Checklist
- [ ] Every strength has a specific example
- [ ] Every development area has a specific example
- [ ] No surprises — issues were raised in real-time, not saved for review
- [ ] Goals are rated against the criteria set at the beginning of the period
- [ ] Compensation and development conversations are separated

---

## Judgment-Based Review Severity Guide

| Level | Judgment Review Meaning |
|---|---|
| 🔴 Blocker | Unacceptable risk — do not proceed without resolution. Material liability, regulatory exposure, critical vendor gap. |
| 🟡 Issue | Significant concern — proceed with mitigation. Negotiate this clause, address this risk, escalate this ticket. |
| 🔵 Suggestion | Worth considering — improves outcome but not blocking. Better terms available, alternative approach, nice-to-have. |
| ✅ Acceptable | Meets reasonable standards for the context. Standard terms, low risk, appropriate priority. |

## Gotchas

- **Separate fact from opinion.** "This contract has a broad indemnification clause" (fact) vs. "I wouldn't sign this" (opinion). Present both, label both.
- **Risk assessment requires evidence for ratings.** "High likelihood" without explanation is just anxiety. What data supports the rating?
- **Vendor evaluation is context-dependent.** The best vendor for a 10-person startup ≠ the best for a 1,000-person enterprise. Adjust weights accordingly.
- **Triage is a routing decision, not a resolution.** The goal is to get the right issue to the right person at the right priority, not to solve it during triage.
- **Performance reviews are about behavior, not character.** "You missed three deadlines in Q2" (behavior) not "You're unreliable" (character).
- **"Should we do this" questions need a framework, not just a yes/no.** What are the tradeoffs? What's the risk? What's the alternative? What would change your answer?
