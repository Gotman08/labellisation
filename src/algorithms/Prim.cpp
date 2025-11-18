#include "algorithms/Prim.h"
#include "utils/Utils.h"
#include <queue>

// ============================================================================
// Fonction principale de labellisation par Prim
// ============================================================================

LabelImage Prim::label(const Image& input, int connectivity) {
    /**
     * Algorithme de Prim pour la labellisation
     *
     * Stratégie : Pour chaque pixel non labellisé, lancer une exploration
     * BFS pour découvrir toute sa composante connexe.
     *
     * Cette approche est inspirée de Prim car elle "grandit" chaque
     * composante à partir d'un point de départ, en ajoutant progressivement
     * les pixels adjacents.
     */

    int width = input.getWidth();
    int height = input.getHeight();

    // Créer l'image de labels
    LabelImage labels(width, height);
    labels.fill(0);  // 0 = non labellisé (fond)

    int current_label = 0;

    // ========================================================================
    // Parcours de l'image pour trouver les composantes connexes
    // ========================================================================

    for (int x = 0; x < height; ++x) {
        for (int y = 0; y < width; ++y) {
            // Si le pixel est un pixel "objet" et n'est pas encore labellisé
            if (input.at(x, y) != 0 && labels.at(x, y) == 0) {
                // Nouvelle composante connexe trouvée
                current_label++;

                // Explorer toute la composante par BFS
                bfs(input, labels, x, y, current_label, connectivity);
            }
        }
    }

    return labels;
}

// ============================================================================
// Exploration par BFS (Breadth-First Search)
// ============================================================================

void Prim::bfs(const Image& input, LabelImage& labels,
              int start_x, int start_y, int label, int connectivity) {
    /**
     * Explore une composante connexe par parcours en largeur (BFS)
     *
     * BFS garantit :
     * - Tous les pixels de la composante sont visités
     * - Parcours par "couches" (bonne localité cache)
     * - Pas de risque de stack overflow (contrairement à DFS récursif)
     *
     * Structure de données : file (FIFO)
     */

    int width = input.getWidth();
    int height = input.getHeight();

    // File pour le BFS : contient les coordonnées (x, y) des pixels à visiter
    std::queue<std::pair<int, int>> queue;

    // Initialisation : ajouter le pixel de départ
    queue.push({start_x, start_y});
    labels.at(start_x, start_y) = label;

    // Parcours BFS
    while (!queue.empty()) {
        // Récupérer le prochain pixel
        std::pair<int, int> current = queue.front();
        queue.pop();

        int x = current.first;
        int y = current.second;

        // Examiner tous les voisins selon la connectivité
        auto neighbors = Utils::getNeighbors(x, y, width, height, connectivity);

        for (const auto& neighbor : neighbors) {
            int nx = neighbor.first;
            int ny = neighbor.second;

            // Vérifier si le voisin est un pixel "objet" non labellisé
            if (input.at(nx, ny) != 0 && labels.at(nx, ny) == 0) {
                // Labelliser le voisin
                labels.at(nx, ny) = label;

                // Ajouter le voisin à la file pour exploration ultérieure
                queue.push({nx, ny});
            }
        }
    }
}

// ============================================================================
// Exploration par DFS (Depth-First Search) - Version alternative
// ============================================================================

void Prim::dfs(const Image& input, LabelImage& labels,
              int x, int y, int label, int connectivity) {
    /**
     * Explore une composante connexe par parcours en profondeur (DFS)
     *
     * Version récursive, plus simple mais :
     * - Risque de stack overflow pour de grandes composantes
     * - Moins bonne localité cache que BFS
     *
     * Cette fonction est fournie comme alternative mais n'est pas
     * utilisée par défaut (on préfère BFS).
     */

    int width = input.getWidth();
    int height = input.getHeight();

    // Vérifications de base
    if (!labels.isValid(x, y)) {
        return;
    }

    if (input.at(x, y) == 0) {
        return;  // Pixel de fond
    }

    if (labels.at(x, y) != 0) {
        return;  // Déjà labellisé
    }

    // Labelliser le pixel courant
    labels.at(x, y) = label;

    // Récursion sur tous les voisins
    auto neighbors = Utils::getNeighbors(x, y, width, height, connectivity);

    for (const auto& neighbor : neighbors) {
        int nx = neighbor.first;
        int ny = neighbor.second;

        dfs(input, labels, nx, ny, label, connectivity);
    }
}
