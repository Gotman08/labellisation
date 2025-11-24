"""
Module algorithms/union_find.py - Algorithme de labellisation par Union-Find

Cette approche utilise directement la structure de données Union-Find
(Disjoint-Set) pour gérer les composantes connexes.

PRINCIPE (modèle de partition du CM05) :

1. Initialisation :
   - Chaque pixel "objet" est un ensemble singleton (sa propre composante)
   - Créer une structure Union-Find pour gérer ces ensembles

2. Parcours de l'image :
   - Pour chaque pixel "objet" p :
       - Pour chaque voisin "objet" v (selon la connectivité) :
           - Si Find(p) != Find(v) : les pixels sont dans des composantes différentes
           - Alors Union(p, v) : fusionner les deux composantes

3. Labellisation finale :
   - Pour chaque pixel, son label est Find(pixel)

STRUCTURE UNION-FIND (CM05: modèle de partition) :

Cette structure maintient une partition de l'ensemble des pixels.
Chaque partition représente une composante connexe.

OPTIMISATIONS :
- Path compression : lors de Find, faire pointer tous les noeuds
  parcourus directement vers la racine
- Union by rank : lors de Union, attacher l'arbre de rang inférieur
  sous l'arbre de rang supérieur

COMPLEXITÉ :
- Temps: O(N * alpha(N)) = O(N) où N est le nombre de pixels
- Espace: O(N) pour la structure Union-Find

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os
from typing import List

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.image import Image, LabelImage


class DisjointSet:
    """
    Structure Union-Find optimisée.

    Implémente la structure de données Disjoint-Set avec :
    - Path compression dans Find
    - Union by rank
    """

    def __init__(self, size: int):
        """
        Constructeur.

        Args:
            size: Nombre d'éléments
        """
        # Initialisation : chaque élément est sa propre racine
        self._parent = list(range(size))
        self._rank = [0] * size

    def find(self, x: int) -> int:
        """
        Trouve le représentant de l'ensemble contenant x.

        Utilise la path compression : tous les noeuds parcourus
        sont directement reliés à la racine pour accélérer les
        futurs Find.

        Args:
            x: Élément

        Returns:
            Représentant (racine) de l'ensemble
        """
        if self._parent[x] != x:
            # Path compression récursif
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def unite(self, x: int, y: int) -> bool:
        """
        Fusionne les ensembles contenant x et y.

        Utilise union by rank : l'arbre de rang inférieur est attaché
        sous l'arbre de rang supérieur pour maintenir l'arbre plat.

        Args:
            x: Premier élément
            y: Deuxième élément

        Returns:
            True si fusion effectuée, False si déjà dans le même ensemble
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Déjà dans le même ensemble

        # Union by rank
        if self._rank[root_x] < self._rank[root_y]:
            self._parent[root_x] = root_y
        elif self._rank[root_x] > self._rank[root_y]:
            self._parent[root_y] = root_x
        else:
            # Rangs égaux : attacher root_y sous root_x et incrémenter le rang
            self._parent[root_y] = root_x
            self._rank[root_x] += 1

        return True


class UnionFind:
    """
    Algorithme de labellisation par Union-Find.

    Cette implémentation suit le modèle de partition du CM05 :
    - L'image est vue comme un ensemble de pixels
    - On cherche à partitionner cet ensemble en composantes connexes
    - Chaque partition est gérée par la structure Union-Find
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

        # Créer la structure Union-Find pour tous les pixels
        ds = DisjointSet(size)

        # Créer l'image de labels
        labels = LabelImage(width, height)
        labels.fill(0)

        # ====================================================================
        # Phase 1 : Union des pixels adjacents
        # ====================================================================

        # Parcours de l'image pour fusionner les pixels adjacents
        # Pour chaque pixel "objet" :
        # - Examiner ses voisins (selon la connectivité)
        # - Si un voisin est aussi "objet", fusionner leurs ensembles
        #
        # Note: On ne parcourt que les voisins "avant" (Nord et Ouest)
        # pour éviter de traiter deux fois la même paire de pixels.

        for x in range(height):
            for y in range(width):
                # Ignorer les pixels de fond
                if input_image.at(x, y) == 0:
                    continue

                current_idx = UnionFind._get_index(x, y, width)

                # Examiner les voisins "précédents" pour éviter les doublons
                if connectivity == 4:
                    # Connectivité 4 : vérifier Nord et Ouest

                    # Nord (x-1, y)
                    if x > 0 and input_image.at(x - 1, y) != 0:
                        neighbor_idx = UnionFind._get_index(x - 1, y, width)
                        ds.unite(current_idx, neighbor_idx)

                    # Ouest (x, y-1)
                    if y > 0 and input_image.at(x, y - 1) != 0:
                        neighbor_idx = UnionFind._get_index(x, y - 1, width)
                        ds.unite(current_idx, neighbor_idx)

                elif connectivity == 8:
                    # Connectivité 8 : vérifier Nord-Ouest, Nord, Nord-Est, Ouest

                    # Nord-Ouest (x-1, y-1)
                    if x > 0 and y > 0 and input_image.at(x - 1, y - 1) != 0:
                        neighbor_idx = UnionFind._get_index(x - 1, y - 1, width)
                        ds.unite(current_idx, neighbor_idx)

                    # Nord (x-1, y)
                    if x > 0 and input_image.at(x - 1, y) != 0:
                        neighbor_idx = UnionFind._get_index(x - 1, y, width)
                        ds.unite(current_idx, neighbor_idx)

                    # Nord-Est (x-1, y+1)
                    if x > 0 and y < width - 1 and input_image.at(x - 1, y + 1) != 0:
                        neighbor_idx = UnionFind._get_index(x - 1, y + 1, width)
                        ds.unite(current_idx, neighbor_idx)

                    # Ouest (x, y-1)
                    if y > 0 and input_image.at(x, y - 1) != 0:
                        neighbor_idx = UnionFind._get_index(x, y - 1, width)
                        ds.unite(current_idx, neighbor_idx)

        # ====================================================================
        # Phase 2 : Labellisation finale
        # ====================================================================

        # Convertir les représentants Union-Find en labels compacts
        #
        # Les représentants Union-Find peuvent avoir des valeurs dispersées
        # (ex: 5, 42, 137...). On les remappe sur des labels compacts
        # (ex: 1, 2, 3...) pour une meilleure visualisation.

        # Première sous-passe : trouver tous les représentants uniques
        root_to_label = [0] * size
        next_label = 1

        for x in range(height):
            for y in range(width):
                if input_image.at(x, y) == 0:
                    labels.set_at(x, y, 0)  # Fond
                    continue

                idx = UnionFind._get_index(x, y, width)
                root = ds.find(idx)

                # Si ce représentant n'a pas encore de label, lui en affecter un
                if root_to_label[root] == 0:
                    root_to_label[root] = next_label
                    next_label += 1

                # Affecter le label au pixel
                labels.set_at(x, y, root_to_label[root])

        return labels

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
