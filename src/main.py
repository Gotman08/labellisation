#!/usr/bin/env python3
"""
Programme principal de labellisation des composantes connexes

Ce programme implémente 4 algorithmes différents :
1. Two-Pass : Algorithme classique en deux passes
2. Union-Find : Approche par structure de données Disjoint-Set
3. Kruskal : Approche par graphe (Minimum Spanning Tree)
4. Prim : Approche par graphe (exploration BFS)

Usage :
  python main.py <input> <output> <algorithm> <connectivity>

Arguments :
  input        : Chemin de l'image d'entree (JPEG, PNG, BMP, PGM, PPM, etc.)
  output       : Chemin de l'image de sortie (PGM, PNG, JPEG, etc.)
  algorithm    : two_pass | union_find | kruskal | prim
  connectivity : 4 | 8

Exemple :
  python main.py input.jpg output.png two_pass 4

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os

# Ajouter le répertoire courant au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.image import Image, LabelImage
from readers.image_io import ImageIO
from algorithms.two_pass import TwoPass
from algorithms.union_find import UnionFind
from algorithms.kruskal import Kruskal
from algorithms.prim import Prim
from utils.utils import Timer


def print_usage(program_name: str) -> None:
    """Affiche l'aide d'utilisation."""
    print(f"\nUsage: python {program_name} <input> <output> <algorithm> <connectivity>\n")
    print("Arguments:")
    print("  input        : Chemin de l'image d'entree (JPEG, PNG, BMP, PGM, PPM, etc.)")
    print("  output       : Chemin de l'image de sortie (PGM, PNG, JPEG, etc.)")
    print("  algorithm    : two_pass | union_find | kruskal | prim")
    print("  connectivity : 4 | 8\n")
    print("Formats supportes: JPEG, PNG, BMP, TIFF, GIF, WEBP, PGM, PPM\n")
    print("Exemples:")
    print(f"  python {program_name} input.jpg output.png two_pass 4")
    print(f"  python {program_name} input.png output.pgm union_find 8")
    print(f"  python {program_name} image.bmp result.png kruskal 4")
    print(f"  python {program_name} photo.jpeg output.pgm prim 8\n")


def main():
    """Fonction principale."""
    print("========================================")
    print("  Labellisation des Composantes Connexes")
    print("========================================\n")

    # Vérifier les arguments
    if len(sys.argv) != 5:
        print("Erreur: nombre d'arguments incorrect", file=sys.stderr)
        print_usage(sys.argv[0])
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    algorithm = sys.argv[3]
    try:
        connectivity = int(sys.argv[4])
    except ValueError:
        print("Erreur: la connectivite doit etre un entier (4 ou 8)", file=sys.stderr)
        return 1

    # Validation des paramètres
    if connectivity not in (4, 8):
        print("Erreur: la connectivite doit etre 4 ou 8", file=sys.stderr)
        return 1

    valid_algorithms = ("two_pass", "union_find", "kruskal", "prim")
    if algorithm not in valid_algorithms:
        print("Erreur: algorithme invalide", file=sys.stderr)
        print_usage(sys.argv[0])
        return 1

    # ========================================================================
    # Étape 1 : Chargement de l'image
    # ========================================================================

    print(f"Chargement de l'image: {input_file}")

    try:
        # Lecture automatique du format (JPEG, PNG, BMP, PGM, PPM, etc.)
        input_image = ImageIO.read_image(input_file)
        print("  -> Image chargee et convertie en niveaux de gris")
    except Exception as e:
        print(f"Erreur lors du chargement: {e}", file=sys.stderr)
        return 1

    print(f"  Dimensions: {input_image.width} x {input_image.height}")
    print(f"  Pixels: {input_image.size}\n")

    # Binariser l'image (seuil à 128)
    input_image.binarize(128)
    print("Image binarisee (seuil = 128)\n")

    # ========================================================================
    # Étape 2 : Labellisation
    # ========================================================================

    print(f"Algorithme: {algorithm}")
    print(f"Connectivite: {connectivity}")
    print("Labellisation en cours...")

    timer = Timer()
    timer.start()

    try:
        if algorithm == "two_pass":
            labels = TwoPass.label(input_image, connectivity)
        elif algorithm == "union_find":
            labels = UnionFind.label(input_image, connectivity)
        elif algorithm == "kruskal":
            labels = Kruskal.label(input_image, connectivity)
        elif algorithm == "prim":
            labels = Prim.label(input_image, connectivity)
    except Exception as e:
        print(f"Erreur lors de la labellisation: {e}", file=sys.stderr)
        return 1

    elapsed = timer.stop()

    # Compter le nombre de composantes
    num_components = labels.count_labels()

    print("\nLabellisation terminee!")
    print(f"  Temps d'execution: {elapsed:.2f} ms")
    print(f"  Composantes connexes trouvees: {num_components}\n")

    # ========================================================================
    # Étape 3 : Sauvegarde de l'image labellisée
    # ========================================================================

    print(f"Sauvegarde de l'image labellisee: {output_file}")

    try:
        # Convertir en image visualisable (normalisation sur [0, 255])
        output_image = labels.to_visualization()

        # Sauvegarder (format detecte automatiquement selon l'extension)
        ImageIO.write_image(output_file, output_image)

        print("Image sauvegardee avec succes!")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}", file=sys.stderr)
        return 1

    print("\n========================================")
    print("  Traitement termine avec succes")
    print("========================================")

    return 0


if __name__ == "__main__":
    sys.exit(main())
