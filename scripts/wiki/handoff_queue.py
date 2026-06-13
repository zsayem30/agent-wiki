#!/usr/bin/env python3
"""Inspect and acknowledge agent-wiki handoff queue entries."""

from __future__ import annotations

import argparse
import hashlib
import json
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
TERMINAL_STATUSES = {"acknowledged", "curated", "deferred", "rejected"}
VALID_STATUSES = {"pending", *TERMINAL_STATUSES}


def now_local() -> str:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    items: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            items.append(item)
    return items


def handoff_id(entry: dict[str, Any], index: int) -> str:
    raw = entry.get("id")
    return str(raw) if raw else f"legacy_{index + 1}"


def load_handoffs() -> list[dict[str, Any]]:
    handoffs = read_jsonl(INBOX)
    for index, entry in enumerate(handoffs):
        entry.setdefault("id", handoff_id(entry, index))
    return handoffs


def status_events() -> dict[str, str]:
    statuses: dict[str, str] = {}
    for event in read_jsonl(EVENTS):
        if event.get("type") != "handoff_status":
            continue
        handoff = event.get("handoff_id")
        status = event.get("curator_status")
        if isinstance(handoff, str) and isinstance(status, str):
            statuses[handoff] = status
    return statuses


def effective_status(entry: dict[str, Any], statuses: dict[str, str]) -> str:
    status = statuses.get(str(entry.get("id"))) or entry.get("curator_status") or "pending"
    return str(status)


def pending_handoffs(handoffs: list[dict[str, Any]], statuses: dict[str, str]) -> list[dict[str, Any]]:
    return [entry for entry in handoffs if effective_status(entry, statuses) not in TERMINAL_STATUSES]


def print_summary(entry: dict[str, Any], status: str) -> None:
    timestamp = entry.get("timestamp_utc") or entry.get("timestamp") or "unknown-time"
    summary = entry.get("summary") or "No summary provided."
    truth = entry.get("current_truth_changed", "unknown")
    changed = entry.get("changed", [])
    changed_count = len(changed) if isinstance(changed, list) else "?"
    print(f"{entry.get('id')}\t{status}\t{timestamp}\ttruth={truth}\tchanged={changed_count}\t{summary}")


def command_list(args: argparse.Namespace) -> None:
    handoffs = load_handoffs()
    statuses = status_events()
    selected = handoffs if args.all else pending_handoffs(handoffs, statuses)
    if not selected:
        print("No handoffs found." if args.all else "No pending handoffs found.")
        return
    for entry in selected:
        print_summary(entry, effective_status(entry, statuses))


def command_next(args: argparse.Namespace) -> None:
    handoffs = pending_handoffs(load_handoffs(), status_events())
    if not handoffs:
        print("No pending handoffs found.")
        return
    print(json.dumps(handoffs[0], indent=2, sort_keys=True))


def find_handoff(handoff: str) -> dict[str, Any]:
    for entry in load_handoffs():
        if entry.get("id") == handoff:
            return entry
    raise SystemExit(f"Unknown handoff: {handoff}")


def command_show(args: argparse.Namespace) -> None:
    print(json.dumps(find_handoff(args.handoff_id), indent=2, sort_keys=True))


def event_id(handoff: str, status: str, timestamp_utc: str) -> str:
    digest = hashlib.sha1(f"{handoff}:{status}:{timestamp_utc}".encode("utf-8")).hexdigest()[:7]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"event_{stamp}_{digest}"


def command_ack(args: argparse.Namespace) -> None:
    find_handoff(args.handoff_id)
    timestamp_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    event: dict[str, Any] = {
        "id": event_id(args.handoff_id, args.status, timestamp_utc),
        "timestamp": now_local(),
        "timestamp_utc": timestamp_utc,
        "type": "handoff_status",
        "handoff_id": args.handoff_id,
        "curator_status": args.status,
    }
    if args.note:
        event["note"] = args.note
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")
    print(json.dumps(event, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Accepted for host-root command symmetry; queue lives under this agent-wiki.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List pending handoffs.")
    list_parser.add_argument("--all", action="store_true", help="Include acknowledged, curated, deferred, and rejected handoffs.")
    list_parser.set_defaults(func=command_list)

    next_parser = subparsers.add_parser("next", help="Print the next pending handoff as JSON.")
    next_parser.set_defaults(func=command_next)

    show_parser = subparsers.add_parser("show", help="Print a handoff by ID as JSON.")
    show_parser.add_argument("handoff_id")
    show_parser.set_defaults(func=command_show)

    ack_parser = subparsers.add_parser("ack", help="Append a handoff status event.")
    ack_parser.add_argument("handoff_id")
    ack_parser.add_argument("--status", choices=sorted(VALID_STATUSES - {"pending"}), default="acknowledged")
    ack_parser.add_argument("--note", default="")
    ack_parser.set_defaults(func=command_ack)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
