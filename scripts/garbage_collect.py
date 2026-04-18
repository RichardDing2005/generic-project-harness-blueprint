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
        "project_name": "Generic_Project",
        "records": [],
    }


def safe_target(storage_dir: Path, rel_text: str) -> Path:
    rel_path = Path(rel_text)
    target = storage_dir / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    candidate = target
    counter = 1
    while candidate.exists():
        candidate = target.with_name(f"{target.stem}-{counter}{target.suffix}")
        counter += 1
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive obsolete files into garbage/ and append garbage index.")
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--retention-reason", required=True)
    parser.add_argument("--replacement-ref", default="")
    parser.add_argument("--derived-lesson-ref", default="")
    parser.add_argument("--superseded-by", default="")
    parser.add_argument("--can-restore", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("paths", nargs="+", help="Repository-relative paths to archive")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    garbage_root = repo_root / "garbage" / "records"
    index_path = repo_root / "garbage" / "index.json"
    garbage_root.mkdir(parents=True, exist_ok=True)
    index = load_index(index_path)

    record_id = f"GARBAGE-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"
    archived_paths: list[str] = []
    storage_dir = garbage_root / record_id

    if not args.dry_run:
        storage_dir.mkdir(parents=True, exist_ok=True)

    for rel_text in args.paths:
        src = (repo_root / rel_text).resolve()
        try:
            src.relative_to(repo_root)
        except ValueError:
            print(f"ERROR: path escapes repository root: {rel_text}", file=sys.stderr)
            return 1
        if not src.exists():
            print(f"WARNING: source not found, skipping: {rel_text}", file=sys.stderr)
            continue
        target = safe_target(storage_dir, rel_text)
        rel_target = target.relative_to(repo_root)
        archived_paths.append(str(rel_target).replace("\\", "/"))
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(target))

    if not archived_paths:
        print("ERROR: no files were archived", file=sys.stderr)
        return 1

    record = {
        "id": record_id,
        "archived_paths": archived_paths,
        "reason": args.reason,
        "retention_reason": args.retention_reason,
        "replacement_ref": args.replacement_ref,
        "derived_lesson_ref": args.derived_lesson_ref,
        "superseded_by": args.superseded_by,
        "can_restore": args.can_restore,
        "created_at": utc_now(),
    }

    if not args.dry_run:
        index["records"].append(record)
        index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({"dry_run": args.dry_run, "record": record}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
