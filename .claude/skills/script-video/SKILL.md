---
name: script-video
description: Écrit ou réécrit le script d'une vidéo du cours (présentation, pré-requis, intro de séquence, correction, conclusion) en langage parlé, avec plan de montage et minutage. Usage : /script-video <fichier.md> ou /script-video "sujet"
---

# Script de vidéo

Un script se dit à voix haute, face caméra, par une personne qui parle à une
autre. Il ne se lit pas. Tout ce qui suit découle de ça.

## Avant d'écrire

1. Lire `charte/regles-redaction.md` et le script existant s'il y en a un.
2. Fixer : qui parle, à qui, combien de temps (le FYC impose 8 min max, 3 min
   pour la présentation du cours), et la seule chose que le spectateur doit
   retenir à la fin.
3. Compter : 140 mots par minute parlée. Un script de 3 min fait 400 mots au
   plus, on vise 380.

## Règles du parlé

- **On parle à quelqu'un.** « Vous » dès la première phrase. Le spectateur
  est seul devant son écran, on s'adresse à lui, pas à un public.
- **Une phrase, une idée, un souffle.** Si on ne peut pas la dire d'une
  traite, elle est trop longue. Pas de proposition relative en cascade, pas
  de parenthèse.
- **Pas de rupture artificielle.** Interdits : « Il s'appelle… », « Pourquoi
  ce sujet ? Parce que… », « Un : … Deux : … », les titres lus, les
  transitions du type « Passons maintenant à ». On enchaîne comme dans une
  conversation : la phrase suivante découle de la précédente.
- **Le titre n'est pas une phrase.** On ne dit pas le titre exact du cours,
  on dit ce que le cours fait. Le titre est à l'écran.
- **Les personnes, pas les postes.** Pour présenter une équipe, on ne récite
  pas « X a écrit ça, Y a fait ça ». On dit qu'on est quatre, ce qui nous
  réunit, et éventuellement une phrase sur la répartition en une seule
  respiration. Les prénoms et rôles vont à l'écran.
- **Pas de contexte scolaire non demandé.** On ne dit pas « nous sommes
  étudiants en première année » sauf si le format l'impose. Le spectateur
  s'inscrit à un cours, pas à une promo.
- **Concret avant abstrait.** Une situation vécue (« vous cliquez, rien ne
  répond pendant trente secondes ») avant le concept (« la latence »).
- **Les listes se disent en phrases.** Trois éléments maximum à l'oral, reliés
  par du sens, pas par des numéros. Au-delà, c'est une incrustation à
  l'écran et on n'en dit que l'essentiel.
- **Les contractions et les tournures orales sont permises** : « ça », « on »,
  « c'est », « pas besoin de ». Le vouvoiement reste.
- **Une seule question rhétorique par script**, au maximum, et on y répond
  dans la phrase suivante.
- **Finir sur une action** : ce que le spectateur fait juste après.

## Test obligatoire avant de livrer

Relire le script à voix haute, en entier, en chronométrant. Toute phrase où
l'on bute est réécrite. Si la durée dépasse la cible, couper des phrases
entières, pas des mots.

## Format du fichier

```markdown
# Vidéo : Titre

- Durée cible : X min (limite FYC : ...)
- Intervenant : ...
- Format : plan fixe, face caméra, incrustations entre crochets
- Mots : N (140 mots par minute)

## Script

[Écran : ...]

Texte parlé, un paragraphe par respiration longue.

## Plan de montage

| Temps | Plan | Écran |
|---|---|---|

Sous-titres : mots à vérifier dans la transcription automatique.
```

Les crochets `[Écran : ...]` ne se lisent pas. Ils indiquent au monteur ce
qui apparaît.

## Ce que le skill ne fait pas

Tourner, monter, sous-titrer. Il livre un texte qu'une personne peut dire
d'une traite, et un plan pour le monteur.
