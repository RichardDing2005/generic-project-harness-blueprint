#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys

ANCHOR_RE = re.compile(r"\[([A-Z_]+:[A-Za-z0-9_.:-]+)\]")


def load_anchors(pipeline_path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in pipeline_path.read_text(encoding="utf-8").splitlines():
        for match in ANCHOR_RE.finditer(line):
            anchors.add(match.group(1))
    return anchors


def choose_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate state, pipeline anchors, config refs, and memory pointers.")
    parser.add_argument("--repo-root", default=None)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    pipeline_path = repo_root / "PIPELINE.md"
    state_path = choose_existing(repo_root / "state" / "CURRENT_STATE.json", repo_root / "state" / "CURRENT_STATE.example.json")
    memory_index_path = choose_existing(repo_root / "memory" / "index.json", repo_root / "memory" / "index.example.json")

    errors: list[str] = []
    warnings: list[str] = []

    if not pipeline_path.exists():
        print("ERROR: PIPELINE.md not found", file=sys.stderr)
        return 1
    if state_path is None:
        print("ERROR: no state file found", file=sys.stderr)
        return 1
    if memory_index_path is None:
        print("ERROR: no memory index file found", file=sys.stderr)
        return 1

    anchors = load_anchors(pipeline_path)
    state = json.loads(state_path.read_text(encoding="utf-8"))
    memory_index = json.loads(memory_index_path.read_text(encoding="utf-8"))

    current_anchor = state.get("current_pipeline_anchor")
    subflow_anchor = state.get("current_subflow_anchor")
    latest_snapshot_ref = state.get("latest_snapshot_ref")
    active_memory_refs = state.get("active_memory_refs", [])
    required_config_refs = state.get("required_config_refs", [])
    bootstrap_mode = bool(state.get("bootstrap_mode"))

    if current_anchor and current_anchor not in anchors:
        errors.append(f"Missing current_pipeline_anchor: {current_anchor}")
    if subflow_anchor and subflow_anchor not in anchors:
        errors.append(f"Missing current_subflow_anchor: {subflow_anchor}")

    for ref in required_config_refs:
        if not (repo_root / ref).exists():
            errors.append(f"Missing config file: {ref}")

    if latest_snapshot_ref:
        if not (repo_root / latest_snapshot_ref).exists():
            errors.append(f"Missing snapshot file: {latest_snapshot_ref}")
    elif not bootstrap_mode:
        errors.append("Normal mode requires latest_snapshot_ref")

    for ref in active_memory_refs:
        if not (repo_root / ref).exists():
            errors.append(f"Missing memory file: {ref}")

    index_snapshot = memory_index.get("active_snapshot")
    if latest_snapshot_ref and index_snapshot and latest_snapshot_ref != index_snapshot:
        warnings.append(
            f"STATE latest_snapshot_ref differs from memory/index.json active_snapshot: {latest_snapshot_ref} != {index_snapshot}"
        )

    state_event_set = set(active_memory_refs)
    index_event_set = set(memory_index.get("recent_events", []))
    if state_event_set and index_event_set and state_event_set != index_event_set:
        warnings.append("STATE active_memory_refs and memory/index.json recent_events differ; STATE remains authoritative.")

    payload = {
        "state_file": str(state_path.relative_to(repo_root)),
        "memory_index_file": str(memory_index_path.relative_to(repo_root)),
        "pipeline_file": str(pipeline_path.relative_to(repo_root)),
        "bootstrap_mode": bootstrap_mode,
        "errors": errors,
        "warnings": warnings,
        "valid": not errors,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
