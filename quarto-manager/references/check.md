# /quarto:check — Vérification de syntaxe et format

## Objectif
Analyser les fichiers .qmd et .Rmd d'un projet Quarto pour détecter les erreurs de syntaxe, les incohérences de formatage et les problèmes potentiels avant compilation.

## Procédure

### 1. Identifier les fichiers à vérifier
Lister tous les fichiers `.qmd` et `.Rmd` du projet. Si l'utilisateur précise un fichier, se limiter à celui-ci.

```bash
find <projet>/ -name "*.qmd" -o -name "*.Rmd" | sort
```

### 2. Valider les headers YAML
Pour chaque fichier, vérifier :

- Le header commence par `---` (ligne 1) et se termine par `---`
- Le champ `title:` est présent
- Les valeurs sont correctement quotées (les titres avec `:` doivent être entre guillemets)
- Les indentations sont cohérentes (2 espaces par niveau)
- Les champs `format:` utilisent des clés valides (`html`, `pdf`, `docx`, `revealjs`, etc.)
- Le champ `bibliography:` pointe vers un fichier existant

Utiliser `scripts/check_yaml.py` pour automatiser :
```bash
python3 scripts/check_yaml.py <fichier.qmd>
```

### 3. Vérifier les délimiteurs mathématiques
Les préférences utilisateur imposent `$...$` pour l'inline et `$$...$$` pour le display.

Vérifier :
- Pas de `\(...\)` ni `\[...\]` (syntaxe LaTeX brute)
- Les `$` sont appariés (nombre pair par ligne pour l'inline)
- Les `$$` sont appariés (ouverture et fermeture sur des lignes séparées ou la même ligne)
- Pas de `$` isolé qui pourrait créer une ambiguïté

Utiliser `scripts/check_math.py` :
```bash
python3 scripts/check_math.py <fichier.qmd>
```

### 4. Vérifier les références croisées
Chercher toutes les références `@fig-`, `@tbl-`, `@eq-`, `@sec-` et vérifier que chaque cible existe :

- `@fig-xxx` → un chunk avec `#| label: fig-xxx` doit exister
- `@tbl-xxx` → un chunk avec `#| label: tbl-xxx` doit exister
- `@eq-xxx` → une équation avec `{#eq-xxx}` doit exister
- `@sec-xxx` → un titre avec `{#sec-xxx}` doit exister

Rapporter les références orphelines (cible manquante) et les labels non référencés.

### 5. Vérifier les chunks de code
Pour les fichiers .qmd :
- Les chunks utilisent le format hashpipe : `#| option: valeur`
- Les options booléennes sont en minuscules : `true`/`false` (pas `TRUE`/`FALSE`)
- Les labels de chunk sont uniques dans le fichier

Pour les fichiers .Rmd :
- Les chunks utilisent le format classique : `{r, option=value}`
- Signaler que la conversion en .qmd est recommandée

### 6. Vérifier _quarto.yml
Si le fichier existe :
- Syntaxe YAML valide
- Les fichiers référencés dans `chapters:` ou `navbar:` existent
- Le `type:` est cohérent avec la structure du répertoire

### 7. Rapport
Présenter les résultats de manière structurée :

```
## Résultat de la vérification

### ✅ Fichiers valides
- index.qmd
- 01-introduction.qmd

### ⚠️ Avertissements
- about.qmd:15 — Délimiteur math `\(` détecté, utiliser `$` à la place
- 02-methodes.qmd:42 — Référence @fig-resultats sans cible

### ❌ Erreurs
- 03-resultats.qmd:1 — Header YAML mal formé (pas de `---` fermant)
```
