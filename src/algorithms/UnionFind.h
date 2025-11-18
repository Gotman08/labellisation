#ifndef UNIONFIND_H
#define UNIONFIND_H

#include "core/Image.h"
#include <vector>

/**
 * @brief Algorithme de labellisation par Union-Find (Disjoint-Set)
 *
 * Cette approche utilise directement la structure de données Union-Find
 * pour gérer les composantes connexes.
 *
 * PRINCIPE (modèle de partition du CM05) :
 *
 * 1. Initialisation :
 *    - Chaque pixel "objet" est un ensemble singleton (sa propre composante)
 *    - Créer une structure Union-Find pour gérer ces ensembles
 *
 * 2. Parcours de l'image :
 *    - Pour chaque pixel "objet" p :
 *        - Pour chaque voisin "objet" v (selon la connectivité) :
 *            - Si Find(p) ≠ Find(v) : les pixels sont dans des composantes différentes
 *            - Alors Union(p, v) : fusionner les deux composantes
 *
 * 3. Labellisation finale :
 *    - Pour chaque pixel, son label est Find(pixel)
 *
 * STRUCTURE UNION-FIND (CM05: modèle de partition) :
 *
 * Cette structure maintient une partition de l'ensemble des pixels.
 * Chaque partition représente une composante connexe.
 *
 * Deux opérations principales :
 * - Find(x) : trouve le représentant de l'ensemble contenant x
 * - Union(x, y) : fusionne les ensembles contenant x et y
 *
 * OPTIMISATIONS :
 * - Path compression : lors de Find, faire pointer tous les nœuds
 *   parcourus directement vers la racine
 * - Union by rank : lors de Union, attacher l'arbre de rang inférieur
 *   sous l'arbre de rang supérieur
 *
 * Ces optimisations donnent une complexité quasi-constante en pratique :
 * - Complexité amortie : O(α(N)) par opération
 *   où α est l'inverse de la fonction d'Ackermann (< 5 en pratique)
 *
 * COMPLEXITÉ GLOBALE :
 * - Temps: O(N · α(N)) ≈ O(N) où N est le nombre de pixels
 * - Espace: O(N) pour la structure Union-Find
 *
 * AVANTAGES vs Two-Pass :
 * - Plus élégant conceptuellement (basé sur la théorie des partitions)
 * - Une seule passe principale (au lieu de 2)
 * - Structure de données réutilisable
 *
 * INCONVÉNIENTS vs Two-Pass :
 * - Peut être légèrement moins efficace en cache
 *   (accès non-séquentiels à la structure parent)
 * - Nécessite plus de mémoire (rank + parent)
 */
class UnionFind {
public:
    /**
     * @brief Labellise les composantes connexes d'une image binaire
     * @param input Image binaire (0 = fond, 255 = objet)
     * @param connectivity Type de connectivité (4 ou 8)
     * @return Image labellisée avec les composantes connexes
     */
    static LabelImage label(const Image& input, int connectivity = 4);

private:
    /**
     * @brief Structure Union-Find optimisée
     *
     * Implémente la structure de données Disjoint-Set avec :
     * - Path compression dans Find
     * - Union by rank
     */
    class DisjointSet {
    private:
        std::vector<int> parent_;  // parent_[i] = parent du nœud i
        std::vector<int> rank_;    // rank_[i] = rang approximatif de l'arbre enraciné en i

    public:
        /**
         * @brief Constructeur
         * @param size Nombre d'éléments
         */
        DisjointSet(int size) {
            parent_.resize(size);
            rank_.resize(size, 0);

            // Initialisation : chaque élément est sa propre racine
            for (int i = 0; i < size; ++i) {
                parent_[i] = i;
            }
        }

        /**
         * @brief Trouve le représentant de l'ensemble contenant x
         * @param x Élément
         * @return Représentant (racine) de l'ensemble
         *
         * Utilise la path compression : tous les nœuds parcourus
         * sont directement reliés à la racine pour accélérer les
         * futurs Find.
         */
        int find(int x) {
            if (parent_[x] != x) {
                // Path compression récursif
                parent_[x] = find(parent_[x]);
            }
            return parent_[x];
        }

        /**
         * @brief Fusionne les ensembles contenant x et y
         * @param x Premier élément
         * @param y Deuxième élément
         * @return true si fusion effectuée, false si déjà dans le même ensemble
         *
         * Utilise union by rank : l'arbre de rang inférieur est attaché
         * sous l'arbre de rang supérieur pour maintenir l'arbre plat.
         */
        bool unite(int x, int y) {
            int root_x = find(x);
            int root_y = find(y);

            if (root_x == root_y) {
                return false;  // Déjà dans le même ensemble
            }

            // Union by rank
            if (rank_[root_x] < rank_[root_y]) {
                parent_[root_x] = root_y;
            } else if (rank_[root_x] > rank_[root_y]) {
                parent_[root_y] = root_x;
            } else {
                // Rangs égaux : attacher root_y sous root_x et incrémenter le rang
                parent_[root_y] = root_x;
                rank_[root_x]++;
            }

            return true;
        }
    };

    /**
     * @brief Convertit les coordonnées 2D en index 1D
     * @param x Coordonnée ligne
     * @param y Coordonnée colonne
     * @param width Largeur de l'image
     * @return Index linéaire
     */
    static inline int getIndex(int x, int y, int width) {
        return x * width + y;
    }
};

#endif // UNIONFIND_H
