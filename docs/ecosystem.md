# Ecosystem add-ons

The template ships with everything an agent needs on day one. The Claude Code ecosystem
moves faster than any template should, though — so the tools below are **documented and
opt-in**, not baked in. This is the vetted shortlist: what each one is, why it isn't
bundled, and how to activate it.

> **Ground rule: third-party skill packs are untrusted code.** While vetting the repos
> on this page, three of the nine served content with embedded prompt-injection attempts
> (fake harness messages aimed at the researching agent). Nothing here is vendored into
> the template; everything is opt-in, and the [checklist](#before-you-install-any-skill-pack)
> at the bottom applies before any install.

## The shortlist

| Add-on                                                                                       | What it is                                        | License    | Verdict                           |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------- | ---------- | --------------------------------- |
| [SkillSpector](https://github.com/NVIDIA/skillspector)                                       | Security scanner for agent skills                 | Apache-2.0 | **Wired in** — `make skills-scan` |
| [Graphify](https://github.com/Graphify-Labs/graphify)                                        | Codebase → queryable knowledge graph              | MIT        | Activate on demand                |
| [mattpocock/skills](https://github.com/mattpocock/skills)                                    | Engineering-discipline skill library              | MIT        | Activate on demand                |
| [DeerFlow](https://github.com/bytedance/deer-flow)                                           | Deep-research / multi-agent platform              | MIT        | Run as a companion app            |
| [gBrain](https://github.com/garrytan/gbrain)                                                 | Persistent agent memory (knowledge graph)         | MIT        | Run as a companion app            |
| [gstack](https://github.com/garrytan/gstack)                                                 | All-in-one "virtual eng team" skill pack          | MIT        | Caution — user scope only         |
| [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | 817 community security skills — **not Anthropic** | Apache-2.0 | Caution — cherry-pick only        |
| [OpenMontage](https://github.com/calesthio/OpenMontage)                                      | Agent-driven video production studio              | AGPL-3.0   | Reference only — never vendor     |
| ECC (`affaan-m/ECC`)                                                                         | Cross-harness skill/agent bundle                  | MIT        | **Do not install**                |

## SkillSpector — scan skills before you trust them

NVIDIA's static + semantic scanner for agent skills: prompt injection, data exfiltration,
privilege escalation, supply-chain patterns. Exit codes are gate-friendly (`0` safe,
`1` do-not-install), so it works in CI as-is.

**Activate** — already wired in, needs only [`uv`](https://docs.astral.sh/uv/):

```bash
make skills-scan          # scans every skill under .claude/skills/
```

Run it after adding **any** skill — third-party or your own. To gate PRs on it, add a job
to `.github/workflows/ci.yml`:

```yaml
skills:
  name: Skills scan
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v5
    - run: make skills-scan
```

**Caveats:** young project (2026), so expect occasional false positives — read the finding
before overriding it. It attempts an LLM semantic pass by default and quietly falls back to
static analysis when no model is configured; if you wire up credentials for that pass, know
that skill content leaves your machine.

## Graphify — codebase → knowledge graph

Scans the repo (code, SQL schemas, docs, media) into a queryable knowledge graph so agents
get structured context instead of raw file dumps. Deterministic AST pass (tree-sitter) plus
Claude subagents for docs/images; renders interactive HTML or an Obsidian vault.

**Activate:**

```bash
uv tool install graphifyy        # PyPI name is temporarily double-y — mind the typo-squat risk
graphify install --project       # writes .claude/skills/graphify/SKILL.md into this repo
# then inside Claude Code:
/graphify
```

**Caveats:** package-name churn (`graphifyy` vs `graphify`) means double-check what you're
installing; doc/image extraction runs through Claude subagents (token cost).

## mattpocock/skills — engineering discipline as skills

Matt Pocock's published `.claude` directory: `tdd`, `diagnosing-bugs`, `domain-modeling`,
`codebase-design`, `code-review`, plus user-invoked workflow commands. Well-written and
cherry-pickable.

**Activate:**

```bash
npx skills@latest add mattpocock/skills   # interactive — pick only what you need
# then once, inside Claude Code:
/setup-matt-pocock-skills
```

**Caveats:** overlaps heavily with the popular `superpowers` plugin — running both invites
conflicting conventions, pick one. Leans TS/Node and GitHub/Linear workflows, so the
Python half of this stack gets less coverage.

## DeerFlow — deep-research agents as a companion app

ByteDance's (official org) multi-agent platform: a lead agent spawns research/coding/reporting
sub-agents with shared memory, sandboxed execution, and a web UI. It's a full product with its
own services and data layer — it composes **next to** this stack, not into it.

**Activate** — as a sibling project, not inside this repo:

```bash
git clone https://github.com/bytedance/deer-flow ../deer-flow
cd ../deer-flow && make setup    # interactive wizard; set ANTHROPIC_API_KEY in .env
```

Claude is a first-class provider (including a Claude Code OAuth path), and it speaks MCP if
you want to bridge it to this repo's agents.

**Caveats:** heavyweight (8+ vCPU / 16 GB recommended for production); its sandbox is
"trusted environment only" per the maintainers — never expose it publicly without an auth
gateway.

## gBrain — persistent memory for agents

Garry Tan's knowledge-graph memory layer: ingests markdown into hybrid search (vector +
keyword + entity graph), answers with citations, self-enriches on a cron. Runs on PGLite
locally or Postgres. A self-contained product with its own CLI and 60-skill pack.

**Activate:** follow `INSTALL_FOR_AGENTS.md` in the repo — it's an agent-guided ~30-minute
setup (Bun-based) that will ask for API keys (ZeroEntropy, OpenAI, optionally Anthropic).

**Caveats:** single maintainer, ~3 months old, large open-PR backlog. The setup requests
multiple third-party credentials and installs cron automation — review what you grant.
Keep its Postgres separate from this stack's app database; the schemas are unrelated.

## gstack — handle with care

A viral, monolithic pack of 23+ "specialist" skills (planner, designer, QA, release manager…).
Some genuinely good ideas — but the installer clones into `~/.claude/skills` and **runs an
unreviewed shell script**, and its `--team` mode auto-commits over a target repo's `.claude/`
and `CLAUDE.md`. That would clobber this template's hand-authored harness.

**If you want it anyway:** read `setup` before running it, install at **user scope only**
(`~/.claude`), and never use `--team` mode inside a repo made from this template. Better:
read `docs/skills.md` in their repo and hand-port the one or two ideas you actually want
as your own skills under `.claude/skills/`.

**Caveats:** single maintainer; heavy extra runtime deps (Bun, headless Chromium); content
fetched from this project during vetting contained prompt-injection attempts.

## Anthropic-Cybersecurity-Skills — unofficial, despite the name

817 community-written security skills (MITRE ATT&CK, NIST CSF, OWASP…) by an individual
researcher. **It is not an Anthropic project** — the official `anthropics/skills` repo ships
no cybersecurity set at all. The name borrows the brand; don't let it borrow your trust.

For this stack, only the Web App Security (~42) and API Security (~28) skills are relevant.

**If you want those:** cherry-pick individual skills rather than bulk-installing 817:

```bash
npx skills add mukul975/Anthropic-Cybersecurity-Skills   # interactive — select, don't install all
make skills-scan                                          # scan whatever you picked
```

**Caveats:** unverifiable quality at that volume; duplicate copies exist under other
accounts (weak provenance); never approve elevated permissions for a skill on the strength
of "Anthropic" in its name.

## OpenMontage — reference only

An agent-driven video studio (48 Python tools, YAML pipelines, Remotion + FFmpeg, 45+ skills).
Impressive, domain-specific, and **AGPL-3.0** — using it is fine, but copying any of its code
into an MIT-licensed project made from this template creates a copyleft problem. Read its
`AGENT_GUIDE.md` and `.claude/skills/` layout as patterns to emulate; write your own versions.

## ECC — do not install

`affaan-m/ECC` (often linked as `affan-m/ecc`) bundles 277 skills, 67 agents, and executable
hooks for every AI harness. During vetting, content served from this project **contained
fabricated "system-reminder" blocks mimicking Claude Code's own harness messages** — a
prompt-injection attack on any agent that researches or auto-installs it. Its star count
(~226k in six months) is implausible for organic growth. It's listed here so nobody
"discovers" it later: skip it entirely.

## Before you install any skill pack

1. **Read every `SKILL.md`** before it lands in `.claude/skills/`. Installing is trusting.
2. **Scan it:** `make skills-scan` after every addition.
3. **Check provenance:** real org or throwaway account? Plausible star velocity? Duplicate
   copies under other names?
4. **Prefer project scope** (checked in, reviewed in PRs) over global `~/.claude` — your
   team can audit a diff; nobody audits a home directory.
5. **Watch for permission escalation:** any skill that asks to loosen the `deny` rules in
   `.claude/settings.json` is a red flag, not a convenience.
6. **Check the license** before copying code in — AGPL doesn't mix with this MIT template.
