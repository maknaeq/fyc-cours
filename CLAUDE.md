# Contexte pour Claude — projet FYC

Ce dépôt contient un cours en ligne rédigé par un groupe d'étudiants (projet
FYC, ESGI / Sciences-U Lyon). Le contenu est en français.

## Rôle attendu de Claude

- Aider à structurer, relire, reformuler, vérifier la cohérence et exporter.
- **Ne jamais rédiger le fond du cours à la place des auteurs.** Le règlement
  considère la génération automatique comme de la triche (exclusion). Si on te
  demande d'écrire un chapitre entier, propose plutôt un plan, des questions
  à traiter, ou une relecture du texte existant.
- Les schémas doivent être construits par l'équipe. Tu peux proposer une
  structure de schéma (mermaid, texte) que l'équipe redessine.

## Contraintes chiffrées à respecter

Détail dans `README.md` et `ressources/presentation-projet-fyc-26-27.pdf`.

- Durée apprenant totale : 10 à 15 h. Cible du groupe : voir `livrables/scenarisation.md`.
- Écrit : ~30 pages de 4 000 signes. Vidéo : ~1 h 30, 8 min max par vidéo.
- Chaque chapitre : au moins 1 exercice. Global : au moins 2 exercices non-QCM,
  1 cas pratique, 1 test de positionnement, 1 test final (~40 QCM).

## Conventions

- Markdown avec les conventions de `charte/guide-de-style.md`.
- Chapitres dans `cours/NN-slug/` avec la structure décrite dans `README.md`.
- Bibliographie dans `livrables/bibliographie.md` aux normes de
  `ressources/normes-bibliographie.pdf`. Style : `Nom I. (année), Titre, Éditeur.`
- Compte-rendus de séance dans `retours-mentor/YYYY-MM-DD-seance-N.md`.
- Export docx : `scripts/build.sh`, mise en page via `charte/reference.docx`.

## Commandes utiles

```bash
scripts/build.sh                 # export docx de tout
scripts/build.sh cours/01-xxx    # export d'un chapitre
scripts/stats.sh                 # signes, pages équivalentes, durées par chapitre
```

## Skills projet

- `/chapitre <NN> <slug> "<Titre>"` : crée un nouveau chapitre avec les fichiers types.
- `/retour-mentor <N> <YYYY-MM-DD>` : crée le compte-rendu d'une séance.
