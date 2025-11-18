#ifndef UTILS_H
#define UTILS_H

#include <cstdint>
#include <vector>
#include <chrono>

/**
 * @brief Classe contenant des fonctions utilitaires
 *
 * IMPORTANT: Toutes les fonctions sont implémentées manuellement
 * sans utiliser std::min, std::max, std::accumulate, etc.
 *
 * Ces fonctions sont nécessaires pour :
 * - Statistiques sur les images
 * - Comparaison de performances (benchmarking)
 * - Manipulation de données
 */
class Utils {
public:
    // ========================================================================
    // Fonctions mathématiques de base (implémentations manuelles)
    // ========================================================================

    /**
     * @brief Retourne le minimum de deux valeurs
     * @param a Première valeur
     * @param b Deuxième valeur
     * @return La plus petite valeur
     */
    template<typename T>
    static T min(T a, T b) {
        return (a < b) ? a : b;
    }

    /**
     * @brief Retourne le maximum de deux valeurs
     * @param a Première valeur
     * @param b Deuxième valeur
     * @return La plus grande valeur
     */
    template<typename T>
    static T max(T a, T b) {
        return (a > b) ? a : b;
    }

    /**
     * @brief Retourne le minimum d'un tableau
     * @param data Tableau de données
     * @param size Taille du tableau
     * @return Valeur minimale
     */
    template<typename T>
    static T minArray(const T* data, int size) {
        if (size <= 0) {
            return T(0);
        }

        T min_val = data[0];
        for (int i = 1; i < size; ++i) {
            if (data[i] < min_val) {
                min_val = data[i];
            }
        }
        return min_val;
    }

    /**
     * @brief Retourne le maximum d'un tableau
     * @param data Tableau de données
     * @param size Taille du tableau
     * @return Valeur maximale
     */
    template<typename T>
    static T maxArray(const T* data, int size) {
        if (size <= 0) {
            return T(0);
        }

        T max_val = data[0];
        for (int i = 1; i < size; ++i) {
            if (data[i] > max_val) {
                max_val = data[i];
            }
        }
        return max_val;
    }

    /**
     * @brief Calcule la moyenne d'un tableau
     * @param data Tableau de données
     * @param size Taille du tableau
     * @return Valeur moyenne
     *
     * Implémentation manuelle sans std::accumulate
     */
    template<typename T>
    static double mean(const T* data, int size) {
        if (size <= 0) {
            return 0.0;
        }

        // Somme manuelle
        double sum = 0.0;
        for (int i = 0; i < size; ++i) {
            sum += static_cast<double>(data[i]);
        }

        return sum / static_cast<double>(size);
    }

    /**
     * @brief Calcule l'écart-type d'un tableau
     * @param data Tableau de données
     * @param size Taille du tableau
     * @return Écart-type
     */
    template<typename T>
    static double standardDeviation(const T* data, int size) {
        if (size <= 0) {
            return 0.0;
        }

        double avg = mean(data, size);

        // Calcul manuel de la variance
        double variance = 0.0;
        for (int i = 0; i < size; ++i) {
            double diff = static_cast<double>(data[i]) - avg;
            variance += diff * diff;
        }
        variance /= static_cast<double>(size);

        // Racine carrée manuelle (méthode de Newton-Raphson)
        return sqrtManual(variance);
    }

    /**
     * @brief Calcule la racine carrée (implémentation manuelle)
     * @param x Valeur
     * @return Racine carrée de x
     *
     * Utilise la méthode de Newton-Raphson pour éviter std::sqrt
     */
    static double sqrtManual(double x);

    // ========================================================================
    // Fonctions de tri (implémentation manuelle)
    // ========================================================================

    /**
     * @brief Trie un tableau (tri rapide - QuickSort)
     * @param data Tableau à trier
     * @param size Taille du tableau
     *
     * Implémentation manuelle pour éviter std::sort
     */
    template<typename T>
    static void quickSort(T* data, int size) {
        quickSortRecursive(data, 0, size - 1);
    }

    // ========================================================================
    // Mesure de temps pour benchmarking
    // ========================================================================

    /**
     * @brief Classe pour mesurer le temps d'exécution
     *
     * Utilisation :
     * Timer timer;
     * timer.start();
     * // ... code à mesurer ...
     * double elapsed = timer.stop();
     */
    class Timer {
    private:
        std::chrono::high_resolution_clock::time_point start_time_;
        std::chrono::high_resolution_clock::time_point end_time_;
        bool running_;

    public:
        Timer() : running_(false) {}

        /**
         * @brief Démarre le chronomètre
         */
        void start() {
            start_time_ = std::chrono::high_resolution_clock::now();
            running_ = true;
        }

        /**
         * @brief Arrête le chronomètre
         * @return Temps écoulé en millisecondes
         */
        double stop() {
            end_time_ = std::chrono::high_resolution_clock::now();
            running_ = false;
            return getElapsedMs();
        }

        /**
         * @brief Retourne le temps écoulé en millisecondes
         * @return Temps en ms
         */
        double getElapsedMs() const {
            auto end = running_ ?
                std::chrono::high_resolution_clock::now() : end_time_;
            auto duration = std::chrono::duration_cast<std::chrono::microseconds>(
                end - start_time_);
            return duration.count() / 1000.0;
        }
    };

    // ========================================================================
    // Gestion de la connectivité
    // ========================================================================

    /**
     * @brief Retourne les voisins d'un pixel selon la connectivité
     * @param x Coordonnée ligne du pixel
     * @param y Coordonnée colonne du pixel
     * @param width Largeur de l'image
     * @param height Hauteur de l'image
     * @param connectivity Type de connectivité (4 ou 8)
     * @return Vecteur de pixels voisins
     *
     * Connectivité 4 (adjacence forte, norme L1) :
     *       N
     *     W P E
     *       S
     *
     * Connectivité 8 (adjacence faible, norme L∞) :
     *     NW N NE
     *     W  P  E
     *     SW S SE
     */
    static std::vector<std::pair<int, int>> getNeighbors(
        int x, int y, int width, int height, int connectivity);

private:
    /**
     * @brief Fonction récursive pour le tri rapide
     */
    template<typename T>
    static void quickSortRecursive(T* data, int low, int high) {
        if (low < high) {
            int pivot_index = partition(data, low, high);
            quickSortRecursive(data, low, pivot_index - 1);
            quickSortRecursive(data, pivot_index + 1, high);
        }
    }

    /**
     * @brief Fonction de partition pour QuickSort
     */
    template<typename T>
    static int partition(T* data, int low, int high) {
        T pivot = data[high];
        int i = low - 1;

        for (int j = low; j < high; ++j) {
            if (data[j] < pivot) {
                ++i;
                // Échanger data[i] et data[j]
                T temp = data[i];
                data[i] = data[j];
                data[j] = temp;
            }
        }

        // Échanger data[i+1] et data[high]
        T temp = data[i + 1];
        data[i + 1] = data[high];
        data[high] = temp;

        return i + 1;
    }
};

#endif // UTILS_H
