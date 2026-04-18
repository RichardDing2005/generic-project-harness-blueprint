# Adoption Guide

## When to use this blueprint

Use this repository if your project has most of the following properties:

- the work spans multiple rounds or sessions,
- the project has named stages or milestones,
- decisions depend on generated artifacts,
- historical context matters but must not flood the runtime,
- you need explicit promotion gates or review points.

## Minimal adoption sequence

1. Introduce `AGENTS.md` as the only always-on control file.
2. Rewrite your workflow description into anchored `PIPELINE.md`.
3. Run `python scripts/init_project.py --project-name <your_project_name>`.
4. Edit `config/stage_defaults.json`.
5. Add `memory/` and start with events only.
6. Add snapshots after the first stable round.
7. Add `garbage/` after the first time historical noise starts polluting memory.
8. Keep schemas and validation scripts in the repository.

## Retrofitting an existing project

If your project already has scripts, run outputs, and ad hoc notes:

- keep the scripts,
- keep the run artifact layout if it is already coherent,
- move control rules into `AGENTS.md`,
- move stage detail into `PIPELINE.md`,
- initialize runtime files,
- promote useful history into `memory/`,
- retire obsolete noise into `garbage/`.

## Common mistakes

- putting stage detail into `AGENTS.md`,
- storing long analysis in `STATE`,
- keeping every failed artifact in active memory,
- letting stage transitions happen without a recorded gate,
- allowing absolute machine-local paths into summaries,
- relying on `memory/index.json` instead of `STATE` as the active-round pointer.
