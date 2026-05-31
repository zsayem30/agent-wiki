#!/usr/bin/env python3
"""Create a dated report from templates/report.md."""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "report.md"
REPORTS = ROOT / "sources" / "reports"
REGISTRY = ROOT / "knowledge" / "report_registry.yaml"


def now_local() -> str:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
    return datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "project_report"


def append_registry(rel: str, title: str, kind: str) -> None:
    text = REGISTRY.read_text(encoding="utf-8") if REGISTRY.exists() else "reports: []\n"
    if "reports: []" in text:
        text = text.replace("reports: []", "reports:")
    if not text.endswith("\n"):
        text += "\n"
    report_id = slugify(Path(rel).stem)
    block = (
        f"  - id: {report_id}\n"
        f"    path: {rel}\n"
        f"    kind: {kind}\n"
        f"    status: draft\n"
        f"    title: {title!r}\n"
        f"    created: {now_local()}\n"
        f"    evidence: []\n"
    )
    REGISTRY.write_text(text + block, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Report title or slug.")
    parser.add_argument("--kind", default="project_report")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    REPORTS.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    slug = slugify(args.title)
    path = REPORTS / f"{today}_{slug}.md"
    if path.exists() and not args.force:
        raise SystemExit(f"Report already exists: {path.relative_to(ROOT)}")

    template = TEMPLATE.read_text(encoding="utf-8")
    created = now_local()
    title = args.title.replace("_", " ").title()
    content = (
        template.replace("created: TODO", f"created: {created}")
        .replace("last_reviewed: TODO", f"last_reviewed: {created}")
        .replace("summary: TODO", f"summary: {title}")
        .replace("# Project Report: Title", f"# Project Report: {title}")
        .replace("Date: TODO", f"Date: {created}")
    )
    path.write_text(content, encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    append_registry(rel, title, args.kind)
    print(f"Wrote {rel}")


if __name__ == "__main__":
    main()

