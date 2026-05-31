#!/usr/bin/env python3
"""Record repository changes as a curator handoff."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


ROOT = Path(__file__).resolve().parents[2]
INBOX = ROOT / "knowledge" / "change_inbox.jsonl"


def now_local() -> str:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
    return datetime.now().astimezone().isoformat(timespec="seconds")


def run_git_status() -> list[dict[str, str]]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    changed: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        status = line[:2].strip() or "?"
        path = line[3:].strip()
        changed.append({"path": path, "status": status})
    return changed


def suggest_routes(changed: list[dict[str, str]]) -> list[str]:
    routes: set[str] = set()
    for item in changed:
        path = item["path"]
        if path.startswith("sources/papers/"):
            routes.add("wiki/topics/literature.md")
            routes.add("knowledge/paper_registry.yaml")
        elif path.startswith("sources/plans/"):
            routes.add("wiki/plans/active_plan.md")
        elif path.startswith("sources/ideas/"):
            routes.add("wiki/topics/project_overview.md")
            routes.add("wiki/OPEN_QUESTIONS.md")
        elif path.startswith("sources/reports/"):
            routes.add("wiki/reports/REPORT_INDEX.md")
            routes.add("knowledge/report_registry.yaml")
        elif path.startswith("results/"):
            routes.add("knowledge/experiment_registry.yaml")
        elif path.startswith("wiki/"):
            routes.add("wiki/CURRENT_STATE.md")
        elif path.startswith("knowledge/"):
            routes.add("wiki/ROUTING_TABLE.md")
        elif path.endswith(".py") or path.startswith(("src/", "scripts/", "experiments/")):
            routes.add("wiki/PROJECT_MAP.md")
            routes.add("wiki/plans/active_plan.md")
    if not routes:
        routes.add("wiki/CURRENT_STATE.md")
    return sorted(routes)


def make_entry(summary: str, kind: str) -> dict[str, object]:
    changed = run_git_status()
    return {
        "timestamp": now_local(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "kind": kind,
        "summary": summary,
        "changed": changed,
        "suggested_routes": suggest_routes(changed),
        "current_truth_changed": "unknown",
        "open_questions": [],
    }


def append_entry(entry: dict[str, object]) -> None:
    INBOX.parent.mkdir(parents=True, exist_ok=True)
    with INBOX.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def once(args: argparse.Namespace) -> dict[str, object]:
    entry = make_entry(args.summary, args.kind)
    if not args.dry_run:
        append_entry(entry)
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", default="Manual scan for curator review.")
    parser.add_argument("--kind", default="manual_scan")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--watch", action="store_true", help="Keep scanning for changed status.")
    parser.add_argument("--interval", type=float, default=15.0)
    args = parser.parse_args()

    if not args.watch:
        entry = once(args)
        print(json.dumps(entry, indent=2, sort_keys=True))
        return

    previous = None
    print(f"Watching for changes every {args.interval:g}s. Press Ctrl-C to stop.")
    try:
        while True:
            changed = run_git_status()
            signature = json.dumps(changed, sort_keys=True)
            if changed and signature != previous:
                entry = make_entry(args.summary, args.kind)
                if not args.dry_run:
                    append_entry(entry)
                print(json.dumps(entry, indent=2, sort_keys=True))
                previous = signature
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    main()

