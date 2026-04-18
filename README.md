# Generic Project Harness Blueprint

A clean, publishable blueprint for long-horizon projects that need a stable control kernel, explicit workflow stages, structured memory, and controlled forgetting.

This repository uses a **kernel-centric harness** model:

- `AGENTS.md` defines the always-on runtime protocol
- `PIPELINE.md` defines the project workflow and stage semantics
- `state/` stores the current execution pointer
- `memory/` stores useful historical evidence
- `garbage/` stores retired noise and superseded artifacts
- `config/` stores stage defaults and operational thresholds

The blueprint supports both:

- **fresh starts** from an empty project
- **retrofits** for projects that already contain code, outputs, and partial history

## Design goals

1. Keep control logic centralized and explicit.
2. Support restartable multi-round work.
3. Keep workflow stages machine-locatable through stable anchors.
4. Prevent context bloat with snapshots and retirement.
5. Preserve useful failure lessons without keeping all raw noise active.
6. Remain clean enough for direct public release.

## Repository layout

```text
generic-project-harness-blueprint/
├── README.md
├── LICENSE
├── AGENTS.md
├── PIPELINE.md
├── CONTRIBUTIONS.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── EXECUTION_PROTOCOL.md
│   ├── MEMORY_POLICY.md
│   ├── GARBAGE_POLICY.md
│   ├── ADOPTION_GUIDE.md
│   └── OPTIMIZATION_NOTES.md
├── state/
│   ├── README.md
│   ├── CURRENT_STATE.json
│   └── CURRENT_STATE.example.json
├── memory/
│   ├── README.md
│   ├── index.json
│   ├── index.example.json
│   ├── active/
│   │   ├── events/
│   │   │   └── MEM-EXAMPLE-0001.example.md
│   │   └── snapshots/
│   │       └── SNAPSHOT-primary_iteration-0001.example.md
│   └── templates/
│       ├── memory_event.template.md
│       └── memory_snapshot.template.md
├── garbage/
│   ├── README.md
│   ├── index.json
│   ├── index.example.json
│   └── records/
│       └── GARBAGE-EXAMPLE-0001.example.md
├── schemas/
│   ├── current_state.schema.json
│   ├── memory_index.schema.json
│   ├── memory_event.schema.json
│   ├── memory_snapshot.schema.json
│   └── garbage_index.schema.json
├── config/
│   ├── stage_defaults.json
│   └── stage_defaults.example.json
├── scripts/
│   ├── extract_pipeline_anchors.py
│   ├── validate_state.py
│   ├── garbage_collect.py
│   └── init_project.py
└── examples/
    └── generic_project/
        ├── CURRENT_STATE.example.json
        ├── pipeline_anchor_map.example.json
        ├── memory_event.example.md
        └── garbage_record.example.md
```

## Quick start

### Fresh start

1. Read `AGENTS.md`.
2. Initialize runtime files if needed:

```bash
python scripts/init_project.py --project-name <your_project_name>
```

3. Open `state/CURRENT_STATE.json`.
4. Resolve the anchors stored in state against `PIPELINE.md`.
5. Read the config files listed in `required_config_refs`.
6. If a snapshot exists, load it together with the event refs named in state.
7. Inspect the required artifacts.
8. Act according to the active stage and subflow rules.
9. Write back state, memory, and optional garbage records.

### Retrofit

1. Add the blueprint files to an existing repository.
2. Run `scripts/init_project.py`.
3. Rewrite `PIPELINE.md` so the stage rules match the real project.
4. Promote useful historical knowledge into `memory/`.
5. Retire obsolete raw material into `garbage/` only after preserving any lesson.

## Why there is no mandatory outer-loop skill

If a control rule is:

- always active,
- project-specific,
- and required on every run,

it belongs in `AGENTS.md`, not in a lazily loaded skill.

Optional skills may still be added later for heavy, reusable, non-core operations.
