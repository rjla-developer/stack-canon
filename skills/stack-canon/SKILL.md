---
name: stack-canon
description: Applies the architecture each framework team publishes for its own stack, makes sure business rules and presentation rules are both tested and actually looked at, keeps the group's business-rules document current as the code changes, and routes each request to a scout, builder or architect agent by what is at stake. Use whenever code is being written or changed - building an app, adding a feature, refactoring, fixing a bug, setting up a project, documenting what a product does, or reviewing whether existing code follows what its framework recommends. Prefer it over improvising a structure: the registry carries what the Flutter, SwiftUI, Astro, Angular, Next.js, Expo, NestJS, Fastify, FastAPI, Spring and .NET teams actually recommend, which is external information no model reliably has.
---

# Stack Canon

Four rules, applied every time, and one question asked before any of them.

Everything else this project used to do was cut because measured experiments did not
support it. `evidencias/de-pocas-pulgas/` has the numbers for rules 1 and 2, losses
included. Rules 3 and 4 have no comparison behind them yet, and rule 4 trades tokens for
fit at a price nobody has measured.

## 0. Before building: where does this live?

**If it is not obvious which platform, project or layer a request belongs to, ask. Once.**

Then build. Never ask a second question, or one you can decide yourself.

This exists because of a failure. Given a technique measured for the web and a Flutter app,
one run asked *"where does this hero live?"*; another decided alone that it was a separate
web property and spent an hour on something the user did not want. **Where a thing lives is
the most expensive decision to reverse and the one only the user can answer.**

Everything else - state management, folder layout, which test layer - you decide, using the
registry, and name in one line when you are done.

## 1. Architecture: what the framework team says, not what you prefer

Read the stack's entry and apply its `architecture` block. Fetch it live; if that fails,
the same file ships with this skill at `${CLAUDE_PLUGIN_ROOT}/registry/<stack>.json`.

```bash
curl -sSL --max-time 20 -o /tmp/sc.json \
  https://raw.githubusercontent.com/rjla-developer/stack-canon/main/registry/<stack>.json \
  || cp "${CLAUDE_PLUGIN_ROOT}/registry/<stack>.json" /tmp/sc.json
python3 -c "import json;d=json.load(open('/tmp/sc.json'));print(json.dumps({k:d[k] for k in ('architecture','testing','key_decisions','gap_map') if k in d},indent=1,ensure_ascii=False))"
```

On the bundled copy, **say the date out loud** from that file's `last_verified`: "using a
catalog entry verified on `<last_verified>`, it may be out of date."

**Stack not in the registry: do not improvise, and do not stop there.** Read the framework's
own documentation, apply it, and write a draft to `stack-canon-<stack>.json` in the project
root: `source_url` on every field you confirmed, `needs_verification: true` on every field
you did not, nothing you could have written from general knowledge. It is a draft for
`github.com/rjla-developer/stack-canon`, not doctrine.

What to take from it:

| Field | Use |
|---|---|
| `pattern`, `folder_strategy` | The structure. Follow it. |
| `layers[].holds` / `.must_not` | The boundaries. A layer that holds what it must not is a defect. |
| `layers[].optional` | **Do not add an optional layer** until something observed requires it. |
| `variants` | The real choice. Pick one, say which, and say what it costs. |
| `rules` | Checkable invariants. These go verbatim into the project's `CLAUDE.md`. |
| `recommended_by` | `framework-team` is doctrine. Anything else is an opinion - present it as one. |

## 2. Tests: business rules and presentation rules

**Both kinds, every time behavior changes.**

**Business rules** - calculations, state transitions, validation, API contracts. Test them
where they live, not through the UI. If a rule can only be reached by rendering a screen,
the rule is in the wrong place: that is an architecture finding, not a testing one.

Test the **exact boundary**, from both sides. A rule that says "80% or more" needs 4/5 and
7/9, not a comfortable middle value. Boundaries are where the bugs are.

**Presentation rules** - what renders, what the user is told, what a control communicates.
These are as real as business rules and they break more often.

**And then look at the screen.** A green suite proves what you thought to assert; the screen
shows what you did not. One run shipped 68 passing tests, a clean analyzer and a compiling
build alongside an overlapping header. Another said "you have a place" with only a disabled
button, which reads as an error. A third found an overflow every green suite had missed.

If you cannot launch it, that is the **last** step, not the first:

- Render the changed screens at real widths in a throwaway test. 320 and 360 logical pixels
  catch the overflow a default test surface hides.
- Another device, another target, another platform. A device already running something else
  is not occupied.
- **Retry once before believing a tooling error.** Emulators report transient startup states
  as hard failures - check the stack's `traps`.

Only then say it plainly: "I could not launch this, so the visual result is unverified."
Never let that read as though it passed.

**Run the whole suite at the end and report the real output.** Never claim done without it.
No coverage targets: a test earns its place by being behavioral, specific, deterministic and
worth its maintenance. The stack's `testing.rules`, `traps` and `what_not_to_test` apply.

## 3. Business rules belong to the group, not to the repo that holds them

Backend and frontend are separate repositories implementing one set of rules, which belong
in one place. **Any change that adds, removes or alters a business rule updates that
document in the same task** - not a refactor, a dependency bump or styling.

Find it in this order: (1) the `Business docs` line in the project's `CLAUDE.md`; (2) a
sibling checkout, by convention `../docs-<group>`; (3) ask once, then write the answer into
`CLAUDE.md`.

Write entities, flows, rules with their exact bounds, valid states and who may do what.
**Never how it is built** - that is `CLAUDE.md`, and a rule kept in two places rots in one
of them. The bound in the test is the same number in the document, in the same change.
Extend the existing file in its own style; start from
`${CLAUDE_PLUGIN_ROOT}/templates/BUSINESS-RULES.md.template` only if the group has none.

It is another repository, so it gets its own commit naming the code change. **If it is not
on disk, do not skip it and do not report it as done**: print the exact entry and its file,
say it is unwritten, and offer to clone.

## 4. Route before you work

You are the orchestrator and the only one who delegates. Route by what is at stake, not by
how big the request sounds:

| The request is | Route | Model |
|---|---|---|
| Answerable from what you hold, or one small edit | yourself | - |
| Finding, listing, reading many files, summarizing | `stack-canon:scout` | haiku |
| The design is decided - build it, test it | `stack-canon:builder` | sonnet |
| Costly to reverse: where it lives, which variant, a rule across repos, a fix that already failed | `stack-canon:architect` | opus |

- Delegating costs tokens and context. If briefing takes longer than doing, do it yourself.
- Rule 0 stays with you: where a thing lives is asked of the user, never delegated.
- Brief with the goal, the files, the exact bounds and what done means. The agent has none
  of your context.
- A subagent's "done" is a claim. Read the diff and run the whole suite yourself (rule 2).
- Escalate one model tier when an agent fails or says it is unsure; never retry a tier twice.
- State the route in one line, and any model override with its reason. No Agent tool: do
  the work yourself and say so.

## The project's CLAUDE.md

Write the architecture rules and exact boundaries into `CLAUDE.md` from
`${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md.template` **before writing code**, so they
constrain the work instead of describing it afterwards. Under 150 lines.

Include only what cannot be inferred from the code: exact commands, the architecture rules
and who recommends them, the path to the business-rules document, the delegation table, and
any platform trap you paid for. **Append a landmine the moment you hit one** - it is the
only part that cannot be re-derived from the code. The `Business docs` line and the table
are what make rules 3 and 4 survive without this skill installed.

On later runs, **read the project's `CLAUDE.md` instead of re-reading this registry** unless
you need something it does not cover.
