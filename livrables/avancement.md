---
title: "Document d'avancement"
subtitle: "Projet FYC 2026-2027"
author: "Quentin Bauduin, Timothé Geoffroy, Kaan Topkaya, Erwin Gossin"
---

<!--
Format demandé par le mentor après la séance 1 : échéances, tâches réellement
terminées, blocages rencontrés, liens ou captures montrant l'avancement concret.
Une section par séance. La V1 (séance 1) est dans
livrables/archives/2026-07-08-avancement-s1.pdf.
-->

# Organisation

## Rôles

Répartition revue le 08/09/2026 après la décision d'un parcours unique Laravel
(FYC-13). Répartition initiale de la séance 1 en archive.

| Membre | Rôle | Périmètre |
|--------|------|-----------|
| Quentin Bauduin | Chef de projet, contenu transversal | Scénarisation, supports écrits communs, vidéos, suivi Linear, document d'avancement |
| Kaan Topkaya | TP Laravel | Briques de code, squelettes et corrigés des TP, dépôts de départ, bibliographie technique |
| Timothé Geoffroy | Fil rouge et comparaisons | Application fil rouge (type Notion avec agents), extraits Spring AI des comparaisons, publications scientifiques |
| Erwin Gossin | Environnement et infrastructure | Guide d'installation, Ollama, pgvector, Docker, CI, ressources par séquence |

## Outils de suivi

- Dépôt GitHub : https://github.com/maknaeq/fyc-cours
- Suivi des tâches : Linear, [projet FYC](https://linear.app/fyc/project/fyc-cours-ia-and-architecture-web-838bc16885f9)
- Documents : ce dépôt (`livrables/`, `cours/`)

# Séance 2 : 09/09/2026

**Attendu :** scénarisation finale, vidéo de présentation, bibliographie, 20 % des supports.

## Tâches terminées depuis la séance 1

| Tâche | Responsable | Terminé le | Preuve (lien, commit, capture) |
|-------|-------------|------------|--------------------------------|
| Mise en place du dépôt GitHub et du workflow | Quentin Bauduin | 08/09/2026 | https://github.com/maknaeq/fyc-cours |
| Mise en place du suivi Linear (jalons, 21 issues) | Quentin Bauduin | 08/09/2026 | https://linear.app/fyc/project/fyc-cours-ia-and-architecture-web-838bc16885f9 |
| Intégration des retours mentor S1 en actions | Quentin Bauduin | 08/09/2026 | `retours-mentor/2026-07-08-seance-1.md` |
| Titre du cours et problématique rédigée (FYC-11) | Quentin Bauduin | 08/09/2026 | https://github.com/maknaeq/fyc-cours/pull/1 |
| Charte d'export des documents (FYC-23, base) | Quentin Bauduin | 08/09/2026 | https://github.com/maknaeq/fyc-cours/pull/2 |
| Activités synchrones remplacées par des activités autonomes (FYC-14) | Quentin Bauduin | 08/09/2026 | https://github.com/maknaeq/fyc-cours/pull/3 |
| Parcours unique Laravel, TP sans SDK (FYC-13) | Groupe, proposition de Kaan | 08/09/2026 | https://github.com/maknaeq/fyc-cours/pull/4 |
| Règles de rédaction et lint automatique | Quentin Bauduin | 08/09/2026 | `charte/regles-redaction.md` |
| Sous-issues du 20 % créées et réparties (FYC-26 à FYC-30) | Quentin Bauduin | 08/09/2026 | https://linear.app/fyc/project/fyc-cours-ia-and-architecture-web-838bc16885f9 |

## Tâches en cours

| Tâche | Responsable | Échéance | Avancement |
|-------|-------------|----------|------------|
| Scénarisation finale : périmètre, durée S3, ressources, vue d'ensemble (FYC-15, 16, 17, 12) | Quentin Bauduin | 09/09/2026 | Rédigé, en relecture : https://github.com/maknaeq/fyc-cours/pull/5 |
| Support écrit S1.1 et S1.2, exercice et QCM corrigés (FYC-26) | Quentin Bauduin | 09/09/2026 | Rédigé, en relecture : https://github.com/maknaeq/fyc-cours/pull/6 |
| Vidéo de présentation et pré-requis (FYC-30) | Quentin Bauduin | 09/09/2026 | Scripts rédigés (https://github.com/maknaeq/fyc-cours/pull/7), tournage à faire |
| Dépôt de départ du TP S1.4 (FYC-27) | Kaan Topkaya | 09/09/2026 | À faire |
| Cas fil rouge, app type Notion avec agents (FYC-28) | Timothé Geoffroy | 09/09/2026 | À faire |
| Guide d'installation de l'environnement (FYC-29) | Erwin Gossin | 09/09/2026 | À faire |
| Bibliographie aux normes (FYC-19) | Kaan Topkaya | 09/09/2026 | Structure en place, champs à compléter |
| Publications scientifiques (FYC-20) | Timothé Geoffroy | 09/09/2026 | À faire |
| Charte graphique définitive, logos, page de garde (FYC-23) | Erwin Gossin | 02/12/2026 | Base posée et mergée (PR #2), reste les logos |

## Blocages rencontrés

| Blocage | Impact | Résolution / décision |
|---------|--------|-----------------------|
| Deux parcours Spring et Laravel : trop large pour 15 h et activités de groupe impossibles sur Moodle | Scénarisation à revoir en profondeur | Parcours unique Laravel, TP sans SDK, Spring AI en comparaison lue (FYC-13, FYC-14) |
| Rôle « parcours Spring » sans objet après cette décision | Répartition à refaire | Timothé prend le fil rouge et les comparaisons (tableau des rôles ci-dessus) |

## Prochaines échéances

| Tâche | Responsable | Échéance |
|-------|-------------|----------|
| Dépôt de la scénarisation finale sur Teams | Quentin Bauduin | 09/09/2026 avant la séance |
| Release GitHub `seance-2` avec tous les docx | Quentin Bauduin | 09/09/2026 |
| Chapitres 00, 01 et 02 complets sur Moodle (50 %) | Groupe | 02/12/2026 |
| Chapitres 03, 04 et 05, cas pratique, test final (100 %) | Groupe | 06/01/2027 |

# Séance 1 : 08/07/2026

Voir `livrables/archives/2026-07-08-avancement-s1.pdf`. Backlog prévisionnel
(toutes les tâches « à faire »). Retour du mentor : ajouter échéances, statuts
réels, blocages et preuves d'avancement.
