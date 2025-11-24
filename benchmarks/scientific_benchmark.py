#!/usr/bin/env python3
"""
Benchmark scientifique pour les algorithmes de labellisation

Ce script effectue des tests rigoureux sur les 4 algorithmes avec:
- Plusieurs images de test
- Deux types de connectivite (4 et 8)
- Plusieurs runs pour la fiabilite statistique
- Export des resultats en CSV

Usage:
    python scientific_benchmark.py [--runs N] [--output results.csv]

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os
import csv
import glob
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

# Ajouter le repertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from src.core.image import Image, LabelImage
from src.readers.image_io import ImageIO
from src.algorithms.two_pass import TwoPass
from src.algorithms.union_find import UnionFind
from src.algorithms.kruskal import Kruskal
from src.algorithms.prim import Prim
from src.utils.utils import Timer


# ============================================================================
# Fonctions statistiques manuelles (pas de numpy)
# ============================================================================

def manual_mean(values: List[float]) -> float:
    """Calcule la moyenne manuellement."""
    if not values:
        return 0.0
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


def manual_min(values: List[float]) -> float:
    """Trouve le minimum manuellement."""
    if not values:
        return 0.0
    result = values[0]
    for v in values[1:]:
        if v < result:
            result = v
    return result


def manual_max(values: List[float]) -> float:
    """Trouve le maximum manuellement."""
    if not values:
        return 0.0
    result = values[0]
    for v in values[1:]:
        if v > result:
            result = v
    return result


def manual_sqrt(x: float) -> float:
    """Calcule la racine carree manuellement (Newton-Raphson)."""
    if x < 0:
        raise ValueError("Racine carree d'un nombre negatif")
    if x == 0:
        return 0.0

    guess = x / 2.0
    for _ in range(50):  # 50 iterations suffisent
        new_guess = (guess + x / guess) / 2.0
        if abs(new_guess - guess) < 1e-10:
            break
        guess = new_guess
    return guess


def manual_std(values: List[float]) -> float:
    """Calcule l'ecart-type manuellement."""
    if len(values) < 2:
        return 0.0

    m = manual_mean(values)
    variance = 0.0
    for v in values:
        diff = v - m
        variance += diff * diff
    variance /= (len(values) - 1)  # Ecart-type echantillon
    return manual_sqrt(variance)


# ============================================================================
# Structure de donnees
# ============================================================================

@dataclass
class BenchmarkResult:
    """Resultat d'un benchmark pour une configuration."""
    image_name: str
    algorithm: str
    connectivity: int
    num_components: int
    runs: int
    times: List[float] = field(default_factory=list)

    @property
    def mean_time(self) -> float:
        return manual_mean(self.times)

    @property
    def std_time(self) -> float:
        return manual_std(self.times)

    @property
    def min_time(self) -> float:
        return manual_min(self.times)

    @property
    def max_time(self) -> float:
        return manual_max(self.times)


# ============================================================================
# Classe principale
# ============================================================================

class ScientificBenchmark:
    """Benchmark scientifique pour les algorithmes de labellisation."""

    ALGORITHMS = {
        'two_pass': TwoPass,
        'union_find': UnionFind,
        'kruskal': Kruskal,
        'prim': Prim
    }

    CONNECTIVITIES = [4, 8]

    def __init__(self, num_runs: int = 10):
        """
        Initialise le benchmark.

        Args:
            num_runs: Nombre de runs par configuration
        """
        self.num_runs = num_runs
        self.results: List[BenchmarkResult] = []

    def find_images(self, input_dir: str) -> List[str]:
        """
        Trouve toutes les images dans un repertoire.

        Args:
            input_dir: Repertoire contenant les images

        Returns:
            Liste des chemins d'images
        """
        extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.pgm', '*.ppm', '*.tiff']
        images = []

        for ext in extensions:
            pattern = os.path.join(input_dir, ext)
            images.extend(glob.glob(pattern))

        # Trier par nom
        images.sort()
        return images

    def run_single_test(self, image: Image, algorithm_name: str,
                        connectivity: int) -> Tuple[float, int]:
        """
        Execute un seul test.

        Args:
            image: Image a traiter
            algorithm_name: Nom de l'algorithme
            connectivity: Connectivite (4 ou 8)

        Returns:
            Tuple (temps en ms, nombre de composantes)
        """
        # Copier l'image pour ne pas la modifier
        test_image = image.copy()

        algorithm_class = self.ALGORITHMS[algorithm_name]

        timer = Timer()
        timer.start()
        labels = algorithm_class.label(test_image, connectivity)
        elapsed = timer.stop()

        num_components = labels.count_labels()

        return elapsed, num_components

    def benchmark_image(self, image_path: str) -> List[BenchmarkResult]:
        """
        Execute le benchmark sur une image.

        Args:
            image_path: Chemin de l'image

        Returns:
            Liste des resultats
        """
        image_name = os.path.basename(image_path)
        print(f"\n{'='*60}")
        print(f"Image: {image_name}")
        print(f"{'='*60}")

        # Charger l'image
        try:
            original_image = ImageIO.read_image(image_path)
            original_image.binarize(128)
            print(f"  Dimensions: {original_image.width} x {original_image.height}")
            print(f"  Pixels: {original_image.size}")
        except Exception as e:
            print(f"  ERREUR: {e}")
            return []

        results = []

        for connectivity in self.CONNECTIVITIES:
            print(f"\n  Connectivite: {connectivity}")
            print(f"  {'-'*50}")

            for algo_name in self.ALGORITHMS.keys():
                result = BenchmarkResult(
                    image_name=image_name,
                    algorithm=algo_name,
                    connectivity=connectivity,
                    num_components=0,
                    runs=self.num_runs
                )

                print(f"    {algo_name:12s}: ", end="", flush=True)

                for run in range(self.num_runs):
                    try:
                        elapsed, num_components = self.run_single_test(
                            original_image, algo_name, connectivity
                        )
                        result.times.append(elapsed)
                        result.num_components = num_components
                        print(".", end="", flush=True)
                    except Exception as e:
                        print(f" ERREUR ({e})")
                        break

                if result.times:
                    print(f" {result.mean_time:8.2f} ms (+/- {result.std_time:6.2f}) "
                          f"| {result.num_components} comp.")
                    results.append(result)

        return results

    def run(self, input_dir: str) -> List[BenchmarkResult]:
        """
        Execute le benchmark complet.

        Args:
            input_dir: Repertoire contenant les images

        Returns:
            Liste de tous les resultats
        """
        print("=" * 60)
        print("  BENCHMARK SCIENTIFIQUE - Labellisation")
        print("=" * 60)
        print(f"\nConfiguration:")
        print(f"  - Nombre de runs: {self.num_runs}")
        print(f"  - Algorithmes: {', '.join(self.ALGORITHMS.keys())}")
        print(f"  - Connectivites: {self.CONNECTIVITIES}")

        # Trouver les images
        images = self.find_images(input_dir)

        if not images:
            print(f"\nAucune image trouvee dans {input_dir}")
            return []

        print(f"\nImages trouvees: {len(images)}")
        for img in images:
            print(f"  - {os.path.basename(img)}")

        # Executer le benchmark
        all_results = []
        for image_path in images:
            results = self.benchmark_image(image_path)
            all_results.extend(results)

        self.results = all_results
        return all_results

    def export_csv(self, output_path: str):
        """
        Exporte les resultats en CSV.

        Args:
            output_path: Chemin du fichier CSV
        """
        if not self.results:
            print("Aucun resultat a exporter")
            return

        # Creer le repertoire si necessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # En-tete
            writer.writerow([
                'image', 'algorithm', 'connectivity', 'runs',
                'mean_time_ms', 'std_time_ms', 'min_time_ms', 'max_time_ms',
                'num_components'
            ])

            # Donnees
            for r in self.results:
                writer.writerow([
                    r.image_name, r.algorithm, r.connectivity, r.runs,
                    f"{r.mean_time:.4f}", f"{r.std_time:.4f}",
                    f"{r.min_time:.4f}", f"{r.max_time:.4f}",
                    r.num_components
                ])

        print(f"\nResultats exportes vers: {output_path}")

    def print_summary(self):
        """Affiche un resume des resultats."""
        if not self.results:
            print("Aucun resultat")
            return

        print("\n" + "=" * 60)
        print("  RESUME DES RESULTATS")
        print("=" * 60)

        # Grouper par algorithme
        algo_times: Dict[str, List[float]] = {}
        for r in self.results:
            if r.algorithm not in algo_times:
                algo_times[r.algorithm] = []
            algo_times[r.algorithm].append(r.mean_time)

        print("\nTemps moyen par algorithme (toutes images/connectivites):")
        print("-" * 40)

        # Trouver le plus rapide pour calculer le speedup
        reference_time = None
        sorted_algos = []

        for algo, times in algo_times.items():
            avg = manual_mean(times)
            sorted_algos.append((algo, avg))

        # Trier par temps
        sorted_algos.sort(key=lambda x: x[1])
        reference_time = sorted_algos[0][1]

        for algo, avg in sorted_algos:
            speedup = reference_time / avg if avg > 0 else 0
            print(f"  {algo:12s}: {avg:8.2f} ms (speedup: {speedup:.2f}x)")

        print("\n" + "=" * 60)


def main():
    """Point d'entree principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Benchmark scientifique des algorithmes de labellisation'
    )
    parser.add_argument('--runs', type=int, default=10,
                        help='Nombre de runs par configuration (defaut: 10)')
    parser.add_argument('--input', type=str, default='images/input',
                        help='Repertoire des images (defaut: images/input)')
    parser.add_argument('--output', type=str, default='benchmarks/results/benchmark_results.csv',
                        help='Fichier CSV de sortie')

    args = parser.parse_args()

    # Changer vers le repertoire du projet
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    # Executer le benchmark
    benchmark = ScientificBenchmark(num_runs=args.runs)
    benchmark.run(args.input)
    benchmark.export_csv(args.output)
    benchmark.print_summary()

    return 0


if __name__ == "__main__":
    sys.exit(main())
