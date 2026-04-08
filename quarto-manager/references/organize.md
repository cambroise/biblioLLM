# /quarto:organize — Organisation de la structure du projet

## Objectif
Analyser et réorganiser la structure d'un projet Quarto pour qu'elle respecte les conventions standard.

## Procédure

### 1. Analyser la structure existante
```bash
ls -R <projet>/
```

Lire `_quarto.yml` s'il existe pour déterminer le type de projet (website ou book).

### 2. Déterminer le type de projet

Si `_quarto.yml` existe, le lire et chercher :
- `type: website` ou clé `website:` → website
- `type: book` ou clé `book:` → book

Si `_quarto.yml` n'existe pas, demander à l'utilisateur : « Ce projet est-il un website ou un book ? »

### 3. Vérifier la structure — Website

Éléments requis :
- `_quarto.yml` à la racine avec configuration `website:`
- `index.qmd` obligatoire (page d'accueil)

Structure recommandée :
```
projet/
├── _quarto.yml
├── index.qmd
├── about.qmd
├── pages/          (optionnel, pour les sous-pages)
├── images/         (images et figures)
├── css/            (feuilles de style personnalisées)
├── js/             (scripts JavaScript)
├── references.bib  (si bibliographie utilisée)
└── _site/          (généré, ne pas versionner)
```

Vérifications :
- Les images sont dans `images/` (pas éparpillées à la racine)
- Les fichiers CSS sont dans `css/`
- Les fichiers JS sont dans `js/`
- `_site/` est dans `.gitignore` si le projet est versionné
- La navbar dans `_quarto.yml` référence des fichiers existants

### 4. Vérifier la structure — Book

Éléments requis :
- `_quarto.yml` à la racine avec configuration `book:`
- `index.qmd` (page d'accueil / préface)
- Chapitres listés dans `book: chapters:`

Structure recommandée :
```
projet/
├── _quarto.yml
├── index.qmd
├── 01-introduction.qmd
├── 02-methodes.qmd
├── 03-resultats.qmd
├── 04-discussion.qmd
├── references.qmd    (page de bibliographie)
├── references.bib
├── figures/
└── _book/            (généré, ne pas versionner)
```

Vérifications :
- Les chapitres sont numérotés de manière séquentielle (01-, 02-, etc.)
- Tous les chapitres listés dans `_quarto.yml` existent comme fichiers
- `references.bib` existe si `bibliography:` est déclaré
- Les figures sont dans `figures/` (pas éparpillées)
- `_book/` est dans `.gitignore`

### 5. Proposer des corrections

Lister les écarts trouvés et proposer un plan de réorganisation. Exemples :

```
## Réorganisation proposée

1. Déplacer img/plot1.png → figures/plot1.png
2. Déplacer img/plot2.png → figures/plot2.png
3. Supprimer le dossier img/ (vide après déplacement)
4. Créer index.qmd (manquant)
5. Renommer chapitre1.qmd → 01-introduction.qmd
6. Mettre à jour _quarto.yml pour refléter les nouveaux noms

Confirmer avant d'exécuter ? [oui/non]
```

Ne rien exécuter sans confirmation explicite.

### 6. Exécuter la réorganisation
Après confirmation :
- Créer un backup du projet
- Déplacer les fichiers
- Mettre à jour les chemins dans `_quarto.yml`
- Mettre à jour les chemins d'images dans les fichiers .qmd (ex: `![](img/plot.png)` → `![](figures/plot.png)`)
- Vérifier que rien n'est cassé avec `/quarto:check`

### 7. Créer _quarto.yml si manquant

**Website minimal :**
```yaml
project:
  type: website

website:
  title: "Mon Site"
  navbar:
    left:
      - href: index.qmd
        text: Accueil

format:
  html:
    theme: cosmo
    toc: true
```

**Book minimal :**
```yaml
project:
  type: book

book:
  title: "Mon Livre"
  author: "Auteur"
  chapters:
    - index.qmd
    - 01-introduction.qmd
    - 02-methodes.qmd
    - references.qmd

bibliography: references.bib

format:
  html:
    theme: cosmo
  pdf:
    documentclass: scrreprt
```
