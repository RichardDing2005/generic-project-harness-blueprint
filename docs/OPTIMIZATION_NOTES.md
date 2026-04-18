# Optimization Notes

These are recommended improvements beyond the base architecture.

## 1. Stable anchor extraction as a build step
Optional enhancement:
- generate a derived `pipeline_anchor_map.json` from `PIPELINE.md`,
- validate it in CI.

This keeps the source of truth in Markdown while giving automation a clean index.

## 2. Relative-path normalization in every generated summary
Normalize every stored path relative to repo root.

## 3. Separate accepted runs from raw runs
If the project grows, consider adding:
- `runs/active/`
- `runs/archive/`

This keeps the current stage cleaner while preserving history.

## 4. Snapshot cadence
Avoid snapshot spam.
Good default:
- one snapshot per completed single-round loop,
- one extra snapshot when the stage interpretation materially changes.

## 5. Promotion of stable rules
If a lesson stops being historical and becomes stable project doctrine, promote it:
- from memory snapshot,
- into `PIPELINE.md` or `AGENTS.md`.

This prevents memory from becoming the hidden source of truth.

## 6. Optional future plugin layer
If later you add optional skills, restrict them to:
- report packaging,
- reusable benchmark comparison,
- heavyweight release or publication prep,
- cross-project review helpers.

Do not push the core loop back into a mandatory skill layer.
