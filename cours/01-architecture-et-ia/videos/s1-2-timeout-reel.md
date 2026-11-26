# Vidéo : Le timeout réel d'un appel d'IA dans un contrôleur

- Durée cible : environ 2 min, 3 min au plus (budget de 3 min dans `livrables/budget-video.md`, limite FYC : 8 min par vidéo). La voix fait 101 mots, soit moins d'une minute : le reste est de la démonstration (attentes accélérées, sorties laissées à l'écran, pauses).
- Intervenant : Quentin Bauduin, voix sur écran, pas de face caméra. Ton : celui d'un collègue qui montre sa console, calme, sans effet de présentation.
- Format : screencast terminal, police 18 pt au moins, thème contrasté, une seule fenêtre à la fois. Actions et incrustations entre crochets, elles ne se lisent pas.
- Mots : 101 (140 mots par minute)
- Place dans le parcours : section 2.1 du chapitre 01 (S1.2, étude de cas). L'apprenant a déjà lu « Lundi, 9 h » et « Lundi, 9 h 01 » : il connaît l'explication par écrit (le texte renvoie à cette vidéo juste après). La vidéo ne la répète donc pas, elle lui fait **voir** le phénomène et lui laisse **parier** avant. Il a fini S1.1, il connaît PHP et Laravel, il n'a encore rien vu sur l'IA.
- Ce que le spectateur doit retenir : le délai qui coupe un appel d'IA lent n'est pas celui qu'on attend (PHP), et un utilisateur parti ne libère pas le processus. Le tableau des trois délais est dans le support (2.1) et dans le README de `etude/` : il reste à l'écran sans commentaire.
- Source : dépôt de l'étude de cas ([xKaan/fyc-tp](https://github.com/xKaan/fyc-tp/tree/fyc-etude-s1-2/etude), branche `fyc-etude-s1-2`, scénarios 2 et 3). Les affirmations (PHP ne compte pas l'attente réseau, délai de 30 s du client HTTP de Laravel, 60 s de nginx) sont sourcées dans la section 2.1 et dans `livrables/bibliographie.md`. La facturation d'un appel abandonné n'est volontairement pas dite dans la vidéo : le support l'explique avec la prudence qu'il faut.

## Script

[Écran : terminal, `etude/charge.sh 1` prêt à être lancé. Incrusté à gauche : « Fournisseur : 90 s. PHP : 30 s. Serveur web : 60 s. »]

Le fournisseur met quatre-vingt-dix secondes à répondre. PHP coupe à trente, le serveur web à soixante. Avant de lancer, notez qui va couper l'appel.

[Écran : l'incrustation reste, silence de 5 secondes, un compte à rebours discret]

On lance.

[Terminal : la commande est validée. Chrono incrusté, attente accélérée jusqu'à 30 s, la ligne `clic 1 : HTTP 500 après 30.0 s` reste 3 s]

Erreur 500, au bout de trente secondes. Ce n'est pas PHP. Le journal le dit.

[Terminal : `docker compose -f etude/compose.yaml logs php | grep "cURL error"`, la ligne `cURL error 28: Operation timed out after 30001 milliseconds` est surlignée]

C'est le client HTTP de Laravel, avec son délai par défaut. Maintenant, on ramène nginx à vingt secondes.

[Terminal : `NGINX_DELAI=20 docker compose -f etude/compose.yaml up -d nginx`, puis `etude/charge.sh 1`. Chrono accéléré, la ligne `504` reste 3 s]

Erreur 504 au bout de vingt secondes : l'utilisateur est parti.

[Terminal : quatre secondes plus tard, `curl -s localhost:8080/fpm-status | grep "^active processes"` affiche `active processes: 2`]

Mais le processus PHP, lui, est toujours là. Il attend un fournisseur que plus personne n'écoute.

[Écran : le tableau des trois délais, 10 s, sans voix : PHP (30 s, ne se déclenche pas), client HTTP de Laravel (30 s, erreur 500), serveur web (60 s par défaut, erreur 504)]

[Écran : le dossier `etude/` dans le dépôt]

Le dossier est dans le dépôt. Lancez le deuxième scénario, et notez votre hypothèse avant.

## Plan de montage

| Temps | Plan | Écran |
|-------|------|-------|
| 0:00 | Screencast | Terminal prêt, incrustation des trois délais, voix |
| 0:12 | Screencast | Silence de 5 s, l'incrustation reste, compte à rebours discret |
| 0:20 | Screencast, accéléré | `etude/charge.sh 1`, chrono incrusté. Attente de 30 s accélérée, la ligne `HTTP 500 après 30.0 s` reste 3 s |
| 0:40 | Screencast | Filtre sur le journal de PHP, ligne `cURL error 28 ... 30001 milliseconds` surlignée |
| 0:55 | Screencast, accéléré | `NGINX_DELAI=20`, nouveau clic, chrono jusqu'à 20 s, la ligne `504` reste 3 s |
| 1:20 | Screencast | `fpm-status` : laisser 4 s sans voix avant « Mais le processus PHP, lui, est toujours là » |
| 1:35 | Incrustation | Tableau des trois délais, 10 s, sans voix |
| 1:45 | Screencast | Arborescence du dossier `etude/`, carton de fin « Section 2.1 du chapitre 01 » |

## À faire au tournage

- Prérequis : Docker, dépôt `xKaan/fyc-tp` sur la branche `fyc-etude-s1-2`, application démarrée (`docker compose -f etude/compose.yaml up -d --build`, puis la migration indiquée dans le README de `etude/`). Avant la prise 1 : `LLM_DELAI=90 docker compose -f etude/compose.yaml up -d faux-llm`.
- Le script n'a pas été tourné : les sorties citées (500 à 30 s, `cURL error 28`, 504 à 20 s, deux processus actifs à 24 s) viennent du README de `etude/`, à confirmer sur la première prise. Si une valeur diffère, corriger le script, pas la prise.
- Relire à voix haute en chronométrant. Toute phrase où l'on bute est réécrite. Les minutages sont calés sur 140 mots par minute et sur des attentes accélérées : à recaler sur la première prise.
- Sous-titres : vérifier « nginx », « PHP », « Laravel », « cURL » et « fpm-status » dans la transcription automatique.
