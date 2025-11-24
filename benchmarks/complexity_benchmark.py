#!/usr/bin/env python3
"""
Benchmark de complexité - Temps = f(Nombre de pixels)

Ce script mesure le temps d'exécution des algorithmes en fonction
de la taille de l'image (128x128, 256x256, 512x512, 1024x1024).

Il génère une courbe Temps = f(N) pour analyser la complexité empirique.

Usage:
    python complexity_benchmark.py [--runs N]

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os
import csv
from typing import List, Dict, Tuple

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.image import Image, LabelImage
from src.algorithms.two_pass import TwoPass
from src.algorithms.union_find import UnionFind
from src.algorithms.kruskal import Kruskal
from src.algorithms.prim import Prim
from src.utils.utils import Timer

# Essayer d'importer matplotlib pour les graphiques
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# ============================================================================
# Fonctions statistiques manuelles
# ============================================================================

def manual_mean(values: List[float]) -> float:
    """Calcule la moyenne manuellement."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def manual_std(values: List[float]) -> float:
    """Calcule l'ecart-type manuellement."""
    if len(values) < 2:
        return 0.0
    m = manual_mean(values)
    variance = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return variance ** 0.5


# ============================================================================
# Génération d'images de test
# ============================================================================

def create_test_image(size: int, density: float = 0.3) -> Image:
    """
    Crée une image de test avec des objets pseudo-aléatoires.

    Args:
        size: Dimension de l'image (size x size)
        density: Densité d'objets (proportion de pixels blancs)

    Returns:
        Image binaire
    """
    image = Image(size, size)

    # Génération pseudo-aléatoire déterministe basée sur la position
    for x in range(size):
        for y in range(size):
            # Utilise une formule pseudo-aléatoire simple
            val = ((x * 7 + y * 13) * 31) % 100
            if val < density * 100:
                image.set_at(x, y, 255)
            else:
                image.set_at(x, y, 0)

    return image


# ============================================================================
# Benchmark de complexité
# ============================================================================

ALGORITHMS = {
    'two_pass': TwoPass,
    'union_find': UnionFind,
    'kruskal': Kruskal,
    'prim': Prim
}

ALGO_COLORS = {
    'two_pass': '#3498db',
    'union_find': '#2ecc71',
    'kruskal': '#e74c3c',
    'prim': '#9b59b6'
}

ALGO_LABELS = {
    'two_pass': 'Two-Pass',
    'union_find': 'Union-Find',
    'kruskal': 'Kruskal',
    'prim': 'Prim'
}


def benchmark_single(image: Image, algorithm_name: str, connectivity: int) -> float:
    """
    Execute un seul test.

    Returns:
        Temps en millisecondes
    """
    test_image = image.copy()
    algorithm_class = ALGORITHMS[algorithm_name]

    timer = Timer()
    timer.start()
    algorithm_class.label(test_image, connectivity)
    elapsed = timer.stop()

    return elapsed


def run_complexity_benchmark(sizes: List[int], num_runs: int = 5) -> Dict:
    """
    Execute le benchmark de complexité.

    Args:
        sizes: Liste des tailles d'images à tester
        num_runs: Nombre de runs par configuration

    Returns:
        Dictionnaire des résultats
    """
    results = {algo: [] for algo in ALGORITHMS}

    print("=" * 60)
    print("  BENCHMARK DE COMPLEXITE")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  - Tailles: {sizes}")
    print(f"  - Runs par config: {num_runs}")
    print(f"  - Connectivite: 4")
    print()

    for size in sizes:
        print(f"\n{'='*50}")
        print(f"  Taille: {size}x{size} ({size*size} pixels)")
        print(f"{'='*50}")

        # Créer l'image de test
        image = create_test_image(size)

        for algo_name in ALGORITHMS:
            times = []

            print(f"    {algo_name:12s}: ", end="", flush=True)

            for _ in range(num_runs):
                elapsed = benchmark_single(image, algo_name, 4)
                times.append(elapsed)
                print(".", end="", flush=True)

            mean_time = manual_mean(times)
            std_time = manual_std(times)

            results[algo_name].append({
                'size': size,
                'pixels': size * size,
                'mean_time': mean_time,
                'std_time': std_time
            })

            print(f" {mean_time:8.2f} ms (+/- {std_time:5.2f})")

    return results


def export_csv(results: Dict, output_path: str):
    """Exporte les résultats en CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['algorithm', 'size', 'pixels', 'mean_time_ms', 'std_time_ms'])

        for algo, data in results.items():
            for entry in data:
                writer.writerow([
                    algo,
                    entry['size'],
                    entry['pixels'],
                    f"{entry['mean_time']:.4f}",
                    f"{entry['std_time']:.4f}"
                ])

    print(f"\nResultats exportes: {output_path}")


def generate_complexity_graph(results: Dict, output_dir: str):
    """Génère le graphique de complexité."""
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib non disponible - graphique non genere")
        return

    os.makedirs(output_dir, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Graphique 1: Temps vs Nombre de pixels
    for algo, data in results.items():
        pixels = [d['pixels'] for d in data]
        times = [d['mean_time'] for d in data]
        stds = [d['std_time'] for d in data]
        color = ALGO_COLORS.get(algo, '#95a5a6')
        label = ALGO_LABELS.get(algo, algo)

        ax1.errorbar(pixels, times, yerr=stds, label=label,
                     color=color, marker='o', capsize=3, linewidth=2)

    ax1.set_xlabel('Nombre de pixels (N)', fontsize=12)
    ax1.set_ylabel('Temps (ms)', fontsize=12)
    ax1.set_title('Complexite empirique: Temps = f(N)', fontsize=14)
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # Graphique 2: Temps normalisé (ms/pixel)
    for algo, data in results.items():
        pixels = [d['pixels'] for d in data]
        times_per_pixel = [d['mean_time'] / d['pixels'] * 1000 for d in data]  # µs/pixel
        color = ALGO_COLORS.get(algo, '#95a5a6')
        label = ALGO_LABELS.get(algo, algo)

        ax2.plot(pixels, times_per_pixel, label=label,
                 color=color, marker='s', linewidth=2)

    ax2.set_xlabel('Nombre de pixels (N)', fontsize=12)
    ax2.set_ylabel('Temps par pixel (µs/pixel)', fontsize=12)
    ax2.set_title('Temps normalise par pixel', fontsize=14)
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_xscale('log')

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'complexity_analysis.png')
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Graphique genere: {output_path}")

    # Graphique additionnel: comparaison par taille
    fig, ax = plt.subplots(figsize=(10, 6))

    sizes = [d['size'] for d in list(results.values())[0]]
    x = range(len(sizes))
    width = 0.2
    offsets = [-1.5, -0.5, 0.5, 1.5]

    for i, (algo, data) in enumerate(results.items()):
        times = [d['mean_time'] for d in data]
        color = ALGO_COLORS.get(algo, '#95a5a6')
        label = ALGO_LABELS.get(algo, algo)
        ax.bar([xi + offsets[i] * width for xi in x], times, width,
               label=label, color=color, edgecolor='black')

    ax.set_xlabel('Taille de l\'image', fontsize=12)
    ax.set_ylabel('Temps (ms)', fontsize=12)
    ax.set_title('Temps d\'execution par taille d\'image', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([f'{s}x{s}' for s in sizes])
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'complexity_by_size.png')
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Graphique genere: {output_path}")


def main():
    """Point d'entree principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Benchmark de complexite des algorithmes de labellisation'
    )
    parser.add_argument('--runs', type=int, default=5,
                        help='Nombre de runs par configuration (defaut: 5)')
    parser.add_argument('--sizes', type=str, default='64,128,256,512',
                        help='Tailles a tester, separees par des virgules')

    args = parser.parse_args()

    # Parser les tailles
    sizes = [int(s.strip()) for s in args.sizes.split(',')]

    # Changer vers le repertoire du projet
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    # Executer le benchmark
    results = run_complexity_benchmark(sizes, args.runs)

    # Exporter les resultats
    csv_path = 'benchmarks/results/complexity_results.csv'
    export_csv(results, csv_path)

    # Generer les graphiques
    generate_complexity_graph(results, 'benchmarks/results/graphs')

    print("\n" + "=" * 60)
    print("  BENCHMARK TERMINE")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
