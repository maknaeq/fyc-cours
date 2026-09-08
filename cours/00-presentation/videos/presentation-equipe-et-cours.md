# Vidéo : Présentation de l'équipe et du cours

- Durée cible : 3 min (maximum imposé par le FYC)
- Intervenant : Quentin Bauduin, face caméra
- Format : plan fixe, téléphone en mode paysage, éclairage de face. Trois
  incrustations de texte à l'écran, indiquées entre crochets.
- Rythme : environ 140 mots par minute, soit 400 à 420 mots. Le script en fait
  410. Parler posément, respirer aux paragraphes.

## Script

[Écran : titre du cours]

Bonjour, et bienvenue dans ce cours. Il s'appelle « Concevoir une application
web maintenable intégrant un agent IA », et il répond à une question simple en
apparence : comment ajouter une IA à une application web sans casser tout ce
qui fait qu'une application est maintenable, testable et sûre.

Je m'appelle Quentin Bauduin. Nous sommes quatre à avoir construit ce cours,
tous en première année de mastère IW à l'ESGI.

[Écran : les quatre prénoms et les rôles]

Kaan Topkaya a écrit les travaux pratiques Laravel, les squelettes de code et
leurs corrigés. Erwin Gossin a préparé l'environnement : le modèle local, la
base vectorielle, le guide d'installation. Timothé Geoffroy a conçu le projet
fil rouge et les comparaisons avec d'autres frameworks. Et moi, j'ai écrit le
contenu transversal et les vidéos.

Pourquoi ce sujet ? Parce qu'aujourd'hui, brancher une IA sur une application
prend dix minutes. Les fournisseurs exposent une API, les frameworks proposent
un SDK, on appelle un modèle depuis un contrôleur et ça marche. Le problème
arrive après. La réponse n'est jamais la même deux fois. L'appel prend parfois
trente secondes. Chaque requête coûte de l'argent. Le fournisseur change de
modèle sans prévenir. Et n'importe quel texte qui entre dans le modèle peut le
manipuler.

Ce cours part de ces cinq caractéristiques, et vous apprend à construire une
application qui les prend en compte dès l'architecture.

[Écran : le plan en cinq séances]

Il se déroule en cinq séances de trois heures, sur Moodle, à votre rythme.
Séance un : les bases de l'architecture web, et pourquoi l'IA les bouscule.
Séance deux : construire un agent, avec des outils et de la recherche dans vos
documents. Séance trois : rendre l'application fiable et mesurer ce que fait
l'agent. Séance quatre : tester un composant qui ne répond jamais pareil, et
se défendre contre les attaques par texte piégé. Séance cinq : mettre en
production, et rédiger la fiche d'architecture qui conclut le cours.

Un fil rouge traverse tout ça : une application de prise de notes, en Laravel,
que vous faites évoluer d'une séance à l'autre. Et un parti pris : vous
n'utiliserez pas de SDK d'IA. Vous construirez vous-même chaque brique, puis
vous la comparerez à ce que font les SDK. À la fin, vous saurez pourquoi
chaque pièce existe.

Le cours est fait pour être suivi seul, avec tout ce qu'il faut à chaque
étape : les supports, le code de départ, les corrigés, et un modèle qui
tourne sur votre machine pour ne rien payer.

La prochaine vidéo détaille les pré-requis. On se retrouve juste après.

## Plan de montage

| Temps | Plan | Écran |
|-------|------|-------|
| 0:00 | Face caméra | Carton titre : nom du cours, logo si disponible |
| 0:20 | Face caméra | Incrustation : quatre prénoms et rôles, un par ligne |
| 1:00 | Face caméra | Rien, ou les cinq caractéristiques qui apparaissent une par une |
| 1:45 | Face caméra | Incrustation : les cinq séances, une par ligne |
| 2:30 | Face caméra | Rien |
| 2:55 | Face caméra | Carton de fin : « Suite : les pré-requis » |

Sous-titres obligatoires : générer automatiquement, puis relire mot à mot.
Les noms propres et « Laravel » sont souvent mal transcrits.
