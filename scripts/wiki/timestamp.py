#!/usr/bin/env python3
"""Print a project-local ISO-8601 timestamp."""

from __future__ import annotations

from datetime import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


def local_now() -> datetime:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Vancouver"))
    return datetime.now().astimezone()


def main() -> None:
    print(local_now().isoformat(timespec="seconds"))


if __name__ == "__main__":
    main()

