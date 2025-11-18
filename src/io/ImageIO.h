#ifndef IMAGEIO_H
#define IMAGEIO_H

#include "core/Image.h"
#include <string>

/**
 * @brief Classe pour la lecture et l'écriture d'images
 *
 * Implémente la lecture/écriture de fichiers PGM (Portable GrayMap) et
 * PPM (Portable PixMap) sans utiliser aucune bibliothèque externe.
 *
 * Format PGM :
 * - Format texte simple pour images en niveaux de gris
 * - Header: "P2" (ASCII) ou "P5" (binaire)
 * - Largeur Hauteur
 * - Valeur maximale (généralement 255)
 * - Données pixels
 *
 * Ce format est idéal pour ce projet car :
 * - Simple à parser manuellement
 * - Pas de compression (pas de dépendances externes)
 * - Lisible par la plupart des visualiseurs d'images
 */
class ImageIO {
public:
    /**
     * @brief Lit une image PGM depuis un fichier
     * @param filename Chemin du fichier
     * @return Image chargée
     * @throws std::runtime_error si le fichier ne peut être lu
     *
     * Supporte les formats P2 (ASCII) et P5 (binaire)
     * Ignore les commentaires (lignes commençant par '#')
     */
    static Image readPGM(const std::string& filename);

    /**
     * @brief Écrit une image au format PGM
     * @param filename Chemin du fichier de sortie
     * @param image Image à sauvegarder
     * @param binary Si true, utilise P5 (binaire), sinon P2 (ASCII)
     * @throws std::runtime_error si le fichier ne peut être écrit
     */
    static void writePGM(const std::string& filename, const Image& image, bool binary = true);

    /**
     * @brief Lit une image PPM (couleur) et la convertit en niveaux de gris
     * @param filename Chemin du fichier
     * @return Image en niveaux de gris
     *
     * Conversion RGB -> Gray avec formule standard :
     * Gray = 0.299*R + 0.587*G + 0.114*B
     * (implémentation manuelle sans coefficients flottants pour la performance)
     */
    static Image readPPM(const std::string& filename);

    /**
     * @brief Écrit une image couleur au format PPM
     * @param filename Chemin du fichier de sortie
     * @param image Image source (sera dupliquée en R=G=B pour visualisation)
     * @param binary Si true, utilise P6 (binaire), sinon P3 (ASCII)
     */
    static void writePPM(const std::string& filename, const Image& image, bool binary = true);

private:
    /**
     * @brief Saute les espaces et commentaires dans un flux
     * @param file Flux de fichier
     *
     * Les commentaires PGM/PPM commencent par '#' et vont jusqu'à la fin de ligne
     */
    static void skipWhitespaceAndComments(std::istream& file);

    /**
     * @brief Lit un entier depuis le flux en sautant les espaces/commentaires
     * @param file Flux de fichier
     * @return Entier lu
     */
    static int readNumber(std::istream& file);
};

#endif // IMAGEIO_H
