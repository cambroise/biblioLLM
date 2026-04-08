# /quarto:convert — Conversion Rmd → qmd

## Objectif
Convertir des fichiers .Rmd en .qmd en adaptant la syntaxe tout en préservant le contenu.

## Procédure

### 1. Identifier les fichiers à convertir
```bash
find <projet>/ -name "*.Rmd" | sort
```

Si l'utilisateur précise un fichier, se limiter à celui-ci. Sinon, lister et demander confirmation.

### 2. Créer un backup
Avant toute modification, sauvegarder les originaux :
```bash
mkdir -p <projet>/backup/
cp <fichier>.Rmd <projet>/backup/<fichier>.Rmd.bak
```

Informer l'utilisateur : « Les originaux ont été sauvegardés dans backup/ ».

### 3. Convertir le YAML header

| Rmd | qmd |
|-----|-----|
| `output:` | `format:` |
| `html_document` | `html` |
| `pdf_document` | `pdf` |
| `word_document` | `docx` |
| `bookdown::html_document2` | `html` |
| `bookdown::pdf_document2` | `pdf` |
| `xaringan::moon_reader` | `revealjs` (approximation) |

Conserver les sous-options en adaptant les noms :
```yaml
# Rmd
output:
  html_document:
    toc: true
    toc_float: true

# qmd
format:
  html:
    toc: true
    toc-location: left
```

Note : `toc_float: true` n'a pas d'équivalent direct. Utiliser `toc-location: left` comme approximation.

### 4. Convertir les chunks de code

Transformer les options inline en hashpipe :

```
# Rmd
{r nom-chunk, echo=FALSE, fig.cap="Légende", fig.width=8}

# qmd
{r}
#| label: nom-chunk
#| echo: false
#| fig-cap: "Légende"
#| fig-width: 8
```

Règles de conversion des options :
- `echo=FALSE` → `#| echo: false` (minuscules)
- `fig.cap=` → `#| fig-cap:` (point → tiret)
- `fig.width=` → `#| fig-width:`
- `fig.height=` → `#| fig-height:`
- `message=FALSE` → `#| message: false`
- `warning=FALSE` → `#| warning: false`
- `results='hide'` → `#| output: false`
- `results='asis'` → `#| output: asis`
- `include=FALSE` → `#| include: false`
- `eval=FALSE` → `#| eval: false`
- `cache=TRUE` → `#| cache: true`

Le nom du chunk devient `#| label: nom-chunk`.

### 5. Convertir les références croisées

| Rmd (bookdown) | qmd |
|-----------------|-----|
| `\@ref(fig:label)` | `@fig-label` |
| `\@ref(tab:label)` | `@tbl-label` |
| `\@ref(eq:label)` | `@eq-label` |
| `\@ref(sec:label)` | `@sec-label` |
| `(ref:label)` | Texte inline ou `fig-cap` |

### 6. Convertir les callouts et divs

```markdown
# Rmd (custom divs ou blocs)
::: {.rmdnote}
Contenu
:::

# qmd
::: {.callout-note}
Contenu
:::
```

Mappings courants : `.rmdnote` → `.callout-note`, `.rmdwarning` → `.callout-warning`, `.rmdtip` → `.callout-tip`.

### 7. Convertir les délimiteurs mathématiques
Vérifier que les maths utilisent `$` et `$$` (pas `\(` / `\[`). Convertir si nécessaire.

### 8. Sauvegarder le fichier converti
Écrire le résultat en `.qmd` dans le même répertoire. Demander confirmation avant d'écrire.

### 9. Utiliser le script automatisé
Pour une conversion rapide :
```bash
python3 scripts/convert_rmd.py <fichier.Rmd> [--output <fichier.qmd>] [--backup-dir backup/]
```

Le script gère les étapes 2 à 7 automatiquement. Vérifier le résultat manuellement après conversion.
