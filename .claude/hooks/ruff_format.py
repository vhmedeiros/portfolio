#!/usr/bin/env python3
"""PostToolUse/Write|Edit hook: ruff-format and import-sort the edited .py file."""
import json
import os
import shutil
import subprocess
import sys

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

path = payload.get("tool_input", {}).get("file_path") or payload.get("tool_response", {}).get("filePath")
if not path or not path.endswith(".py") or not os.path.isfile(path):
    sys.exit(0)

ruff = shutil.which("ruff") or os.path.expanduser("~/.local/bin/ruff")
if not os.path.exists(ruff):
    sys.exit(0)

subprocess.run([ruff, "check", "--fix", "--select", "I", "--quiet", path], check=False)
subprocess.run([ruff, "format", "--quiet", path], check=False)
