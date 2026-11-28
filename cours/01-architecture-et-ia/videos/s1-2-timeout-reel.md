# Vidéo : Le timeout réel d'un appel d'IA dans un contrôleur

- Durée cible : environ 3 min (budget de 3 min dans `livrables/budget-video.md`, limite FYC : 8 min par vidéo). La voix dure environ 2:32 à 140 mots par minute et couvre toute la démonstration, avec une pause de quelques secondes pour le pari et quelques sorties laissées à l'écran.
- Intervenant : Quentin Bauduin, voix sur écran, pas de face caméra. Ton : celui d'une personne qui fait la démonstration en direct et dit ce qu'elle fait, avec « on » et « je » (voir la compétence `script-video`, section « Parler comme on montre »).
- Format : screencast terminal, police 18 pt au moins, thème contrasté, une seule fenêtre à la fois. Actions et incrustations entre crochets, elles ne se lisent pas.
- Mots : 356 (140 mots par minute)
- Place dans le parcours : section 2.1 du chapitre 01 (S1.2, étude de cas). L'apprenant a déjà lu « Lundi, 9 h » et « Lundi, 9 h 01 » : il connaît l'explication par écrit (le texte renvoie à cette vidéo juste après). La vidéo la lui fait **voir** et lui laisse **parier** avant. Il a fini S1.1, il connaît PHP et Laravel, il n'a encore rien vu sur l'IA.
- Ce que le spectateur doit retenir : le délai qui coupe un appel d'IA lent n'est pas celui qu'on attend (PHP), et un utilisateur parti ne libère pas le processus. Le tableau des trois délais est dans le support (2.1) et dans le README de `etude/`.
- Source : dépôt de l'étude de cas ([xKaan/fyc-tp](https://github.com/xKaan/fyc-tp/tree/fyc-etude-s1-2/etude), branche `fyc-etude-s1-2`, scénarios 2 et 3). Les affirmations (PHP ne compte pas l'attente réseau, délai de 30 s du client HTTP de Laravel, 60 s de nginx) sont sourcées dans la section 2.1 et dans `livrables/bibliographie.md`. La facturation d'un appel abandonné n'est volontairement pas dite dans la vidéo : le support l'explique avec la prudence qu'il faut.

## Script

[Écran : l'application de notes, une note ouverte. Puis le terminal, dossier `etude/`]

Vous venez de lire ce qui se passe quand le fournisseur d'IA ralentit. Alors on va le reproduire, parce que c'est beaucoup plus parlant quand on le voit arriver.

[Écran : l'arborescence du dossier `etude/`, puis le terminal avec la commande `LLM_DELAI=90 docker compose -f etude/compose.yaml up -d faux-llm`]

Dans ce dossier, on a l'application de notes, un serveur web nginx devant, PHP avec huit processus, et un faux fournisseur d'IA dont on peut régler la lenteur. Ici, je le règle à quatre-vingt-dix secondes. Donc quand un utilisateur clique sur « Résumer », il va attendre une minute et demie la réponse.

[Écran : incrustation « PHP : 30 s. Serveur web : 60 s. Fournisseur : 90 s. », qui reste jusqu'au résultat]

Maintenant, il y a deux délais en jeu. PHP est réglé à trente secondes, et nginx à soixante. Avant de lancer, mettez la vidéo en pause et notez qui, d'après vous, va couper l'appel. D'accord ? Alors on y va.

[Terminal : `etude/charge.sh 1`. Un chrono s'affiche en bas à droite. Attente accélérée, la ligne `clic 1 : HTTP 500 après 30.0 s` reste 3 secondes]

Alors, au bout de trente secondes, on obtient une erreur 500. Donc, qui a coupé ? Contrairement à ce qu'on pourrait croire, ce n'est pas PHP. Pour le savoir, on va lire le journal de PHP.

[Terminal : `docker compose -f etude/compose.yaml logs php | grep "cURL error"`. La ligne `cURL error 28: Operation timed out after 30001 milliseconds` est surlignée]

Et là, on voit cURL error 28, operation timed out, après trente secondes. C'est donc le client HTTP de Laravel qui a abandonné, avec son délai par défaut. Et ça, c'est important : personne n'a choisi ce délai. Le contrôleur n'en fixe aucun, il hérite de celui du framework.

[Terminal : `NGINX_DELAI=20 docker compose -f etude/compose.yaml up -d nginx`, puis `etude/charge.sh 1`. Chrono accéléré, la ligne `504` reste 3 secondes]

Maintenant, on va mettre devant un serveur plus pressé. Je règle nginx sur vingt secondes, et je relance le même clic. Cette fois, on a une erreur 504 au bout de vingt secondes. C'est nginx qui répond à l'utilisateur, et l'utilisateur, lui, est parti.

[Terminal : `curl -s localhost:8080/fpm-status | grep "^active processes"`, qui affiche `active processes: 2`]

Mais regardons le serveur, quatre secondes plus tard. On a deux processus actifs. Le premier répond à cette page d'état. Le deuxième, c'est celui du clic : il attend toujours la réponse du fournisseur, alors que personne ne l'écoute plus. Il ne se libérera qu'à trente secondes, quand le client HTTP abandonnera à son tour.

[Écran : le tableau des trois délais, 8 secondes : PHP, client HTTP de Laravel, serveur web]

Donc pour résumer, on a trois délais, posés par trois couches différentes, et aucun n'a été choisi pour cet appel. Les solutions, on les construit en séance 3. En attendant, le dossier est dans le dépôt du chapitre : lancez le deuxième scénario vous-même, et notez d'abord qui va couper.

## Plan de montage

| Temps | Plan | Écran |
|-------|------|-------|
| 0:00 | Screencast | Application de notes, puis terminal dans `etude/` |
| 0:12 | Screencast | Arborescence de `etude/`, commande `LLM_DELAI=90 ... up -d faux-llm` |
| 0:35 | Incrustation sur le terminal | Incrustation des trois délais, qui reste jusqu'au résultat. Pause de 6 s après « D'accord ? » |
| 0:58 | Screencast, accéléré | `etude/charge.sh 1`, chrono incrusté, attente accélérée, la ligne `HTTP 500 après 30.0 s` reste 3 s |
| 1:16 | Screencast | Journal de PHP filtré, ligne `cURL error 28 ... 30001 milliseconds` surlignée, laissée 3 s |
| 1:40 | Screencast, accéléré | `NGINX_DELAI=20`, même clic, chrono accéléré, la ligne `504` reste 3 s |
| 1:59 | Screencast | `fpm-status` : `active processes: 2`, laissé 3 s avant « Le deuxième, c'est celui du clic » |
| 2:23 | Incrustation | Tableau des trois délais, 8 s, puis le dossier `etude/` dans le dépôt |

## À faire au tournage

- Prérequis : Docker, dépôt `xKaan/fyc-tp` sur la branche `fyc-etude-s1-2`, application démarrée (`docker compose -f etude/compose.yaml up -d --build`, puis la migration indiquée dans le README de `etude/`). Le script suppose le faux fournisseur réglé à 90 s avant la prise (première commande à l'écran).
- Le script n'a pas été tourné : les sorties citées (500 à 30 s, `cURL error 28`, 504 à 20 s, deux processus actifs 4 s après) viennent du README de `etude/`, à confirmer sur la première prise. Si une valeur diffère, corriger le script, pas la prise.
- Le texte est écrit pour être dit **pendant** que les commandes tournent : pendant les attentes accélérées, continuer à parler (« alors, on attend… ») plutôt que laisser le silence. Seule vraie pause : celle du pari.
- Relire à voix haute en chronométrant. Toute phrase où l'on bute est réécrite. Si la prise dépasse 3 min, couper la phrase sur « une minute et demie » et la phrase de récapitulatif avant les explications.
- Sous-titres : vérifier « nginx », « PHP », « Laravel », « cURL » et « fpm-status » dans la transcription automatique.
