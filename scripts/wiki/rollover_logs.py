#!/usr/bin/env python3
"""Identify or roll over long active logs."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


ROOT = Path(__file__).resolve().parents[2]
ACTIVE = ROOT / "wiki" / "logs" / "active"
ARCHIVE = ROOT / "wiki" / "logs" / "archive"


def stamp() -> str:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Vancouver")).strftime("%Y%m%d_%H%M%S")
    return datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold", type=int, default=800)
    parser.add_argument("--apply", action="store_true", help="Archive long logs and create fresh active logs.")
    args = parser.parse_args()

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    long_logs = []
    for path in sorted(ACTIVE.glob("*.md")):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(lines) > args.threshold:
            long_logs.append((path, len(lines)))

    if not long_logs:
        print(f"No active logs exceed {args.threshold} lines.")
        return

    for path, count in long_logs:
        print(f"{path.relative_to(ROOT)} has {count} lines.")
        if not args.apply:
            continue
        archived = ARCHIVE / f"{path.stem}_{stamp()}.md"
        path.rename(archived)
        path.write_text(
            "# Active Project Log\n\n"
            "Newest first. Previous entries archived at "
            f"`{archived.relative_to(ROOT).as_posix()}`.\n\n"
            "## TODO Timestamp\n\n"
            "Status: active\n\n"
            "Summary: Continue logging newest-first entries here.\n",
            encoding="utf-8",
        )
        print(f"Archived to {archived.relative_to(ROOT)}")

    if not args.apply:
        print("Run with --apply to archive long logs.")


if __name__ == "__main__":
    main()

