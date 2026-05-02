---
title: "Design-as-code: how we rebuilt our entire platform in 12 days"
source: "https://www.vm0.ai/en/blog/posts/design-as-code"
author:
  - "[[VM0]]"
published: 2026-04-29
created: 2026-04-30
description: "A frontend engineer's take on the new design-engineering workflow in the AI era."
tags:
  - "clippings"
---
*A frontend engineer's take on the new product-engineering workflow in the AI era*

---

## A Number That Shouldn't Make Sense

12 days. Two people: a product designer and a frontend engineer. One complete platform rebuild.

Not a prototype. Not an MVP. A full replacement of a production application, culminating in a single PR that deleted 26,000 lines of legacy code. Every page, every route, every interaction, rebuilt from scratch and shipped to real users.

In any traditional product development workflow, this timeline is absurd. A project of this scope would typically take months: weeks of design exploration in Figma, rounds of stakeholder review, a handoff ceremony, sprint planning, and then the slow grind of pixel-perfect implementation. What happened here was fundamentally different. Not because we worked harder, but because the way we work together changed.

This is the story of how we shipped the Zero platform at VM0, and what it taught me about the future of product-engineering collaboration.

## The Old Bottleneck

Every frontend engineer knows the traditional pipeline:

1. Designer creates mockups in Figma
2. Design review, iteration, sign-off
3. Annotated specs with spacing, colors, breakpoints
4. Engineer translates visual specs into code
5. Back-and-forth: "Can you move this 4px to the left?"
6. Finally, wire up the API layer
7. Integration testing, more back-and-forth

![Before and After: The old handoff-heavy workflow vs. the new direct collaboration](https://clever-flame-3d70727f81.media.strapiapp.com/blog_illustration_workflow_c4c15248cb.png)

The bottleneck was never in any single step. It was in the **gaps between steps**: the waiting, the translation loss, the context switching. A designer's mental model of an interaction, once flattened into a static Figma frame and annotated with redlines, arrives at the engineer's desk already degraded. The engineer rebuilds a version of what the designer imagined, but it's inevitably a lossy copy.

We'd gotten so used to this friction that we stopped seeing it. It was just "how things work."

## The Experiment: What If the Designer Ships Code?

On March 5, 2026, Ming, our product designer, opened PR #3685: `feat(platform): add zero app with shell, pages and polish`. It added 4,146 lines of working React code.

Not a Figma file. Not a design token export. A running application.

The PR contained a complete app shell: sidebar navigation, routing structure, page skeletons for chat, schedule, activity, team management, and settings, all styled with our design system, all rendering in the browser. The data was mocked, but the UI was real. You could `npm run dev` and click through every page.

Ming didn't write this code from scratch in the traditional sense. She used AI coding tools (first Cursor, later Claude Code) to translate her design vision directly into React components. The AI handled the mechanical translation (JSX structure, CSS properties, component composition), while Ming directed the visual and interaction decisions that no AI can make: the rhythm of the layout, the hierarchy of information, the feel of the transitions.

Over the next four days, three more PRs landed:

| Date | PR | What Ming Shipped |
| --- | --- | --- |
| Mar 5 | #3685 | App shell, sidebar, all page skeletons (+4,146 lines) |
| Mar 6 | #3825 | Schedule pages, UI polish (+2,650 lines) |
| Mar 9 | #3993 | Onboarding flow, Slack config dialog (+1,146 lines) |
| Mar 9 | #4050 | About page, floating nav card |

By March 9, the entire frontend surface of our new platform existed as running code. Every page you'd eventually see in production was already clickable in a dev environment. It just didn't do anything real yet.

That's where I came in.

## My New Job: Injecting the Soul

![The 12-day migration: UI blocks placed, logic wired in, the big switch flipped](https://clever-flame-3d70727f81.media.strapiapp.com/blog_illustration_timeline_44cf9647d0.png)

When I opened the codebase on March 9, I didn't face the usual challenge of translating a flat design into code. The code was already there. My job was to replace every mock with reality, to connect each beautifully designed surface to the living, breathing backend underneath.

This changed my work in a fundamental way. Instead of thinking about pixels, I was thinking about data flows. Instead of asking "does this match the mockup?", I was asking "what API call does this page need, and what happens when it fails?"

Here's what my first week looked like:

**Day 1 (March 9):** Auth and org switching. I wired Ming's shell to Clerk authentication, added cross-domain redirects, and made the org switcher actually switch orgs. Two PRs, both merged same day.

**Day 2 (March 10):** Connectors and schedule. I replaced the mock connector grid with real API data, wired the schedule tab to actual cron jobs, and connected the instructions editor to the backend. Four PRs.

**Day 3 (March 11):** The big wiring day. Team page got real subagent data (+3,271 lines). Activity page got real logs. And the crown jewel: the chat page got connected to the actual agent run pipeline, replacing ~1,200 lines of demo code with a working AI conversation interface. That same day, I introduced `FeatureSwitchKey.Zero`, a feature flag that let us run the old and new platforms side by side.

**Days 4-5 (March 12-13):** File attachments, session management, multi-agent chat, settings persistence. Every page that Ming had built was now doing real work.

The rhythm was almost musical. Each morning I'd pick a page from Ming's scaffold, study its component structure, identify what data it expected, build the API integration, handle the error states, and push. By afternoon, another page was alive.

## The Feature Switch: Parallel Worlds

The `FeatureSwitchKey.Zero` feature flag deserves its own mention, because it's what made this migration safe rather than reckless.

From March 11 onward, our production app ran two complete UIs in parallel. Users on the old system saw the old routes. Internal testers on the new system saw Zero. Every page I wired up could be tested in production context without risking a single user's workflow.

This isn't revolutionary. Feature flags are standard practice. But the combination of feature flags with the design-as-code workflow created something special: we could validate the entire UX of the new platform (because Ming had built a complete, browsable UI) while progressively making each page functional (because I was wiring them one by one). At any point, if something went wrong, we could flip the switch back.

Nothing went wrong.

## Day 12: The Big Switch

On March 17, I opened PR #5095: `refactor: remove all non-zero platform pages and feature flag`.

The diff: **+456 lines, -26,041 lines.**

*Before: the old VM0 Platform. Tables, run IDs, and raw session data.*

![The old VM0 Platform](https://clever-flame-3d70727f81.media.strapiapp.com/screenshot_before_resized_2106db2c6e.png)

*After: the new Zero. A conversational AI workspace with pinned agents and use case cards.*

![The new Zero platform](https://clever-flame-3d70727f81.media.strapiapp.com/screenshot_after_final_030307aec7.png)

In a single merge, every legacy route was deleted. The feature flag was removed. Zero was no longer an option; it was the only mode. A follow-up PR (#5155) dropped the `/zero` URL prefix entirely: what had been `/zero/chat` became simply `/chat`.

Why did I feel confident making this cut? Because:

- Every page had been running under the feature flag for at least 5 days
- Every API integration had been tested against production data
- The old and new systems shared the same backend. This was a frontend swap, not a data migration
- We had real users on the new system providing feedback throughout

The 26,000 lines weren't deleted with anxiety. They were deleted with relief.

## The Pattern Repeats

What surprised me most wasn't the migration itself. It was that the workflow we'd discovered became our default mode for every feature that followed. Ming builds the UI shell with AI assistance, I wire the logic and extend the architecture. The same design-as-code pattern, at feature scale:

### Permissions System (March 19 → April 7)

Ming shipped PR #5467, a permissions drawer UI with Sheet components and toggle controls. Three commits, clean UI.

I added 13 commits to the same PR: database migration for `firewall_access_requests`, API endpoints, integration tests, lint fixes. Then over the next two weeks, 10+ follow-up PRs built out the full permission layer: approval card redesign, Slack notifications for access requests, CLI `doctor` commands for diagnosing permission issues, and eventually renaming the entire concept from "firewall" to "permission" across the codebase.

Ming's drawer was the seed. The permission system was the tree.

### Schedule System (March 23 → April 13)

Ming designed the schedule detail route and calendar UX (#6155). Three commits of clean UI work.

I added 14 commits: description editing with auto-generation, Slack channel selection for notifications, unsaved-changes confirmation dialogs, calendar/list view unification, and comprehensive tests. Then 15+ follow-up PRs expanded it into a full recurring task system with run history, timezone handling, and cron expression support.

### Telegram Integration (April 27 → April 28)

By this point, the pattern was so well-practiced that we shipped an entire platform integration in 48 hours. Ming built the Settings UI (#11196) and Onboarding flow (#11399). I built the multi-bot API, message send/receive, file upload/download, rich message context, Ably real-time updates, and E2E tests. The next day, it was enabled for all users.

## Where AI Fits In

I want to be precise about AI's role here, because it's easy to either overstate or understate it.

**AI enabled the designer to code.** Ming is a product designer, not a software engineer. She thinks in layouts, hierarchies, and interactions, not in React hooks and TypeScript generics. AI tools (Cursor, then Claude Code) bridged that gap by handling the mechanical translation from design intent to working code. Ming directed; AI typed. The result was code that a designer authored but an engineer could build on.

**AI accelerated the review loop.** On collaborative PRs, my AI agent would review Ming's code, classify issues by priority (P0/P1/P2), and push fix commits directly. PR #5060 went through five review rounds in 38 minutes. PR #5467 completed three rounds in 20 minutes. This isn't "AI replacing code review". I still read every change. But the mechanical work of identifying lint issues, missing types, and test gaps was automated away.

**AI did not make the design decisions.** The information architecture of each page, the interaction patterns, the visual hierarchy: these came from Ming's product instinct, informed by user research and domain expertise. AI can generate a settings page, but it can't decide what should be a toggle versus a dropdown, or when a confirmation dialog is warranted versus when it's friction.

**AI did not make the architecture decisions.** The choice to use a feature flag for parallel deployment, the API layer separation strategy, the decision to wire pages incrementally rather than all-at-once: these were engineering judgment calls. AI helped me write the code faster, but the sequencing and risk management were human.

The honest summary: AI eliminated the translation layer between design and engineering. It didn't replace either discipline; it removed the gap between them.

## What Changed About My Role

After living in this workflow for three months, I see my role as a frontend engineer differently.

**I'm no longer a visual translator.** The days of receiving a Figma file and spending hours matching spacing values are over. Not because I'm faster at it, but because it's no longer my job. The designer's intent arrives as code, not as a picture of code.

**I'm an architecture extender.** My primary value is taking a working UI surface and building the invisible infrastructure underneath: API integrations, data validation, error handling, permission checks, real-time updates, tests. The ratio on most collaborative PRs tells the story. Ming contributes 3 commits of UI, I contribute 13 commits of everything else.

**I'm a quality gatekeeper.** With AI-assisted review loops, I can maintain code quality across a much larger surface area than before. The automated review catches the mechanical issues; I focus on architectural concerns, edge cases, and making sure the feature actually works end-to-end.

**I'm a delivery strategist.** Feature flags, incremental wiring, parallel deployments: the sequencing of how a feature goes from code to production is now a core part of my work, not an afterthought.

## The Numbers

Three months. Two people. AI-assisted throughout.

- **914 merged PRs** (679 mine, 235 Ming's)
- **12 days** from first scaffold to full platform replacement
- **48 hours** for a complete Telegram integration (our fastest feature)
- **26,000 lines** deleted in a single confident merge
- **88%** of my PRs and **66%** of Ming's carry AI co-authorship

These aren't hustle metrics. Neither of us worked weekends or pulled all-nighters. The velocity comes from eliminating the dead time: the handoff meetings, the spec misunderstandings, the "can you move this 4px" back-and-forth. When design intent flows directly into code, and engineering extends that code in-place, there's simply less waste.

## What This Means for Teams

I'm not claiming every team should work this way. This workflow emerged from our specific context: a small team, a greenfield rebuild opportunity, and early access to capable AI coding tools. Your mileage will vary.

But I do believe the underlying shift is universal: **the boundary between design and engineering is dissolving, and AI is the solvent.** As AI tools get better at translating intent into code, more designers will ship code directly. As that happens, engineers will spend less time on translation and more time on architecture, quality, and delivery.

The frontend engineer's job isn't going away. It's changing shape. And honestly? The new shape is more interesting.

---

*Yuma is a frontend engineer at VM0, where he builds the platform that powers Zero, an AI agent operating system. He has mass-deleted more legacy code than he'd like to admit.*