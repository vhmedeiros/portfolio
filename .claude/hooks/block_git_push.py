#!/usr/bin/env python3
"""PreToolUse/Bash hook: deny any `git push` (pushing to main deploys to production)."""
import json
import re
import sys

try:
    command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
except Exception:
    sys.exit(0)

# `git` (optionally followed by global flags like `-C dir`) then the `push` subcommand.
PUSH = re.compile(r"(?<![\w-])git(\s+-{1,2}[\w-]+(=\S+|\s+[^-\s]\S*)?)*\s+push(\s|$)")

if PUSH.search(command):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "git push is blocked in this repo: every push to main deploys to "
                "production. Commit locally; the user pushes."
            ),
        }
    }))
