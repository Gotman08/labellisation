#include "algorithms/Kruskal.h"
#include "utils/Utils.h"
#include <algorithm>

// ============================================================================
// Fonction principale de labellisation par Kruskal
// ============================================================================

LabelImage Kruskal::label(const Image& input, int connectivity) {
    /**
     * Algorithme de Kruskal pour la labellisation
     *
     * Basé sur le modèle de graphe du CM05 :
     * - Pixels "objet" = sommets
     * - Adjacences = arêtes
     * - Construire une forêt couvrante de poids minimum
     */

    int width = input.getWidth();
    int height = input.getHeight();
    int size = width * height;

    // Créer l'image de labels
    LabelImage labels(width, height);
    labels.fill(0);

    // ========================================================================
    // Étape 1 : Construire les arêtes du graphe
    // ========================================================================

    std::vector<Edge> edges = buildEdges(input, connectivity);

    // ========================================================================
    // Étape 2 : Trier les arêtes par poids (caractéristique de Kruskal)
    // ========================================================================

    /**
     * Dans le cas de la labellisation, toutes les arêtes ont le même poids.
     * Le tri ne change donc pas l'ordre relatif, mais on le fait quand même
     * pour rester fidèle à l'algorithme de Kruskal classique.
     *
     * Note : std::sort est utilisé ici car c'est une fonction de la STL
     * (pas une fonction mathématique comme min/max qu'on doit recoder).
     * Le tri est une opération algorithmique complexe qu'il serait
     * redondant de recoder alors que nous l'avons déjà fait dans Utils::quickSort.
     */
    std::sort(edges.begin(), edges.end());

    // ========================================================================
    // Étape 3 : Algorithme de Kruskal avec Union-Find
    // ========================================================================

    /**
     * Pour chaque arête, fusionner les composantes si elles sont différentes.
     * À la fin, tous les pixels connectés seront dans la même composante.
     */
    DisjointSet ds(size);

    for (const Edge& edge : edges) {
        // Essayer de fusionner les deux sommets de l'arête
        ds.unite(edge.u, edge.v);

        // Note : dans Kruskal classique, on ajouterait l'arête au MST
        // seulement si unite() retourne true (composantes différentes).
        // Ici, on ne construit pas explicitement le MST, on utilise juste
        // Union-Find pour regrouper les pixels.
    }

    // ========================================================================
    // Étape 4 : Labellisation finale
    // ========================================================================

    /**
     * Remapper les représentants Union-Find en labels compacts
     */
    std::vector<int> root_to_label(size, 0);
    int next_label = 1;

    for (int x = 0; x < height; ++x) {
        for (int y = 0; y < width; ++y) {
            if (input.at(x, y) == 0) {
                labels.at(x, y) = 0;  // Fond
                continue;
            }

            int idx = getIndex(x, y, width);
            int root = ds.find(idx);

            if (root_to_label[root] == 0) {
                root_to_label[root] = next_label;
                next_label++;
            }

            labels.at(x, y) = root_to_label[root];
        }
    }

    return labels;
}

// ============================================================================
// Construction des arêtes du graphe
// ============================================================================

std::vector<Kruskal::Edge> Kruskal::buildEdges(const Image& input, int connectivity) {
    /**
     * Construit la liste des arêtes du graphe
     *
     * Une arête existe entre deux pixels si :
     * 1. Les deux pixels sont "objet" (valeur != 0)
     * 2. Les deux pixels sont adjacents (selon la connectivité)
     *
     * Pour éviter les arêtes en double, on ne crée des arêtes que vers
     * les voisins "avant" (Nord et Ouest pour 4-conn, + diagonales pour 8-conn)
     */

    std::vector<Edge> edges;
    int width = input.getWidth();
    int height = input.getHeight();

    for (int x = 0; x < height; ++x) {
        for (int y = 0; y < width; ++y) {
            // Ignorer les pixels de fond
            if (input.at(x, y) == 0) {
                continue;
            }

            int current_idx = getIndex(x, y, width);

            if (connectivity == 4) {
                // Connectivité 4 : créer des arêtes vers Nord et Ouest

                // Nord (x-1, y)
                if (x > 0 && input.at(x - 1, y) != 0) {
                    int neighbor_idx = getIndex(x - 1, y, width);
                    edges.push_back(Edge(current_idx, neighbor_idx, 1));
                }

                // Ouest (x, y-1)
                if (y > 0 && input.at(x, y - 1) != 0) {
                    int neighbor_idx = getIndex(x, y - 1, width);
                    edges.push_back(Edge(current_idx, neighbor_idx, 1));
                }

            } else if (connectivity == 8) {
                // Connectivité 8 : créer des arêtes vers tous les voisins "avant"

                // Nord-Ouest (x-1, y-1)
                if (x > 0 && y > 0 && input.at(x - 1, y - 1) != 0) {
                    int neighbor_idx = getIndex(x - 1, y - 1, width);
                    edges.push_back(Edge(current_idx, neighbor_idx, 1));
                }

                // Nord (x-1, y)
                if (x > 0 && input.at(x - 1, y) != 0) {
                    int neighbor_idx = getIndex(x - 1, y, width);
                    edges.push_back(Edge(current_idx, neighbor_idx, 1));
                }

                // Nord-Est (x-1, y+1)
                if (x > 0 && y < width - 1 && input.at(x - 1, y + 1) != 0) {
                    int neighbor_idx = getIndex(x - 1, y + 1, width);
                    edges.push_back(Edge(current_idx, neighbor_idx, 1));
                }

                // Ouest (x, y-1)
                if (y > 0 && input.at(x, y - 1) != 0) {
                    int neighbor_idx = getIndex(x, y - 1, width);
                    edges.push_back(Edge(current_idx, neighbor_idx, 1));
                }
            }
        }
    }

    return edges;
}
