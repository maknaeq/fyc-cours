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
   plus, on vise 380. C'est un budget de longueur, pas un débit à tenir : on
   parle naturellement. Dans une vidéo de démonstration, la voix couvre toute
   la durée (voir « Parler comme on montre ») : un script de 3 min à 100 mots
   laisse des trous entre des phrases isolées, et sonne haché.
4. Viser 4 à 6 min, jamais plus de 8. Une correction ou une démo plus longue
   se découpe en 2 ou 3 vidéos, chacune avec un objectif et un titre.

## Règles du parlé

- **On parle à quelqu'un.** « Vous » dès la première phrase pour s'adresser à
  lui (« mettez en pause », « lancez-le vous-même »), « on » pour ce qu'on fait
  ensemble à l'écran. Le spectateur est seul devant son écran, on s'adresse à
  lui, pas à un public.
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
- **Montrer avant d'expliquer.** On fait apparaître le phénomène à l'écran
  (la requête qui bloque, l'agent qui obéit à l'injection), puis on explique.

## Parler comme on montre

Repères mesurés sur sept transcripts d'un cours en ligne de référence
(screencasts de 1 à 5 minutes, voix continue). Ils décrivent ce qui fait
« parlé » ; on s'en inspire sans en recopier les phrases.

- **La voix ne s'arrête pas pendant la démonstration.** Environ 145 mots par
  minute du début à la fin : une vidéo de 4 min 30 fait 800 mots. On ne
  laisse pas de plan muet, sauf un silence voulu (le pari, un résultat qu'on
  laisse lire). Pendant une attente accélérée, on continue de parler.
- **On dit ce qu'on fait en le faisant**, au présent, avec « on » (nous qui
  faisons ensemble) et « je » (ce que je règle ou choisis) : « ici, dans le
  terminal, on lance… », « je règle nginx sur vingt secondes ». Chaque action
  à l'écran a sa phrase juste avant ou pendant.
- **On enchaîne avec des mots d'oral, pas avec des points d'arrêt** :
  « alors », « donc », « maintenant », « et là », « voilà ». À peu près un
  tous les cinquante mots. Chaque phrase s'appuie sur la précédente.
- **On dit ce que le résultat veut dire dès qu'il apparaît**, puis pourquoi, puis
  ce qu'on en retient ou ce qu'on recommande : « ce n'est probablement pas ce
  qu'on veut, donc le mieux est de… ».
- **On vérifie qu'on est suivi** de temps en temps : « d'accord ? ». Une fois
  par vidéo ou deux, pas à chaque phrase.
- **On rassure et on reste humain** : dire qu'un réglage est impressionnant
  mais qu'on n'a pas besoin de tous les connaître, qu'on ne les connaît pas
  tous soi-même, vaut mieux qu'un ton d'expert. Une plaisanterie brève, annoncée
  comme telle, est permise.
- **Les énumérations se disent en phrases ordinales** (« le premier problème,
  c'est…, le deuxième… »), jamais en « Un : … Deux : … ».
- **Ouverture** : le sujet en une phrase, puis le plan en une respiration
  (« on va voir… puis… et on finira par… »). **Clôture** : une phrase de bilan
  (« voilà pour… »), puis ce qui vient ensuite, ou l'action du spectateur.
- **Longueur des phrases** : une dizaine de mots en moyenne, reliées par les
  connecteurs ci-dessus. Moins de 8 mots en moyenne, ou plus de quatre phrases
  de moins de 6 mots d'affilée, sonne haché. À mesurer sur le script avant de
  le livrer.
- **À ne pas copier** : les hésitations et les répétitions d'un oral spontané
  (« le compilateur, le compilateur »).

## Screencast et live coding

- Le code à l'écran est lisible (police 18 pt au moins, thème clair ou
  contrasté), une seule fenêtre à la fois.
- On dit ce qu'on fait avant de le taper (« on ajoute un délai au client
  HTTP »), puis pourquoi, pas chaque caractère.
- Une erreur en direct se garde si elle apprend quelque chose : on lit le
  message, on explique la cause, on corrige.
- Une correction commence par « Si vous n'avez pas encore essayé, mettez en
  pause » et montre d'abord le raisonnement, puis le code.
- Le script indique les actions entre crochets : `[Code : ajouter
  ->timeout(10)]`, `[Terminal : php artisan test]`.

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
