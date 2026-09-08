# Vidéo : Présentation des pré-requis

- Durée cible : 3 min 30 (maximum 8)
- Intervenant : Quentin Bauduin, face caméra
- Format : plan fixe, même cadrage que la vidéo de présentation. Deux
  incrustations de texte, indiquées entre crochets. Possibilité de couper sur
  une capture d'écran du guide d'installation à 2:30.
- Rythme : environ 480 mots. Le script en fait 470.

## Script

Avant de commencer, vérifions ensemble ce qu'il faut savoir et ce qu'il faut
installer. Rien de tout ça n'est difficile, mais si un point vous manque,
c'est le moment de le combler.

[Écran : ce qu'il faut savoir, quatre lignes]

Côté connaissances, quatre choses.

Un : programmer en orienté objet en PHP. Classes, interfaces, injection de
dépendances. Si vous savez écrire une interface et une classe qui
l'implémente, c'est bon.

Deux : connaître les bases de Laravel. Les routes, les contrôleurs, Eloquent
pour la base de données, et le conteneur de dépendances. Pas besoin d'être
expert : on part d'un contrôleur simple et on le fait évoluer.

Trois : savoir ce qu'est une API REST, et comment se passe un aller-retour
HTTP entre un client et un serveur. Tout le cours tourne autour d'appels HTTP
vers un fournisseur d'IA.

Quatre : utiliser Git au quotidien. Cloner un dépôt, créer une branche,
commiter. Chaque TP part d'un dépôt et vous versionnez votre travail.

Ce qu'il ne faut pas savoir : rien sur l'intelligence artificielle. Aucune
notion de réseau de neurones, aucune formule. On traite le modèle comme une
boîte à laquelle on envoie du texte et qui renvoie du texte. Tout le reste,
on le construit ensemble. Et pas besoin de Java non plus : les extraits Spring
que vous verrez dans les comparaisons se lisent, ils ne s'exécutent pas.

[Écran : ce qu'il faut installer, cinq lignes]

Côté machine, cinq choses, toutes gratuites.

PHP 8.3 et Composer. Un éditeur, celui que vous voulez. Docker, pour lancer
PostgreSQL avec l'extension pgvector, qui servira à la recherche dans vos
documents à partir de la séance deux. Ollama, qui fait tourner un modèle de
langage directement sur votre ordinateur. Et, en option, une clé d'accès chez
un fournisseur d'IA en ligne.

Un mot sur ce dernier point. Tout le cours peut se faire avec le modèle local,
sans payer et sans connexion. La clé en ligne sert à comparer : vitesse,
qualité, coût. Si vous n'en voulez pas, vous ne perdez rien d'essentiel.

Pour Ollama, comptez seize gigaoctets de mémoire pour être à l'aise avec un
petit modèle. Si votre machine en a moins, le guide d'installation propose un
modèle plus léger, ou l'API en ligne seule.

[Écran : capture du guide d'installation]

Le guide d'installation pas à pas est dans la première séance. Il se termine
par une commande de vérification qui vous dit si tout est en place. Faites-le
avant de commencer la séance un : ça vous évitera de perdre le fil au milieu
du premier TP.

Un dernier conseil. Ce cours se suit seul, à votre rythme, mais il demande de
manipuler. Chaque séance contient un TP d'une heure environ. Lire sans faire,
ça ne marche pas pour ce sujet-là. Prévoyez trois heures par séance, avec
votre éditeur ouvert.

C'est tout. Rendez-vous dans la séance un.

## Plan de montage

| Temps | Plan | Écran |
|-------|------|-------|
| 0:00 | Face caméra | Carton : « Pré-requis » |
| 0:15 | Face caméra | Incrustation : les quatre connaissances, une par ligne |
| 1:30 | Face caméra | Rien |
| 1:50 | Face caméra | Incrustation : les cinq outils, un par ligne |
| 2:30 | Capture d'écran | Guide d'installation, puis la commande de vérification |
| 3:00 | Face caméra | Rien |
| 3:25 | Face caméra | Carton de fin : « Séance 1 » |

Sous-titres obligatoires. Vérifier « pgvector », « Ollama », « Composer »
dans la transcription automatique.
