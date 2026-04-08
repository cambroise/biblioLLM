# CLAUDE.md — Research vault

## Project context

This repository centralizes the work of a researcher (PhD student, postdoc, independent researcher) as a wiki of reading notes, concepts, and bibliographic references maintained by an LLM.

**Pattern**: raw sources (PDFs, articles) → the LLM builds and maintains an interlinked markdown wiki → the user reads the wiki in Obsidian while the LLM writes it.

To initialize a new vault: run `/init-biblioLLM`.

---

## Vault structure

```
<vault>/
├── index.md              # Catalog of all pages (keep up to date)
├── log.md                # Append-only chronological journal of operations
├── Bibliography/         # Papis bibliography + Obsidian vault
│   ├── .papis.config     # Papis config (library name, current directory)
│   ├── references.bib    # BibTeX exported from Papis
│   └── <dirname>/        # One folder per article (lowercase-hyphenated name)
│       ├── info.yaml     # Papis metadata (including `ref` field = BibTeX key)
│       ├── <dirname>.pdf # Article PDF
│       └── <dirname>.md  # Obsidian reading notes
└── Notes/                # Thematic notes, concepts, syntheses (.md or .qmd)
```

---

## Bibliography management (Papis)

- **Tool**: [Papis](https://papis.readthedocs.io/) — CLI bibliography manager
- **Obsidian vault**: `Bibliography/` is also an Obsidian vault — `<dirname>.md` files are reading notes browsable in Obsidian
- **Folder naming**: `<dirname>` in lowercase with hyphens (e.g. `graphical-metho-evans-2012`)
- **BibTeX key**: the `ref` field in `info.yaml` may differ from the folder name — this `ref` is what is used in Quarto citations (`@Graphical_metho_Evans_2012`)
- **BibTeX**: exported to `Bibliography/references.bib`

### Library initialization

**Always** identify the active library before any papis command:

```bash
papis list --libraries              # list available libraries
export PAPIS_LIB=<library-name>     # select the library
papis cache reset                   # full rescan of the directory (avoids missing entries)
```

`$VAULT_DIR` = parent directory of the active library's `Bibliography/` folder.

### Common commands

```bash
papis list --all                        # list all entries
papis add <file.pdf>                    # add an article
papis open <ref>                        # open a PDF
papis rm --all --force --doc-folder Bibliography/<folder>  # delete an entry
```

### BibTeX export — systematic operation

**After any addition, deletion or modification**, regenerate BibTeX:

```bash
papis export --all --format bibtex > "$VAULT_DIR/Bibliography/references.bib"
```

### Detecting and removing duplicates

Signs of a duplicate: two folders for the same article. Procedure:

```bash
papis cache reset
papis list --all        # spot duplicates (same author + year)
# Delete the empty duplicate (without PDF):
papis rm --all --force --doc-folder Bibliography/<empty-folder>
papis export --all --format bibtex > "$VAULT_DIR/Bibliography/references.bib"
```

---

## Quarto files (.qmd)

- **Format**: Quarto with HTML and PDF output
- **Bibliography**: `bibliography: references.bib` in the YAML header
- **Math**: standard LaTeX (`amsmath`, `amssymb`)
- **Diagrams**: Mermaid for timelines and schemas
- **Code**: R or Python chunks depending on the file
- Compilation: `quarto render <file.qmd>`

---

## Python (and R) code

- Scripts go in `Code/`
- Use standard scientific libraries: `numpy`, `scipy`, `sklearn`, `networkx`, `matplotlib`
- Quarto notebooks with Python/R chunks are accepted in `Notes/`

---

## Vault maintenance — mandatory rule

**Each time a markdown file is added** (reading note, concept page, author page), systematically update:

1. **`index.md`** — add a line in the appropriate section (Sources, Thematic notes, Concepts, People) with the `[[wikilink]]`, date/author if relevant, and a one-line summary. Increment the statistics at the bottom.

2. **`log.md`** — prepend an entry (format `## [YYYY-MM-DD] <type> | <title>`) with the fields: source, author, BibTeX ref if applicable, action taken, affected pages.

Log types: `ingest` (new source), `update` (updated existing note), `create` (new concept/author page), `lint` (vault audit), `setup` (structural change).

---

## Style conventions

- **Language**: English for notes and documents
- **Citations**: Quarto style `@key` with `.bib` file
- **Math**: standard LaTeX notation, `align` and `equation` environments
- **Commits**: descriptive and concise messages
- **Tags in Obsidian properties**: the `tags` line in YAML frontmatter uses tags **without `#`**:
  ```yaml
  tags: [claude, reading, concept, causal-discovery]
  ```
  Never write `tags: [#claude, #reading, ...]` — `#` is forbidden in YAML values.
