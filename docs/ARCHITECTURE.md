# Architecture

## 1. Core model

This repository uses a **kernel-centric harness**.

The runtime is driven by five layers:

- `AGENTS.md` — execution kernel
- `PIPELINE.md` — project specification
- `state/` — execution pointer
- `memory/` — structured historical record
- `garbage/` — retired noise and superseded artifacts

`config/` acts as a required support layer for stage defaults, gates, and operational thresholds.

## 2. Why this architecture

Long-horizon projects repeatedly run into the same failure mode: **control diffusion**.

Part of the behavior lives in prompts, part in one-off scripts, part in ad hoc notes, and part in short-term model context. That makes the workflow fragile.

This architecture consolidates control:

- always-on control goes into `AGENTS.md`,
- project detail goes into `PIPELINE.md`,
- current position goes into `STATE`,
- evidence goes into `MEMORY`,
- retired noise goes into `garbage/`,
- configurable thresholds stay in `config/`.

## 3. Runtime data model

### 3.1 AGENTS.md
Stores:
- read order,
- bootstrap handling,
- execution cycle,
- writeback rules,
- escalation conditions,
- pointer authority,
- garbage rules.

### 3.2 PIPELINE.md
Stores:
- bootstrap stage,
- formal stage definitions,
- stage-local reads,
- stage-local verification,
- stage exits,
- subflow defaults,
- active subflow definitions.

### 3.3 STATE
Stores:
- bootstrap flag,
- current stage,
- current subflow step,
- anchor pointers,
- config refs,
- memory refs,
- blocking status,
- next action.

### 3.4 MEMORY
Stores:
- event records,
- compressed snapshots,
- discovery index.

### 3.5 garbage/
Stores:
- invalidated runs,
- superseded reports,
- retired logs,
- retirement index entries.

## 4. Intended scaling behavior

As the project grows:

- `PIPELINE.md` grows in **detail**, not in control duplication.
- `STATE` stays small.
- `MEMORY` grows through events and snapshots.
- `garbage/` prevents obsolete history from polluting the active context.
- `config/` remains the place for concrete gate values and defaults.

## 5. Context strategy

The control loop should never load the entire repository history.

Instead:

1. state selects the stage,
2. stage selects the relevant pipeline anchors,
3. state names the required config,
4. pipeline determines which artifacts matter,
5. memory provides only the latest relevant summary and event chain.

This keeps context bounded without erasing historical traceability.
