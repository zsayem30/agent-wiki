#!/usr/bin/env python3
"""Record host-project changes as a curator handoff."""

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


WIKI_ROOT = Path(__file__).resolve().parents[2]
INBOX = WIKI_ROOT / "knowledge" / "change_inbox.jsonl"


def now_local() -> str:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
    return datetime.now().astimezone().isoformat(timespec="seconds")


def resolve_project_root(value: str | None) -> Path:
    if value:
        return Path(value).resolve()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=WIKI_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip()).resolve()
    except OSError:
        pass
    return WIKI_ROOT


def run_git_status(project_root: Path) -> list[dict[str, str]]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=project_root,
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


def wiki_prefix(project_root: Path) -> str:
    try:
        return WIKI_ROOT.relative_to(project_root).as_posix().strip("/")
    except ValueError:
        return ""


def strip_wiki_prefix(path: str, prefix: str) -> str:
    if prefix and path.startswith(prefix + "/"):
        return path[len(prefix) + 1 :]
    return path


def suggest_routes(changed: list[dict[str, str]], project_root: Path) -> list[str]:
    routes: set[str] = set()
    prefix = wiki_prefix(project_root)
    for item in changed:
        path = item["path"]
        local = strip_wiki_prefix(path, prefix)
        in_wiki = local != path or not prefix
        if in_wiki and local.startswith("sources/papers/"):
            routes.add("agent-wiki/wiki/topics/literature.md")
            routes.add("agent-wiki/knowledge/paper_registry.yaml")
        elif in_wiki and local.startswith("sources/plans/"):
            routes.add("agent-wiki/wiki/plans/active_plan.md")
        elif in_wiki and local.startswith("sources/ideas/"):
            routes.add("agent-wiki/wiki/topics/project_overview.md")
            routes.add("agent-wiki/wiki/OPEN_QUESTIONS.md")
        elif in_wiki and local.startswith("sources/reports/"):
            routes.add("agent-wiki/wiki/reports/REPORT_INDEX.md")
            routes.add("agent-wiki/knowledge/report_registry.yaml")
        elif in_wiki and local.startswith("wiki/"):
            routes.add("agent-wiki/wiki/CURRENT_STATE.md")
        elif in_wiki and local.startswith("knowledge/"):
            routes.add("agent-wiki/wiki/ROUTING_TABLE.md")
        elif path.startswith(("results/", "figures/")):
            routes.add("agent-wiki/knowledge/experiment_registry.yaml")
        elif path.endswith((".py", ".rs", ".cpp", ".c", ".h", ".ts", ".tsx", ".js")) or path.startswith(("src/", "scripts/", "experiments/")):
            routes.add("agent-wiki/wiki/PROJECT_MAP.md")
            routes.add("agent-wiki/wiki/plans/active_plan.md")
    if not routes:
        routes.add("agent-wiki/wiki/CURRENT_STATE.md")
    return sorted(routes)


def make_entry(summary: str, kind: str, project_root: Path) -> dict[str, object]:
    changed = run_git_status(project_root)
    return {
        "timestamp": now_local(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "kind": kind,
        "summary": summary,
        "project_root": str(project_root),
        "agent_wiki_root": str(WIKI_ROOT),
        "changed": changed,
        "suggested_routes": suggest_routes(changed, project_root),
        "current_truth_changed": "unknown",
        "open_questions": [],
    }


def append_entry(entry: dict[str, object]) -> None:
    INBOX.parent.mkdir(parents=True, exist_ok=True)
    with INBOX.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def once(args: argparse.Namespace, project_root: Path) -> dict[str, object]:
    entry = make_entry(args.summary, args.kind, project_root)
    if not args.dry_run:
        append_entry(entry)
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default="", help="Host project root. Use '.' from host root.")
    parser.add_argument("--summary", default="Manual scan for curator review.")
    parser.add_argument("--kind", default="manual_scan")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--watch", action="store_true", help="Keep scanning for changed status.")
    parser.add_argument("--interval", type=float, default=15.0)
    args = parser.parse_args()

    project_root = resolve_project_root(args.project_root or None)

    if not args.watch:
        entry = once(args, project_root)
        print(json.dumps(entry, indent=2, sort_keys=True))
        return

    previous = None
    print(f"Watching {project_root} for changes every {args.interval:g}s. Press Ctrl-C to stop.")
    try:
        while True:
            changed = run_git_status(project_root)
            signature = json.dumps(changed, sort_keys=True)
            if changed and signature != previous:
                entry = make_entry(args.summary, args.kind, project_root)
                if not args.dry_run:
                    append_entry(entry)
                print(json.dumps(entry, indent=2, sort_keys=True))
                previous = signature
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    main()
