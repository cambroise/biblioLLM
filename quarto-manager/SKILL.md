---
name: quarto-manager
description: |
  Complete Quarto project manager (websites and books). Use this skill whenever the user
  is working with .qmd or .Rmd files, mentions Quarto, wants to create/check/compile a
  Quarto site or book, manage a BibTeX bibliography, convert Rmd files to qmd, or organize
  a Quarto project structure. Also triggers for: _quarto.yml, cross-references (@fig-, @tbl-,
  @eq-), R/Python chunks, quarto render, revealjs, beamer, or any Quarto syntax question.
triggers:
  - /quarto
---

# Quarto Manager

End-to-end Quarto project management: syntax checking, Rmd→qmd conversion, directory organization, bibliography management, and compilation.

## User preferences

- Inline math: `$...$`
- Display equations: `$$...$$`
- Style: precise and concise

## Quarto best practices

- After editing Quarto files, always verify PDF compilation with `quarto render`.
- Be careful with special characters (`---`, `|`) in markdown cells — they break YAML parsing.
- When adding images or covers, ensure changes work for **both HTML and PDF** output, not just one.
- For multiline equations, use `$$` delimiters with `\begin{aligned}` inside. Avoid `\begin{align}` directly in markdown cells — it can cause rendering issues in PDF output.

## Commands

Five slash commands are available. Each has detailed documentation in `references/`. Read the corresponding reference file before executing the command.

| Command | Action | Reference |
|---------|--------|-----------|
| `/quarto:check` | Check format and syntax | `references/check.md` |
| `/quarto:convert` | Convert .Rmd → .qmd | `references/convert.md` |
| `/quarto:organize` | Organize project structure | `references/organize.md` |
| `/quarto:bib` | Manage bibliography | `references/bib.md` |
| `/quarto:render` | Compile the project | `references/render.md` |

## General behavior

### Caution and backups
Always ask for confirmation before modifying or deleting files. Create automatic backups before any conversion or reorganization (`backup/` folder). Suggest corrections without ever forcing them.

### Project type detection
Read `_quarto.yml` to determine the type:

- Presence of `website:` → website project
- Presence of `book:` → book project
- Absence of `_quarto.yml` → offer to create it by asking the type

### Directory structures

**Website:**
```
project/
├── _quarto.yml
├── index.qmd
├── about.qmd
├── images/
├── css/
├── js/
├── references.bib
└── _site/           (generated)
```

**Book:**
```
project/
├── _quarto.yml
├── index.qmd
├── 01-introduction.qmd
├── 02-methods.qmd
├── references.bib
├── figures/
└── _book/           (generated)
```

## Quarto expertise

### YAML header
A valid header starts and ends with `---`. Common fields:
```yaml
---
title: "My document"
author: "Name"
date: today
format:
  html:
    toc: true
  pdf:
    documentclass: article
bibliography: references.bib
---
```

### Cross-references
- Figures: `@fig-label` with `#| label: fig-label`
- Tables: `@tbl-label` with `#| label: tbl-label`
- Equations: `@eq-label` with `$$ ... $$ {#eq-label}`
- Sections: `@sec-label` with `{#sec-label}`

### Code chunks (qmd format, hashpipe)
````markdown
```{r}
#| label: fig-example
#| fig-cap: "Caption"
#| echo: false
plot(x, y)
```
````

### Key differences Rmd → qmd
- Chunk options: `{r, echo=FALSE}` → `#| echo: false`
- Cross-references: `\@ref(fig:label)` → `@fig-label`
- YAML: `output:` → `format:`
- Callouts: `::: {.callout-note}` (native pandoc divs)

### Supported output formats
`html`, `pdf`, `docx`, `revealjs`, `beamer`, `pptx`, `epub`, `gfm`, `hugo-md`

## Scripts

Python scripts are available in `scripts/` for automated operations:

| Script | Function |
|--------|----------|
| `scripts/check_yaml.py` | Validate YAML headers |
| `scripts/check_math.py` | Check `$`/`$$` delimiters |
| `scripts/convert_rmd.py` | Convert .Rmd to .qmd |
| `scripts/check_bib.py` | Check citations vs .bib |
