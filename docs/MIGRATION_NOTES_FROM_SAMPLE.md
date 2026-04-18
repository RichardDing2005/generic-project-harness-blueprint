# Migration Notes From the Uploaded Sample

## Good structures retained

The uploaded example already had several strong patterns:

1. **Formal workflow naming**
   - `argon_k1_inner`
   - `k1_ready_review`
   - `argon_k4_inner`
   - `outer_review`
   - `hg_validation`

2. **A narrower active subflow**
   - stage identification
   - artifact analysis
   - minimal repair
   - coding
   - smoke
   - formal run
   - post-run analysis
   - stop and summarize

3. **Artifact-first decision making**
   - stage summaries
   - review summaries
   - fit diagnostics
   - fit plots

4. **Program separation**
   - training
   - review
   - scans
   - workflow orchestration

5. **Configurable defaults**
   - thresholds
   - weak-curve targets
   - scan settings

## Main issues corrected

### Issue 1 — Outer control was split across too many places
The sample spread control logic across:
- pipeline text,
- prompt text,
- skill text,
- orchestration code.

This architecture consolidates that.

### Issue 2 — Generated summaries used absolute local paths
Those are unsuitable for public, portable repositories.  
All generated references should be relative.

### Issue 3 — The skill duplicated always-on logic
The repository can run more cleanly if the always-on control rules live in `AGENTS.md`.

### Issue 4 — Memory and retirement were implicit
The sample had many run artifacts but no explicit memory-governance layer and no explicit retirement area.

This architecture adds:
- `memory/`
- `garbage/`
- schemas
- indexing rules

## Migration sequence

1. Keep your current training / review / scan scripts.
2. Replace the old workflow-control role of the skill with `AGENTS.md`.
3. Refactor `pipeline.md` into anchored `PIPELINE.md`.
4. Introduce `state/CURRENT_STATE.json`.
5. Introduce `memory/` and `garbage/`.
6. Convert summaries to relative paths.
7. Add validation scripts.
