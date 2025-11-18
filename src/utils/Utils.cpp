#include "utils/Utils.h"
#include "core/Image.h"

// ============================================================================
// Implémentation de la racine carrée manuelle
// ============================================================================

double Utils::sqrtManual(double x) {
    /**
     * Calcule la racine carrée par la méthode de Newton-Raphson
     *
     * Formule itérative : x_{n+1} = (x_n + S/x_n) / 2
     * où S est le nombre dont on cherche la racine
     *
     * Cette méthode converge très rapidement (convergence quadratique).
     * Implémentation manuelle pour éviter std::sqrt.
     */

    if (x < 0.0) {
        return 0.0;  // Pas de racine carrée pour les négatifs
    }

    if (x == 0.0) {
        return 0.0;
    }

    // Estimation initiale
    double guess = x / 2.0;
    if (guess < 1.0) {
        guess = 1.0;
    }

    // Itérations de Newton-Raphson
    const int max_iterations = 50;
    const double epsilon = 1e-10;

    for (int i = 0; i < max_iterations; ++i) {
        double next_guess = (guess + x / guess) / 2.0;

        // Vérifier la convergence
        double diff = next_guess - guess;
        if (diff < 0.0) {
            diff = -diff;
        }

        if (diff < epsilon) {
            return next_guess;
        }

        guess = next_guess;
    }

    return guess;
}

// ============================================================================
// Gestion des voisins selon la connectivité
// ============================================================================

std::vector<std::pair<int, int>> Utils::getNeighbors(
    int x, int y, int width, int height, int connectivity) {
    /**
     * Retourne les voisins d'un pixel selon la connectivité choisie
     *
     * Connectivité 4 (CM03: adjacence forte, ||x-y||_1 = 1) :
     * - Nord: (x-1, y)
     * - Sud:  (x+1, y)
     * - Ouest: (x, y-1)
     * - Est:   (x, y+1)
     *
     * Connectivité 8 (CM03: adjacence faible, ||x-y||_∞ = 1) :
     * - Les 4 voisins ci-dessus +
     * - Nord-Ouest: (x-1, y-1)
     * - Nord-Est:   (x-1, y+1)
     * - Sud-Ouest:  (x+1, y-1)
     * - Sud-Est:    (x+1, y+1)
     *
     * IMPORTANT: Pour éviter le paradoxe de Jordan (CM03),
     * on utilise généralement des adjacences duales :
     * - 4-connexité pour l'objet
     * - 8-connexité pour le fond
     */

    std::vector<std::pair<int, int>> neighbors;

    if (connectivity == 4) {
        // Connectivité 4
        // Ordre: Nord, Sud, Ouest, Est
        const int dx[] = {-1, 1,  0, 0};
        const int dy[] = { 0, 0, -1, 1};

        for (int i = 0; i < 4; ++i) {
            int nx = x + dx[i];
            int ny = y + dy[i];

            // Vérifier que le voisin est dans l'image
            if (nx >= 0 && nx < height && ny >= 0 && ny < width) {
                neighbors.push_back({nx, ny});
            }
        }
    } else if (connectivity == 8) {
        // Connectivité 8
        // Ordre: N, S, O, E, NO, NE, SO, SE
        const int dx[] = {-1, 1,  0, 0, -1, -1,  1,  1};
        const int dy[] = { 0, 0, -1, 1, -1,  1, -1,  1};

        for (int i = 0; i < 8; ++i) {
            int nx = x + dx[i];
            int ny = y + dy[i];

            // Vérifier que le voisin est dans l'image
            if (nx >= 0 && nx < height && ny >= 0 && ny < width) {
                neighbors.push_back({nx, ny});
            }
        }
    }

    return neighbors;
}
