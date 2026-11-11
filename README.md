> **CultureReset fork of [dorianorellanobbap/omarchy-jarvis](https://github.com/dorianorellanobbap/omarchy-jarvis).** Wake-word voice assistant for the Omarchy bar: ask out loud, hear the answer. Local wake word + transcription; pluggable agent backend.
>
> - **Why it is here:** A starting point for a voice Jarvis. The CultureReset commits replace the always-on wake word with a session that starts only on a call, text or remote session, reads an allowlist, and calls local Paperclip and vault wrappers.
> - **Does anything run from it:** No.
> - **Changes:** The default branch carries 5 CultureReset commits on top of upstream.
> - **License:** MIT, from upstream. For updates and issues, use [upstream](https://github.com/dorianorellanobbap/omarchy-jarvis).
>
> The upstream README follows unchanged.

---

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
