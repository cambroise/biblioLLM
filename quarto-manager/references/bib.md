# /quarto:bib — Gestion de la bibliographie

## Objectif
Vérifier, nettoyer et maintenir la bibliographie d'un projet Quarto : cohérence entre citations et fichier .bib, intégration dans `_quarto.yml`.

## Procédure

### 1. Localiser le fichier .bib
Chercher `bibliography:` dans `_quarto.yml` ou dans les headers YAML des fichiers .qmd.

```bash
grep -r "bibliography:" <projet>/_quarto.yml <projet>/*.qmd
```

Si aucun fichier .bib n'est déclaré, le signaler et proposer d'ajouter `bibliography: references.bib` dans `_quarto.yml`.

### 2. Valider le fichier .bib
Vérifier :
- Le fichier existe au chemin déclaré
- La syntaxe BibTeX est valide (accolades appariées, champs obligatoires présents)
- Chaque entrée a une clé unique
- Les champs requis selon le type d'entrée :
  - `@article` : author, title, journal, year
  - `@book` : author/editor, title, publisher, year
  - `@inproceedings` : author, title, booktitle, year
  - `@misc` : author, title, year (minimum)

Utiliser le script :
```bash
python3 scripts/check_bib.py <references.bib> --qmd-dir <projet>/
```

### 3. Collecter les citations dans les fichiers .qmd
Scanner tous les fichiers .qmd pour extraire les citations :

- `@clé` — citation narrative
- `[@clé]` — citation entre parenthèses
- `[@clé1; @clé2]` — citations multiples
- `[-@clé]` — citation sans auteur (année seule)

Regex utile : `@([a-zA-Z0-9_][a-zA-Z0-9_:.-]*)` en filtrant les faux positifs (`@fig-`, `@tbl-`, `@eq-`, `@sec-`).

### 4. Croiser citations et entrées .bib

**Citations orphelines** (dans les .qmd mais pas dans le .bib) :
```
⚠️ Citations sans entrée .bib :
  - @smith2020 (dans 02-methodes.qmd:45)
  - @jones2019 (dans 03-resultats.qmd:12, 03-resultats.qmd:78)
```

**Entrées non utilisées** (dans le .bib mais jamais citées) :
```
ℹ️ Entrées .bib non citées :
  - @dupont2018
  - @martin2015
```

### 5. Vérifier l'intégration dans _quarto.yml

Le fichier `_quarto.yml` devrait contenir :
```yaml
bibliography: references.bib
csl: <style>.csl       # optionnel, style de citation
```

Si `bibliography:` est absent de `_quarto.yml` mais présent dans des headers individuels, proposer de centraliser :
- Ajouter `bibliography: references.bib` dans `_quarto.yml`
- Retirer les déclarations individuelles des headers .qmd

### 6. Vérifier le style CSL (optionnel)
Si un fichier `.csl` est déclaré :
- Vérifier qu'il existe
- Signaler s'il est absent (Quarto utilisera le style par défaut Chicago)

### 7. Proposer des corrections

Exemples de propositions :
```
## Corrections proposées

1. Ajouter l'entrée @smith2020 dans references.bib
   → Fournir les informations bibliographiques pour que je crée l'entrée
2. Retirer @dupont2018 du .bib (non utilisé) — optionnel
3. Ajouter `bibliography: references.bib` dans _quarto.yml
4. Corriger l'entrée @jones2019 : champ 'year' manquant

Confirmer les corrections à appliquer ?
```

### 8. Page de bibliographie (books)
Pour les projets book, vérifier qu'un fichier `references.qmd` existe avec :
```markdown
# Références {.unnumbered}
```

Et qu'il est listé dans `book: chapters:` de `_quarto.yml`.
