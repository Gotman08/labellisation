# Projet Labellisation des Composantes Connexes

Projet de traitement d'image implémentant différents algorithmes de labellisation des composantes connexes d'une image binaire.

## 🚀 Quick Start

```bash
# 1. Compiler le projet
mkdir build && cd build
cmake .. && make

# 2. Exécuter les tests
./test_algorithms

# 3. Tester un algorithme
./labellisation ../images/input/test.pgm ../images/output/result.pgm two_pass 4

# 4. Comparer les performances
./benchmark ../images/input/*.pgm
```

Pour plus de détails, voir [USAGE.md](USAGE.md).

## ✨ Features

### Algorithmes implémentés
- ✅ **Two-Pass** : Algorithme classique en deux passes avec table d'équivalence
- ✅ **Union-Find** : Structure Disjoint-Set avec path compression et union by rank
- ✅ **Kruskal** : Approche par graphe (Minimum Spanning Tree)
- ✅ **Prim** : Exploration BFS pour labellisation

### Caractéristiques techniques
- 🚫 **Aucune bibliothèque externe** : Tout codé from scratch (pas d'OpenCV)
- 🔧 **Fonctions manuelles** : min/max/mean/sqrt implémentés à la main
- 📁 **I/O custom** : Lecture/écriture PGM/PPM sans dépendances
- ⚡ **Optimisé** : Code C++17 optimisé pour la performance
- 📖 **Bien documenté** : Commentaires détaillés référençant les cours (CM03, CM05)

### Outils inclus
- 🧪 **Tests unitaires** : Validation complète de chaque algorithme
- 📊 **Benchmark** : Comparaison automatisée des performances
- 📄 **Documentation** : Rapport LaTeX/Markdown + présentation

## Structure du projet

```
labellisation/
├── src/
│   ├── core/              # Structures de base (Image, Pixel)
│   ├── io/                # Lecture/écriture d'images (PGM/PPM)
│   ├── algorithms/        # Implémentations des 4 algorithmes
│   ├── utils/             # Fonctions utilitaires
│   └── main.cpp          # Programme principal
├── tests/                # Tests unitaires
├── benchmarks/           # Comparaison de performance
├── images/               # Images de test
│   ├── input/           # Images d'entrée (à ajouter)
│   └── output/          # Résultats labellisés
├── docs/                # Documentation (LaTeX + Markdown)
│   ├── rapport/         # Rapport complet (PDF + MD)
│   └── presentation/    # Slides de présentation (PDF + MD)
├── CMakeLists.txt       # Configuration CMake
├── README.md            # Ce fichier
└── USAGE.md             # Guide d'utilisation détaillé
```

## Compilation

```bash
mkdir build
cd build
cmake ..
make
```

## Utilisation

```bash
# Lancer le programme principal
./labellisation <image_input> <image_output> <algorithme> <connexite>

# Algorithmes disponibles: two_pass, union_find, kruskal, prim
# Connexité: 4 ou 8

# Exemple
./labellisation ../images/input/test.pgm ../images/output/result.pgm two_pass 4
```

## Tests

```bash
# Exécuter les tests unitaires
./test_two_pass
./test_union_find
./test_kruskal
./test_prim
```

## Benchmark

```bash
# Comparer les performances des algorithmes
./benchmark
```

## Documentation

### Formats disponibles

La documentation est disponible en **deux formats** :

#### 📄 LaTeX (pour PDF académique)
- `docs/rapport/rapport.tex` - Rapport complet
- `docs/presentation/presentation.tex` - Slides Beamer

Pour compiler :
```bash
cd docs/rapport
pdflatex rapport.tex
pdflatex rapport.tex  # Deux fois pour les références
```

#### 📝 Markdown (pour lecture en ligne)
- `docs/rapport/RAPPORT.md` - Rapport complet
- `docs/presentation/PRESENTATION.md` - Slides

Lisible directement sur GitHub ou avec n'importe quel éditeur Markdown.

Voir [docs/README.md](docs/README.md) pour plus de détails.

## Contraintes d'implémentation

- ✅ Aucune bibliothèque externe (OpenCV, etc.)
- ✅ Toutes les fonctions sont implémentées manuellement
- ✅ Code optimisé pour la performance
- ✅ Commentaires détaillés référençant les cours (CM03, CM05)

## Auteurs

- **Romain Despoullain**
- **Nicolas Marano**
- **Amin Braham**

## Date de rendu

- 📅 **Compte rendu** : 1er décembre
- 🎤 **Présentation orale** : 9 décembre

## 📋 Prochaines étapes

### Pour commencer
1. **Ajouter des images de test** dans `images/input/`
   - Format PGM recommandé (simple et sans compression)
   - Ou convertir vos images : `convert input.jpg output.pgm`

2. **Compiler et tester**
   ```bash
   mkdir build && cd build
   cmake .. && make
   ./test_algorithms
   ```

3. **Exécuter les benchmarks** sur vos images
   ```bash
   ./benchmark ../images/input/*.pgm
   ```

### Pour le rapport (avant le 1er décembre)
1. **Compléter les résultats** dans `docs/rapport/RAPPORT.md` ou `rapport.tex`
   - Copier les résultats du benchmark
   - Ajouter votre configuration (CPU, RAM)
   - Compléter la répartition du travail

2. **Compiler le PDF**
   ```bash
   cd docs/rapport
   pdflatex rapport.tex
   pdflatex rapport.tex
   ```

### Pour la présentation (9 décembre)
1. **Préparer les slides** dans `docs/presentation/`
   - Version LaTeX : `presentation.tex`
   - Ou version Markdown : `PRESENTATION.md`

2. **S'entraîner**
   - 15 minutes au total (5 min par personne)
   - Préparer une démo du programme
   - Anticiper les questions

## 📚 Ressources

- 📖 **Guide d'utilisation détaillé** : [USAGE.md](USAGE.md)
- 📄 **Documentation complète** : [docs/](docs/)
- 💻 **Code source** : [src/](src/)
- 🧪 **Tests** : [tests/](tests/)

## 🤝 Contribution

Ce projet a été réalisé en équipe. Pensez à :
- Compléter la section "Répartition du travail" dans le rapport
- Indiquer qui a fait quoi (algorithmes, tests, documentation, etc.)
