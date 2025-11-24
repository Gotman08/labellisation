# Projet Labellisation des Composantes Connexes

Projet de traitement d'image implementant differents algorithmes de labellisation des composantes connexes d'une image binaire.

## Quick Start

```bash
# 1. Installer les dependances
pip install numpy opencv-python

# 2. Tester un algorithme (supporte JPEG, PNG, BMP, PGM, PPM, etc.)
python src/main.py images/input/test.jpg images/output/result.png two_pass 4

# 3. Comparer les performances
python benchmarks/benchmark.py images/input/*.png
```

Pour plus de details, voir [USAGE.md](USAGE.md).

## Features

### Algorithmes implementes
- **Two-Pass** : Algorithme classique en deux passes avec table d'equivalence
- **Union-Find** : Structure Disjoint-Set avec path compression et union by rank
- **Kruskal** : Approche par graphe (Minimum Spanning Tree)
- **Prim** : Exploration BFS pour labellisation

### Caracteristiques techniques
- **Formats supportes** : JPEG, PNG, BMP, TIFF, GIF, WEBP, PGM, PPM (via OpenCV)
- **Dependance minimale** : NumPy/OpenCV uniquement pour charger les images
- **Fonctions manuelles** : min/max/mean/sqrt et toutes les operations implementees a la main
- **I/O flexible** : Lecture/ecriture multi-formats
- **Python 3** : Code Python optimise
- **Bien documente** : Commentaires detailles referencant les cours (CM03, CM05)

### Outils inclus
- **Benchmark** : Comparaison automatisee des performances
- **Documentation** : Rapport LaTeX/Markdown + presentation

## Structure du projet

```
labellisation/
├── src/
│   ├── __init__.py        # Package principal
│   ├── core/              # Structures de base (Image, Pixel)
│   │   ├── __init__.py
│   │   └── image.py
│   ├── io/                # Lecture/ecriture d'images (PGM/PPM)
│   │   ├── __init__.py
│   │   └── image_io.py
│   ├── algorithms/        # Implementations des 4 algorithmes
│   │   ├── __init__.py
│   │   ├── two_pass.py
│   │   ├── union_find.py
│   │   ├── kruskal.py
│   │   └── prim.py
│   ├── utils/             # Fonctions utilitaires
│   │   ├── __init__.py
│   │   └── utils.py
│   └── main.py            # Programme principal
├── benchmarks/            # Comparaison de performance
│   └── benchmark.py
├── images/                # Images de test
│   ├── input/             # Images d'entree (a ajouter)
│   └── output/            # Resultats labellises
├── docs/                  # Documentation (LaTeX + Markdown)
│   ├── rapport/           # Rapport complet (PDF + MD)
│   └── presentation/      # Slides de presentation (PDF + MD)
├── README.md              # Ce fichier
└── USAGE.md               # Guide d'utilisation detaille
```

## Installation

```bash
# Installer les dependances
pip install numpy opencv-python
```

## Utilisation

```bash
# Lancer le programme principal
python src/main.py <image_input> <image_output> <algorithme> <connexite>

# Formats supportes: JPEG, PNG, BMP, TIFF, GIF, WEBP, PGM, PPM
# Algorithmes disponibles: two_pass, union_find, kruskal, prim
# Connexite: 4 ou 8

# Exemples
python src/main.py photo.jpg result.png two_pass 4
python src/main.py image.png output.pgm union_find 8
```

## Benchmark

```bash
# Comparer les performances des algorithmes
python benchmarks/benchmark.py images/input/*.pgm
```

## Documentation

### Formats disponibles

La documentation est disponible en **deux formats** :

#### LaTeX (pour PDF academique)
- `docs/rapport/rapport.tex` - Rapport complet
- `docs/presentation/presentation.tex` - Slides Beamer

Pour compiler :
```bash
cd docs/rapport
pdflatex rapport.tex
pdflatex rapport.tex  # Deux fois pour les references
```

#### Markdown (pour lecture en ligne)
- `docs/rapport/RAPPORT.md` - Rapport complet
- `docs/presentation/PRESENTATION.md` - Slides

Lisible directement sur GitHub ou avec n'importe quel editeur Markdown.

Voir [docs/README.md](docs/README.md) pour plus de details.

## Contraintes d'implementation

- Dependance minimale (uniquement NumPy)
- Toutes les fonctions utilitaires sont implementees manuellement
- Code optimise pour la lisibilite et la performance
- Commentaires detailles referencant les cours (CM03, CM05)

## Auteurs

- **Romain Despoullain**
- **Nicolas Marano**
- **Amin Braham**

## Date de rendu

- **Compte rendu** : 1er decembre
- **Presentation orale** : 9 decembre

## Prochaines etapes

### Pour commencer
1. **Ajouter des images de test** dans `images/input/`
   - Format PGM recommande (simple et sans compression)
   - Ou convertir vos images : `convert input.jpg output.pgm`

2. **Tester le programme**
   ```bash
   python src/main.py images/input/test.pgm images/output/result.pgm two_pass 4
   ```

3. **Executer les benchmarks** sur vos images
   ```bash
   python benchmarks/benchmark.py images/input/*.pgm
   ```

### Pour le rapport (avant le 1er decembre)
1. **Completer les resultats** dans `docs/rapport/RAPPORT.md` ou `rapport.tex`
   - Copier les resultats du benchmark
   - Ajouter votre configuration (CPU, RAM)
   - Completer la repartition du travail

2. **Compiler le PDF**
   ```bash
   cd docs/rapport
   pdflatex rapport.tex
   pdflatex rapport.tex
   ```

### Pour la presentation (9 decembre)
1. **Preparer les slides** dans `docs/presentation/`
   - Version LaTeX : `presentation.tex`
   - Ou version Markdown : `PRESENTATION.md`

2. **S'entrainer**
   - 15 minutes au total (5 min par personne)
   - Preparer une demo du programme
   - Anticiper les questions

## Ressources

- **Guide d'utilisation detaille** : [USAGE.md](USAGE.md)
- **Documentation complete** : [docs/](docs/)
- **Code source** : [src/](src/)

## Contribution

Ce projet a ete realise en equipe. Pensez a :
- Completer la section "Repartition du travail" dans le rapport
- Indiquer qui a fait quoi (algorithmes, tests, documentation, etc.)
