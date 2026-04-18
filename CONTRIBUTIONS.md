# CONTRIBUTIONS

## Non-negotiable rules

1. **Do not duplicate control logic across files.**
   - `AGENTS.md` defines runtime behavior.
   - `PIPELINE.md` defines project-specific stage logic.
   - `STATE` stores only the current pointer and minimal control data.
   - `MEMORY` stores history.
   - `garbage/` stores retired noise.
   - `config/` stores concrete defaults and thresholds.

2. **Use relative paths only** in generated JSON, summaries, and indexes.

3. **Every stage heading in `PIPELINE.md` must have a stable anchor token** in square brackets.
   - Example: `## [PIPELINE:stage.primary_iteration] Stage: Primary Iteration`

4. **Every meaningful action must write one memory event.**
   - If a stage boundary is crossed or the local understanding changes materially, also write a snapshot.

5. **Retire raw noise, preserve lessons.**
   - Failed runs may be moved to `garbage/`.
   - Any actionable conclusion extracted from that failure should remain in `memory/`.

6. **Treat `STATE` as the authoritative runtime pointer.**
   - `memory/index.json` is discovery metadata, not the active-round controller.

7. **Do not add a mandatory outer-loop skill** unless the project requirements fundamentally change.

## Change workflow

1. Update `PIPELINE.md` if stage logic changed.
2. Update `AGENTS.md` only if the runtime kernel changed.
3. Update schemas if structure changed.
4. Run:
   - `python scripts/extract_pipeline_anchors.py`
   - `python scripts/validate_state.py`
5. If you retire artifacts, use `python scripts/garbage_collect.py --help`.
