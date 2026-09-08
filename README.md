# FYC — Find Your Course

Dépôt de travail du projet FYC (ESGI / Sciences-U Lyon, promo 2026-2027).
Le livrable final est un cours en ligne déposé sur Moodle. Ce dépôt sert à
écrire le contenu en Markdown, à le versionner, à suivre les retours du mentor
et à générer les documents Word (docx) avec la charte graphique du groupe.

> Sujet du cours (titre V1, à reformuler) : **Architectures web boostées à l'IA** —
> comment organiser, sécuriser et tester une application web qui intègre un agent IA.
> Parcours Spring AI (Java) ou Laravel AI SDK (PHP).
> Problématique : _à formuler pour la séance 2_ (voir `livrables/problematique.md`).

## Équipe

| Nom | Prénom | Filière | Rôle |
|-----|--------|---------|------|
| Bauduin | Quentin | _à compléter_ | Chef de projet, contenu transversal |
| Geoffroy | Timothé | _à compléter_ | Parcours Spring / Java |
| Topkaya | Kaan | _à compléter_ | Parcours Laravel / PHP |
| Gossin | Erwin | _à compléter_ | Environnement & infrastructure |

## Contraintes du projet (résumé)

Source : `ressources/presentation-projet-fyc-26-27.pdf`.

- Durée apprenant : **10 à 15 h**. Minimum 1/3 écrit, 1/3 vidéo.
- Écrit : ~**30 pages** (1 page = 4 000 signes), 20 % max en illustrations/code.
  Schémas construits par nous. Reproduction citée et limitée à 15 %.
- Vidéo : ~**1 h 30** au total, **8 min max** par vidéo, **sous-titres obligatoires**.
  Vidéos imposées : équipe, présentation du cours (3 min max), pré-requis,
  2 sujets complexes, conclusion « pour aller plus loin », correction du cas pratique.
- Évaluation apprenant : test de positionnement, 1 exercice par chapitre,
  au moins 2 exercices non-QCM, 1 cas pratique avec corrigé vidéo,
  test final (~40 QCM). Corrigés pour tout.
- Bibliographie aux normes de `ressources/normes-bibliographie.pdf`.
- Pas de drive. Dépôts GitHub publics autorisés, accessibles 5 ans.
- Toute génération IA automatique est considérée comme de la triche.
  L'IA sert ici d'outillage (structure, relecture, export), pas de rédaction du fond.

## Jalons

| Date | Séance | Attendu |
|------|--------|---------|
| 8 juil. 2026 | Séance 1 | Scénarisation V0 + ébauche biblio validées |
| 9 sept. 2026 | Séance 2 | Scénarisation finale, vidéo de présentation, biblio, 20 % des supports |
| 2 déc. 2026 | Séance 3 | 50 % du contenu sur Moodle, test des QCM/exercices/vidéos |
| 6 janv. 2027 | Séance 4 | 100 % du contenu sur Moodle, V0 du support de soutenance |
| 25 janv. 2027 | Fermeture Moodle | Mise en ligne définitive |
| 3 févr. 2027 | Soutenance | 15 min présentation, 25 min Q&R |

## Organisation du dépôt

```
ressources/       Documents fournis par l'école (consigne, template, normes biblio)
cours/            Contenu du cours en Markdown, un dossier par chapitre
livrables/        Problématique, scénarisation, bibliographie, accroche, avancement, soutenance
                  archives/ : les PDF tels que rendus à chaque séance
retours-mentor/   Compte-rendu de chaque séance avec le mentor
charte/           Charte graphique : reference.docx, logos, guide de style
scripts/          Outils de build (md → docx)
build/            Sorties générées (ignoré par git)
```

Chaque chapitre dans `cours/NN-slug/` contient :

```
README.md         Fiche du chapitre : objectifs, durée apprenant, pré-requis
cours.md          Le support écrit
exercices.md      Exercices non-QCM avec corrigés
qcm.md            Questions à choix multiples avec corrigés
videos/           Scripts des vidéos (un fichier par vidéo) et sous-titres
assets/           Schémas et images construits par nous
```

## Workflow

1. Une branche par tâche (`feat/03-nom-du-chapitre`), pull request vers `main`.
2. Chaque tâche a une issue Linear. Le titre de l'issue commence par le
   numéro du chapitre. L'estimation est en **heures apprenant** : la somme
   des estimations doit égaler la durée cible du cours.
3. Le contenu s'écrit en Markdown. Les conventions sont dans `charte/guide-de-style.md`.
4. Export docx : `scripts/build.sh` (voir ci-dessous).
5. Après chaque séance, on note les retours du mentor dans `retours-mentor/`
   et on crée les issues correspondantes.

## Export docx

Prérequis : [pandoc](https://pandoc.org) (`brew install pandoc`).

```bash
scripts/build.sh                      # tout le cours et tous les livrables
scripts/build.sh cours/01-intro       # un chapitre
scripts/build.sh livrables/scenarisation.md
```

Les fichiers sortent dans `build/`. La mise en page vient de
`charte/reference.docx` : modifier ce fichier dans Word change la charte de
tous les exports.

## Suivi du projet

Le suivi se fait dans Linear (projet FYC). Un jalon par séance, une issue
par chapitre ou par livrable.
