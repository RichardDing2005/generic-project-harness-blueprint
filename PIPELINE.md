# Generic Project Pipeline Specification

This file is the **detailed project specification**. It defines the bootstrap entry stage, the formal workflow, the active subflow model, local verification rules, and stage exit conditions.

All anchors in square brackets are **stable machine-readable tokens**. `STATE` must point to these anchors, not to plain-language headings.

---

## [PIPELINE:overview] Overview

The repository contains three views of the same project:

1. the **bootstrap entry stage**,
2. the **formal full workflow**,
3. the **currently active targeted subflow**.

Bootstrap exists to let a project start from zero or to retrofit an existing repository that has partial history but no working harness state.

The formal workflow defines the complete long-horizon path. The active subflow defines what should actually be executed right now unless the state explicitly says otherwise.

---

## [PIPELINE:bootstrap] Bootstrap entry stage

### [GOAL:bootstrap]
Create enough structure to move from an uninitialized or partially initialized repository into a valid formal stage.

### [READS:bootstrap]
Read only the minimum required inputs:

- `state/CURRENT_STATE.json`, if it exists,
- each file in `required_config_refs`,
- the top-level repository layout,
- the minimum existing artifact or note set needed to determine the first real working stage.

### [VERIFY:bootstrap]
Bootstrap succeeds only when:

- runtime files exist,
- the first formal stage is chosen,
- the first pipeline anchor is valid,
- the first memory event is written,
- state has been updated out of bootstrap mode.

### [EXIT:bootstrap]
Exit bootstrap by updating state to a formal stage and, if applicable, the default subflow for that stage.

---

## [PIPELINE:formal_workflow] Formal full workflow

```text
primary_iteration
-> gate_review
-> downstream_iteration
-> integration_review
-> external_validation
```

### Formal interpretation

- `primary_iteration` is the first mainline build / diagnose / improve stage.
- `gate_review` is a read-only promotion gate between the primary stage and the downstream stage.
- `downstream_iteration` is the stage entered only after the primary candidate is promoted.
- `integration_review` is the structured review layer that judges project-wide coherence.
- `external_validation` is the final validation stage against an accepted external target, held-out set, or downstream benchmark.

---

## [PIPELINE:active_subflow_model] Active subflow model

The blueprint supports stage-scoped active subflows.

- A formal stage may define a default subflow.
- `STATE` may override the default subflow when the repository has a justified local reason.
- If a formal stage does not define a default subflow, it is valid to operate without an active subflow.

### [SUBFLOW_DEFAULT:primary_iteration]
Default anchor: `PIPELINE:subflow.stage_identification`

### [SUBFLOW_DEFAULT:gate_review]
No default subflow.

### [SUBFLOW_DEFAULT:downstream_iteration]
No default subflow in the base blueprint.

### [SUBFLOW_DEFAULT:integration_review]
No default subflow in the base blueprint.

### [SUBFLOW_DEFAULT:external_validation]
No default subflow in the base blueprint.

### [RULE:state_overrides_default_subflow]
If `STATE` provides a valid `current_subflow_anchor`, use it instead of the stage default.

---

## [PIPELINE:active_subflow] Active targeted repair subflow

The default active operational main line for `primary_iteration` is:

```text
stage identification
-> existing artifact analysis
-> problem isolation
-> minimal repair strategy
-> implementation
-> smoke check
-> formal execution
-> artifact analysis
-> stop and summarize
```

This subflow exists inside the `primary_iteration` working period and is intentionally narrower than the full workflow.

---

## [PIPELINE:global_boundaries] Global boundaries

### [RULE:family_name]
- Active family name: `candidate_family`

### [RULE:main_line]
- Main line: primary workstream
- External validation is validation-only, not the primary iteration line

### [RULE:source_policy]
- Unaccepted or experimental sources must not silently become the main line
- Accepted validation sources must be declared in `data/processed/data_manifest.json`
- Validation-only sources must remain downstream until explicitly promoted

### [RULE:data_contract]
The data contract should preserve at least:

- `record_id`
- `input_signature`
- `target_value`
- `partition`
- `source_file`
- `source_group`
- `created_at`

Add project-specific fields as needed, but keep the minimum contract stable across stages.

### [RULE:direction_of_work]
The project must keep a stable declared direction of work.

Examples:
- `input -> prediction`
- `artifact bundle -> review decision`
- `code change -> execution artifact -> verification result`

### [RULE:window_policy]
If the project uses local windows, slices, checkpoints, or target subsets, choose them deliberately for a round and freeze them for that round.

### [RULE:active_scope]
During the active repair phase, work only inside the currently declared narrow target. Do not broaden to unrelated downstream ideas without passing the current stage gate.

### [RULE:invariant_protection]
Do not trade away accepted core behavior merely to improve a surface metric. The project must name which invariants are protected before each round.

### [RULE:config_contract]
Every stage that depends on thresholds, defaults, acceptance limits, or gate logic must declare those files through `STATE.required_config_refs`. Config is a first-class runtime input, not an implicit assumption.

---

## [PIPELINE:data_layer] Data layer

### [DATA:raw_inputs]
Raw inputs live under `data/raw/`.

Examples may include:

- source datasets,
- raw logs,
- instrument captures,
- external benchmark bundles,
- imported project artifacts.

### [DATA:processed_outputs]
Processed outputs live under `data/processed/`.

Expected outputs include:

- canonical processed dataset(s),
- `data_manifest.json`,
- `DATA_INTERFACE.md`,
- any stable stage-ready material required by the main workflow.

### [DATA:semantics]
- Storage may remain wide even if the current implementation does not consume every field directly.
- Preprocessing should remove clearly unusable records while preserving traceability.
- The project should keep a stable record of source provenance.

---

## [PIPELINE:artifact_layer] Artifact layer

### [ARTIFACT:runs_root]
All generated stage outputs should live under `runs/`.

### [ARTIFACT:recommended_structure]
Recommended categories:

- `runs/workflow/` — workflow-level summaries
- `runs/primary_iteration/` — active inner-loop runs
- `runs/gate_review/` — promotion decisions
- `runs/downstream_iteration/` — promoted-stage runs
- `runs/integration_review/` — broad review outputs
- `runs/external_validation/` — validation outputs

### [ARTIFACT:latest_aliases]
If the project exposes `latest/` aliases or symlinks, ensure they always resolve to repository-relative targets.

---

## [PIPELINE:stage.primary_iteration] Stage: Primary Iteration

### [GOAL:primary_iteration]
Perform the active inner-loop diagnosis and improvement cycle for the current mainline candidate.

### [SCOPE:primary_iteration]
Allowed:
- narrow repair inside the current target,
- implementation changes required for diagnosis or improvement,
- smoke and formal runs,
- artifact analysis.

Not allowed by default:
- automatic entry into downstream stages,
- rewriting the validation track as the main line,
- broadening the scope beyond the declared target of the round.

### [READS:primary_iteration]
Before acting, read:

- current state,
- each file in `required_config_refs`,
- latest stage summary for the most recent primary run,
- latest review summary if it exists,
- latest diagnostics if they exist,
- representative artifacts for the current target,
- any preserved lessons tied to the current narrow target.

### [FOCUS:primary_iteration]
Prioritize, in project-specific order:
1. highest-risk artifacts,
2. boundary cases,
3. recent regressions,
4. artifacts named explicitly by state.

### [VERIFY:primary_iteration.loop]
For local iteration quality, inspect a **set** of project-relevant signals, not a single global aggregate.

Typical categories:
- primary quality metric,
- secondary quality metric,
- stability / sanity metric,
- regression count,
- artifact completeness,
- stage-specific invariants.

Do not use one aggregate score alone as the decision basis.

### [EXIT:primary_iteration]
This stage may exit into `gate_review` only after:
- a formal primary run exists,
- the stage summary exists,
- the required artifacts exist,
- the run has been analyzed and recorded in memory.

### [MEMORY_WRITE:primary_iteration]
Required writes:
- one event after each diagnosis or execution step,
- one snapshot after a completed single-round cycle,
- state update after every formal run and after every stage summary judgment.

---

## [PIPELINE:stage.gate_review] Stage: Gate Review

### [GOAL:gate_review]
Decide whether the current primary candidate is allowed to enter the downstream stage.

### [READS:gate_review]
Required inputs:
- the latest stage summary from the primary stage,
- each file in `required_config_refs`,
- the baseline or accepted reference bundle,
- the most recent retained blocker lessons if the candidate has failed before.

### [VERIFY:gate_review]
Formal gate:
- stage sanity checks pass,
- candidate quality remains within the configured tolerance relative to the accepted baseline,
- no protected invariant is broken,
- no unresolved blocker remains hidden in memory or state.

### [EXIT:gate_review]
If the gate fails:
- stop downstream progression,
- record the failed gate as a memory event,
- remain in primary-oriented work.

If the gate passes:
- update state to allow `downstream_iteration`.

### [MEMORY_WRITE:gate_review]
Required write:
- one review event with the decision,
- optional snapshot if the decision changes the project trajectory.

---

## [PIPELINE:stage.downstream_iteration] Stage: Downstream Iteration

### [GOAL:downstream_iteration]
Run the next planned stage after the primary candidate has been promoted.

### [STATUS:downstream_iteration]
This stage exists in the formal workflow but is not part of the active repair subflow by default.

### [VERIFY:downstream_iteration]
Stage-local verification should confirm:
- the stage summary exists,
- promoted-stage sanity checks pass,
- downstream artifact generation is complete enough for review.

### [EXIT:downstream_iteration]
May advance to `integration_review` only when the local artifacts are sufficient for project-wide review.

---

## [PIPELINE:stage.integration_review] Stage: Integration Review

### [GOAL:integration_review]
Perform the main structured review of project-wide agreement between implementation, artifacts, and declared objectives.

### [READS:integration_review]
Required inputs:
- latest downstream stage summary,
- each file in `required_config_refs`,
- latest project-level diagnostic summary,
- latest integration or feature review summary,
- any support evidence declared by the project.

### [VERIFY:integration_review]
Primary gate:
- required review artifacts exist and are interpretable,
- expected metric ordering or review logic remains coherent,
- upstream sanity is still valid,
- the promoted candidate still fits the declared project direction.

Support-only evidence:
- optional deeper scans,
- optional benchmark expansions,
- optional secondary analyses.

### [EXIT:integration_review]
If integration review fails:
- stop before external validation,
- record the blocking reason in memory and state.

If it passes:
- allow `external_validation`.

---

## [PIPELINE:stage.external_validation] Stage: External Validation

### [GOAL:external_validation]
Validate the promoted architecture, implementation, or workflow against an accepted external target.

### [READS:external_validation]
Required inputs:
- the accepted validation dataset or benchmark bundle,
- the promoted upstream candidate,
- each file in `required_config_refs`,
- the validation source policy.

### [VERIFY:external_validation]
Validation must confirm:
- the accepted source policy was respected,
- the run is tied to the same core candidate or promoted family,
- the external result remains within the intended design envelope.

### [EXIT:external_validation]
A validation pass records a downstream result for the promoted family. It does not rewrite the full project specification by itself.

---

## [PIPELINE:subflow.stage_identification] Active subflow: stage identification

### [GOAL:stage_identification]
Automatically identify:
- current formal workflow stage,
- current active subflow stage,
- latest stage directory relevant to the working round.

### [OUTPUT:stage_identification]
Write an event recording:
- stage determination,
- evidence files used,
- latest relevant artifact directory.

---

## [PIPELINE:subflow.artifact_analysis_pre] Active subflow: existing artifact analysis

### [GOAL:artifact_analysis_pre]
Analyze the latest available artifacts before changing code or project logic.

### [READS:artifact_analysis_pre]
Read, when present:
- `workflow_summary.json`
- `stage_summary.json`
- `review_summary.json`
- diagnostics reports
- representative artifacts
- any recent retained blocker events

### [VERIFY:artifact_analysis_pre]
The analysis must explicitly distinguish:
- primary error / mismatch,
- stability risk,
- boundary-case risk,
- artifact-generation risk,
- whether any apparent gain is merely cosmetic.

---

## [PIPELINE:subflow.problem_isolation] Active subflow: problem isolation

### [GOAL:problem_isolation]
Reduce the observed mismatch to the smallest actionable problem statement.

### [OUTPUT:problem_isolation]
Produce one event that names:
- the dominant issue,
- the affected artifact family or scope,
- the intended narrow repair target.

---

## [PIPELINE:subflow.minimal_repair_strategy] Active subflow: minimal repair strategy

### [GOAL:minimal_repair_strategy]
Choose the smallest justified repair strategy for the active round.

### [RULE:minimal_repair_strategy]
Do not broaden to downstream-only ideas during the active repair round.

### [OUTPUT:minimal_repair_strategy]
Record:
- what will change,
- what will not change,
- which failure mode is being targeted.

---

## [PIPELINE:subflow.implementation] Active subflow: implementation

### [GOAL:implementation]
Implement the selected minimal repair.

### [VERIFY:implementation]
Before formal execution:
- code or project changes are coherent,
- affected files are known,
- the intended repair scope did not silently expand.

---

## [PIPELINE:subflow.smoke_check] Active subflow: smoke check

### [GOAL:smoke_check]
Run a low-cost smoke validation before a formal stage execution.

### [VERIFY:smoke_check]
A smoke run must be sufficient to detect:
- broken execution,
- clearly invalid outputs,
- obvious artifact generation failure.

If smoke fails:
- remain in the current subflow,
- record a failure event,
- optionally archive invalid raw artifacts to `garbage/`.

---

## [PIPELINE:subflow.formal_execution] Active subflow: formal execution

### [GOAL:formal_execution]
Run the formal stage for the active round.

### [VERIFY:formal_execution]
The formal run should produce the project-defined minimum artifact set, typically including:
- stage summary,
- diagnostics,
- representative outputs,
- any required scorecards or parameter summaries.

---

## [PIPELINE:subflow.artifact_analysis_post] Active subflow: post-run artifact analysis

### [GOAL:artifact_analysis_post]
Analyze the new formal outputs and decide whether the round improved the target behavior.

### [VERIFY:artifact_analysis_post]
The analysis must explicitly check:
- protected invariant preservation,
- quality change,
- stability change,
- local feature or artifact quality,
- whether any apparent gain was merely cosmetic.

---

## [PIPELINE:subflow.round_summary] Active subflow: stop and summarize

### [GOAL:round_summary]
Stop after one completed round and summarize the result.

### [OUTPUT:round_summary]
Write:
- one stage snapshot,
- one updated state file,
- optional garbage records for retired noise.

Do not automatically begin a second repair round.

---

## [PIPELINE:garbage_policy] Garbage and forgetting policy

### [RULE:garbage_when]
Move a record or artifact into `garbage/` when:
- it is invalidated,
- it is superseded,
- it is too verbose to retain in active memory,
- it is a failed exploratory branch whose useful lesson has already been preserved elsewhere.

### [RULE:garbage_keep_lessons]
Before retiring raw failure detail, preserve at least one short lesson in active memory if the failure taught something real.

### [RULE:garbage_index]
Every garbage move must append a record to `garbage/index.json`.

---

## [PIPELINE:path_policy] Path policy

All machine-readable outputs must use repository-relative paths. Absolute local-machine paths are forbidden in generated state, memory, review, or workflow summaries.

---

## [PIPELINE:end] End of specification
