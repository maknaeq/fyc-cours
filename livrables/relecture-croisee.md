# Relecture croisée des chapitres 00 à 02

Livrable de l'issue FYC-62 (annexe), échéance 1er décembre 2026, avant le dépôt du
50 % sur Teams (séance 3, 2 décembre). Ce fichier répartit la relecture, donne la
liste de contrôle et garde la trace de ce qui a été relu.

## Pourquoi maintenant

La règle 2 de `charte/regles-redaction.md` demande qu'un membre relise et valide
tout texte rédigé avec l'IA **avant** son merge sur `main`. Pour tenir le rythme
des 50 %, plusieurs PR du chapitre 00 et du chapitre 01 ont été mergées après
une lecture rapide, case « Relu par un humain » non cochée, avec une relecture de
fond reportée à ce jalon. Cette relecture est donc le moment où la règle est
tenue : elle précède le dépôt sur Teams, pas l'inverse.

## Périmètre et répartition

Personne ne relit ce qu'il a écrit ou fait écrire. Les tailles sont les
caractères des fichiers, README compris, à titre d'ordre de grandeur
(`scripts/stats.sh` en compte moins) ; une page fait 4 000 signes.

| Lot | Contenu | Taille (pages) | Auteur | Relecteur |
|---|---|---|---|---|
| A | Chapitre 00 : accueil, positionnement, README | 19415 (4,9) | Quentin | Kaan |
| B | Chapitre 00 : script de la vidéo de présentation (tournée) | 5430 (1,4) | Quentin | Kaan |
| C | Chapitre 01 : support, exercices, QCM, README | 52329 (13.1) | Quentin, Kaan | Timothé |
| D | Chapitre 01 : trois scripts vidéo | 17065 (4,3) | Quentin | Kaan |
| E | Chapitre 01 : TP S1.3, étude de cas S1.2 (dépôts `xKaan/fyc-tp`) | dépôts | Kaan | Erwin |
| F | Chapitre 01 : dépôts d'exemple Laravel et Spring (`sorantino/notion-lite-*`) | dépôts | Timothé | Erwin |
| G | Chapitre 02 : fil rouge et support S2.1 (PR en cours) | 8059 (2,0) + PR | Timothé | Quentin |
| H | Chapitre 00 : guide d'installation (00.3) | à écrire | Erwin | Timothé |

Pourquoi ces choix : Erwin relit les dépôts parce qu'il peut les lancer (Docker,
Ollama) : c'est la seule façon de confirmer les valeurs que la vidéo du timeout
réel affiche (erreur 500 à 30 s, `cURL error 28`, erreur 504 à 20 s, deux
processus actifs à 24 s). Timothé prend le plus gros lot de texte parce qu'il n'a
écrit aucune ligne du support du chapitre 01. Le lot H n'existe pas encore : le
guide est dû le 30 novembre (FYC-97).

Les lots changent avec ce qui est mergé avant le 1er décembre : tout nouveau
support du 50 % s'ajoute à cette table avec son relecteur.

## Liste de contrôle

À copier dans la review de la PR ou dans le commentaire Linear de FYC-62.

**Pour tout texte**

- [ ] `scripts/lint.sh` et `scripts/build.sh <chapitre>` passent.
- [ ] Chaque affirmation technique vérifiable a une source dans
      `livrables/bibliographie.md` ou un lien en ligne qui s'ouvre. Les versions
      ont été revérifiées (Laravel, PHP, Ollama).
- [ ] Une affirmation absolue sur un comportement qui dépend du fournisseur
      (facturation, quotas, délais) est nuancée.
- [ ] Le texte tient ce qu'il promet : un renvoi vers une section, un dépôt, une
      vidéo ou un corrigé qui existe.
- [ ] Les durées et les objectifs sont ceux de `livrables/scenarisation.md`.
- [ ] Le texte se lit seul : un apprenant qui connaît PHP et Laravel, mais pas
      l'IA, le comprend sans avoir suivi la conversation d'équipe.

**Support écrit**

- [ ] Chaque section a son mini-exercice et sa réponse juste après.
- [ ] Le code PHP est celui du dépôt du TP (même noms de classes et de méthodes).
- [ ] Une section qui répète ce qu'une autre dit est coupée ou renvoie à l'autre.

**QCM et exercices**

- [ ] Une seule bonne réponse, sans indice de longueur ou de formulation.
- [ ] Chaque option a son explication.
- [ ] Le corrigé de l'exercice dit comment vérifier sa propre réponse.

**TP et dépôts**

- [ ] Le dépôt se clone et se lance en suivant le seul énoncé.
- [ ] Les tests annoncés passent (nombre et nom).
- [ ] Un résultat d'essai cité dans un énoncé ou une vidéo a été observé, pas
      déduit.

**Script vidéo**

- [ ] La voix tient dans la durée à 140 mots par minute.
- [ ] La ligne « Place dans le parcours » est exacte.
- [ ] Le ton est celui d'une personne qui parle à une autre : lu à voix haute, on
      ne bute sur aucune phrase.

## Points ouverts à trancher à la relecture

Ils sont aussi listés dans les corps de PR (« À relire en priorité »).

- **Budget de signes du chapitre 01** : `cours.md` pèse 32 100 signes contre 24 800
  avant la refonte pédagogique ; le chapitre fait 11,4 pages sur les ~30 du cours,
  avec quatre chapitres à écrire. Garder, ou couper (encarts CQRS et Spring,
  explications de QCM).
- **Durée de lecture de S1.1** : prévue 24 min, probablement 30 avec les quatre
  mini-exercices. À chronométrer.
- **Promesses de la page d'accueil** (`accueil.md`) : un dépôt de départ et un
  corrigé pour chaque TP, un mini-exercice par section, le fil rouge dès la
  séance 2. Elles ne sont tenues aujourd'hui que pour le chapitre 01.
- **Nom du fil rouge** : « Notion Lite » dans les dépôts d'exemple, « NoteFlow »
  dans la page d'accueil et la suite des TP. Un seul nom à choisir.
- **Test de positionnement** : distracteurs faibles aux questions 4, 9 et 10 ;
  explications par option absentes aux questions 1 à 10.
- **Ton des scripts vidéo** : jugé trop peu parlé (FYC-127). À régler après le
  premier tournage.

## Suivi

À remplir par chaque relecteur. « Corrections » renvoie à la PR qui les applique.

| Lot | Relecteur | Date | Verdict | Corrections |
|---|---|---|---|---|
| A | Kaan | | | |
| B | Kaan | | | |
| C | Timothé | | | |
| D | Kaan | | | |
| E | Erwin | | | |
| F | Erwin | | | |
| G | Quentin | | | |
| H | Timothé | | | |
