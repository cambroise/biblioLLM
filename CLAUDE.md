# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`biblioLLM` is the **schema layer** of an LLM-maintained research wiki. It contains reusable skills and slash-command definitions that tell an LLM agent how to act as a disciplined wiki maintainer over a Papis bibliography + Obsidian vault. It does not contain the wiki or the raw sources themselves — those live in the user's vault.

The pattern: raw sources (PDFs, articles) → LLM builds and maintains a persistent wiki of interlinked markdown files → user reads the wiki in Obsidian while the LLM writes it.

## Repository structure

```
commands/       # Slash-command definitions for wiki operations
  ingest.md     # /ingest — process a new Papis source into the vault
  query.md      # /query  — answer questions against the vault
  lint.md       # /lint   — health-check the vault

papis/
  skill.md      # Papis CLI reference + workflow (imported as a skill)

quarto-manager/
  SKILL.md      # Quarto project management skill
  references/   # Detailed reference docs for each /quarto:* command
  scripts/      # Python utilities (check_yaml.py, check_bib.py, convert_rmd.py, check_math.py)
```

## Vault conventions (applies when operating on a user's vault)

The vault operated on by these commands has this layout:

```
Bibliography/           # Papis library — one subfolder per paper
  <dirname>/
    info.yaml           # metadata; `ref` field = BibTeX key
    <dirname>.pdf
    <dirname>.md        # reading notes (filed by /ingest)
Notes/                  # thematic notes, concept pages, syntheses (.md or .qmd)
index.md                # master index: every wiki page with one-line summary
log.md                  # append-only log: ## [YYYY-MM-DD] <op> | <title>
```

**Papis config:** identify the active library with `papis list --libraries`, then derive `$VAULT_DIR` (parent of `Bibliography/`).

## Core operations

### `/init-biblioLLM`
Bootstrap or resync a vault: detect the active Papis library, scan all existing sources and notes, then create or update `index.md` and `log.md`.

### `/ingest <dirname-or-pdf-or-url>`
Five-step workflow: read source → identify affected pages (confirm with user) → write `Bibliography/<dirname>/<dirname>.md` → update concept/author pages in `Notes/` → update `index.md` and `log.md`. A single ingest typically touches 10–15 wiki pages.

### `/query <question>`
Read `index.md` first, then drill into relevant pages. Always offer to persist the answer as a new `Notes/` page tagged `#claude #query`.

### `/lint [links|orphans|stale|gaps|contradictions]`
Audit the vault, produce a structured report, propose concrete actions, then log the audit run.

## Key conventions

- **BibTeX key (`ref`)** in `info.yaml` may differ from the folder name. Always read `info.yaml` to get the correct key before generating citations.
- **Wikilinks** use `[[filename]]` syntax (Obsidian-compatible). Every note should link to related notes.
- **Log format:** entries must start with `## [YYYY-MM-DD] <verb> | <title>` so they are grep-parseable.
- **index.md** is updated on every ingest and query-to-vault operation. Never let it go stale.
- **Papis folder naming:** `<word1>-<word2>-<author>-<year>` in lowercase with hyphens.
- After any Papis import, always re-export BibTeX: `papis export --all --format bibtex > references.bib`

## Papis quick reference

```bash
papis list --libraries                          # list available libraries
papis add --from arxiv https://arxiv.org/abs/… # import from arXiv
papis add paper.pdf --from doi 10.xxxx/…       # import from DOI
papis add --from bibtex "$(pbpaste)"           # import from clipboard BibTeX
papis export --all --format bibtex > refs.bib  # export full library
papis update --set KEY VALUE QUERY             # edit a field
papis tag --add TAG QUERY                      # add a tag
papis cache reset                              # rebuild cache
```

## Quarto scripts

Located in `quarto-manager/scripts/`. Run directly with Python 3:

```bash
python3 quarto-manager/scripts/check_yaml.py <file.qmd>
python3 quarto-manager/scripts/check_bib.py <refs.bib> --qmd-dir <project>/
python3 quarto-manager/scripts/check_math.py <file.qmd>
python3 quarto-manager/scripts/convert_rmd.py <file.Rmd>
```

## Extending this repo

- To add a new slash command: create `commands/<name>.md` following the structure of `ingest.md` (numbered steps, bash blocks for grep/find, explicit "wait for user confirmation" gates before writes).
- To add a new skill: create `<skill-name>/skill.md` with YAML frontmatter (`name`, `description`, `triggers`) followed by the skill body.
- Reference docs too long for a skill file go in `<skill-name>/references/<topic>.md` and are referenced from the main `SKILL.md`.
