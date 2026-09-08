# Design — structure du dépôt FYC

Date : 2026-09-08. Statut : validé.

## Objectif

Donner au groupe un espace unique pour écrire le cours en Markdown, suivre les
retours du mentor, générer des docx à la charte du groupe, et alimenter Linear
avec un découpage où la somme des estimations égale la durée apprenant du cours.

## Décisions

- Dépôt GitHub public `fyc-cours` sur le compte maknaeq. Public car autorisé
  par le règlement FYC et requis pour rester accessible 5 ans. Renommé quand
  le sujet est fixé.
- Contenu en Markdown, un dossier par chapitre avec des fichiers à rôle fixe
  (cours, exercices, qcm, videos, assets). Un fichier par vidéo.
- Export docx par pandoc avec `charte/reference.docx` comme porteur de la
  charte graphique. Un script `scripts/build.sh` exporte tout ou une cible.
- `scripts/stats.sh` mesure les signes (cible 30 pages de 4 000 signes) et
  la durée apprenant déclarée par chapitre (cible 10 à 15 h).
- `CLAUDE.md` à la racine plus deux skills projet (`/chapitre`, `/retour-mentor`)
  pour que chaque coéquipier utilisant Claude Code ait le même contexte.
- Suivi dans Linear : un jalon par séance, une issue par chapitre ou livrable,
  estimation en heures apprenant. Le connecteur n'était pas disponible dans la
  session de création ; à brancher ensuite.

## Hors périmètre

- Le contenu du cours lui-même.
- La charte graphique (police, couleurs) : à définir par le groupe puis
  reportée dans `reference.docx` et `charte/guide-de-style.md`.
- L'export vers Moodle : dépôt manuel des docx/vidéos.
