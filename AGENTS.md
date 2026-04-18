# AGENTS.md

This file is the **always-on runtime kernel** for the repository.

It defines how the agent must operate. It does **not** store the detailed project specification.

---

## 1. Runtime identity

You are operating inside a **kernel-centric harness**.

Your job is to:

1. initialize or read the current execution pointer,
2. locate the correct stage and subflow context,
3. load only the necessary history,
4. perform the minimal justified next action,
5. write back new history,
6. update the pointer,
7. retire invalid noise when appropriate.

---

## 2. Startup modes

The repository supports two startup modes.

### 2.1 Bootstrap mode

Bootstrap mode applies when either of the following is true:

- `state/CURRENT_STATE.json` does not exist,
- `state/CURRENT_STATE.json` exists and `bootstrap_mode` is `true`.

In bootstrap mode:

1. ensure the runtime files exist,
2. read `state/CURRENT_STATE.json`,
3. resolve `PIPELINE:bootstrap`,
4. read the config files listed in `required_config_refs`,
5. inspect only the minimum repository cues needed to determine the first real working stage,
6. write the first memory event,
7. update state out of bootstrap mode.

If the runtime files do not exist, initialize them with:

```bash
python scripts/init_project.py --project-name <your_project_name>
```

### 2.2 Normal mode

Normal mode applies when `bootstrap_mode` is `false`.

In normal mode, follow the required reading order below.

---

## 3. Required reading order

Before any analysis, coding, verification, or stage transition, read in this order:

1. `AGENTS.md`
2. `state/CURRENT_STATE.json`
3. `PIPELINE.md` at:
   - `current_pipeline_anchor`
   - `current_subflow_anchor` if present
4. each file in `required_config_refs`
5. `memory/index.json`
6. the snapshot referenced by `latest_snapshot_ref`, if present
7. each entry in `active_memory_refs`
8. the artifact files named in `required_artifact_refs` or required by the current stage

Do **not** begin implementation before completing this read sequence.

### 3.1 Pointer authority

`STATE` is the **authoritative runtime pointer** for the current execution round.

If `state/CURRENT_STATE.json` disagrees with `memory/index.json`:

- trust `STATE` for immediate execution,
- record a mismatch event in memory,
- reconcile `memory/index.json` before closing the round.

`memory/index.json` is a discovery and browsing aid. It is not the authoritative pointer for the active round.

---

## 4. Runtime principles

### 4.1 Minimal justified action
Take the smallest action that advances the current stage without silently broadening scope.

### 4.2 No silent stage jumping
Do not enter a downstream stage unless the current stage exit conditions are satisfied.

### 4.3 Artifact-first reasoning
When the current stage depends on produced outputs, inspect the newest relevant artifacts before proposing changes.

### 4.4 Relative-path discipline
All generated summaries, state entries, memory records, garbage records, and config references must use repository-relative paths only.

### 4.5 Preserve negative knowledge
If a failed attempt taught something real, keep the lesson in active memory even if the raw artifacts are moved to `garbage/`.

### 4.6 Do not let history sprawl
Use `memory/` for useful historical evidence, snapshots, and retained lessons. Use `garbage/` for retired noise, superseded artifacts, and raw failure detail that no longer belongs in the active context.

### 4.7 Stage-required config is mandatory input
If the current stage names a config requirement, treat that config as a required runtime input. Do not improvise thresholds, gates, or acceptance limits when a config file is expected.

---

## 5. Standard execution cycle

### Step A — initialize or locate
If runtime files are missing, initialize them. Then read `state/CURRENT_STATE.json`.

### Step B — resolve
Use the state anchors to find the active stage and subflow in `PIPELINE.md`.

### Step C — hydrate
Read the required config files, the latest snapshot if one exists, and the referenced event records from `memory/`.

### Step D — inspect
Read the artifacts required by the current stage.

### Step E — decide
Choose the minimal next action consistent with the current stage.

### Step F — act
Implement, analyze, verify, summarize, or initialize according to the stage rules.

### Step G — record
Write:
- one memory event,
- optional snapshot,
- updated state,
- updated memory index.

### Step H — retire
If the step produced invalidated noise, move it into `garbage/` and record the move.

---

## 6. Ask-user conditions

Do **not** stop for routine local ambiguity. Continue automatically unless one of these holds:

1. a destructive cleanup is required,
2. the pipeline rules and codebase conflict in a way that changes stage semantics,
3. the stage cannot proceed without a new project decision,
4. the current stage would need to broaden beyond the allowed subflow,
5. the artifact set, config inputs, and state pointer disagree in a way that cannot be resolved from the repository.

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
- per-stage config values,
- local verification metrics,
- data schema details,
- per-stage repair strategy options.

Those belong in `PIPELINE.md` and `config/`.
