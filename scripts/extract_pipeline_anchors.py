#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import sys

ANCHOR_RE = re.compile(r"\[([A-Z_]+:[A-Za-z0-9_.:-]+)\]")

def main() -> int:
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    pipeline_path = repo_root / "PIPELINE.md"
    if not pipeline_path.exists():
        print(f"PIPELINE.md not found at {pipeline_path}", file=sys.stderr)
        return 1

    anchors = []
    for lineno, line in enumerate(pipeline_path.read_text(encoding="utf-8").splitlines(), start=1):
        for match in ANCHOR_RE.finditer(line):
            anchors.append({"anchor": match.group(1), "line": lineno})

    print(json.dumps({
        "pipeline_path": str(pipeline_path.relative_to(repo_root)),
        "anchor_count": len(anchors),
        "anchors": anchors,
    }, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
