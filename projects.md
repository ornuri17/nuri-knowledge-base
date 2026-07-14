# Active Projects

*Last updated: 2026-07-14*

## monday chat
- **What:** Real-time, Slack-like messaging experience built natively within monday.com's platform infrastructure.
- **Role:** Or is Senior Tech Lead.
- **Status:** Active development.
- **Team:** Guy (Tech Lead), Elias (Engineer), Michal (Product Lead), Nir Lachman (Group Tech Lead - mobile counterpart)
- **Architectural direction:**
  - Modular, async-first, high-concurrency event fabric
  - Deep MCP integration for agent-to-agent and agent-to-human communication
  - Agents (including Ellie) are first-class participants - not integrations
  - Enterprise-grade: multi-tenant, permissions-aware, audit-logged from day one

## A11y AI
- **What:** A team of 8-9 AI agents that autonomously solve accessibility (a11y) issues in monday.com's product.
- **Origin:** Started as an internal agents hackathon at monday.com. Or, Roni (PM), and Rivka (developer) participated - won 1st place. Decided to continue.
- **Team:** Or, Roni (PM), Rivka (developer), Hanan (co-leads development with Rivka)
- **Status:** Active, post-hackathon expansion.

## GradeByAI
- **What:** A public tool that measures how "legible" a website is to LLMs (Claude, Gemini, ChatGPT, Perplexity). Scores GEO (Generative Engine Optimization) readiness.
- **URL:** https://GradeByAI.com
- **Status:** Public, live. Or built and launched this as a side project.
- **Origin:** Built to validate the hypothesis that most websites are invisible to AI discovery layers.
- **Product features:**
  - 5 scoring dimensions: Structured Data, Content Quality, Technical Accessibility, AI Signals, Freshness
  - Single-URL analysis with detailed dimension breakdown
  - Side-by-side URL comparison (compare mode)
  - Public leaderboard of top-scoring sites
  - Embeddable score badge for websites
  - OG image generation per score (dynamic social share cards)
  - Site monitoring (scheduled re-scans with alerts)
  - Bulk scan API for multiple URLs
  - Admin dashboard
  - Multi-language UI: English, Hebrew, French, German, Spanish, Russian
- **Stack:**
  - Frontend: React + Vite + TypeScript, hosted on S3 + CloudFront
  - Backend: Node.js 22 + Express + Prisma ORM (singleton pattern), deployed as AWS Lambda
  - Database: Neon serverless Postgres (migrated from RDS July 2026)
  - Cache: Upstash Redis REST (migrated from ElastiCache July 2026)
  - Email: SendGrid
  - Crawler: Cheerio (HTML parsing)
  - Auth/admin: custom ADMIN_SECRET header
- **Infrastructure:**
  - Fully serverless, no VPC, no NAT Gateway
  - AWS: Lambda + API Gateway + S3 + CloudFront + EventBridge (scheduled scans)
  - IaC: Terraform
  - CI/CD: GitHub Actions
  - Monthly cost: ~$5-10/mo (down from ~$75/mo after July 2026 migration)

## AI Adoption Agent (internal name TBD)
- **What:** An agent that interviews a dev team, understands their workflows and context, reviews their codebase, and at the end of the interview - automatically spins up a full agentic team tailored to that team. Also creates a new monday.com Workspace with boards for their processes.
- **Goal:** Embed AI into dev teams at monday.com that currently have no agentic tooling in their daily workflows.
- **Status:** Active development, Or is driving this solo/leading.
