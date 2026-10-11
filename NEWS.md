# What's new in stack-canon

Written for someone who uses the skill, not for someone who contributes to it. Newest
first. For the full technical record see [CHANGELOG.md](CHANGELOG.md).

Every entry carries a **Post angle** line: whether the change is worth telling anyone
about, and if so, what the story is. Some releases are plumbing. Those say so.

**Format contract** — each entry's heading is `## <id> · <date> · <headline>`, where `<id>`
never changes once published. A tool watching this file compares the topmost `<id>` against
the last one it saw.

---

## 2026-10-11-multi-agent-routing · 2026-10-11 · The orchestrator picks the agent and the model

**v1.4.0.** A fourth rule: each request is routed by what is at stake, not by how big it
sounds. The main session acts as orchestrator over three agents the plugin now ships.

**What you get:** a `scout` on Haiku that finds and reports, a `builder` on Sonnet that
builds what is already decided and runs the suite, and an `architect` on Opus for decisions
that are expensive to reverse. A one-line rename never leaves the main session, because
briefing an agent would cost more than the edit.

**Three limits are the point, not the fine print.** Where a thing lives is never delegated:
it is asked of the user, because that is the one decision only they can answer. A
subagent's "done" is a claim, so the orchestrator reads the diff and runs the whole suite
itself. And only the orchestrator delegates - Claude Code lets subagents spawn subagents
three levels deep by default, which would turn a routing table into a tree, so every agent
is built to be unable to.

The two read-only agents are read-only by construction: their tool lists contain nothing
that writes. A promise in a description would have been cheaper and worth less. A validator
now fails the build if a description promises read-only and the tools disagree.

**What is not known.** Nobody has measured whether this saves money, time or defects. It
adds about 180 tokens to every session by Claude Code's own estimate, and each delegation
costs tokens and context the saved model tier may or may not repay. The rule says so in the
skill, the README, the changelog and here.

**Post angle: no, not yet.** The project's whole claim is that it only says what it has
measured, and this is an unmeasured cost optimisation - exactly the kind of post that
sounds impressive and cannot be checked. What would change the answer is `evals/05`: ten
tasks run routed and unrouted, compared on tokens, time, suite result and defects found,
published with the tasks where routing lost. A post about *that result* is a strong one,
whichever way it lands. A post about the feature before it is not.

## 2026-09-27-plugin-root-paths · 2026-09-27 · The skill pointed at files it gave you no way to find

**v1.3.0.** A bug report, a fix, and a new behaviour that came out of the same thread.

**The bug.** Someone installed the plugin and reported that the copy shipped only `SKILL.md`
— no `registry/`, no `templates/` — although the skill referenced both. They were right about
the effect and wrong about the cause: the files *are* shipped. The skill referenced them as
bare relative paths, so from the model's seat they resolved against the user's project and
did not exist. Functionally identical to not shipping them.

Fixed with `${CLAUDE_PLUGIN_ROOT}`, which Claude Code resolves anywhere in a skill's Markdown
body. The live fetch now falls back to the bundled copy in the same command instead of hoping.

**The second half of the same report.** They looked for `synced_at` in a stack file and found
it empty. It was never there — `synced_at` lives in `index.json`; a stack file carries
`last_verified`. The skill told you to state a date from a field that does not exist in the
file it told you to read. Now it names the right field.

**The new behaviour.** When a stack is not in the catalog, the skill no longer just says so.
It reads the framework's own documentation in that run, applies it, and writes a draft catalog
entry to the project root — every confirmed field with the `source_url` it opened,
`needs_verification: true` on everything it could not confirm, and nothing it could have
written from general knowledge. A human reviews and merges.

That last part is a deliberate limit, not a shortcut. The catalog's whole value is that its
fields were checked against primary sources; a catalog that fills itself is indistinguishable
from the model improvising, which is the problem this skill exists to solve. The SwiftUI entry
is the proof: the correct answer was *"Apple does not prescribe this"*, and an automatic
process would almost certainly have written "MVVM, recommended by Apple" — plausible, and
false.

**Post angle: yes, on the bug.** "A user told me my plugin shipped broken. They were wrong
about why, and the real cause was worse." The lesson generalises past this project: a
reference an agent cannot resolve is not a reference, and nothing fails loudly when it can't.
The self-writing-catalog refusal is a good second beat for the same post.

## 2026-09-27-swiftui-fastify · 2026-09-27 · SwiftUI and Fastify, and what Apple does not tell you

**v1.2.0.** Two stacks added, bringing the catalog to eleven. Both came from a real project
that installed the skill and reported rule 1 as useless without them.

**What you get:** SwiftUI/iOS and Fastify now resolve. If you build on either, the skill
stops improvising the structure.

**The finding that matters: Apple never names an architecture.** Apple documents data flow
precisely — state lives in the least common ancestor of the views that need it, `@Observable`
on model types, never `@State` for persistence — and there is no Apple page that says MVVM,
VIPER or TCA. The catalog records Apple's rules as doctrine and everything above them as its
own judgment, labelled as such.

Second: **Apple ships no API for unit-testing a SwiftUI view's body.** Reading `body` outside
a rendering context is not supported. So presentation rules either move into an observable
model or get reached through XCUITest. There is no third option, and the catalog says so
instead of pretending there is.

Fastify is the opposite case — it prescribes plenty, through the plugin system. Encapsulation
*is* the architecture. The load order, the `app.js`/`server.js` split and `inject()` are the
team's own words.

Neither stack has a framework-team agent skill. The two `SKILL.md` files in the `fastify` org
belong to its documentation website — the same trap already recorded for Astro, where 22 of
them turn out to be maintainer tooling.

**Post angle: yes, strong.** "I added Apple to my tool's catalog and the honest answer was
*Apple doesn't prescribe an architecture*." It inverts the expectation — people assume Apple
is prescriptive and Node is loose, and here it is the reverse. Pairs with the verifiable
detail that there is no way to unit-test a SwiftUI view.

---

## 2026-09-23-business-rules-document · 2026-09-23 · One document for the group's business rules

**v1.1.0.** A third rule: when a change alters a business rule, the group's business-rules
document is updated in the same task and committed where it lives.

**What you get:** if your backend and frontend are separate repositories implementing one set
of rules, those rules stop being scattered. The skill resolves where the document lives from
a `Business docs` line in the repo's `CLAUDE.md`, then from a sibling `../docs-<group>`
checkout, and only then asks.

That line in `CLAUDE.md` is the mechanism, not a convenience: it is what keeps the habit alive
in repositories where the skill is not installed. `CLAUDE.md` also stopped carrying domain
rules and now carries the path to the document that does — a bound kept in two places rots in
one of them.

**No measured comparison supports this rule**, unlike the two before it. It says so in the
skill, in the README and in the changelog, and it stays that way until an experiment says
otherwise.

**Post angle: moderate, and only with the caveat.** The interesting frame is the problem, not
the feature: AI agents are good at reading one repository and bad at knowing the business
rule that lives in another. Do not present it as proven.

---

## 2026-09-11-only-what-evidence-supports · 2026-09-11 · Nine capabilities cut to two

**v1.0.0.** The project deleted seven of its nine capabilities and changed its name from
`dev-mentor` to `stack-canon`.

**What you get:** a skill you can read in one sitting — one page, two rules at the time — and
a catalog of architecture and testing doctrine verified against each framework team's own
documentation.

**Why:** five measured comparisons supported the architecture pillar and the testing pillar.
They did not support the rest. The rule that mattered most — ask when a decision is expensive
to reverse and only the user can answer it — was written, correct, and buried among nine
others, and a run walked straight past it. Ten doctrines dilute the one that matters.

**Post angle: yes, and it is the best story in the project.** A 1.0 that shipped by removing
things is rare, and the evidence is public including the parts where the tool lost. See
[`evidencias/de-pocas-pulgas/`](evidencias/de-pocas-pulgas/).
