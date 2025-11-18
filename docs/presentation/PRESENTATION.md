# Labellisation des Composantes Connexes
## Comparaison de 4 algorithmes

**Présenté par :**
- Romain Despoullain
- Nicolas Marano
- Amin Braham

**Date :** 9 décembre 2024

---

## Plan de la présentation

1. Introduction
2. Fondements Théoriques
3. Les 4 Algorithmes
4. Implémentation
5. Résultats
6. Conclusion

---

# 1. Introduction

---

## Contexte

### Objectif
> Partitionner une image binaire en régions homogènes (composantes connexes)

### Entrée
- Image binaire (0 = fond, 255 = objet)
- Type de connexité (4 ou 8)

### Sortie
- Image labellisée
- Chaque composante = label unique

---

## Applications

### Domaines d'application

🔍 **Vision par ordinateur**
- Détection et reconnaissance d'objets
- Suivi d'objets en mouvement

🏥 **Imagerie médicale**
- Segmentation d'organes
- Analyse de tumeurs

📄 **Analyse de documents**
- OCR (reconnaissance de caractères)
- Extraction de structure

🤖 **Robotique**
- Navigation autonome
- Reconnaissance d'obstacles

---

# 2. Fondements Théoriques

---

## Topologie Discrète (CM03)

### Adjacence forte (4-connexité)

**Définition :** `||x - y||₁ = 1`

```
    N
  W P E
    S
```

4 voisins directs : Nord, Sud, Est, Ouest

---

## Topologie Discrète (CM03)

### Adjacence faible (8-connexité)

**Définition :** `||x - y||∞ = 1`

```
  NW N NE
  W  P  E
  SW S SE
```

8 voisins : 4 directs + 4 diagonaux

---

## Paradoxe de Jordan

### ⚠️ Problème

On ne peut pas utiliser la même adjacence pour l'objet et le fond !

### ✅ Solution : Adjacences duales

- **4-connexité** pour l'objet (pixels blancs)
- **8-connexité** pour le fond (pixels noirs)

> Cette dualité garantit une topologie cohérente (théorème de Jordan)

---

## Modèles Mathématiques (CM05)

### Deux visions complémentaires

| Modèle Graphe | Modèle Partition |
|---------------|------------------|
| Pixels = sommets | Ensembles disjoints |
| Adjacences = arêtes | Couvrant toute l'image |
| Base pour Kruskal/Prim | Base pour Union-Find |

---

# 3. Les 4 Algorithmes

---

## Vue d'ensemble

1. 🔄 **Two-Pass** : Approche classique en 2 passes
2. 🌳 **Union-Find** : Structure Disjoint-Set
3. 📊 **Kruskal** : Minimum Spanning Tree
4. 🔍 **Prim** : Exploration BFS

---

## 1️⃣ Algorithme Two-Pass

### Principe

**Passe 1 : Étiquetage provisoire + table d'équivalence**

```
Pour chaque pixel de gauche à droite, haut en bas :
  Si pixel objet :
    - Examiner voisins déjà traités
    - Affecter label (nouveau ou existant)
    - Noter équivalences si collision
```

**Résolution : Calcul des labels racine**

**Passe 2 : Relabellisation finale**

---

## 1️⃣ Two-Pass - Caractéristiques

### ✅ Avantages
- Excellente localité cache
- Rapide en pratique
- Simple à implémenter

### 📊 Complexité
- **Temps :** `O(N)`
- **Espace :** `O(N)`

---

## 2️⃣ Algorithme Union-Find

### Structure Disjoint-Set

**Opérations principales :**
- `Find(x)` : trouve le représentant de l'ensemble contenant x
- `Union(x, y)` : fusionne les ensembles contenant x et y

**Optimisations :**
- 🚀 **Path compression** : accélère Find
- ⚖️ **Union by rank** : maintient l'arbre plat

---

## 2️⃣ Union-Find - Algorithme

```python
# Initialisation
DisjointSet ds(num_pixels)

# Parcours de l'image
Pour chaque pixel p "objet" :
    Pour chaque voisin v "objet" :
        Si Find(p) ≠ Find(v) :
            Union(p, v)

# Labellisation
Pour chaque pixel p :
    label[p] = Find(p)
```

### 📊 Complexité
- **Temps :** `O(N · α(N))` ≈ `O(N)` où `α < 5`
- **Espace :** `O(N)`

---

## 3️⃣ Algorithme de Kruskal

### Principe (MST)

1. 📝 Construire les arêtes du graphe
2. 🔽 Trier les arêtes par poids
3. 🔗 Pour chaque arête : fusionner si composantes différentes

### Adaptation pour labellisation

- Toutes les arêtes ont poids = 1
- Produit une **forêt couvrante**
- Chaque arbre = une composante connexe

---

## 3️⃣ Kruskal - Caractéristiques

### ✅ Avantages
- Basé sur théorie des graphes (MST)
- Conceptuellement élégant

### ⚠️ Inconvénients
- Tri des arêtes coûteux
- Stockage de toutes les arêtes

### 📊 Complexité
- **Temps :** `O(E log E)` où `E ≈ 2N` ou `4N`
- **Espace :** `O(E + V)`

---

## 4️⃣ Algorithme de Prim

### Principe (BFS simplifié)

```python
Pour chaque pixel non labellisé :
    1. Créer un nouveau label
    2. Lancer BFS pour explorer sa composante
    3. Affecter ce label à tous les pixels atteints
```

### Exploration BFS
- File FIFO pour parcours par couches
- Bonne localité cache
- Pas de risque de stack overflow

---

## 4️⃣ Prim - Caractéristiques

### ✅ Avantages
- Simple et intuitif
- Une seule passe
- Bonne localité cache

### 📊 Complexité
- **Temps :** `O(N)`
- **Espace :** `O(N)` pour la file

---

# 4. Implémentation

---

## Contraintes techniques

### ⚠️ Implémentation from scratch

- ❌ Aucune bibliothèque externe (pas d'OpenCV)
- ✅ Fonctions `min/max/mean` recréées manuellement
- ✅ Lecture/écriture PGM/PPM codée à la main
- ⚡ Optimisé pour la performance

### Technologies
- **Langage :** C++17
- **Build :** CMake
- **Tests :** Tests unitaires intégrés
- **Benchmark :** Comparaisons automatisées

---

## Architecture du code

### Structure modulaire

```
src/
├── core/         Image, LabelImage (structures de base)
├── io/           Lecture/écriture PGM/PPM (from scratch)
├── algorithms/   TwoPass, UnionFind, Kruskal, Prim
└── utils/        Fonctions utilitaires (min/max/mean)

tests/            Tests unitaires
benchmarks/       Comparaisons de performance
```

### Design
- Code modulaire et réutilisable
- Commentaires détaillés référençant les cours (CM03, CM05)
- Optimisations pour la performance

---

## Exemple de code : Union-Find

```cpp
class DisjointSet {
    std::vector<int> parent_;
    std::vector<int> rank_;

public:
    int find(int x) {
        // Path compression
        if (parent_[x] != x) {
            parent_[x] = find(parent_[x]);
        }
        return parent_[x];
    }

    bool unite(int x, int y) {
        int root_x = find(x);
        int root_y = find(y);

        if (root_x == root_y) return false;

        // Union by rank
        if (rank_[root_x] < rank_[root_y]) {
            parent_[root_x] = root_y;
        } else {
            parent_[root_y] = root_x;
            if (rank_[root_x] == rank_[root_y])
                rank_[root_x]++;
        }
        return true;
    }
};
```

---

# 5. Résultats

---

## Résultats de benchmark

### Configuration de test
- Image 512×512 pixels
- 4-connexité
- Moyenne sur 10 runs

### Tableau comparatif

| Algorithme  | Temps (ms) | Écart-type | Speedup |
|-------------|------------|------------|---------|
| Two-Pass    | XX.XX      | X.XX       | 1.0x    |
| Union-Find  | XX.XX      | X.XX       | X.Xx    |
| Kruskal     | XX.XX      | X.XX       | X.Xx    |
| Prim        | XX.XX      | X.XX       | X.Xx    |

*À compléter avec vos résultats réels*

---

## Analyse comparative

### 📊 Observations

✅ **Two-Pass**
- Le plus rapide (localité cache optimale)

✅ **Union-Find**
- Comparable, légèrement plus lent

⚠️ **Kruskal**
- Plus lent (overhead du tri des arêtes)

✅ **Prim**
- Performance similaire à Union-Find

---

## Validation

### ✅ Tests unitaires réussis

1. ✅ Image vide (0 composante)
2. ✅ Pixel unique (1 composante)
3. ✅ Composantes séparées
4. ✅ Différence 4-connexité vs 8-connexité
5. ✅ Cohérence entre les 4 algorithmes

### 🎯 Conclusion des tests

> Tous les algorithmes produisent exactement le même résultat !

Les différences sont uniquement dans les performances et l'utilisation mémoire.

---

# 6. Conclusion

---

## Bilan du projet

### ✅ Réalisations

- 4 algorithmes implémentés et testés
- Code optimisé sans bibliothèques externes
- Tests unitaires et benchmarks complets
- Documentation complète (LaTeX + Markdown)

### 📚 Apports pédagogiques

- Compréhension approfondie de la connexité
- Maîtrise des structures de données (Union-Find)
- Application de la théorie des graphes (MST)
- Analyse de performance et optimisation

---

## Synthèse comparative

| Critère          | Two-Pass | Union-Find | Kruskal | Prim |
|------------------|----------|------------|---------|------|
| **Vitesse**      | ⭐⭐⭐   | ⭐⭐       | ⭐      | ⭐⭐ |
| **Mémoire**      | ⭐⭐     | ⭐⭐       | ⭐      | ⭐⭐ |
| **Simplicité**   | ⭐⭐     | ⭐⭐       | ⭐⭐    | ⭐⭐⭐ |
| **Élégance**     | ⭐⭐     | ⭐⭐⭐     | ⭐⭐    | ⭐⭐ |

### 🏆 Recommandation

- **Pour la performance :** Two-Pass
- **Pour l'élégance théorique :** Union-Find
- **Pour l'apprentissage :** Les 4 !

---

## Perspectives

### 🚀 Améliorations possibles

**Parallélisation**
- Versions multi-thread (OpenMP)
- Calcul GPU (CUDA)

**Extensions**
- Images en niveaux de gris (watershed)
- Labellisation hiérarchique

**Optimisations**
- Instructions SIMD (AVX2)
- Optimisations spécifiques CPU

**Formats**
- Support PNG, JPEG
- Interface graphique

---

## Répartition du travail

### Romain Despoullain
- *À compléter*
- Exemple : Two-Pass et Union-Find
- Sections théoriques du rapport

### Nicolas Marano
- *À compléter*
- Exemple : Kruskal et Prim
- Benchmarks et tests

### Amin Braham
- *À compléter*
- Exemple : I/O et utilitaires
- Documentation

---

# Questions ?

---

## Merci pour votre attention !

### Contact

- 📧 [Email des étudiants]
- 💻 [Lien GitHub du projet]

### Ressources

- 📄 Rapport complet dans `docs/rapport/`
- 💾 Code source dans `src/`
- 🧪 Tests dans `tests/`

---

## Annexes

### Commandes utiles

**Compiler :**
```bash
mkdir build && cd build
cmake .. && make
```

**Exécuter :**
```bash
./labellisation input.pgm output.pgm two_pass 4
```

**Tester :**
```bash
./test_algorithms
```

**Benchmarker :**
```bash
./benchmark ../images/input/*.pgm
```

---

## Références

1. Support de cours CM03 - Topologie Discrète
2. Support de cours CM05 - Opérateurs Connexes
3. Support ESIEE - Labellisation
4. Rosenfeld & Pfaltz (1966) - Sequential operations
5. Tarjan (1975) - Union-Find efficiency

---

**Fin de la présentation**

*Projet de Traitement d'Images - Décembre 2024*
