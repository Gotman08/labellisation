#!/usr/bin/env python3
"""
Script principal pour executer le benchmark complet

Ce script:
1. Execute le benchmark scientifique sur toutes les images
2. Genere les graphiques automatiquement
3. Cree un rapport texte recapitulatif

Usage:
    python run_all.py [--runs N]

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os
import subprocess
from datetime import datetime


def print_header(text: str):
    """Affiche un en-tete formate."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def check_dependencies():
    """Verifie que les dependances sont installees."""
    print_header("VERIFICATION DES DEPENDANCES")

    dependencies = {
        'numpy': False,
        'cv2': False,
        'matplotlib': False
    }

    try:
        import numpy
        dependencies['numpy'] = True
        print("  [OK] numpy")
    except ImportError:
        print("  [MANQUANT] numpy - pip install numpy")

    try:
        import cv2
        dependencies['cv2'] = True
        print("  [OK] opencv (cv2)")
    except ImportError:
        print("  [MANQUANT] opencv - pip install opencv-python")

    try:
        import matplotlib
        dependencies['matplotlib'] = True
        print("  [OK] matplotlib")
    except ImportError:
        print("  [MANQUANT] matplotlib - pip install matplotlib")

    # numpy et cv2 sont obligatoires, matplotlib est optionnel
    if not dependencies['numpy'] or not dependencies['cv2']:
        print("\n  ERREUR: Dependances obligatoires manquantes!")
        print("  Installez-les avec: pip install numpy opencv-python matplotlib")
        return False

    if not dependencies['matplotlib']:
        print("\n  ATTENTION: matplotlib manquant - les graphiques ne seront pas generes")
        print("  Installez-le avec: pip install matplotlib")

    return True


def run_benchmark(num_runs: int, input_dir: str, output_csv: str):
    """
    Execute le benchmark scientifique.

    Args:
        num_runs: Nombre de runs
        input_dir: Repertoire des images
        output_csv: Fichier CSV de sortie
    """
    print_header("EXECUTION DU BENCHMARK")

    # Importer et executer le benchmark
    from scientific_benchmark import ScientificBenchmark

    benchmark = ScientificBenchmark(num_runs=num_runs)
    benchmark.run(input_dir)
    benchmark.export_csv(output_csv)
    benchmark.print_summary()

    return benchmark.results


def generate_graphs(csv_path: str, output_dir: str):
    """
    Genere les graphiques.

    Args:
        csv_path: Chemin du fichier CSV
        output_dir: Repertoire de sortie
    """
    try:
        import matplotlib
        print_header("GENERATION DES GRAPHIQUES")

        from generate_graphs import generate_all_graphs
        generate_all_graphs(csv_path, output_dir)

    except ImportError:
        print("\n  ATTENTION: matplotlib non disponible - graphiques ignores")


def generate_report(results, output_path: str, num_runs: int):
    """
    Genere un rapport texte recapitulatif.

    Args:
        results: Resultats du benchmark
        output_path: Chemin du fichier de sortie
        num_runs: Nombre de runs effectues
    """
    print_header("GENERATION DU RAPPORT")

    # Fonctions utilitaires
    def manual_mean(values):
        if not values:
            return 0.0
        return sum(values) / len(values)

    # Creer le repertoire si necessaire
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("  RAPPORT DE BENCHMARK - LABELLISATION DES COMPOSANTES CONNEXES\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Nombre de runs: {num_runs}\n\n")

        # Resume par algorithme
        f.write("-" * 70 + "\n")
        f.write("  RESUME PAR ALGORITHME\n")
        f.write("-" * 70 + "\n\n")

        algo_times = {}
        for r in results:
            if r.algorithm not in algo_times:
                algo_times[r.algorithm] = []
            algo_times[r.algorithm].append(r.mean_time)

        # Trier par temps moyen
        sorted_algos = [(a, manual_mean(times)) for a, times in algo_times.items()]
        sorted_algos.sort(key=lambda x: x[1])

        reference = sorted_algos[0][1] if sorted_algos else 1.0

        f.write(f"{'Algorithme':<15} {'Temps moyen':>12} {'Speedup':>10}\n")
        f.write("-" * 40 + "\n")

        for algo, avg in sorted_algos:
            speedup = reference / avg if avg > 0 else 0
            f.write(f"{algo:<15} {avg:>10.2f} ms {speedup:>9.2f}x\n")

        # Details par image
        f.write("\n" + "-" * 70 + "\n")
        f.write("  DETAILS PAR IMAGE\n")
        f.write("-" * 70 + "\n\n")

        images = sorted(set(r.image_name for r in results))

        for image in images:
            f.write(f"\n  Image: {image}\n")
            f.write("  " + "-" * 50 + "\n")

            image_results = [r for r in results if r.image_name == image]

            for connectivity in [4, 8]:
                f.write(f"\n    Connectivite {connectivity}:\n")
                conn_results = [r for r in image_results if r.connectivity == connectivity]

                for r in sorted(conn_results, key=lambda x: x.mean_time):
                    f.write(f"      {r.algorithm:<12}: {r.mean_time:8.2f} ms "
                            f"(+/- {r.std_time:6.2f}) | {r.num_components} composantes\n")

        # Verification de coherence
        f.write("\n" + "-" * 70 + "\n")
        f.write("  VERIFICATION DE COHERENCE\n")
        f.write("-" * 70 + "\n\n")

        all_consistent = True
        for image in images:
            image_results = [r for r in results if r.image_name == image and r.connectivity == 4]
            components = set(r.num_components for r in image_results)

            if len(components) == 1:
                f.write(f"  [OK] {image}: {components.pop()} composantes\n")
            else:
                f.write(f"  [ERREUR] {image}: valeurs differentes! {components}\n")
                all_consistent = False

        if all_consistent:
            f.write("\n  Tous les algorithmes trouvent le meme nombre de composantes.\n")
        else:
            f.write("\n  ATTENTION: Incoherence detectee!\n")

        f.write("\n" + "=" * 70 + "\n")
        f.write("  FIN DU RAPPORT\n")
        f.write("=" * 70 + "\n")

    print(f"  Rapport genere: {output_path}")


def main():
    """Point d'entree principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Execute le benchmark complet avec graphiques et rapport'
    )
    parser.add_argument('--runs', type=int, default=10,
                        help='Nombre de runs par configuration (defaut: 10)')
    parser.add_argument('--input', type=str, default='images/input',
                        help='Repertoire des images (defaut: images/input)')

    args = parser.parse_args()

    # Changer vers le repertoire du projet
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    # Ajouter le repertoire benchmarks au path
    sys.path.insert(0, os.path.join(project_dir, 'benchmarks'))

    print_header("BENCHMARK COMPLET - LABELLISATION")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Repertoire: {project_dir}")

    # Verifier les dependances
    if not check_dependencies():
        return 1

    # Chemins de sortie
    results_dir = 'benchmarks/results'
    csv_path = os.path.join(results_dir, 'benchmark_results.csv')
    graphs_dir = os.path.join(results_dir, 'graphs')
    report_path = os.path.join(results_dir, 'rapport_benchmark.txt')

    # Creer les repertoires
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(graphs_dir, exist_ok=True)

    # Executer le benchmark
    results = run_benchmark(args.runs, args.input, csv_path)

    if not results:
        print("\n  ERREUR: Aucun resultat obtenu")
        return 1

    # Generer les graphiques
    generate_graphs(csv_path, graphs_dir)

    # Generer le rapport
    generate_report(results, report_path, args.runs)

    print_header("BENCHMARK TERMINE")
    print(f"  Resultats CSV:  {csv_path}")
    print(f"  Graphiques:     {graphs_dir}/")
    print(f"  Rapport:        {report_path}")
    print("")

    return 0


if __name__ == "__main__":
    sys.exit(main())
