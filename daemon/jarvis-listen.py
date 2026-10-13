#!/usr/bin/env python3
"""Removed.

The always-listening wake-word listener has been replaced.
Use jarvis-session.py --trigger call|text|remote

No wake word. No always-on microphone.
Jarvis starts only on session trigger per Ghost Platform rules.
"""
import sys
print("jarvis-listen.py has been removed. Use jarvis-session.py --trigger <call|text|remote>", file=sys.stderr)
sys.exit(1)
