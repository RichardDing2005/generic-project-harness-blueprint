#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone
import shutil
import sys

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def load_index(index_path: Path) -> dict:
    if index_path.exists():
        return json.loads(index_path.read_text(encoding="utf-8"))
    return {
        "schema_version": "1.0.0",
        "project_name": "Research_Workspace",
        "records": []
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Archive obsolete files into garbage/ and append garbage index.")
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--replacement-ref", default="")
    parser.add_argument("paths", nargs="+", help="Repository-relative paths to archive")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    garbage_root = repo_root / "garbage" / "records"
    garbage_root.mkdir(parents=True, exist_ok=True)
    index_path = repo_root / "garbage" / "index.json"
    index = load_index(index_path)

    record_id = f"GARBAGE-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"
    archived_paths: list[str] = []
    storage_dir = garbage_root / record_id
    storage_dir.mkdir(parents=True, exist_ok=True)

    for rel_text in args.paths:
        src = repo_root / rel_text
        if not src.exists():
            print(f"WARNING: source not found, skipping: {rel_text}", file=sys.stderr)
            continue
        target = storage_dir / src.name
        shutil.move(str(src), str(target))
        archived_paths.append(str(target.relative_to(repo_root)).replace("\\", "/"))

    record = {
        "id": record_id,
        "archived_paths": archived_paths,
        "reason": args.reason,
        "replacement_ref": args.replacement_ref,
        "created_at": utc_now()
    }
    index["records"].append(record)
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
