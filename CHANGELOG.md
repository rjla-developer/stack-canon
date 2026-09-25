# Changelog

## 1.2.0

### Added

- **`swiftui` and `fastify`**, verified on 2026-09-25 against primary sources. Both were
  reported missing by a real project that had the skill installed and found rule 1 useless
  without them.

  **SwiftUI carries an uncomfortable finding: Apple never names an architecture.** It
  documents data flow in detail - state lives in the least common ancestor, `@Observable`
  on model types, don't use `@State` for persistence - and there is no Apple page that says
  MVVM, VIPER or TCA. Anyone presenting one as "the Apple way" is presenting an opinion.
  The entry records Apple's rules as doctrine and everything above them as this catalog's
  judgment. It also records that Apple ships **no API for unit-testing a view's body**, so
  presentation rules have to move into the model or be reached through XCUITest.

  **Fastify prescribes more than most Node frameworks, through the plugin system.** The
  load order, the `app.js`/`server.js` split and `inject()` are the team's own words. The
  `services/` layer is this catalog's.

  Neither has a framework-team agent skill. The `fastify` org publishes two SKILL.md files
  and both belong to its documentation website - the same trap already recorded for Astro.

### Fixed

- **The 1.1.0 sweep for leftovers missed `registry/`.** Eighteen strings across nine files
  still said "the mentor", including the `recommended_by` enum in `schema.json`. The 1.1.0
  changelog claimed that vocabulary was gone; it was gone from the scripts and the docs
  only. The enum value is now `catalog`, which no stack file was using.

## 1.1.0

### Added

- **Rule 3: the group's business rules live in one document.** A change that adds, removes
  or alters a business rule now updates that document in the same task, with the same exact
  bound the test uses, committed in the repository that holds it. Written for groups where
  backend and frontend are separate repositories implementing one set of rules - the
  document is resolved from the `Business docs` line in `CLAUDE.md`, then from a sibling
  `../docs-<group>` checkout, and only then by asking.

  **No measured comparison supports this rule**, unlike rules 1 and 2. It is stated as such
  in `SKILL.md` and in the README, and it stays that way until an experiment says otherwise.

- **`templates/BUSINESS-RULES.md.template`** - entities, vocabulary, states with their legal
  transitions, rules with their exact bound and the test that holds it, permissions,
  cross-repository flows, and undecided rules recorded so they are not silently invented.

### Changed

- **`CLAUDE.md` no longer carries domain rules.** It carries the path to the document that
  does. The template's `Domain rules` section became `Business rules`, holding the
  `Business docs` line and the instruction to update it - a bound kept in two places rots
  in one of them.
- **Astro was missing from the skill's description**, so the skill could fail to trigger in
  an Astro project although `registry/astro.json` has shipped since 1.0.0.

### Removed — leftovers from the nine-capability tool

A full sweep of every document, script and registry file. None of this was reachable code;
all of it was instructions pointing at things deleted in 1.0.0.

- **Eleven `gap_map` fallbacks across eight stacks told the model to apply
  `references/quality-gate.md` or `references/growth-signals.md`** — files deleted in 1.0.0.
  This is data the skill reads and acts on, so it was the worst of the leftovers. They now
  name rule 1 or rule 2 of `SKILL.md`.
- **Four `schema.json` field descriptions** cited those same files plus
  `references/delivery-gates.md`, and `dead_code_risks` still described feeding
  `mentor-clean`.
- **"The mentor" throughout** `CONTRIBUTING.md`, `docs/REGISTRY.md`, both scripts' error
  messages and the sync report. That was the vocabulary of `dev-mentor` 0.x.
- **`.gitignore` entries** for `cleanup-plan.json`, `candidates.json` and `AGENTS.md` —
  outputs of `/mentor-clean` and `flatten_claude_md.py`, both deleted.
- **`CONTRIBUTING.md` linked `references/growth-signals.md`**; `evals/README.md` linked
  `evals/scorecard.md`, the 14-row checklist for the 0.x runs.
- **`docs/ROADMAP.md` claimed five stacks still needed their architecture verified.** All
  nine now carry a framework-team source URL. It also omitted Astro entirely; Astro is the
  one stack with no `operability` block, and the roadmap now says so instead of implying
  the set is complete.
- **The changelog listed `0.2.0` above `1.0.0`**, with an `Unreleased` section between
  `1.0.0` and `0.1.0` describing the reference-loading budget and the `AGENTS.md`
  flattener — work that shipped in 0.2.0 and was deleted in 1.0.0, reading as pending.
- **Both plugin manifests still described the old tool** to anyone browsing the
  marketplace: "orchestrates... and mentors the developer on architecture, testing and code
  health", with `mentoring` and `dead-code` among the keywords.

## 1.0.0 — the version that only claims what the evidence supports

Cut from nine capabilities to two. Five measured experiments are in
`evidencias/historico-0.x/`; they supported the architecture pillar and the testing pillar,
and did not support the rest.

### Removed

`mentor-review` and `mentor-clean` — never invoked once in five experiments. The seven
reference files, including growth signals, delivery gates, project stage and the mentoring
voice. The `guided`/`technical` modes. The three-line status block. The `CLAUDE.md` line-cap
hook and the `AGENTS.md` flattener.

**Why, in one sentence: ten doctrines dilute the one that matters.** The rule "ask when a
decision is expensive to reverse and only the user can answer it" was written, correct, and
buried among nine others — and a run walked straight past it, deciding on its own that a
feature belonged on a different platform entirely. The rule is now third from the top of a
112-line file, with nothing competing.

### Kept

The registry, unchanged: eight stacks with architecture verified against each framework
team's own documentation, stack-specific test rules and traps, and the decisions each stack
forces. This is the asset — it cost research, not code.

The `CLAUDE.md` generation, as the mechanism that makes the architecture rules persist in
the project after the skill is gone.

### Added

**One question before building.** If it is not obvious which platform, project or layer a
request belongs to, ask — once. Written from the failure above.

**Presentation rules as a first-class test subject**, alongside business rules, with the
requirement to launch the app and look at the screen, and the fallbacks for when that is
not possible: real device widths in a throwaway test, another target, retry once before
believing a tooling error.

## 0.2.0

Everything here came out of two controlled comparisons against a baseline of 57 personal
skills. Where a change was caused by an observed failure, the failure is named.

### Added

- **`architecture`, `testing.rules` and `key_decisions` for all eight stacks**, verified
  against each framework team's own documentation. The registry previously said what
  skills exist; it now says how the code should be structured, which layer a test belongs
  in, and which decisions the stack forces with no default.
- **`guided` mode, now the default.** The standards are applied rather than discussed:
  decisions resolve from the registry, filtered by project stage, and are declared in a
  short footer afterwards. `technical` mode is opt-in and keeps the old behaviour.
- **Project stage** - spike, prototype, pre-release, production, maintenance. The same
  observation is a release blocker in production and noise on a spike.
- **The run-the-app rule.** A green suite is not evidence the screen is right. Anything
  with a UI must be launched and looked at, or the visual result declared unverified.
  Added after a comparison run shipped 68 passing tests, a clean analyzer and a compiling
  build - alongside an overlapping header no test would ever have caught.

### Fixed

- **The plugin failed to load.** `plugin.json` declared `hooks/hooks.json`, which Claude
  Code already loads by convention, producing "Duplicate hooks file detected". The skill
  still loaded, so nothing looked wrong while the `CLAUDE.md` line cap silently went
  unenforced. Found on the first real marketplace install; CI never installs the plugin.
- **Angular's architecture entry was wrong.** It described `core/shared/features`, which
  is community convention. The official style guide groups by feature and advises against
  directories named for types. Corrected, with the community layout kept as a variant.
- **The template had grown to 145 of the 150 lines it enforces.** Split into a 75-line
  core plus optional blocks, each carrying the condition that admits it.
- `sync_registry.py` reformatted the whole of `index.json` on every run, turning a
  one-line change into a 129-line diff. The weekly pull request exists to be read.

### Shipped late in 0.2.0, then removed in 1.0.0

These landed after the 0.2.0 notes above were written and were deleted in 1.0.0 along with
the reference files they applied to. Kept for the record, not as pending work.

#### Changed

- **The doctrine no longer reloads when the project already carries it.** A generated
  `CLAUDE.md` is the same doctrine compiled for that codebase at an eighth of the size, so
  runs after the first read it instead of the reference set. References also stopped
  pre-loading - each one loads when its step is reached - and the registry is filtered to
  the fields in use rather than printed whole. Measured: ~26k tokens per run down to ~12k
  on a new project and ~7k on one with a `CLAUDE.md`.
- **The doctrine now has a size cap**, enforced in CI. This project capped the user's
  `CLAUDE.md` at 150 lines and exempted its own references from any limit, which is how
  one of them reached 11.9k bytes.

#### Fixed

- **A run reported "no growth signal crossed a threshold" without counting.** Its own
  longest `build()` had grown from 91 to 103 lines against a stated threshold of 100. The
  instruction said "every signal requires evidence" and was read as permission to stay
  silent. `growth-signals.md` now requires producing the number - the nearest value against
  its threshold - or saying plainly that nothing was measured.

## 0.1.0

Initial release: stack-canon orchestrator, mentor-review, mentor-clean, an eight-stack
registry, the 150-line `CLAUDE.md` hook, and four eval scenarios.
