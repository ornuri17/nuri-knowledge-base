#!/usr/bin/env python3
"""
SessionEnd hook: auto-update ornuri17/nuri-knowledge-base after each session.

Reads the session transcript, extracts conversation content, and spawns
a headless `claude -p` with the update-kb skill to push KB updates.
Exits silently if there's nothing to process.
"""
import sys
import json
import os
import subprocess


def extract_conversation(transcript_path, max_messages=50, max_chars_per_msg=2000):
    messages = []
    try:
        with open(transcript_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get('type') != 'message':
                        continue
                    role = entry.get('role', '')
                    if role not in ('user', 'assistant'):
                        continue
                    content = entry.get('content', '')
                    if isinstance(content, list):
                        text = ' '.join(
                            c.get('text', '')
                            for c in content
                            if isinstance(c, dict) and c.get('type') == 'text'
                        )
                    else:
                        text = str(content)
                    text = text.strip()
                    if text:
                        if len(text) > max_chars_per_msg:
                            text = text[:max_chars_per_msg] + '...[truncated]'
                        messages.append(f"{role}: {text}")
                except (json.JSONDecodeError, KeyError):
                    continue
    except OSError:
        pass
    return '\n\n'.join(messages[-max_messages:])


def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({"suppressOutput": True}))
        return

    session_id = data.get('session_id', '')
    if not session_id:
        print(json.dumps({"suppressOutput": True}))
        return

    home = os.path.expanduser('~')
    projects_dir = os.path.join(home, '.claude', 'projects')
    transcript_path = None

    try:
        for entry in os.scandir(projects_dir):
            if entry.is_dir():
                candidate = os.path.join(entry.path, f'{session_id}.jsonl')
                if os.path.isfile(candidate):
                    transcript_path = candidate
                    break
    except OSError:
        print(json.dumps({"suppressOutput": True}))
        return

    if not transcript_path:
        print(json.dumps({"suppressOutput": True}))
        return

    conversation = extract_conversation(transcript_path)
    if len(conversation) < 200:
        # Too short to have anything KB-relevant
        print(json.dumps({"suppressOutput": True}))
        return

    plugin_dir = os.path.join(home, '.claude', 'plugins', 'local', 'update-kb')
    if not os.path.isdir(plugin_dir):
        print(json.dumps({"suppressOutput": True}))
        return

    prompt = (
        "Review the session transcript below and update the personal knowledge base "
        "at ornuri17/nuri-knowledge-base on GitHub.\n\n"
        "Use the update-kb skill. Pass --auto as the argument (headless mode: skip confirmation, "
        "commit directly).\n\n"
        "Session transcript:\n"
        + conversation
    )

    log_path = os.path.join(home, '.claude', 'hooks', 'update-kb-last-run.log')
    try:
        log_file = open(log_path, 'w')
    except OSError:
        log_file = subprocess.DEVNULL

    subprocess.Popen(
        [
            'claude', '--bare', '-p', prompt,
            '--plugin-dir', plugin_dir,
            '--dangerously-skip-permissions',
        ],
        stdout=log_file,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )

    print(json.dumps({"suppressOutput": True}))


if __name__ == '__main__':
    main()
