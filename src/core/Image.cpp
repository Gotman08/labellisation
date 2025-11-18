#include "core/Image.h"
#include <stdexcept>
#include <algorithm>

// ============================================================================
// Classe Image - Implémentation
// ============================================================================

Image::Image() : width_(0), height_(0), max_value_(255) {}

Image::Image(int width, int height, int max_value)
    : width_(width), height_(height), max_value_(max_value) {
    if (width <= 0 || height <= 0) {
        throw std::invalid_argument("Les dimensions de l'image doivent être positives");
    }
    data_.resize(width * height, 0);
}

Image::~Image() {}

uint8_t& Image::at(int x, int y) {
    if (!isValid(x, y)) {
        throw std::out_of_range("Coordonnées hors limites");
    }
    // Stockage row-major: index = x * width + y
    return data_[x * width_ + y];
}

uint8_t Image::at(int x, int y) const {
    if (!isValid(x, y)) {
        throw std::out_of_range("Coordonnées hors limites");
    }
    return data_[x * width_ + y];
}

bool Image::isValid(int x, int y) const {
    return x >= 0 && x < height_ && y >= 0 && y < width_;
}

void Image::fill(uint8_t value) {
    // Remplissage manuel (pas d'utilisation de std::fill)
    for (int i = 0; i < static_cast<int>(data_.size()); ++i) {
        data_[i] = value;
    }
}

void Image::copyFrom(const Image& other) {
    width_ = other.width_;
    height_ = other.height_;
    max_value_ = other.max_value_;
    data_ = other.data_;
}

void Image::binarize(uint8_t threshold) {
    /**
     * Binarisation manuelle sans utiliser de fonctions standard
     * Convertit l'image en image binaire (0 ou 255)
     *
     * Cette opération est souvent nécessaire avant la labellisation
     * pour s'assurer que l'image ne contient que des pixels "objet"
     * (blanc, valeur 255) et "fond" (noir, valeur 0).
     */
    for (int i = 0; i < static_cast<int>(data_.size()); ++i) {
        if (data_[i] >= threshold) {
            data_[i] = 255;
        } else {
            data_[i] = 0;
        }
    }
}

// ============================================================================
// Classe LabelImage - Implémentation
// ============================================================================

LabelImage::LabelImage() : width_(0), height_(0) {}

LabelImage::LabelImage(int width, int height)
    : width_(width), height_(height) {
    if (width <= 0 || height <= 0) {
        throw std::invalid_argument("Les dimensions de l'image doivent être positives");
    }
    labels_.resize(width * height, 0);
}

LabelImage::~LabelImage() {}

int32_t& LabelImage::at(int x, int y) {
    if (!isValid(x, y)) {
        throw std::out_of_range("Coordonnées hors limites");
    }
    return labels_[x * width_ + y];
}

int32_t LabelImage::at(int x, int y) const {
    if (!isValid(x, y)) {
        throw std::out_of_range("Coordonnées hors limites");
    }
    return labels_[x * width_ + y];
}

bool LabelImage::isValid(int x, int y) const {
    return x >= 0 && x < height_ && y >= 0 && y < width_;
}

void LabelImage::fill(int32_t value) {
    // Remplissage manuel
    for (int i = 0; i < static_cast<int>(labels_.size()); ++i) {
        labels_[i] = value;
    }
}

int LabelImage::countLabels() const {
    /**
     * Compte le nombre de labels distincts (implémentation manuelle)
     *
     * Méthode :
     * 1. Parcourir tous les labels
     * 2. Marquer les labels rencontrés dans un tableau booléen
     * 3. Compter le nombre de labels marqués (hors 0 qui est le fond)
     */

    // Trouver le label maximum pour dimensionner le tableau
    int max_label = 0;
    for (int i = 0; i < static_cast<int>(labels_.size()); ++i) {
        if (labels_[i] > max_label) {
            max_label = labels_[i];
        }
    }

    if (max_label == 0) {
        return 0;
    }

    // Créer un tableau de marquage
    std::vector<bool> seen(max_label + 1, false);

    // Marquer les labels présents
    for (int i = 0; i < static_cast<int>(labels_.size()); ++i) {
        if (labels_[i] > 0) {
            seen[labels_[i]] = true;
        }
    }

    // Compter les labels distincts (hors 0)
    int count = 0;
    for (int i = 1; i <= max_label; ++i) {
        if (seen[i]) {
            count++;
        }
    }

    return count;
}

Image LabelImage::toVisualization() const {
    /**
     * Convertit l'image de labels en image visualisable
     *
     * Méthode :
     * 1. Trouver le nombre de labels distincts
     * 2. Normaliser les labels sur [0, 255]
     * 3. Créer une image 8-bit pour la visualisation
     *
     * Note: Si il y a plus de 255 labels, il y aura des collisions
     * visuelles mais c'est acceptable pour la visualisation.
     */

    Image result(width_, height_);

    // Trouver le label maximum
    int max_label = 0;
    for (int i = 0; i < static_cast<int>(labels_.size()); ++i) {
        if (labels_[i] > max_label) {
            max_label = labels_[i];
        }
    }

    if (max_label == 0) {
        // Pas de labels, retourner une image noire
        result.fill(0);
        return result;
    }

    // Normaliser les labels
    for (int x = 0; x < height_; ++x) {
        for (int y = 0; y < width_; ++y) {
            int32_t label = at(x, y);
            if (label == 0) {
                // Fond reste noir
                result.at(x, y) = 0;
            } else {
                // Mapper le label sur [1, 255]
                // Formule manuelle: value = (label * 254 / max_label) + 1
                uint8_t value = static_cast<uint8_t>((label * 254 / max_label) + 1);
                result.at(x, y) = value;
            }
        }
    }

    return result;
}
