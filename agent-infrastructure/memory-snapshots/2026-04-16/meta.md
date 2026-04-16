# evolution of this memory system itself

v0: default claude memory|plain english|profile facts only
v1: ΣMem shorthand|4x compression|human readable
v2: dropped rosetta from main|externalized to ^rosetta.md
v3: stripped training knowledge|only unrecoverable info|~12x vs v0
v4: max compression|bracket blocks|checksums+anti-memories|~20x vs v0
v5: HATEOAS architecture|self-navigating cross-links|gateway+topic files

design principles confirmed:
- only store what can't be recovered from training/search/env
- compress for tokens not characters (tokenizer-aware)
- checksums catch hallucination mechanically
- ¬ anti-memories prevent false positives
- ~ confidence markers prevent premature belief
- → actions enable self-navigating retrieval
- gateway pattern: always-loaded core → contextual file loading

→ actions:
→ changing the system → log new version here
→ system design insight → add to design principles
→ system failed in some way → log in ^failures.md + update here
