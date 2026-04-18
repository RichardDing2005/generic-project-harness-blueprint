#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: dict, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize or reset bootstrap runtime files.")
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--project-name", default="Generic_Project")
    parser.add_argument("--force", action="store_true", help="Overwrite existing runtime files.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    now = utc_now()

    state = {
        "schema_version": "1.0.0",
        "project_name": args.project_name,
        "candidate_name": "",
        "bootstrap_mode": True,
        "formal_stage": "bootstrap",
        "active_subflow_stage": None,
        "current_pipeline_anchor": "PIPELINE:bootstrap",
        "current_subflow_anchor": None,
        "latest_snapshot_ref": None,
        "active_memory_refs": [],
        "required_artifact_refs": [],
        "required_config_refs": ["config/stage_defaults.json"],
        "last_verification": {
            "status": "bootstrap",
            "source": "bootstrap initialization",
            "checked_at": now,
        },
        "blocked": False,
        "blocking_reason": "",
        "next_action": "Survey the repository, determine the first formal stage, and write the first memory event before leaving bootstrap mode.",
        "updated_at": now,
    }

    memory_index = {
        "schema_version": "1.0.0",
        "project_name": args.project_name,
        "active_snapshot": None,
        "recent_events": [],
        "garbage_policy_version": "1.0.0",
        "updated_at": now,
    }

    garbage_index = {
        "schema_version": "1.0.0",
        "project_name": args.project_name,
        "records": [],
    }

    config_example = repo_root / "config" / "stage_defaults.example.json"
    config_actual = repo_root / "config" / "stage_defaults.json"
    if (not config_actual.exists()) or args.force:
        if config_example.exists():
            config_actual.write_text(config_example.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            config_actual.write_text("{}\n", encoding="utf-8")

    write_json(repo_root / "state" / "CURRENT_STATE.json", state, args.force)
    write_json(repo_root / "memory" / "index.json", memory_index, args.force)
    write_json(repo_root / "garbage" / "index.json", garbage_index, args.force)

    summary = {
        "repo_root": str(repo_root),
        "project_name": args.project_name,
        "wrote": [
            "state/CURRENT_STATE.json",
            "memory/index.json",
            "garbage/index.json",
            "config/stage_defaults.json",
        ],
        "force": args.force,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
