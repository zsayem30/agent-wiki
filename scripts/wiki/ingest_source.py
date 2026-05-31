#!/usr/bin/env python3
"""Register a source document in knowledge/source_manifest.yaml."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "knowledge" / "source_manifest.yaml"


def now_local() -> str:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
    return datetime.now().astimezone().isoformat(timespec="seconds")


def slug_for(path: Path) -> str:
    stem = "_".join(path.with_suffix("").parts)
    stem = re.sub(r"[^A-Za-z0-9_]+", "_", stem).strip("_").lower()
    return stem or "source"


def already_registered(rel: str, text: str) -> bool:
    return f"path: {rel}" in text or f'path: "{rel}"' in text


def append_manifest(rel: str, kind: str, status: str, summary: str) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    text = MANIFEST.read_text(encoding="utf-8") if MANIFEST.exists() else "sources:\n"
    if already_registered(rel, text):
        print(f"Already registered: {rel}")
        return
    source_id = slug_for(Path(rel))
    timestamp = now_local()
    block = (
        f"  - id: {source_id}\n"
        f"    path: {rel}\n"
        f"    kind: {kind}\n"
        f"    status: {status}\n"
        f"    summary: {summary!r}\n"
        f"    added: {timestamp}\n"
        f"    last_reviewed: null\n"
    )
    if not text.endswith("\n"):
        text += "\n"
    MANIFEST.write_text(text + block, encoding="utf-8")
    print(f"Registered {rel} as {source_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Source path to register.")
    parser.add_argument("--kind", default="source", help="plan, idea, paper, report, external, source.")
    parser.add_argument("--status", default="new", help="new, active, background, archived, superseded.")
    parser.add_argument("--summary", default="TODO", help="Short source summary.")
    args = parser.parse_args()

    path = (ROOT / args.path).resolve()
    try:
        rel = path.relative_to(ROOT).as_posix()
    except ValueError:
        raise SystemExit("Source must be inside the repository.")
    if not path.exists():
        raise SystemExit(f"Missing source: {rel}")
    append_manifest(rel, args.kind, args.status, args.summary)


if __name__ == "__main__":
    main()

