# Architecture

## 1. Core model

This repository uses a **kernel-centric harness**.

The runtime is driven by four core layers:

- `AGENTS.md` — execution kernel
- `PIPELINE.md` — project specification
- `state/` — execution pointer
- `memory/` — structured historical record

A fifth support layer exists:

- `garbage/` — retired noise and superseded artifacts

## 2. Why this architecture

The uploaded sample project already had good bones:

- stage names were explicit,
- outputs were organized under `runs/`,
- training and review were separated,
- the active K1 repair subflow was clearly narrower than the full workflow.

The main problem was not missing concepts. The main problem was **control diffusion**:

- part of the behavior lived in the pipeline text,
- part in a generated skill,
- part in the prompt,
- and part in the scripts.

This architecture consolidates control:

- always-on control goes into `AGENTS.md`,
- project detail goes into `PIPELINE.md`,
- current position goes into `STATE`,
- evidence goes into `MEMORY`.

## 3. Runtime data model

### 3.1 AGENTS.md
Stores:
- read order,
- execution cycle,
- writeback rules,
- escalation conditions,
- garbage rules.

### 3.2 PIPELINE.md
Stores:
- stage definitions,
- stage-local reads,
- stage-local verification,
- stage exits,
- active subflow.

### 3.3 STATE
Stores:
- current stage,
- current subflow step,
- anchor pointers,
- memory refs,
- blocking status,
- next action.

### 3.4 MEMORY
Stores:
- event records,
- compressed snapshots,
- index references.

### 3.5 garbage/
Stores:
- invalidated runs,
- superseded reports,
- retired logs,
- garbage index entries.

## 4. Intended scaling behavior

As the project grows:

- `PIPELINE.md` grows in **detail**, not in control duplication.
- `STATE` stays small.
- `MEMORY` grows through events and snapshots.
- `garbage/` prevents obsolete history from polluting the active context.

## 5. Context strategy

The control loop should never load the entire repository history.

Instead:

1. state selects the stage,
2. stage selects the relevant pipeline anchors,
3. pipeline determines which artifacts matter,
4. memory provides only the latest relevant summary and event chain.

This keeps context bounded without erasing historical traceability.

## 6. When to add optional skills later

A separate skill is justified only if all of these hold:

- it is not always-on,
- it is reusable across projects,
- it is costly enough that lazy loading matters,
- it should be isolated from the core loop.

Examples:
- a heavy reporting skill,
- a paper-ready figure packaging skill,
- a benchmark comparison skill shared across repositories.

The base control architecture should remain skill-free.
