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

## Organisation et suivi

- Gestion de projet : un jalon par séance avec le mentor, une tâche par
  chapitre et par livrable, chaque tâche assignée à un responsable avec une
  échéance.
- Suivi des tâches : Linear, [projet FYC](https://linear.app/fyc/project/fyc-cours-ia-and-architecture-web-838bc16885f9).
  L'avancement du projet y est calculé sur la durée apprenant des chapitres
  terminés.
- Chaque document et chaque support est relu par un autre membre du groupe
  avant d'être considéré comme terminé.

# Séance 2 : 09/09/2026

**Attendu :** scénarisation finale, vidéo de présentation, bibliographie, 20 % des supports.

## Tâches terminées depuis la séance 1

| Tâche | Responsable | Terminé le | Preuve (lien, commit, capture) |
|-------|-------------|------------|--------------------------------|
| Mise en place de la gestion de projet et du suivi dans Linear (jalons, rôles, 21 tâches) | Quentin Bauduin | 08/09/2026 | https://linear.app/fyc/project/fyc-cours-ia-and-architecture-web-838bc16885f9 |
| Intégration des retours mentor S1 en actions suivies | Quentin Bauduin | 08/09/2026 | Tâches étiquetées « retour-mentor » dans Linear |
| Titre du cours et problématique rédigée (FYC-11) | Quentin Bauduin | 08/09/2026 | https://github.com/maknaeq/fyc-cours/pull/1 |
| Charte de mise en forme commune à tous les documents rendus | Quentin Bauduin | 08/09/2026 | Ce document |
| Activités synchrones remplacées par des activités autonomes (FYC-14) | Quentin Bauduin | 08/09/2026 | https://github.com/maknaeq/fyc-cours/pull/3 |
| Parcours unique Laravel, TP sans SDK (FYC-13) | Groupe, proposition de Kaan | 08/09/2026 | https://github.com/maknaeq/fyc-cours/pull/4 |
| Sous-issues du 20 % créées et réparties (FYC-26 à FYC-30) | Quentin Bauduin | 08/09/2026 | https://linear.app/fyc/project/fyc-cours-ia-and-architecture-web-838bc16885f9 |

## Tâches en cours au 09/09/2026

| Tâche | Responsable | Échéance | Avancement |
|-------|-------------|----------|------------|
| Scénarisation finale : périmètre, durée S3, ressources, vue d'ensemble (FYC-15, 16, 17, 12) | Quentin Bauduin | 09/09/2026 | Terminé, mergé |
| Support écrit S1.1 et S1.2, exercice et QCM corrigés (FYC-26) | Quentin Bauduin | 09/09/2026 | Terminé, mergé |
| Dépôt de départ du TP S1.4 (FYC-27) | Kaan Topkaya | 09/09/2026 | Terminé, dépôt public lié depuis le chapitre 01 |
| Cas fil rouge, app type Notion avec agents (FYC-28) | Timothé Geoffroy | 09/09/2026 | Terminé |
| Bibliographie aux normes (FYC-19) | Kaan Topkaya | 09/09/2026 | Terminé, chaque entrée vérifiée à la source |
| Publications scientifiques (FYC-20) | Timothé Geoffroy | 09/09/2026 | Terminé, 4 catégories ajoutées |
| Vidéo de présentation du cours, de l'équipe et des pré-requis (FYC-30) | Quentin Bauduin | 13/09/2026 | Tournée le 09/09, à refaire après le retour du mentor |
| Guide d'installation de l'environnement (FYC-29) | Erwin Gossin | 13/09/2026 | En cours |
| Charte graphique définitive, logos, page de garde (FYC-23) | Erwin Gossin | 02/12/2026 | Base mergée (PR #2), reste les logos |

## Blocages rencontrés

| Blocage | Impact | Résolution / décision |
|---------|--------|-----------------------|
| Deux parcours Spring et Laravel : trop large pour 15 h et activités de groupe impossibles sur Moodle | Scénarisation à revoir en profondeur | Parcours unique Laravel, TP sans SDK, Spring AI en comparaison lue (FYC-13, FYC-14) |
| Rôle « parcours Spring » sans objet après cette décision | Répartition à refaire | Timothé prend le fil rouge et les comparaisons (tableau des rôles ci-dessus) |
| Vidéo de présentation montrée en séance sans montage | Le mentor n'a vu que le rush et l'a jugé ennuyeux | Script réécrit avec accroche, nouvelle prise et montage avant le 13/09 (FYC-31, FYC-30) |

## Retours de la séance 2 et suite

Compte-rendu complet : `retours-mentor/2026-09-09-seance-2.md`. Quatre retours,
transformés en tâches Linear le 12/09/2026 (FYC-31 à FYC-36).

| Retour du mentor | Action | Responsable | Échéance |
|------------------|--------|-------------|----------|
| La vidéo de présentation doit donner envie, pas ouvrir sur « Bonjour » | Script réécrit : accroche, cible nommée, valeur montrée (FYC-31), puis nouvelle prise et montage (FYC-30) | Quentin Bauduin | 13/09/2026 |
| Le TP 1 n'a pas de consignes écrites | Fiche apprenant pas à pas : étapes numérotées, résultat attendu, critères de réussite, corrigé (FYC-32) | Kaan Topkaya | 13/09/2026 |
| Renvoyer vers des ressources externes là où une notion extérieure est manipulée | Rubrique « Ressources » normalisée dans le modèle de chapitre (FYC-33), chapitres 00 et 01 complétés (FYC-34), renvois en ligne dans les TP (FYC-35) | Quentin Bauduin, Kaan Topkaya | 02/12/2026 |
| Piste bonus : une vidéo de live coding par TP | Tâche ouverte en réserve, conditionnée à un cours complet et à la place restante dans l'enveloppe vidéo (FYC-36) | Groupe | non planifié |

## Rendu du week-end du 12 au 13/09/2026

| Livrable | Responsable | État |
|----------|-------------|------|
| Suivi Linear à jour : qui fait quoi, échéances, statuts réels | Quentin Bauduin | Fait. Export du jalon dans `livrables/suivi-linear.md` |
| Bibliographie aux normes (FYC-19, FYC-20) | Kaan Topkaya, Timothé Geoffroy | Fait |
| Vidéo de présentation montée et sous-titrée (FYC-30, FYC-31) | Quentin Bauduin | Fait le 12/09/2026 : script réécrit après le retour du mentor, nouvelle prise, montage et sous-titres. Remise directe sur Teams, pas d'hébergement public |

## Prochaines échéances

| Tâche | Responsable | Échéance |
|-------|-------------|----------|
| Rendu du week-end : suivi Linear, bibliographie, vidéo de présentation | Groupe | 13/09/2026 |
| Chapitres 00, 01 et 02 complets sur Moodle (50 %) | Groupe | 02/12/2026 |
| Chapitres 03, 04 et 05, cas pratique, test final (100 %) | Groupe | 06/01/2027 |

# Séance 1 : 08/07/2026

Voir le document d'avancement remis à la séance 1. Backlog prévisionnel
(toutes les tâches « à faire »). Retour du mentor : ajouter échéances, statuts
réels, blocages et preuves d'avancement.
