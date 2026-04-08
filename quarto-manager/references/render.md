# /quarto:render — Compilation du projet

## Objectif
Compiler un projet Quarto en détectant automatiquement le type de projet et en rapportant les erreurs de manière précise.

## Prérequis
Vérifier que Quarto est installé :
```bash
quarto --version
```

Si Quarto n'est pas disponible, informer l'utilisateur et proposer les instructions d'installation selon le système.

## Procédure

### 1. Détecter le type de projet
Lire `_quarto.yml` :
- `type: website` → `quarto render` produira `_site/`
- `type: book` → `quarto render` produira `_book/`
- Fichier unique → `quarto render <fichier.qmd>`

### 2. Vérification préalable (optionnelle mais recommandée)
Proposer d'exécuter `/quarto:check` avant la compilation pour détecter les problèmes en amont. Cela évite des erreurs de compilation difficiles à diagnostiquer.

### 3. Compiler

**Projet complet :**
```bash
cd <projet>/ && quarto render
```

**Fichier unique :**
```bash
quarto render <fichier.qmd>
```

**Format spécifique :**
```bash
quarto render --to html
quarto render --to pdf
quarto render --to docx
```

### 4. Analyser les erreurs
Si la compilation échoue, analyser la sortie d'erreur et la localiser précisément :

**Erreurs YAML :**
```
Erreur dans <fichier>:1-15 — Header YAML invalide
→ Vérifier l'indentation et les guillemets
```

**Erreurs Knitr/R :**
```
Erreur dans <fichier>, chunk '<label>' (ligne ~42)
→ <message d'erreur R>
→ Suggestion : vérifier que les packages sont installés
```

**Erreurs LaTeX (PDF) :**
```
Erreur LaTeX dans <fichier> (ligne ~78)
→ <message d'erreur LaTeX>
→ Suggestion : vérifier les commandes LaTeX et les packages
```

**Erreurs de références croisées :**
```
Avertissement : référence @fig-xxx non résolue dans <fichier>:25
→ Vérifier que le chunk avec label fig-xxx existe
```

### 5. Rapporter le résultat

**En cas de succès :**
```
✅ Compilation réussie

Sortie : _site/ (website) ou _book/ (book)
Format : HTML
Fichiers générés : 12 pages

Pour prévisualiser : quarto preview
```

**En cas d'échec :**
```
❌ Compilation échouée

Erreurs trouvées :
1. 02-methodes.qmd:42 — Chunk R : package 'ggplot2' non trouvé
2. 03-resultats.qmd:78 — Référence @fig-missing non résolue

Suggestions :
1. Installer le package : install.packages("ggplot2")
2. Ajouter un chunk avec #| label: fig-missing
```

### 6. Prévisualisation
Après une compilation réussie, proposer :
```bash
quarto preview
```

Cela lance un serveur local avec rechargement automatique — utile pour le développement itératif.

### 7. Compilation ciblée (projets volumineux)
Pour les projets avec beaucoup de fichiers, proposer de compiler uniquement le fichier modifié :
```bash
quarto render <fichier-modifié.qmd>
```

Puis recompiler le projet complet pour vérifier la cohérence globale.
