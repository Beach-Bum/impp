# IMPP Attach Modes — Formal Specification

This document defines the runtime semantics for each IMPP attach mode. An attach mode specifies HOW a memory artifact influences a consuming agent's behavior at runtime.

## Why Attach Modes Exist

"Installing a memory artifact" is ambiguous. Does the artifact become part of the system prompt? Does it get indexed for retrieval? Does it become a tool? The answer changes the artifact's impact on agent behavior, latency, cost, and risk profile.

Attach modes make this explicit. The publisher declares which modes are supported and recommended. The consumer chooses at install time.

## Mode Definitions

### `prepend_policy`

The artifact's knowledge content is prepended to the agent's system prompt on every invocation.

**Runtime behavior:**
- Full artifact content injected before user messages
- Persists across all interactions in the session
- Agent treats content as authoritative context

**When to use:** Small artifacts (under 4K tokens) with always-relevant knowledge.

**Risks:**
- Consumes context window on every call
- Content is always visible to the model, even when irrelevant
- Potential for instruction conflict with existing system prompts

**Cost model:** `O(artifact_tokens * invocations)` — linear token cost per call.

### `few_shot_examples`

Artifact sections are formatted as input/output demonstration pairs.

**Runtime behavior:**
- Publisher provides structured sections that map to example pairs
- Consumer specifies `max_examples` at attach time
- Examples are injected after the system prompt, before user messages

**When to use:** Calibration artifacts where the goal is to demonstrate a scoring or assessment pattern.

**Risks:**
- Strong anchoring effect — model may over-index on examples
- Requires artifact content structured as separable sections
- Token cost scales with example count

**Cost model:** `O(examples * avg_example_tokens * invocations)`

### `retrieval_only`

Artifact content is indexed locally. At runtime, the agent's current context is matched against the index, and top-k relevant sections are injected.

**Runtime behavior:**
- Artifact sections indexed at install time (local embedding or keyword index)
- Per-invocation: query against index, inject top-k results
- Consumer specifies `top_k` at attach time

**When to use:** Large reference artifacts where only a subset is relevant per query.

**Risks:**
- Retrieval quality depends on index and query quality
- Adds latency (~50-200ms per retrieval)
- May miss relevant sections if query doesn't match well

**Cost model:** `O(top_k * avg_section_tokens * invocations)` — sublinear in artifact size.

### `tool_policy`

Artifact knowledge is exposed as tool/function descriptions.

**Runtime behavior:**
- Artifact sections mapped to tool schemas
- Model decides when to invoke knowledge based on task context
- Consumer's tool-calling infrastructure handles execution

**When to use:** Agentic workflows where the model should autonomously decide when domain knowledge is relevant.

**Risks:**
- Requires model with tool/function calling support
- Model may invoke knowledge at inappropriate times
- Higher autonomy, lower predictability
- Tool schema design affects retrieval quality

**Cost model:** Tool description tokens consumed on every call; actual retrieval only when model invokes.

### `read_only_reference`

Artifact is available for the agent to consult but does not automatically influence behavior.

**Runtime behavior:**
- Artifact stored locally, accessible via explicit reference
- Agent must be instructed (or learn) to consult the artifact
- No automatic injection into context

**When to use:** Background reference material, documentation, lookup tables.

**Risks:**
- Agent may never consult the artifact if not prompted
- Least reliable for behavioral change
- Most conservative — minimal risk of negative transfer

**Cost model:** `O(0)` base cost — tokens only consumed when explicitly referenced.

## Conflict Resolution

When multiple artifacts are attached:
1. Check `conflicts` declarations — fail if conflicting artifacts are attached simultaneously
2. For `prepend_policy`: artifacts are concatenated in install order
3. For `few_shot_examples`: examples from all artifacts are interleaved
4. For `retrieval_only`: all artifacts share a single index
5. For `tool_policy`: tools from all artifacts are merged into the tool list

If two artifacts provide contradictory knowledge for the same subcategory, the higher-trust-score artifact takes precedence. This is a heuristic — proper conflict resolution is an open research problem.

## Publisher Declarations

Publishers declare attach support in the artifact schema:

```json
{
  "attach": {
    "supported_modes": ["prepend_policy", "retrieval_only"],
    "default_mode": "prepend_policy",
    "prohibited_modes": ["tool_policy"]
  }
}
```

- `supported_modes`: modes the publisher has tested and validated
- `default_mode`: recommended mode for typical use
- `prohibited_modes`: modes the publisher explicitly does not support (e.g., artifact structure is incompatible)

If no attach declaration is present, all modes are assumed supported with `prepend_policy` as default.
