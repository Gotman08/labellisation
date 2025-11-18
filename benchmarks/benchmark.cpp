/**
 * Programme de benchmark pour comparer les algorithmes de labellisation
 *
 * Ce programme compare les 4 algorithmes sur différentes images et
 * génère des statistiques de performance.
 *
 * Métriques mesurées :
 * - Temps d'exécution (moyenne sur plusieurs runs)
 * - Écart-type du temps
 * - Nombre de composantes connexes trouvées
 * - Vérification de la cohérence des résultats
 *
 * Usage :
 *   ./benchmark <image1.pgm> [image2.pgm] [...]
 */

#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

#include "core/Image.h"
#include "io/ImageIO.h"
#include "algorithms/TwoPass.h"
#include "algorithms/UnionFind.h"
#include "algorithms/Kruskal.h"
#include "algorithms/Prim.h"
#include "utils/Utils.h"

// ============================================================================
// Structures pour les résultats
// ============================================================================

struct AlgorithmResult {
    std::string name;
    double mean_time;      // Temps moyen (ms)
    double std_dev;        // Écart-type (ms)
    double min_time;       // Temps minimum (ms)
    double max_time;       // Temps maximum (ms)
    int num_components;    // Nombre de composantes trouvées
};

struct BenchmarkConfig {
    int num_runs = 10;             // Nombre de runs pour moyenner
    int connectivity = 4;          // Connectivité à tester
    bool verify_results = true;    // Vérifier que tous les algos donnent le même résultat
};

// ============================================================================
// Fonctions de benchmark
// ============================================================================

AlgorithmResult benchmarkAlgorithm(
    const std::string& algo_name,
    const Image& input,
    int connectivity,
    int num_runs) {

    AlgorithmResult result;
    result.name = algo_name;

    std::vector<double> times;
    times.reserve(num_runs);

    LabelImage labels;

    for (int run = 0; run < num_runs; ++run) {
        Utils::Timer timer;
        timer.start();

        // Exécuter l'algorithme
        if (algo_name == "Two-Pass") {
            labels = TwoPass::label(input, connectivity);
        } else if (algo_name == "Union-Find") {
            labels = UnionFind::label(input, connectivity);
        } else if (algo_name == "Kruskal") {
            labels = Kruskal::label(input, connectivity);
        } else if (algo_name == "Prim") {
            labels = Prim::label(input, connectivity);
        }

        double elapsed = timer.stop();
        times.push_back(elapsed);
    }

    // Calculer les statistiques (implémentations manuelles)
    result.mean_time = Utils::mean(times.data(), num_runs);
    result.std_dev = Utils::standardDeviation(times.data(), num_runs);
    result.min_time = Utils::minArray(times.data(), num_runs);
    result.max_time = Utils::maxArray(times.data(), num_runs);
    result.num_components = labels.countLabels();

    return result;
}

void printResults(const std::vector<AlgorithmResult>& results,
                 const std::string& image_name,
                 int image_size,
                 int connectivity) {

    std::cout << "\n========================================\n";
    std::cout << "Resultats pour: " << image_name << "\n";
    std::cout << "  Taille: " << image_size << " pixels\n";
    std::cout << "  Connectivite: " << connectivity << "\n";
    std::cout << "========================================\n\n";

    // Header du tableau
    std::cout << std::setw(15) << "Algorithme"
              << std::setw(12) << "Moyenne"
              << std::setw(12) << "Ecart-type"
              << std::setw(12) << "Min"
              << std::setw(12) << "Max"
              << std::setw(15) << "Composantes\n";
    std::cout << std::string(78, '-') << "\n";

    // Résultats pour chaque algorithme
    for (const auto& result : results) {
        std::cout << std::setw(15) << result.name
                  << std::setw(12) << std::fixed << std::setprecision(2) << result.mean_time
                  << std::setw(12) << std::fixed << std::setprecision(2) << result.std_dev
                  << std::setw(12) << std::fixed << std::setprecision(2) << result.min_time
                  << std::setw(12) << std::fixed << std::setprecision(2) << result.max_time
                  << std::setw(15) << result.num_components << "\n";
    }

    std::cout << "\n";

    // Trouver l'algorithme le plus rapide (implémentation manuelle)
    int fastest_idx = 0;
    for (size_t i = 1; i < results.size(); ++i) {
        if (results[i].mean_time < results[fastest_idx].mean_time) {
            fastest_idx = i;
        }
    }

    std::cout << "Algorithme le plus rapide: " << results[fastest_idx].name << "\n";

    // Speedup relatif par rapport au plus rapide
    std::cout << "\nSpeedup relatif (par rapport a " << results[fastest_idx].name << "):\n";
    for (size_t i = 0; i < results.size(); ++i) {
        double speedup = results[i].mean_time / results[fastest_idx].mean_time;
        std::cout << "  " << std::setw(15) << results[i].name
                  << ": " << std::fixed << std::setprecision(2) << speedup << "x\n";
    }

    // Vérification de cohérence
    std::cout << "\nVerification de coherence:\n";
    int reference_count = results[0].num_components;
    bool all_match = true;
    for (const auto& result : results) {
        if (result.num_components != reference_count) {
            all_match = false;
            std::cout << "  ATTENTION: " << result.name << " a trouve "
                      << result.num_components << " composantes (attendu: "
                      << reference_count << ")\n";
        }
    }
    if (all_match) {
        std::cout << "  OK - Tous les algorithmes trouvent le meme nombre de composantes\n";
    }
}

// ============================================================================
// Fonction principale
// ============================================================================

int main(int argc, char* argv[]) {
    std::cout << "========================================\n";
    std::cout << "  Benchmark - Labellisation\n";
    std::cout << "========================================\n\n";

    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <image1.pgm> [image2.pgm] [...]\n";
        return 1;
    }

    BenchmarkConfig config;

    std::cout << "Configuration:\n";
    std::cout << "  Nombre de runs par algorithme: " << config.num_runs << "\n";
    std::cout << "  Connectivite: " << config.connectivity << "\n\n";

    // Liste des algorithmes à tester
    std::vector<std::string> algorithms = {
        "Two-Pass",
        "Union-Find",
        "Kruskal",
        "Prim"
    };

    // Pour chaque image fournie en argument
    for (int img_idx = 1; img_idx < argc; ++img_idx) {
        std::string image_file = argv[img_idx];

        std::cout << "Chargement de l'image: " << image_file << "\n";

        Image input;
        try {
            input = ImageIO::readPGM(image_file);
        } catch (const std::exception& e) {
            std::cerr << "Erreur: " << e.what() << "\n";
            continue;
        }

        // Binariser l'image
        input.binarize(128);

        // Benchmarker tous les algorithmes
        std::vector<AlgorithmResult> results;

        for (const auto& algo_name : algorithms) {
            std::cout << "  Benchmark " << algo_name << "... ";
            std::cout.flush();

            AlgorithmResult result = benchmarkAlgorithm(
                algo_name, input, config.connectivity, config.num_runs);

            results.push_back(result);

            std::cout << "OK (" << std::fixed << std::setprecision(2)
                      << result.mean_time << " ms)\n";
        }

        // Afficher les résultats
        printResults(results, image_file, input.getSize(), config.connectivity);
    }

    std::cout << "\n========================================\n";
    std::cout << "  Benchmark termine\n";
    std::cout << "========================================\n";

    return 0;
}
