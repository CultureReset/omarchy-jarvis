#!/usr/bin/env python3
"""Jarvis session runner for Ghost Platform.

Starts only when a session is triggered (call answered, text arrived, or remote/web app connected).
No wake word. No always-on microphone.
Reads every address and the allowlist from the single config file.
Runs only allowlisted actions.
"""

import argparse
import json
import os
import sys
import subprocess
import time
from pathlib import Path

CONFIG_PATH = os.environ.get("GHOST_CONFIG", "/etc/ghost/config.json")

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[jarvis] failed to load config from {CONFIG_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

def allowed(cfg, action):
    return action in cfg.get("allowlist", [])

def append_vault(cfg, content, source):
    if not allowed(cfg, "append_vault"):
        return
    # Minimal append. Real implementation calls the vault REST endpoint.
    print(f"[jarvis] vault append ({source}): {content[:200]}", file=sys.stderr)

def handle_session(trigger, cfg):
    print(f"[jarvis] session started via {trigger}", file=sys.stderr)
    append_vault(cfg, f"Session started via {trigger}", "jarvis")
    # Transcription and speech remain available for the session.
    # Allowlisted actions only. Paperclip is called only when the task needs the orchestrator.
    print("[jarvis] ready for session input. No wake word. No continuous listen.", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trigger", choices=["call", "text", "remote"], required=True,
                        help="What started this session")
    args = parser.parse_args()

    cfg = load_config()
    handle_session(args.trigger, cfg)

if __name__ == "__main__":
    main()
