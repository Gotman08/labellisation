"""
Module algorithms/two_pass.py - Algorithme de labellisation en deux passes

Cet algorithme est l'approche classique pour la labellisation des
composantes connexes d'une image binaire.

PRINCIPE (décrit dans la source ESIEE) :

1ère Passe - Étiquetage provisoire et table d'équivalence :
   - Parcours de l'image de gauche à droite, de haut en bas
   - Pour chaque pixel "objet" (blanc) :
       a) Si aucun voisin "objet" déjà traité : nouveau label
       b) Si un voisin "objet" : prendre son label
       c) Si plusieurs voisins avec labels différents :
          - Prendre le plus petit label
          - Noter l'équivalence dans la table

Passe intermédiaire - Résolution des équivalences :
   - Calculer les "labels racine" pour chaque classe d'équivalence
   - Utilise une structure Union-Find simplifiée

2ème Passe - Relabellisation finale :
   - Parcours de l'image
   - Remplacer chaque label provisoire par son label racine

COMPLEXITÉ :
- Temps: O(N) où N est le nombre de pixels (2 passes linéaires)
- Espace: O(N) pour l'image de labels + O(L) pour la table d'équivalence
          où L est le nombre de labels provisoires

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import sys
import os
from typing import List, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.image import Image, LabelImage


class EquivalenceTable:
    """
    Structure pour gérer les équivalences entre labels.

    Implémente une version simplifiée d'Union-Find :
    - Chaque label pointe vers son "parent"
    - La racine d'un label est trouvée par remontée
    - Path compression pour optimiser les recherches
    """

    def __init__(self):
        """Initialise la table d'équivalence. Label 0 réservé pour le fond."""
        self._parent = [0]

    def make_set(self) -> int:
        """
        Crée un nouveau label.

        Returns:
            Nouveau label
        """
        label = len(self._parent)
        self._parent.append(label)
        return label

    def find(self, x: int) -> int:
        """
        Trouve la racine d'un label (avec path compression).

        Args:
            x: Label

        Returns:
            Label racine
        """
        if x <= 0 or x >= len(self._parent):
            return 0

        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])

        return self._parent[x]

    def unite(self, x: int, y: int) -> None:
        """
        Fusionne deux labels (union).

        Fait pointer le plus grand label vers le plus petit
        pour minimiser les labels finaux.

        Args:
            x: Premier label
            y: Deuxième label
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return

        if root_x < root_y:
            self._parent[root_y] = root_x
        else:
            self._parent[root_x] = root_y

    def size(self) -> int:
        """Retourne le nombre de labels."""
        return len(self._parent)


class TwoPass:
    """
    Algorithme de labellisation en deux passes.

    Cet algorithme est optimisé pour la localité cache grâce à
    ses parcours séquentiels de l'image (source ESIEE).
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

        equiv = EquivalenceTable()

        TwoPass._first_pass(input_image, labels, equiv, connectivity)
        TwoPass._second_pass(labels, equiv)

        return labels

    @staticmethod
    def _first_pass(input_image: Image, labels: LabelImage,
                    equiv: EquivalenceTable, connectivity: int) -> None:
        """
        Première passe : étiquetage provisoire et détection d'équivalences.

        Parcours de l'image de gauche à droite, de haut en bas.
        Pour chaque pixel "objet" :
        1. Examiner les voisins déjà traités (au-dessus et à gauche)
        2. Cas possibles :
           a) Aucun voisin objet -> créer un nouveau label
           b) Un seul label parmi les voisins -> utiliser ce label
           c) Plusieurs labels différents -> collision d'équivalence
              - Utiliser le plus petit label
              - Enregistrer l'équivalence dans la table

        Args:
            input_image: Image binaire
            labels: Image de labels (sortie)
            equiv: Table d'équivalence (sortie)
            connectivity: Connectivité (4 ou 8)
        """
        width = input_image.width
        height = input_image.height

        for x in range(height):
            for y in range(width):
                if input_image.at(x, y) == 0:
                    labels.set_at(x, y, 0)
                    continue

                neighbors = TwoPass._get_previous_neighbors(x, y, width, height, connectivity)

                neighbor_labels = []
                for nx, ny in neighbors:
                    if input_image.at(nx, ny) != 0:
                        neighbor_label = labels.at(nx, ny)
                        if neighbor_label > 0:
                            neighbor_labels.append(neighbor_label)

                if not neighbor_labels:
                    new_label = equiv.make_set()
                    labels.set_at(x, y, new_label)
                else:
                    min_label = neighbor_labels[0]
                    for i in range(1, len(neighbor_labels)):
                        if neighbor_labels[i] < min_label:
                            min_label = neighbor_labels[i]

                    labels.set_at(x, y, min_label)

                    for i in range(len(neighbor_labels)):
                        if neighbor_labels[i] != min_label:
                            equiv.unite(min_label, neighbor_labels[i])

    @staticmethod
    def _second_pass(labels: LabelImage, equiv: EquivalenceTable) -> None:
        """
        Deuxième passe : relabellisation avec les labels racine.

        Remplace chaque label provisoire par son label racine
        (résolution des équivalences).

        Cette passe garantit que tous les pixels d'une même composante
        connexe auront exactement le même label final.

        Args:
            labels: Image de labels (entrée/sortie)
            equiv: Table d'équivalence
        """
        width = labels.width
        height = labels.height

        for x in range(height):
            for y in range(width):
                label = labels.at(x, y)
                if label > 0:
                    labels.set_at(x, y, equiv.find(label))

    @staticmethod
    def _get_previous_neighbors(x: int, y: int, width: int, height: int,
                                 connectivity: int) -> List[Tuple[int, int]]:
        """
        Retourne les voisins déjà traités dans un parcours gauche->droite, haut->bas.

        Pour la connectivité 4 :
            [X]     <- Nord (x-1, y) : déjà traité
          [X][P]    <- Ouest (x, y-1) : déjà traité, Pixel courant (P)

        Pour la connectivité 8 :
          [X][X][X]  <- Nord-Ouest, Nord, Nord-Est : déjà traités
          [X][P]     <- Ouest : déjà traité, Pixel courant (P)

        Cette optimisation évite d'examiner les voisins pas encore traités,
        ce qui améliore la localité cache.

        Args:
            x: Coordonnée ligne
            y: Coordonnée colonne
            width: Largeur
            height: Hauteur
            connectivity: Connectivité

        Returns:
            Liste de tuples (x, y) des voisins déjà parcourus
        """
        neighbors = []

        if connectivity == 4:
            if x > 0:
                neighbors.append((x - 1, y))
            if y > 0:
                neighbors.append((x, y - 1))

        elif connectivity == 8:
            if x > 0 and y > 0:
                neighbors.append((x - 1, y - 1))
            if x > 0:
                neighbors.append((x - 1, y))
            if x > 0 and y < width - 1:
                neighbors.append((x - 1, y + 1))
            if y > 0:
                neighbors.append((x, y - 1))

        return neighbors
