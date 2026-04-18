# Memory

`memory/` is the structured historical layer.

## Directory model

- `active/events/` — granular event records
- `active/snapshots/` — compressed stage-level summaries
- `templates/` — reusable record templates
- `index.json` — active index

## Governance rules

1. Every meaningful step writes one event.
2. Every completed round writes one snapshot.
3. Compression creates snapshots.
4. Forgetting / retirement moves raw noise into `garbage/`.
5. Lessons extracted from failed work remain in active memory.

## Reading pattern

The runtime should usually read:

1. `memory/index.json`
2. the latest snapshot
3. only the event files referenced by state

It should not read the entire memory history by default.
