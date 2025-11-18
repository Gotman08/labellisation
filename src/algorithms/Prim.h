#ifndef PRIM_H
#define PRIM_H

#include "core/Image.h"
#include <vector>
#include <queue>

/**
 * @brief Algorithme de Prim pour la labellisation
 *
 * Comme Kruskal, Prim est un algorithme de Minimum Spanning Tree (MST).
 * Il utilise également le modèle de graphe du CM05.
 *
 * DIFFÉRENCE KRUSKAL vs PRIM :
 *
 * - Kruskal : approche "par arêtes"
 *   → Trie toutes les arêtes et les ajoute une par une
 *
 * - Prim : approche "par sommets"
 *   → Grandit l'arbre à partir d'un sommet initial
 *   → À chaque étape, ajoute le sommet le plus proche de l'arbre courant
 *
 * ALGORITHME DE PRIM CLASSIQUE :
 *
 * 1. Choisir un sommet de départ arbitraire
 * 2. Marquer ce sommet comme "dans l'arbre"
 * 3. Répéter jusqu'à ce que tous les sommets soient dans l'arbre :
 *    a) Trouver l'arête de poids minimum entre :
 *       - Un sommet "dans l'arbre"
 *       - Un sommet "hors de l'arbre"
 *    b) Ajouter cette arête au MST
 *    c) Marquer le nouveau sommet comme "dans l'arbre"
 *
 * APPLICATION À LA LABELLISATION :
 *
 * Pour la labellisation, on adapte Prim :
 * - Construire une forêt (pas un seul arbre) car le graphe a plusieurs
 *   composantes connexes
 * - Algorithme :
 *   1. Pour chaque pixel "objet" non encore labellisé :
 *      a) Créer un nouveau label
 *      b) Lancer Prim depuis ce pixel pour explorer toute sa composante
 *      c) Tous les pixels atteints reçoivent ce label
 *
 * IMPLÉMENTATION :
 *
 * On utilise une approche BFS (Breadth-First Search) / DFS (Depth-First Search)
 * simplifiée au lieu de Prim avec file de priorité, car :
 * - Toutes les arêtes ont le même poids (pas besoin de file de priorité)
 * - BFS/DFS explore exactement la même composante connexe que Prim
 * - Plus simple et plus efficace
 *
 * PSEUDO-CODE (version BFS) :
 *
 * Pour chaque pixel (x, y) :
 *   Si pixel est "objet" ET non labellisé :
 *     label_actuel++
 *     queue.push((x, y))
 *     Tant que queue non vide :
 *       p = queue.pop()
 *       labels[p] = label_actuel
 *       Pour chaque voisin v de p :
 *         Si v est "objet" ET non labellisé :
 *           queue.push(v)
 *
 * COMPLEXITÉ :
 * - Temps: O(N) où N est le nombre de pixels
 *   (chaque pixel est visité une seule fois)
 * - Espace: O(N) pour la file (dans le pire cas)
 *
 * COMPARAISON :
 * - Plus simple que Kruskal (pas de tri d'arêtes)
 * - Même complexité pratique que Union-Find
 * - Bon cache locality si BFS (parcours par couches)
 */
class Prim {
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
     * @brief Explore une composante connexe par BFS
     * @param input Image binaire
     * @param labels Image de labels (modifiée)
     * @param start_x Coordonnée ligne de départ
     * @param start_y Coordonnée colonne de départ
     * @param label Label à affecter
     * @param connectivity Connectivité (4 ou 8)
     *
     * Explore tous les pixels de la composante connexe contenant
     * (start_x, start_y) et leur affecte le label donné.
     */
    static void bfs(const Image& input, LabelImage& labels,
                   int start_x, int start_y, int label, int connectivity);

    /**
     * @brief Explore une composante connexe par DFS (alternative)
     * @param input Image binaire
     * @param labels Image de labels (modifiée)
     * @param x Coordonnée ligne courante
     * @param y Coordonnée colonne courante
     * @param label Label à affecter
     * @param connectivity Connectivité (4 ou 8)
     *
     * Version récursive (DFS). Attention à la taille de la pile
     * pour les grandes composantes !
     */
    static void dfs(const Image& input, LabelImage& labels,
                   int x, int y, int label, int connectivity);
};

#endif // PRIM_H
