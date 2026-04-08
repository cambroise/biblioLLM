# Query — Search the vault

Answers a question by exploring the vault, synthesizes the findings, and offers to save the answer as a new page.

**Usage**: `/query <question>` — the question can be open-ended ("how does LiNGAM handle latent variables?"), comparative ("compare NOTEARS and DAGMA"), or exploratory ("what connections exist between Bell inequalities and ICA?").

---

## Step 1 — Read the index

Read `index.md` first to identify candidate pages. Do not search blindly.

---

## Step 2 — Collect relevant pages

From the index, read pages directly related to the question. Use Grep if needed to find occurrences of key terms in `Bibliography/` and `Notes/`:

```bash
# $VAULT_DIR is derived from the active library (papis list --libraries)
grep -r "<term>" "$VAULT_DIR/Bibliography" --include="*.md" -l
grep -r "<term>" "$VAULT_DIR/Notes" --include="*.md" -l
```

Read only the pages that are truly relevant — do not read everything.

---

## Step 3 — Synthesize the answer

Choose the format best suited to the question:

| Question type | Suggested format |
|---------------|-----------------|
| Conceptual explanation | Structured markdown page |
| Method comparison | Markdown table |
| Presentation / lecture | Marp slideshow (`.md` with `marp: true`) |
| Quantitative data | matplotlib script + figure |
| Connections between ideas | Narrative page with `[[wikilinks]]` |

The answer must:
- Cite sources with `[[wikilinks]]` to the pages read
- Explicitly state what is established in the vault vs what is an inference
- Flag gaps ("this question would require reading X")

---

## Step 4 — Offer to save the answer to the vault

After the answer, always propose:

> "Would you like me to save this answer to the vault under `Notes/<title>.md`?"

If yes:
- Create the page with tags `claude` and `query`
- Add the `[[wikilink]]` from source pages to this new page
- Update `index.md` (section "Thematic notes") and `log.md`:

```
## [YYYY-MM-DD] create | <Answer title>

- **Type**: query
- **Question**: <question asked>
- **Pages read**: [[page1]], [[page2]]
- **Action**: answer saved to `Notes/<title>.md`
```
