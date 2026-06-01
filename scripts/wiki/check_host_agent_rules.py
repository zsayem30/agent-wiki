#!/usr/bin/env python3
"""Check whether host OpenCode agents include agent-wiki memory rules."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).with_name("inject_host_agent_rules.py")


def main() -> None:
    args = [sys.executable, str(SCRIPT), "--check", *sys.argv[1:]]
    raise SystemExit(subprocess.run(args).returncode)


if __name__ == "__main__":
    main()
