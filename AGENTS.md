# AGENTS.md

This file is the **always-on runtime kernel** for the repository.

It does **not** store the detailed project specification. It defines **how the agent must operate**.

---

## 1. Runtime identity

You are operating inside a **kernel-centric harness**.

Your job is not to re-derive the workflow from scratch. Your job is to:

1. read the current execution pointer,
2. locate the correct stage and subflow context,
3. load only the necessary history,
4. perform the minimal justified next action,
5. write back new history,
6. update the pointer,
7. retire invalid noise when appropriate.

---

## 2. Required reading order

Before any analysis, coding, verification, or stage transition, read in this order:

1. `AGENTS.md`
2. `state/CURRENT_STATE.json`
3. `PIPELINE.md` at:
   - `current_pipeline_anchor`
   - `current_subflow_anchor` if present
4. `memory/index.json`
5. the referenced snapshot in `latest_snapshot_ref`
6. each entry in `active_memory_refs`
7. the artifact files named in state or required by the current stage

Do **not** begin implementation before completing this read sequence.

---

## 3. Runtime principles

### 3.1 Minimal justified action
Take the smallest action that advances the current stage without silently broadening scope.

### 3.2 No silent stage jumping
Do not enter a downstream stage unless the current stage exit conditions are satisfied.

### 3.3 Artifact-first reasoning
When the current stage depends on produced outputs, inspect the newest relevant artifacts before proposing changes.

### 3.4 Relative-path discipline
All generated summaries, state entries, memory records, and garbage records must use repository-relative paths only.

### 3.5 Preserve negative knowledge
If a failed attempt taught something real, keep the lesson in active memory even if the raw artifacts are moved to `garbage/`.

---

## 4. Current repository kernel rules

### 4.1 Current project shape
This repository supports:

- one **formal full workflow**
- one **currently active subflow**
- stage-gated progression
- iterative artifact analysis
- explicit memory and garbage governance

### 4.2 Stage gating
A stage may only advance when:

- its local verification rules pass,
- its exit gate passes,
- state is updated,
- memory has recorded the decision.

### 4.3 Memory governance
For every meaningful step:

- write one event record,
- update `memory/index.json`,
- optionally create a snapshot if the stage understanding materially changed.

### 4.4 Garbage governance
Move noise to `garbage/` when any of the following becomes true:

- the artifact is superseded,
- the artifact is invalidated by a later decision,
- the artifact is known to be misleading,
- the artifact is too verbose to keep in active context and its useful lesson has already been extracted.

---

## 5. Standard execution cycle

### Step A — locate
Read `state/CURRENT_STATE.json`.

### Step B — resolve
Use the state anchors to find the active stage and subflow in `PIPELINE.md`.

### Step C — hydrate
Read the latest snapshot and the referenced event records from `memory/`.

### Step D — inspect
Read the artifacts required by the current stage.

### Step E — decide
Choose the minimal next action consistent with the current stage.

### Step F — act
Implement, analyze, verify, or summarize according to the stage rules.

### Step G — record
Write:
- one memory event,
- optional snapshot,
- updated state.

### Step H — retire
If the step produced invalidated noise, move it into `garbage/` and record the move.

---

## 6. Ask-user conditions

Do **not** stop for routine local ambiguity. Continue automatically unless one of these holds:

1. a destructive cleanup is required,
2. the pipeline rules and codebase conflict in a way that changes stage semantics,
3. the stage cannot proceed without a new research decision,
4. the current stage would need to broaden beyond the allowed subflow,
5. the artifact and the state pointer disagree in a way that cannot be resolved from the repository.

---

## 7. Output format for human-facing updates

For each completed sub-step, prefer this structure:

- `Stage Result`
- `Evidence`
- `Next Choice`

Keep evidence anchored to concrete files and concrete observations.

---

## 8. Do not store here

Do not place the following in `AGENTS.md`:

- detailed stage thresholds,
- stage-specific artifact lists,
- local verification metrics,
- data schema details,
- per-stage repair strategy options.

Those belong in `PIPELINE.md`.
