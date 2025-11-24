"""
Module algorithms/prim.py - Algorithme de Prim pour la labellisation

Comme Kruskal, Prim est un algorithme de Minimum Spanning Tree (MST).
Il utilise également le modèle de graphe du CM05.

DIFFÉRENCE KRUSKAL vs PRIM :

- Kruskal : approche "par arêtes"
  -> Trie toutes les arêtes et les ajoute une par une

- Prim : approche "par sommets"
  -> Grandit l'arbre à partir d'un sommet initial
  -> À chaque étape, ajoute le sommet le plus proche de l'arbre courant

APPLICATION À LA LABELLISATION :

Pour la labellisation, on adapte Prim :
- Construire une forêt (pas un seul arbre) car le graphe a plusieurs
  composantes connexes
- Algorithme :
  1. Pour chaque pixel "objet" non encore labellisé :
     a) Créer un nouveau label
     b) Lancer Prim depuis ce pixel pour explorer toute sa composante
     c) Tous les pixels atteints reçoivent ce label

IMPLÉMENTATION :

On utilise une approche BFS (Breadth-First Search) / DFS (Depth-First Search)
simplifiée au lieu de Prim avec file de priorité, car :
- Toutes les arêtes ont le même poids (pas besoin de file de priorité)
- BFS/DFS explore exactement la même composante connexe que Prim
- Plus simple et plus efficace

COMPLEXITÉ :
- Temps: O(N) où N est le nombre de pixels
  (chaque pixel est visité une seule fois)
- Espace: O(N) pour la file (dans le pire cas)

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os
from typing import List, Tuple
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.image import Image, LabelImage
from utils.utils import get_neighbors


class Prim:
    """
    Algorithme de Prim pour la labellisation.

    Stratégie : Pour chaque pixel non labellisé, lancer une exploration
    BFS pour découvrir toute sa composante connexe.

    Cette approche est inspirée de Prim car elle "grandit" chaque
    composante à partir d'un point de départ, en ajoutant progressivement
    les pixels adjacents.
    """

    @staticmethod
    def label(input_image: Image, connectivity: int = 4) -> LabelImage:
        """
        Labellise les composantes connexes d'une image binaire.

        Args:
            input_image: Image binaire (0 = fond, 255 = objet)
            connectivity: Type de connectivité (4 ou 8)

        Returns:
            Image labellisée avec les composantes connexes
        """
        width = input_image.width
        height = input_image.height

        labels = LabelImage(width, height)
        labels.fill(0)
        current_label = 0

        """
        Parcours de l'image : pour chaque pixel objet non labellisé,
        lancer un BFS pour explorer toute sa composante connexe.
        """
        for x in range(height):
            for y in range(width):
                if input_image.at(x, y) != 0 and labels.at(x, y) == 0:
                    current_label += 1
                    Prim._bfs(input_image, labels, x, y, current_label, connectivity)

        return labels

    @staticmethod
    def _bfs(input_image: Image, labels: LabelImage,
             start_x: int, start_y: int, label: int, connectivity: int) -> None:
        """
        Explore une composante connexe par parcours en largeur (BFS).

        BFS garantit :
        - Tous les pixels de la composante sont visités
        - Parcours par "couches" (bonne localité cache)
        - Pas de risque de stack overflow (contrairement à DFS récursif)

        Args:
            input_image: Image binaire
            labels: Image de labels (modifiée)
            start_x: Coordonnée ligne de départ
            start_y: Coordonnée colonne de départ
            label: Label à affecter
            connectivity: Connectivité (4 ou 8)
        """
        width = input_image.width
        height = input_image.height

        queue = deque()
        queue.append((start_x, start_y))
        labels.set_at(start_x, start_y, label)

        while queue:
            x, y = queue.popleft()
            neighbors = get_neighbors(x, y, width, height, connectivity)

            for nx, ny in neighbors:
                if input_image.at(nx, ny) != 0 and labels.at(nx, ny) == 0:
                    labels.set_at(nx, ny, label)
                    queue.append((nx, ny))

    @staticmethod
    def _dfs(input_image: Image, labels: LabelImage,
             x: int, y: int, label: int, connectivity: int) -> None:
        """
        Explore une composante connexe par parcours en profondeur (DFS).

        Version récursive, plus simple mais :
        - Risque de stack overflow pour de grandes composantes
        - Moins bonne localité cache que BFS

        Cette fonction est fournie comme alternative mais n'est pas
        utilisée par défaut (on préfère BFS).

        Args:
            input_image: Image binaire
            labels: Image de labels (modifiée)
            x: Coordonnée ligne courante
            y: Coordonnée colonne courante
            label: Label à affecter
            connectivity: Connectivité (4 ou 8)
        """
        width = input_image.width
        height = input_image.height

        if not labels.is_valid(x, y):
            return
        if input_image.at(x, y) == 0:
            return
        if labels.at(x, y) != 0:
            return

        labels.set_at(x, y, label)
        neighbors = get_neighbors(x, y, width, height, connectivity)

        for nx, ny in neighbors:
            Prim._dfs(input_image, labels, nx, ny, label, connectivity)
