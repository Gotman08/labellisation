#ifndef KRUSKAL_H
#define KRUSKAL_H

#include "core/Image.h"
#include <vector>

/**
 * @brief Algorithme de Kruskal pour la labellisation
 *
 * Cette approche utilise le modèle de graphe (CM05) pour la labellisation.
 *
 * MODÈLE DE GRAPHE (CM05) :
 *
 * L'image est vue comme un graphe G = (V, E) où :
 * - V = ensemble des pixels "objet" (sommets)
 * - E = ensemble des arêtes entre pixels adjacents (selon la connectivité)
 *
 * ALGORITHME DE KRUSKAL :
 *
 * Kruskal est un algorithme classique pour trouver un Arbre Couvrant de
 * Poids Minimum (MST - Minimum Spanning Tree).
 *
 * 1. Trier toutes les arêtes par poids croissant
 * 2. Pour chaque arête (u, v) dans l'ordre :
 *    - Si u et v sont dans des composantes différentes :
 *        - Ajouter l'arête au MST
 *        - Fusionner les composantes de u et v (Union-Find)
 *
 * APPLICATION À LA LABELLISATION :
 *
 * Pour la labellisation, on adapte Kruskal :
 * - Toutes les arêtes ont le même poids (poids = 1)
 * - On construit une FORÊT COUVRANTE (pas un seul arbre)
 * - Chaque arbre de la forêt = une composante connexe
 *
 * Propriété importante :
 * - Si le graphe a K composantes connexes, l'algorithme produit
 *   une forêt de K arbres
 * - Tous les pixels dans le même arbre reçoivent le même label
 *
 * PSEUDO-CODE :
 *
 * 1. Construire la liste des arêtes entre pixels adjacents
 * 2. Initialiser Union-Find avec chaque pixel comme singleton
 * 3. Pour chaque arête (u, v) :
 *    - Si Find(u) ≠ Find(v) :
 *        - Union(u, v)
 * 4. Labelliser : pixels avec même Find reçoivent même label
 *
 * COMPLEXITÉ :
 * - Temps: O(E log E) pour le tri des arêtes
 *   où E = nombre d'arêtes ≈ 2N pour connectivité 4, ≈ 4N pour connectivité 8
 * - Espace: O(E + V) pour stocker le graphe
 *
 * COMPARAISON avec Union-Find direct :
 * - Plus lent en théorie (tri des arêtes)
 * - Mais produit exactement le même résultat !
 * - Intéressant conceptuellement car basé sur la théorie des graphes (MST)
 *
 * Note : Comme toutes les arêtes ont le même poids, le tri ne change pas
 * le résultat final. On pourrait éviter le tri, mais on le garde pour
 * rester fidèle à l'algorithme de Kruskal classique.
 */
class Kruskal {
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
     * @brief Structure représentant une arête du graphe
     */
    struct Edge {
        int u;      // Premier sommet (index linéaire du pixel)
        int v;      // Deuxième sommet (index linéaire du pixel)
        int weight; // Poids de l'arête (toujours 1 pour la labellisation)

        Edge(int u_, int v_, int weight_ = 1)
            : u(u_), v(v_), weight(weight_) {}

        /**
         * @brief Opérateur de comparaison pour le tri
         */
        bool operator<(const Edge& other) const {
            return weight < other.weight;
        }
    };

    /**
     * @brief Structure Union-Find pour Kruskal
     *
     * Identique à celle utilisée dans UnionFind.cpp
     * (on pourrait la factoriser dans utils, mais on la garde ici
     * pour que chaque algorithme soit autonome)
     */
    class DisjointSet {
    private:
        std::vector<int> parent_;
        std::vector<int> rank_;

    public:
        DisjointSet(int size) {
            parent_.resize(size);
            rank_.resize(size, 0);
            for (int i = 0; i < size; ++i) {
                parent_[i] = i;
            }
        }

        int find(int x) {
            if (parent_[x] != x) {
                parent_[x] = find(parent_[x]);
            }
            return parent_[x];
        }

        bool unite(int x, int y) {
            int root_x = find(x);
            int root_y = find(y);

            if (root_x == root_y) {
                return false;
            }

            if (rank_[root_x] < rank_[root_y]) {
                parent_[root_x] = root_y;
            } else if (rank_[root_x] > rank_[root_y]) {
                parent_[root_y] = root_x;
            } else {
                parent_[root_y] = root_x;
                rank_[root_x]++;
            }

            return true;
        }
    };

    /**
     * @brief Convertit les coordonnées 2D en index 1D
     */
    static inline int getIndex(int x, int y, int width) {
        return x * width + y;
    }

    /**
     * @brief Construit la liste des arêtes du graphe
     * @param input Image binaire
     * @param connectivity Connectivité (4 ou 8)
     * @return Liste des arêtes
     */
    static std::vector<Edge> buildEdges(const Image& input, int connectivity);
};

#endif // KRUSKAL_H
