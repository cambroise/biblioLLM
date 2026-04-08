# Init-biblioLLM — Initialize the vault

Creates or updates `index.md` and `log.md` by inventorying all existing Papis sources and notes in the vault.

**Usage**: `/init-biblioLLM` — run once in a new vault, or to resync the index after manual additions.

---

## Step 1 — Identify the vault

```bash
papis list --libraries          # list available libraries
```

Display the list of libraries. Ask the user which target library to use.

Derive from the library directory:
- `$VAULT_DIR` = parent directory of `Bibliography/` (e.g. if the library is in `/path/to/vault/Bibliography/`, then `$VAULT_DIR=/path/to/vault`)
- `$PAPIS_LIB` = name of the selected library

```bash
export PAPIS_LIB=<library-name>
papis cache reset               # full rescan of the directory
```

**Wait for user confirmation before continuing.**

---

## Step 2 — Scan the vault

Recursively read the vault to collect:

**Papis sources** — for each folder `$VAULT_DIR/Bibliography/<dirname>/`:
- Read `info.yaml`: extract `author`, `title`, `year`, `ref`, `tags`, `abstract`
- Check for the presence of the PDF and the `.md` notes file

**Thematic notes** — `$VAULT_DIR/Notes/**/*.md` and `*.qmd`:
- Read the YAML frontmatter of each file (title, tags, date)
- Identify concept pages (tag `concept`) and person pages (tag `author` or `person`)

**Other folders** — note the presence of `Administration/`, `Code/`, etc.

Present a summary to the user:
- N Papis articles found
- M notes in `Notes/`
- P concept pages, Q author pages
- `index.md` and `log.md`: existing or to create

**Wait for confirmation before writing.**

---

## Step 3 — Create or update `index.md`

**If `index.md` does not exist**, create `$VAULT_DIR/index.md`:

```markdown
---
tags: [index]
updated: YYYY-MM-DD
---

# Vault Index

## Sources (Papis bibliography)

| Wikilink | Authors | Year | Summary |
|----------|---------|------|---------|
| [[<dirname>]] | <authors> | <year> | <one-line summary> |

## Thematic notes

- [[<note>]] — one-line summary

## Concepts

- [[<Concept>]] — short definition

## People

- [[<Author>]] — role / contribution

---

**Statistics**: N sources · M notes · P concepts · Q people
*Last updated: YYYY-MM-DD*
```

**If `index.md` already exists**: read the current content, identify missing entries (Papis sources or notes not yet referenced), and propose only the additions. Do not remove existing entries.

For each Papis source:
- Use `[[<dirname>]]` as the wikilink (folder name)
- Summary: first sentence of `abstract` in `info.yaml`, or a generated summary from the title

---

## Step 4 — Create or update `log.md`

**If `log.md` does not exist**, create `$VAULT_DIR/log.md`:

```markdown
# Vault journal

## [YYYY-MM-DD] setup | Vault initialization

- **Action**: created `index.md` and `log.md` via `/init-biblioLLM`
- **Papis library**: `$PAPIS_LIB`
- **Sources indexed**: N articles
- **Notes indexed**: M files
- **Affected pages**: `index.md`, `log.md`
```

**If `log.md` already exists**, prepend a new entry:

```markdown
## [YYYY-MM-DD] setup | Vault reindex

- **Action**: updated `index.md` via `/init-biblioLLM`
- **Papis library**: `$PAPIS_LIB`
- **Additions**: N new entries in index.md
- **Affected pages**: `index.md`, `log.md`
```
