---
name: audit-plan
description: Compare la scénarisation finale et les livrables obligatoires FYC au projet Linear, et liste les trous (ressource prévue sans issue, description périmée, issue sans échéance ou au statut dépassé). Lecture seule, propose les corrections sans les appliquer. Usage : /audit-plan [jalon]
---

# Audit : Linear suit-il le plan du cours ?

Argument optionnel : un jalon (`S3`, `S4`, `fermeture`). Sans argument, auditer
les deux prochains jalons à partir de la date du jour.

Pourquoi cette skill existe : le 02/11/2026, le backlog ne contenait que
9 issues ouvertes pour toute la suite du projet, avec des descriptions de
chapitre restées à la V1 alors que la scénarisation avait changé à la séance 2.
Personne ne comparait le plan à Linear. Cette skill fait cette comparaison.

## 1. Lire les sources

1. `livrables/scenarisation.md` : le tableau « Plan du cours » (séquence, durée)
   et, dans « Détails des séquences », la colonne « Ressources nécessaires » de
   chaque étape. C'est la source de vérité.
2. `CLAUDE.md` et `README.md` : livrables obligatoires FYC (au moins 1 exercice
   par chapitre, 2 exercices non-QCM, 1 cas pratique, 1 test de
   positionnement, 1 test final de ~40 QCM, vidéo ~1 h 30, 8 min max par vidéo).
3. Linear, projet FYC : `list_milestones` (jalons, dates, descriptions) puis
   `list_issues` du projet avec titre, description, statut, jalon, assigné,
   échéance, parent.
4. L'état réel du dépôt : `scripts/stats.sh` et le contenu de `cours/*/`.

## 2. Contrôles

Pour chaque jalon audité, produire trois listes.

**A. Prévu dans le plan, sans issue.**
- Chaque séquence `Sx.y` du jalon a au moins une issue dont le titre contient
  `Sx.y`.
- Chaque ressource de la colonne « Ressources nécessaires » est couverte par
  une issue (titre ou description). Une ressource déjà présente dans le dépôt
  compte comme couverte si une issue Done la mentionne.
- Chaque livrable obligatoire FYC a une issue (test final, cas pratique,
  test de positionnement, budget vidéo).
- Les attendus écrits dans la description du jalon Linear (ex. « dépôt sur
  Moodle », « V0 du support de soutenance ») ont une issue.

**B. Issue qui ne correspond plus au plan.**
- Durées, séquences ou choix (parcours, format) d'une description différents de
  la scénarisation finale.
- Issue qui renvoie à une décision annulée (ex. « deux parcours »).

**C. Hygiène.**
- Issue ouverte sans échéance ou sans assigné.
- Issue ouverte dans un jalon dont la date est passée.
- Issue « In Progress » sans mise à jour depuis plus de 3 semaines.
- Titre de contenu qui ne suit pas la convention `NN · Sx.y · …` (ou
  `NN · Vidéo · …`, `Moodle · …`, `Avancement · …`, `Évaluation · …`).
  Exceptions : les issues parentes de chapitre (FYC-5 à FYC-10) et les issues
  étiquetées `retour-mentor`.
- Exception à l'échéance : une issue en réserve sans jalon (ex. bonus live
  coding) n'a pas besoin d'échéance.

## 3. Restituer

Un tableau par liste : élément, source (ligne de la scénarisation ou jalon),
issue concernée ou « aucune », correction proposée (titre d'issue, assigné
selon les rôles de `livrables/avancement.md`, échéance).

Terminer par un compte : N trous, N issues périmées, N problèmes d'hygiène.

## 4. Corriger

Ne rien créer ni modifier sans confirmation. Après accord, créer ou mettre à
jour les issues dans Linear avec la convention de titre, puis relancer les
contrôles A à C pour vérifier qu'il ne reste rien.
