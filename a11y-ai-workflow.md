# A11y AI — Pipeline Architecture Reference

*Last updated: 2026-07-13*
*Source: DaPulse/a11y-knowledge-base (internal)*

## What It Is
A fully automated multi-agent system that takes raw accessibility audit files and turns them into merged, verified code fixes — with minimal human involvement.

## The Agents
- **Allison** — Parses uploaded audit files, creates one finding per violation
- **Dorit** — Triages findings into actionable tasks with WCAG criteria and acceptance criteria
- **Scout** — Investigates the codebase, produces a concrete fix suggestion (cron-triggered)
- **Felix** — Implements the fix, creates a PR, iterates on Paladin's feedback
- **Paladin** — Reviews the PR, scores Risk (0–10) and Confidence (0–10), routes to merge or escalation
- **Porter** — Upgrades Vibe npm packages, consolidates all items per repo into one PR
- **Axel** — Merges "Ready to merge" PRs via Sphera API, posts Slack summary
- **Dana** — Sends Slack notification when an item reaches a terminal status

## The Flow
Audit file uploaded → Allison parses → Dorit triages → Scout investigates → Felix implements → Paladin reviews → Axel merges → Dana notifies

## Human Touchpoints (only 4)
1. Uploading audit files (pipeline entry)
2. "Requires engineer" — Vibe bug with no existing fix, or blocker too complex for agents
3. "Requires human review" — Paladin found Risk > 0 (behavioral change for non-AT users)
4. Vibe upgrade PRs — Porter flags for human review before merge

## Key Design Principle
Agents don't communicate directly. **Monday.com is the shared communication layer** — status changes trigger the next agent, item updates carry context, column values carry structured data.

## Merge Criteria
Paladin must score Risk = 0 AND Confidence = 10 for autonomous merge. Anything else escalates.

## Origin
Started as an internal hackathon at monday.com. Or, Roni (PM), and Rivka (developer) won 1st place. Expanded post-hackathon; Hanan joined to co-lead development with Rivka.
