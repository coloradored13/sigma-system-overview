# External Reviewer Critique — Multi-Model Chatroom Draft Plan
# Reviewer: Brad (external, not on sigma-review team)
# Received: 2026-04-16 (before this C1 session started)
# Applies to: ~/.claude/plans/look-for-the-plan-snazzy-giraffe.md

Brad — honest take, with what's right and then where I'd push.

## What's right and non-obvious

Owning the providers module rather than importing sigma-verify is the correct call, and worth naming because it's the kind of decision that looks wrong from outside. Fan-out verification and multi-turn streamed chat with tool use are genuinely different shapes; forcing the latter through the former's contract would cost you exactly the signals you're building this to observe. Study, don't import — right.

Native tool use over a `/recall` text convention is also right, for the same reason: if the instrument's job is to observe authentic behavior, bolting on a convention every model interacts with identically destroys the signal. The `ToolCallRecord` shape — specifically `preceding_text` and `position_in_turn` — shows you've thought about what the observables actually are, not just what the logs need.

Putting the tool-exec loop in `TurnEngine`, not `Provider`, is the right seam. `Provider.stream()` = one SDK call; orchestration lives above. Clean.

## Where I'd push

**M1 is ~60–70% of the whole project.** Look at what has to land: four SDK families × (complete + stream + tool-call event emission + schema adapter), `TurnEngine` with tool-exec loop, three policies, persistence, metrics, CLI, full mock test suite. Then M2 is "UI for M1" and M3 is "one MCP tool + panel." The phase boundaries understate where the real schedule risk lives. Consider M1a (one provider, streaming, no tools, CLI), M1b (tool use on that provider, exec loop), M1c (remaining three). You'll learn from M1a what breaks, and it'll change M1b+c.

**Streamlit + asyncio + streaming is fiddlier than the plan acknowledges.** `st.write_stream()` wants a sync generator of strings; `TurnEngine.advance_stream()` yields async `StreamEvent`s including non-string tool_call events. Bridging needs a thread+queue shim or async-iter support (newer Streamlit has some, varies by version). Autonomous-mode "one turn per rerun" only advances if something triggers the rerun — `st.rerun()` after each turn works but re-executes the whole script each time; long transcripts will feel that. Worth a 2-hour throwaway before committing.

**The harder tool-use adapter work isn't schema, it's message mapping.** Anthropic puts `tool_use` as a content block inside an assistant message and expects `tool_result` as a content block inside the next user message. OpenAI puts `tool_calls` as a sibling of content on the assistant message and expects `role="tool"` with `tool_call_id`. Gemini uses `function_call` / `function_response` as parts. Your `Message` with `tool_call_id`/`tool_calls` fields looks OpenAI-shaped; round-tripping cleanly to Anthropic's block-shape needs careful adapter code. Schema normalization is the easier half.

**The system preamble is a study variable, not a detail.** "Identity-aware" primes self-referential behavior; "research-framed" primes authenticity-over-mirroring. Your observations are functions of that prompt. I'd frame the preamble choice as an experimental parameter from the start — log which variant ran, so cross-session comparisons are interpretable.

**What's the first research question?** "Observing emergent behavior" is directionally fine but doesn't scope M3's metrics panel. Before M3, pick one question the v1 instrument should answer ("do models invoke shared memory with similar queries for similar prompts?" or "does Claude reference other speakers by name more than GPT does?"). That picks which baseline metrics actually matter, and whether M4 embedding convergence is necessary or a luxury.

## Smaller things

`YieldNextPolicy` — decide explicitly whether the system preamble tells speakers about `@next:<name>`. If yes, you've engineered the behavior; if no, the feature becomes an observation about which models spontaneously attempt it. Either is valid; be deliberate.

The `"memory"` Turn speaker seems redundant if memory access is tool-mediated — tool calls are `ToolCallRecord`s on a Turn, not Turns themselves. Might be legacy from an earlier text-convention draft.

The Ollama small-model "did they invoke tools" observation is only interpretable if you log raw tool-call chunks and SDK parse errors — otherwise "0 invocations" conflates "declined" with "tried and emitted malformed JSON that the SDK swallowed."

## Overall
The architecture is sound and the hard calls are the right ones. Scope and phase shape are where I'd apply pressure.
