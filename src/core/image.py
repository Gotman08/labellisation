"""
Module core/image.py - Classes Image, LabelImage et Pixel

Ce module implémente les structures de données de base pour le traitement d'images.
Toutes les opérations sont implémentées manuellement sans bibliothèque externe.

Note: numpy est utilisé UNIQUEMENT dans io/image_io.py pour charger l'image
depuis un fichier. Ici, tout est fait avec des listes Python pures.

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Pixel:
    """
    Structure représentant un pixel avec ses coordonnées.

    Utilisée pour la manipulation des pixels dans les algorithmes
    de labellisation (notamment pour Union-Find, Kruskal et Prim).
    """
    x: int = 0  # Coordonnée en ligne
    y: int = 0  # Coordonnée en colonne

    def __eq__(self, other: 'Pixel') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Image:
    """
    Classe représentant une image en niveaux de gris.

    Cette classe implémente toutes les opérations de base sur les images
    sans utiliser de bibliothèque externe.

    L'image est stockée en mémoire comme une liste 2D Python.
    """

    def __init__(self, width: int = 0, height: int = 0, max_value: int = 255):
        """
        Constructeur avec dimensions.

        Args:
            width: Largeur de l'image
            height: Hauteur de l'image
            max_value: Valeur maximale des pixels (défaut: 255)
        """
        self._width = width
        self._height = height
        self._max_value = max_value

        # Créer une liste 2D initialisée à 0
        if width > 0 and height > 0:
            self._data = [[0 for _ in range(width)] for _ in range(height)]
        else:
            self._data = []

    @property
    def width(self) -> int:
        """Largeur de l'image."""
        return self._width

    @property
    def height(self) -> int:
        """Hauteur de l'image."""
        return self._height

    @property
    def max_value(self) -> int:
        """Valeur maximale des pixels."""
        return self._max_value

    @property
    def size(self) -> int:
        """Nombre total de pixels."""
        return self._width * self._height

    @property
    def data(self) -> List[List[int]]:
        """Accès direct aux données."""
        return self._data

    @data.setter
    def data(self, value: List[List[int]]):
        """Définit les données de l'image."""
        self._data = value
        if value and len(value) > 0:
            self._height = len(value)
            self._width = len(value[0]) if value[0] else 0
        else:
            self._height = 0
            self._width = 0

    def at(self, x: int, y: int) -> int:
        """
        Accès à un pixel (lecture).

        Args:
            x: Coordonnée ligne
            y: Coordonnée colonne

        Returns:
            Valeur du pixel
        """
        if not self.is_valid(x, y):
            raise IndexError("Coordonnées hors limites")
        return self._data[x][y]

    def set_at(self, x: int, y: int, value: int):
        """
        Définit la valeur d'un pixel.

        Args:
            x: Coordonnée ligne
            y: Coordonnée colonne
            value: Nouvelle valeur du pixel
        """
        if not self.is_valid(x, y):
            raise IndexError("Coordonnées hors limites")
        # S'assurer que la valeur est dans [0, 255]
        if value < 0:
            value = 0
        elif value > 255:
            value = 255
        self._data[x][y] = value

    def is_valid(self, x: int, y: int) -> bool:
        """
        Vérifie si les coordonnées sont valides.

        Args:
            x: Coordonnée ligne
            y: Coordonnée colonne

        Returns:
            True si les coordonnées sont dans l'image
        """
        return 0 <= x < self._height and 0 <= y < self._width

    def fill(self, value: int):
        """
        Remplit l'image avec une valeur (implémentation manuelle).

        Args:
            value: Valeur à affecter à tous les pixels
        """
        for x in range(self._height):
            for y in range(self._width):
                self._data[x][y] = value

    def copy_from(self, other: 'Image'):
        """
        Copie les données d'une autre image (implémentation manuelle).

        Args:
            other: Image source
        """
        self._width = other._width
        self._height = other._height
        self._max_value = other._max_value
        # Copie manuelle profonde
        self._data = [[other._data[x][y] for y in range(other._width)]
                      for x in range(other._height)]

    def binarize(self, threshold: int):
        """
        Binarise l'image avec un seuil (implémentation manuelle).

        Les pixels >= threshold deviennent 255 (blanc)
        Les pixels < threshold deviennent 0 (noir)

        Args:
            threshold: Seuil de binarisation
        """
        for x in range(self._height):
            for y in range(self._width):
                if self._data[x][y] >= threshold:
                    self._data[x][y] = 255
                else:
                    self._data[x][y] = 0

    def copy(self) -> 'Image':
        """
        Crée une copie de l'image (implémentation manuelle).

        Returns:
            Nouvelle instance Image avec les mêmes données
        """
        new_image = Image(self._width, self._height, self._max_value)
        # Copie manuelle profonde
        for x in range(self._height):
            for y in range(self._width):
                new_image._data[x][y] = self._data[x][y]
        return new_image


class LabelImage:
    """
    Classe pour une image d'étiquettes (labels).

    Utilisée pour stocker le résultat de la labellisation.
    Utilise des entiers Python pour supporter un grand nombre de labels.
    """

    def __init__(self, width: int = 0, height: int = 0):
        """
        Constructeur avec dimensions.

        Args:
            width: Largeur de l'image
            height: Hauteur de l'image
        """
        self._width = width
        self._height = height

        # Créer une liste 2D initialisée à 0
        if width > 0 and height > 0:
            self._labels = [[0 for _ in range(width)] for _ in range(height)]
        else:
            self._labels = []

    @property
    def width(self) -> int:
        """Largeur de l'image."""
        return self._width

    @property
    def height(self) -> int:
        """Hauteur de l'image."""
        return self._height

    @property
    def size(self) -> int:
        """Nombre total de pixels."""
        return self._width * self._height

    @property
    def data(self) -> List[List[int]]:
        """Accès direct aux labels."""
        return self._labels

    @data.setter
    def data(self, value: List[List[int]]):
        """Définit les données de labels."""
        self._labels = value
        if value and len(value) > 0:
            self._height = len(value)
            self._width = len(value[0]) if value[0] else 0
        else:
            self._height = 0
            self._width = 0

    def at(self, x: int, y: int) -> int:
        """
        Accès à un label (lecture).

        Args:
            x: Coordonnée ligne
            y: Coordonnée colonne

        Returns:
            Label du pixel
        """
        if not self.is_valid(x, y):
            raise IndexError("Coordonnées hors limites")
        return self._labels[x][y]

    def set_at(self, x: int, y: int, value: int):
        """
        Définit le label d'un pixel.

        Args:
            x: Coordonnée ligne
            y: Coordonnée colonne
            value: Nouveau label
        """
        if not self.is_valid(x, y):
            raise IndexError("Coordonnées hors limites")
        self._labels[x][y] = value

    def is_valid(self, x: int, y: int) -> bool:
        """
        Vérifie si les coordonnées sont valides.

        Args:
            x: Coordonnée ligne
            y: Coordonnée colonne

        Returns:
            True si les coordonnées sont dans l'image
        """
        return 0 <= x < self._height and 0 <= y < self._width

    def fill(self, value: int):
        """
        Remplit l'image avec une valeur (implémentation manuelle).

        Args:
            value: Valeur à affecter à tous les labels
        """
        for x in range(self._height):
            for y in range(self._width):
                self._labels[x][y] = value

    def count_labels(self) -> int:
        """
        Compte le nombre de labels distincts (hors 0) - implémentation manuelle.

        Returns:
            Nombre de composantes connexes
        """
        # Utiliser un set pour trouver les labels uniques
        seen = set()
        for x in range(self._height):
            for y in range(self._width):
                label = self._labels[x][y]
                if label > 0:
                    seen.add(label)
        return len(seen)

    def to_visualization(self) -> Image:
        """
        Normalise les labels pour la visualisation (implémentation manuelle).

        Remappe les labels sur [0, 255] pour pouvoir sauvegarder
        l'image labellisée au format PGM.

        Returns:
            Image 8-bit avec labels normalisés
        """
        result = Image(self._width, self._height)

        # Trouver le label maximum (implémentation manuelle)
        max_label = 0
        for x in range(self._height):
            for y in range(self._width):
                if self._labels[x][y] > max_label:
                    max_label = self._labels[x][y]

        if max_label == 0:
            # Pas de labels, retourner une image noire
            result.fill(0)
            return result

        # Normaliser les labels (implémentation manuelle)
        for x in range(self._height):
            for y in range(self._width):
                label = self._labels[x][y]
                if label == 0:
                    result.set_at(x, y, 0)
                else:
                    # Mapper le label sur [1, 255]
                    value = ((label * 254) // max_label) + 1
                    result.set_at(x, y, value)

        return result

    def to_color_visualization(self) -> 'ColorImage':
        """
        Génère une visualisation couleur avec LUT aléatoire (implémentation manuelle).

        Chaque composante connexe reçoit une couleur distincte et vive,
        permettant une meilleure visualisation que les niveaux de gris.

        Returns:
            ColorImage avec couleurs distinctes pour chaque label
        """
        result = ColorImage(self._width, self._height)

        # Trouver tous les labels uniques
        unique_labels = set()
        for x in range(self._height):
            for y in range(self._width):
                if self._labels[x][y] > 0:
                    unique_labels.add(self._labels[x][y])

        if not unique_labels:
            return result

        # Générer une LUT de couleurs pseudo-aléatoires (mais déterministes)
        # Utilise une fonction de hachage simple pour des couleurs distinctes
        color_lut = {}
        for label in unique_labels:
            # Génération pseudo-aléatoire basée sur le label
            # Utilise des nombres premiers pour une bonne distribution
            r = ((label * 67) % 200) + 55    # 55-254 (évite le noir)
            g = ((label * 97) % 200) + 55
            b = ((label * 131) % 200) + 55

            # Assurer une couleur vive en forçant au moins une composante
            max_val = max(r, g, b)
            if max_val < 150:
                if r == max_val:
                    r = 200
                elif g == max_val:
                    g = 200
                else:
                    b = 200

            color_lut[label] = (r, g, b)

        # Appliquer les couleurs
        for x in range(self._height):
            for y in range(self._width):
                label = self._labels[x][y]
                if label == 0:
                    result.set_at(x, y, (0, 0, 0))  # Fond noir
                else:
                    result.set_at(x, y, color_lut[label])

        return result


class ColorImage:
    """
    Classe pour une image couleur RGB.

    Utilisée pour la visualisation des labels avec des couleurs distinctes.
    """

    def __init__(self, width: int = 0, height: int = 0):
        self._width = width
        self._height = height
        if width > 0 and height > 0:
            self._data = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
        else:
            self._data = []

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def data(self):
        return self._data

    def at(self, x: int, y: int) -> tuple:
        """Retourne le tuple (R, G, B) du pixel."""
        return self._data[x][y]

    def set_at(self, x: int, y: int, rgb: tuple):
        """Définit le tuple (R, G, B) du pixel."""
        self._data[x][y] = rgb

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self._height and 0 <= y < self._width
