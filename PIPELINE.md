# Research Workspace Pipeline Specification

This file is the **detailed project specification**. It defines the formal workflow, the currently active subflow, stage boundaries, local verification rules, and stage exit conditions.

All anchors in square brackets are **stable machine-readable tokens**. `STATE` must point to these anchors, not to plain-language headings.

---

## [PIPELINE:overview] Overview

The repository contains two valid views of the same project:

1. the **formal full workflow**
2. the **currently active K1-only repair subflow**

The formal workflow defines the complete long-horizon path.  
The active subflow defines what should actually be executed right now unless the state explicitly says otherwise.

---

## [PIPELINE:formal_workflow] Formal full workflow

```text
argon_k1_inner
-> k1_ready_review
-> argon_k4_inner
-> outer_review
-> hg_validation
```

### Formal interpretation

- `argon_k1_inner` is the first Argon training stage.
- `k1_ready_review` is a read-only gate between `K=1` and `K=4`.
- `argon_k4_inner` is the downstream Argon stage after K1 promotion.
- `outer_review` is the model-to-data review layer.
- `hg_validation` is the Mercury validation stage after passing outer review.

---

## [PIPELINE:active_subflow] Active K1-only repair subflow

The active operational main line is:

```text
stage identification
-> existing artifact analysis
-> problem isolation
-> minimal K1 repair strategy
-> coding
-> K1 smoke
-> K1 formal
-> artifact analysis
-> stop and summarize
```

This subflow exists inside the `argon_k1_inner` working period and is intentionally narrower than the full workflow.

---

## [PIPELINE:global_boundaries] Global boundaries

### [RULE:family_name]
- Active family name: `rw_v1`

### [RULE:main_line]
- Main line: Argon
- Mercury is validation-only, not the primary iteration line

### [RULE:mercury_sources]
- Forbidden Mercury source: `178_CH1VsCH2.xlsx`
- Allowed Mercury source: `fig3_extracted_package`
- Validation only accepts the black extracted curve family

### [RULE:data_contract]
The data contract must preserve at least:

- `gas`
- `curve_id`
- `Va`
- `Ip`
- `Vr`
- `temperature_C`
- `source_file`
- `source_group`

### [RULE:training_direction]
Training direction remains physical-forward:

- `Va / Vr / T-placeholder -> Ip`

### [RULE:window_policy]
Argon and Mercury local-scan window strategies are chosen separately and then frozen for a round.

### [RULE:active_kernel_scope]
During the active repair phase, use `K=1 only`.

### [RULE:oscillation_protection]
Weak-curve oscillation structure must not be traded away for a smoother envelope-only fit.

---

## [PIPELINE:data_layer] Data layer

### [DATA:raw_inputs]
Raw inputs live under `data/experiment_raw_data/`.

Required sources:

- `argon/FHdata.xlsx`
- `mercury/fig3_extracted_package/`

### [DATA:processed_outputs]
Processed outputs live under `data/processed_data/`.

Expected outputs include:

- `argon/argon_curves.csv`
- `mercury/mercury_fig3_black_curves.csv`
- `combined/standardized_curves.csv`
- `data_manifest.json`
- `DATA_INTERFACE.md`

### [DATA:semantics]
- Argon curves are mainly distinguished by `Vr`
- Mercury curves are mainly distinguished by `temperature_C`
- Storage may remain wide even if the current model does not consume every field directly
- Preprocessing should remove clearly abnormal points and preserve a usable `Va` grid

---

## [PIPELINE:stage.argon_k1_inner] Stage: Argon K1 Inner Loop

### [GOAL:argon_k1_inner]
Perform the active `K=1` kernel-focused training and diagnosis loop for Argon.

### [SCOPE:argon_k1_inner]
Allowed:
- local kernel repair
- implementation changes required for K1 diagnosis or improvement
- smoke and formal K1 runs
- artifact analysis

Not allowed by default:
- automatic entry into `K=4`
- treating Mercury validation as the main line

### [READS:argon_k1_inner]
Before acting, read:

- current state
- latest stage summary for the most recent K1 run
- latest review summary if it exists
- latest fit diagnostics if they exist
- fit plots for weak curves

### [FOCUS:argon_k1_inner]
Prioritize weak curves:
- `Vr=0`
- `Vr=8`
- `Vr=10`

Priority order:
1. `Vr=0`
2. `Vr=8`
3. `Vr=10`

### [VERIFY:argon_k1_inner.loop]
For local iteration quality, inspect:
- `rmse`
- `raw_mse`
- `env_mse`
- `osc_mse`
- peak counts / valley counts
- peak centers / valley centers
- mean peak-valley contrast

Do not use global RMSE alone as the decision basis.

### [EXIT:argon_k1_inner]
This stage may exit into `k1_ready_review` only after:
- a formal K1 run exists,
- the stage summary exists,
- the required fit artifacts exist,
- the run has been analyzed and recorded in memory.

### [MEMORY_WRITE:argon_k1_inner]
Required writes:
- one event after each diagnosis or execution step,
- one snapshot after a completed single-round K1 cycle,
- state update after every formal run and after every stage summary judgment.

---

## [PIPELINE:stage.k1_ready_review] Stage: K1 Ready Review

### [GOAL:k1_ready_review]
Decide whether the current K1 candidate is allowed to enter `K=4`.

### [READS:k1_ready_review]
Required inputs:
- the latest `stage_summary.json` from the K1 stage
- the configured ratio limit
- the baseline reference bundle

### [VERIFY:k1_ready_review]
Formal gate:
- `physics_sanity == true`
- `energy_sanity == true`
- `candidate_max_weak_curve_rmse <= reference_max_weak_curve_rmse * ratio_limit`

### [EXIT:k1_ready_review]
If the gate fails:
- stop downstream progression,
- record the failed gate as a memory event,
- remain in K1-oriented work.

If the gate passes:
- update state to allow `argon_k4_inner`.

### [MEMORY_WRITE:k1_ready_review]
Required write:
- one review event with the decision,
- optional snapshot if the decision changes the project trajectory.

---

## [PIPELINE:stage.argon_k4_inner] Stage: Argon K4 Inner Loop

### [GOAL:argon_k4_inner]
Run downstream Argon training after K1 promotion.

### [STATUS:argon_k4_inner]
This stage exists in the formal workflow but is not part of the active repair subflow by default.

### [VERIFY:argon_k4_inner]
Stage-local training verification should confirm:
- the stage summary exists,
- sanity checks pass,
- downstream artifact generation is complete enough for review.

### [EXIT:argon_k4_inner]
May advance to `outer_review` only when the local artifacts are sufficient for model-to-data review.

---

## [PIPELINE:stage.outer_review] Stage: Outer Review

### [GOAL:outer_review]
Perform the main structured review of local model-to-data agreement.

### [READS:outer_review]
Required inputs:
- latest K4 stage summary
- latest local feature scan summary
- latest Argon level scan summary

### [VERIFY:outer_review]
Primary gate:
- local feature scan exists and is interpretable
- the expected RMSE orders are present
- upstream sanity is still valid

Support-only evidence:
- Argon `K=1..6` level scan

### [EXIT:outer_review]
If outer review fails:
- stop before Mercury validation
- record the blocking reason in memory and state

If it passes:
- allow `hg_validation`

---

## [PIPELINE:stage.hg_validation] Stage: Mercury Validation

### [GOAL:hg_validation]
Validate the promoted architecture on Mercury using the accepted data contract.

### [READS:hg_validation]
Required inputs:
- the accepted Mercury processed dataset
- the promoted upstream candidate
- any configured validation defaults

### [VERIFY:hg_validation]
Validation must confirm:
- the accepted Mercury source policy was respected
- the run is tied to the shared physical core
- per-curve Mercury-specific variability remains within the intended design

### [EXIT:hg_validation]
A Mercury validation pass does not rewrite the full project specification by itself.  
It records a downstream validation result for the promoted family.

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
Analyze the latest available artifacts before changing code.

### [READS:artifact_analysis_pre]
Read, when present:
- `workflow_summary.json`
- `stage_summary.json`
- `review_summary.json`
- `fit_diagnostics.json`
- `fit_overview.png`
- `fit_curves/*.png`

### [VERIFY:artifact_analysis_pre]
The analysis must explicitly distinguish:
- envelope error
- oscillation error
- phase / event-center offset
- valley flattening risk

---

## [PIPELINE:subflow.problem_isolation] Active subflow: problem isolation

### [GOAL:problem_isolation]
Reduce the observed mismatch to the smallest actionable kernel problem statement.

### [OUTPUT:problem_isolation]
Produce one event that names:
- the dominant issue,
- the affected curves,
- the intended narrow repair target.

---

## [PIPELINE:subflow.minimal_repair_strategy] Active subflow: minimal K1 repair strategy

### [GOAL:minimal_repair_strategy]
Choose the smallest justified K1-only repair strategy.

### [RULE:minimal_repair_strategy]
Do not broaden to K4-only ideas during the active repair round.

### [OUTPUT:minimal_repair_strategy]
Record:
- what will change,
- what will not change,
- which failure mode is being targeted.

---

## [PIPELINE:subflow.coding] Active subflow: coding

### [GOAL:coding]
Implement the selected minimal repair.

### [VERIFY:coding]
Before formal training:
- code changes are coherent,
- affected files are known,
- the intended repair scope did not silently expand.

---

## [PIPELINE:subflow.k1_smoke] Active subflow: K1 smoke

### [GOAL:k1_smoke]
Run a low-cost smoke validation before a formal K1 run.

### [VERIFY:k1_smoke]
A smoke run must be sufficient to detect:
- broken execution,
- clearly invalid outputs,
- obvious artifact generation failure.

If smoke fails:
- remain in the current subflow,
- record a failure event,
- optionally archive invalid raw artifacts to `garbage/`.

---

## [PIPELINE:subflow.k1_formal] Active subflow: K1 formal

### [GOAL:k1_formal]
Run the formal K1 stage for the active round.

### [VERIFY:k1_formal]
The formal run should produce:
- stage summary
- fit diagnostics
- fit overview
- weak-curve fit plots
- any required scorecards or parameter summaries

---

## [PIPELINE:subflow.artifact_analysis_post] Active subflow: post-run artifact analysis

### [GOAL:artifact_analysis_post]
Analyze the new formal outputs and decide whether the round improved the target behavior.

### [VERIFY:artifact_analysis_post]
The analysis must explicitly check:
- weak-curve oscillation preservation
- valley depth
- phase alignment
- local feature quality
- whether any apparent gain was merely envelope smoothing

---

## [PIPELINE:subflow.round_summary] Active subflow: stop and summarize

### [GOAL:round_summary]
Stop after one completed round and summarize the result.

### [OUTPUT:round_summary]
Write:
- one stage snapshot
- one updated state file
- optional garbage records for retired noise

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

All machine-readable outputs must use repository-relative paths.  
Absolute local-machine paths are forbidden in generated state, memory, review, or workflow summaries.

---

## [PIPELINE:end] End of specification
