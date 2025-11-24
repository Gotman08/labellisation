# Package principal pour la labellisation de composantes connexes
"""
Projet de labellisation de composantes connexes pour images binaires.

Ce package implémente 4 algorithmes différents :
- Two-Pass : Algorithme classique en deux passes
- Union-Find : Structure Disjoint-Set avec compression de chemin
- Kruskal : Approche arbre couvrant minimum
- Prim : Parcours BFS/DFS

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

from .core.image import Image, LabelImage, Pixel
from .readers.image_io import ImageIO
from .algorithms.two_pass import TwoPass
from .algorithms.union_find import UnionFind
from .algorithms.kruskal import Kruskal
from .algorithms.prim import Prim

__version__ = "1.0.0"
__all__ = [
    "Image",
    "LabelImage",
    "Pixel",
    "ImageIO",
    "TwoPass",
    "UnionFind",
    "Kruskal",
    "Prim",
]
