# LinkedIn Post Draft — A11y AI Pipeline

*Created: 2026-07-13 | Status: Awaiting Or's approval before publishing*

---

We built 8 AI agents that autonomously fix accessibility bugs in a product used by millions.

No ticket assignments. No sprint planning. No "we'll get to it next quarter."

Just: audit file in → merged PR out.

In 3 months, we've opened nearly 200 PRs. 60% merged autonomously. What used to take 5 months per violation now takes hours.

But the most interesting part isn't the speed. It's that **the system gets smarter every time it runs.**

---

**The problem with accessibility in enterprise SaaS**

A11y debt doesn't accumulate because teams don't care. It accumulates because the fix-to-effort ratio is brutal.

Each violation requires: investigation → root cause analysis → code fix → PR → review → merge. Multiply that by hundreds of findings across dozens of repos.

At monday.com, we asked: what if agents handled all of that?

---

**The pipeline: 8 agents, one shared communication layer**

We didn't build a single "accessibility agent." We built a pipeline — each agent owns exactly one stage:

1. **Allison** — parses the audit file, creates one item per violation
2. **Dorit** — triages each finding, writes acceptance criteria aligned to WCAG
3. **Scout** — investigates the entire codebase, traces the violation to its root cause
4. **Felix** — implements the fix and opens a PR
5. **Paladin** — reviews the PR, scores Risk (0–10) and Confidence (0–10)
6. **Porter** — handles library upgrades when the root cause is a package bug
7. **Axel** — merges clean PRs autonomously
8. **Dana** — keeps the team informed via Slack

The critical architectural decision: **agents don't talk to each other directly. Monday.com is the communication layer.**

Status changes trigger the next agent. Item updates carry investigation context. Column values carry structured data — PR links, confidence scores, fix suggestions. Any agent — or human — can see the full history of any item and understand exactly where it is and why.

---

**The hard part nobody talks about: finding the code**

Fixing an accessibility violation sounds simple. It isn't.

The audit file tells you *what* is broken — a screen reader can't interpret a UI element, a focus state is missing, a color contrast ratio fails. It does not tell you *where* in a 10+ year old, multi-million line enterprise codebase that violation lives.

Scout's job is to figure that out. It searches the codebase, maps the violation description to actual code, understands our design system, identifies whether the root cause is a custom implementation or a library bug, and produces a fix suggestion specific enough for Felix to implement without any further research.

This is not a simple lookup. It's genuine codebase reasoning at scale.

---

**The merge bar is non-negotiable**

Paladin only approves autonomous merge when: **Risk = 0 AND Confidence = 10.**

Risk measures whether the fix changes product behavior for non-AT users. Confidence measures whether the fix is correct and complete.

Anything below that bar escalates to a human engineer. We didn't optimize for maximum autonomous throughput. We optimized for trust. If Axel merged it, the team needs to know it's safe — unconditionally.

---

**The flywheel: a system that gets smarter as it fails**

This is the part that surprised us most.

The agents maintain a shared knowledge base. Felix learns which types of implementations Paladin consistently rejects. Future runs reference past failures before making the same mistake. The system accumulates context — coding patterns, design system constraints, violation-to-solution mappings — without any agent's prompt ever changing.

Every human-in-the-loop escalation is a learning event, not just a handoff.

When an agent asks for human involvement, we review *why*. Was it a genuine blocker? Or was the agent uncertain in a situation it could have handled? We feed that analysis back. Over time, the threshold for what the system can handle autonomously keeps rising.

**The system gets better every time it "fails" — because every failure becomes a lesson.**

This is the compounding effect that most agent pipelines never reach. They're static. Ours isn't.

---

**Humans enter the flow at exactly 3 points**

1. Uploading the audit file — the pipeline starts here
2. When the root cause requires a decision no agent should make
3. When Paladin finds Risk > 0 — anything touching non-AT user behavior gets human eyes, always

Everything else runs autonomously. And that "everything else" grows larger every week.

---

**The number that still surprises me**

Before this pipeline, the average time from audit file to merged fix: **5 months.**

Now: hours.

Nearly 200 PRs opened in 3 months. 60% merged without a single human touching the code.

That's not a productivity gain. That's a category change.

---

What category of work at your company is important, chronically deprioritized, and structurally broken — not because people don't care, but because the fix-to-effort ratio makes it impossible?

That's where agents belong.

#AI #AgenticAI #Accessibility #TechLeadership #EngineeringExcellence #mondaydotcom
