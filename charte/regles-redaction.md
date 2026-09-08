# Règles de rédaction

Règles qui s'appliquent à tout texte publié ou affiché : contenu du cours,
livrables, scripts vidéo, QCM, exercices, textes Moodle. Elles s'appliquent
aussi bien aux humains qu'à Claude.

Ce fichier est chargé automatiquement par Claude dans chaque session (via
`CLAUDE.md`). Les règles marquées **[lint]** sont vérifiées mécaniquement par
`scripts/lint.sh`, lancé après chaque écriture de fichier et avant chaque PR.

Pour ajouter une règle : une ligne ici, et si elle est vérifiable, un bloc
dans `scripts/lint.sh`.

## Typographie

1. **[lint] Pas de tiret long (U+2014, dit « em dash ») dans le texte.** Remplacer par deux
   points, une virgule, des parenthèses ou une nouvelle phrase. Dans un titre
   composé, utiliser « : » (ex. `S1.1 : Architectures web`).

## Relecture

2. Tout texte rédigé par Claude est relu par un membre du groupe avant d'être
   mergé sur `main`. La PR ouverte par `/ship` reste en review tant qu'un
   humain ne l'a pas approuvée.
