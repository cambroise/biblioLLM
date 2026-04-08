# Lint — Vault health audit

Inspects the vault, detects structural and content issues, and produces an actionable report.

**Usage**: `/lint` (full audit) or `/lint <category>` to target: `links`, `orphans`, `stale`, `gaps`, `contradictions`.

---

## Step 1 — Collect vault state

Read `index.md` for the full map. Read `log.md` to identify recent additions (candidates for contradictions with existing content).

```bash
# Identify the vault: derive $VAULT_DIR from papis list --libraries
papis list --libraries
export PAPIS_LIB=<library-name>

# Markdown pages in the vault
find "$VAULT_DIR/Bibliography" -name "*.md" | grep -v CLAUDE
find "$VAULT_DIR/Notes" -name "*.md" -o -name "*.qmd"

# Pages with no incoming links (potential orphans)
grep -r "\[\[" "$VAULT_DIR" --include="*.md" | grep -o "\[\[[^\]]*\]\]" | sort | uniq -c | sort -rn
```

---

## Step 2 — Checks to perform

Review each category:

### `orphans` — Pages with no incoming links
- List pages in `index.md` that are not referenced in any other `.md` file
- Also flag pages present on disk but absent from `index.md`

### `links` — Broken links
- For each `[[wikilink]]` found in `.md` files, verify that a matching page exists in the vault

### `stale` — Potentially outdated claims
- Compare dates of entries in `log.md`: if a recent source contradicts or refines an older note, flag it
- Look for notes that cite a method without mentioning its known variants or successors in the vault

### `gaps` — Concepts mentioned without their own page
- List `[[wikilinks]]` pointing to non-existent pages
- Identify frequent technical terms (≥ 3 occurrences in the vault) without a dedicated page

### `contradictions` — Conflicting claims
- Look for opposing claims about the same concept in different pages (e.g. algorithmic complexity, model assumptions)

---

## Step 3 — Produce the report

Report format:

```markdown
# Lint report — YYYY-MM-DD

## Summary
- X orphans | Y broken links | Z gaps | W stale alerts | V contradictions

## Papis articles without a markdown note
- ...

## Orphans
- [[page]] — no incoming links found

## Broken links
- `[[target]]` in [[source-page]] — target page missing

## Gaps (concepts without a page)
- "term" — mentioned N times, notably in [[page1]], [[page2]]

## Stale alerts
- [[old-note]] — claim X potentially contradicted by [[recent-source]]

## Contradictions
- [[pageA]] says X; [[pageB]] says Y — to reconcile

## New questions to investigate
- …

## Sources to find
- …
```

---

## Step 4 — Proposed actions

For each issue detected, propose a concrete action:
- Orphan → suggest a `[[wikilink]]` to add in an existing page
- Broken link → propose creating a stub or correcting the link
- Papis article without a note → write the missing markdown note and add it to `index.md`
- Important gap → propose `/ingest <source>` or creation of a concept page
- Contradiction → propose a reconciliation or an arbitration note

Ask the user which actions to execute.

---

## Step 5 — Log the audit

Append to `log.md`:

```
## [YYYY-MM-DD] lint | Health audit

- **Result**: X orphans, Y broken links, Z gaps, W alerts
- **Actions taken**: …
```
