# FYC : Find Your Course

Dépôt de travail du projet FYC (ESGI / Sciences-U Lyon, promo 2026-2027).
Le livrable final est un cours en ligne déposé sur Moodle. Ce dépôt sert à
écrire le contenu en Markdown, à le versionner, à suivre les retours du mentor
et à générer les documents Word (docx) avec la charte graphique du groupe.

> **Concevoir une application web maintenable intégrant un agent IA : architecture, tests, sécurité et mise en production.**
> Parcours Laravel (PHP), TP sans SDK d'IA. Le Laravel AI SDK et Spring AI servent de points de comparaison.
>
> Problématique : _Comment intégrer un agent IA dans une application web sans dégrader sa maintenabilité, sa testabilité, sa sécurité et sa maîtrise en production ?_
> Détail dans `livrables/problematique.md`.

## Équipe

| Nom | Prénom | Filière | Rôle |
|-----|--------|---------|------|
| Bauduin | Quentin | IW | Chef de projet, contenu transversal |
| Geoffroy | Timothé | IW | Parcours Spring / Java |
| Topkaya | Kaan | IW | Parcours Laravel / PHP |
| Gossin | Erwin | IW | Environnement & infrastructure |

## Contraintes du projet (résumé)

Source : `ressources/presentation-projet-fyc-26-27.pdf`.

- Durée apprenant : **10 à 15 h**. Minimum 1/3 écrit, 1/3 vidéo.
- Écrit : ~**30 pages** (1 page = 4 000 signes), 20 % max en illustrations/code.
  Schémas construits par nous. Reproduction citée et limitée à 15 %.
- Vidéo : ~**1 h 30** au total, **8 min max** par vidéo, **sous-titres obligatoires**.
  Vidéos imposées : cours, équipe et pré-requis (une seule vidéo, 3 min max),
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

## Rendus par jalon

Les docx ne sont pas versionnés (`build/` est ignoré). À chaque jalon, on
publie une release GitHub qui contient tous les exports, et on archive une
copie datée dans `livrables/archives/` :

```bash
scripts/release.sh seance-2 "Séance 2 : scénarisation finale, biblio, 20 % des supports"
```

La release est l'endroit centralisé des rendus. Coller son lien dans le jalon
Linear et dans les issues concernées. `livrables/archives/` garde aussi les
PDF tels que déposés sur Teams ou Moodle.

## Avec Claude Code ou Codex

Le dépôt fonctionne avec les deux. Les fichiers de contexte et les skills sont
partagés :

| | Claude Code | Codex |
|---|---|---|
| Contexte du projet | `CLAUDE.md` | `AGENTS.md` (lien vers le même fichier) |
| Skills (`/ship`, `/chapitre`, `/retour-mentor`) | `.claude/skills/` | `.agents/skills/` (lien vers le même dossier) |
| Lint après chaque écriture | hook dans `.claude/settings.json` | pas d'équivalent : installer le hook git ci-dessous |
| Linear | connecteur claude.ai | serveur MCP Linear à déclarer dans `~/.codex/config.toml` |

Après le clonage, quel que soit l'outil :

```bash
scripts/install-hooks.sh   # refuse un commit qui viole charte/regles-redaction.md
```

## Suivi du projet

Le suivi se fait dans Linear : [projet FYC](https://linear.app/fyc/project/fyc-cours-ia-and-architecture-web-838bc16885f9).

- Un jalon par séance (S2, S3, S4, fermeture Moodle, soutenance).
- Une issue par chapitre (label `chapitre`, estimation = heures apprenant,
  Linear n'accepte que des entiers : le chapitre 00 vaut 1 pour 30 min réelles).
- Une issue par action issue d'un retour du mentor (label `retour-mentor`).
- Labels `spring` / `laravel` pour les tâches propres à un parcours.
- Nomenclature complète (labels, jalons, priorités, statuts, définition de
  terminé) : [document Linear](https://linear.app/fyc/document/nomenclature-linear-comment-on-utilise-ce-projet-ef7b50633f27).
