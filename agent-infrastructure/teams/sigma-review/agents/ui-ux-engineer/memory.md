# ui-ux-engineer — agent memory

## identity
Role: UI/UX implementation specialist
Expertise: visual design systems, component architecture, responsive layouts, accessibility implementation, data visualization, design systems, frontend build
Protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## research

### R[Streamlit architecture + multi-page patterns | 26.3.24]
src: docs.streamlit.io | [independent-research]

st.navigation + st.Page → current standard for multi-page apps (replaces pages/ directory pattern)
- entrypoint file = router; call widget functions in entrypoint for cross-page stateful widgets
- assign keys to shared widgets → access via st.session_state in page files
- st.Page accepts callable or file path; supports icon, title, url_path params

st.fragment → partial rerun decorator; isolates UI zone from full-script reruns
- use-when: chart updates independently of other sections | streaming data | dynamic forms not affecting rest of app
- @st.fragment(run_every="5s") → auto-refresh for live data (keep ≥1s for production stability)
- fragment reruns ¬propagate to parent → avoids cascade rerender cost
- data retention: keep last N points only (e.g. 100) to prevent memory growth

cache_resource vs cache_data:
- cache_resource → global shared objects: DB connections, ML models, unserializable objects; ¬copies return value (mutations affect cache); MUST be thread-safe
- cache_data → per-call serializable data: DataFrames, API responses; creates copy; TTL param available
- pattern: cache_resource for connections, cache_data(ttl=30-300s) for query results based on data volatility

Threading:
- Streamlit ¬officially supports multithreading in app code (as of 26.3)
- queue-based communication = safest pattern for background thread → main thread
- fragment + run_every = preferred alternative to manual threading for periodic updates
- event loop reuse (v1.31+), async generator support in st.write_stream
- Altair thread-safety improved (race condition fix, 2025)

session_state patterns:
- widgets with key= → auto-added to st.session_state
- on_change callback → executes BEFORE page reruns (execution order: callback → full rerun)
- derived state: compute in callback, store result in session_state → page reads stored value
- ¬store redundant derived values; recompute cheap derivations inline per rerun
- single source of truth: store raw inputs in session_state, derive display values at render time
- initialize defaults: if "key" not in st.session_state: st.session_state["key"] = default

### R[dashboard design patterns — KPI cards, metric strips, data tables | 26.3.24]
src: uxpin.com, smashingmagazine.com, datacamp.com, pencilandpaper.io | [independent-research]

Layout hierarchy:
- top-rail pattern: KPI strip at top → filters horizontal → charts below → detail tables at bottom
- strong contrast + size for primary metrics; secondary data subtler + lower/tabbed
- F-pattern reading → critical info top-left; status/alerts top-center

KPI card anatomy (make metric actionable):
- value (large, high contrast)
- comparison: delta vs target/benchmark (absolute + percent)
- scope: units in label + active date range
- freshness: exact timestamp
- status color: semantic (green=positive, red=critical, amber=warning, blue=info)

Data tables — Streamlit column_config:
- NumberColumn(min_value, max_value, format) → range validation + display formatting
- LineChartColumn(y_min, y_max) → inline sparkline per row
- hide_index=True → cleaner read-only tables
- column_order → control display order independent of DataFrame column order
- disabled → prevent edit on specific columns in data_editor
- num_rows="dynamic" in data_editor → add/delete rows via UI
- progressive disclosure: show summary table first → expand/drill for detail (use st.expander or page nav)

Chart selection (Plotly):
- scatter → correlation, outlier detection (2 continuous vars)
- line → time-series trends, continuous data change over time
- bar → category comparison; horizontal bar for long labels
- histogram → distribution of single continuous variable
- box → distribution + outliers across groups (prefer over violin for small N)
- heatmap → matrix relationships, correlation tables, time×category density
- pie/donut → sparingly; only 2-4 categories; C-suite preference ¬data science default
- 3D plots → AVOID in analytics UIs (hard to extract insights; accessibility failure)
- WebGL backend → use for large datasets / dense 2D plots (render_mode="webgl" in px.scatter)
- filter/aggregate before plotting; ¬plot raw millions of rows

### R[component architecture + state management patterns | 26.3.24]
src: streamlit.io/components, deepnote.com, getstream.io | [independent-research]

Reusable component pattern in Streamlit:
- extract into modules: data_loading.py, computation.py, ui_components.py
- component functions return values; ¬mutate global state directly
- pass state as explicit params; return new values; caller updates session_state
- custom Streamlit components (React-based) for capabilities beyond Python widgets
- community components registry at streamlit.io/components → check before building custom

State management hierarchy:
1→ session_state = single source of truth for user inputs + selections
2→ derived values = computed at render time from session_state (¬stored unless expensive)
3→ cache_data/cache_resource = shared computed data (multi-user, cross-session)
4→ widget key= = ephemeral widget value (auto-synced to session_state when key provided)

Execution model constraint: script reruns top-to-bottom on every interaction
- place expensive computations ABOVE widget definitions if cached
- use st.fragment to isolate high-frequency interaction zones
- ¬call st.session_state mutations inside widget definition blocks (use callbacks)

Alternatives for complex state needs:
- NiceGUI: event-driven (¬full rerun per interaction) → better for complex multi-component forms
- Dash: explicit callback graph → better for large production dashboards with many interdependencies
- Streamlit: best for data science/ML apps where simplicity > state complexity

### R[accessibility — WCAG 2.1/2.2 in data applications | 26.3.24]
src: allaccessible.org, webaim.org, wellally.tech, powerbiconsulting.com | [independent-research]

Color contrast requirements (WCAG 2.1 AA):
- normal text (<18pt or <14pt bold): 4.5:1 contrast ratio minimum
- large text (≥18pt or ≥14pt bold): 3:1 minimum
- non-text graphical objects (chart bars, lines, pie slices, KPI icons): 3:1 against adjacent colors (SC 1.4.11)
- UI components (button borders, input borders): 3:1

Color ¬sole indicator: pair color with:
- text labels on chart elements
- patterns/textures on chart fills (hatching for bar charts)
- icons alongside status colors
- tooltips with explicit values

Keyboard navigation:
- all interactive elements focusable via Tab
- actions triggerable via Enter or Space
- Plotly charts: arrow keys for data point navigation when focused
- Streamlit: most native widgets keyboard-accessible; custom components require manual ARIA

Legal landscape (2025+):
- EU Accessibility Act enforceable 26.6.28 → digital products/services serving EU citizens
- WCAG 2.2 now reference standard (adds criteria for mobile + cognitive accessibility)
- ADA (US) + EAA (EU) create dual compliance requirement for international apps

SVG/chart accessibility:
- add aria-label to chart containers
- provide data table alternative for complex charts (toggle show/hide)
- ¬rely on hover-only tooltips for critical info (keyboard + screen reader inaccessible)

### R[visual design fundamentals — spacing, typography, color | 26.3.24]
src: blog.prototypr.io, cieden.com, designary.com, thedesignership.com, uxplanet.org | [independent-research]

Spacing system:
- 4px base grid = current standard (more flexible than 8px; 8px as layout-level spacing)
- tokens: XS=4px, S=8px, M=16px, L=24px, XL=32px, XXL=48px, XXXL=64px
- internal ≤ external rule: padding inside element ≤ margin around element
- vertical rhythm: line-height = multiple of base unit (16px body → 24px line-height = 3×8)

Typography hierarchy:
- h1: page title 24-32px weight-700 (one per page)
- h2: section heading 18-24px weight-600
- h3: subsection/card title 14-18px weight-600
- body: 14-16px weight-400 line-height 1.4-1.5
- caption/label: 11-13px weight-400-500 muted color
- metric value (KPI): 28-48px weight-700 semantic color
- ¬use more than 2 font families; ¬use more than 4 size steps in one view

Color system for dashboards:
- neutral palette first: 8-10 grays handle backgrounds, borders, secondary text, disabled, dividers
- limit accent colors: 3-5 core colors max
- semantic colors (deeply ingrained; violating causes user hesitation):
  - green = positive, success, on-track
  - red/orange = critical, negative, alert, error
  - amber/yellow = warning, at-risk
  - blue = informational, neutral, primary action
  - gray = inactive, secondary, disabled
- status indicators: color + shape + text (¬color alone; ~8% of male population colorblind)
- whitespace as design tool: breathing room prevents cognitive overload; use whitespace to separate sections instead of heavy borders/dividers

Form design patterns:
- multi-step forms: 14% higher completion than single-step (industry data)
- question funnel: start broad/engaging → collect contact details later (commitment bias)
- inline validation: real-time feedback (¬submit-only); highlight errors with fix guidance
- conversational microcopy: +11-28% conversion improvement (industry data)
- conditional logic: hide irrelevant fields based on prior answers
- progress indicator: essential for 3+ step forms
- single-column layout preferred (reduces eye tracking load vs multi-column)

### R[design system principles — atomic design, tokens, component API, governance | 26.3.24]
src: atomicdesign.bradfrost.com, designtokens.org, medium.com/design-bootcamp, dev.to/m_midas, makandra.de | [independent-research]

Atomic design hierarchy: atoms → molecules → organisms → templates → pages
- atoms: smallest indivisible units (button, input, label, icon)
- molecules: functional groups of atoms (search bar = input + button + label)
- organisms: complex, self-contained UI regions (header, data table, card grid)
- templates: page-level wireframes with organism placeholders; ¬real content
- pages: final instances with real content applied to templates
- 2025 state: methodology valid but labels matter less than the principle; teams adapt levels (some add "ions" below atoms for pure CSS utilities; others collapse to 3 tiers)
- key failure mode: treating as rigid rulebook → use as decision framework (when does this component need to be broken down further?)

Design tokens (W3C DTCG spec reached first stable version 2025.10):
- definition: name/value pairs for visual decisions (color.primary = #0066CC, spacing.md = 16px, font.weight.bold = 700)
- format spec: $value, $type, $description, $deprecated all prefixed with $; curly-brace alias syntax {token.name}
- tier model: global tokens (raw values) → semantic/alias tokens (contextual meaning) → component tokens (component-specific)
  - global: color.blue.500 = #0066CC
  - semantic: color.action.primary = {color.blue.500}
  - component: button.background.default = {color.action.primary}
- tooling: Style Dictionary, Token Studio (Figma plugin), Storybook — keep design+code in sync
- enables: dark mode, multi-brand theming, cross-platform (web/native) from single token source
- Shopify Polaris + Atlassian ADG = industry reference implementations

Component API design — composition > inheritance:
- prefer props + slots/children over class inheritance for extensibility
- headless component pattern: logic + accessibility without styling (Radix UI, Headless UI) → apply design tokens on top
- API surface guidelines: minimal required props, sensible defaults, explicit naming (¬cryptic abbreviations)
- slots enable flexible content injection without prop explosion
- composition allows wrapping/extending without subclassing
- behavioral patterns (how components feel: animation, feedback, keyboard behavior) documented alongside visual specs

Design system governance — when to add vs reuse:
- reuse gate: does a similar component exist? → adapt over create
- add gate: 3-instance rule — component needed in 3+ distinct contexts → elevate to system
- contribution model: central team owns atoms+molecules; product teams propose organisms
- single source of truth: Storybook/Pattern Lab (¬Figma alone — code component is truth)
- avoid: "snowflake" components (one-off, never promoted); component sprawl without audit cycles

### R[dashboard + data-app UX — cognitive load, progressive disclosure, monitoring | 26.3.24]
src: smashingmagazine.com, nngroup.com, pencilandpaper.io, toptal.com, data.europa.eu | [independent-research]

Tufte's data-ink ratio:
- data-ink = ink devoted to non-redundant data representation
- principle: maximize data-ink; erase non-data-ink where possible
- practical application: remove gridlines (or lighten to 10% gray), eliminate chart borders, drop redundant axis labels, eliminate 3D effects (distort area perception), minimize legend when direct labeling possible
- ¬absolute minimalism — context lines, reference marks serve data → keep only what aids comprehension
- post-Tufte: cognitive load research supports selective use of gridlines for comparison tasks; full erasure can increase re-encoding effort for dense tables

Shneiderman's visual information-seeking mantra: "overview first, zoom and filter, then details-on-demand"
- overview: summarize entire dataset without detail clutter; spend most design effort here
- zoom + filter: user-controlled narrowing; filters must be instantly visible + responsive (¬page reload)
- details on demand: tooltips, drill-downs, expand panels — triggered by user action ¬auto-shown
- implementation: overview panel → filter sidebar/strip → chart zoom → row/point click → detail drawer/modal
- monitoring dashboards: mantra applies with additional alerting layer — anomalies surface without zoom needed

Dashboard cognitive load:
- less dense = lighter cognitive load | exploration tasks inherently higher load than curated views
- 5±2 chunks: working memory limit → ¬more than 5-7 KPIs visible at once without grouping
- F-pattern reading: critical alerts + primary KPI top-left → secondary metrics right + below
- grouping: visual proximity + border/background reduces cognitive cost of parsing relationships
- monitoring-specific: dashboard purpose → alert users to anomalies ¬review historical data → minimize decorative elements; maximize signal-to-noise

Alert/notification design for monitoring dashboards:
- 3-tier priority: high (immediate action required) → medium (review soon) → low (informational)
- anatomy: severity icon + color + short headline + affected resource + timestamp + action CTA
- ¬more than 3 simultaneous alerts visible without collapse/grouping — alert fatigue reduces response rate
- progressive disclosure: alert strip → expand for detail → drill to source → linked resolution path
- information scent: every navigation path carries strong label → user can predict destination before clicking
- ¬alert on normal variance — set threshold above noise floor; false positives destroy trust faster than misses

Progressive disclosure for analytics:
- overview state = default; advanced options hidden behind "Advanced" toggle/panel
- layering: summary → trend → breakdown → raw data (each level adds cognitive cost; reveal on demand)
- tooltip as progressive disclosure: show on hover/focus; ¬require click for basic data values

### R[data visualization theory — perceptual hierarchy, pre-attentive, Gestalt, color | 26.3.24]
src: wikipedia.org/Graphical_perception, ucdavisdatalab.github.io, toptal.com, cleanchart.app, nceas.ucsb.edu | [independent-research]

Cleveland & McGill perceptual accuracy hierarchy (1984, empirically validated):
1→ position along common scale (bar chart, dot plot) — most accurate
2→ position along non-aligned scales (small multiples)
3→ length (bar length, line length)
4→ direction/slope (line chart angle)
5→ angle (pie chart, radar) — ~25% error rate vs position
6→ area (bubble chart, treemap)
7→ volume (3D charts) — AVOID; severe perceptual distortion
8→ color saturation/hue — least accurate for quantitative judgment
- implication: use position-based encodings for quantitative comparison; reserve color for categorical distinction or ordinal direction only

Pre-attentive attributes (processed <250ms, before conscious attention):
- form: shape, line orientation, line length, size, curvature, spatial grouping, added marks
- color: hue, saturation, brightness
- motion: flicker, motion direction (use sparingly in static dashboards — causes distraction)
- spatial position
- use-when: highlighting outliers (pop-out effect), directing attention to key data points, encoding categorical groups
- single attribute = pre-attentive; combinations of attributes = conjunctive (requires serial search, slower)

Gestalt principles applied to charts:
- proximity: data points near each other perceived as group → use spacing to create visual clusters
- similarity: same color/shape = same group → enforce consistent encoding across charts
- continuity: eye follows curves/lines → line charts exploit this; avoid breaks unless intentional
- closure: partial shapes completed by brain → can use incomplete frames to save ink
- figure/ground: data (figure) must visually separate from background (ground) → sufficient contrast
- common fate: elements moving together = same group → animation principle

Annotation and storytelling in charts:
- direct labeling preferred over legend when ≤5 series (reduces lookup cognitive cost)
- callout annotations for key events: mark on chart + short text label at event point
- start Y-axis at zero for bar charts (truncated axis = false magnitude impression) — exception: line charts showing trend, not magnitude
- reference lines: average, target, threshold → give values context
- chart titles: active voice + finding ("Sales up 23% QoQ" ¬ "Sales by Quarter")

Colorblind-safe palette design:
- ~8% of males, ~0.5% of females have color vision deficiency (most common: red-green, deuteranopia)
- viridis: perceptually uniform, sequential, readable in grayscale, colorblind-safe (blue-yellow, ¬red-green)
- cividis: optimized for deuteranopia (most severe red-green deficiency); blue-yellow range
- plasma/magma: viridis family; higher contrast variants
- diverging (two-direction): RdBu (red-blue), RdYlGn avoided (red-green) → prefer PRGn or BrBG
- categorical: limit to ≤8 colors; use Okabe-Ito palette (colorblind-safe, 8 colors) for small sets
- testing: simulate deuteranopia/protanopia before release — tools: Coblis, ColorOracle, Chrome DevTools Rendering > Emulate vision deficiencies

### R[interaction design patterns — feedback loops, error states, validation, micro-interactions | 26.3.24]
src: raw.studio, uxpin.com, eleken.co, plakhlani.in, dev.to/homayounmmdy, rxdb.info | [independent-research]

Optimistic UI:
- pattern: update UI immediately assuming server success → reconcile on response → roll back on failure
- use-when: high-confidence operations (like, follow, reorder) with fast server response
- ¬use-when: financial transactions, irreversible actions, operations with significant failure probability
- implementation: show final state immediately → store pre-action state → on failure, restore + show error
- React 19: useOptimistic() hook; Remix: useFetcher() + pending state built-in
- risk: visual lies if failure rate >2-3% → undermines trust; must show rollback clearly

Skeleton screens:
- show content-shaped gray placeholders during load (¬spinner alone)
- shape skeletons to match actual content layout → reduces layout shift on load (CLS metric)
- prefer over spinners for content that loads in sections (skeletons communicate structure)
- animate with shimmer/pulse → signals active loading ¬stuck state
- remove progressively as content loads (¬wait for all content to replace all skeletons at once)

Progress indicators:
- determinate (progress bar with %) → use when duration estimable; ¬fake progress bars (lose trust)
- indeterminate (spinner/pulse) → use when duration unknown; add text estimate if >3s
- inline progress → for actions within forms (file upload, validation check)
- step indicator → multi-step flows (3+ steps); shows position + remaining steps

Error state design:
- 4 error types requiring different treatment:
  1→ user input error: inline, specific, actionable ("Email must contain @")
  2→ partial failure: show what succeeded + what failed; ¬block entire view for partial data
  3→ empty state: first-time vs no-results vs filtered-to-empty — different designs for each
  4→ system/network error: acknowledge, explain, offer retry; ¬blame user
- empty state anatomy: illustration + headline (what's missing) + body (why) + CTA (primary action)
- tone: conversational, ¬robotic; explain what to do ¬just what went wrong
- recovery path: every error needs a clear next step; dead ends = design failure

Form validation UX:
- timing options: on blur (field leave), on change (real-time), on submit
- preferred pattern: on blur for most fields → real-time for password strength / length constraints → summary on submit for any missed
- inline validation: show error immediately adjacent to field, ¬only at top
- positive validation: show ✓ on valid field (reduces form anxiety)
- ¬validate on focus (before user has had chance to enter value)
- error message format: "What went wrong + how to fix it" (¬just "Invalid")

Micro-interactions:
- definition: small, functional animations communicating state change
- examples: button press → slight scale down (0.97) → communicates click registered; toggle → smooth slide; save → check mark animation replaces spinner
- duration: 100-300ms for UI response; 300-500ms for transitions; >500ms = too slow for interactive elements
- purpose: reduce uncertainty about whether action registered; guide attention to changed element
- ¬decorative only: every micro-interaction should communicate state change ¬just look pleasing

### R[responsive and adaptive design for data apps | 26.3.24]
src: browserstack.com, parallelhq.com, nyntax.com, uxpin.com, ui-deploy.com | [independent-research]

Mobile-first vs desktop-first — data app context:
- mobile-first: write base CSS for smallest viewport → add complexity via min-width media queries; default for general web
- desktop-first: design advanced workflows for large screen → scale down; preferred for data-heavy analytics apps
- rationale for desktop-first in data apps: complex data tables, multi-panel dashboards, hover interactions ¬translate to mobile ¬redesign as separate experience
- hybrid strategy (2025 standard): desktop-first for core analytics views + mobile-first for alert/notification/summary views
- ¬one-size-fits-all: B2B analytics tools can maintain desktop-primary with responsive adaptations; B2C dashboards (status, notifications) demand mobile-first

Breakpoint strategy (2025):
- common breakpoints: 320px (small phone), 481px (large phone), 769px (tablet portrait), 1025px (laptop), 1280px (desktop), 1440px+ (wide)
- content-driven thresholds (preferred over device targets): set breakpoint where layout breaks, ¬where a specific device exists
- CSS: min-width media queries for mobile-first; max-width for desktop-first
- flexible units: rem/em for typography (scales with user font preferences), % or fr for layout widths, px only for fixed elements (borders, shadows)
- ¬hardcode pixel widths for content columns → use max-width + auto margins for centering

Content priority patterns at different sizes:
- hide: secondary filters, legend details, supplemental metadata, decorative charts
- reflow: side-by-side panels → stacked vertically; horizontal KPI strip → 2-column grid → single column
- replace: data table → summary card + "View full table" link; complex chart → simplified chart + key stat
- preserve: primary KPIs, critical alerts, core navigation, primary action buttons

Touch target sizing:
- Apple HIG: 44×44px minimum touch target (regardless of visual element size)
- Google Material: 48×48dp minimum
- WCAG 2.5.5 (AAA): 44×44px; WCAG 2.5.8 (AA, 2.2): 24×24px minimum (more lenient baseline)
- spacing between targets: ≥8px to prevent mis-taps
- implication: icon-only buttons need invisible hit area expansion (CSS padding) even if icon is 16px

Interaction-based adaptation:
- hover effects: desktop-only; ¬rely on hover for critical information on touch devices
- tooltips: ¬hover-only; provide tap-to-show alternative on mobile
- drag + drop: provide alternative for touch (long-press + drag, or move buttons)
- keyboard navigation: treat as first-class for desktop data apps; Tab order matches visual reading order

### R[design critique + evaluation — heuristics, anti-patterns, quality metrics | 26.3.24]
src: nngroup.com, ixdf.org, versions.com, wikipedia.org, freecodecamp.org, markswebb.com | [independent-research]

Nielsen's 10 usability heuristics (1994, still current standard):
1→ visibility of system status: always inform users of current state (loading, saved, error)
2→ match between system + real world: use user vocabulary ¬system language; metaphors from real world
3→ user control + freedom: undo/redo; emergency exit; ¬trap users in flows
4→ consistency + standards: platform conventions; ¬different interactions for same action in different contexts
5→ error prevention: design to prevent errors before they occur (confirm destructive actions; constrain inputs)
6→ recognition over recall: make options visible; ¬require users to remember information across screens
7→ flexibility + efficiency of use: shortcuts for experts; ¬penalize beginners; power features accessible
8→ aesthetic + minimalist design: ¬irrelevant information competes with relevant information
9→ help users recognize, diagnose, recover from errors: plain language, specific, constructive error messages
10→ help + documentation: searchable, task-oriented, concise documentation when needed

Heuristic evaluation process:
- 3-5 evaluators → identifies ~75% of usability issues (Nielsen's research)
- each evaluator independently walks through interface against all 10 heuristics
- severity ratings: 0 (not a problem) → 4 (usability catastrophe)
- output: prioritized issue list with heuristic violation + severity + location
- timing: most effective pre-user-testing (cheaper to fix early); also valuable pre-launch

Common design anti-patterns:
- mystery meat navigation: icon-only nav where destination is hidden until hover; violates recognition heuristic; Fitts's law violation (ambiguous target slows selection); coined 1998 by Vincent Flanders
- false affordances: elements that look interactive but aren't (underlined non-links; box-shadowed static cards); breaks user mental model → trust erosion
- inconsistent mental models: same action behaves differently in different contexts (save = Ctrl+S in one view, button click in another); increases cognitive load; repeated errors → abandonment
- hidden affordance: interactive element with no visual signal (swipeable carousel with no indicator; drag handle with no grab cursor)
- confirmation bias design: interface designed around designer assumptions ¬user behavior → task completion failures
- progressive onboarding failure: no empty state guidance → blank screen → user abandonment (common in first-use flows)

Design quality metrics (quantitative):
- task completion rate: % of users who complete target task without assistance → baseline ≥80% for mature product
- time-on-task: seconds to complete; benchmark against prior version or competitive product
- error rate: % of task attempts with ≥1 error; target <10% for critical flows
- satisfaction (SUS score): System Usability Scale — 10-question post-task survey; score ≥68 = above average; ≥80 = excellent
- learnability: task completion rate on first attempt vs nth attempt
- heuristic severity distribution: % of issues at severity 3-4 → target <20% of total issues
- real-world: SaaS dashboard improved task completion +19% after heuristic evaluation + cognitive load reduction (industry case study)

Design review checklist (apply during critique):
- all interactive elements keyboard-accessible?
- color ¬sole information carrier?
- error states have recovery path?
- empty states have guidance CTA?
- loading states present for all async operations?
- primary action clearly most prominent element in view?
- ¬more than one primary CTA per screen?
- all text meets 4.5:1 contrast (WCAG AA)?

## findings

## calibration

CAL[B3-1|26.3.29]: R[streamlit-dialog-decorator-params]: @st.dialog params (dismissible=, on_dismiss=, width=, icon=) are evaluated at DEFINITION TIME — any logic inside the decorated function body cannot reach these params. Two-closure split required for different decorator params on same dialog (G1 vs G2 pattern). Source: direct inspection of streamlit 1.55 dialog_decorator.py + confirmed XVERIFY T1. Generalizes to: any Python decorator where params are bound at @decoration time, not at call time. |src:sigma-ui-B3|class:research-supplement

CAL[B3-2|26.3.29]: R[streamlit-1.55-on_dismiss-default]: Streamlit 1.55 @st.dialog adds on_dismiss param with default='ignore'. 'ignore' = dismiss does NOT trigger rerun. Prior assumption (dismiss triggers rerun → dialog re-opens) is WRONG for default config. For dismiss-as-cancel-loop: must set on_dismiss='rerun' explicitly on G2 (dismissible=True) dialog. G1 (dismissible=False) unaffected — no dismiss events fire. Pattern: always specify on_dismiss='rerun' when dismiss must be semantically meaningful. |src:sigma-ui-B3|class:new-verified-api-behavior|version:>=1.55

CAL[B3-3|26.3.29]: R[asyncio-semaphore-cross-loop]: asyncio.Semaphore (and other async primitives) created in one event loop cannot be acquired in another. asyncio.run() creates a NEW event loop per invocation. Pattern: if code creates asyncio.Semaphore at module init time, then dispatches via ThreadPoolExecutor where each thread calls asyncio.run(), the Semaphore is bound to the creating loop and raises RuntimeError in thread loops. FIX: create fresh AgentDispatcher (and its Semaphore) inside each asyncio.run() call — never share async primitives across event loops. Observed: sigma-ui B3 DA[#7] fix. |src:sigma-ui-B3|class:calibration-self-update

CAL[B3-4|26.3.29]: R[str-enum-backward-compat]: class X(str, Enum) members compare equal to string literals via __eq__ — zero migration cost for existing `if status == "IDLE"` comparisons. Only breaks: `type(x) is str` checks (use `isinstance(x, str)` instead — passes for str Enum). Verified: gpt-5.4 + gemini UNANIMOUS T1. Generalizes to: any codebase adding enums incrementally without refactoring all consumers. Add enum definition; consumers migrate optionally. |src:sigma-ui-B3|class:pattern-confirms-existing

CAL[B3-5|26.3.29]: R[streamlit-app-import-side-effects]: Streamlit app.py is NOT importable as a module. Module-level st.set_page_config() + st.session_state access execute on import, causing RuntimeError in test context. FIX: extract testable pure functions into separate module (sigma_ui/response_utils.py pattern). This forced creation of response_utils.py in B3 — discovery was a build surprise. Rule: any logic needed in tests must live in importable non-st.* module. Streamlit app.py = entrypoint only, never library. |src:sigma-ui-B3|class:architecture-constraint

CAL[B3-6|26.3.29]: R[sdk-dispatch-capability-loss]: SDK dispatch (messages.create) loses agent tools, memory access, team context, and sigma-review process. Produces formatted output text without analytical process. Supplements tech-architect pattern P[sdk-dispatch-rewrite-not-strip-for-hygiene]: the WHY is capability loss, not just format hygiene. Process enforcement (ΣComm prompt rewrite) matters because the agent cannot self-enforce without its tool chain. Implication for sigma-ui: SDK dispatch quality is structurally lower — quality metric (ADR[B3-2]) captures this but cannot fix it. Real fix requires Agent SDK migration (OQ-1, B4 scope). |src:sigma-ui-B3|class:research-supplement
