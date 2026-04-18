# Memory Policy

## 1. Memory is not a dump

`memory/` exists to preserve useful history, not to preserve every byte forever.

The repository distinguishes:

- **events** — granular step records
- **snapshots** — compressed stage-level summaries

## 2. Event records

An event records one meaningful action or one meaningful observation.

Typical event types:

- `stage_identification`
- `artifact_analysis`
- `decision`
- `implementation`
- `smoke_result`
- `formal_run_result`
- `verification`
- `lesson`
- `blocker`

## 3. Snapshots

A snapshot is a compressed summary of the current stage understanding.

Write a snapshot when:

- a stage boundary is crossed,
- a completed round finishes,
- the dominant interpretation changes,
- several old events should be compacted into a single retained summary.

## 4. Compress vs forget

### Compress
Use compression when the old material still matters but is too long.

### Forget / garbage
Use forgetting when the old raw material no longer deserves a place in active context.

Examples of compress-worthy material:
- several repeated observations that converge on one diagnosis,
- many small implementation events that culminate in one stage result.

Examples of garbage-worthy material:
- invalid smoke artifacts,
- superseded exploratory analysis,
- large verbose logs whose lessons were already extracted,
- abandoned intermediate outputs.

## 5. Preserve negative knowledge

Do not keep noisy failed runs in active memory if they are not useful.  
Do keep the lesson if the failure established something real.

Example:
- raw run files move to `garbage/`
- one event remains in `memory/` saying:
  "Repair strategy X flattened Vr=0 valleys and should not be reused."

## 6. Index discipline

`memory/index.json` should point to:

- active snapshot
- recent events
- garbage policy version
- last update time

It should not become a second giant memory document.
