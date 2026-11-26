# Vidéo : Où placer un appel à une IA dans une appli en couches

- Durée cible : environ 2 min 30 (budget de 6 min dans `livrables/budget-video.md`, limite FYC : 8 min). Plus court que prévu : la vidéo pose la question, elle ne répond pas, la réponse est dans le support. On garde la marge ou on enrichit après avoir tourné.
- Intervenant : Quentin Bauduin, voix sur écran, pas de face caméra. Ton : celui d'un collègue qui montre son écran, calme, sans effet de présentation.
- Format : screencast, police 18 pt au moins, thème contrasté, une seule fenêtre à la fois (deux fenêtres côte à côte quand le script le dit). Actions et incrustations entre crochets, elles ne se lisent pas.
- Mots : 201 (140 mots par minute). La voix tient en 86 secondes, le reste est du code qui défile et deux silences.
- Place dans le parcours : S1.1, tout début du chapitre 01, avant le support écrit. L'apprenant vient du chapitre 00 : environnement installé, test de positionnement fait. Il connaît PHP et Laravel, il n'a encore rien lu sur les couches ni sur l'IA. La vidéo ne leur apprend rien de nouveau : elle lui fait sentir le problème sur du code réel, puis le fait parier (où ranger l'appel ?) avant de lire. La réponse est en section 1.3 du support, le TP S1.3 la lui fait écrire.
- Ce que le spectateur doit retenir : il existe plusieurs endroits possibles pour un appel à une IA, le plus court (le contrôleur) mélange ce qui change vite (fournisseur, modèle, consigne) avec ce qui doit durer (les règles du métier). Il repart avec sa propre réponse, notée, à confronter au support.
- Source : le contrôleur de départ du TP S1.3 ([xKaan/fyc-tp](https://github.com/xKaan/fyc-tp), branche `fyc-tp-s1`, `app/Http/Controllers/NoteController.php`, méthodes `summarize` et `suggestTags`). Tout ce que la voix dit du code est lisible à l'écran : adresse du fournisseur, clé lue dans `env()`, modèle et consigne écrits en dur, bloc d'appel recopié dans les deux méthodes, aucun traitement du cas où le fournisseur ne répond pas. Aucune affirmation chiffrée ni sourcée n'est faite dans la vidéo.

## Script

[Écran : l'application de notes dans le navigateur, une note ouverte, un bouton « Résumer » ajouté sur la capture]

Votre responsable produit veut un bouton « Résumer » sur chaque note. L'appel à l'IA tient en quelques lignes. La vraie décision, c'est où les ranger.

[Écran : `NoteController.php` du dépôt du TP, méthode `summarize`, défilement lent. Surligner au fil de la phrase : l'adresse du fournisseur, la clé, le modèle, la consigne, la lecture de la réponse]

Le chemin le plus court, c'est le contrôleur. Voilà ce que ça donne : l'adresse du fournisseur, la clé, le modèle, la consigne, et la façon de lire la réponse, tout au même endroit.

[Écran : la méthode `suggestTags`, le bloc d'appel entouré de la même couleur que celui de `summarize`]

Et la méthode d'après, qui propose des étiquettes, recopie le même bloc. Rien ne prévoit le cas où le fournisseur ne répond pas.

[Écran : trois cartes côte à côte : « Le contrôleur », « Le modèle Note », « Une classe à part »]

Mettez la vidéo en pause. Si vous deviez ranger ce code autrement, où mettriez-vous l'appel à l'IA : dans le contrôleur, dans le modèle Note, ou ailleurs ? Notez votre réponse, et surtout la raison.

[Écran : les trois cartes restent 10 secondes, sans voix]

Je ne vous donne pas la réponse ici : le support la construit, et le TP vous la fait écrire. Je vous donne seulement de quoi juger la vôtre. Dans votre code, certaines choses changent vite : le fournisseur, le modèle, la consigne. D'autres doivent durer : les règles de votre métier, par exemple qu'une note doit avoir un titre. Une bonne réponse les garde séparées.

[Écran : carton « Support, section 1.1 »]

Gardez votre réponse sous les yeux et ouvrez le support. Vous la retrouverez à la section 1.3.

## Plan de montage

| Temps | Plan | Écran |
|-------|------|-------|
| 0:00 | Screencast | Application dans le navigateur, une note ouverte, bouton « Résumer » ajouté sur la capture |
| 0:15 | Screencast | `NoteController.php`, `summarize`, défilement lent, surlignages au rythme de la phrase |
| 0:37 | Screencast | `suggestTags`, bloc d'appel entouré de la même couleur que celui de `summarize` |
| 0:51 | Incrustation | Trois cartes : le contrôleur, le modèle Note, une classe à part. Elles restent 10 s après la question, sans voix |
| 1:20 | Incrustation | Les cartes restent pendant le critère, sans surlignage : la réponse n'est pas donnée |
| 1:47 | Carton | « Support, section 1.1 » |

## À faire au tournage

- Aucun lancement du code : on lit le fichier, pas besoin d'application qui tourne. La capture de l'application (premier plan) vient du dépôt du TP (`sail up`), le bouton « Résumer » y est déjà présent, la maquette n'est utile que si l'application n'est pas lancée.
- Ne pas montrer la réponse (une classe à part derrière une interface) : elle est donnée par le support. La vidéo ne la dit pas, ni à l'écran ni à la voix.
- La vidéo du TP S1.3 (« Un port, deux fournisseurs, une ligne de config ») montre la solution à partir du même contrôleur : ne pas la dévoiler ici.
- Relire à voix haute en chronométrant. Toute phrase où l'on bute est réécrite.

Sous-titres : vérifier les noms propres et le code lu à voix haute dans la transcription automatique.

Minutages calés sur 140 mots par minute et sur des temps d'écran estimés : à recaler sur la première prise.
