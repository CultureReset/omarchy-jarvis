#!/usr/bin/env python3
"""Jarvis session runner for Ghost Platform.

Starts only on call / text / remote trigger.
No wake word. No always-on microphone.
Reads the config file. Runs only allowlisted actions through the wrappers.
App maps stay on the box. Paperclip only when this session was given a task.
"""

import argparse
import json
import os
import sys
import subprocess

CONFIG_PATH = os.environ.get("GHOST_CONFIG", "/etc/ghost/config.json")
WRAPPERS = os.environ.get("GHOST_WRAPPERS", "/opt/ghost/ghost-platform/wrappers")
BOX = os.environ.get("GHOST_BOX", "/opt/ghost/ghost-platform/box")


def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[jarvis] failed to load config from {CONFIG_PATH}: {e}", file=sys.stderr)
        sys.exit(1)


def allowed(cfg, action):
    return action in cfg.get("allowlist", [])


def run_node(script, args):
    if not os.path.exists(script):
        print(f"[jarvis] missing: {script}", file=sys.stderr)
        return 1
    print(f"[jarvis] {os.path.basename(script)} {' '.join(args)}", file=sys.stderr)
    return subprocess.run(["node", script, *args], check=False).returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trigger", choices=["call", "text", "remote"], required=True)
    parser.add_argument("--text", default="")
    parser.add_argument("--task", default="")
    parser.add_argument("--description", default="")
    parser.add_argument("--map", default="")
    args = parser.parse_args()
    cfg = load_config()

    print(f"[jarvis] session started via {args.trigger}", file=sys.stderr)
    if allowed(cfg, "append_vault"):
        note = args.text or f"Session started via {args.trigger}"
        run_node(os.path.join(WRAPPERS, "vault.js"), ["append", note, "jarvis"])

    if args.map:
        if not allowed(cfg, "run_app_map"):
            print("[jarvis] run_app_map not in allowlist", file=sys.stderr)
            sys.exit(1)
        code = run_node(os.path.join(BOX, "maps.js"), ["run", args.map])
        sys.exit(code)

    if args.task:
        if not allowed(cfg, "post_to_paperclip"):
            print("[jarvis] post_to_paperclip not in allowlist", file=sys.stderr)
            sys.exit(1)
        code = run_node(
            os.path.join(WRAPPERS, "paperclip.js"),
            [args.task, args.description],
        )
        sys.exit(code)

    print("[jarvis] session ready. no task, no app map.", file=sys.stderr)


if __name__ == "__main__":
    main()
