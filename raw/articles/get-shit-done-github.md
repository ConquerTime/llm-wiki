<div align="center">

# GET SHIT DONE

**English** · [Português](README.pt-BR.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja-JP.md) · [한국어](README.ko-KR.md)

**A light-weight and powerful meta-prompting, context engineering and spec-driven development system for Claude Code, OpenCode, Gemini CLI, Kilo, Codex, Copilot, Cursor, Windsurf, Antigravity, Augment, Trae, Qwen Code, Cline, and CodeBuddy.**

**Solves context rot — the quality degradation that happens as Claude fills its context window.**

[![npm version](https://img.shields.io/npm/v/get-shit-done-cc?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/get-shit-done-cc)
[![npm downloads](https://img.shields.io/npm/dm/get-shit-done-cc?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/get-shit-done-cc)
[![GitHub stars](https://img.shields.io/github/stars/gsd-build/get-shit-done?style=for-the-badge&logo=github&color=181717)](https://github.com/gsd-build/get-shit-done)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)

```bash
npx get-shit-done-cc@latest
```

**Works on Mac, Windows, and Linux.**

*"If you know clearly what you want, this WILL build it for you. No bs."*

*"I've done SpecKit, OpenSpec and Taskmaster — this has produced the best results for me."*

*"By far the most powerful addition to my Claude Code. Nothing over-engineered. Literally just gets shit done."*

**Trusted by engineers at Amazon, Google, Shopify, and Webflow.**

[Why I Built This](#why-i-built-this) · [How It Works](#how-it-works) · [Commands](#commands) · [Why It Works](#why-it-works) · [User Guide](docs/USER-GUIDE.md)

</div>

---

## Why I Built This

I'm a solo developer. I don't write code — Claude Code does.

Other spec-driven development tools exist; BMAD, Speckit... But they all seem to make things way more complicated than they need to be (sprint ceremonies, story points, stakeholder syncs, retrospectives, Jira workflows) or lack real big picture understanding of what you're building. I'm not a 50-person software company. I don't want to play enterprise theater. I'm just a creative person trying to build great things that work.

So I built GSD. The complexity is in the system, not in your workflow. Behind the scenes: context engineering, XML prompt formatting, subagent orchestration, state management. What you see: a few commands that just work.

The system gives Claude everything it needs to do the work *and* verify it. I trust the workflow. It just does a good job.

That's what this is. No enterprise roleplay bullshit. Just an incredibly effective system for building cool stuff consistently using Claude Code.

— **TÂCHES**

---

Vibecoding has a bad reputation. You describe what you want, AI generates code, and you get inconsistent garbage that falls apart at scale.

GSD fixes that. It's the context engineering layer that makes Claude Code reliable. Describe your idea, let the system extract everything it needs to know, and let Claude Code get to work.

---

## Who This Is For

People who want to describe what they want and have it built correctly — without pretending they're running a 50-person engineering org.

Built-in quality gates catch real problems: schema drift detection flags ORM changes missing migrations, security enforcement anchors verification to threat models, and scope reduction detection prevents the planner from silently dropping your requirements.

---

## Getting Started

```bash
npx get-shit-done-cc@latest
```

The installer prompts you to choose:
1. **Runtime** — Claude Code, OpenCode, Gemini, Kilo, Codex, Copilot, Cursor, Windsurf, or more
2. **Location** — Global (all projects) or local (current project only)

Verify with `/gsd-help`.

---

## How It Works

### 1. Initialize Project

```
/gsd-new-project
```

1. **Questions** — Asks until it understands your idea completely
2. **Research** — Spawns parallel agents to investigate the domain
3. **Requirements** — Extracts what's v1, v2, and out of scope
4. **Roadmap** — Creates phases mapped to requirements

**Creates:** `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`, `.planning/research/`

---

### 2. Discuss Phase

```
/gsd-discuss-phase 1
```

The system analyzes the phase and identifies gray areas. Output — `CONTEXT.md` — feeds into research and planning.

**Creates:** `{phase_num}-CONTEXT.md`

---

### 3. Plan Phase

```
/gsd-plan-phase 1
```

1. **Researches** — Investigates how to implement this phase, guided by CONTEXT.md
2. **Plans** — Creates 2-3 atomic task plans with XML structure
3. **Verifies** — Checks plans against requirements, loops until they pass

Each plan is small enough to execute in a fresh context window. No degradation, no "I'll be more concise now."

**Creates:** `{phase_num}-RESEARCH.md`, `{phase_num}-{N}-PLAN.md`

---

### 4. Execute Phase

```
/gsd-execute-phase 1
```

1. **Runs plans in waves** — Parallel where possible, sequential when dependent
2. **Fresh context per plan** — 200k tokens purely for implementation, zero accumulated garbage
3. **Commits per task** — Every task gets its own atomic commit
4. **Verifies against goals** — Checks the codebase delivers what the phase promised

Walk away, come back to completed work with clean git history.

**How Wave Execution Works:**

Plans are grouped into "waves" based on dependencies. Within each wave, plans run in parallel. Waves run sequentially.

```
┌────────────────────────────────────────────────────────────────────┐
│  PHASE EXECUTION                                                   │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  WAVE 1 (parallel)          WAVE 2 (parallel)          WAVE 3      │
│  ┌─────────┐ ┌─────────┐    ┌─────────┐ ┌─────────┐    ┌─────────┐ │
│  │ Plan 01 │ │ Plan 02 │ →  │ Plan 03 │ │ Plan 04 │ →  │ Plan 05 │ │
│  │ User    │ │ Product │    │ Orders  │ │ Cart    │    │ Checkout│ │
│  │ Model   │ │ Model   │    │ API     │ │ API     │    │ UI      │ │
│  └─────────┘ └─────────┘    └─────────┘ └─────────┘    └─────────┘ │
│       │           │              ↑           ↑              ↑      │
│       └───────────┴──────────────┴───────────┘              │      │
│              Dependencies: Plan 03 needs Plan 01                   │
└────────────────────────────────────────────────────────────────────┘
```

**Creates:** `{phase_num}-{N}-SUMMARY.md`, `{phase_num}-VERIFICATION.md`

---

### 5. Verify Work

```
/gsd-verify-work 1
```

1. **Extracts testable deliverables**
2. **Walks you through one at a time**
3. **Diagnoses failures automatically** — Spawns debug agents to find root causes
4. **Creates verified fix plans** — Ready for immediate re-execution

**Creates:** `{phase_num}-UAT.md`, fix plans if issues found

---

## Why It Works

### Context Engineering

| File | What it does |
|------|--------------|
| `PROJECT.md` | Project vision, always loaded |
| `research/` | Ecosystem knowledge (stack, features, architecture, pitfalls) |
| `REQUIREMENTS.md` | Scoped v1/v2 requirements with phase traceability |
| `ROADMAP.md` | Where you're going, what's done |
| `STATE.md` | Decisions, blockers, position — memory across sessions |
| `PLAN.md` | Atomic task with XML structure, verification steps |
| `SUMMARY.md` | What happened, what changed, committed to history |

### XML Prompt Formatting

Every plan is structured XML optimized for Claude:

```xml
<task type="auto">
  <name>Create login endpoint</name>
  <files>src/app/api/auth/login/route.ts</files>
  <action>
    Use jose for JWT (not jsonwebtoken - CommonJS issues).
    Validate credentials against users table.
    Return httpOnly cookie on success.
  </action>
  <verify>curl -X POST localhost:3000/api/auth/login returns 200 + Set-Cookie</verify>
  <done>Valid credentials return cookie, invalid return 401</done>
</task>
```

### Multi-Agent Orchestration

| Stage | Orchestrator does | Agents do |
|-------|------------------|-----------|
| Research | Coordinates, presents findings | 4 parallel researchers investigate stack, features, architecture, pitfalls |
| Planning | Validates, manages iteration | Planner creates plans, checker verifies, loop until pass |
| Execution | Groups into waves, tracks progress | Executors implement in parallel, each with fresh 200k context |
| Verification | Presents results, routes next | Verifier checks codebase against goals, debuggers diagnose failures |

The orchestrator never does heavy lifting. It spawns agents, waits, integrates results.

**The result:** You can run an entire phase and your main context window stays at 30-40%. The work happens in fresh subagent contexts. Your session stays fast and responsive.

### Atomic Git Commits

Each task gets its own commit immediately after completion:

```bash
abc123f docs(08-02): complete user registration plan
def456g feat(08-02): add email confirmation flow
hij789k feat(08-02): implement password hashing
lmn012o feat(08-02): create registration endpoint
```

---

## Commands

### Core Workflow

| Command | What it does |
|---------|--------------|
| `/gsd-new-project [--auto]` | Full initialization: questions → research → requirements → roadmap |
| `/gsd-discuss-phase [N]` | Capture implementation decisions before planning |
| `/gsd-plan-phase [N]` | Research + plan + verify for a phase |
| `/gsd-execute-phase <N>` | Execute all plans in parallel waves, verify when complete |
| `/gsd-verify-work [N]` | Manual user acceptance testing |
| `/gsd-ship [N] [--draft]` | Create PR from verified phase work |
| `/gsd-next` | Automatically advance to the next logical workflow step |
| `/gsd-fast <text>` | Inline trivial tasks — skips planning entirely |
| `/gsd-complete-milestone` | Archive milestone, tag release |
| `/gsd-new-milestone [name]` | Start next version |

---

## Configuration

### Model Profiles

| Profile | Planning | Execution | Verification |
|---------|----------|-----------|--------------|
| `quality` | Opus | Opus | Sonnet |
| `balanced` (default) | Opus | Sonnet | Sonnet |
| `budget` | Sonnet | Sonnet | Haiku |
| `inherit` | Inherit | Inherit | Inherit |

### Key Workflow Settings

| Setting | Default | What it controls |
|---------|---------|------------------|
| `workflow.use_worktrees` | `true` | Toggle worktree isolation for execution |
| `parallelization.enabled` | `true` | Run independent plans simultaneously |
| `workflow.auto_advance` | `false` | Auto-chain discuss → plan → execute |

---

## License

MIT License. See [LICENSE](LICENSE) for details.

**Claude Code is powerful. GSD makes it reliable.**

Source: https://github.com/gsd-build/get-shit-done
