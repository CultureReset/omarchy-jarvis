#!/usr/bin/env python3
"""Jarvis session runner for Ghost Platform.

Starts only on call / text / remote trigger.
No wake word. No always-on microphone.
Reads config file. Runs only allowlisted actions by calling wrappers.
App maps stay on the box. Paperclip only when the task needs the orchestrator.
"""

import argparse
import json
import os
import sys
import subprocess

CONFIG_PATH = os.environ.get("GHOST_CONFIG", "/etc/ghost/config.json")
WRAPPERS = os.environ.get("GHOST_WRAPPERS", "/opt/ghost/ghost-platform/wrappers")

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[jarvis] failed to load config from {CONFIG_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

def allowed(cfg, action):
    return action in cfg.get("allowlist", [])

def run_wrapper(script, *args):
    path = os.path.join(WRAPPERS, script)
    if not os.path.exists(path):
        print(f"[jarvis] wrapper missing: {path}", file=sys.stderr)
        return
    print(f"[jarvis] running {script}", file=sys.stderr)
    subprocess.run(["node", path] + list(args), check=False)

def handle_session(trigger, cfg):
    print(f"[jarvis] session started via {trigger}", file=sys.stderr)
    if allowed(cfg, "append_vault"):
        run_wrapper("vault.js", "append", f"Session started via {trigger}", "jarvis")
    if allowed(cfg, "post_to_paperclip"):
        run_wrapper("paperclip.js")
    print("[jarvis] session ready. Allowlisted actions only.", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trigger", choices=["call", "text", "remote"], required=True)
    args = parser.parse_args()
    cfg = load_config()
    handle_session(args.trigger, cfg)

if __name__ == "__main__":
    main()
