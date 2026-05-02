---
title: "Context, Not Control"
source: "https://www.vm0.ai/en/blog/posts/context-not-control-1"
author:
  - "[[VM0]]"
published: 2026-04-14
created: 2026-04-30
description: "Why your agent's system prompt is a bureaucracy."
tags:
  - "clippings"
---
Every rule in your agent's prompt started as a bug.

Someone saw bad behavior, wrote a rule, moved on. Someone else did the same. A third person added a "never do X" because the model did something weird once on a Tuesday. Nobody deleted anything.

Six months later the agent is spending more of its context window navigating its rulebook than thinking about the actual task.

That is control-style thinking. And I think it's one of the biggest design mistakes teams make when building AI agents.

### A Small Example That Reveals a Bigger Pattern

We ran into a problem where an agent triggered by a scheduled task kept creating *new* scheduled tasks from inside the run. Infinite recursion, except with real-world side effects.

Two ways to respond.

**Control style:** Ban it. Write code that blocks schedules from creating schedules. Add a prompt rule: "never create a schedule inside a schedule." Ship it.

**Context style:** Tell the agent what is actually happening.

> You were triggered by a scheduled task at 3:00 AM Pacific time. Schedule ID: sched\_29x8f. A scheduled run is an isolated execution with a defined scope the user originally authorized. Creating a new scheduled task would extend that scope beyond the original authorization.

The first approach patches one behavior. The second gives the agent a model of the situation.

Now it can reason about nearby questions too: Should I send a notification at 3 AM? Should I create a follow-up process the user didn't explicitly ask for? Should I modify something that extends beyond the original run's scope?

No rule needed. The agent figured it out.

A lot of teams reach for control when what they actually need is context.

### The Same Distinction Shows Up Inside Prompts

This isn't just about system-level enforcement. The context vs control split exists inside prompts too.

**Context-style prompting:** mostly facts, minimal opinion:

> You are running because of a scheduled task. Triggered at 3:00 AM Beijing time. Task ID: sched\_29x8f. The user authorized this run for a specific scope.

**Control-style prompting:** opinionated, prescriptive:

> Avoid creating schedules. You should notify the user with tool X. Never do Y unless Z.

Sometimes prescriptive instructions are useful. But very often they're compensating for missing facts. And once you start compensating that way, it gets addictive.

### How Prompts Become Bureaucracy

This is the deeper failure mode.

A team sees an issue and adds a rule. Then another. Then another. Each one patches a local problem, but together they create a system full of *proxies*.

Bezos described this pattern in his 2016 shareholder letter: good process serves you so you can serve customers. But if you're not careful, the process becomes the thing.

That is exactly what happens in agent systems.

The rule is not the thing. The rule is a proxy for the outcome you want. And proxies compound. One creates edge cases that require more. Soon the agent is reasoning through layers of accumulated instructions, each added for some historical reason nobody fully remembers.

In human organizations, this becomes bureaucracy. In agent systems, it becomes a giant prompt full of scar tissue.

### Facts Age. Opinions Rot.

A fact like "this run was triggered by a scheduled task at 3 AM" is stable. It remains true regardless of which model reads it: Claude, GPT, Gemini, whatever ships next quarter.

A statement like "you should avoid creating sub-schedules" is fragile. It depends on interpretation. It may help in one situation and silently misfire in another.

When you swap models, every opinion in your prompt is a potential landmine. The new model has different reasoning tendencies, and your carefully calibrated "avoid" might mean something completely different to it.

But grounded facts about the environment, permissions, scope, and constraints tend to generalize across models and edge cases. That's why facts are the better building material.

### The Model-Quirk Trap

This might be the most insidious version of the control problem: **teams constantly turn temporary model defects into permanent system structure.**

A model behaves badly in some narrow case. The team adds a guardrail: a prompt patch, a code check, a weird branch that only exists to stop one specific failure mode.

That patch is a bet that the quirk will persist. It almost never does.

Three months later, the model changes. The original behavior disappears. But the patch remains. Nobody wants to remove it, because maybe it was there for a reason.

This is how system prompts become legacy code.

We can easily recognize the danger when stated abstractly. But in practice, patching Sonnet's current reasoning tendencies in prompt after prompt is the same pattern in disguise.

**Documenting stable system behavior is valuable. Patching a model's reasoning tendencies is a treadmill.** The model will change under you faster than you can maintain your patches.

### A Good Test Case: Permission Denied

You can see the distinction clearly in tool diagnostics. When an agent hits a permission error:

**Control style:**

> TOKEN is missing. Run "zero permissions request gmail.send" to fix it.

Direct, but the agent learns nothing. Next time it hits a different permission error, it's stuck.

**Context style:**

> process.env.GMAIL\_TOKEN → exists zero connectors inspect gmail → connected zero permissions inspect gmail.send → denied

Options:

1. Request user approval for gmail.send
2. Use an already-authorized path if one exists

The agent now knows the token exists, the connector works, and the specific permission is denied. It understands the system's state and can reason about novel situations the rule-writer never anticipated.

### The Heuristic

Here's what I keep coming back to:

> **Whenever you're about to write "don't," "avoid," or "never" in a prompt. Stop. Ask: what fact is this rule compensating for?**

Usually there's a missing fact. The agent doesn't understand what environment it's in, what the user authorized, which actions are irreversible, or why this run differs from a normal chat interaction.

Write that fact down. Delete the rule.

Sometimes you'll still want the constraint, especially around destructive actions, money movement, or safety boundaries. Hard controls still matter.

But many prompt rules aren't true boundaries. They're compensations for missing understanding. And those are exactly the ones that pile up and rot.

### The Goal

The goal is not an agent that memorizes a checklist.

The goal is an agent that understands its situation well enough to make good decisions inside clear boundaries.

One philosophy controls behavior by stacking rules. The other improves behavior by making the world legible.

The first tends toward bureaucracy. The second tends toward understanding.

Build context. Delete the scar tissue. Ship agents that can think.