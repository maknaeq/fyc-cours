---
name: chapitre
description: Crée un nouveau chapitre du cours dans cours/NN-slug/ avec les fichiers types (README, cours, exercices, qcm, videos, assets). Usage : /chapitre NN slug "Titre du chapitre"
---

# Créer un chapitre

Arguments attendus : `NN slug "Titre"` (ex. `/chapitre 01 introduction "Introduction et contexte"`).
Si un argument manque, demander avant de créer.

## Étapes

1. Vérifier que `cours/NN-slug/` n'existe pas déjà.
2. Créer la structure :

```
cours/NN-slug/
├── README.md
├── cours.md
├── exercices.md
├── qcm.md
├── videos/.gitkeep
└── assets/.gitkeep
```

3. Contenu de `README.md` :

```markdown
# NN — Titre

- Durée apprenant : _X h_ (lecture + vidéos + exercices)
- Pré-requis : _..._
- Objectifs pédagogiques :
  - _..._
- Vidéos prévues : _..._
- Exercices : _..._
- Auteur principal : _..._
- Issue Linear : _..._
```

4. Contenu de `cours.md` :

```markdown
# Chapitre NN — Titre

> Durée estimée : _X min_ · Objectifs : _..._

## 1. 

## 2. 
```

5. `exercices.md` et `qcm.md` : un seul exemple vide au format de
   `charte/guide-de-style.md` (sections Exercices et QCM).
6. Rappeler à l'utilisateur de créer l'issue Linear correspondante avec
   l'estimation en heures apprenant, et d'ajouter la ligne dans le plan de
   `livrables/scenarisation.md`.

Ne pas rédiger de contenu de fond : uniquement le squelette.
