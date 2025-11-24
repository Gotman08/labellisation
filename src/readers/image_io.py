"""
Module io/image_io.py - Lecture et écriture d'images

Supporte les formats :
- PGM/PPM (lecture native)
- JPEG, PNG, BMP, TIFF, etc. (via OpenCV)

IMPORTANT: numpy/OpenCV sont utilisés UNIQUEMENT pour charger l'image depuis
le fichier et la convertir en tableau. Toutes les autres opérations sont manuelles.

Auteurs : Romain Despoullain, Nicolas Marano, Amin Braham
"""

import numpy as np  # UNIQUEMENT pour np.frombuffer lors de la lecture binaire PGM/PPM
from pathlib import Path
from typing import BinaryIO, List
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.image import Image, ColorImage

# Essayer d'importer OpenCV pour les formats JPEG, PNG, etc.
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


class ImageIO:
    """
    Classe pour la lecture et l'écriture d'images.

    Supporte :
    - PGM/PPM : lecture native (numpy uniquement pour convertir bytes en array)
    - JPEG, PNG, BMP, TIFF, etc. : via OpenCV (cv2.imread)

    Toutes les autres opérations sont implémentées manuellement.
    """

    @staticmethod
    def _skip_whitespace_and_comments(file: BinaryIO) -> None:
        """
        Saute les espaces blancs et les commentaires dans le fichier PGM/PPM.
        """
        while True:
            c = file.read(1)
            if not c:
                break

            if c == b'#':
                while c and c != b'\n':
                    c = file.read(1)
            elif not c.isspace():
                file.seek(file.tell() - 1)
                break

    @staticmethod
    def _read_number(file: BinaryIO) -> int:
        """
        Lit un entier du flux en gérant les espaces et commentaires.
        """
        ImageIO._skip_whitespace_and_comments(file)

        number = 0
        has_digit = False

        while True:
            c = file.read(1)
            if not c:
                break

            if c.isdigit():
                number = number * 10 + int(c)
                has_digit = True
            else:
                file.seek(file.tell() - 1)
                break

        if not has_digit:
            raise RuntimeError("Erreur de lecture: nombre attendu")

        return number

    @staticmethod
    def _numpy_array_to_list2d(arr, height: int, width: int) -> List[List[int]]:
        """
        Convertit un array numpy 1D en liste Python 2D.
        """
        result = []
        for x in range(height):
            row = []
            for y in range(width):
                row.append(int(arr[x * width + y]))
            result.append(row)
        return result

    @staticmethod
    def _cv2_array_to_list2d(arr) -> List[List[int]]:
        """
        Convertit un array OpenCV 2D en liste Python 2D.

        OpenCV est utilisé UNIQUEMENT pour charger l'image.
        Cette fonction convertit immédiatement en listes Python pures.

        Args:
            arr: Array numpy 2D retourné par cv2.imread

        Returns:
            Liste 2D Python
        """
        height = arr.shape[0]
        width = arr.shape[1]
        result = []
        for x in range(height):
            row = []
            for y in range(width):
                row.append(int(arr[x, y]))
            result.append(row)
        return result

    @staticmethod
    def read_with_opencv(filename: str) -> Image:
        """
        Lit une image avec OpenCV (JPEG, PNG, BMP, TIFF, etc.).

        OpenCV est utilisé UNIQUEMENT pour charger l'image depuis le fichier.
        L'array est immédiatement converti en liste Python 2D.

        Args:
            filename: Chemin du fichier

        Returns:
            Image en niveaux de gris

        Raises:
            RuntimeError: si OpenCV n'est pas disponible ou si le fichier ne peut être lu
        """
        if not OPENCV_AVAILABLE:
            raise RuntimeError(
                "OpenCV n'est pas installe. Installez-le avec: pip install opencv-python"
            )

        # SEUL USAGE D'OPENCV: charger l'image en niveaux de gris
        cv_image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

        if cv_image is None:
            raise RuntimeError(f"Impossible de lire l'image: {filename}")

        # Obtenir les dimensions
        height, width = cv_image.shape

        # Créer l'objet Image
        image = Image(width, height, 255)

        # Convertir immédiatement l'array OpenCV en liste Python 2D
        image.data = ImageIO._cv2_array_to_list2d(cv_image)

        return image

    @staticmethod
    def read_pgm(filename: str) -> Image:
        """
        Lit une image PGM depuis un fichier.
        Supporte les formats P2 (ASCII) et P5 (binaire).
        """
        with open(filename, 'rb') as file:
            magic = b''
            c = file.read(1)
            while c and not c.isspace():
                magic += c
                c = file.read(1)
            magic = magic.decode('ascii')

            if magic not in ('P2', 'P5'):
                raise RuntimeError(f"Format non supporte (uniquement P2 et P5): {magic}")

            is_binary = (magic == 'P5')

            width = ImageIO._read_number(file)
            height = ImageIO._read_number(file)
            max_value = ImageIO._read_number(file)

            if width <= 0 or height <= 0:
                raise RuntimeError("Dimensions invalides")

            image = Image(width, height, max_value)

            if is_binary:
                file.read(1)
                raw_data = file.read(width * height)
                if len(raw_data) != width * height:
                    raise RuntimeError("Erreur de lecture des donnees binaires")

                numpy_arr = np.frombuffer(raw_data, dtype=np.uint8)
                image.data = ImageIO._numpy_array_to_list2d(numpy_arr, height, width)
            else:
                data = [[0 for _ in range(width)] for _ in range(height)]
                for x in range(height):
                    for y in range(width):
                        value = ImageIO._read_number(file)
                        if value < 0 or value > max_value:
                            raise RuntimeError("Valeur de pixel invalide")
                        data[x][y] = value
                image.data = data

        return image

    @staticmethod
    def write_pgm(filename: str, image: Image, binary: bool = True) -> None:
        """
        Écrit une image au format PGM.
        """
        with open(filename, 'wb') as file:
            if binary:
                header = f"P5\n# Created by Labellisation Project\n{image.width} {image.height}\n{image.max_value}\n"
                file.write(header.encode('ascii'))
                for x in range(image.height):
                    for y in range(image.width):
                        file.write(bytes([image.at(x, y)]))
            else:
                header = f"P2\n# Created by Labellisation Project\n{image.width} {image.height}\n{image.max_value}\n"
                file.write(header.encode('ascii'))
                count = 0
                for x in range(image.height):
                    for y in range(image.width):
                        file.write(f"{image.at(x, y)} ".encode('ascii'))
                        count += 1
                        if count % 16 == 0:
                            file.write(b"\n")
                if count % 16 != 0:
                    file.write(b"\n")

    @staticmethod
    def read_ppm(filename: str) -> Image:
        """
        Lit une image PPM (couleur) et la convertit en niveaux de gris.
        """
        with open(filename, 'rb') as file:
            magic = b''
            c = file.read(1)
            while c and not c.isspace():
                magic += c
                c = file.read(1)
            magic = magic.decode('ascii')

            if magic not in ('P3', 'P6'):
                raise RuntimeError(f"Format non supporte (uniquement P3 et P6): {magic}")

            is_binary = (magic == 'P6')

            width = ImageIO._read_number(file)
            height = ImageIO._read_number(file)
            max_value = ImageIO._read_number(file)

            if width <= 0 or height <= 0:
                raise RuntimeError("Dimensions invalides")

            image = Image(width, height, max_value)
            data = [[0 for _ in range(width)] for _ in range(height)]

            if is_binary:
                file.read(1)
                raw_data = file.read(width * height * 3)
                if len(raw_data) != width * height * 3:
                    raise RuntimeError("Erreur de lecture des donnees binaires")

                numpy_arr = np.frombuffer(raw_data, dtype=np.uint8)

                for x in range(height):
                    for y in range(width):
                        idx = (x * width + y) * 3
                        r = int(numpy_arr[idx])
                        g = int(numpy_arr[idx + 1])
                        b = int(numpy_arr[idx + 2])
                        gray = (299 * r + 587 * g + 114 * b) // 1000
                        data[x][y] = gray
            else:
                for x in range(height):
                    for y in range(width):
                        r = ImageIO._read_number(file)
                        g = ImageIO._read_number(file)
                        b = ImageIO._read_number(file)
                        gray = (299 * r + 587 * g + 114 * b) // 1000
                        data[x][y] = gray

            image.data = data

        return image

    @staticmethod
    def write_ppm(filename: str, image: Image, binary: bool = True) -> None:
        """
        Écrit une image couleur au format PPM.
        """
        with open(filename, 'wb') as file:
            if binary:
                header = f"P6\n# Created by Labellisation Project\n{image.width} {image.height}\n{image.max_value}\n"
                file.write(header.encode('ascii'))
                for x in range(image.height):
                    for y in range(image.width):
                        value = image.at(x, y)
                        file.write(bytes([value, value, value]))
            else:
                header = f"P3\n# Created by Labellisation Project\n{image.width} {image.height}\n{image.max_value}\n"
                file.write(header.encode('ascii'))
                count = 0
                for x in range(image.height):
                    for y in range(image.width):
                        value = image.at(x, y)
                        file.write(f"{value} {value} {value} ".encode('ascii'))
                        count += 1
                        if count % 5 == 0:
                            file.write(b"\n")

    @staticmethod
    def write_with_opencv(filename: str, image: Image) -> None:
        """
        Écrit une image avec OpenCV (JPEG, PNG, BMP, etc.).

        Args:
            filename: Chemin du fichier de sortie
            image: Image à sauvegarder
        """
        if not OPENCV_AVAILABLE:
            raise RuntimeError(
                "OpenCV n'est pas installe. Installez-le avec: pip install opencv-python"
            )

        # Convertir la liste 2D en array numpy pour OpenCV
        import numpy as np
        height = image.height
        width = image.width
        arr = np.zeros((height, width), dtype=np.uint8)
        for x in range(height):
            for y in range(width):
                arr[x, y] = image.at(x, y)

        # Écrire avec OpenCV
        cv2.imwrite(filename, arr)

    @staticmethod
    def read_image(filename: str) -> Image:
        """
        Lit une image en détectant automatiquement le format.

        Supporte :
        - PGM, PPM (lecture native)
        - JPEG, PNG, BMP, TIFF, GIF, WEBP, etc. (via OpenCV)

        Args:
            filename: Chemin du fichier

        Returns:
            Image chargée
        """
        ext = Path(filename).suffix.lower()

        # Formats PGM/PPM : lecture native
        if ext == '.pgm':
            return ImageIO.read_pgm(filename)
        elif ext == '.ppm':
            return ImageIO.read_ppm(filename)

        # Formats courants : utiliser OpenCV
        opencv_formats = {
            '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif',
            '.gif', '.webp', '.ico', '.pbm'
        }

        if ext in opencv_formats:
            return ImageIO.read_with_opencv(filename)

        # Essayer de détecter le format par le magic number
        try:
            with open(filename, 'rb') as f:
                magic = f.read(2).decode('ascii', errors='ignore')

            if magic in ('P2', 'P5'):
                return ImageIO.read_pgm(filename)
            elif magic in ('P3', 'P6'):
                return ImageIO.read_ppm(filename)
        except:
            pass

        # En dernier recours, essayer OpenCV
        if OPENCV_AVAILABLE:
            try:
                return ImageIO.read_with_opencv(filename)
            except:
                pass

        raise RuntimeError(f"Format de fichier non reconnu: {filename}")

    @staticmethod
    def write_image(filename: str, image: Image) -> None:
        """
        Écrit une image en détectant automatiquement le format.

        Args:
            filename: Chemin du fichier de sortie
            image: Image à sauvegarder
        """
        ext = Path(filename).suffix.lower()

        if ext == '.pgm':
            ImageIO.write_pgm(filename, image)
        elif ext == '.ppm':
            ImageIO.write_ppm(filename, image)
        elif ext in {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}:
            ImageIO.write_with_opencv(filename, image)
        else:
            # Par défaut, écrire en PGM
            ImageIO.write_pgm(filename, image)

    @staticmethod
    def write_color_image(filename: str, color_image: ColorImage) -> None:
        """
        Écrit une image couleur (RGB).

        Args:
            filename: Chemin du fichier de sortie
            color_image: Image couleur à sauvegarder
        """
        ext = Path(filename).suffix.lower()

        if ext == '.ppm':
            ImageIO.write_color_ppm(filename, color_image)
        elif ext in {'.png', '.bmp', '.tiff', '.tif'}:
            ImageIO.write_color_with_opencv(filename, color_image)
        else:
            # Par défaut, écrire en PPM
            ImageIO.write_color_ppm(filename, color_image)

    @staticmethod
    def write_color_ppm(filename: str, color_image: ColorImage, binary: bool = True) -> None:
        """
        Écrit une image couleur au format PPM.

        Args:
            filename: Chemin du fichier
            color_image: Image couleur RGB
            binary: True pour P6 (binaire), False pour P3 (ASCII)
        """
        with open(filename, 'wb') as file:
            if binary:
                header = f"P6\n# Color visualization - Labellisation Project\n{color_image.width} {color_image.height}\n255\n"
                file.write(header.encode('ascii'))
                for x in range(color_image.height):
                    for y in range(color_image.width):
                        r, g, b = color_image.at(x, y)
                        file.write(bytes([r, g, b]))
            else:
                header = f"P3\n# Color visualization - Labellisation Project\n{color_image.width} {color_image.height}\n255\n"
                file.write(header.encode('ascii'))
                count = 0
                for x in range(color_image.height):
                    for y in range(color_image.width):
                        r, g, b = color_image.at(x, y)
                        file.write(f"{r} {g} {b} ".encode('ascii'))
                        count += 1
                        if count % 5 == 0:
                            file.write(b"\n")

    @staticmethod
    def write_color_with_opencv(filename: str, color_image: ColorImage) -> None:
        """
        Écrit une image couleur avec OpenCV (PNG, BMP, etc.).

        Args:
            filename: Chemin du fichier de sortie
            color_image: Image couleur à sauvegarder
        """
        if not OPENCV_AVAILABLE:
            raise RuntimeError(
                "OpenCV n'est pas installe. Utilisez le format PPM ou installez OpenCV."
            )

        import numpy as np
        height = color_image.height
        width = color_image.width

        # OpenCV utilise BGR, pas RGB
        arr = np.zeros((height, width, 3), dtype=np.uint8)
        for x in range(height):
            for y in range(width):
                r, g, b = color_image.at(x, y)
                arr[x, y] = [b, g, r]  # BGR pour OpenCV

        cv2.imwrite(filename, arr)
