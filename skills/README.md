# update-kb Skill

Automatically updates this knowledge base based on Claude Code session context.

## What it does

After each session (or when invoked manually), the skill:
1. Scans the conversation for durable KB-relevant facts (project changes, team updates, decisions, preference shifts)
2. Proposes file-by-file changes
3. Pushes confirmed changes to this repo via the GitHub API

## Installation

Copy the files into place and register in Claude Code settings:

```bash
# 1. Create plugin directory
mkdir -p ~/.claude/plugins/local/update-kb/skills/update-kb
cp SKILL.md ~/.claude/plugins/local/update-kb/skills/update-kb/SKILL.md

# 2. Copy hook script
cp update-kb-session-end-hook.py ~/.claude/hooks/update-kb-session-end.py

# 3. Register plugin in ~/.claude/plugins/installed_plugins.json
# Add to the "plugins" object:
#   "update-kb@local": [{
#     "scope": "user",
#     "installPath": "/Users/YOUR_USERNAME/.claude/plugins/local/update-kb",
#     "version": "1.0.0",
#     "installedAt": "...",
#     "lastUpdated": "..."
#   }]

# 4. Enable plugin in ~/.claude/settings.json
# Add to "enabledPlugins": { "update-kb@local": true }

# 5. Add SessionEnd hook in ~/.claude/settings.json under "hooks":
# "SessionEnd": [{ "hooks": [{ "command": "python3 ~/.claude/hooks/update-kb-session-end.py", "type": "command", "timeout": 10, "async": true }] }]
```

## Manual usage

In any Claude Code session:
```
/update-kb
```

## Auto-trigger

The `update-kb-session-end-hook.py` script fires automatically at `SessionEnd`. It:
- Reads the session transcript
- Spawns a headless `claude -p` with the session content
- The skill runs in `--auto` mode (no confirmation, commits directly)
- Output is logged to `~/.claude/hooks/update-kb-last-run.log`

## What gets updated vs. skipped

**Updates**: project status/stack, team changes, architecture decisions, goal shifts, preference discoveries, new collaborators

**Skips**: code details, debugging steps, temporary context, duplicates of existing KB content
