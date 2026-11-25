# Contexte pour Claude : projet FYC

Ce dépôt contient un cours en ligne rédigé par un groupe d'étudiants (projet
FYC, ESGI / Sciences-U Lyon). Le contenu est en français.

## Rôle attendu de Claude

- Structurer, rédiger, relire, reformuler, vérifier la cohérence et exporter.
- Le groupe travaille avec l'IA en aller-retour : elle propose, structure,
  rédige et relit, et chaque contenu est vérifié et validé par un membre du
  groupe avant merge (la PR le signale). Ce n'est pas une génération
  automatique au sens du règlement FYC. Décision du 08/09/2026, confirmée le
  24/11/2026.
- Les schémas doivent être construits par l'équipe. Tu peux proposer une
  structure de schéma (mermaid, texte) que l'équipe redessine.

## Règles de rédaction

Tout texte publié ou affiché respecte `charte/regles-redaction.md` et
`charte/guide-de-style.md` (déroulé d'une section, format des exercices et
QCM). Pour écrire ou relire du contenu de cours, utiliser la skill `prof` :
elle donne le niveau attendu et les fiches de sources vérifiées par thème. Ce fichier
est la source unique des règles, à lire avant d'écrire. Résumé des règles
vérifiées par le lint :

- Pas de tiret long (U+2014, « em dash »). Utiliser « : », une virgule ou une nouvelle phrase.

`scripts/lint.sh` tourne automatiquement après chaque écriture de fichier
Markdown (hook dans `.claude/settings.json`) et bloque en cas de violation.

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
- `/script-video <fichier.md>` : écrit ou réécrit un script de vidéo en langage parlé,
  avec minutage et plan de montage.
- `prof` : l'enseignant référent du cours. À charger pour rédiger, relire ou
  vérifier un support, un exercice, un QCM ou un script vidéo.
- `/ship <FYC-nn>` : lit l'issue Linear et son contexte, fait le travail dans
  une branche, vérifie lint et export, ouvre la PR, passe l'issue en In Review.
- `/audit-plan [jalon]` : compare la scénarisation et les livrables FYC à
  Linear, liste les ressources sans issue, les issues périmées et sans échéance.

## Linear suit le plan

`livrables/scenarisation.md` est la source du découpage. Linear doit la suivre :

- Une sous-issue par ressource de la colonne « Ressources nécessaires », sous
  l'issue du chapitre. Titre : `NN · Sx.y · …` (ou `NN · Vidéo · …`,
  `Teams · …`, `Avancement · …`, `Évaluation · …` pour le transversal).
- Une PR qui modifie `livrables/scenarisation.md` liste dans sa description
  les issues créées, modifiées ou fermées en conséquence.
- Les deux prochains jalons sont toujours découpés, avec responsable et
  échéance. `/audit-plan` le vérifie, `/retour-mentor` le lance.
