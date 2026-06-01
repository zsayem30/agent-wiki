#!/usr/bin/env python3
"""Inject agent-wiki memory rules into host OpenCode agents."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


RULE_REF = "{file:./agent-wiki/.opencode/host-agent-memory-rules.md}"
CURATOR = "wiki-curator"


def load_config(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing OpenCode config: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")


def write_config(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def split_csv(values: list[str]) -> set[str]:
    out: set[str] = set()
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                out.add(item)
    return out


def agent_names(config: dict[str, Any]) -> list[str]:
    agents = config.get("agent", {})
    if not isinstance(agents, dict):
        raise SystemExit("opencode.json has no object-valued 'agent' field.")
    return sorted(agents.keys())


def target_agents(config: dict[str, Any], selected: set[str], excluded: set[str]) -> list[str]:
    names = agent_names(config)
    if selected:
        missing = sorted(selected - set(names))
        if missing:
            raise SystemExit(f"Unknown agent(s): {', '.join(missing)}")
        candidates = sorted(selected)
    else:
        candidates = [name for name in names if name != CURATOR]
    return [name for name in candidates if name not in excluded and name != CURATOR]


def prompt_has_rules(prompt: Any) -> bool:
    return isinstance(prompt, str) and RULE_REF in prompt


def inject_prompt(prompt: Any) -> str:
    if prompt is None:
        return RULE_REF
    if not isinstance(prompt, str):
        raise SystemExit("Only string-valued OpenCode agent prompts are supported.")
    if RULE_REF in prompt:
        return prompt
    if prompt.strip():
        return prompt.rstrip() + "\n\n" + RULE_REF
    return RULE_REF


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Host project root.")
    parser.add_argument("--config", default="opencode.json", help="OpenCode config path relative to project root.")
    parser.add_argument("--agent", action="append", default=[], help="Specific agent to inject. Can be repeated or comma-separated.")
    parser.add_argument("--exclude", action="append", default=[], help="Agent to skip. Can be repeated or comma-separated.")
    parser.add_argument("--list", action="store_true", help="List host agents and injection status.")
    parser.add_argument("--check", action="store_true", help="Fail if selected/default agents are missing rules.")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing.")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    config_path = (project_root / args.config).resolve()
    config = load_config(config_path)
    agents = config.get("agent", {})
    selected = split_csv(args.agent)
    excluded = split_csv(args.exclude)

    if args.list:
        for name in agent_names(config):
            status = "injected" if prompt_has_rules(agents[name].get("prompt")) else "missing"
            role = "curator" if name == CURATOR else "host"
            print(f"{name}\t{role}\t{status}")
        return

    targets = target_agents(config, selected, excluded)
    missing: list[str] = []
    changed: list[str] = []

    for name in targets:
        agent = agents.get(name)
        if not isinstance(agent, dict):
            raise SystemExit(f"Agent {name!r} is not an object.")
        if prompt_has_rules(agent.get("prompt")):
            continue
        missing.append(name)
        if not args.check:
            agent["prompt"] = inject_prompt(agent.get("prompt"))
            changed.append(name)

    if args.check:
        if missing:
            print("Agents missing agent-wiki memory rules:")
            for name in missing:
                print(f"- {name}")
            raise SystemExit(1)
        print("All selected host agents include agent-wiki memory rules.")
        return

    if changed:
        if args.dry_run:
            print("Would inject agent-wiki memory rules into:")
        else:
            write_config(config_path, config)
            print("Injected agent-wiki memory rules into:")
        for name in changed:
            print(f"- {name}")
    else:
        print("No host agents needed injection.")


if __name__ == "__main__":
    main()
