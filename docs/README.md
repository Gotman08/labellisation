# Documentation du Projet Labellisation

Ce dossier contient toute la documentation du projet en plusieurs formats.

## 📁 Structure

```
docs/
├── rapport/
│   ├── rapport.tex        # Rapport LaTeX (version PDF compilable)
│   └── RAPPORT.md         # Rapport Markdown (lecture en ligne)
│
└── presentation/
    ├── presentation.tex   # Slides Beamer LaTeX
    └── PRESENTATION.md    # Slides Markdown (reveal.js / Marp compatible)
```

## 📄 Formats disponibles

### Version LaTeX (pour PDF)

Les fichiers `.tex` sont conçus pour être compilés en PDF de haute qualité pour la remise officielle.

**Avantages :**
- ✅ Qualité professionnelle
- ✅ Formules mathématiques bien rendues
- ✅ Pagination et mise en forme académique
- ✅ Bibliographie automatique

### Version Markdown (pour lecture en ligne)

Les fichiers `.md` sont parfaits pour une lecture rapide sur GitHub, GitLab, ou tout éditeur de texte.

**Avantages :**
- ✅ Lecture directe sans compilation
- ✅ Prévisualisation GitHub
- ✅ Modification facile
- ✅ Compatible avec de nombreux outils

## 🔨 Compilation LaTeX

### Rapport

```bash
cd docs/rapport
pdflatex rapport.tex
pdflatex rapport.tex  # Deux fois pour les références
```

Résultat : `rapport.pdf`

### Présentation

```bash
cd docs/presentation
pdflatex presentation.tex
pdflatex presentation.tex
```

Résultat : `presentation.pdf`

### Prérequis LaTeX

Vous aurez besoin d'une distribution LaTeX installée :

- **Windows :** MiKTeX ou TeX Live
- **macOS :** MacTeX
- **Linux :** TeX Live (`sudo apt install texlive-full`)

Packages requis :
- `babel` (français)
- `amsmath` / `amssymb` (maths)
- `graphicx` (images)
- `listings` (code)
- `beamer` (pour la présentation)

## 📖 Lecture des Markdown

### Sur GitHub/GitLab

Les fichiers `.md` s'affichent automatiquement avec une mise en forme élégante.

### Dans VSCode

1. Ouvrir le fichier `.md`
2. Appuyer sur `Ctrl+Shift+V` (ou `Cmd+Shift+V` sur Mac)
3. Ou cliquer sur l'icône de prévisualisation en haut à droite

### Convertir Markdown en slides

#### Avec Marp (recommandé pour PRESENTATION.md)

```bash
# Installer Marp CLI
npm install -g @marp-team/marp-cli

# Convertir en PDF
marp PRESENTATION.md -o presentation-marp.pdf

# Convertir en HTML
marp PRESENTATION.md -o presentation.html
```

#### Avec reveal.js

```bash
# Utiliser pandoc
pandoc PRESENTATION.md -t revealjs -s -o presentation-reveal.html
```

#### Avec mdp (terminal)

```bash
# Installer mdp
sudo apt install mdp  # Linux
brew install mdp      # macOS

# Présenter dans le terminal
mdp PRESENTATION.md
```

## 📝 Contenu des documents

### Rapport (RAPPORT.md / rapport.tex)

Le rapport complet contient :

1. **Introduction**
   - Contexte du projet
   - Objectifs
   - Méthodes implémentées

2. **Fondements Théoriques**
   - Topologie discrète (CM03)
   - Modèles mathématiques (CM05)
   - Adjacence et connexité

3. **Méthodologie et Implémentation**
   - Description détaillée des 4 algorithmes
   - Pseudo-code
   - Complexités

4. **Résultats et Analyse**
   - Benchmarks
   - Comparaisons
   - Tableaux et graphiques

5. **Conclusion**
   - Bilan
   - Perspectives

### Présentation (PRESENTATION.md / presentation.tex)

La présentation (15 minutes) contient :

1. **Introduction** (2-3 min)
   - Contexte et objectif
   - Applications

2. **Théorie** (3-4 min)
   - Topologie discrète
   - Modèles mathématiques

3. **Les 4 Algorithmes** (5-6 min)
   - Two-Pass
   - Union-Find
   - Kruskal
   - Prim

4. **Résultats** (3-4 min)
   - Benchmarks
   - Comparaisons

5. **Conclusion** (2 min)
   - Bilan
   - Perspectives

## ✏️ Modification des documents

### Pour le rapport

1. **Version LaTeX :** Modifier `rapport.tex`
2. **Version Markdown :** Modifier `RAPPORT.md`

### Pour la présentation

1. **Version LaTeX :** Modifier `presentation.tex`
2. **Version Markdown :** Modifier `PRESENTATION.md`

### Synchronisation

⚠️ **Important :** Les versions LaTeX et Markdown ne sont pas automatiquement synchronisées. Si vous modifiez l'une, pensez à mettre à jour l'autre.

## 📊 Ajout des résultats

Les fichiers contiennent des placeholders (`XX.XX`, `[À compléter]`) pour vos résultats :

### Dans le rapport

```markdown
| Algorithme  | Moyenne (ms) | Écart-type | Speedup |
|-------------|--------------|------------|---------|
| Two-Pass    | XX.XX        | X.XX       | 1.0x    |  ← À remplacer
| Union-Find  | XX.XX        | X.XX       | X.Xx    |  ← À remplacer
```

### Comment obtenir ces résultats

```bash
# Compiler et exécuter le benchmark
cd build
./benchmark ../images/input/*.pgm

# Copier les résultats dans le rapport
```

## 🎯 Checklist avant remise

### Pour le rapport (1er décembre)

- [ ] Compléter les résultats de benchmark
- [ ] Ajouter la configuration de test (CPU, RAM)
- [ ] Compléter la répartition du travail
- [ ] Vérifier toutes les formules mathématiques
- [ ] Compiler le PDF LaTeX sans erreur
- [ ] Vérifier la numérotation des pages
- [ ] Ajouter des images/graphiques si disponibles

### Pour la présentation (9 décembre)

- [ ] Vérifier le timing (15 min = 5 min par personne)
- [ ] Préparer la démonstration du programme
- [ ] Tester les slides (LaTeX ou Markdown)
- [ ] Préparer les réponses aux questions fréquentes
- [ ] S'entraîner à présenter

## 🛠️ Outils recommandés

### Éditeurs Markdown

- **VSCode** (avec extension Markdown All in One)
- **Typora** (WYSIWYG)
- **Mark Text** (open source)
- **GitHub/GitLab** (en ligne)

### Éditeurs LaTeX

- **Overleaf** (en ligne, collaboratif)
- **TeXstudio** (desktop, multiplateforme)
- **VSCode** (avec extension LaTeX Workshop)
- **TeXShop** (macOS)

### Présentations

- **Marp** (Markdown → slides)
- **reveal.js** (HTML slides)
- **mdp** (terminal slides)
- **Beamer** (LaTeX slides)

## 📚 Ressources

- [Guide LaTeX Beamer](https://www.overleaf.com/learn/latex/Beamer)
- [Markdown Guide](https://www.markdownguide.org/)
- [Marp Documentation](https://marpit.marp.app/)
- [Reveal.js Documentation](https://revealjs.com/)

## ❓ Aide

En cas de problème :

1. Vérifier que tous les packages LaTeX sont installés
2. Vérifier que les chemins de fichiers sont corrects
3. Consulter les logs d'erreur LaTeX (fichier `.log`)
4. Pour Markdown, vérifier la syntaxe avec un linter

---

**Bon courage pour votre présentation ! 🚀**
