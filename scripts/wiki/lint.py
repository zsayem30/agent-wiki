#!/usr/bin/env python3
"""Lightweight lint checks for the agent-wiki scaffold."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


WIKI_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "USER_PROMPT_GUIDE.md",
    "wiki/START_HERE.md",
    "wiki/CURRENT_STATE.md",
    "wiki/ROUTING_TABLE.md",
    "wiki/OPEN_QUESTIONS.md",
    "wiki/PROJECT_MAP.md",
    ".agents/wiki-curator.md",
    "knowledge/source_manifest.yaml",
    "knowledge/claim_registry.yaml",
    "knowledge/experiment_registry.yaml",
    "knowledge/paper_registry.yaml",
    "knowledge/report_registry.yaml",
    "knowledge/change_inbox.jsonl",
    "templates/project-root/opencode.json",
    "templates/project-root/AGENTS.md",
    "templates/optional-agents/implementer.md",
    "templates/optional-agents/deep-research.md",
    "templates/optional-agents/reporter.md",
]

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
IGNORE_PARTS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "env",
}


def is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "#"))


def strip_target(target: str) -> str:
    target = target.split("#", 1)[0]
    target = target.split(":", 1)[0] if target.startswith("/") and ":" in target else target
    return unquote(target.strip("<>"))


def check_required(errors: list[str]) -> None:
    for rel in REQUIRED_PATHS:
        if not (WIKI_ROOT / rel).exists():
            errors.append(f"Missing required path: {rel}")


def check_links(errors: list[str], warnings: list[str]) -> None:
    for md in WIKI_ROOT.rglob("*.md"):
        if any(part in IGNORE_PARTS for part in md.parts):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            raw = match.group(1)
            if is_external(raw):
                continue
            target = strip_target(raw)
            if not target:
                continue
            candidate = (md.parent / target).resolve()
            try:
                candidate.relative_to(WIKI_ROOT)
            except ValueError:
                warnings.append(f"{md.relative_to(WIKI_ROOT)} links outside repo: {raw}")
                continue
            if not candidate.exists():
                errors.append(f"Broken link in {md.relative_to(WIKI_ROOT)}: {raw}")


def check_jsonl(errors: list[str]) -> None:
    for rel in ["knowledge/change_inbox.jsonl", "knowledge/events.jsonl"]:
        path = WIKI_ROOT / rel
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"Invalid JSONL {rel}:{lineno}: {exc}")


def check_json_files(errors: list[str]) -> None:
    for rel in ["templates/project-root/opencode.json"]:
        path = WIKI_ROOT / rel
        if not path.exists():
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON {rel}: {exc}")


def check_size(warnings: list[str]) -> None:
    limits = {
        "wiki/START_HERE.md": 180,
        "wiki/CURRENT_STATE.md": 500,
        "wiki/ROUTING_TABLE.md": 300,
    }
    for rel, limit in limits.items():
        path = WIKI_ROOT / rel
        if path.exists():
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            if len(lines) > limit:
                warnings.append(f"{rel} has {len(lines)} lines; target <= {limit}.")


def check_active_logs(warnings: list[str]) -> None:
    active = WIKI_ROOT / "wiki" / "logs" / "active"
    if not active.exists():
        return
    for path in active.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "Newest first" not in text:
            warnings.append(f"{path.relative_to(WIKI_ROOT)} should state that entries are newest-first.")
        if len(text.splitlines()) > 800:
            warnings.append(f"{path.relative_to(WIKI_ROOT)} is over 800 lines; consider rollover.")


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    check_required(errors)
    check_links(errors, warnings)
    check_jsonl(errors)
    check_json_files(errors)
    check_size(warnings)
    check_active_logs(warnings)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"agent-wiki lint failed: {len(errors)} error(s), {len(warnings)} warning(s).")
        sys.exit(1)
    print(f"agent-wiki lint passed: {len(warnings)} warning(s).")


if __name__ == "__main__":
    main()

