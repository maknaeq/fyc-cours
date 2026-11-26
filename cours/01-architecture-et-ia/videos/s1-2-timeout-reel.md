# Vidéo : Le timeout réel d'un appel d'IA dans un contrôleur

- Durée cible : 3 min (limite FYC : 8 min par vidéo). Voix de 256 mots, soit environ 1 min 50 à 140 mots par minute, le reste est de la démonstration (attentes accélérées, sorties de terminal laissées à l'écran).
- Intervenant : Quentin Bauduin (voix sur écran, pas de face caméra)
- Format : screencast terminal, police 18 pt au moins, thème contrasté, une seule fenêtre à la fois. Actions et incrustations entre crochets, elles ne se lisent pas.
- Mots : 256
- Séquence : S1.2, issue Linear FYC-47. S'appuie sur le dépôt de l'étude de cas ([xKaan/fyc-tp](https://github.com/xKaan/fyc-tp/tree/fyc-etude-s1-2/etude), branche `fyc-etude-s1-2`, scénarios 2 et 3 du README de `etude/`) et sur la section 2.1 du chapitre 01.
- Ce que le spectateur doit retenir : le délai qui coupe un appel d'IA lent n'est pas celui qu'on croit (PHP) et personne ne l'a choisi ; trois couches posent chacune le leur.
- Sources des affirmations : PHP Manual, `set_time_limit` (le temps d'attente réseau n'est pas compté dans `max_execution_time`) ; Laravel 13.x, HTTP Client (délai par défaut de 30 secondes) ; nginx, `fastcgi_read_timeout` (60 secondes par défaut). Voir `livrables/bibliographie.md`. La facturation d'un appel abandonné n'est garantie par aucune documentation de fournisseur : le script dit « probablement ».

## Script

[Écran : un terminal, la commande `etude/charge.sh 1` est tapée, puis un chrono apparaît en bas à droite]

Un utilisateur clique sur « Résumer ». Le fournisseur d'IA met quatre-vingt-dix secondes à répondre. Regardez le chrono.

[Écran : le chrono défile en accéléré, s'arrête à 30 s, la sortie affiche `clic 1 : HTTP 500 après 30.0 s`]

Trente secondes, et c'est une erreur 500. Qui a coupé ? Vous pensez peut-être à PHP, avec son délai de trente secondes. Ce n'est pas lui.

[Terminal : `docker compose -f etude/compose.yaml logs php | grep "cURL error"`, la ligne `cURL error 28: Operation timed out after 30001 milliseconds` est surlignée]

Voilà le coupable : le client HTTP de Laravel, qui abandonne par défaut au bout de trente secondes. Sous Linux, PHP ne compte pas le temps qu'il passe à attendre le réseau, son délai ne se déclenche jamais.

Et ce délai, personne ne l'a choisi. Le contrôleur n'en fixe aucun, il hérite de celui du framework, qui n'a rien à voir avec le temps qu'un utilisateur accepte d'attendre.

[Terminal : le journal du faux fournisseur montre l'appel reçu, puis sa réponse perdue]

Et le fournisseur, lui, a bien reçu l'appel. Avec un vrai, il sera probablement facturé.

[Terminal : `NGINX_DELAI=20 docker compose -f etude/compose.yaml up -d nginx`, puis `etude/charge.sh 1`, le chrono s'arrête à 20 s sur `504`]

Maintenant, on règle nginx, le serveur web placé devant PHP, sur vingt secondes. Cette fois, l'utilisateur reçoit une erreur 504 au bout de vingt secondes. Il est parti.

[Terminal : quatre secondes plus tard, `curl -s localhost:8080/fpm-status | grep "^active processes"` affiche `active processes: 2`]

Mais regardez le serveur. Deux processus sont actifs : celui qui répond à cette page d'état, et celui du clic, qui attend toujours un fournisseur que plus personne n'écoute. Il ne se libère qu'à trente secondes.

Et l'utilisateur reclique. Un deuxième appel, un deuxième processus occupé, une deuxième facture possible.

[Écran : un tableau à trois lignes : PHP, client HTTP de Laravel, serveur web ou proxy, avec trente, trente et soixante secondes]

Retenez ceci : trois délais coexistent, posés par trois couches différentes, et aucun n'a été choisi pour cet appel.

[Écran : le dossier `etude/` dans le dépôt]

Le dépôt de l'étude de cas est dans le chapitre. Lancez le deuxième scénario vous-même, notez avant de lancer qui va couper, et comparez. Les parades, on les construit en séance 3.

## Plan de montage

| Temps | Plan | Écran |
|-------|------|-------|
| 0:00 | Screencast | Terminal, `etude/charge.sh 1` tapé. Chrono incrusté en bas à droite, qui démarre à la validation |
| 0:20 | Screencast, accéléré | L'attente de 30 s est accélérée (chrono visible). Fin : la ligne `clic 1 : HTTP 500 après 30.0 s` reste à l'écran 3 s |
| 0:44 | Screencast | Filtre sur le journal de PHP, ligne `cURL error 28 ... 30001 milliseconds` surlignée |
| 1:10 | Screencast | Journal du faux fournisseur : l'appel reçu, la réponse perdue |
| 1:22 | Screencast, accéléré | `NGINX_DELAI=20`, nouveau clic, chrono qui s'arrête à 20 s sur l'erreur 504 |
| 1:50 | Screencast | `fpm-status` à 24 s : `active processes: 2`. Laisser la sortie 4 s avant « Mais regardez le serveur » |
| 2:20 | Incrustation | Tableau de trois lignes : PHP (30 s, ne se déclenche pas), client HTTP de Laravel (30 s, erreur 500), serveur web (60 s par défaut, ici 20 s, erreur 504) |
| 2:40 | Screencast | Arborescence du dossier `etude/`, puis carton de fin « Section 2.1 du chapitre 01 » |

## À faire au tournage

- Prérequis : Docker, dépôt `xKaan/fyc-tp` sur la branche `fyc-etude-s1-2`, application démarrée (`docker compose -f etude/compose.yaml up -d --build`, puis la migration indiquée dans le README de `etude/`). Le script n'a pas été tourné : les sorties citées (500 à 30 s, `cURL error 28`, 504 à 20 s, deux processus actifs à 24 s) viennent de la description du README de `etude/`, à confirmer sur la première prise. Si une valeur diffère, corriger le script, pas la prise.
- Scénario 2 : `LLM_DELAI=90 docker compose -f etude/compose.yaml up -d faux-llm` avant la prise. Scénario 3 : `NGINX_DELAI=20`, fournisseur toujours à 90 s.
- Relire le script à voix haute en chronométrant. Toute phrase où l'on bute est réécrite. Si la prise dépasse 3 min, couper des phrases entières (la phrase sur la deuxième facture est la première candidate).
- Minutages du plan de montage calés sur 140 mots par minute : à recaler sur la première prise.
- Sous-titres : vérifier « nginx », « PHP », « Laravel », « cURL » et « fpm-status » dans la transcription automatique.
