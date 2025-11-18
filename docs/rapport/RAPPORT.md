# Projet : Labellisation des Composantes Connexes

**Traitement d'Images**

**Auteurs :**
- Romain Despoullain
- Nicolas Marano
- Amin Braham

**Date :** Décembre 2024

---

## Table des matières

1. [Introduction](#introduction)
2. [Fondements Théoriques](#fondements-théoriques)
3. [Méthodologie et Implémentation](#méthodologie-et-implémentation)
4. [Résultats et Analyse](#résultats-et-analyse)
5. [Conclusion](#conclusion)
6. [Références](#références)

---

## Introduction

### Contexte

Le traitement d'images numériques est un domaine fondamental de l'informatique moderne, avec des applications variées allant de la vision par ordinateur à l'analyse médicale. Une image numérique (CM01) est définie comme une fonction discrète `f: Ω → V` où `Ω ⊂ ℤ²` représente le domaine spatial et `V` l'ensemble des valeurs possibles.

Ce projet s'inscrit dans le cadre des **opérateurs non-linéaires** (CM02, CM05) et plus particulièrement du **cadre topologique** (CM05). Il vise à implémenter et comparer différentes méthodes de labellisation des composantes connexes d'une image binaire.

### Objectif du projet

L'objectif principal est de **partitionner l'image en régions homogènes**, où l'homogénéité est définie par la connexité. Plus précisément, il s'agit de :

- Identifier toutes les composantes connexes d'une image binaire
- Affecter un label unique à chaque composante
- Comparer différentes approches algorithmiques
- Analyser leurs performances respectives

### Méthodes implémentées

Quatre algorithmes ont été implémentés et comparés :

1. **Algorithme en deux passes** : Approche classique avec table d'équivalence
2. **Union-Find** : Structure de données Disjoint-Set optimisée
3. **Kruskal** : Approche par graphe (Minimum Spanning Tree)
4. **Prim** : Approche par exploration (BFS/DFS)

---

## Fondements Théoriques

### Topologie Discrète (CM03)

#### Adjacence

La notion de connexité repose sur la **topologie discrète** (CM03). Le point de départ est la notion d'**adjacence** entre pixels.

**Adjacence forte (4-connexité) :**

Deux pixels `x` et `y` sont adjacents si :

```
||x - y||₁ = 1
```

Cette définition correspond aux 4 voisins directs (Nord, Sud, Est, Ouest).

```
    N
  W P E
    S
```

**Adjacence faible (8-connexité) :**

Deux pixels `x` et `y` sont adjacents si :

```
||x - y||∞ = 1
```

Cette définition inclut également les voisins diagonaux.

```
  NW N NE
  W  P  E
  SW S SE
```

#### Paradoxe de Jordan et Dualité

Le **paradoxe de l'échiquier de Jordan** (CM03) démontre qu'on ne peut pas utiliser la même adjacence pour l'objet et le fond. Pour avoir une topologie cohérente (par exemple, pour qu'un "cercle" de pixels ait bien un intérieur et un extérieur), il faut utiliser des **adjacences duales** (CM03) :

- **4-connexité pour l'objet** (pixels blancs)
- **8-connexité pour le fond** (pixels noirs)

### Modèles Mathématiques (CM05)

Le cours CM05 fournit deux modèles formels pour la labellisation :

#### Modèle en Graphe

L'image est vue comme un **graphe** `G = (V, E)` où :

- `V` = ensemble des pixels (sommets)
- `E` = ensemble des liens d'adjacence (arêtes)

Ce modèle est la base des algorithmes de Kruskal et Prim.

#### Modèle en Partition

Le but de la labellisation est de trouver une **partition** `P` de l'image telle que :

```
∀ X, Y ∈ P, X ≠ Y ⇒ X ∩ Y = ∅
⋃ P = Ω
```

Ce modèle est la base de l'algorithme Union-Find.

---

## Méthodologie et Implémentation

### Contraintes d'implémentation

Le projet a été développé en **C++17** avec les contraintes suivantes :

- ✅ **Aucune bibliothèque externe** (pas d'OpenCV)
- ✅ Toutes les fonctions de base (`min`, `max`, `mean`) implémentées manuellement
- ✅ Lecture/écriture d'images au format PGM/PPM codée from scratch
- ✅ Code optimisé pour la performance

### Algorithme en Deux Passes

#### Principe

L'algorithme en deux passes est l'approche classique décrite dans la littérature.

**Première passe : Étiquetage provisoire**

```
label ← 1
Pour chaque pixel (x, y) de gauche à droite, haut en bas :
    Si pixel est objet :
        N ← voisins déjà traités qui sont objets
        Si N = ∅ :
            Affecter nouveau label et incrémenter
        Sinon :
            Affecter min(labels(N))
            Enregistrer équivalences entre labels
```

**Deuxième passe : Relabellisation finale**

Remplacer chaque label provisoire par son label racine (résolution des équivalences).

#### Complexité

- **Temps :** `O(N)` où `N` est le nombre de pixels
- **Espace :** `O(N + L)` où `L` est le nombre de labels provisoires

#### Avantages

- ✅ Excellente localité cache (parcours séquentiel)
- ✅ Simple à implémenter
- ✅ Très efficace en pratique

### Algorithme Union-Find

#### Principe

Utilise la structure de données Disjoint-Set avec les optimisations :

- **Path compression** : lors de `Find`, tous les nœuds parcourus pointent directement vers la racine
- **Union by rank** : lors de `Union`, l'arbre de rang inférieur est attaché sous l'arbre de rang supérieur

#### Algorithme

```cpp
// Initialisation : chaque pixel est un singleton
DisjointSet ds(width * height);

// Parcours de l'image
Pour chaque pixel p "objet" :
    Pour chaque voisin v "objet" :
        Si Find(p) ≠ Find(v) :
            Union(p, v)

// Labellisation finale
Pour chaque pixel p :
    label[p] = Find(p)
```

#### Complexité

- **Temps :** `O(N · α(N))` où `α` est l'inverse d'Ackermann (< 5 en pratique)
- **Espace :** `O(N)`

### Algorithme de Kruskal

#### Principe

Kruskal est un algorithme de Minimum Spanning Tree adapté à la labellisation :

1. Construire la liste des arêtes entre pixels adjacents
2. Trier les arêtes (toutes de poids 1)
3. Pour chaque arête `(u, v)` : si `u` et `v` dans composantes différentes, fusionner

Le résultat est une **forêt couvrante** où chaque arbre = une composante connexe.

#### Algorithme

```cpp
// 1. Construire les arêtes
edges ← BuildEdges(image, connectivity)

// 2. Trier les arêtes (par poids)
Sort(edges)

// 3. Kruskal avec Union-Find
DisjointSet ds(num_pixels)
Pour chaque arête (u, v) dans edges :
    ds.Unite(u, v)

// 4. Labellisation
Pour chaque pixel p :
    label[p] = ds.Find(p)
```

#### Complexité

- **Temps :** `O(E log E)` où `E ≈ 2N` (4-conn) ou `4N` (8-conn)
- **Espace :** `O(E + V)`

### Algorithme de Prim

#### Principe

Version simplifiée basée sur BFS (toutes les arêtes ont le même poids) :

1. Pour chaque pixel non labellisé
2. Lancer BFS pour explorer toute sa composante
3. Affecter le même label à tous les pixels atteints

#### Algorithme

```cpp
current_label ← 0

Pour chaque pixel (x, y) :
    Si pixel est "objet" ET non labellisé :
        current_label++
        BFS(x, y, current_label)

// BFS
Fonction BFS(start_x, start_y, label) :
    queue.push((start_x, start_y))
    labels[start_x, start_y] ← label

    Tant que queue non vide :
        (x, y) ← queue.pop()
        Pour chaque voisin (nx, ny) :
            Si voisin est "objet" ET non labellisé :
                labels[nx, ny] ← label
                queue.push((nx, ny))
```

#### Complexité

- **Temps :** `O(N)`
- **Espace :** `O(N)` pour la file BFS

---

## Résultats et Analyse

### Configuration des tests

Les tests ont été effectués sur :

- **Processeur :** [À compléter avec votre configuration]
- **RAM :** [À compléter]
- **Compilateur :** g++ avec flag `-O3`
- **Images :** Diverses tailles (128×128, 256×256, 512×512, 1024×1024)

### Résultats de benchmark

#### Tableau comparatif (Image 512×512, 4-connexité)

| Algorithme  | Moyenne (ms) | Écart-type | Min (ms) | Max (ms) | Speedup |
|-------------|--------------|------------|----------|----------|---------|
| Two-Pass    | XX.XX        | X.XX       | XX.XX    | XX.XX    | 1.0x    |
| Union-Find  | XX.XX        | X.XX       | XX.XX    | XX.XX    | X.Xx    |
| Kruskal     | XX.XX        | X.XX       | XX.XX    | XX.XX    | X.Xx    |
| Prim        | XX.XX        | X.XX       | XX.XX    | XX.XX    | X.Xx    |

*Note : Compléter avec vos résultats réels après exécution du benchmark*

### Analyse comparative

#### Efficacité pratique

D'après la littérature et nos observations :

- ✅ **Two-Pass** : Souvent le plus rapide grâce à la localité cache
- ✅ **Union-Find** : Comparable, légèrement moins bon en cache
- ⚠️ **Kruskal** : Plus lent à cause du tri des arêtes
- ✅ **Prim (BFS)** : Performance similaire à Union-Find

#### Avantages et inconvénients

| Algorithme  | Avantages                                      | Inconvénients                           |
|-------------|------------------------------------------------|-----------------------------------------|
| **Two-Pass** | • Excellente localité cache<br>• Simple<br>• Rapide en pratique | • Deux passes complètes<br>• Table d'équivalence |
| **Union-Find** | • Une seule passe principale<br>• Élégant (théorie des partitions)<br>• Structure réutilisable | • Accès mémoire non-séquentiels<br>• Plus de mémoire (rank + parent) |
| **Kruskal** | • Basé sur théorie des graphes<br>• Facile à comprendre | • Tri des arêtes coûteux<br>• Stockage de toutes les arêtes |
| **Prim (BFS)** | • Simple<br>• Bonne localité<br>• Une passe | • Utilise une file (overhead mémoire) |

### Validation

Tous les tests unitaires passent avec succès :

- ✅ Image vide (0 composante)
- ✅ Pixel unique (1 composante)
- ✅ Composantes séparées
- ✅ Différence 4-connexité vs 8-connexité
- ✅ Cohérence entre les 4 algorithmes

---

## Conclusion

Ce projet a permis d'implémenter et de comparer quatre approches différentes pour la labellisation des composantes connexes. Chaque algorithme présente des caractéristiques uniques :

- **Two-Pass** reste l'approche la plus efficace en pratique
- **Union-Find** offre une vision élégante basée sur les partitions
- **Kruskal et Prim** illustrent l'application de la théorie des graphes

L'implémentation complète from scratch (sans bibliothèques externes) a permis de comprendre en profondeur les mécanismes sous-jacents et d'apprécier les subtilités de chaque approche.

### Apports pédagogiques

- 📚 Compréhension approfondie de la topologie discrète (CM03)
- 🧩 Maîtrise des structures de données avancées (Union-Find)
- 🌐 Application concrète de la théorie des graphes (MST)
- ⚡ Analyse de performance et optimisation

### Perspectives

Des améliorations possibles incluent :

- **Parallélisation** : Versions multi-thread (OpenMP) ou GPU (CUDA)
- **Extension** : Labellisation d'images en niveaux de gris (watershed)
- **Optimisations** : Instructions SIMD (AVX2) pour Two-Pass
- **Formats** : Support de PNG, JPEG via bibliothèques légères

---

## Répartition du travail

### Romain Despoullain
*À compléter*
- Exemple : Implémentation Two-Pass et Union-Find
- Rédaction des sections théoriques du rapport

### Nicolas Marano
*À compléter*
- Exemple : Implémentation Kruskal et Prim
- Système de benchmark et tests

### Amin Braham
*À compléter*
- Exemple : Module I/O (lecture/écriture PGM)
- Documentation LaTeX et Markdown

---

## Références

1. **Support de cours CM03** - Topologie Discrète
2. **Support de cours CM05** - Opérateurs Connexes
3. **Support ESIEE** - Labellisation des Composantes Connexes
4. Rosenfeld, A., & Pfaltz, J. L. (1966). "Sequential operations in digital picture processing"
5. Tarjan, R. E. (1975). "Efficiency of a Good But Not Linear Set Union Algorithm"

---

**Projet réalisé dans le cadre du module de Traitement d'Images**

*Date de rendu : 1er décembre 2024*

*Présentation orale : 9 décembre 2024*
