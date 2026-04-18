# Execution Protocol

## Canonical run order

The canonical execution order is:

1. read `AGENTS.md`
2. read `state/CURRENT_STATE.json`
3. resolve anchors in `PIPELINE.md`
4. read memory snapshot and referenced events
5. inspect required artifacts
6. execute the minimal justified action
7. verify the result
8. write memory
9. update state
10. retire garbage if needed

## State-first, but under AGENTS control

The practical phrasing is:

> start from `AGENTS.md`; `AGENTS.md` tells the agent to read `STATE` first.

This keeps the architecture conceptually clean:

- `AGENTS.md` is the kernel,
- `STATE` is the first runtime operand.

## Required writeback sequence

After any meaningful action:

1. write memory event,
2. if understanding changed materially, write snapshot,
3. update state,
4. if noise became invalid, move it to `garbage/` and index it.

Do not update state before memory is written.

## Failure handling

If an action fails:

1. write a failure event,
2. decide whether the raw failure detail belongs in active memory or garbage,
3. preserve the lesson if one exists,
4. update state with the blocking condition or next action.

## Single-round policy

For the active repair subflow:

- do one full round,
- stop and summarize,
- do not automatically start round two.
