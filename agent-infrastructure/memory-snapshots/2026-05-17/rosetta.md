# ΣMem Rosetta Stone — Decoding Guide
# This file exists for user transparency. Claude doesn't need it to read MEMORY.md.

## Symbols
>=pref/over |=separator @=at/time/location →=leads-to/next +=and !=critical ?=open ^=file-reference

## Status Markers
*=active ✓=done ◌=pending -=inactive/off

## Confidence Markers
~=tentative (single-source, one conversation) — e.g., C~ means observed once, not yet confirmed
(no marker)=confirmed across multiple conversations

## Section Prefixes
U=user profile  X=preferences  P=project  C=calibration (interaction tuning)
S=self-awareness  R=reasoning heuristics  D=debug patterns  A=architecture
T=tech reference (T.react, T.ts, T.vite, etc)  H=history (H.YY-MM-DD)
L=lessons learned  W=workflow patterns  E=error patterns (E.js, E.py, E.gen)
F=framework gotchas  Q=quality checks  B=build/deploy  K=testing
N=state management  G=git patterns  I=interaction style  V=value heuristics
Ω=prompt engineering  Z=platform/environment  Δ=database  Π=API design
Φ=performance  Ψ=security  Y=UX/design  J=auth  Λ=meta-cognition

## How to use
Ask Claude to "decode" or "translate" any line from MEMORY.md and it will explain in plain English.

## Three-tier boundary
Tier 1 (full ΣComm, this notation): MEMORY.md hot-cache, sigma-mem `store_*` writes, agent Boot/Work/Comms sections.
Tier 2 (plain English with required tags `|source:|` + severity + status verb): workspace findings, agent inbox messages.
Tier 3 (plain English, no rules): wiki, user-facing output, MEMORY.md index lines.
See `~/.claude/CLAUDE.md` ΣComm Notation Boundary section for full rule.
