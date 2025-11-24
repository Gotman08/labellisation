# Guide d'utilisation - Labellisation

## Installation

### Prerequis
- Python 3.7 ou superieur
- NumPy
- OpenCV (pour les formats JPEG, PNG, BMP, etc.)

### Installation des dependances

```bash
pip install numpy opencv-python
```

## Utilisation

### Programme principal

```bash
python src/main.py <input> <output> <algorithm> <connectivity>
```

**Arguments :**
- `input` : Chemin de l'image d'entree (JPEG, PNG, BMP, TIFF, GIF, WEBP, PGM, PPM)
- `output` : Chemin de l'image de sortie (PNG, JPEG, BMP, PGM, etc.)
- `algorithm` : `two_pass` | `union_find` | `kruskal` | `prim`
- `connectivity` : `4` | `8`

**Formats supportes :** JPEG, PNG, BMP, TIFF, GIF, WEBP, PGM, PPM

**Exemples :**

```bash
# Labellisation d'une image JPEG avec Two-Pass
python src/main.py photo.jpg result.png two_pass 4

# Labellisation d'une image PNG avec Union-Find
python src/main.py image.png output.pgm union_find 8

# Labellisation d'une image BMP avec Kruskal
python src/main.py picture.bmp result.png kruskal 4

# Labellisation avec Prim
python src/main.py input.tiff output.png prim 8
```

### Benchmark

```bash
# Comparer les performances sur une ou plusieurs images
python benchmarks/benchmark.py images/input/image1.pgm images/input/image2.pgm

# Le benchmark affiche :
# - Temps moyen d'execution (sur 10 runs)
# - Ecart-type
# - Speedup relatif
# - Nombre de composantes trouvees
```

## Formats d'images supportes

Le projet supporte de nombreux formats d'images grace a OpenCV :

| Format | Extension | Lecture | Ecriture |
|--------|-----------|---------|----------|
| JPEG   | .jpg, .jpeg | Oui | Oui |
| PNG    | .png | Oui | Oui |
| BMP    | .bmp | Oui | Oui |
| TIFF   | .tiff, .tif | Oui | Oui |
| GIF    | .gif | Oui | Non |
| WEBP   | .webp | Oui | Non |
| PGM    | .pgm | Oui | Oui |
| PPM    | .ppm | Oui | Oui |

**Note :** Les images couleur sont automatiquement converties en niveaux de gris.

## Visualiser les resultats

Les images labellisees peuvent etre sauvegardees dans differents formats (PNG, JPEG, PGM, etc.).
Chaque composante connexe est representee par un niveau de gris different.

Vous pouvez visualiser les resultats avec :
- N'importe quel visualiseur d'images (si format PNG/JPEG)
- **GIMP** : Ouvrir directement le fichier
- **VSCode** : Extensions d'affichage d'images

## Compilation du rapport LaTeX

```bash
cd docs/rapport
pdflatex rapport.tex
pdflatex rapport.tex  # Deux fois pour les references

cd ../presentation
pdflatex presentation.tex
pdflatex presentation.tex
```

## Problemes courants

### Module non trouve (ModuleNotFoundError)

Si vous obtenez une erreur "No module named...":
```bash
# Verifier que vous etes dans le bon repertoire
cd labellisation

# Executer depuis la racine du projet
python src/main.py ...
```

### Image non trouvee

Verifiez que le chemin est correct. Utilisez des chemins relatifs ou absolus :
```bash
# Chemin relatif depuis la racine du projet
python src/main.py images/input/test.pgm images/output/result.pgm two_pass 4

# Chemin absolu
python src/main.py /chemin/complet/vers/input.pgm /chemin/vers/output.pgm two_pass 4
```

### Erreur "Format non supporte"

Verifiez que OpenCV est installe :
```bash
pip install opencv-python
```

Si le probleme persiste, essayez de convertir l'image en PNG ou JPEG.

## Structure des fichiers

```
labellisation/
├── src/                    # Code source Python
│   ├── __init__.py        # Package principal
│   ├── core/              # Classes de base (Image, LabelImage)
│   │   ├── __init__.py
│   │   └── image.py
│   ├── io/                # Lecture/ecriture PGM/PPM
│   │   ├── __init__.py
│   │   └── image_io.py
│   ├── algorithms/        # Les 4 algorithmes
│   │   ├── __init__.py
│   │   ├── two_pass.py
│   │   ├── union_find.py
│   │   ├── kruskal.py
│   │   └── prim.py
│   ├── utils/             # Fonctions utilitaires
│   │   ├── __init__.py
│   │   └── utils.py
│   └── main.py            # Programme principal
├── benchmarks/            # Benchmarks de performance
│   └── benchmark.py
├── images/                # Images d'entree/sortie
├── docs/                  # Documentation LaTeX
└── README.md              # Documentation principale
```

## API Python

### Utilisation en tant que module

Vous pouvez aussi utiliser le code comme une bibliotheque Python :

```python
from src.core.image import Image, LabelImage
from src.io.image_io import ImageIO
from src.algorithms.two_pass import TwoPass
from src.algorithms.union_find import UnionFind
from src.algorithms.kruskal import Kruskal
from src.algorithms.prim import Prim

# Charger une image (JPEG, PNG, BMP, PGM, etc.)
image = ImageIO.read_image("photo.jpg")

# Binariser
image.binarize(128)

# Labelliser avec l'algorithme de votre choix
labels = TwoPass.label(image, connectivity=4)
# ou
labels = UnionFind.label(image, connectivity=8)
# ou
labels = Kruskal.label(image, connectivity=4)
# ou
labels = Prim.label(image, connectivity=8)

# Obtenir le nombre de composantes
num_components = labels.count_labels()
print(f"Composantes trouvees: {num_components}")

# Sauvegarder le resultat (PNG, JPEG, PGM, etc.)
output_image = labels.to_visualization()
ImageIO.write_image("output.png", output_image)
```

## Aide

Pour plus d'informations :
- Voir [README.md](README.md) pour une vue d'ensemble
- Consulter le rapport LaTeX dans `docs/rapport/`
- Examiner le code source dans `src/`
