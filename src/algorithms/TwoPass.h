#ifndef TWOPASS_H
#define TWOPASS_H

#include "core/Image.h"
#include <vector>

/**
 * @brief Algorithme de labellisation en deux passes
 *
 * Cet algorithme est l'approche classique pour la labellisation des
 * composantes connexes d'une image binaire.
 *
 * PRINCIPE (décrit dans la source ESIEE) :
 *
 * 1ère Passe - Étiquetage provisoire et table d'équivalence :
 *    - Parcours de l'image de gauche à droite, de haut en bas
 *    - Pour chaque pixel "objet" (blanc) :
 *        a) Si aucun voisin "objet" déjà traité : nouveau label
 *        b) Si un voisin "objet" : prendre son label
 *        c) Si plusieurs voisins avec labels différents :
 *           - Prendre le plus petit label
 *           - Noter l'équivalence dans la table
 *
 * Passe intermédiaire - Résolution des équivalences :
 *    - Calculer les "labels racine" pour chaque classe d'équivalence
 *    - Utilise une structure Union-Find simplifiée
 *
 * 2ème Passe - Relabellisation finale :
 *    - Parcours de l'image
 *    - Remplacer chaque label provisoire par son label racine
 *
 * COMPLEXITÉ :
 * - Temps: O(N) où N est le nombre de pixels (2 passes linéaires)
 * - Espace: O(N) pour l'image de labels + O(L) pour la table d'équivalence
 *           où L est le nombre de labels provisoires
 *
 * AVANTAGES (source ESIEE) :
 * - Simple à implémenter
 * - Très bon cache locality (parcours séquentiel)
 * - Efficace en pratique malgré 2 passes
 *
 * CONNECTIVITÉ (CM03) :
 * - Supporte 4-connexité et 8-connexité
 * - Pour éviter le paradoxe de Jordan, utiliser des adjacences duales
 */
class TwoPass {
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
     * @brief Structure pour gérer les équivalences entre labels
     *
     * Implémente une version simplifiée d'Union-Find :
     * - Chaque label pointe vers son "parent"
     * - La racine d'un label est trouvée par remontée
     * - Path compression pour optimiser les recherches
     */
    class EquivalenceTable {
    private:
        std::vector<int> parent_;  // parent_[i] = parent du label i

    public:
        EquivalenceTable() {
            // Label 0 réservé pour le fond
            parent_.push_back(0);
        }

        /**
         * @brief Crée un nouveau label
         * @return Nouveau label
         */
        int makeSet() {
            int label = parent_.size();
            parent_.push_back(label);  // Initialement, chaque label est sa propre racine
            return label;
        }

        /**
         * @brief Trouve la racine d'un label (avec path compression)
         * @param x Label
         * @return Label racine
         */
        int find(int x) {
            if (x <= 0 || x >= static_cast<int>(parent_.size())) {
                return 0;
            }

            // Path compression : faire pointer directement vers la racine
            if (parent_[x] != x) {
                parent_[x] = find(parent_[x]);
            }

            return parent_[x];
        }

        /**
         * @brief Fusionne deux labels (union)
         * @param x Premier label
         * @param y Deuxième label
         *
         * Fait pointer le plus grand label vers le plus petit
         * pour minimiser les labels finaux.
         */
        void unite(int x, int y) {
            int root_x = find(x);
            int root_y = find(y);

            if (root_x == root_y) {
                return;  // Déjà dans la même classe
            }

            // Union : toujours pointer le plus grand vers le plus petit
            if (root_x < root_y) {
                parent_[root_y] = root_x;
            } else {
                parent_[root_x] = root_y;
            }
        }

        /**
         * @brief Retourne le nombre de labels
         */
        int size() const {
            return parent_.size();
        }
    };

    /**
     * @brief Première passe : étiquetage provisoire
     * @param input Image binaire
     * @param labels Image de labels (sortie)
     * @param equiv Table d'équivalence (sortie)
     * @param connectivity Connectivité (4 ou 8)
     */
    static void firstPass(const Image& input, LabelImage& labels,
                         EquivalenceTable& equiv, int connectivity);

    /**
     * @brief Deuxième passe : relabellisation avec labels finaux
     * @param labels Image de labels (entrée/sortie)
     * @param equiv Table d'équivalence
     */
    static void secondPass(LabelImage& labels, EquivalenceTable& equiv);

    /**
     * @brief Retourne les voisins déjà traités (pour la première passe)
     * @param x Coordonnée ligne
     * @param y Coordonnée colonne
     * @param width Largeur
     * @param height Hauteur
     * @param connectivity Connectivité
     * @return Vecteur de voisins déjà parcourus
     *
     * Pour un parcours gauche->droite, haut->bas, les voisins déjà
     * traités sont ceux qui sont au-dessus et à gauche du pixel courant.
     */
    static std::vector<std::pair<int, int>> getPreviousNeighbors(
        int x, int y, int width, int height, int connectivity);
};

#endif // TWOPASS_H
