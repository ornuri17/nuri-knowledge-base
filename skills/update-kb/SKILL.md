---
name: update-kb
description: Update Or Nuri's personal knowledge base (ornuri17/nuri-knowledge-base on GitHub) based on what happened in the current session. Invoke when the user says /update-kb, "update my KB", "sync the knowledge base", or "update the personal KB". Also auto-triggered at session end via a hook. The KB stores durable facts about Or's life and work — projects, team, decisions, goals, preferences — not code or debugging context.
argument-hint: "[--auto]"
user-invocable: true
allowed-tools: [Bash, Read]
---

# update-kb

Scans the current session for durable facts worth persisting to Or Nuri's personal KB repo (`ornuri17/nuri-knowledge-base`), proposes changes, and pushes on confirmation.

## Modes

| Invocation | Behavior |
|------------|----------|
| `/update-kb` (no args) | **Interactive**: show proposed changes, wait for confirmation |
| `--auto` in `$ARGUMENTS` | **Headless**: skip confirmation, push directly. Used by the SessionEnd hook. |

Check `$ARGUMENTS` at the start. If it contains `--auto`, use headless mode throughout.

---

## What belongs in the KB — and what doesn't

The KB is a durable personal record that future Claude sessions can load to understand Or. It is NOT a task log.

**Update the KB when the session surfaced:**
- Project status, stack, or architecture changes (including migrations, tech decisions)
- New collaborators, role changes, or team updates
- Shifts in goals, branding direction, or content strategy
- Observed preferences, workflow patterns, or working-style changes that weren't already captured
- Decisions that will shape future sessions ("we migrated off X to Y", "we're starting project Z")

**Do NOT add to KB:**
- Code snippets, implementation details, debugging steps
- Temporary context ("fixing this bug this week", "trying a workaround")
- Anything task-specific that only matters for the current session
- Content already present in the KB

**The test**: if a future Claude session working on something completely unrelated would benefit from knowing this fact about Or, it belongs in the KB. If not, skip it.

If nothing in the session passes this test, output: "Nothing KB-relevant this session." and stop.

---

## Step 1: Synthesize KB-relevant facts from the session

Read the current conversation (or, in headless mode, the session transcript in the prompt). For each KB-relevant fact, note which file it belongs in:

| File | What it covers |
|------|---------------|
| `projects.md` | Active projects: status, stack, architecture, product features |
| `people.md` | Collaborators, roles, team structure |
| `goals.md` | Personal ambitions, strategic targets |
| `branding.md` | Public presence, content topics, platforms |
| `working-style.md` | Decision patterns, energy, delegation, workflow |
| `preferences.md` | Communication style, diet, aesthetics, hard rules |
| `personal.md` | Home, finances, lifestyle |
| `schedule.md` | Work hours, WFH days, protected time |

If a topic doesn't fit any existing file cleanly and is substantial enough to deserve its own page, propose creating a new file (only in interactive mode — skip new file creation in `--auto` mode to avoid noise).

---

## Step 2: Read the KB index

```bash
gh auth switch --user ornuri17 2>/dev/null
gh api repos/ornuri17/nuri-knowledge-base/contents/index.md --jq '.content' | base64 -d
```

Skim the index to confirm current file names and scope. This prevents updating files that have been renamed or creating duplicates of existing content.

---

## Step 3: Fetch current content of affected files

For each file that needs updating, fetch its current content and SHA:

```bash
RESPONSE=$(gh api repos/ornuri17/nuri-knowledge-base/contents/FILENAME.md)
SHA=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])")
CONTENT=$(echo "$RESPONSE" | python3 -c "import sys,json,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())")
```

Store both `SHA` and `CONTENT` for each file. Changes are based only on what was actually fetched — never assumed or invented.

---

## Step 4: Draft changes

Compare the current file content with the facts from Step 1. Be surgical:
- Add or update only what's new
- Do not reformat sections that aren't changing
- Match the existing file's tone, heading structure, and list style (the KB uses `##` headers and `- **Field:** value` bullets)
- Update the `*Last updated: YYYY-MM-DD*` line if the file has one

For new files: follow the closest existing file's structure.

---

## Step 5a: Propose changes (interactive mode only)

Show a concise summary of what would change, file by file:

```
KB Update Proposal

projects.md
  ~ Updated GradeByAI stack: Neon + Upstash, $5-10/mo infra cost

people.md
  No changes

[any new files]
  + Create: new-topic.md — [reason]

Confirm? (y/n)
```

Wait for explicit confirmation before pushing. If the user says no or asks for edits, revise and re-propose. Do not push without a "y" or equivalent.

---

## Step 5b: Headless mode — skip confirmation

Skip Step 5a entirely in `--auto` mode. Proceed directly to Step 6.

---

## Step 6: Push updates

For each file to update or create:

```bash
UPDATED_CONTENT=$(cat <<'EOF'
[full updated file content here]
EOF
)
ENCODED=$(printf '%s' "$UPDATED_CONTENT" | base64)

gh api repos/ornuri17/nuri-knowledge-base/contents/FILENAME.md \
  --method PUT \
  --field message="update: [one-line description of what changed]" \
  --field content="$ENCODED" \
  --field sha="$SHA_FROM_STEP_3" \
  --jq '.commit.sha'
```

For new files, omit the `sha` field.

**Always restore the primary gh account after all pushes**, whether they succeeded or failed:

```bash
gh auth switch --user or-nuri-monday 2>/dev/null
```

---

## Step 7: Report

Output one line per file:

```
Updated projects.md — GradeByAI infrastructure migration to Neon + Upstash
No changes: people.md, goals.md, branding.md
```

In headless mode, this goes to stdout (captured in logs). In interactive mode, show it in the conversation.

---

## Fail-safes

- **Nothing KB-relevant**: stop at Step 1, output "Nothing KB-relevant this session." — do not push anything
- **GitHub API error on fetch**: report the error with filename and stop; don't push partial updates
- **409 Conflict (SHA mismatch)**: re-fetch the current SHA for that file and retry the push once
- **Account switch fails**: proceed anyway — gh may already be on `ornuri17`. Always attempt `gh auth switch --user or-nuri-monday` at the end, even if earlier steps failed
- **In headless mode, transcript unavailable or too short to judge**: exit silently, do not push
