"""
Module algorithms/kruskal.py - Algorithme de Kruskal pour la labellisation

Cette approche utilise le modèle de graphe (CM05) pour la labellisation.

MODÈLE DE GRAPHE (CM05) :

L'image est vue comme un graphe G = (V, E) où :
- V = ensemble des pixels "objet" (sommets)
- E = ensemble des arêtes entre pixels adjacents (selon la connectivité)

ALGORITHME DE KRUSKAL :

Kruskal est un algorithme classique pour trouver un Arbre Couvrant de
Poids Minimum (MST - Minimum Spanning Tree).

1. Trier toutes les arêtes par poids croissant
2. Pour chaque arête (u, v) dans l'ordre :
   - Si u et v sont dans des composantes différentes :
       - Ajouter l'arête au MST
       - Fusionner les composantes de u et v (Union-Find)

APPLICATION À LA LABELLISATION :

Pour la labellisation, on adapte Kruskal :
- Toutes les arêtes ont le même poids (poids = 1)
- On construit une FORÊT COUVRANTE (pas un seul arbre)
- Chaque arbre de la forêt = une composante connexe

COMPLEXITÉ :
- Temps: O(E log E) pour le tri des arêtes
  où E = nombre d'arêtes ≈ 2N pour connectivité 4, ≈ 4N pour connectivité 8
- Espace: O(E + V) pour stocker le graphe

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os
from typing import List, Tuple
from dataclasses import dataclass

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.image import Image, LabelImage


@dataclass
class Edge:
    """Structure représentant une arête du graphe."""
    u: int      # Premier sommet (index linéaire du pixel)
    v: int      # Deuxième sommet (index linéaire du pixel)
    weight: int = 1  # Poids de l'arête (toujours 1 pour la labellisation)

    def __lt__(self, other: 'Edge') -> bool:
        """Opérateur de comparaison pour le tri."""
        return self.weight < other.weight


class DisjointSetKruskal:
    """
    Structure Union-Find pour Kruskal.

    Identique à celle utilisée dans union_find.py
    (on la garde ici pour que chaque algorithme soit autonome)
    """

    def __init__(self, size: int):
        """
        Constructeur.

        Args:
            size: Nombre d'éléments
        """
        self._parent = list(range(size))
        self._rank = [0] * size

    def find(self, x: int) -> int:
        """
        Trouve le représentant de l'ensemble contenant x.

        Args:
            x: Élément

        Returns:
            Représentant (racine) de l'ensemble
        """
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def unite(self, x: int, y: int) -> bool:
        """
        Fusionne les ensembles contenant x et y.

        Args:
            x: Premier élément
            y: Deuxième élément

        Returns:
            True si fusion effectuée, False si déjà dans le même ensemble
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self._rank[root_x] < self._rank[root_y]:
            self._parent[root_x] = root_y
        elif self._rank[root_x] > self._rank[root_y]:
            self._parent[root_y] = root_x
        else:
            self._parent[root_y] = root_x
            self._rank[root_x] += 1

        return True


class Kruskal:
    """
    Algorithme de Kruskal pour la labellisation.

    Basé sur le modèle de graphe du CM05 :
    - Pixels "objet" = sommets
    - Adjacences = arêtes
    - Construire une forêt couvrante de poids minimum
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
        size = width * height

        # Créer l'image de labels
        labels = LabelImage(width, height)
        labels.fill(0)

        # ====================================================================
        # Étape 1 : Construire les arêtes du graphe
        # ====================================================================

        edges = Kruskal._build_edges(input_image, connectivity)

        # ====================================================================
        # Étape 2 : Trier les arêtes par poids (caractéristique de Kruskal)
        # ====================================================================

        # Dans le cas de la labellisation, toutes les arêtes ont le même poids.
        # Le tri ne change donc pas l'ordre relatif, mais on le fait quand même
        # pour rester fidèle à l'algorithme de Kruskal classique.
        edges.sort()

        # ====================================================================
        # Étape 3 : Algorithme de Kruskal avec Union-Find
        # ====================================================================

        # Pour chaque arête, fusionner les composantes si elles sont différentes.
        # À la fin, tous les pixels connectés seront dans la même composante.
        ds = DisjointSetKruskal(size)

        for edge in edges:
            # Essayer de fusionner les deux sommets de l'arête
            ds.unite(edge.u, edge.v)

        # ====================================================================
        # Étape 4 : Labellisation finale
        # ====================================================================

        # Remapper les représentants Union-Find en labels compacts
        root_to_label = [0] * size
        next_label = 1

        for x in range(height):
            for y in range(width):
                if input_image.at(x, y) == 0:
                    labels.set_at(x, y, 0)  # Fond
                    continue

                idx = Kruskal._get_index(x, y, width)
                root = ds.find(idx)

                if root_to_label[root] == 0:
                    root_to_label[root] = next_label
                    next_label += 1

                labels.set_at(x, y, root_to_label[root])

        return labels

    @staticmethod
    def _build_edges(input_image: Image, connectivity: int) -> List[Edge]:
        """
        Construit la liste des arêtes du graphe.

        Une arête existe entre deux pixels si :
        1. Les deux pixels sont "objet" (valeur != 0)
        2. Les deux pixels sont adjacents (selon la connectivité)

        Pour éviter les arêtes en double, on ne crée des arêtes que vers
        les voisins "avant" (Nord et Ouest pour 4-conn, + diagonales pour 8-conn)

        Args:
            input_image: Image binaire
            connectivity: Connectivité (4 ou 8)

        Returns:
            Liste des arêtes
        """
        edges = []
        width = input_image.width
        height = input_image.height

        for x in range(height):
            for y in range(width):
                # Ignorer les pixels de fond
                if input_image.at(x, y) == 0:
                    continue

                current_idx = Kruskal._get_index(x, y, width)

                if connectivity == 4:
                    # Connectivité 4 : créer des arêtes vers Nord et Ouest

                    # Nord (x-1, y)
                    if x > 0 and input_image.at(x - 1, y) != 0:
                        neighbor_idx = Kruskal._get_index(x - 1, y, width)
                        edges.append(Edge(current_idx, neighbor_idx, 1))

                    # Ouest (x, y-1)
                    if y > 0 and input_image.at(x, y - 1) != 0:
                        neighbor_idx = Kruskal._get_index(x, y - 1, width)
                        edges.append(Edge(current_idx, neighbor_idx, 1))

                elif connectivity == 8:
                    # Connectivité 8 : créer des arêtes vers tous les voisins "avant"

                    # Nord-Ouest (x-1, y-1)
                    if x > 0 and y > 0 and input_image.at(x - 1, y - 1) != 0:
                        neighbor_idx = Kruskal._get_index(x - 1, y - 1, width)
                        edges.append(Edge(current_idx, neighbor_idx, 1))

                    # Nord (x-1, y)
                    if x > 0 and input_image.at(x - 1, y) != 0:
                        neighbor_idx = Kruskal._get_index(x - 1, y, width)
                        edges.append(Edge(current_idx, neighbor_idx, 1))

                    # Nord-Est (x-1, y+1)
                    if x > 0 and y < width - 1 and input_image.at(x - 1, y + 1) != 0:
                        neighbor_idx = Kruskal._get_index(x - 1, y + 1, width)
                        edges.append(Edge(current_idx, neighbor_idx, 1))

                    # Ouest (x, y-1)
                    if y > 0 and input_image.at(x, y - 1) != 0:
                        neighbor_idx = Kruskal._get_index(x, y - 1, width)
                        edges.append(Edge(current_idx, neighbor_idx, 1))

        return edges

    @staticmethod
    def _get_index(x: int, y: int, width: int) -> int:
        """
        Convertit les coordonnées 2D en index 1D.

        Args:
            x: Coordonnée ligne
            y: Coordonnée colonne
            width: Largeur de l'image

        Returns:
            Index linéaire
        """
        return x * width + y
