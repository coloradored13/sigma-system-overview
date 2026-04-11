# /sprint-planning - Plan a Sprint

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Plan the next sprint. Scope work to capacity, set goals, and align the team on what to build.

## Usage

```
/sprint-planning [sprint duration (default: 1 week)]
```

## Workflow

### 1. Review the Previous Sprint

- What shipped?
- What carried over?
- What was cut?
- Velocity: how many points did the team complete?
- Blockers: what stood in the way?

### 2. Assess Capacity

Calculate team capacity:
- How many engineers on the team?
- Account for known absences (PTO, interviews, training, on-call)
- Estimate % of time available for planned feature work
- Common baseline: 60-70% capacity for planned features

### 3. Propose Priorities

Based on the roadmap and backlog:
- What are the highest-priority items?
- What are the dependencies?
- What is the right mix of work?

Ask the team:
- Do you agree these are the priorities?
- Any concerns about feasibility?
- Any blockers we need to address upfront?

### 4. Estimate and Scope

For each proposed item:
- Story points or t-shirt sizing
- Owner assignment
- Acceptance criteria clarity
- Dependencies identified

**Facilitation tips**:
- Come with estimates prepared. Do not ask the team to estimate 20 items in planning.
- Include buffer for unknowns. If capacity is 40 points, commit to 30-35.
- If everything is "highest priority," clarify what is truly must-have vs. nice-to-have.
- Break down large items. A 20-point story should become 3-4 smaller stories.

### 5. Define Sprint Goal(s)

Articulate 1-2 outcomes for the sprint:
- User-facing: "Onboarded 50% of signups to their first team"
- Technical: "Reduced API latency by 30%"
- Reliability: "Achieved 99.9% uptime"
- Goals should be outcomes, not outputs

### 6. Identify Risks and Blockers

- What dependencies outside the team could cause issues?
- What investigations or decisions do we need to make early?
- What is the contingency plan if something slips?

### 7. Finalize the Plan

**Sprint checklist**:
- Capacity allocated: ~70% features, ~20% tech debt, ~10% unplanned
- All items have owners
- All items have clear acceptance criteria
- Dependencies are identified and owned
- Risk mitigation plan exists
- Sprint goal is clear and inspiring

## Output Format

```
## Sprint Plan: [Sprint dates]

### Sprint Goal
[1-2 sentence outcome for the sprint]

### Capacity
- Team size: X engineers
- Available capacity: Y story points (after accounting for absences/overhead)
- Target allocation: 70% features, 20% tech debt, 10% buffer

### Committed Work
| Item | Points | Owner | Status |
|------|--------|-------|--------|
| [Feature/Story] | X | Name | Not started |
| [Feature/Story] | X | Name | Not started |

Total: X points

### Carry-Over from Previous Sprint
| Item | Status | Plan |
|------|--------|------|
| [Item] | In progress | Continue |
| [Item] | Blocked | [Resolution plan] |

### Risks and Blockers
- [Risk]: [Mitigation]
- [Blocker]: [Resolution plan]

### Success Metrics
- Sprint goal achievement: [measurement approach]
- Velocity: [target points]
- Quality: [any QA focus]
```

## Tips

- The sprint plan is a commitment, not a forecast. Be conservative.
- If the team consistently commits and delivers the same number of points, use that as a baseline.
- Build in buffer for unknowns. The first time a team estimates, they usually overcommit.
- Celebrate completed sprints. Hitting goals builds momentum.
- Learn from missed sprints. If you consistently miss, adjust estimates or reduce scope.