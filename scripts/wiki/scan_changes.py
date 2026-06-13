#!/usr/bin/env python3
"""Record host-project changes as a curator handoff."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


WIKI_ROOT = Path(__file__).resolve().parents[2]
INBOX = WIKI_ROOT / "knowledge" / "change_inbox.jsonl"
EVENTS = WIKI_ROOT / "knowledge" / "events.jsonl"

VALID_KINDS = {
    "manual_scan",
    "implementation",
    "research",
    "debug",
    "experiment",
    "report",
    "audit",
    "other",
}
VALID_TRUTH_IMPACTS = {"yes", "no", "unknown"}
VALID_CURATOR_STATUSES = {"pending", "acknowledged", "curated", "deferred", "rejected"}


def now_local() -> str:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
    return datetime.now().astimezone().isoformat(timespec="seconds")


def timestamp_pair() -> tuple[str, str, str]:
    utc_now = datetime.now(timezone.utc)
    return now_local(), utc_now.isoformat(timespec="seconds"), utc_now.strftime("%Y%m%d_%H%M%S")


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


def run_git(project_root: Path, args: list[str], input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=project_root,
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return subprocess.CompletedProcess(["git", *args], 127, "", str(exc))


def git_output(project_root: Path, args: list[str]) -> str | None:
    result = run_git(project_root, args)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def git_repo_root(project_root: Path) -> str | None:
    return git_output(project_root, ["rev-parse", "--show-toplevel"])


def run_git_status(project_root: Path) -> list[dict[str, str]]:
    result = run_git(project_root, ["status", "--short"])
    if result.returncode != 0:
        return []
    changed: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        status = line[:2].strip() or "?"
        path = line[3:].strip()
        item = {"path": path, "status": status}
        if " -> " in path:
            old_path, new_path = path.split(" -> ", 1)
            item = {"path": new_path, "old_path": old_path, "status": status}
        changed.append(item)
    return changed


def parse_name_status(text: str) -> list[dict[str, str]]:
    changed: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        if len(parts) >= 3 and status[:1] in {"R", "C"}:
            changed.append({"path": parts[2], "old_path": parts[1], "status": status})
        elif len(parts) >= 2:
            changed.append({"path": parts[1], "status": status})
    return changed


def changed_for_commit(project_root: Path, commit: str) -> list[dict[str, str]]:
    result = run_git(project_root, ["show", "--name-status", "--format=", commit])
    if result.returncode != 0:
        raise SystemExit(f"Unable to inspect commit {commit!r}: {result.stderr.strip()}")
    return parse_name_status(result.stdout)


def stat_lines(text: str) -> list[str]:
    return [line.rstrip() for line in text.splitlines() if line.strip()]


def worktree_diff_stat(project_root: Path) -> list[str]:
    lines: list[str] = []
    for args in (["diff", "--stat", "--no-ext-diff"], ["diff", "--cached", "--stat", "--no-ext-diff"]):
        result = run_git(project_root, args)
        if result.returncode == 0 and result.stdout.strip():
            lines.extend(stat_lines(result.stdout))
    return lines


def commit_diff_stat(project_root: Path, commit: str) -> list[str]:
    result = run_git(project_root, ["show", "--stat", "--format=", "--no-ext-diff", commit])
    if result.returncode != 0:
        raise SystemExit(f"Unable to inspect commit stat {commit!r}: {result.stderr.strip()}")
    return stat_lines(result.stdout)


def parse_trailers(project_root: Path, message: str) -> dict[str, list[str]]:
    result = run_git(project_root, ["interpret-trailers", "--parse"], input_text=message)
    text = result.stdout if result.returncode == 0 and result.stdout.strip() else ""
    trailers: dict[str, list[str]] = {}
    for line in text.splitlines():
        key, sep, value = line.partition(":")
        if not sep:
            continue
        trailers.setdefault(key.strip(), []).append(value.strip())
    return trailers


def commit_metadata(project_root: Path, commit: str) -> dict[str, Any]:
    sha = git_output(project_root, ["rev-parse", "--verify", f"{commit}^{{commit}}"])
    if not sha:
        raise SystemExit(f"Unknown commit: {commit}")
    subject = git_output(project_root, ["show", "-s", "--format=%s", sha]) or ""
    author = git_output(project_root, ["show", "-s", "--format=%an <%ae>", sha]) or ""
    date = git_output(project_root, ["show", "-s", "--format=%aI", sha]) or ""
    body = git_output(project_root, ["show", "-s", "--format=%B", sha]) or ""
    return {
        "sha": sha,
        "ref": commit,
        "subject": subject,
        "author": author,
        "date": date,
        "trailers": parse_trailers(project_root, body),
    }


def trailer_lookup(trailers: dict[str, list[str]], *names: str) -> list[str]:
    wanted = {name.lower() for name in names}
    values: list[str] = []
    for key, found in trailers.items():
        if key.lower() in wanted:
            values.extend(found)
    return values


def split_values(values: list[str], *, split: bool = True) -> list[str]:
    out: list[str] = []
    for value in values:
        pieces = [value]
        if split:
            pieces = value.replace(";", ",").split(",")
        for piece in pieces:
            piece = piece.strip()
            if piece and piece not in out:
                out.append(piece)
    return out


def truth_impact_from_trailers(trailers: dict[str, list[str]]) -> str | None:
    values = trailer_lookup(trailers, "Truth-Change", "Truth-Impact", "Current-Truth-Changed")
    if not values:
        return None
    value = values[-1].strip().lower()
    return value if value in VALID_TRUTH_IMPACTS else None


def collect_git_metadata(project_root: Path, commit: str | None) -> dict[str, Any]:
    available = git_repo_root(project_root) is not None
    if not available:
        if commit:
            raise SystemExit("--commit requires project-root to be inside a Git repository.")
        return {
            "available": False,
            "branch": None,
            "head": None,
            "commit": None,
            "is_dirty": False,
            "changed": [],
            "diff_stat": [],
        }

    branch = git_output(project_root, ["branch", "--show-current"])
    if not branch:
        branch = git_output(project_root, ["rev-parse", "--abbrev-ref", "HEAD"])
    head = git_output(project_root, ["rev-parse", "HEAD"])
    worktree_changed = run_git_status(project_root)
    commit_info = commit_metadata(project_root, commit) if commit else None
    changed = changed_for_commit(project_root, commit) if commit else worktree_changed
    diff_stat = commit_diff_stat(project_root, commit) if commit else worktree_diff_stat(project_root)

    return {
        "available": True,
        "branch": branch,
        "head": head,
        "commit": commit_info,
        "is_dirty": bool(worktree_changed),
        "changed": changed,
        "diff_stat": diff_stat,
    }


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


def stable_id(prefix: str, stamp: str, payload: dict[str, Any]) -> str:
    digest = hashlib.sha1(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:7]
    return f"{prefix}_{stamp}_{digest}"


def make_entry(args: argparse.Namespace, project_root: Path) -> dict[str, Any]:
    timestamp, timestamp_utc, stamp = timestamp_pair()
    git = collect_git_metadata(project_root, args.commit or None)
    trailers = git.get("commit", {}).get("trailers", {}) if git.get("commit") else {}
    changed = git["changed"]
    evidence = split_values(args.evidence + trailer_lookup(trailers, "Evidence"))
    verification = split_values(args.verification + trailer_lookup(trailers, "Verification"))
    open_questions = split_values(args.open_question + trailer_lookup(trailers, "Open-Question"), split=False)
    routes = suggest_routes(changed, project_root)
    routes.extend(split_values(args.suggested_routes + trailer_lookup(trailers, "Routes", "Route")))
    routes = sorted(dict.fromkeys(routes))
    truth_impact = args.truth_impact
    if truth_impact == "unknown":
        truth_impact = truth_impact_from_trailers(trailers) or truth_impact

    entry: dict[str, Any] = {
        "timestamp": timestamp,
        "timestamp_utc": timestamp_utc,
        "kind": args.kind,
        "summary": args.summary,
        "project_root": str(project_root),
        "agent_wiki_root": str(WIKI_ROOT),
        "git": git,
        "changed": changed,
        "evidence": evidence,
        "verification": verification,
        "suggested_routes": routes,
        "current_truth_changed": truth_impact,
        "open_questions": open_questions,
        "curator_status": args.curator_status,
    }
    entry["id"] = stable_id(
        "handoff",
        stamp,
        {
            "timestamp_utc": timestamp_utc,
            "summary": args.summary,
            "project_root": str(project_root),
            "git_head": git.get("head"),
            "git_commit": git.get("commit", {}).get("sha") if git.get("commit") else None,
            "changed": changed,
            "evidence": evidence,
            "verification": verification,
            "current_truth_changed": truth_impact,
            "suggested_routes": routes,
            "open_questions": open_questions,
        },
    )
    return entry


def append_entry(entry: dict[str, object]) -> None:
    INBOX.parent.mkdir(parents=True, exist_ok=True)
    with INBOX.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def append_event(event: dict[str, object]) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")


def make_handoff_event(entry: dict[str, Any]) -> dict[str, Any]:
    timestamp, timestamp_utc, stamp = timestamp_pair()
    git = entry.get("git", {}) if isinstance(entry.get("git"), dict) else {}
    changed = git.get("changed", []) if isinstance(git.get("changed"), list) else []
    event: dict[str, Any] = {
        "timestamp": timestamp,
        "timestamp_utc": timestamp_utc,
        "type": "handoff_created",
        "handoff_id": entry.get("id"),
        "summary": entry.get("summary", ""),
        "project_root": entry.get("project_root", ""),
        "agent_wiki_root": entry.get("agent_wiki_root", str(WIKI_ROOT)),
        "current_truth_changed": entry.get("current_truth_changed", "unknown"),
        "curator_status": entry.get("curator_status", "pending"),
        "suggested_routes": entry.get("suggested_routes", []),
        "git": {
            "branch": git.get("branch"),
            "head": git.get("head"),
            "is_dirty": git.get("is_dirty"),
            "changed_count": len(changed),
        },
    }
    event["id"] = stable_id(
        "event",
        stamp,
        {"type": "handoff_created", "handoff_id": event["handoff_id"], "timestamp_utc": timestamp_utc},
    )
    return event


def once(args: argparse.Namespace, project_root: Path) -> dict[str, object]:
    entry = make_entry(args, project_root)
    if not args.dry_run:
        append_entry(entry)
        if not args.no_event:
            append_event(make_handoff_event(entry))
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default="", help="Host project root. Use '.' from host root.")
    parser.add_argument("--summary", default="Manual scan for curator review.")
    parser.add_argument("--kind", default="manual_scan", choices=sorted(VALID_KINDS))
    parser.add_argument("--commit", default="", help="Optional commit SHA/ref to scan instead of the worktree.")
    parser.add_argument("--evidence", action="append", default=[], help="Evidence path or note. Can be repeated.")
    parser.add_argument("--verification", action="append", default=[], help="Verification evidence. Can be repeated.")
    parser.add_argument(
        "--truth-impact",
        default="unknown",
        choices=sorted(VALID_TRUTH_IMPACTS),
        help="Whether current project truth changed: yes, no, or unknown.",
    )
    parser.add_argument(
        "--suggested-route",
        "--route",
        dest="suggested_routes",
        action="append",
        default=[],
        help="Additional wiki route for curator review. Can be repeated.",
    )
    parser.add_argument("--open-question", action="append", default=[], help="Open question for curator review. Can be repeated.")
    parser.add_argument("--curator-status", default="pending", choices=sorted(VALID_CURATOR_STATUSES))
    parser.add_argument("--no-event", action="store_true", help="Do not emit a handoff_created event.")
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
                entry = make_entry(args, project_root)
                if not args.dry_run:
                    append_entry(entry)
                    if not args.no_event:
                        append_event(make_handoff_event(entry))
                print(json.dumps(entry, indent=2, sort_keys=True))
                previous = signature
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    main()
