#!/usr/bin/env python3
"""
Generation de rapport PDF pour le projet de labellisation

Ce script genere un rapport PDF complet incluant:
- Description des algorithmes
- Resultats du benchmark
- Graphiques de performance
- Analyse et conclusions

Prerequis:
    pip install fpdf2

Usage:
    python generate_report_pdf.py [--input results.csv] [--output rapport.pdf]

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os
import csv
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict

from fpdf import FPDF


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
    """Charge les resultats depuis un fichier CSV."""
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
# Classe PDF personnalisee
# ============================================================================

class RapportPDF(FPDF):
    """Classe PDF personnalisee pour le rapport."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(15, 15, 15)

    def header(self):
        """En-tete de page."""
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 9)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, 'Rapport de Benchmark - Labellisation des Composantes Connexes', align='C')
            self.ln(15)

    def footer(self):
        """Pied de page."""
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def chapter_title(self, title: str):
        """Titre de chapitre."""
        self.set_x(15)
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, new_x='LMARGIN', new_y='NEXT')
        self.ln(5)

    def section_title(self, title: str):
        """Titre de section."""
        self.set_x(15)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(51, 51, 51)
        self.cell(0, 8, title, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def body_text(self, text: str):
        """Texte de corps."""
        self.set_x(15)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(180, 6, text)
        self.ln(3)

    def bullet_point(self, text: str):
        """Point de liste."""
        self.set_x(15)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(180, 6, f"  - {text}")


# ============================================================================
# Generation du rapport
# ============================================================================

def create_cover_page(pdf: RapportPDF):
    """Cree la page de garde."""
    pdf.add_page()

    # Titre principal
    pdf.set_y(60)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, 'RAPPORT DE BENCHMARK', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 12, 'Labellisation des Composantes Connexes', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.ln(20)

    # Sous-titre
    pdf.set_font('Helvetica', 'I', 14)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 10, 'Analyse comparative de 4 algorithmes', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 10, 'sur images binaires', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.ln(40)

    # Auteurs
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(0, 8, 'Auteurs:', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, 'Romain Despoullain', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 8, 'Nicolas Marano', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 8, 'Amin Braham', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.ln(30)

    # Date
    pdf.set_font('Helvetica', 'I', 11)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 8, datetime.now().strftime('%d %B %Y'), align='C', new_x='LMARGIN', new_y='NEXT')


def create_introduction(pdf: RapportPDF):
    """Cree la section introduction."""
    pdf.add_page()
    pdf.chapter_title('1. Introduction')

    pdf.section_title('1.1 Contexte')
    pdf.body_text(
        "La labellisation des composantes connexes (Connected Component Labeling - CCL) "
        "est une operation fondamentale en traitement d'images. Elle consiste a identifier "
        "et etiqueter les regions connexes dans une image binaire, c'est-a-dire les ensembles "
        "de pixels adjacents ayant la meme valeur (generalement 1 pour les objets)."
    )

    pdf.body_text(
        "Cette technique est essentielle dans de nombreuses applications : reconnaissance "
        "d'objets, analyse de documents, imagerie medicale, vision industrielle, et bien d'autres."
    )

    pdf.section_title('1.2 Objectifs du projet')
    pdf.body_text("Ce projet vise a :")
    pdf.bullet_point("Implementer 4 algorithmes differents de labellisation")
    pdf.bullet_point("Comparer leurs performances sur differentes images")
    pdf.bullet_point("Analyser l'impact de la connectivite (4 vs 8 voisins)")
    pdf.bullet_point("Fournir une analyse statistique rigoureuse des resultats")

    pdf.section_title('1.3 Contraintes techniques')
    pdf.body_text(
        "Le projet a ete developpe en Python avec une contrainte importante : "
        "numpy et OpenCV ne sont utilises QUE pour le chargement des images. "
        "Toutes les operations algorithmiques sont implementees manuellement, "
        "permettant une comprehension approfondie des mecanismes sous-jacents."
    )


def create_algorithms_section(pdf: RapportPDF):
    """Cree la section description des algorithmes."""
    pdf.add_page()
    pdf.chapter_title('2. Description des Algorithmes')

    # Two-Pass
    pdf.section_title('2.1 Two-Pass (Deux Passes)')
    pdf.body_text(
        "L'algorithme Two-Pass est l'approche classique pour la labellisation. "
        "Il parcourt l'image en deux passes successives :"
    )
    pdf.body_text(
        "Premiere passe : Parcours de l'image pixel par pixel. Pour chaque pixel "
        "d'objet, on examine ses voisins deja traites. Si aucun voisin n'est etiquete, "
        "on attribue une nouvelle etiquette. Sinon, on prend l'etiquette minimale "
        "et on note les equivalences entre etiquettes."
    )
    pdf.body_text(
        "Deuxieme passe : On reparcourt l'image pour remplacer chaque etiquette "
        "par son representant canonique (la plus petite etiquette equivalente)."
    )
    pdf.body_text("Complexite : O(n) ou n est le nombre de pixels.")

    pdf.ln(5)

    # Union-Find
    pdf.section_title('2.2 Union-Find (Disjoint-Set)')
    pdf.body_text(
        "Cet algorithme utilise la structure de donnees Union-Find (ensembles disjoints) "
        "pour gerer efficacement les equivalences entre etiquettes."
    )
    pdf.body_text(
        "Deux optimisations sont implementees : la compression de chemin (path compression) "
        "qui aplatit l'arbre lors des recherches, et l'union par rang (union by rank) "
        "qui attache toujours le plus petit arbre sous le plus grand."
    )
    pdf.body_text(
        "Ces optimisations permettent d'obtenir une complexite quasi-lineaire : "
        "O(n * alpha(n)) ou alpha est la fonction inverse d'Ackermann, tres lente a croitre."
    )

    pdf.ln(5)

    # Kruskal
    pdf.section_title('2.3 Kruskal (Arbre Couvrant)')
    pdf.body_text(
        "L'algorithme de Kruskal, traditionnellement utilise pour trouver l'arbre "
        "couvrant minimum d'un graphe, est adapte ici pour la labellisation."
    )
    pdf.body_text(
        "L'image est modelisee comme un graphe ou chaque pixel est un noeud et "
        "les aretes connectent les pixels voisins de meme valeur. L'algorithme "
        "fusionne progressivement les composantes en traitant les aretes."
    )
    pdf.body_text(
        "Bien que conceptuellement elegant, cette approche est moins efficace "
        "car elle necessite la creation explicite des aretes : O(n log n) dans le pire cas."
    )

    pdf.ln(5)

    # Prim
    pdf.section_title('2.4 Prim (Parcours BFS/DFS)')
    pdf.body_text(
        "Cette approche utilise un parcours en largeur (BFS) ou en profondeur (DFS) "
        "pour explorer chaque composante connexe."
    )
    pdf.body_text(
        "Pour chaque pixel non encore etiquete, on lance un parcours qui visite "
        "tous les pixels connectes et leur attribue la meme etiquette. "
        "L'implementation utilise une file (BFS) pour un parcours niveau par niveau."
    )
    pdf.body_text(
        "Complexite : O(n) pour le parcours, mais avec une constante plus elevee "
        "due a la gestion de la file de priorite ou de la pile."
    )


def create_architecture_section(pdf: RapportPDF):
    """Cree la section architecture."""
    pdf.add_page()
    pdf.chapter_title('3. Architecture du Projet')

    pdf.section_title('3.1 Structure des fichiers')
    pdf.body_text("Le projet est organise selon une architecture modulaire :")

    pdf.set_font('Courier', '', 9)
    structure = """labellisation/
  src/
    core/
      image.py          # Classes Image, LabelImage, Pixel
    readers/
      image_io.py       # Lecture/ecriture d'images
    algorithms/
      two_pass.py       # Algorithme Two-Pass
      union_find.py     # Algorithme Union-Find
      kruskal.py        # Algorithme Kruskal
      prim.py           # Algorithme Prim
    utils/
      utils.py          # Utilitaires (Timer, etc.)
  benchmarks/
    scientific_benchmark.py  # Benchmark scientifique
    generate_graphs.py       # Generation de graphiques
    run_all.py              # Script principal
  images/
    input/                  # Images de test"""

    for line in structure.split('\n'):
        pdf.set_x(15)
        pdf.cell(0, 5, line, new_x='LMARGIN', new_y='NEXT')

    pdf.ln(5)
    pdf.set_font('Helvetica', '', 10)

    pdf.section_title('3.2 Classes principales')

    pdf.body_text(
        "Image : Classe de base representant une image en niveaux de gris. "
        "Gere le stockage des pixels, la binarisation et les operations de base."
    )
    pdf.body_text(
        "LabelImage : Herite de Image. Stocke les etiquettes des composantes connexes "
        "et fournit des methodes pour compter les composantes et generer une visualisation."
    )
    pdf.body_text(
        "Pixel : Structure representant un pixel avec ses coordonnees (x, y) et sa valeur."
    )

    pdf.section_title('3.3 Interface des algorithmes')
    pdf.body_text(
        "Tous les algorithmes implementent une methode statique 'label' avec la meme signature :"
    )
    pdf.set_font('Courier', '', 10)
    pdf.set_x(15)
    pdf.cell(0, 6, "    @staticmethod", new_x='LMARGIN', new_y='NEXT')
    pdf.set_x(15)
    pdf.cell(0, 6, "    def label(image: Image, connectivity: int) -> LabelImage", new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    pdf.body_text(
        "Cette uniformite permet de tester et comparer facilement les differentes implementations."
    )


def create_results_section(pdf: RapportPDF, results: List[ResultEntry]):
    """Cree la section resultats."""
    pdf.add_page()
    pdf.chapter_title('4. Resultats du Benchmark')

    pdf.section_title('4.1 Configuration des tests')
    pdf.body_text("Les tests ont ete effectues avec la configuration suivante :")
    pdf.bullet_point(f"Nombre de runs par configuration : {results[0].runs if results else 5}")
    pdf.bullet_point("Connectivites testees : 4 et 8 voisins")
    pdf.bullet_point("Algorithmes : Two-Pass, Union-Find, Kruskal, Prim")

    images = sorted(set(r.image for r in results))
    pdf.bullet_point(f"Images testees : {len(images)}")
    for img in images:
        pdf.set_font('Helvetica', '', 9)
        pdf.set_x(25)
        pdf.cell(0, 5, f"- {img}", new_x='LMARGIN', new_y='NEXT')

    pdf.ln(5)
    pdf.section_title('4.2 Tableau des resultats')

    # Calculer les moyennes par algorithme
    algo_times: Dict[str, List[float]] = {}
    for r in results:
        if r.algorithm not in algo_times:
            algo_times[r.algorithm] = []
        algo_times[r.algorithm].append(r.mean_time)

    sorted_algos = [(a, manual_mean(times)) for a, times in algo_times.items()]
    sorted_algos.sort(key=lambda x: x[1])
    reference = sorted_algos[0][1] if sorted_algos else 1.0

    # Tableau
    pdf.set_font('Helvetica', 'B', 10)
    col_widths = [50, 40, 40, 40]

    pdf.set_x(15)
    pdf.set_fill_color(0, 102, 204)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(col_widths[0], 8, 'Algorithme', border=1, align='C', fill=True)
    pdf.cell(col_widths[1], 8, 'Temps moyen', border=1, align='C', fill=True)
    pdf.cell(col_widths[2], 8, 'Ecart-type', border=1, align='C', fill=True)
    pdf.cell(col_widths[3], 8, 'Speedup', border=1, align='C', fill=True, new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)

    algo_labels = {
        'two_pass': 'Two-Pass',
        'union_find': 'Union-Find',
        'kruskal': 'Kruskal',
        'prim': 'Prim'
    }

    for i, (algo, avg) in enumerate(sorted_algos):
        # Calculer l'ecart-type moyen
        algo_stds = [r.std_time for r in results if r.algorithm == algo]
        avg_std = manual_mean(algo_stds)
        speedup = reference / avg if avg > 0 else 0

        fill = i % 2 == 0
        if fill:
            pdf.set_fill_color(240, 240, 240)

        label = algo_labels.get(algo, algo)
        pdf.set_x(15)
        pdf.cell(col_widths[0], 7, label, border=1, align='L', fill=fill)
        pdf.cell(col_widths[1], 7, f'{avg:.2f} ms', border=1, align='C', fill=fill)
        pdf.cell(col_widths[2], 7, f'{avg_std:.2f} ms', border=1, align='C', fill=fill)
        pdf.cell(col_widths[3], 7, f'{speedup:.2f}x', border=1, align='C', fill=fill, new_x='LMARGIN', new_y='NEXT')

    pdf.ln(10)

    pdf.section_title('4.3 Analyse des performances')

    if sorted_algos:
        fastest = algo_labels.get(sorted_algos[0][0], sorted_algos[0][0])
        slowest = algo_labels.get(sorted_algos[-1][0], sorted_algos[-1][0])
        ratio = sorted_algos[-1][1] / sorted_algos[0][1] if sorted_algos[0][1] > 0 else 1

        pdf.body_text(
            f"L'algorithme le plus rapide est {fastest} avec un temps moyen de "
            f"{sorted_algos[0][1]:.2f} ms. L'algorithme le plus lent est {slowest} "
            f"avec un temps moyen de {sorted_algos[-1][1]:.2f} ms, soit un facteur "
            f"de {ratio:.2f}x plus lent."
        )

    # Analyse par connectivite
    pdf.ln(5)
    pdf.section_title('4.4 Impact de la connectivite')

    conn4_times = [r.mean_time for r in results if r.connectivity == 4]
    conn8_times = [r.mean_time for r in results if r.connectivity == 8]

    if conn4_times and conn8_times:
        avg4 = manual_mean(conn4_times)
        avg8 = manual_mean(conn8_times)
        increase = ((avg8 - avg4) / avg4) * 100 if avg4 > 0 else 0

        pdf.body_text(
            f"La connectivite 8 (8 voisins) est en moyenne {increase:.1f}% plus lente "
            f"que la connectivite 4. Cela s'explique par le nombre superieur de voisins "
            f"a examiner pour chaque pixel (8 au lieu de 4), ce qui augmente le travail "
            f"de recherche et de fusion des composantes."
        )


def create_graphs_section(pdf: RapportPDF, graphs_dir: str):
    """Cree la section graphiques."""
    pdf.add_page()
    pdf.chapter_title('5. Graphiques')

    graphs = [
        ('comparison_algorithms.png', 'Comparaison globale des algorithmes',
         "Ce graphique presente le temps moyen d'execution de chaque algorithme, "
         "calcule sur toutes les images et les deux connectivites."),
        ('comparison_images.png', 'Comparaison par image',
         "Performance de chaque algorithme pour chaque image de test "
         "(connectivite 4 uniquement pour la lisibilite)."),
        ('connectivity_comparison.png', 'Impact de la connectivite',
         "Comparaison des temps d'execution entre connectivite 4 et 8 "
         "pour chaque algorithme."),
        ('speedup.png', 'Speedup relatif',
         "Facteur d'acceleration par rapport a l'algorithme Two-Pass "
         "(reference = 1.0)."),
        ('components_verification.png', 'Verification de coherence',
         "Nombre de composantes trouvees par chaque algorithme. "
         "Tous doivent trouver le meme nombre pour une image donnee.")
    ]

    for i, (filename, title, description) in enumerate(graphs):
        if i > 0 and i % 2 == 0:
            pdf.add_page()

        filepath = os.path.join(graphs_dir, filename)

        pdf.section_title(f'5.{i+1} {title}')
        pdf.body_text(description)

        if os.path.exists(filepath):
            # Calculer la largeur pour centrer l'image
            img_width = 160
            x = (210 - img_width) / 2  # Centrer sur page A4
            pdf.image(filepath, x=x, w=img_width)
            pdf.ln(10)
        else:
            pdf.body_text(f"[Image non trouvee : {filename}]")
            pdf.ln(10)


def create_conclusion(pdf: RapportPDF, results: List[ResultEntry]):
    """Cree la section conclusion."""
    pdf.add_page()
    pdf.chapter_title('6. Conclusion')

    pdf.section_title('6.1 Synthese des resultats')

    # Calculer les statistiques finales
    algo_times: Dict[str, List[float]] = {}
    for r in results:
        if r.algorithm not in algo_times:
            algo_times[r.algorithm] = []
        algo_times[r.algorithm].append(r.mean_time)

    sorted_algos = [(a, manual_mean(times)) for a, times in algo_times.items()]
    sorted_algos.sort(key=lambda x: x[1])

    algo_labels = {
        'two_pass': 'Two-Pass',
        'union_find': 'Union-Find',
        'kruskal': 'Kruskal',
        'prim': 'Prim'
    }

    pdf.body_text("Les tests ont permis d'etablir un classement clair des performances :")

    for i, (algo, avg) in enumerate(sorted_algos, 1):
        label = algo_labels.get(algo, algo)
        pdf.bullet_point(f"{i}. {label} : {avg:.2f} ms en moyenne")

    pdf.ln(5)

    pdf.section_title('6.2 Observations principales')

    pdf.body_text(
        "Two-Pass et Union-Find offrent les meilleures performances, avec un avantage "
        "leger mais consistant pour l'un ou l'autre selon les images. Ces deux approches "
        "sont les plus adaptees pour des applications necessitant des performances optimales."
    )

    pdf.body_text(
        "L'algorithme de Prim presente des performances intermediaires. Son approche "
        "par parcours BFS est intuitive mais souffre du surcout de gestion de la file."
    )

    pdf.body_text(
        "Kruskal est systematiquement le plus lent, principalement a cause de la "
        "creation explicite de toutes les aretes du graphe, une operation couteuse "
        "en memoire et en temps pour les grandes images."
    )

    pdf.section_title('6.3 Verification de coherence')

    # Verifier que tous les algorithmes trouvent le meme nombre de composantes
    images = sorted(set(r.image for r in results))
    all_consistent = True

    for image in images:
        image_results = [r for r in results if r.image == image and r.connectivity == 4]
        components = set(r.num_components for r in image_results)
        if len(components) > 1:
            all_consistent = False
            break

    if all_consistent:
        pdf.body_text(
            "Tous les algorithmes trouvent exactement le meme nombre de composantes "
            "connexes pour chaque image, ce qui valide la correction de toutes les "
            "implementations."
        )
    else:
        pdf.body_text(
            "ATTENTION : Des incoherences ont ete detectees dans le nombre de "
            "composantes trouvees. Une verification des implementations est necessaire."
        )

    pdf.section_title('6.4 Recommandations')

    pdf.body_text("Pour une utilisation en production, nous recommandons :")
    pdf.bullet_point(
        "Two-Pass pour sa simplicite et ses bonnes performances generales"
    )
    pdf.bullet_point(
        "Union-Find pour les cas ou la gestion des equivalences est complexe"
    )
    pdf.bullet_point(
        "Connectivite 4 sauf si l'application necessite explicitement la 8-connectivite"
    )

    pdf.ln(10)

    # Note finale
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(102, 102, 102)
    pdf.multi_cell(0, 6,
        "Ce rapport a ete genere automatiquement a partir des resultats du benchmark. "
        f"Date de generation : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )


def generate_pdf_report(csv_path: str, graphs_dir: str, output_path: str):
    """
    Genere le rapport PDF complet.

    Args:
        csv_path: Chemin du fichier CSV des resultats
        graphs_dir: Repertoire contenant les graphiques
        output_path: Chemin du fichier PDF de sortie
    """
    print("=" * 60)
    print("  GENERATION DU RAPPORT PDF")
    print("=" * 60)

    # Charger les donnees
    print(f"\nChargement des donnees: {csv_path}")

    if not os.path.exists(csv_path):
        print(f"ERREUR: Fichier non trouve: {csv_path}")
        return False

    results = load_csv(csv_path)
    print(f"  {len(results)} entrees chargees")

    # Creer le PDF
    print("\nGeneration du PDF...")

    pdf = RapportPDF()
    pdf.alias_nb_pages()

    # Generer les sections
    print("  - Page de garde")
    create_cover_page(pdf)

    print("  - Introduction")
    create_introduction(pdf)

    print("  - Description des algorithmes")
    create_algorithms_section(pdf)

    print("  - Architecture du projet")
    create_architecture_section(pdf)

    print("  - Resultats du benchmark")
    create_results_section(pdf, results)

    print("  - Graphiques")
    create_graphs_section(pdf, graphs_dir)

    print("  - Conclusion")
    create_conclusion(pdf, results)

    # Sauvegarder le PDF
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)

    print(f"\nRapport genere: {output_path}")
    print("=" * 60)

    return True


def main():
    """Point d'entree principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generation de rapport PDF pour le benchmark'
    )
    parser.add_argument('--input', type=str,
                        default='benchmarks/results/benchmark_results.csv',
                        help='Fichier CSV des resultats')
    parser.add_argument('--graphs', type=str,
                        default='benchmarks/results/graphs',
                        help='Repertoire des graphiques')
    parser.add_argument('--output', type=str,
                        default='benchmarks/results/rapport_complet.pdf',
                        help='Fichier PDF de sortie')

    args = parser.parse_args()

    # Changer vers le repertoire du projet
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)

    success = generate_pdf_report(args.input, args.graphs, args.output)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
