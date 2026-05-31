#!/usr/bin/env python3
"""Print a compact, role-aware context pack for agents."""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


ROOT = Path(__file__).resolve().parents[2]

ROLE_ALIASES = {
    "curator": "wiki-curator",
    "wiki_curator": "wiki-curator",
    "research": "deep-research",
    "deep_research": "deep-research",
    "deepresearch": "deep-research",
}

ROLE_EXTRA_FILES = {
    "implementer": [
        "wiki/PROJECT_MAP.md",
        "wiki/plans/active_plan.md",
        "knowledge/experiment_registry.yaml",
    ],
    "wiki-curator": [
        "wiki/OPEN_QUESTIONS.md",
        "knowledge/source_manifest.yaml",
        "knowledge/claim_registry.yaml",
        "knowledge/change_inbox.jsonl",
    ],
    "deep-research": [
        "wiki/topics/literature.md",
        "knowledge/paper_registry.yaml",
        "knowledge/claim_registry.yaml",
    ],
    "reporter": [
        "wiki/reports/REPORT_INDEX.md",
        "knowledge/report_registry.yaml",
        "knowledge/claim_registry.yaml",
        "knowledge/experiment_registry.yaml",
    ],
}

BASE_FILES = [
    "AGENTS.md",
    "wiki/START_HERE.md",
    "wiki/CURRENT_STATE.md",
    "wiki/ROUTING_TABLE.md",
]


def local_timestamp() -> str:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds")
    return datetime.now().astimezone().isoformat(timespec="seconds")


def normalize_role(role: str) -> str:
    return ROLE_ALIASES.get(role, role)


def read_text(path: Path, max_lines: int) -> str:
    if not path.exists():
        return f"[missing: {path.relative_to(ROOT)}]\n"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if len(lines) > max_lines:
        shown = "\n".join(lines[:max_lines])
        return f"{shown}\n\n[truncated after {max_lines} lines]\n"
    return "\n".join(lines) + "\n"


def git_status() -> str:
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
    except OSError as exc:
        return f"[git unavailable: {exc}]\n"
    if result.returncode != 0:
        return "[not a git repository or git status failed]\n"
    return result.stdout.strip() + "\n" if result.stdout.strip() else "clean\n"


def topic_path(topic: str) -> str:
    topic = topic.strip().replace("\\", "/").removeprefix("wiki/topics/")
    if not topic.endswith(".md"):
        topic = f"{topic}.md"
    return f"wiki/topics/{topic}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", default="implementer", help="Agent role.")
    parser.add_argument("--task", default="", help="Optional task summary.")
    parser.add_argument("--topic", default="", help="Optional topic hub to include.")
    parser.add_argument("--max-lines", type=int, default=220, help="Lines per file.")
    parser.add_argument("--no-git", action="store_true", help="Skip git status.")
    args = parser.parse_args()

    role = normalize_role(args.role)
    role_file = f".agents/{role}.md"

    files = list(BASE_FILES)
    files.append(role_file)
    files.extend(ROLE_EXTRA_FILES.get(role, []))
    if args.topic:
        files.append(topic_path(args.topic))

    print("# Agent Wiki Context Pack\n")
    print(f"- Generated: {local_timestamp()}")
    print(f"- Generated UTC: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print(f"- Role: {role}")
    if args.task:
        print(f"- Task: {args.task}")
    print(f"- Repository: {ROOT}\n")

    print("## Standing Instructions\n")
    print("- Follow `AGENTS.md` and the role contract.")
    print("- Do not bulk-read `sources/` or `results/`.")
    print("- Route through `wiki/ROUTING_TABLE.md` before opening long sources.")
    print("- Put raw or long material in `sources/`; compact truth belongs in `wiki/`.")
    print("- If project truth changes, update the wiki or leave a curator handoff.\n")

    for rel in files:
        print(f"## {rel}\n")
        print(read_text(ROOT / rel, args.max_lines))

    if not args.no_git:
        print("## Git Status\n")
        print(git_status())

    print("## Recommended Next Actions\n")
    print("1. Restate the user's task in the context of this project.")
    print("2. Choose the smallest route from `wiki/ROUTING_TABLE.md`.")
    print("3. Open only the source files needed for that route.")
    print("4. Do the work.")
    print("5. Run focused verification.")
    print("6. Leave a curator handoff if durable truth may have changed.")


if __name__ == "__main__":
    main()

