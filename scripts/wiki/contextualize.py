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


WIKI_ROOT = Path(__file__).resolve().parents[2]

ROLE_ALIASES = {
    "curator": "wiki-curator",
    "wiki_curator": "wiki-curator",
}

ROLE_EXTRA_FILES = {
    "wiki-curator": [
        "wiki/OPEN_QUESTIONS.md",
        "knowledge/source_manifest.yaml",
        "knowledge/claim_registry.yaml",
        "knowledge/change_inbox.jsonl",
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


def display_path(path: Path, root: Path = WIKI_ROOT) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def read_text(path: Path, max_lines: int) -> str:
    if not path.exists():
        return f"[missing: {display_path(path)}]\n"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if len(lines) > max_lines:
        shown = "\n".join(lines[:max_lines])
        return f"{shown}\n\n[truncated after {max_lines} lines]\n"
    return "\n".join(lines) + "\n"


def git_status(project_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=project_root,
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
    parser.add_argument("--role", default="wiki-curator", help="Agent role.")
    parser.add_argument("--task", default="", help="Optional task summary.")
    parser.add_argument("--topic", default="", help="Optional topic hub to include.")
    parser.add_argument("--project-root", default="", help="Host project root. Use '.' from the host root.")
    parser.add_argument("--max-lines", type=int, default=220, help="Lines per file.")
    parser.add_argument("--no-git", action="store_true", help="Skip git status.")
    args = parser.parse_args()

    role = normalize_role(args.role)
    role_file = f".agents/{role}.md"
    project_root = resolve_project_root(args.project_root or None)

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
    print(f"- Host Project Root: {project_root}")
    print(f"- Agent-Wiki Root: {WIKI_ROOT}\n")

    print("## Standing Instructions\n")
    print("- Follow the host `AGENTS.md` if present, then `agent-wiki/AGENTS.md`.")
    print("- This scaffold bundles only the `wiki-curator` by default.")
    print("- Do not bulk-read `agent-wiki/sources/` or host `results/`.")
    print("- Route through `agent-wiki/wiki/ROUTING_TABLE.md` before opening long sources.")
    print("- Put raw or long material in `agent-wiki/sources/`; compact truth belongs in `agent-wiki/wiki/`.")
    print("- If project truth changes, update the wiki or leave a curator handoff.\n")

    host_agents = project_root / "AGENTS.md"
    if host_agents.exists() and host_agents.resolve() != (WIKI_ROOT / "AGENTS.md").resolve():
        print("## Host AGENTS.md\n")
        print(read_text(host_agents, args.max_lines))

    for rel in files:
        print(f"## agent-wiki/{rel}\n")
        print(read_text(WIKI_ROOT / rel, args.max_lines))

    if not args.no_git:
        print("## Host Git Status\n")
        print(git_status(project_root))

    print("## Recommended Next Actions\n")
    print("1. Restate the user's task in the context of the host project.")
    print("2. Choose the smallest route from `agent-wiki/wiki/ROUTING_TABLE.md`.")
    print("3. Open only the source files needed for that route.")
    print("4. Update compact memory only when evidence supports it.")
    print("5. Run focused verification, usually `python agent-wiki/scripts/wiki/lint.py`.")
    print("6. Leave ambiguity in `agent-wiki/wiki/OPEN_QUESTIONS.md`.")


if __name__ == "__main__":
    main()
