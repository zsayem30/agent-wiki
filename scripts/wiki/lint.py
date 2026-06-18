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
    "scripts/wiki/scan_changes.py",
    "scripts/wiki/watch_handoffs.py",
    "scripts/wiki/handoff_queue.py",
    "scripts/wiki/check_host_agent_rules.py",
    "scripts/wiki/inject_host_agent_rules.py",
    ".opencode/host-agent-memory-rules.md",
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

HANDOFF_TRUTH_VALUES = {"yes", "no", "unknown"}
HANDOFF_CURATOR_STATUSES = {"pending", "acknowledged", "curated", "deferred", "rejected"}
STATUS_NEEDS_EVIDENCE = {"completed", "verified"}
OPENCODE_AGENT_COLORS = {"primary", "secondary", "accent", "success", "warning", "error", "info"}
HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

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


def has_nonempty_value(value: object) -> bool:
    if isinstance(value, list):
        return any(has_nonempty_value(item) for item in value)
    if isinstance(value, dict):
        return any(has_nonempty_value(item) for item in value.values())
    if isinstance(value, str):
        stripped = value.strip()
        return bool(stripped) and stripped.upper() != "TODO"
    return value is not None


def check_handoff_record(rel: str, lineno: int, record: object, warnings: list[str]) -> None:
    if not isinstance(record, dict):
        warnings.append(f"{rel}:{lineno} should contain a JSON object handoff record.")
        return

    truth = record.get("current_truth_changed")
    if truth is None:
        warnings.append(f"{rel}:{lineno} missing current_truth_changed truth-impact field.")
    elif truth not in HANDOFF_TRUTH_VALUES:
        warnings.append(f"{rel}:{lineno} has unsupported current_truth_changed value: {truth!r}.")

    if truth == "yes" and not has_nonempty_value(record.get("evidence")):
        warnings.append(f"{rel}:{lineno} says current truth changed but has no evidence.")

    new_schema = "id" in record or "git" in record
    if new_schema:
        for field in ["id", "git", "evidence", "verification", "suggested_routes", "open_questions", "curator_status"]:
            if field not in record:
                warnings.append(f"{rel}:{lineno} new-schema handoff missing {field}.")
        status = record.get("curator_status")
        if status is not None and status not in HANDOFF_CURATOR_STATUSES:
            warnings.append(f"{rel}:{lineno} has unsupported curator_status value: {status!r}.")

    status = record.get("curator_status")
    if status == "curated" and truth == "yes" and not has_nonempty_value(record.get("evidence")):
        warnings.append(f"{rel}:{lineno} curated truth-changing handoff has no evidence.")


def check_event_record(rel: str, lineno: int, record: object, warnings: list[str]) -> None:
    if not isinstance(record, dict):
        warnings.append(f"{rel}:{lineno} should contain a JSON object event record.")
        return
    if record.get("type") == "handoff_created" and not record.get("handoff_id"):
        warnings.append(f"{rel}:{lineno} handoff_created event missing handoff_id.")
    if record.get("type") == "handoff_status":
        status = record.get("curator_status")
        if status not in HANDOFF_CURATOR_STATUSES:
            warnings.append(f"{rel}:{lineno} handoff_status event has unsupported curator_status: {status!r}.")


def check_jsonl(errors: list[str], warnings: list[str]) -> None:
    for rel in ["knowledge/change_inbox.jsonl", "knowledge/events.jsonl"]:
        path = WIKI_ROOT / rel
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"Invalid JSONL {rel}:{lineno}: {exc}")
                continue
            if rel == "knowledge/change_inbox.jsonl":
                check_handoff_record(rel, lineno, record, warnings)
            elif rel == "knowledge/events.jsonl":
                check_event_record(rel, lineno, record, warnings)


def check_json_files(errors: list[str]) -> None:
    for rel in ["templates/project-root/opencode.json"]:
        path = WIKI_ROOT / rel
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON {rel}: {exc}")
            continue
        check_opencode_template(rel, data, errors)


def check_opencode_template(rel: str, data: object, errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append(f"Invalid OpenCode template {rel}: expected top-level object.")
        return
    agents = data.get("agent")
    if not isinstance(agents, dict):
        return
    for name, agent in agents.items():
        if not isinstance(agent, dict) or "color" not in agent:
            continue
        color = agent.get("color")
        if not isinstance(color, str):
            errors.append(f"Invalid OpenCode agent color in {rel}: agent.{name}.color should be a string.")
            continue
        if color not in OPENCODE_AGENT_COLORS and not HEX_COLOR_RE.match(color):
            errors.append(
                f"Invalid OpenCode agent color in {rel}: agent.{name}.color={color!r}; "
                f"use one of {sorted(OPENCODE_AGENT_COLORS)} or a #RRGGBB value."
            )


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


def section_between(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start == -1:
        return ""
    rest = text[start + len(marker) :]
    next_heading = rest.find("\n## ")
    return rest if next_heading == -1 else rest[:next_heading]


def check_current_truth_support(warnings: list[str]) -> None:
    current = WIKI_ROOT / "wiki" / "CURRENT_STATE.md"
    if current.exists():
        text = current.read_text(encoding="utf-8", errors="replace")
        truth = section_between(text, "Current Truth")
        evidence = section_between(text, "Important Evidence")
        evidence_items = [line for line in evidence.splitlines() if line.strip().startswith("-")]
        if "- " in truth and not has_nonempty_value(evidence_items):
            warnings.append("wiki/CURRENT_STATE.md has Current Truth bullets without Important Evidence entries.")

    topics = WIKI_ROOT / "wiki" / "topics"
    if not topics.exists():
        return
    for path in sorted(topics.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "Status: starter" in text:
            continue
        has_assertive_summary = "## Summary" in text or "## Current Method" in text
        has_evidence = "## Evidence" in text or "Source" in text or "claim_registry" in text
        if has_assertive_summary and not has_evidence:
            warnings.append(f"{path.relative_to(WIKI_ROOT)} has synthesized truth without an evidence/source pointer.")


def yaml_blocks(text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if re.match(r"^\s*-\s+id:\s*", line):
            if current:
                blocks.append(current)
            current = [line]
        elif current:
            current.append(line)
    if current:
        blocks.append(current)
    return blocks


def block_value(block: list[str], key: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$")
    for line in block:
        match = pattern.match(line)
        if match:
            return match.group(1).strip().strip("\"'")
    return None


def block_key_has_content(block: list[str], key: str) -> bool:
    pattern = re.compile(rf"^(\s*){re.escape(key)}:\s*(.*)$")
    for index, line in enumerate(block):
        match = pattern.match(line)
        if not match:
            continue
        base_indent = len(match.group(1))
        inline = match.group(2).strip()
        if inline and inline != "[]" and inline.upper() != "TODO":
            return True
        for child in block[index + 1 :]:
            if not child.strip():
                continue
            indent = len(child) - len(child.lstrip())
            if indent <= base_indent and re.match(r"^\s*\w", child):
                break
            stripped = child.strip()
            if stripped.startswith("-"):
                stripped = stripped[1:].strip()
            if stripped and stripped.upper() != "TODO":
                return True
    return False


def block_has_evidence(block: list[str]) -> bool:
    for key in ["evidence", "verification", "outputs", "result", "results"]:
        if block_key_has_content(block, key):
            return True
    return False


def check_status_evidence(warnings: list[str]) -> None:
    for rel in [
        "knowledge/claim_registry.yaml",
        "knowledge/experiment_registry.yaml",
        "knowledge/paper_registry.yaml",
        "knowledge/report_registry.yaml",
    ]:
        path = WIKI_ROOT / rel
        if not path.exists():
            continue
        for block in yaml_blocks(path.read_text(encoding="utf-8", errors="replace")):
            status = block_value(block, "status")
            if status not in STATUS_NEEDS_EVIDENCE:
                continue
            item_id = block_value(block, "id") or "unknown-id"
            if not block_has_evidence(block):
                warnings.append(f"{rel} item {item_id} is {status} without evidence or verification.")


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    check_required(errors)
    check_links(errors, warnings)
    check_jsonl(errors, warnings)
    check_json_files(errors)
    check_size(warnings)
    check_active_logs(warnings)
    check_current_truth_support(warnings)
    check_status_evidence(warnings)

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
