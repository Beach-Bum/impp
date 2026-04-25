# IMPP Attach Modes

IMPP artifacts do not merely get "installed." They are attached to an agent runtime through a declared attach mode. Attach mode is part of the protocol because it determines how a memory artifact changes behavior, safety posture, latency, token use, and conflict handling.

A registry entry is incomplete unless it declares:

```yaml
attach:
  allowed_modes: []
  prohibited_modes: []
  default_mode: retrieval_only
```

## Why attach modes matter

A memory artifact can be used as policy, examples, retrieval context, a tool constraint, or a read-only reference. These are not equivalent. The same artifact may be safe as `retrieval_only` but unsafe as `prepend_policy`. The receiving runtime must know how the artifact is allowed to influence the agent.

## Mode summary

| Mode | Runtime behavior | Best use | Main risk |
|---|---|---|---|
| `prepend_policy` | Injects artifact instructions near the top of the agent context | High-priority procedural rules | Hidden instructions or policy conflict |
| `few_shot_examples` | Supplies examples that shape task behavior | Calibration, formatting, task demonstrations | Benchmark anchoring or example overfit |
| `retrieval_only` | Indexes artifact and retrieves relevant chunks on demand | Domain knowledge, large artifacts | Retrieval poisoning or irrelevant context |
| `tool_policy` | Constrains or guides tool calls and permissions | Safety, escalation, operational policy | Incorrectly granting or blocking actions |
| `read_only_reference` | Exposes artifact as a file/namespace consulted only when requested | Documentation, audit, low-risk review | Agent may ignore useful knowledge |

## `prepend_policy`

The artifact contributes instructions that are placed near the beginning of the context, often below system/developer policy but above task-specific user content.

### Intended use

- Safety policies.
- Domain decision rules.
- Escalation criteria.
- Strict operating procedures.

### Requirements

Artifacts using this mode should have:

- high trust state, normally `verified` or `curated`;
- no unresolved hidden-instruction findings;
- explicit conflict declarations;
- narrow scope;
- clear precedence rules against host policy.

### Risks

This is the highest-influence mode. A malicious or stale artifact can steer behavior broadly. Registries should default to blocking this mode unless the artifact explicitly allows it.

## `few_shot_examples`

The artifact contributes examples, rubrics, or demonstrations used to guide the model on similar tasks.

### Intended use

- Scoring calibration.
- Output format examples.
- Domain-specific reasoning demonstrations.
- Skill transfer through worked examples.

### Requirements

Examples should be marked as examples, not policy. If examples are derived from benchmarks, they must not overlap with live evaluation holdouts.

### Risks

Few-shot examples can leak answer keys, create anchoring effects, or overfit to benchmark structure. Sanitized examples are preferred for public artifacts.

## `retrieval_only`

The artifact is indexed and retrieved only when a runtime query indicates relevance. The artifact is not automatically injected into every task.

### Intended use

- Large procedural or semantic memory packages.
- Domain references.
- Low-friction onboarding.
- Artifacts with mixed relevance.

### Requirements

Runtime should preserve source attribution and namespace retrieved chunks. Retrieved content should be treated as untrusted context, not as system authority.

### Risks

Retrieval can surface irrelevant or adversarial chunks. Retrieval-only is safer than prepend-policy, but still needs prompt-injection handling.

## `tool_policy`

The artifact constrains or guides tool usage. Examples: when to call a scanner, when to request human review, which action requires approval, or what evidence must exist before a tool is called.

### Intended use

- Security triage.
- Compliance workflows.
- Deployment/runbook policies.
- Approval gates.

### Requirements

Tool-policy artifacts must declare exact tool namespaces, allowed actions, blocked actions, and escalation conditions. They should be verified or curated before production use.

### Risks

Incorrect tool policy can create operational damage by authorizing unsafe actions or blocking necessary ones.

## `read_only_reference`

The artifact is available as a document, file, or namespace but is not automatically inserted into model context. The agent or user must explicitly consult it.

### Intended use

- Documentation.
- Audit trails.
- Low-trust imports.
- Human review.

### Requirements

The runtime should make it clear when the artifact is being consulted.

### Risks

This is the safest mode but also the weakest transfer mechanism.

## Conflict handling

When multiple artifacts are installed, the runtime must resolve conflicts before execution.

Recommended order of precedence:

1. Host system/developer policy.
2. Organization policy.
3. Verified safety/tool-policy artifacts.
4. Domain artifacts.
5. User-selected references.
6. Imported or unverified artifacts.

If two artifacts declare the same conflict namespace and no precedence rule exists, the runtime should refuse automatic attachment and request review.

## Default safety posture

Recommended defaults:

- `imported`: `read_only_reference` only.
- `parsed`: `read_only_reference` or sandboxed `retrieval_only`.
- `evaluated`: `retrieval_only` or `few_shot_examples` if evaluation passed.
- `verified`: all declared allowed modes except high-risk modes blocked by host policy.
- `curated`: all declared allowed modes, still subject to host policy.

## Paper note

In the IMPP paper, "installing memory" should be defined as attaching a memory artifact under one of these modes. This prevents "install" from becoming a metaphor with unclear operational meaning.
