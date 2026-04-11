# Standards-Based Review

Evaluation against defined standards, regulations, schemas, or checklists. The reviewer checks pass/fail against specific criteria — subjective judgment is minimal.

**Use for:** accessibility audits (WCAG), compliance checks (regulatory, policy), data validation (QA before sharing), SOX testing, SEO audits, schema validation, audit support.

---

## Accessibility Review (WCAG 2.1 AA)

### Critical Checks

| WCAG SC | Requirement | How to Check |
|---|---|---|
| 1.1.1 | Non-text content has alt text | Inspect images, icons, charts |
| 1.3.1 | Info and structure conveyed semantically | Check heading hierarchy, landmark regions |
| 1.4.3 | Color contrast ≥ 4.5:1 (normal), ≥ 3:1 (large) | Use contrast checker tool |
| 1.4.11 | Non-text contrast ≥ 3:1 (UI components) | Check buttons, inputs, icons |
| 2.1.1 | All functionality via keyboard | Tab through the entire flow |
| 2.4.3 | Logical focus order | Tab and verify sequence makes sense |
| 2.4.7 | Visible focus indicator | Tab and look for visible focus ring |
| 2.5.5 | Touch target ≥ 44x44 CSS pixels | Measure interactive elements |
| 3.3.1 | Error identification (describe the error) | Trigger validation, check messages |
| 3.3.2 | Labels or instructions for inputs | Check every form field has a label |
| 4.1.2 | Name, role, value for all UI components | Screen reader test or inspect ARIA |

### Testing Approach
1. Automated scan (catches ~30% of issues)
2. Keyboard-only navigation (Tab, Enter, Space, Escape, Arrow keys)
3. Screen reader testing (VoiceOver on Mac, NVDA on Windows)
4. Color contrast verification
5. Zoom to 200% — does layout break?
6. Check with high-contrast mode / dark mode

### Common Failures
- Insufficient color contrast (most common)
- Missing form labels
- No keyboard access to interactive elements
- Missing alt text on meaningful images
- Focus traps in modals/overlays
- Missing ARIA landmarks
- Auto-playing media without controls

---

## Data Validation (Pre-Delivery QA)

### Data Quality Checks
- [ ] **Source verification**: Correct tables/data sources for this question?
- [ ] **Freshness**: Data current enough? "As of" date noted?
- [ ] **Completeness**: No unexpected gaps in time series or segments?
- [ ] **Null handling**: Null rates checked, handling appropriate (excluded/imputed/flagged)?
- [ ] **Deduplication**: No double-counting from bad joins or duplicate records?
- [ ] **Filter verification**: WHERE clauses correct, no unintended exclusions?

### Calculation Checks
- [ ] **Aggregation logic**: GROUP BY includes all non-aggregated columns
- [ ] **Denominator correctness**: Rates/percentages use right denominator, non-zero
- [ ] **Date alignment**: Same period lengths compared, partial periods excluded or noted
- [ ] **Join correctness**: Appropriate join types, no many-to-many inflation
- [ ] **Metric definitions**: Match how stakeholders define them
- [ ] **Subtotals sum**: Parts add up to whole (or explanation of why not)

### Reasonableness Checks
- [ ] **Magnitude**: Numbers in plausible range (revenue not negative, percentages 0-100%)
- [ ] **Trend continuity**: No unexplained jumps or drops
- [ ] **Cross-reference**: Key numbers match other known sources
- [ ] **Edge cases**: Boundaries, empty segments, zero-activity periods

### Common Pitfalls
- **Join explosion**: Many-to-many join silently multiplies rows. Check row count before and after.
- **Survivorship bias**: Only analyzing entities that still exist, missing those that churned/failed.
- **Simpson's paradox**: Aggregated trend reverses when broken into subgroups.
- **Trailing vs. leading periods**: Comparing a complete quarter to an incomplete one.
- **Denominator mismatch**: Using different populations for numerator and denominator.

---

## Compliance Check Framework

### Assessment Structure
1. **Identify applicable regulations** — GDPR, CCPA, HIPAA, SOX, PCI-DSS, industry-specific
2. **Map requirements to the initiative** — what's required, what's recommended
3. **Assess current compliance posture** — met, not met, unknown
4. **Identify gaps and risks** — what needs to happen before proceeding
5. **Produce action items** — specific, assigned, with deadlines

### Output Format

| Regulation | Relevance | Key Requirements | Status |
|---|---|---|---|
| [Regulation] | [How it applies] | [What's required] | Met / Not Met / Unknown |

### Compliance Review Verdict Scale
- **Proceed**: All requirements met, no material risks
- **Proceed with conditions**: Requirements mostly met, specific actions needed before/during launch
- **Requires further review**: Material gaps or unknowns — escalate to qualified professional

**Important**: Compliance assessments are frameworks for analysis, not legal advice. Requirements change frequently — verify current requirements with authoritative sources.

---

## SEO Audit Framework

### Technical SEO
- Page load speed (Core Web Vitals: LCP, FID, CLS)
- Mobile responsiveness
- Crawlability (robots.txt, sitemap.xml)
- Canonical tags, redirect chains
- Structured data / schema markup

### On-Page SEO
- Title tags (unique, descriptive, under 60 chars)
- Meta descriptions (compelling, under 160 chars)
- Heading structure (H1 → H2 → H3 hierarchy)
- Internal linking structure
- Image optimization (alt text, compression, WebP)

### Content Quality
- Search intent alignment
- Content depth and originality
- Keyword coverage without stuffing
- Freshness and update frequency

---

## Standards-Based Review Severity Guide

| Level | Standards Review Meaning |
|---|---|
| 🔴 Blocker | Compliance failure — regulatory violation, WCAG Level A failure, data integrity error that produces wrong results |
| 🟡 Issue | Standards gap — WCAG AA failure, missing validation, incomplete audit trail |
| 🔵 Suggestion | Best practice gap — recommended but not required, optimization opportunity |
| ✅ Pass | Meets or exceeds the standard |

## Gotchas

- **Cite the specific standard.** "This isn't accessible" = opinion. "Fails WCAG 2.1 SC 1.4.3 — contrast 3.2:1, minimum 4.5:1" = standards review.
- **Automated tools catch ~30% of accessibility issues.** Manual testing is required.
- **Compliance ≠ security ≠ privacy.** A SOC 2 Type II report doesn't mean the product is secure — it means controls exist and were tested.
- **Data validation is not data analysis.** Validation checks if the analysis is CORRECT; it doesn't interpret what the data MEANS.

---

## Cross-Reference: Data Validation

The data validation checklist above overlaps with the data-analysis skill's `references/data-validation.md`. If you're doing a full data QA (not just a review checkpoint), load the data-analysis skill — it has deeper coverage including join explosion detection, survivorship bias checks, and Simpson's paradox warnings. This skill provides the review framework; data-analysis provides the full validation toolkit.
