# Execution Protocol

## Canonical run order

The canonical execution order is:

1. read `AGENTS.md`
2. read `state/CURRENT_STATE.json`
3. if bootstrap mode is active, resolve `PIPELINE:bootstrap`
4. otherwise resolve the current anchors in `PIPELINE.md`
5. read the config files listed in `required_config_refs`
6. read `memory/index.json`
7. read the snapshot and events named by state, if present
8. inspect required artifacts
9. execute the minimal justified action
10. verify the result
11. write memory
12. update state
13. retire garbage if needed

## State-first, but under AGENTS control

The practical phrasing is:

> start from `AGENTS.md`; `AGENTS.md` tells the agent to read `STATE` first.

This keeps the architecture conceptually clean:

- `AGENTS.md` is the kernel,
- `STATE` is the first runtime operand,
- `PIPELINE.md` provides the stage-local semantics,
- `MEMORY` provides the required historical evidence,
- `config/` provides the stage-required operational defaults.

## Pointer authority

`STATE` is authoritative for the current round.

If `memory/index.json` points somewhere else:

- execute using `STATE`,
- record the mismatch,
- reconcile the index before the round closes.

## Reading discipline

Never load the entire repository by default.

Read only:

- the current stage and subflow anchors,
- the config files named by state,
- the latest snapshot named by state,
- the event refs pointed to by state,
- the artifacts required by the current stage.

## Single-round policy for active repair

For the default active repair subflow:

- do one full round,
- stop and summarize,
- do not automatically start round two.

This prevents silent drift and keeps memory snapshots meaningful.

## Failure handling

When a step fails:

1. record an event,
2. decide whether the raw failure detail belongs in active memory or garbage,
3. preserve the lesson if one exists,
4. update state with the blocking condition or next action.
