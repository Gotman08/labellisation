/**
 * Programme principal de labellisation des composantes connexes
 *
 * Ce programme implémente 4 algorithmes différents :
 * 1. Two-Pass : Algorithme classique en deux passes
 * 2. Union-Find : Approche par structure de données Disjoint-Set
 * 3. Kruskal : Approche par graphe (Minimum Spanning Tree)
 * 4. Prim : Approche par graphe (exploration BFS)
 *
 * Usage :
 *   ./labellisation <input> <output> <algorithm> <connectivity>
 *
 * Arguments :
 *   input        : Chemin de l'image d'entrée (PGM ou PPM)
 *   output       : Chemin de l'image de sortie (PGM)
 *   algorithm    : two_pass | union_find | kruskal | prim
 *   connectivity : 4 | 8
 *
 * Exemple :
 *   ./labellisation input.pgm output.pgm two_pass 4
 */

#include <iostream>
#include <string>
#include <cstring>

#include "core/Image.h"
#include "io/ImageIO.h"
#include "algorithms/TwoPass.h"
#include "algorithms/UnionFind.h"
#include "algorithms/Kruskal.h"
#include "algorithms/Prim.h"
#include "utils/Utils.h"

// ============================================================================
// Fonctions utilitaires
// ============================================================================

void printUsage(const char* program_name) {
    std::cout << "\nUsage: " << program_name << " <input> <output> <algorithm> <connectivity>\n\n";
    std::cout << "Arguments:\n";
    std::cout << "  input        : Chemin de l'image d'entree (PGM ou PPM)\n";
    std::cout << "  output       : Chemin de l'image de sortie (PGM)\n";
    std::cout << "  algorithm    : two_pass | union_find | kruskal | prim\n";
    std::cout << "  connectivity : 4 | 8\n\n";
    std::cout << "Exemples:\n";
    std::cout << "  " << program_name << " input.pgm output.pgm two_pass 4\n";
    std::cout << "  " << program_name << " input.pgm output.pgm union_find 8\n";
    std::cout << "  " << program_name << " input.pgm output.pgm kruskal 4\n";
    std::cout << "  " << program_name << " input.pgm output.pgm prim 8\n\n";
}

bool isExtension(const std::string& filename, const std::string& ext) {
    if (filename.length() < ext.length()) {
        return false;
    }
    return filename.compare(filename.length() - ext.length(), ext.length(), ext) == 0;
}

// ============================================================================
// Fonction principale
// ============================================================================

int main(int argc, char* argv[]) {
    std::cout << "========================================\n";
    std::cout << "  Labellisation des Composantes Connexes\n";
    std::cout << "========================================\n\n";

    // Vérifier les arguments
    if (argc != 5) {
        std::cerr << "Erreur: nombre d'arguments incorrect\n";
        printUsage(argv[0]);
        return 1;
    }

    std::string input_file = argv[1];
    std::string output_file = argv[2];
    std::string algorithm = argv[3];
    int connectivity = std::atoi(argv[4]);

    // Validation des paramètres
    if (connectivity != 4 && connectivity != 8) {
        std::cerr << "Erreur: la connectivite doit etre 4 ou 8\n";
        return 1;
    }

    if (algorithm != "two_pass" && algorithm != "union_find" &&
        algorithm != "kruskal" && algorithm != "prim") {
        std::cerr << "Erreur: algorithme invalide\n";
        printUsage(argv[0]);
        return 1;
    }

    // ========================================================================
    // Étape 1 : Chargement de l'image
    // ========================================================================

    std::cout << "Chargement de l'image: " << input_file << "\n";

    Image input;
    try {
        if (isExtension(input_file, ".pgm") || isExtension(input_file, ".PGM")) {
            input = ImageIO::readPGM(input_file);
        } else if (isExtension(input_file, ".ppm") || isExtension(input_file, ".PPM")) {
            input = ImageIO::readPPM(input_file);
            std::cout << "  -> Image PPM convertie en niveaux de gris\n";
        } else {
            std::cerr << "Erreur: format non supporte (utilisez PGM ou PPM)\n";
            return 1;
        }
    } catch (const std::exception& e) {
        std::cerr << "Erreur lors du chargement: " << e.what() << "\n";
        return 1;
    }

    std::cout << "  Dimensions: " << input.getWidth() << " x " << input.getHeight() << "\n";
    std::cout << "  Pixels: " << input.getSize() << "\n\n";

    // Binariser l'image (seuil à 128)
    input.binarize(128);
    std::cout << "Image binarisee (seuil = 128)\n\n";

    // ========================================================================
    // Étape 2 : Labellisation
    // ========================================================================

    std::cout << "Algorithme: " << algorithm << "\n";
    std::cout << "Connectivite: " << connectivity << "\n";
    std::cout << "Labellisation en cours...\n";

    LabelImage labels;
    Utils::Timer timer;
    timer.start();

    try {
        if (algorithm == "two_pass") {
            labels = TwoPass::label(input, connectivity);
        } else if (algorithm == "union_find") {
            labels = UnionFind::label(input, connectivity);
        } else if (algorithm == "kruskal") {
            labels = Kruskal::label(input, connectivity);
        } else if (algorithm == "prim") {
            labels = Prim::label(input, connectivity);
        }
    } catch (const std::exception& e) {
        std::cerr << "Erreur lors de la labellisation: " << e.what() << "\n";
        return 1;
    }

    double elapsed = timer.stop();

    // Compter le nombre de composantes
    int num_components = labels.countLabels();

    std::cout << "\nLabellisation terminee!\n";
    std::cout << "  Temps d'execution: " << elapsed << " ms\n";
    std::cout << "  Composantes connexes trouvees: " << num_components << "\n\n";

    // ========================================================================
    // Étape 3 : Sauvegarde de l'image labellisée
    // ========================================================================

    std::cout << "Sauvegarde de l'image labellisee: " << output_file << "\n";

    try {
        // Convertir en image visualisable (normalisation sur [0, 255])
        Image output = labels.toVisualization();

        // Sauvegarder au format PGM
        ImageIO::writePGM(output_file, output, true);

        std::cout << "Image sauvegardee avec succes!\n";
    } catch (const std::exception& e) {
        std::cerr << "Erreur lors de la sauvegarde: " << e.what() << "\n";
        return 1;
    }

    std::cout << "\n========================================\n";
    std::cout << "  Traitement termine avec succes\n";
    std::cout << "========================================\n";

    return 0;
}
