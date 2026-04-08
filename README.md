# biblioLLM

An LLM-maintained research wiki schema. It provides reusable skills and slash-command definitions that tell a Claude Code agent how to act as a disciplined wiki maintainer over a [Papis](https://papis.readthedocs.io/) bibliography + [Obsidian](https://obsidian.md/) vault.

**Pattern:** raw sources (PDFs, articles) → LLM builds and maintains a persistent wiki of interlinked markdown files → you read the wiki in Obsidian while the LLM writes it.

This repo contains the **schema layer only** — the skills and commands. Your vault (the actual wiki content) lives separately.

---

## Prerequisites

### 1. Papis — bibliography manager

[Papis](https://papis.readthedocs.io/) is a command-line bibliography manager. It organizes your papers into a folder-based library with YAML metadata.

```bash
pip install papis
```

Create a library (a folder that will hold your papers):

```bash
mkdir -p ~/research/Bibliography
papis config  # creates ~/.config/papis/config
```

Add your library to `~/.config/papis/config`:

```ini
[my-research]
dir = ~/research/Bibliography
```

Test it:

```bash
papis list --libraries              # should show "my-research"
papis add --from arxiv https://arxiv.org/abs/2301.00001
```

### 2. Obsidian — vault viewer (optional but recommended)

[Obsidian](https://obsidian.md/) is a markdown editor that renders `[[wikilinks]]` as a navigable graph. Your `Bibliography/` folder doubles as an Obsidian vault.

1. Download and install Obsidian from [obsidian.md](https://obsidian.md/)
2. Open Obsidian → **Open folder as vault** → select your vault directory (e.g. `~/research/`)
3. Obsidian will index all `.md` files and render wikilinks automatically

Useful plugins (Community plugins):
- **Dataview** — query your notes like a database
- **Graph view** — visualize connections between pages

### 3. Claude Code — the AI

[Claude Code](https://claude.ai/code) is Anthropic's CLI agent. It reads skills and commands from this repo to act as your wiki maintainer.

**Install:**
```bash
npm install -g @anthropic/claude-code
```

**Authenticate:**
```bash
claude
# follow the login prompts
```

**Verify:**
```bash
claude --version
```

### 4. Quarto — for .qmd notes (optional)

[Quarto](https://quarto.org/) renders `.qmd` files to HTML/PDF with LaTeX math, code chunks, and citations.

```bash
# macOS
brew install quarto

# Or download from https://quarto.org/docs/get-started/
```

---

## Setup

### 1. Clone this repo

```bash
git clone https://github.com/cambroise/biblioLLM
cd biblioLLM
```

### 2. Register skills and commands in Claude Code

Copy `CLAUDE-biblioLLM.md` to your vault root as `CLAUDE.md` — Claude Code automatically reads this file when you open that directory:

```bash
cp CLAUDE-biblioLLM.md ~/research/CLAUDE.md
```

Then edit `~/research/CLAUDE.md` if needed (it's a template — adjust any project-specific details).

To make the skills globally available, add the paths to your global `~/.claude/CLAUDE.md`:

```markdown
## Skills
- Use skills from /path/to/biblioLLM/papis/skill.md for Papis operations
- Use skills from /path/to/biblioLLM/quarto-manager/SKILL.md for Quarto operations
```

### 3. Initialize your vault

Open Claude Code in your vault directory:

```bash
cd ~/research
claude
```

Then run:

```
/init-biblioLLM
```

This will:
1. Detect your Papis library via `papis list --libraries`
2. Scan all existing sources (`Bibliography/*/info.yaml`) and notes (`Notes/**/*.md`)
3. Generate `index.md` — master index of all pages with one-line summaries
4. Generate `log.md` — append-only operation journal

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/init-biblioLLM` | Initialize or resync `index.md` and `log.md` from the vault |
| `/ingest <source>` | Integrate a new Papis source or PDF into the vault (creates reading note, updates concept/author pages, updates index and log) |
| `/query <question>` | Answer a question by exploring the vault; offers to save the answer as a new note |
| `/lint [category]` | Audit vault health: broken links, orphans, gaps, stale claims, contradictions |

---

## Available Skills

| Skill | Triggers | Description |
|-------|----------|-------------|
| `/papis` | `papis`, `info.yaml`, BibTeX ops | Full Papis bibliography management |
| `/quarto:check` | `.qmd` files | Validate YAML headers, math delimiters, cross-references |
| `/quarto:render` | Quarto compilation | Compile project, detect and fix errors |
| `/quarto:bib` | Bibliography ops | Cross-check citations vs `.bib` entries |
| `/quarto:convert` | `.Rmd` files | Convert `.Rmd` → `.qmd` |
| `/quarto:organize` | Project structure | Standardize directory layout |

---

## Vault layout

The commands expect this structure in your vault:

```
<vault>/
├── index.md              # Master index — every wiki page with one-line summary
├── log.md                # Append-only log: ## [YYYY-MM-DD] <verb> | <title>
├── CLAUDE.md             # Copy of CLAUDE-biblioLLM.md (instructions for the LLM)
├── Bibliography/         # Papis library (also an Obsidian vault)
│   ├── .papis.config     # Papis config
│   ├── references.bib    # Exported BibTeX
│   └── <dirname>/        # One folder per paper (lowercase-hyphenated)
│       ├── info.yaml     # Papis metadata; `ref` field = BibTeX key
│       ├── <dirname>.pdf
│       └── <dirname>.md  # Reading notes
└── Notes/                # Thematic notes, concept pages, syntheses (.md / .qmd)
```

---

## How library discovery works

No hardcoded paths. Every command starts by identifying the active library:

```bash
papis list --libraries          # list available libraries
export PAPIS_LIB=<library-name> # select the target library
papis cache reset               # rebuild cache
```

`$VAULT_DIR` is derived as the parent directory of the library's `Bibliography/` folder.

---

## Key conventions

- **BibTeX key (`ref`)** in `info.yaml` may differ from the folder name — always read `info.yaml` before generating citations.
- **Wikilinks** use `[[filename]]` syntax (Obsidian-compatible). Every note should link to related notes.
- **Log format:** `## [YYYY-MM-DD] <verb> | <title>` — grep-parseable.
- **Tags in YAML frontmatter:** no `#` prefix (`tags: [claude, reading]` not `tags: [#claude]`).
- **After any Papis import**, re-export BibTeX: `papis export --all --format bibtex > "$VAULT_DIR/Bibliography/references.bib"`.

---

## Extending

- **New slash command:** create `commands/<name>.md` following the structure of `ingest.md` (numbered steps, bash blocks, explicit user confirmation gates before writes).
- **New skill:** create `<skill-name>/skill.md` with YAML frontmatter (`name`, `description`, `triggers`) followed by the skill body.
- **Reference docs** too long for a skill file go in `<skill-name>/references/<topic>.md`.
