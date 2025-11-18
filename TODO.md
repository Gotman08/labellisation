# TODO - Checklist du Projet

Ce fichier récapitule ce qui a été fait et ce qu'il reste à compléter.

## ✅ Déjà implémenté

### Code source
- [x] Structure de base (Image, LabelImage, Pixel)
- [x] Lecture/écriture PGM/PPM (from scratch)
- [x] Fonctions utilitaires (min/max/mean manuels)
- [x] Algorithme Two-Pass
- [x] Algorithme Union-Find
- [x] Algorithme Kruskal
- [x] Algorithme Prim
- [x] Programme principal (CLI)
- [x] Tests unitaires
- [x] Système de benchmark

### Documentation
- [x] README.md principal
- [x] USAGE.md (guide d'utilisation)
- [x] Rapport LaTeX (rapport.tex)
- [x] Rapport Markdown (RAPPORT.md)
- [x] Présentation LaTeX (presentation.tex)
- [x] Présentation Markdown (PRESENTATION.md)
- [x] Documentation du dossier docs/

### Configuration
- [x] CMakeLists.txt
- [x] .gitignore
- [x] Structure de dossiers

## 📝 À compléter par vous

### 1. Images de test (PRIORITAIRE)

**Où :** `images/input/`

**À faire :**
- [ ] Ajouter au moins 3-4 images de test au format PGM
- [ ] Varier les tailles (petite, moyenne, grande)
- [ ] Inclure différents cas :
  - Image simple (peu de composantes)
  - Image complexe (beaucoup de composantes)
  - Image avec diagonales (pour tester 4-conn vs 8-conn)

**Comment créer des images PGM :**
```bash
# Convertir depuis PNG/JPG
convert input.jpg -colorspace Gray output.pgm

# Ou créer manuellement (format texte)
# Voir USAGE.md pour un exemple
```

### 2. Compilation et tests

**À faire :**
- [ ] Compiler le projet
  ```bash
  mkdir build && cd build
  cmake ..
  cmake --build .
  ```
- [ ] Vérifier que la compilation réussit sans erreur
- [ ] Exécuter les tests unitaires
  ```bash
  ./test_algorithms
  ```
- [ ] Vérifier que tous les tests passent

### 3. Benchmarks

**À faire :**
- [ ] Exécuter le benchmark sur vos images
  ```bash
  ./benchmark ../images/input/*.pgm
  ```
- [ ] Noter les résultats :
  - Temps moyen pour chaque algorithme
  - Écart-type
  - Nombre de composantes trouvées
- [ ] Tester avec différentes tailles d'images
- [ ] Tester avec 4-connexité et 8-connexité

### 4. Rapport (À RENDRE LE 1ER DÉCEMBRE)

**Où :** `docs/rapport/rapport.tex` ou `docs/rapport/RAPPORT.md`

**À compléter :**
- [ ] **Page de garde** : Remplacer "Étudiant 1, 2, 3" par vos vrais noms
- [ ] **Configuration de test** :
  - Processeur (CPU)
  - RAM
  - Système d'exploitation
- [ ] **Tableaux de résultats** : Remplacer les "XX.XX" par vos vrais résultats de benchmark
- [ ] **Analyse** : Commenter vos résultats
  - Quel algorithme est le plus rapide ?
  - Pourquoi ?
  - Les résultats correspondent-ils à la théorie ?
- [ ] **Répartition du travail** : Qui a fait quoi ?
  - Étudiant 1 : ...
  - Étudiant 2 : ...
  - Étudiant 3 : ...
- [ ] **Images/graphiques** (optionnel mais recommandé) :
  - Exemple d'image labellisée
  - Graphique de comparaison des performances
- [ ] **Compiler le PDF** :
  ```bash
  cd docs/rapport
  pdflatex rapport.tex
  pdflatex rapport.tex
  ```

### 5. Présentation (POUR LE 9 DÉCEMBRE)

**Où :** `docs/presentation/presentation.tex` ou `docs/presentation/PRESENTATION.md`

**À faire :**
- [ ] **Page de titre** : Vos noms
- [ ] **Compléter les résultats** : Remplacer les "XX.XX" par vos résultats
- [ ] **Préparer une démo** :
  - Montrer le programme en action
  - Préparer une commande qui fonctionne
  - Avoir une image de résultat à montrer
- [ ] **Répartir les rôles** (15 min = 5 min/personne) :
  - Personne 1 : Introduction + Théorie (5 min)
  - Personne 2 : Les 4 algorithmes (5 min)
  - Personne 3 : Résultats + Conclusion (5 min)
- [ ] **S'entraîner** :
  - Chronométrer la présentation
  - Vérifier le timing
  - Préparer les réponses aux questions possibles
- [ ] **Compiler les slides** (si LaTeX) :
  ```bash
  cd docs/presentation
  pdflatex presentation.tex
  pdflatex presentation.tex
  ```

### 6. Questions fréquentes à préparer

**Questions possibles du jury :**

- [ ] "Pourquoi Two-Pass est-il généralement plus rapide ?"
  - **Réponse suggérée** : Meilleure localité cache (parcours séquentiel)

- [ ] "Quelle est la différence entre 4-connexité et 8-connexité ?"
  - **Réponse** : Voir section théorique (adjacence forte vs faible)

- [ ] "Qu'est-ce que le paradoxe de Jordan ?"
  - **Réponse** : Voir rapport section théorique

- [ ] "Quelle est la complexité de Union-Find ?"
  - **Réponse** : O(N·α(N)) ≈ O(N) où α < 5

- [ ] "Pourquoi avez-vous tout codé from scratch ?"
  - **Réponse** : Pour comprendre les mécanismes en profondeur + contrainte du projet

- [ ] "Pouvez-vous montrer une démo ?"
  - **Préparation** : Avoir une commande prête et une image de résultat

### 7. Git et versioning (optionnel)

**Si vous utilisez Git :**
- [ ] Faire des commits réguliers
- [ ] Ajouter les fichiers au dépôt :
  ```bash
  git add .
  git commit -m "Ajout des images de test"
  git commit -m "Complétion du rapport avec résultats"
  git commit -m "Préparation de la présentation"
  ```
- [ ] Pousser sur GitHub/GitLab (si applicable)

## 🎯 Checklist finale (avant remise)

### Rapport (1er décembre)
- [ ] Tous les noms sont corrects
- [ ] Tous les tableaux sont remplis
- [ ] Toutes les sections "À compléter" sont complétées
- [ ] Le PDF compile sans erreur
- [ ] La pagination est correcte
- [ ] Les références sont présentes
- [ ] Le fichier PDF est nommé correctement (selon consignes)

### Présentation (9 décembre)
- [ ] Les slides sont prêtes
- [ ] Le timing est respecté (15 min)
- [ ] La démo fonctionne
- [ ] Tout le monde sait ce qu'il doit présenter
- [ ] Les réponses aux questions sont préparées
- [ ] Le PDF/fichier de présentation est prêt

### Code
- [ ] Le code compile sans warning
- [ ] Tous les tests passent
- [ ] Les benchmarks fonctionnent
- [ ] Le README est à jour

## 📊 Ordre recommandé des tâches

### Semaine 1 (priorité haute)
1. Compiler le projet
2. Ajouter des images de test
3. Exécuter les benchmarks
4. Noter les résultats

### Semaine 2 (priorité moyenne)
5. Compléter le rapport avec les résultats
6. Compiler le PDF du rapport
7. Vérifier que tout est correct

### Semaine 3 (avant présentation)
8. Préparer les slides de présentation
9. S'entraîner à présenter
10. Préparer la démo

## 💡 Conseils

### Pour le rapport
- Ne pas attendre la dernière minute pour compiler LaTeX
- Vérifier la compilation régulièrement
- Faire relire par les autres membres du groupe
- Ajouter des captures d'écran si possible

### Pour la présentation
- Répéter plusieurs fois
- Chronométrer
- Ne pas mettre trop de texte sur les slides
- Avoir un plan B si la démo échoue (capture d'écran)
- Arriver en avance le jour J

### Pour le code
- Tester sur plusieurs images différentes
- Vérifier que les 4 algorithmes donnent le même résultat
- Noter les cas particuliers dans le rapport

## ❓ En cas de problème

### Le code ne compile pas
1. Vérifier la version de CMake (`cmake --version`)
2. Vérifier le compilateur C++17 (`g++ --version`)
3. Supprimer le dossier `build/` et recommencer
4. Consulter les messages d'erreur

### Les tests échouent
1. Vérifier les chemins d'images
2. Vérifier le format des images (PGM)
3. Consulter les messages d'erreur dans les tests

### LaTeX ne compile pas
1. Vérifier que tous les packages sont installés
2. Lire le fichier `.log` pour voir l'erreur
3. Essayer de compiler ligne par ligne
4. Utiliser Overleaf en ligne si nécessaire

### Les benchmarks sont bizarres
1. Compiler en mode Release : `cmake -DCMAKE_BUILD_TYPE=Release ..`
2. Fermer les autres applications
3. Exécuter plusieurs fois pour moyenner
4. Vérifier que les 4 algorithmes trouvent le même nombre de composantes

## 🎓 Bon courage !

Vous avez tout le code nécessaire, il ne reste plus qu'à :
1. Ajouter vos images
2. Exécuter les tests
3. Compléter la documentation
4. Préparer la présentation

**Le plus gros du travail est déjà fait !** 🎉
