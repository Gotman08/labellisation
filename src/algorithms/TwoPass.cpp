#include "algorithms/TwoPass.h"
#include "utils/Utils.h"

// ============================================================================
// Fonction principale de labellisation
// ============================================================================

LabelImage TwoPass::label(const Image& input, int connectivity) {
    /**
     * Algorithme de labellisation en deux passes
     *
     * Cet algorithme est optimisé pour la localité cache grâce à
     * ses parcours séquentiels de l'image (source ESIEE).
     */

    int width = input.getWidth();
    int height = input.getHeight();

    // Créer l'image de labels
    LabelImage labels(width, height);
    labels.fill(0);  // 0 = fond

    // Créer la table d'équivalence
    EquivalenceTable equiv;

    // Première passe : étiquetage provisoire
    firstPass(input, labels, equiv, connectivity);

    // Deuxième passe : relabellisation finale
    secondPass(labels, equiv);

    return labels;
}

// ============================================================================
// Première passe : étiquetage provisoire et détection d'équivalences
// ============================================================================

void TwoPass::firstPass(const Image& input, LabelImage& labels,
                       EquivalenceTable& equiv, int connectivity) {
    /**
     * Première passe de l'algorithme
     *
     * Parcours de l'image de gauche à droite, de haut en bas.
     * Pour chaque pixel "objet" :
     * 1. Examiner les voisins déjà traités (au-dessus et à gauche)
     * 2. Cas possibles :
     *    a) Aucun voisin objet -> créer un nouveau label
     *    b) Un seul label parmi les voisins -> utiliser ce label
     *    c) Plusieurs labels différents -> collision d'équivalence
     *       - Utiliser le plus petit label
     *       - Enregistrer l'équivalence dans la table
     */

    int width = input.getWidth();
    int height = input.getHeight();

    for (int x = 0; x < height; ++x) {
        for (int y = 0; y < width; ++y) {
            // Ignorer les pixels de fond (valeur 0)
            if (input.at(x, y) == 0) {
                labels.at(x, y) = 0;
                continue;
            }

            // Pixel objet : examiner les voisins déjà traités
            auto neighbors = getPreviousNeighbors(x, y, width, height, connectivity);

            // Collecter les labels des voisins objet
            std::vector<int> neighbor_labels;
            for (const auto& neighbor : neighbors) {
                int nx = neighbor.first;
                int ny = neighbor.second;

                // Vérifier que le voisin est aussi un pixel objet
                if (input.at(nx, ny) != 0) {
                    int neighbor_label = labels.at(nx, ny);
                    if (neighbor_label > 0) {
                        neighbor_labels.push_back(neighbor_label);
                    }
                }
            }

            if (neighbor_labels.empty()) {
                // Cas a) : Aucun voisin objet -> nouveau label
                int new_label = equiv.makeSet();
                labels.at(x, y) = new_label;
            } else {
                // Trouver le label minimum parmi les voisins
                // (implémentation manuelle de min)
                int min_label = neighbor_labels[0];
                for (size_t i = 1; i < neighbor_labels.size(); ++i) {
                    if (neighbor_labels[i] < min_label) {
                        min_label = neighbor_labels[i];
                    }
                }

                // Affecter le label minimum au pixel courant
                labels.at(x, y) = min_label;

                // Cas c) : Enregistrer les équivalences entre labels
                for (size_t i = 0; i < neighbor_labels.size(); ++i) {
                    if (neighbor_labels[i] != min_label) {
                        equiv.unite(min_label, neighbor_labels[i]);
                    }
                }
            }
        }
    }
}

// ============================================================================
// Deuxième passe : relabellisation avec les labels racine
// ============================================================================

void TwoPass::secondPass(LabelImage& labels, EquivalenceTable& equiv) {
    /**
     * Deuxième passe de l'algorithme
     *
     * Remplace chaque label provisoire par son label racine
     * (résolution des équivalences).
     *
     * Cette passe garantit que tous les pixels d'une même composante
     * connexe auront exactement le même label final.
     */

    int width = labels.getWidth();
    int height = labels.getHeight();

    for (int x = 0; x < height; ++x) {
        for (int y = 0; y < width; ++y) {
            int label = labels.at(x, y);
            if (label > 0) {
                // Trouver le label racine et l'affecter
                labels.at(x, y) = equiv.find(label);
            }
        }
    }
}

// ============================================================================
// Fonction utilitaire : voisins déjà traités
// ============================================================================

std::vector<std::pair<int, int>> TwoPass::getPreviousNeighbors(
    int x, int y, int width, int height, int connectivity) {
    /**
     * Retourne les voisins déjà traités dans un parcours gauche->droite, haut->bas
     *
     * Pour la connectivité 4 :
     *     [X]     <- Nord (x-1, y) : déjà traité
     *   [X][P]    <- Ouest (x, y-1) : déjà traité, Pixel courant (P)
     *
     * Pour la connectivité 8 :
     *   [X][X][X]  <- Nord-Ouest, Nord, Nord-Est : déjà traités
     *   [X][P]     <- Ouest : déjà traité, Pixel courant (P)
     *
     * Cette optimisation évite d'examiner les voisins pas encore traités,
     * ce qui améliore la localité cache.
     */

    std::vector<std::pair<int, int>> neighbors;

    if (connectivity == 4) {
        // Connectivité 4 : Nord et Ouest
        // Nord (x-1, y)
        if (x > 0) {
            neighbors.push_back({x - 1, y});
        }
        // Ouest (x, y-1)
        if (y > 0) {
            neighbors.push_back({x, y - 1});
        }
    } else if (connectivity == 8) {
        // Connectivité 8 : Nord-Ouest, Nord, Nord-Est, Ouest

        // Nord-Ouest (x-1, y-1)
        if (x > 0 && y > 0) {
            neighbors.push_back({x - 1, y - 1});
        }
        // Nord (x-1, y)
        if (x > 0) {
            neighbors.push_back({x - 1, y});
        }
        // Nord-Est (x-1, y+1)
        if (x > 0 && y < width - 1) {
            neighbors.push_back({x - 1, y + 1});
        }
        // Ouest (x, y-1)
        if (y > 0) {
            neighbors.push_back({x, y - 1});
        }
    }

    return neighbors;
}
