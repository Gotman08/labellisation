#!/usr/bin/env python3
"""
Programme de benchmark pour comparer les algorithmes de labellisation

Ce programme compare les 4 algorithmes sur différentes images et
génère des statistiques de performance.

Métriques mesurées :
- Temps d'exécution (moyenne sur plusieurs runs)
- Écart-type du temps
- Nombre de composantes connexes trouvées
- Vérification de la cohérence des résultats

Usage :
  python benchmark.py <image1.pgm> [image2.pgm] [...]

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os
from dataclasses import dataclass
from typing import List

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from src.core.image import Image, LabelImage
from src.readers.image_io import ImageIO
from src.algorithms.two_pass import TwoPass
from src.algorithms.union_find import UnionFind
from src.algorithms.kruskal import Kruskal
from src.algorithms.prim import Prim
from src.utils.utils import Timer, mean, standard_deviation, min_array, max_array


@dataclass
class AlgorithmResult:
    """Structure pour les résultats d'un algorithme."""
    name: str
    mean_time: float      # Temps moyen (ms)
    std_dev: float        # Écart-type (ms)
    min_time: float       # Temps minimum (ms)
    max_time: float       # Temps maximum (ms)
    num_components: int   # Nombre de composantes trouvées


@dataclass
class BenchmarkConfig:
    """Configuration du benchmark."""
    num_runs: int = 10            # Nombre de runs pour moyenner
    connectivity: int = 4         # Connectivité à tester
    verify_results: bool = True   # Vérifier que tous les algos donnent le même résultat


def benchmark_algorithm(algo_name: str, input_image: Image,
                       connectivity: int, num_runs: int) -> AlgorithmResult:
    """
    Exécute le benchmark pour un algorithme donné.

    Args:
        algo_name: Nom de l'algorithme
        input_image: Image d'entrée
        connectivity: Connectivité (4 ou 8)
        num_runs: Nombre de runs

    Returns:
        Résultat du benchmark
    """
    times = []
    labels = None

    for _ in range(num_runs):
        timer = Timer()
        timer.start()

        # Exécuter l'algorithme
        if algo_name == "Two-Pass":
            labels = TwoPass.label(input_image, connectivity)
        elif algo_name == "Union-Find":
            labels = UnionFind.label(input_image, connectivity)
        elif algo_name == "Kruskal":
            labels = Kruskal.label(input_image, connectivity)
        elif algo_name == "Prim":
            labels = Prim.label(input_image, connectivity)

        elapsed = timer.stop()
        times.append(elapsed)

    # Calculer les statistiques
    return AlgorithmResult(
        name=algo_name,
        mean_time=mean(times),
        std_dev=standard_deviation(times),
        min_time=min_array(times),
        max_time=max_array(times),
        num_components=labels.count_labels() if labels else 0
    )


def print_results(results: List[AlgorithmResult], image_name: str,
                 image_size: int, connectivity: int) -> None:
    """
    Affiche les résultats du benchmark.

    Args:
        results: Liste des résultats
        image_name: Nom de l'image
        image_size: Taille de l'image (pixels)
        connectivity: Connectivité
    """
    print("\n========================================")
    print(f"Resultats pour: {image_name}")
    print(f"  Taille: {image_size} pixels")
    print(f"  Connectivite: {connectivity}")
    print("========================================\n")

    # Header du tableau
    print(f"{'Algorithme':>15} {'Moyenne':>12} {'Ecart-type':>12} {'Min':>12} {'Max':>12} {'Composantes':>15}")
    print("-" * 78)

    # Résultats pour chaque algorithme
    for result in results:
        print(f"{result.name:>15} {result.mean_time:>12.2f} {result.std_dev:>12.2f} "
              f"{result.min_time:>12.2f} {result.max_time:>12.2f} {result.num_components:>15}")

    print()

    # Trouver l'algorithme le plus rapide
    fastest_idx = 0
    for i in range(1, len(results)):
        if results[i].mean_time < results[fastest_idx].mean_time:
            fastest_idx = i

    print(f"Algorithme le plus rapide: {results[fastest_idx].name}")

    # Speedup relatif par rapport au plus rapide
    print(f"\nSpeedup relatif (par rapport a {results[fastest_idx].name}):")
    for result in results:
        speedup = result.mean_time / results[fastest_idx].mean_time
        print(f"  {result.name:>15}: {speedup:.2f}x")

    # Vérification de cohérence
    print("\nVerification de coherence:")
    reference_count = results[0].num_components
    all_match = True
    for result in results:
        if result.num_components != reference_count:
            all_match = False
            print(f"  ATTENTION: {result.name} a trouve {result.num_components} "
                  f"composantes (attendu: {reference_count})")
    if all_match:
        print("  OK - Tous les algorithmes trouvent le meme nombre de composantes")


def main():
    """Fonction principale."""
    print("========================================")
    print("  Benchmark - Labellisation")
    print("========================================\n")

    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <image1.pgm> [image2.pgm] [...]", file=sys.stderr)
        return 1

    config = BenchmarkConfig()

    print("Configuration:")
    print(f"  Nombre de runs par algorithme: {config.num_runs}")
    print(f"  Connectivite: {config.connectivity}\n")

    # Liste des algorithmes à tester
    algorithms = ["Two-Pass", "Union-Find", "Kruskal", "Prim"]

    # Pour chaque image fournie en argument
    for img_idx in range(1, len(sys.argv)):
        image_file = sys.argv[img_idx]

        print(f"Chargement de l'image: {image_file}")

        try:
            input_image = ImageIO.read_image(image_file)
        except Exception as e:
            print(f"Erreur: {e}", file=sys.stderr)
            continue

        # Binariser l'image
        input_image.binarize(128)

        # Benchmarker tous les algorithmes
        results = []

        for algo_name in algorithms:
            print(f"  Benchmark {algo_name}... ", end="", flush=True)

            result = benchmark_algorithm(
                algo_name, input_image, config.connectivity, config.num_runs)

            results.append(result)

            print(f"OK ({result.mean_time:.2f} ms)")

        # Afficher les résultats
        print_results(results, image_file, input_image.size, config.connectivity)

    print("\n========================================")
    print("  Benchmark termine")
    print("========================================")

    return 0


if __name__ == "__main__":
    sys.exit(main())
