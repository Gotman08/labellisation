#include "io/ImageIO.h"
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <cctype>

// ============================================================================
// Fonctions utilitaires privées
// ============================================================================

void ImageIO::skipWhitespaceAndComments(std::istream& file) {
    /**
     * Saute les espaces blancs et les commentaires dans le fichier PGM/PPM
     *
     * Les commentaires commencent par '#' et s'étendent jusqu'à la fin de ligne.
     * Cette fonction est nécessaire pour parser correctement le header.
     */
    char c;
    while (file.get(c)) {
        if (c == '#') {
            // Commentaire: ignorer jusqu'à la fin de ligne
            while (file.get(c) && c != '\n') {}
        } else if (!std::isspace(static_cast<unsigned char>(c))) {
            // Caractère non-espace trouvé, le remettre dans le flux
            file.unget();
            break;
        }
    }
}

int ImageIO::readNumber(std::istream& file) {
    /**
     * Lit un entier du flux en gérant les espaces et commentaires
     *
     * Implémentation manuelle du parsing d'entier pour éviter
     * les problèmes avec operator>> qui ne gère pas les commentaires.
     */
    skipWhitespaceAndComments(file);

    int number = 0;
    char c;

    // Lire les chiffres
    bool hasDigit = false;
    while (file.get(c)) {
        if (std::isdigit(static_cast<unsigned char>(c))) {
            number = number * 10 + (c - '0');
            hasDigit = true;
        } else {
            file.unget();
            break;
        }
    }

    if (!hasDigit) {
        throw std::runtime_error("Erreur de lecture: nombre attendu");
    }

    return number;
}

// ============================================================================
// Lecture PGM
// ============================================================================

Image ImageIO::readPGM(const std::string& filename) {
    /**
     * Implémentation complète de la lecture PGM sans bibliothèque externe
     *
     * Format PGM:
     * P2 (ou P5)        <- Magic number (P2=ASCII, P5=binaire)
     * # commentaire     <- Optionnel
     * width height      <- Dimensions
     * maxval            <- Valeur max (généralement 255)
     * data...           <- Pixels
     */

    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        throw std::runtime_error("Impossible d'ouvrir le fichier: " + filename);
    }

    // Lire le magic number
    std::string magic;
    file >> magic;

    if (magic != "P2" && magic != "P5") {
        throw std::runtime_error("Format non supporté (uniquement P2 et P5): " + magic);
    }

    bool isBinary = (magic == "P5");

    // Lire les dimensions et max_value
    int width = readNumber(file);
    int height = readNumber(file);
    int max_value = readNumber(file);

    if (width <= 0 || height <= 0) {
        throw std::runtime_error("Dimensions invalides");
    }

    // Créer l'image
    Image image(width, height, max_value);

    if (isBinary) {
        // Format binaire P5
        // Sauter le dernier caractère d'espacement après max_value
        char c;
        file.get(c);

        // Lire les données binaires directement
        file.read(reinterpret_cast<char*>(image.getData()), width * height);

        if (!file) {
            throw std::runtime_error("Erreur de lecture des données binaires");
        }
    } else {
        // Format ASCII P2
        // Lire les pixels un par un
        for (int x = 0; x < height; ++x) {
            for (int y = 0; y < width; ++y) {
                int value = readNumber(file);
                if (value < 0 || value > max_value) {
                    throw std::runtime_error("Valeur de pixel invalide");
                }
                image.at(x, y) = static_cast<uint8_t>(value);
            }
        }
    }

    file.close();
    return image;
}

// ============================================================================
// Écriture PGM
// ============================================================================

void ImageIO::writePGM(const std::string& filename, const Image& image, bool binary) {
    /**
     * Sauvegarde une image au format PGM
     *
     * @param binary Si true, utilise P5 (binaire, plus compact)
     *               Si false, utilise P2 (ASCII, lisible en texte)
     */

    std::ofstream file(filename, binary ? std::ios::binary : std::ios::out);
    if (!file.is_open()) {
        throw std::runtime_error("Impossible d'ouvrir le fichier: " + filename);
    }

    // Écrire le header
    if (binary) {
        file << "P5\n";
    } else {
        file << "P2\n";
    }

    file << "# Created by Labellisation Project\n";
    file << image.getWidth() << " " << image.getHeight() << "\n";
    file << image.getMaxValue() << "\n";

    if (binary) {
        // Format binaire
        file.write(reinterpret_cast<const char*>(image.getData()),
                   image.getWidth() * image.getHeight());
    } else {
        // Format ASCII
        // Écrire les pixels avec 16 valeurs par ligne pour la lisibilité
        int count = 0;
        for (int x = 0; x < image.getHeight(); ++x) {
            for (int y = 0; y < image.getWidth(); ++y) {
                file << static_cast<int>(image.at(x, y)) << " ";
                count++;
                if (count % 16 == 0) {
                    file << "\n";
                }
            }
        }
        if (count % 16 != 0) {
            file << "\n";
        }
    }

    file.close();
}

// ============================================================================
// Lecture PPM (avec conversion en niveaux de gris)
// ============================================================================

Image ImageIO::readPPM(const std::string& filename) {
    /**
     * Lit une image PPM couleur et la convertit en niveaux de gris
     *
     * Format PPM:
     * P3 (ou P6)
     * width height
     * maxval
     * R G B R G B ...   (triplets de valeurs)
     *
     * Conversion RGB -> Grayscale :
     * Gray = 0.299*R + 0.587*G + 0.114*B
     *
     * Pour éviter les flottants, on utilise l'arithmétique entière :
     * Gray = (299*R + 587*G + 114*B) / 1000
     */

    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        throw std::runtime_error("Impossible d'ouvrir le fichier: " + filename);
    }

    // Lire le magic number
    std::string magic;
    file >> magic;

    if (magic != "P3" && magic != "P6") {
        throw std::runtime_error("Format non supporté (uniquement P3 et P6): " + magic);
    }

    bool isBinary = (magic == "P6");

    // Lire les dimensions et max_value
    int width = readNumber(file);
    int height = readNumber(file);
    int max_value = readNumber(file);

    if (width <= 0 || height <= 0) {
        throw std::runtime_error("Dimensions invalides");
    }

    // Créer l'image en niveaux de gris
    Image image(width, height, max_value);

    if (isBinary) {
        // Format binaire P6
        char c;
        file.get(c);

        // Lire et convertir les pixels RGB
        for (int x = 0; x < height; ++x) {
            for (int y = 0; y < width; ++y) {
                uint8_t r, g, b;
                file.read(reinterpret_cast<char*>(&r), 1);
                file.read(reinterpret_cast<char*>(&g), 1);
                file.read(reinterpret_cast<char*>(&b), 1);

                // Conversion manuelle RGB -> Gray
                int gray = (299 * r + 587 * g + 114 * b) / 1000;
                image.at(x, y) = static_cast<uint8_t>(gray);
            }
        }
    } else {
        // Format ASCII P3
        for (int x = 0; x < height; ++x) {
            for (int y = 0; y < width; ++y) {
                int r = readNumber(file);
                int g = readNumber(file);
                int b = readNumber(file);

                // Conversion manuelle RGB -> Gray
                int gray = (299 * r + 587 * g + 114 * b) / 1000;
                image.at(x, y) = static_cast<uint8_t>(gray);
            }
        }
    }

    file.close();
    return image;
}

// ============================================================================
// Écriture PPM
// ============================================================================

void ImageIO::writePPM(const std::string& filename, const Image& image, bool binary) {
    /**
     * Sauvegarde une image en niveaux de gris au format PPM couleur
     * (en dupliquant la valeur sur R=G=B)
     *
     * Utile pour certains visualiseurs qui ne supportent que PPM.
     */

    std::ofstream file(filename, binary ? std::ios::binary : std::ios::out);
    if (!file.is_open()) {
        throw std::runtime_error("Impossible d'ouvrir le fichier: " + filename);
    }

    // Écrire le header
    if (binary) {
        file << "P6\n";
    } else {
        file << "P3\n";
    }

    file << "# Created by Labellisation Project\n";
    file << image.getWidth() << " " << image.getHeight() << "\n";
    file << image.getMaxValue() << "\n";

    if (binary) {
        // Format binaire: écrire R=G=B pour chaque pixel
        for (int x = 0; x < image.getHeight(); ++x) {
            for (int y = 0; y < image.getWidth(); ++y) {
                uint8_t value = image.at(x, y);
                file.write(reinterpret_cast<const char*>(&value), 1);
                file.write(reinterpret_cast<const char*>(&value), 1);
                file.write(reinterpret_cast<const char*>(&value), 1);
            }
        }
    } else {
        // Format ASCII
        int count = 0;
        for (int x = 0; x < image.getHeight(); ++x) {
            for (int y = 0; y < image.getWidth(); ++y) {
                int value = static_cast<int>(image.at(x, y));
                file << value << " " << value << " " << value << " ";
                count++;
                if (count % 5 == 0) {
                    file << "\n";
                }
            }
        }
    }

    file.close();
}
