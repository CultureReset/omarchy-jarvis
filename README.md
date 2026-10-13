# Jarvis (Ghost Platform)

Voice front door on the box.

- No wake word.
- No always-on microphone.
- Starts only when a session starts: phone call answered, text arrived, or remote / web app connected.
- Transcribes speech locally and speaks replies.
- Runs only actions on the allowlist.
- Does not choose which agent or workflow runs. That is Paperclip’s job when the task needs the orchestrator.
- Runs local app maps directly on the box.
- All addresses come from the single config file.

## Session start

```sh
python jarvis-session.py --trigger call
python jarvis-session.py --trigger text
python jarvis-session.py --trigger remote
```

The systemd unit does not hold a microphone open. A session trigger (call answer script, SMS arrival, or web app connect) starts the process for that session only.

## Config

Reads `GHOST_CONFIG` (default `/etc/ghost/config.json`). Wrappers and this process only read that file. Change a URL to move a service. No code change.

## Allowlist

Anything not listed does not run. Paperclip is posted to only when the task needs the orchestrator. App maps stay on the box and never go to Paperclip.

This replaces the previous always-listening implementation.
