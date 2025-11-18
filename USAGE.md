# Guide d'utilisation - Labellisation

## Compilation

### Prérequis
- CMake (version 3.10 minimum)
- Compilateur C++17 (g++, clang++, MSVC)

### Étapes de compilation

```bash
# 1. Créer un dossier de build
mkdir build
cd build

# 2. Configurer avec CMake
cmake ..

# 3. Compiler
cmake --build .
# Ou sur Unix/Linux/Mac :
make

# 4. (Optionnel) Mode Release pour optimisation maximale
cmake -DCMAKE_BUILD_TYPE=Release ..
make
```

Les exécutables seront créés dans le dossier `build/`.

## Utilisation

### Programme principal

```bash
./labellisation <input> <output> <algorithm> <connectivity>
```

**Arguments :**
- `input` : Chemin de l'image d'entrée (PGM ou PPM)
- `output` : Chemin de l'image de sortie (PGM)
- `algorithm` : `two_pass` | `union_find` | `kruskal` | `prim`
- `connectivity` : `4` | `8`

**Exemples :**

```bash
# Labellisation avec Two-Pass en 4-connexité
./labellisation ../images/input/test.pgm ../images/output/result.pgm two_pass 4

# Labellisation avec Union-Find en 8-connexité
./labellisation ../images/input/test.pgm ../images/output/result.pgm union_find 8

# Labellisation avec Kruskal
./labellisation ../images/input/test.pgm ../images/output/result.pgm kruskal 4

# Labellisation avec Prim
./labellisation ../images/input/test.pgm ../images/output/result.pgm prim 4
```

### Tests unitaires

```bash
# Exécuter tous les tests
./test_algorithms

# Les tests vérifient :
# - Cohérence entre les 4 algorithmes
# - Cas limites (image vide, pixel unique)
# - Différence 4-conn vs 8-conn
```

### Benchmark

```bash
# Comparer les performances sur une ou plusieurs images
./benchmark ../images/input/image1.pgm ../images/input/image2.pgm

# Le benchmark affiche :
# - Temps moyen d'exécution (sur 10 runs)
# - Écart-type
# - Speedup relatif
# - Nombre de composantes trouvées
```

## Préparation des images

### Format PGM (recommandé)

Le projet utilise le format PGM (Portable GrayMap) qui est :
- Simple (pas de compression)
- Lisible en texte (format P2) ou binaire (format P5)
- Supporté par de nombreux outils

### Créer une image PGM de test

Vous pouvez créer une image PGM simple avec n'importe quel éditeur de texte :

```pgm
P2
# Test image
5 5
255
0 0 0 0 0
0 255 255 0 0
0 255 255 0 0
0 0 0 255 0
0 0 0 0 0
```

Enregistrez ce fichier sous `test.pgm`.

### Convertir d'autres formats en PGM

Si vous avez des images PNG/JPG, utilisez ImageMagick ou GIMP :

```bash
# Avec ImageMagick
convert input.png -colorspace Gray output.pgm

# Ou avec GIMP
# File → Export As → Sélectionner PGM
```

## Visualiser les résultats

Les images labellisées sont sauvegardées en PGM avec des niveaux de gris.
Vous pouvez les visualiser avec :

- **ImageMagick** : `display output.pgm`
- **GIMP** : Ouvrir directement le fichier PGM
- **VSCode** : Extensions d'affichage d'images
- Convertir en PNG : `convert output.pgm output.png`

## Compilation du rapport LaTeX

```bash
cd docs/rapport
pdflatex rapport.tex
pdflatex rapport.tex  # Deux fois pour les références

cd ../presentation
pdflatex presentation.tex
pdflatex presentation.tex
```

## Problèmes courants

### Erreur de compilation C++17

Si vous obtenez des erreurs liées à C++17 :
```bash
# Vérifier la version de votre compilateur
g++ --version

# Forcer C++17
cmake -DCMAKE_CXX_STANDARD=17 ..
```

### Image non trouvée

Vérifiez que le chemin est correct. Utilisez des chemins relatifs ou absolus :
```bash
# Chemin relatif depuis build/
./labellisation ../images/input/test.pgm ../images/output/result.pgm two_pass 4

# Chemin absolu
./labellisation /chemin/complet/vers/input.pgm /chemin/vers/output.pgm two_pass 4
```

### Erreur "Format non supporté"

Le projet ne supporte que PGM et PPM. Convertissez vos images :
```bash
convert input.jpg -colorspace Gray output.pgm
```

## Structure des fichiers

```
labellisation/
├── src/                    # Code source
│   ├── core/              # Classes de base (Image, LabelImage)
│   ├── io/                # Lecture/écriture PGM/PPM
│   ├── algorithms/        # Les 4 algorithmes
│   ├── utils/             # Fonctions utilitaires
│   └── main.cpp          # Programme principal
├── tests/                 # Tests unitaires
├── benchmarks/           # Benchmarks de performance
├── images/               # Images d'entrée/sortie
├── docs/                 # Documentation LaTeX
├── build/                # Fichiers de compilation (créé par CMake)
├── CMakeLists.txt        # Configuration CMake
└── README.md             # Documentation principale
```

## Aide

Pour plus d'informations :
- Voir [README.md](README.md) pour une vue d'ensemble
- Consulter le rapport LaTeX dans `docs/rapport/`
- Examiner le code source dans `src/`
