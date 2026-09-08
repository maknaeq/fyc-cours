---
name: retour-mentor
description: Crée le compte-rendu d'une séance avec le mentor dans retours-mentor/ à partir du template, puis aide à transformer les retours en actions. Usage : /retour-mentor N YYYY-MM-DD
---

# Compte-rendu de séance mentor

Arguments : `N YYYY-MM-DD` (numéro de séance, date). Demander si absents.

## Étapes

1. Copier `retours-mentor/_template.md` vers `retours-mentor/YYYY-MM-DD-seance-N.md`
   en remplaçant le titre.
2. Demander à l'utilisateur de coller ou dicter les retours du mentor.
   Les reformuler en points courts et factuels, sans en ajouter.
3. Pour chaque retour, proposer une action concrète (fichier à modifier,
   chapitre concerné, estimation) dans la section « Actions ».
4. Si le connecteur Linear est disponible, proposer de créer les issues
   correspondantes (une par action) dans le projet FYC, en demandant
   confirmation avant de créer.
5. Si un retour change une contrainte du projet (durée cible, périmètre,
   plan), mettre à jour `README.md` et `livrables/scenarisation.md` en
   conséquence et le signaler.
