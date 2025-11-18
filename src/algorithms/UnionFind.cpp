#include "algorithms/UnionFind.h"
#include "utils/Utils.h"

// ============================================================================
// Fonction principale de labellisation par Union-Find
// ============================================================================

LabelImage UnionFind::label(const Image& input, int connectivity) {
    /**
     * Algorithme de labellisation par Union-Find
     *
     * Cette implémentation suit le modèle de partition du CM05 :
     * - L'image est vue comme un ensemble de pixels
     * - On cherche à partitionner cet ensemble en composantes connexes
     * - Chaque partition est gérée par la structure Union-Find
     */

    int width = input.getWidth();
    int height = input.getHeight();
    int size = width * height;

    // Créer la structure Union-Find pour tous les pixels
    DisjointSet ds(size);

    // Créer l'image de labels
    LabelImage labels(width, height);
    labels.fill(0);

    // ========================================================================
    // Phase 1 : Union des pixels adjacents
    // ========================================================================

    /**
     * Parcours de l'image pour fusionner les pixels adjacents
     *
     * Pour chaque pixel "objet" :
     * - Examiner ses voisins (selon la connectivité)
     * - Si un voisin est aussi "objet", fusionner leurs ensembles
     *
     * Note: On ne parcourt que les voisins "avant" (Nord et Ouest)
     * pour éviter de traiter deux fois la même paire de pixels.
     */
    for (int x = 0; x < height; ++x) {
        for (int y = 0; y < width; ++y) {
            // Ignorer les pixels de fond
            if (input.at(x, y) == 0) {
                continue;
            }

            int current_idx = getIndex(x, y, width);

            // Examiner les voisins "précédents" pour éviter les doublons
            if (connectivity == 4) {
                // Connectivité 4 : vérifier Nord et Ouest

                // Nord (x-1, y)
                if (x > 0 && input.at(x - 1, y) != 0) {
                    int neighbor_idx = getIndex(x - 1, y, width);
                    ds.unite(current_idx, neighbor_idx);
                }

                // Ouest (x, y-1)
                if (y > 0 && input.at(x, y - 1) != 0) {
                    int neighbor_idx = getIndex(x, y - 1, width);
                    ds.unite(current_idx, neighbor_idx);
                }

            } else if (connectivity == 8) {
                // Connectivité 8 : vérifier Nord-Ouest, Nord, Nord-Est, Ouest

                // Nord-Ouest (x-1, y-1)
                if (x > 0 && y > 0 && input.at(x - 1, y - 1) != 0) {
                    int neighbor_idx = getIndex(x - 1, y - 1, width);
                    ds.unite(current_idx, neighbor_idx);
                }

                // Nord (x-1, y)
                if (x > 0 && input.at(x - 1, y) != 0) {
                    int neighbor_idx = getIndex(x - 1, y, width);
                    ds.unite(current_idx, neighbor_idx);
                }

                // Nord-Est (x-1, y+1)
                if (x > 0 && y < width - 1 && input.at(x - 1, y + 1) != 0) {
                    int neighbor_idx = getIndex(x - 1, y + 1, width);
                    ds.unite(current_idx, neighbor_idx);
                }

                // Ouest (x, y-1)
                if (y > 0 && input.at(x, y - 1) != 0) {
                    int neighbor_idx = getIndex(x, y - 1, width);
                    ds.unite(current_idx, neighbor_idx);
                }
            }
        }
    }

    // ========================================================================
    // Phase 2 : Labellisation finale
    // ========================================================================

    /**
     * Convertir les représentants Union-Find en labels compacts
     *
     * Les représentants Union-Find peuvent avoir des valeurs dispersées
     * (ex: 5, 42, 137...). On les remappe sur des labels compacts
     * (ex: 1, 2, 3...) pour une meilleure visualisation.
     */

    // Première sous-passe : trouver tous les représentants uniques
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

            // Si ce représentant n'a pas encore de label, lui en affecter un
            if (root_to_label[root] == 0) {
                root_to_label[root] = next_label;
                next_label++;
            }

            // Affecter le label au pixel
            labels.at(x, y) = root_to_label[root];
        }
    }

    return labels;
}
