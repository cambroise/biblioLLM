# Ingest — Integrate a source into the vault

4-step workflow to integrate a new source (typically a Papis article) into the Obsidian vault.

**Prerequisites**: `PAPIS_LIB` must be set, or run `papis list --libraries` to identify the active library and derive `$VAULT_DIR`.

## Vault context

- Reading notes: `Notes/` for thematic notes, courses, syntheses
- Each note is a markdown `.md` or Quarto `.qmd` file
- Papis bibliography: `Bibliography/`
- Each Papis article: folder `<dirname>/` containing `info.yaml`, `<dirname>.pdf`, `<dirname>.md`
- BibTeX key: `ref` field in `info.yaml` (may differ from folder name)
- Papis config:
  ```bash
  papis list --libraries          # identify the active library
  export PAPIS_LIB=<library-name>
  papis cache reset
  ```

---

## Step 1 — Read and analyze the source

If the argument is a Papis folder (e.g. `/ingest graphical-metho-evans-2012`):
- Read `Bibliography/<dirname>/info.yaml` for metadata
- Read the PDF `Bibliography/<dirname>/<dirname>.pdf` if available
- Read `Bibliography/<dirname>/<dirname>.md` if a note already exists

If the argument is a PDF file or a URL, read/fetch the content.

Produce:
- **Summary** in 3–5 points
- **Key takeaways**: the 3–5 most important points for the research project
- **Key equations**: extract and display the central equations with their meaning

---

## Step 2 — Identify affected pages

Search the vault for existing notes related to this source using Grep on `Bibliography/` and `Notes/` (`.md` files), looking for author names, key concepts and themes identified in Step 1.

Present to the user:
1. The **main note** to create or update (`Bibliography/<dirname>/<dirname>.md`)
2. **Existing thematic notes** to enrich (`Notes/`)
3. **Concept or author pages** to create or complete

One line of justification per page.

**Wait for user confirmation or adjustments before continuing.**

---

## Step 3 — Write the main note

For a Papis ingest, write to `Bibliography/<dirname>/<dirname>.md`.
For another source, create `Notes/Reading-[Short-Title].md`.

Note structure:

```markdown
---
tags: [claude, reading, <topic>]
source: "[[<dirname>]]"
ref: "@<bibtex-ref>"
date: YYYY-MM-DD
---

# <Full title>

**Authors**: …  **Year**: …  **Venue**: …

## 1. Summary

…

## 2. Key takeaways

- …

## 3. Key equations

…

## 4. Connections in the vault

- [[existing-note]] — reason for the link

## 5. Open questions / follow-ups

- …
```

Update the `notes: <dirname>.md` field in `info.yaml` if not already set.

---

## Step 4 — Update concept and author pages

For each concept or person confirmed in Step 2:

**If the page exists** in `Notes/`: add a bullet with a `[[wikilink]]` to the new note and a sentence of context.

**If the page does not exist** but is important: create a minimal stub in `Notes/<Concept>.md`:

```markdown
---
tags: [claude, concept]
---

# <Concept>

> Page created during ingest of [[<dirname>]].

## Definition

…

## References in the vault

- [[<dirname>]] — …
```

Only create pages confirmed in Step 2.

---

## Step 5 — Update index.md and log.md

**`index.md`**: add a line in the "Sources" section (or "Thematic notes" as appropriate) with `[[wikilink]]`, authors, year, one-line summary. Increment statistics.

**`log.md`**: append an entry:

```
## [YYYY-MM-DD] ingest | <Short title>

- **Source**: `Bibliography/<dirname>/`
- **Author**: …
- **BibTeX ref**: `@<ref>`
- **Action**: note written, pages created/updated.
- **Affected pages**: [[page1]], [[page2]]
```
