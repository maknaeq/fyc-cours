# Guide de style

Conventions d'écriture du cours. La mise en page Word vient de `reference.docx`,
ce guide couvre le fond et la structure Markdown.

## Charte graphique

Décidée le 08/09/2026 avec la page « Charte FYC », reportée dans `reference.docx`.

| Élément | Valeur |
|---|---|
| Police titres et corps | Arial, corps 11 pt, interligne 1,3 |
| Police code | JetBrains Mono (à installer sur chaque poste, Word remplace sinon) |
| Titres | Noir `#111111`, gras, numérotés, niveau 1 en capitales, sans filet |
| Accent | Bleu pétrole `#14526D` : liens, filet gauche des citations |
| Tableaux | Bordures `#999999`, en-tête fond `#EFEFEF` en gras, lignes alternées `#F5F7F9`, texte 9 pt |
| Page de titre | Alignée à gauche, sans bandeau |
| Logos | `charte/logos/` (à ajouter) |

Pour changer une valeur : rouvrir la page Charte FYC, enregistrer, puis
reporter dans `reference.docx` (styles Word) et ici.

## Structure d'un fichier `cours.md`

```markdown
# Chapitre N : Titre

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
## Exercice N : Titre

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
# Vidéo : Titre

- Durée cible : X min (max 8)
- Intervenant : ...
- Format : face caméra / screencast / live-coding

## Script
...

## Plan de montage
...
```

Les sous-titres (`.srt` ou `.vtt`) sont dans le même dossier.
