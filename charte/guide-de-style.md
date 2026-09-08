# Guide de style

Conventions d'écriture du cours. La mise en page Word vient de `reference.docx`,
ce guide couvre le fond et la structure Markdown.

## Charte graphique

_À définir par le groupe._ À renseigner ici puis à reporter dans `reference.docx` :

- Police titres : _à définir_
- Police corps : _à définir_
- Couleur principale : _à définir_
- Couleur secondaire : _à définir_
- Logos : `charte/logos/`

## Structure d'un fichier `cours.md`

```markdown
# Chapitre N — Titre

> Durée estimée : X min · Objectifs : ...

## 1. Section
### 1.1 Sous-section
```

- Un seul `#` (titre de niveau 1) par fichier.
- Les titres de niveau 2 sont numérotés à la main (`## 1.`, `## 2.`) pour
  garder la numérotation cohérente entre Markdown et docx.
- Pas de titre de niveau 4 ou plus.

## Écriture

- Vouvoiement de l'apprenant, ton direct et concret.
- Phrases courtes. Un paragraphe = une idée.
- Chaque notion nouvelle est définie à sa première apparition, en **gras**.
- Les termes techniques anglais sont en _italique_ à la première occurrence,
  avec une traduction ou explication.
- Les exemples de code ont un langage déclaré : ```` ```python ````.
- Les schémas sont dans `assets/` du chapitre, référencés avec une légende :
  `![Légende du schéma](assets/nom.png)`.

## Exercices et QCM

Format d'un exercice (`exercices.md`) :

```markdown
## Exercice N — Titre

**Objectif :** ...
**Durée :** X min

### Énoncé
...

### Corrigé
...
```

Format d'une question (`qcm.md`) :

```markdown
## Question N

Énoncé de la question ?

- [ ] Réponse A
- [x] Réponse B (bonne réponse)
- [ ] Réponse C
- [ ] Réponse D

**Explication :** pourquoi B.
```

## Sources et citations

- Toute reprise de contenu externe est citée : `(Auteur, année)` dans le texte
  et entrée complète dans `livrables/bibliographie.md`.
- Limite : 15 % de contenu reproduit sur l'ensemble du cours.
- Format des références : voir `ressources/normes-bibliographie.pdf`.

## Vidéos

Un fichier par vidéo dans `cours/NN-slug/videos/` :

```markdown
# Vidéo — Titre

- Durée cible : X min (max 8)
- Intervenant : ...
- Format : face caméra / screencast / live-coding

## Script
...

## Plan de montage
...
```

Les sous-titres (`.srt` ou `.vtt`) sont dans le même dossier.
