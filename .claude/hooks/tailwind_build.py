#!/usr/bin/env python3
"""PostToolUse/Write|Edit hook: rebuild core/static/core/css/site.css when a template or Tailwind source changes."""

import json
import os
import shutil
import subprocess
import sys

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

path = (
    payload.get("tool_input", {}).get("file_path")
    or payload.get("tool_response", {}).get("filePath")
    or ""
)
root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
rel = os.path.relpath(os.path.abspath(path), root) if path else ""

triggers = (rel.endswith(".html") and "/templates/" in f"/{rel}") or rel in (
    "assets/tailwind.css",
    "tailwind.config.js",
)
if not triggers:
    sys.exit(0)

tw = shutil.which("tailwindcss") or os.path.expanduser("~/.local/bin/tailwindcss")
if not os.path.exists(tw):
    print("tailwindcss não encontrado: site.css NÃO foi regerado", file=sys.stderr)
    sys.exit(0)

subprocess.run(
    [tw, "-i", "assets/tailwind.css", "-o", "core/static/core/css/site.css", "--minify"],
    cwd=root,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    check=False,
)
