---
name: ship
description: Prend une issue Linear (ex. FYC-12), lit tout son contexte (description, commentaires, parent, enfants, bloqueurs), fait le travail dans une branche, vérifie le lint et l'export docx, ouvre la PR GitHub et passe l'issue en In Review. Usage : /ship FYC-12
---

# Ship une issue Linear

Argument attendu : un identifiant d'issue (`FYC-12`). Sans argument, demander.

## 1. Lire le contexte

Avec le connecteur Linear :

1. `get_issue` sur l'identifiant : titre, description, labels, jalon, assigné,
   estimation, état.
2. `list_comments` sur l'issue : les commentaires peuvent contenir des
   décisions ou des précisions postérieures à la description. Ils priment.
3. Si l'issue a un `parentId` : `get_issue` du parent pour le cadre général.
4. `list_issues` avec `parentId` = cette issue : les enfants. Si un enfant n'est
   pas Done, le signaler et demander si on ship quand même la partie parent.
5. Regarder les relations `blockedBy`. Si un bloqueur n'est pas Done, s'arrêter
   et le dire.
6. Lire les fichiers du dépôt que l'issue mentionne (chemins dans la
   description ou les commentaires), plus `charte/regles-redaction.md` et
   `charte/guide-de-style.md`.

## 2. Confirmer avant d'agir

Résumer en quelques lignes : ce que demande l'issue, ce qui a été précisé en
commentaire, les fichiers qui vont changer, et ce qui reste ambigu. Attendre
le feu vert de l'utilisateur. Si un point est ambigu et change le résultat,
poser la question avant de coder.

## 3. Travailler dans une branche

1. `git status` doit être propre sur `main`. Sinon, s'arrêter.
2. `git pull` puis créer la branche avec le nom proposé par Linear
   (`gitBranchName` dans `get_issue`).
3. Passer l'issue en `In Progress` (`save_issue`, state).
4. Faire le travail. Respecter `charte/regles-redaction.md` (chargé via
   `CLAUDE.md`) et les conventions Markdown de `charte/guide-de-style.md`.
5. Ne pas toucher à ce que l'issue ne demande pas.

## 4. Vérifier

1. `scripts/lint.sh` sur les fichiers modifiés : zéro violation.
2. Si un fichier de `livrables/` ou `cours/` a changé : `scripts/build.sh`
   sur la cible pour vérifier que l'export docx passe.
3. Si un chapitre a changé : `scripts/stats.sh` et vérifier que les durées
   restent cohérentes.

## 5. Livrer

1. Commit avec un message court en français qui commence par l'identifiant :
   `FYC-12 : réécrit la vue d'ensemble`. **Exception** : si la PR ne termine
   pas l'issue (il reste des cases non cochées), ne pas mettre l'identifiant
   en tête du commit ni du titre de la PR. L'intégration GitHub de Linear
   passe l'issue en Done au merge dès qu'elle voit l'identifiant, y compris
   dans le message du commit squashé. Mettre le lien de l'issue dans le corps
   de la PR seulement.
2. `git push -u origin <branche>`.
3. Ouvrir la PR avec `gh pr create`. Titre = `FYC-12 : <titre de l'issue>`
   (sans l'identifiant si la PR ne termine pas l'issue, voir ci-dessus).
   Corps : lien vers l'issue Linear, résumé de ce qui a été fait, ce que le
   relecteur doit vérifier en priorité, et une case à cocher « Relu par un
   humain » (règle 2 de `charte/regles-redaction.md`).
4. Passer l'issue en `In Review` et ajouter un commentaire Linear avec le lien
   de la PR (`save_comment`).
5. Cocher dans la description de l'issue les cases `- [ ]` réellement
   terminées (`save_issue` avec `patch`).

## 6. Rendre compte

Dire à l'utilisateur : lien PR, lien issue, ce qui a été fait, ce qui reste à
relire, et tout point laissé de côté avec la raison.

## Ce que le skill ne fait pas

- Merger la PR. C'est un humain qui approuve et merge.
- Passer l'issue en Done. L'intégration GitHub de Linear le fait au merge si
  elle est activée, sinon c'est manuel.
- Travailler sur plusieurs issues à la fois. Une issue, une branche, une PR.
