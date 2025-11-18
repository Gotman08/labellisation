#ifndef IMAGE_H
#define IMAGE_H

#include <vector>
#include <cstdint>

/**
 * @brief Structure représentant un pixel avec ses coordonnées
 *
 * Utilisée pour la manipulation des pixels dans les algorithmes
 * de labellisation (notamment pour Union-Find, Kruskal et Prim)
 */
struct Pixel {
    int x;  // Coordonnée en ligne
    int y;  // Coordonnée en colonne

    Pixel() : x(0), y(0) {}
    Pixel(int x_, int y_) : x(x_), y(y_) {}

    bool operator==(const Pixel& other) const {
        return x == other.x && y == other.y;
    }

    bool operator!=(const Pixel& other) const {
        return !(*this == other);
    }
};

/**
 * @brief Classe représentant une image en niveaux de gris
 *
 * Cette classe implémente toutes les opérations de base sur les images
 * sans utiliser de bibliothèque externe (OpenCV, etc.).
 *
 * L'image est stockée en mémoire comme un tableau 1D pour optimiser
 * la localité spatiale et l'accès cache (important pour la performance).
 */
class Image {
private:
    int width_;          // Largeur de l'image
    int height_;         // Hauteur de l'image
    int max_value_;      // Valeur maximale des pixels (255 pour 8-bit)
    std::vector<uint8_t> data_;  // Données de l'image (stockage 1D)

public:
    /**
     * @brief Constructeur par défaut (image vide)
     */
    Image();

    /**
     * @brief Constructeur avec dimensions
     * @param width Largeur de l'image
     * @param height Hauteur de l'image
     * @param max_value Valeur maximale des pixels (défaut: 255)
     */
    Image(int width, int height, int max_value = 255);

    /**
     * @brief Destructeur
     */
    ~Image();

    // Getters
    int getWidth() const { return width_; }
    int getHeight() const { return height_; }
    int getMaxValue() const { return max_value_; }
    int getSize() const { return width_ * height_; }

    /**
     * @brief Accès à un pixel (lecture/écriture)
     * @param x Coordonnée ligne
     * @param y Coordonnée colonne
     * @return Référence vers la valeur du pixel
     */
    uint8_t& at(int x, int y);

    /**
     * @brief Accès à un pixel (lecture seule)
     * @param x Coordonnée ligne
     * @param y Coordonnée colonne
     * @return Valeur du pixel
     */
    uint8_t at(int x, int y) const;

    /**
     * @brief Vérifie si les coordonnées sont valides
     * @param x Coordonnée ligne
     * @param y Coordonnée colonne
     * @return true si les coordonnées sont dans l'image
     */
    bool isValid(int x, int y) const;

    /**
     * @brief Remplit l'image avec une valeur
     * @param value Valeur à affecter à tous les pixels
     */
    void fill(uint8_t value);

    /**
     * @brief Copie les données d'une autre image
     * @param other Image source
     */
    void copyFrom(const Image& other);

    /**
     * @brief Accès direct aux données (utile pour l'I/O)
     * @return Pointeur vers les données
     */
    uint8_t* getData() { return data_.data(); }
    const uint8_t* getData() const { return data_.data(); }

    /**
     * @brief Binarise l'image avec un seuil
     * @param threshold Seuil de binarisation
     *
     * Les pixels >= threshold deviennent 255 (blanc)
     * Les pixels < threshold deviennent 0 (noir)
     */
    void binarize(uint8_t threshold);
};

/**
 * @brief Classe pour une image d'étiquettes (labels)
 *
 * Utilisée pour stocker le résultat de la labellisation.
 * Utilise des entiers 32-bit pour supporter un grand nombre de labels.
 */
class LabelImage {
private:
    int width_;
    int height_;
    std::vector<int32_t> labels_;  // Stockage des labels

public:
    LabelImage();
    LabelImage(int width, int height);
    ~LabelImage();

    int getWidth() const { return width_; }
    int getHeight() const { return height_; }
    int getSize() const { return width_ * height_; }

    int32_t& at(int x, int y);
    int32_t at(int x, int y) const;

    bool isValid(int x, int y) const;
    void fill(int32_t value);

    int32_t* getData() { return labels_.data(); }
    const int32_t* getData() const { return labels_.data(); }

    /**
     * @brief Compte le nombre de labels distincts (hors 0)
     * @return Nombre de composantes connexes
     */
    int countLabels() const;

    /**
     * @brief Normalise les labels pour la visualisation
     * @return Image 8-bit avec labels normalisés
     *
     * Remappe les labels sur [0, 255] pour pouvoir sauvegarder
     * l'image labellisée au format PGM.
     */
    Image toVisualization() const;
};

#endif // IMAGE_H
