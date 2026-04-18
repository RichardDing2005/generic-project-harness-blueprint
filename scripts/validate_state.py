#!/usr/bin/env python3
from __future__ import annotations

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

def main() -> int:
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    pipeline_path = repo_root / "PIPELINE.md"
    state_path = repo_root / "state" / "CURRENT_STATE.example.json"

    if not pipeline_path.exists():
        print("ERROR: PIPELINE.md not found", file=sys.stderr)
        return 1
    if not state_path.exists():
        print("ERROR: state/CURRENT_STATE.example.json not found", file=sys.stderr)
        return 1

    anchors = load_anchors(pipeline_path)
    state = json.loads(state_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    current_anchor = state.get("current_pipeline_anchor", "")
    subflow_anchor = state.get("current_subflow_anchor", "")
    latest_snapshot_ref = state.get("latest_snapshot_ref", "")
    active_memory_refs = state.get("active_memory_refs", [])

    if current_anchor and current_anchor not in anchors:
        errors.append(f"Missing current_pipeline_anchor: {current_anchor}")
    if subflow_anchor and subflow_anchor not in anchors:
        errors.append(f"Missing current_subflow_anchor: {subflow_anchor}")

    if latest_snapshot_ref:
        if not (repo_root / latest_snapshot_ref).exists():
            errors.append(f"Missing snapshot file: {latest_snapshot_ref}")

    for ref in active_memory_refs:
        if not (repo_root / ref).exists():
            errors.append(f"Missing memory file: {ref}")

    payload = {
        "state_file": str(state_path.relative_to(repo_root)),
        "pipeline_file": str(pipeline_path.relative_to(repo_root)),
        "errors": errors,
        "valid": not errors
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
