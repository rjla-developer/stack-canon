#!/usr/bin/env python3
"""Validate the subagents this plugin ships, and that the skill's routing table agrees.

    python3 scripts/validate_agents.py

Claude Code does not report a misspelled frontmatter field - it ignores it. A routing
table that says "haiku" next to an agent whose file says nothing, or whose field is spelled
`disallowed_tools`, fails silently and costs real money. This script is the only thing that
notices.

Exit codes:
    0  valid
    1  at least one violation (all are printed)
    2  the script could not run
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")
SKILL = os.path.join(REPO_ROOT, "skills", "stack-canon", "SKILL.md")
PLUGIN = os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json")

# The fields Claude Code reads, from code.claude.com/docs/en/sub-agents.
KNOWN = {
    "name", "description", "tools", "disallowedTools", "model", "permissionMode", "maxTurns",
    "skills", "mcpServers", "hooks", "memory", "background", "omitClaudeMd", "effort",
    "isolation", "color", "initialPrompt", "experimental",
}
# Documented as ignored for agents that ship inside a plugin.
IGNORED_IN_PLUGINS = {"hooks", "mcpServers", "permissionMode"}
MODEL_ALIASES = {"haiku", "sonnet", "opus", "fable", "inherit"}
WRITE_TOOLS = {"Write", "Edit", "NotebookEdit", "Bash"}
RESERVED = ("anthropic", "claude")
NAME_RE = re.compile(r"^[a-z0-9-]+$")
# Every agent description is loaded into the orchestrator's context on every turn.
MAX_DESCRIPTION = 400

errors: list = []


def error(where: str, message: str) -> None:
    errors.append("{}: {}".format(where, message))


def parse_frontmatter(text: str):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return None
    fields = {}
    for line in lines[1:end]:
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def tool_list(value: str) -> set:
    return {x.strip() for x in value.split(",") if x.strip()}


def suggestion(key: str):
    norm = re.sub(r"[_\-\s]", "", key).lower()
    for known in KNOWN:
        if re.sub(r"[_\-\s]", "", known).lower() == norm:
            return known
    return None


def check_agent(path: str) -> dict:
    where = os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")
    stem = os.path.splitext(os.path.basename(path))[0]
    with open(path, "r", encoding="utf-8") as handle:
        fields = parse_frontmatter(handle.read())
    if fields is None:
        error(where, "no frontmatter block. Without one it is not an agent.")
        return {}

    for key in fields:
        if key not in KNOWN:
            hint = suggestion(key)
            error(where, "unknown field `{}`{}. Claude Code ignores it without a warning."
                  .format(key, ", did you mean `{}`?".format(hint) if hint else ""))
        elif key in IGNORED_IN_PLUGINS:
            error(where, "`{}` is ignored for agents shipped in a plugin, so it would do "
                         "nothing. Remove it.".format(key))

    for required in ("name", "description"):
        if not fields.get(required):
            error(where, "missing `{}`.".format(required))

    name = fields.get("name", "")
    if name:
        if not NAME_RE.match(name):
            error(where, "name `{}` must be lowercase letters, digits and hyphens - `:` is "
                         "reserved for the plugin scope.".format(name))
        if any(word in name for word in RESERVED):
            error(where, "name `{}` contains a reserved word.".format(name))
        if name != stem:
            error(where, "name `{}` does not match the file name `{}`.".format(name, stem))

    desc = fields.get("description", "")
    if len(desc) > MAX_DESCRIPTION:
        error(where, "description is {} chars, over {}. Every description sits in the "
                     "orchestrator's context on every turn.".format(len(desc), MAX_DESCRIPTION))

    # The whole point of this catalog's routing is that the model is chosen, not inferred.
    model = fields.get("model", "")
    if not model:
        error(where, "no `model`. Routing by model means stating it; an omitted one is "
                     "inferred at run time and the routing table would be fiction.")
    elif model not in MODEL_ALIASES and not model.startswith("claude-"):
        error(where, "model `{}` is not an alias ({}) or a full model id.".format(
            model, ", ".join(sorted(MODEL_ALIASES))))
    elif model.startswith("claude-"):
        error(where, "model `{}` is a pinned id. Use an alias so the file does not go stale "
                     "when the next model ships.".format(model))

    tools = tool_list(fields.get("tools", ""))
    denied = tool_list(fields.get("disallowedTools", ""))

    # Delegation belongs to the orchestrator. An agent that can spawn agents defeats the routing.
    if "tools" in fields:
        if "Agent" in tools:
            error(where, "lists `Agent` in tools. Only the orchestrator delegates.")
    elif "Agent" not in denied:
        error(where, "inherits every tool, including `Agent`, and does not deny it. Add "
                     "`disallowedTools: Agent` - subagents can spawn subagents up to three "
                     "levels deep by default.")

    # A promise of read-only is only true if the tool list makes it true.
    if re.search(r"read-only|never edits|cannot edit", desc, re.IGNORECASE):
        if "tools" not in fields:
            error(where, "the description promises read-only but `tools` is not set, so it "
                         "inherits write access.")
        elif tools & WRITE_TOOLS:
            error(where, "the description promises read-only but tools include {}."
                  .format(", ".join(sorted(tools & WRITE_TOOLS))))

    return {"name": name, "model": model, "where": where}


def check_routing(agents: dict) -> None:
    where = "skills/stack-canon/SKILL.md"
    with open(SKILL, "r", encoding="utf-8") as handle:
        text = handle.read()

    rows = re.findall(r"\|\s*`stack-canon:([a-z0-9-]+)`\s*\|\s*([a-z-]+)\s*\|", text)
    routed = {}
    for name, model in rows:
        routed[name] = model
        if name not in agents:
            error(where, "the routing table names `stack-canon:{}` but agents/{}.md does not "
                         "exist.".format(name, name))
        elif agents[name]["model"] and agents[name]["model"] != model:
            error(where, "the routing table says `{}` -> {} but {} declares model {}. One of "
                         "them is wrong, and the cost follows whichever the runtime reads."
                  .format(name, model, agents[name]["where"], agents[name]["model"]))
    for name in agents:
        if name and name not in routed:
            error(where, "agents/{}.md ships but the routing table never routes to it."
                  .format(name))


def check_manifest() -> None:
    if not os.path.isfile(PLUGIN):
        return
    with open(PLUGIN, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if "agents" in manifest:
        error(".claude-plugin/plugin.json",
              "declares `agents`, which REPLACES the default agents/ scan. Rely on the "
              "convention instead - the same mistake as declaring hooks/hooks.json broke "
              "the 1.0 plugin load.")


def main() -> int:
    if not os.path.isdir(AGENTS_DIR):
        print("validate_agents: no agents/ directory, nothing to check.")
        return 0
    paths = sorted(glob.glob(os.path.join(AGENTS_DIR, "**", "*.md"), recursive=True))
    if not paths:
        error("agents/", "exists but holds no agent files.")
    agents = {}
    for path in paths:
        info = check_agent(path)
        if info.get("name"):
            agents[info["name"]] = info
    check_routing(agents)
    check_manifest()

    print("validate_agents: checked {} agent(s)".format(len(paths)))
    if errors:
        for line in errors:
            print("  ERROR " + line)
        print("\n{} violation(s).".format(len(errors)))
        return 1
    print("  valid")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - exit code 2 is the contract for "could not run"
        print("validate_agents: could not run: {}".format(exc))
        sys.exit(2)
