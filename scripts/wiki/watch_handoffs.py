#!/usr/bin/env python3
"""Watch agent-wiki handoff events and notify a curator terminal."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path
from typing import Any


WIKI_ROOT = Path(__file__).resolve().parents[2]
EVENTS = WIKI_ROOT / "knowledge" / "events.jsonl"


def read_events(offset: int = 0) -> tuple[list[dict[str, Any]], int]:
    if not EVENTS.exists():
        return [], 0
    text = EVENTS.read_text(encoding="utf-8", errors="replace")
    if offset > len(text):
        offset = 0
    events: list[dict[str, Any]] = []
    for line in text[offset:].splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events, len(text)


def handoff_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [event for event in events if event.get("type") == "handoff_created"]


def notify_macos(title: str, message: str) -> None:
    result = subprocess.run(
        ["osascript", "-e", f'display notification {json.dumps(message)} with title {json.dumps(title)}'],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"macOS notification failed: {result.stderr.strip()}")


def print_handoff(event: dict[str, Any], *, bell: bool, notify: str, tmux_pane: str) -> None:
    if bell:
        print("\a", end="")
    handoff_id = event.get("handoff_id") or "unknown"
    summary = event.get("summary") or "No summary provided."
    truth = event.get("current_truth_changed", "unknown")
    routes = event.get("suggested_routes", [])
    git = event.get("git", {}) if isinstance(event.get("git"), dict) else {}

    print("New agent-wiki handoff")
    print(f"- id: {handoff_id}")
    print(f"- summary: {summary}")
    print(f"- truth impact: {truth}")
    if git:
        print(f"- git: branch={git.get('branch')} head={git.get('head')} dirty={git.get('is_dirty')}")
    if routes:
        print("- suggested routes:")
        for route in routes:
            print(f"  - {route}")
    print("- curator command: /wiki-review-next")
    print(f"- CLI: python scripts/wiki/handoff_queue.py show {handoff_id}")

    if notify == "macos":
        notify_macos("agent-wiki handoff", str(summary))
    if tmux_pane:
        print(
            f"tmux pane {tmux_pane} was not modified. "
            "Prompt injection requires an explicit idle/lock signal; run /wiki-review-next manually."
        )


def once(args: argparse.Namespace) -> None:
    events, _ = read_events()
    handoffs = handoff_events(events)
    if not handoffs:
        print(f"No handoff_created events found in {EVENTS}.")
        return
    print_handoff(handoffs[-1], bell=args.bell, notify=args.notify, tmux_pane=args.tmux_pane)


def watch(args: argparse.Namespace) -> None:
    _, offset = read_events()
    print(f"Watching {EVENTS} every {args.interval:g}s. Press Ctrl-C to stop.")
    try:
        while True:
            events, offset = read_events(offset)
            for event in handoff_events(events):
                print_handoff(event, bell=args.bell, notify=args.notify, tmux_pane=args.tmux_pane)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Stopped.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Accepted for symmetry with scan_changes.py; events live under this agent-wiki.")
    parser.add_argument("--once", action="store_true", help="Print the latest handoff event and exit.")
    parser.add_argument("--interval", type=float, default=5.0, help="Polling interval in seconds.")
    parser.add_argument("--notify", choices=["none", "macos"], default="none", help="Optional desktop notification backend.")
    parser.add_argument("--no-bell", dest="bell", action="store_false", help="Suppress terminal bell.")
    parser.add_argument("--tmux-pane", default="", help="Advanced placeholder; prints safe instructions instead of injecting text.")
    parser.set_defaults(bell=True)
    args = parser.parse_args()

    if args.once:
        once(args)
    else:
        watch(args)


if __name__ == "__main__":
    main()
