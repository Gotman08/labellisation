#!/usr/bin/env python3
"""
Generation de graphiques pour les resultats de benchmark

Ce script lit les resultats CSV et genere des graphiques scientifiques:
- Comparaison des algorithmes (barres)
- Comparaison par image
- Impact de la connectivite
- Speedup relatif

Prerequis:
    pip install matplotlib

Usage:
    python generate_graphs.py [--input results.csv] [--output-dir graphs/]

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os
import csv
from dataclasses import dataclass
from typing import List, Dict

# Importer matplotlib
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("ERREUR: matplotlib n'est pas installe.")
    print("Installez-le avec: pip install matplotlib")


# ============================================================================
# Structure de donnees
# ============================================================================

@dataclass
class ResultEntry:
    """Une entree de resultat."""
    image: str
    algorithm: str
    connectivity: int
    runs: int
    mean_time: float
    std_time: float
    min_time: float
    max_time: float
    num_components: int


# ============================================================================
# Fonctions utilitaires
# ============================================================================

def manual_mean(values: List[float]) -> float:
    """Calcule la moyenne."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def load_csv(filepath: str) -> List[ResultEntry]:
    """
    Charge les resultats depuis un fichier CSV.

    Args:
        filepath: Chemin du fichier CSV

    Returns:
        Liste des entrees
    """
    results = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            entry = ResultEntry(
                image=row['image'],
                algorithm=row['algorithm'],
                connectivity=int(row['connectivity']),
                runs=int(row['runs']),
                mean_time=float(row['mean_time_ms']),
                std_time=float(row['std_time_ms']),
                min_time=float(row['min_time_ms']),
                max_time=float(row['max_time_ms']),
                num_components=int(row['num_components'])
            )
            results.append(entry)

    return results


# ============================================================================
# Generation des graphiques
# ============================================================================

# Couleurs pour les algorithmes
ALGO_COLORS = {
    'two_pass': '#3498db',      # Bleu
    'union_find': '#2ecc71',    # Vert
    'kruskal': '#e74c3c',       # Rouge
    'prim': '#9b59b6'           # Violet
}

ALGO_LABELS = {
    'two_pass': 'Two-Pass',
    'union_find': 'Union-Find',
    'kruskal': 'Kruskal',
    'prim': 'Prim'
}


def graph_algorithm_comparison(results: List[ResultEntry], output_dir: str):
    """
    Graphique 1: Comparaison globale des algorithmes.

    Args:
        results: Liste des resultats
        output_dir: Repertoire de sortie
    """
    if not MATPLOTLIB_AVAILABLE:
        return

    # Grouper par algorithme
    algo_times: Dict[str, List[float]] = {}
    algo_stds: Dict[str, List[float]] = {}

    for r in results:
        if r.algorithm not in algo_times:
            algo_times[r.algorithm] = []
            algo_stds[r.algorithm] = []
        algo_times[r.algorithm].append(r.mean_time)
        algo_stds[r.algorithm].append(r.std_time)

    # Calculer les moyennes
    algorithms = list(algo_times.keys())
    means = [manual_mean(algo_times[a]) for a in algorithms]
    stds = [manual_mean(algo_stds[a]) for a in algorithms]
    colors = [ALGO_COLORS.get(a, '#95a5a6') for a in algorithms]
    labels = [ALGO_LABELS.get(a, a) for a in algorithms]

    # Creer le graphique
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(labels, means, yerr=stds, capsize=5, color=colors, edgecolor='black')

    ax.set_xlabel('Algorithme', fontsize=12)
    ax.set_ylabel('Temps moyen (ms)', fontsize=12)
    ax.set_title('Comparaison des algorithmes de labellisation\n(Moyenne sur toutes les images et connectivites)', fontsize=14)

    # Ajouter les valeurs sur les barres
    for bar, mean, std in zip(bars, means, stds):
        height = bar.get_height()
        ax.annotate(f'{mean:.1f}ms',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'comparison_algorithms.png')
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"  Graphique cree: {output_path}")


def graph_image_comparison(results: List[ResultEntry], output_dir: str):
    """
    Graphique 2: Comparaison par image (grouped bars).

    Args:
        results: Liste des resultats
        output_dir: Repertoire de sortie
    """
    if not MATPLOTLIB_AVAILABLE:
        return

    # Grouper par image et algorithme (connectivite 4 seulement pour simplifier)
    images = sorted(set(r.image for r in results))
    algorithms = sorted(set(r.algorithm for r in results))

    # Filtrer pour connectivite 4
    data: Dict[str, Dict[str, float]] = {img: {} for img in images}

    for r in results:
        if r.connectivity == 4:
            data[r.image][r.algorithm] = r.mean_time

    # Creer le graphique
    fig, ax = plt.subplots(figsize=(12, 6))

    x = range(len(images))
    width = 0.2
    offsets = [-1.5, -0.5, 0.5, 1.5]

    for i, algo in enumerate(algorithms):
        values = [data[img].get(algo, 0) for img in images]
        color = ALGO_COLORS.get(algo, '#95a5a6')
        label = ALGO_LABELS.get(algo, algo)
        ax.bar([xi + offsets[i] * width for xi in x], values, width,
               label=label, color=color, edgecolor='black')

    ax.set_xlabel('Image', fontsize=12)
    ax.set_ylabel('Temps (ms)', fontsize=12)
    ax.set_title('Temps d\'execution par image et algorithme\n(Connectivite 4)', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([img[:15] + '...' if len(img) > 15 else img for img in images], rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'comparison_images.png')
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"  Graphique cree: {output_path}")


def graph_connectivity_comparison(results: List[ResultEntry], output_dir: str):
    """
    Graphique 3: Impact de la connectivite (4 vs 8).

    Args:
        results: Liste des resultats
        output_dir: Repertoire de sortie
    """
    if not MATPLOTLIB_AVAILABLE:
        return

    # Grouper par algorithme et connectivite
    data: Dict[str, Dict[int, List[float]]] = {}

    for r in results:
        if r.algorithm not in data:
            data[r.algorithm] = {4: [], 8: []}
        data[r.algorithm][r.connectivity].append(r.mean_time)

    # Calculer les moyennes
    algorithms = list(data.keys())
    times_4 = [manual_mean(data[a][4]) for a in algorithms]
    times_8 = [manual_mean(data[a][8]) for a in algorithms]
    labels = [ALGO_LABELS.get(a, a) for a in algorithms]

    # Creer le graphique
    fig, ax = plt.subplots(figsize=(10, 6))

    x = range(len(algorithms))
    width = 0.35

    bars1 = ax.bar([xi - width/2 for xi in x], times_4, width, label='Connectivite 4',
                   color='#3498db', edgecolor='black')
    bars2 = ax.bar([xi + width/2 for xi in x], times_8, width, label='Connectivite 8',
                   color='#e74c3c', edgecolor='black')

    ax.set_xlabel('Algorithme', fontsize=12)
    ax.set_ylabel('Temps moyen (ms)', fontsize=12)
    ax.set_title('Impact de la connectivite sur les performances', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'connectivity_comparison.png')
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"  Graphique cree: {output_path}")


def graph_speedup(results: List[ResultEntry], output_dir: str):
    """
    Graphique 4: Speedup relatif (reference = two_pass).

    Args:
        results: Liste des resultats
        output_dir: Repertoire de sortie
    """
    if not MATPLOTLIB_AVAILABLE:
        return

    # Calculer le temps moyen par algorithme
    algo_times: Dict[str, List[float]] = {}

    for r in results:
        if r.algorithm not in algo_times:
            algo_times[r.algorithm] = []
        algo_times[r.algorithm].append(r.mean_time)

    algorithms = list(algo_times.keys())
    means = {a: manual_mean(algo_times[a]) for a in algorithms}

    # Utiliser two_pass comme reference
    reference = means.get('two_pass', 1.0)
    if reference == 0:
        reference = 1.0

    speedups = [reference / means[a] if means[a] > 0 else 0 for a in algorithms]
    colors = [ALGO_COLORS.get(a, '#95a5a6') for a in algorithms]
    labels = [ALGO_LABELS.get(a, a) for a in algorithms]

    # Creer le graphique
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(labels, speedups, color=colors, edgecolor='black')

    # Ligne de reference a 1.0
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Reference (Two-Pass)')

    ax.set_xlabel('Algorithme', fontsize=12)
    ax.set_ylabel('Speedup (x)', fontsize=12)
    ax.set_title('Speedup relatif par rapport a Two-Pass\n(>1 = plus rapide)', fontsize=14)

    # Ajouter les valeurs sur les barres
    for bar, speedup in zip(bars, speedups):
        height = bar.get_height()
        ax.annotate(f'{speedup:.2f}x',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'speedup.png')
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"  Graphique cree: {output_path}")


def graph_components_comparison(results: List[ResultEntry], output_dir: str):
    """
    Graphique 5: Verification de la coherence (nombre de composantes).

    Args:
        results: Liste des resultats
        output_dir: Repertoire de sortie
    """
    if not MATPLOTLIB_AVAILABLE:
        return

    # Grouper par image
    images = sorted(set(r.image for r in results))

    fig, ax = plt.subplots(figsize=(12, 6))

    # Pour chaque image, verifier que tous les algorithmes trouvent le meme nombre
    x = range(len(images))
    width = 0.15
    algorithms = ['two_pass', 'union_find', 'kruskal', 'prim']
    offsets = [-1.5, -0.5, 0.5, 1.5]

    for i, algo in enumerate(algorithms):
        values = []
        for img in images:
            # Prendre connectivite 4
            for r in results:
                if r.image == img and r.algorithm == algo and r.connectivity == 4:
                    values.append(r.num_components)
                    break
            else:
                values.append(0)

        color = ALGO_COLORS.get(algo, '#95a5a6')
        label = ALGO_LABELS.get(algo, algo)
        ax.bar([xi + offsets[i] * width for xi in x], values, width,
               label=label, color=color, edgecolor='black')

    ax.set_xlabel('Image', fontsize=12)
    ax.set_ylabel('Nombre de composantes', fontsize=12)
    ax.set_title('Verification de coherence: nombre de composantes connexes\n(Tous les algorithmes doivent trouver le meme nombre)', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([img[:15] + '...' if len(img) > 15 else img for img in images], rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'components_verification.png')
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"  Graphique cree: {output_path}")


def generate_all_graphs(csv_path: str, output_dir: str):
    """
    Genere tous les graphiques.

    Args:
        csv_path: Chemin du fichier CSV
        output_dir: Repertoire de sortie
    """
    if not MATPLOTLIB_AVAILABLE:
        print("ERREUR: matplotlib n'est pas disponible")
        return

    print("=" * 60)
    print("  GENERATION DES GRAPHIQUES")
    print("=" * 60)

    # Charger les donnees
    print(f"\nChargement des donnees: {csv_path}")

    if not os.path.exists(csv_path):
        print(f"ERREUR: Fichier non trouve: {csv_path}")
        return

    results = load_csv(csv_path)
    print(f"  {len(results)} entrees chargees")

    # Creer le repertoire de sortie
    os.makedirs(output_dir, exist_ok=True)

    # Generer les graphiques
    print(f"\nGeneration des graphiques dans: {output_dir}")

    graph_algorithm_comparison(results, output_dir)
    graph_image_comparison(results, output_dir)
    graph_connectivity_comparison(results, output_dir)
    graph_speedup(results, output_dir)
    graph_components_comparison(results, output_dir)

    print("\n" + "=" * 60)
    print("  Tous les graphiques ont ete generes!")
    print("=" * 60)


def main():
    """Point d'entree principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generation de graphiques pour les resultats de benchmark'
    )
    parser.add_argument('--input', type=str, default='benchmarks/results/benchmark_results.csv',
                        help='Fichier CSV des resultats')
    parser.add_argument('--output-dir', type=str, default='benchmarks/results/graphs',
                        help='Repertoire de sortie pour les graphiques')

    args = parser.parse_args()

    # Changer vers le repertoire du projet
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    generate_all_graphs(args.input, args.output_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
