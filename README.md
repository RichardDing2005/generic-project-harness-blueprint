# Research Workspace Harness Architecture

A **kernel-centric harness blueprint** for long-horizon research and code-iteration projects.

This repository distills the usable parts of the uploaded `Research_Workspace` example into a cleaner, more open-source-ready architecture. The design intentionally avoids a mandatory outer-loop skill. Instead, it treats:

- `AGENTS.md` as the **always-on runtime kernel**
- `PIPELINE.md` as the **project-specific specification**
- `state/` as the **current execution pointer**
- `memory/` as the **structured historical record**
- `garbage/` as the **archive for superseded noise, invalid runs, and retired artifacts**

## Design goals

1. Keep the harness **highly integrated**, not fragmented across many small control files.
2. Make long-running work **recoverable** after interruption.
3. Keep stage logic **explicit** and **machine-locatable** through stable anchors.
4. Prevent context bloat by separating:
   - active memory
   - stage snapshots
   - garbage / retired records
5. Make the repository usable as a **public architecture package** without requiring a separate orchestration skill.

## What was retained from the sample project

The following ideas were preserved because they are structurally strong:

- A stage-based formal workflow with named gates.
- A separate active subflow for the current research focus.
- A clear distinction between:
  - training stages
  - review stages
  - support scans
- Artifact-first iteration: inspect the latest outputs before deciding the next action.
- Configuration-driven thresholds and stage defaults.
- Output organization under `runs/`.

## What was intentionally changed

The following changes make the architecture more coherent:

- The outer-loop skill is removed as a required control layer.
- `AGENTS.md` becomes the primary runtime kernel.
- `PIPELINE.md` becomes the single detailed project specification, with stable anchors.
- `STATE` is reduced to a small control pointer rather than a giant status document.
- `MEMORY` is structured into events and snapshots.
- Historical noise is not merely compressed; it can be retired into `garbage/`.
- Generated summaries should use **relative paths only**, never machine-specific absolute paths.

## Repository layout

```text
Research_Workspace_Harness_Architecture/
├── README.md
├── LICENSE
├── AGENTS.md
├── PIPELINE.md
├── CONTRIBUTING.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── EXECUTION_PROTOCOL.md
│   ├── MEMORY_POLICY.md
│   ├── GARBAGE_POLICY.md
│   ├── MIGRATION_NOTES_FROM_SAMPLE.md
│   └── OPTIMIZATION_NOTES.md
├── state/
│   ├── README.md
│   └── CURRENT_STATE.example.json
├── memory/
│   ├── README.md
│   ├── index.example.json
│   ├── active/
│   │   ├── events/
│   │   │   └── MEM-2026-04-17-0001.example.md
│   │   └── snapshots/
│   │       └── SNAPSHOT-argon_k1_inner-0001.example.md
│   └── templates/
│       ├── memory_event.template.md
│       └── memory_snapshot.template.md
├── garbage/
│   ├── README.md
│   ├── index.example.json
│   └── records/
│       └── GARBAGE-2026-04-17-0001.example.md
├── schemas/
│   ├── current_state.schema.json
│   ├── memory_index.schema.json
│   ├── memory_event.schema.json
│   ├── memory_snapshot.schema.json
│   └── garbage_index.schema.json
├── config/
│   └── stage_defaults.example.json
├── scripts/
│   ├── extract_pipeline_anchors.py
│   ├── validate_state.py
│   └── garbage_collect.py
└── examples/
    └── research_workspace/
        ├── CURRENT_STATE.example.json
        ├── pipeline_anchor_map.example.json
        ├── memory_event.example.md
        └── garbage_record.example.md
```

## Quick start

1. Read `AGENTS.md`.
2. Open `state/CURRENT_STATE.json` or a copy of `CURRENT_STATE.example.json`.
3. Resolve the anchors stored in state against `PIPELINE.md`.
4. Load the referenced memory snapshot and recent event records.
5. Act according to the active stage rules.
6. Write back:
   - one event
   - optional snapshot
   - updated state
7. Retire obsolete noise to `garbage/`.

## Why there is no mandatory outer-loop skill

This repository follows a **kernel-centric harness** model. If a control rule is always-on, project-specific, and should be read every run, it belongs in `AGENTS.md`, not in a separate lazily-loaded skill.

Optional skills may still be added later for heavy, reusable, non-core operations. They are intentionally **not** part of the base control architecture.

## Recommended next step

Merge the following files first if you want to retrofit the uploaded sample project:

- `AGENTS.md`
- `PIPELINE.md`
- `state/CURRENT_STATE.example.json`
- `memory/README.md`
- `garbage/README.md`
