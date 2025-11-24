"""
Module utils/utils.py - Fonctions utilitaires

Contient des fonctions utilitaires pour :
- Statistiques sur les images
- Comparaison de performances (benchmarking)
- Manipulation de données
- Gestion de la connectivité

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import time
from typing import List, Tuple, Union
import math


def min_val(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Retourne le minimum de deux valeurs.

    Args:
        a: Première valeur
        b: Deuxième valeur

    Returns:
        La plus petite valeur
    """
    return a if a < b else b


def max_val(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Retourne le maximum de deux valeurs.

    Args:
        a: Première valeur
        b: Deuxième valeur

    Returns:
        La plus grande valeur
    """
    return a if a > b else b


def min_array(data: List) -> Union[int, float]:
    """
    Retourne le minimum d'une liste.

    Args:
        data: Liste de données

    Returns:
        Valeur minimale
    """
    if not data:
        return 0

    min_v = data[0]
    for i in range(1, len(data)):
        if data[i] < min_v:
            min_v = data[i]
    return min_v


def max_array(data: List) -> Union[int, float]:
    """
    Retourne le maximum d'une liste.

    Args:
        data: Liste de données

    Returns:
        Valeur maximale
    """
    if not data:
        return 0

    max_v = data[0]
    for i in range(1, len(data)):
        if data[i] > max_v:
            max_v = data[i]
    return max_v


def mean(data: List) -> float:
    """
    Calcule la moyenne d'une liste.

    Args:
        data: Liste de données

    Returns:
        Valeur moyenne
    """
    if not data:
        return 0.0

    total = 0.0
    for value in data:
        total += float(value)

    return total / len(data)


def standard_deviation(data: List) -> float:
    """
    Calcule l'écart-type d'une liste.

    Args:
        data: Liste de données

    Returns:
        Écart-type
    """
    if not data:
        return 0.0

    avg = mean(data)

    variance = 0.0
    for value in data:
        diff = float(value) - avg
        variance += diff * diff
    variance /= len(data)

    return sqrt_manual(variance)


def sqrt_manual(x: float) -> float:
    """
    Calcule la racine carrée (méthode de Newton-Raphson).

    Args:
        x: Valeur

    Returns:
        Racine carrée de x
    """
    if x < 0:
        raise ValueError("Impossible de calculer la racine carrée d'un nombre négatif")

    if x == 0:
        return 0.0

    guess = x / 2.0
    epsilon = 1e-10

    for _ in range(100):
        new_guess = (guess + x / guess) / 2.0
        if abs(new_guess - guess) < epsilon:
            break
        guess = new_guess

    return guess


def quick_sort(data: List) -> List:
    """
    Trie une liste (tri rapide - QuickSort).

    Args:
        data: Liste à trier

    Returns:
        Liste triée
    """
    if len(data) <= 1:
        return data.copy()

    result = data.copy()
    _quick_sort_recursive(result, 0, len(result) - 1)
    return result


def _quick_sort_recursive(data: List, low: int, high: int) -> None:
    """
    Fonction récursive pour le tri rapide.

    Args:
        data: Liste à trier
        low: Index de début
        high: Index de fin
    """
    if low < high:
        pivot_index = _partition(data, low, high)
        _quick_sort_recursive(data, low, pivot_index - 1)
        _quick_sort_recursive(data, pivot_index + 1, high)


def _partition(data: List, low: int, high: int) -> int:
    """
    Fonction de partition pour QuickSort.

    Args:
        data: Liste à partitionner
        low: Index de début
        high: Index de fin

    Returns:
        Index du pivot
    """
    pivot = data[high]
    i = low - 1

    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]

    data[i + 1], data[high] = data[high], data[i + 1]

    return i + 1


def get_neighbors(x: int, y: int, width: int, height: int, connectivity: int = 4) -> List[Tuple[int, int]]:
    """
    Retourne les voisins d'un pixel selon la connectivité.

    Args:
        x: Coordonnée ligne du pixel
        y: Coordonnée colonne du pixel
        width: Largeur de l'image
        height: Hauteur de l'image
        connectivity: Type de connectivité (4 ou 8)

    Returns:
        Liste de tuples (x, y) des pixels voisins

    Connectivité 4 (adjacence forte, norme L1) :
          N
        W P E
          S

    Connectivité 8 (adjacence faible, norme L infini) :
        NW N NE
        W  P  E
        SW S SE
    """
    neighbors = []

    if connectivity == 4:
        if x > 0:
            neighbors.append((x - 1, y))
        if x < height - 1:
            neighbors.append((x + 1, y))
        if y < width - 1:
            neighbors.append((x, y + 1))
        if y > 0:
            neighbors.append((x, y - 1))

    elif connectivity == 8:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < height and 0 <= ny < width:
                    neighbors.append((nx, ny))

    return neighbors


class Timer:
    """
    Classe pour mesurer le temps d'exécution.

    Utilisation :
        timer = Timer()
        timer.start()
        # ... code à mesurer ...
        elapsed = timer.stop()
    """

    def __init__(self):
        """Initialise le timer."""
        self._start_time = 0.0
        self._end_time = 0.0
        self._running = False

    def start(self) -> None:
        """Démarre le chronomètre."""
        self._start_time = time.perf_counter()
        self._running = True

    def stop(self) -> float:
        """
        Arrête le chronomètre.

        Returns:
            Temps écoulé en millisecondes
        """
        self._end_time = time.perf_counter()
        self._running = False
        return self.get_elapsed_ms()

    def get_elapsed_ms(self) -> float:
        """
        Retourne le temps écoulé en millisecondes.

        Returns:
            Temps en ms
        """
        end = time.perf_counter() if self._running else self._end_time
        return (end - self._start_time) * 1000.0

    def __enter__(self):
        """Support pour context manager."""
        self.start()
        return self

    def __exit__(self, *args):
        """Support pour context manager."""
        self.stop()
