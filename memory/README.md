# Memory

`memory/` is the structured historical layer.

## Directory model

- `active/events/` — granular event records
- `active/snapshots/` — compressed stage-level summaries
- `templates/` — reusable record templates
- `index.json` — discovery index for active memory

## Governance rules

1. Every meaningful step writes one event.
2. Every completed round writes one snapshot.
3. Compression creates snapshots.
4. Forgetting / retirement moves raw noise into `garbage/`.
5. Lessons extracted from failed work remain in active memory.

## Reading pattern

The runtime should usually read:

1. `memory/index.json`
2. the snapshot named by state, if any
3. only the event files referenced by state

It should not read the entire memory history by default.

## Authority rule

`memory/index.json` is a discovery aid, not the authoritative execution pointer.

If it disagrees with `state/CURRENT_STATE.json`, the runtime follows state and then reconciles the index.
