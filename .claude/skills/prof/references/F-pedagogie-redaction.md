# Thème F : pédagogie, rédaction et ton d'un cours en ligne technique

> Référence pour l'agent « prof » du FYC. Recherche du 24/11/2026.
> Ce document **complète** `charte/regles-redaction.md`, `charte/guide-de-style.md`
> et la skill `.claude/skills/script-video/SKILL.md` : il ne les remplace pas.
> En cas de doute, la charte du groupe gagne (vouvoiement, pas de tiret long,
> format des exercices et QCM, 8 min max par vidéo).
>
> Convention : chaque affirmation tirée d'une source renvoie à son entrée de la
> section 7 par un code entre crochets, par exemple [Guo14]. Les mesures que j'ai
> faites moi-même (débits de parole) sont signalées comme telles.

## 1. Principes de conception

Dix-huit principes, tous applicables à notre cours de 15 h (5 séances de 3 h,
public mastère qui connaît PHP et Laravel). Chacun donne la règle, ce qu'elle
change chez nous, et la source.

### P1. Un objectif, un verbe, et la même activité dans le TP et dans l'évaluation

Biggs demande de formuler chaque acquis visé avec un verbe (deux au plus), de
faire pratiquer ce verbe pendant les activités, puis d'évaluer ce même verbe
[Biggs14]. Chez nous : l'objectif « Justifier un choix technique » ne peut pas
être évalué par un QCM de définitions ; il l'est par la fiche d'architecture du
cas pratique (S5.3), et il doit avoir été pratiqué avant (grilles comparatives
S1.4 et S4.3). Pour chaque chapitre, le prof écrit en tête du `README.md` la
liste « objectif → activité → évaluation » et vérifie qu'aucune case n'est vide.

### P2. Placer chaque objectif dans la table de Bloom révisée

La taxonomie révisée croise six processus (se souvenir, comprendre, appliquer,
analyser, évaluer, créer) et quatre types de connaissances (factuelles,
conceptuelles, procédurales, métacognitives) [Krathwohl02]. Pour un mastère, la
majorité des objectifs doit viser « appliquer », « analyser » et « évaluer » :
implémenter un adaptateur (appliquer, procédural), repérer les points de rupture
d'un contrôleur (analyser), comparer le code maison au Laravel AI SDK (évaluer),
concevoir la fiche d'architecture (créer). Les questions de pure mémoire sont
réservées au test de positionnement et à quelques QCM de vocabulaire.

### P3. Partir d'un problème, puis activer, montrer, faire appliquer, intégrer

Merrill résume les modèles d'enseignement efficaces en quatre phases centrées
sur un problème : activer l'expérience antérieure, démontrer, faire appliquer,
intégrer dans une activité réelle [Merrill02]. Notre fil rouge est la phase
d'intégration ; chaque séquence doit aussi commencer par activer ce que
l'apprenant sait déjà (« vous avez déjà appelé une API de paiement depuis un
contrôleur ? ») avant la démonstration.

### P4. Guider explicitement ce qui est nouveau ; la découverte sert à pratiquer

Pour du contenu nouveau, l'instruction explicite avec pratique et retour est
plus efficace que la découverte peu guidée ; les projets servent à pratiquer ce
qui vient d'être appris [Clark12]. Notre choix « TP sans SDK » est exigeant :
il n'est tenable que si chaque TP fournit un squelette, des tests qui échouent
au départ et des étapes nommées. Le prof n'écrit jamais « implémentez la boucle
d'agent » sans exemple travaillé préalable.

### P5. Exemple travaillé d'abord, puis exercice semblable, puis estompage

La revue d'Atkinson et al. montre que le transfert progresse quand on présente
au moins deux exemples par type de problème, et cite la recommandation de faire
suivre un exemple d'un problème similaire à résoudre aussitôt [Atkinson00].
Brown et Wilson recommandent des exemples travaillés avec sous-objectifs
étiquetés [Brown18] ; Wilson décrit les exemples « estompés » (des étapes
clés effacées progressivement) [Wilson19]. Chez nous : un premier outil
(`GetOrderStatus`) entièrement écrit, un second (`CancelOrder`) avec des trous,
un troisième à écrire seul.

### P6. Ne pas sur-expliquer à des développeurs confirmés

L'effet d'inversion d'expertise : un guidage utile aux novices devient
redondant, voire nuisible, quand l'apprenant en sait plus ; le guidage doit
s'estomper avec l'expertise [Kalyuga03]. Nos apprenants connaissent Laravel :
on ne réexplique pas les routes ni Eloquent, on renvoie à un encart
« rappel » optionnel. Le guidage des TP diminue de S1.4 (très guidé) à S4.4
(consignes et critères seulement).

### P7. Supprimer tout ce qui n'aide pas à apprendre

Principe de cohérence de Mayer : on apprend mieux quand le matériel superflu
est retiré (18 tests sur 19, effet médian d = 0,86) [Mayer23]. Pas d'anecdote
historique sur les LLM « pour faire joli », pas de musique sous la voix, pas de
capture d'écran décorative. Une anecdote reste si elle sert la notion.

### P8. Signaler la structure

Principe de signalement : titres, plan annoncé, mots-clés mis en évidence,
accent de la voix sur les termes clés (26 tests sur 28, d = 0,70) [Mayer23].
À l'écrit : un plan de trois lignes en tête de section. En vidéo : surlignage
de la ligne de code dont on parle, flèche sur le schéma.

### P9. Découper et pré-enseigner le vocabulaire

Segmentation (d = 0,67) et pré-entraînement (présenter les concepts clés avant
la leçon, d = 0,78) [Mayer23]. Avant la vidéo sur la boucle d'agent, l'écrit a
déjà défini « appel d'outil », « tour de conversation », « résultat d'outil ».
Les vidéos font moins de 6 minutes quand c'est possible [Guo14][Brame16].

### P10. Parler à l'apprenant, pas de l'apprenant

Principe de personnalisation : un style conversationnel (« votre contrôleur »
plutôt que « le contrôleur ») produit un meilleur transfert (13 tests sur 15,
d = 1,00), avec une réserve : l'effet peut disparaître pour des apprenants
expérimentés ou des leçons longues [Mayer23]. On garde le vouvoiement de la
charte, sur un ton direct, sans familiarité forcée.

### P11. Faire récupérer en mémoire, souvent

Se tester améliore la rétention à une semaine bien plus que relire, même si la
relecture donne plus confiance [Roediger06]. Wilson conseille une vérification
d'une ou deux minutes toutes les 10 à 15 minutes [Wilson19]. Chaque section du
support écrit se termine par un mini-exercice ; chaque vidéo de plus de
4 minutes propose une question avant la fin.

### P12. Espacer et entrelacer

Dunlosky et al. évaluent dix techniques d'étude, dont le test de pratique et la
pratique distribuée, et notent que les manuels regroupent souvent les exercices
en fin de chapitre au lieu de les répartir [Dunlosky13]. Chez nous : chaque
séance commence par deux questions sur la séance précédente, et le test final
mélange les séances au lieu de les présenter bloc par bloc.

### P13. Le test de positionnement est aussi un outil d'apprentissage

L'effet de prétest : répondre (même faux) à des questions avant de lire un texte
améliore l'apprentissage des notions testées, par rapport à un temps de lecture
plus long [Richland09]. Le test de positionnement pose donc aussi quelques
questions sur le contenu du cours, pas seulement sur les pré-requis, et
annonce que l'échec est attendu.

### P14. Un corrigé dit où l'on va, où l'on en est, et quoi faire ensuite

Hattie et Timperley : un retour efficace répond à trois questions (où vais-je,
où en suis-je, et après ?) et agit au niveau de la tâche, du processus ou de
l'autorégulation ; l'éloge centré sur la personne a peu d'effet [Hattie07].
Nos corrigés n'écrivent pas « Bravo ! » : ils expliquent la solution, la
démarche, et ce que l'apprenant doit revoir s'il s'est trompé.

### P15. Coder devant l'apprenant, erreurs comprises

Le live coding est recommandé plutôt que des diapositives de code : il ralentit
l'enseignant, montre l'ordre réel d'écriture et la façon de diagnostiquer une
erreur [Brown18][Wilson19]. Wilson en fait sa règle principale : assumer ses
erreurs et les raisonner à voix haute [Wilson19]. Nos vidéos de démo et de
correction gardent les erreurs qui enseignent quelque chose.

### P16. Des tâches authentiques et des victoires rapides

Wilson rappelle que la réussite motive plus que les encouragements, et propose
d'enseigner d'abord ce qui est rapide à maîtriser et immédiatement utile
[Wilson19]. Chez nous : dès S1.3, l'apprenant change de fournisseur d'IA en
changeant une ligne de configuration. C'est la victoire rapide qui rend
crédible toute l'architecture par ports et adaptateurs.

### P17. Des sous-titres activables, pas du texte redondant à l'écran

Plus de cent études montrent que les sous-titres améliorent compréhension,
attention et mémorisation, surtout pour les non-natifs et les personnes sourdes
ou malentendantes [Gernsbacher15]. Le principe de redondance de Mayer
(ne pas ajouter de texte qui répète la narration) n'a qu'un effet faible et
peu stable (8 tests sur 12, d = 0,10) [Mayer23]. Conclusion pratique :
sous-titres obligatoires en fichier `.srt`/`.vtt` activable, mais pas de
paragraphes incrustés qui répètent ce que dit la voix.

### P18. Penser la vidéo comme un format en soi

Guo et al. (6,9 millions de sessions edX) : vidéos courtes plus regardées
(médiane d'engagement de 6 minutes au plus), cadre informel plus engageant
qu'un studio, insertion du visage entre les diapositives utile, débit rapide
et enthousiaste plus engageant ; les tutoriels sont revus et parcourus, donc
il faut les rendre faciles à reprendre [Guo14]. Brame en tire : signalement,
segmentation, langage conversationnel et questions associées à la vidéo
[Brame16].

## 2. Écrire comme un prof

### 2.1 Budget

Le cours vise environ 30 pages de 4 000 signes, soit 120 000 signes, dont
20 % au plus de code et d'illustrations. Avec 19 séquences, cela fait
en moyenne 6 000 signes de texte par séquence, soit une page et demie. Une
séquence théorique (S2.1, S4.1) peut en prendre 9 000, un TP 3 000 (le
reste est dans le dépôt). Le prof compte avant de rendre.

### 2.2 Structure d'une section (gabarit)

Chaque section de `cours.md` suit six temps. Les intitulés ci-dessous sont
pour le prof : dans le texte publié, on n'écrit pas « Accroche », on écrit
le contenu.

1. **Le problème (3 à 6 lignes).** Une situation concrète que l'apprenant
   reconnaît, avec un détail technique précis : une requête, un temps de
   réponse, un message d'erreur, un coût. Elle se termine par la question à
   laquelle la section répond. Pas de définition à ce stade (P3, P10).
2. **L'explication (le cœur).** On nomme la notion, on la définit en gras à sa
   première apparition (charte), et on dit pourquoi elle résout le problème.
   Un paragraphe, une idée. Un schéma s'il y a un flux (requête, boucle,
   pipeline) ; il est construit par nous et légendé.
3. **L'exemple travaillé.** Code court (20 à 40 lignes), langage déclaré,
   découpé en étapes nommées par des commentaires de sous-objectif
   (`// 1. Décrire l'outil`, `// 2. Exécuter`, `// 3. Renvoyer le résultat`)
   [Brown18]. On montre l'exécution et le résultat, pas seulement le code.
4. **Le piège fréquent.** L'erreur que font vraiment les développeurs, avec sa
   cause. On la tire des retours de relecture, des tickets, des forums ou de
   sa propre expérience [Wilson19]. Format : « On voit souvent… ; le problème,
   c'est que… ; à la place… ».
5. **Le mini-exercice (2 à 5 minutes).** Une prédiction (« que renvoie cet
   appel si… ? »), un problème de Parsons (remettre des lignes dans l'ordre),
   un exemple à trous, ou un classement. La réponse est donnée juste après,
   repliée ou en fin de section (P5, P11).
6. **Le récap (3 points au plus).** Ce qu'il faut retenir, formulé comme des
   règles d'action, puis une phrase qui ouvre sur la section suivante.

Règles transverses :

- **Concret avant abstrait**, comme dans la skill vidéo : le cas d'abord, le
  terme ensuite.
- **Annoncer le plan** de la section en une ou deux phrases (P8).
- **Une seule notion nouvelle par section.** Si on en introduit deux, on coupe.
- **Expliquer le comportement par le mécanisme.** Quand l'IA invente une
  source, on explique pourquoi à partir de son fonctionnement, comme le fait
  ScienceEtonnante (section 6), au lieu de le constater.
- **Dire ce qu'on ne sait pas.** Sur la sécurité des LLM, certaines questions
  n'ont pas de solution connue ; on le dit (voir Simon Willison, section 6).
- **Nommer la limite de l'analogie** juste après l'avoir donnée (voir
  Karpathy, section 6).
- **Reporter explicitement** ce qui sera vu plus tard (« on le construit en
  séance 3 »), au lieu de l'esquiver.
- **Pas de remplissage** : ni « Il est important de noter que », ni
  « Dans cette section, nous allons voir ». On le fait, on ne l'annonce pas
  deux fois.

### 2.3 Exemple avant / après (S2.1, le tool calling)

**Avant** (style encyclopédique, à éviter) :

> Le function calling, ou tool calling, est une fonctionnalité proposée par
> les principaux fournisseurs de modèles de langage. Elle permet au modèle de
> générer des appels de fonctions structurés selon un schéma JSON défini par
> le développeur. Il est important de noter que cette fonctionnalité présente
> de nombreux avantages en termes d'intégration. Dans cette section, nous
> allons étudier son fonctionnement en détail.

Ce qui ne va pas : aucun problème posé, définition d'entrée, une phrase vide
(« il est important de noter »), une annonce au lieu d'un contenu, aucune
action pour l'apprenant.

**Après** (style visé) :

> Un client écrit dans le chat de votre boutique : « Où en est ma commande
> 1042 ? ». Le modèle ne connaît pas votre base de données. Laissé seul, il
> répondra quelque chose de plausible, et probablement faux. Comment lui
> donner accès au vrai statut sans lui ouvrir la base ?
>
> La réponse s'appelle le **tool calling** (_appel d'outil_). Vous décrivez au
> modèle les actions disponibles : un nom, une description, le format des
> paramètres. Le modèle ne les exécute pas. Il répond « je voudrais appeler
> `get_order_status` avec `order_id = 1042` », et c'est votre code qui décide
> de l'exécuter, puis qui lui renvoie le résultat.
>
> ```php
> // 1. Décrire l'outil : c'est le contrat lu par le modèle
> final class GetOrderStatus implements Tool
> {
>     public function name(): string { return 'get_order_status'; }
>
>     public function description(): string
>     {
>         return "Renvoie le statut d'une commande à partir de son numéro.";
>     }
>
>     public function parameters(): array
>     {
>         return [
>             'type' => 'object',
>             'properties' => ['order_id' => ['type' => 'integer']],
>             'required' => ['order_id'],
>         ];
>     }
>
>     // 2. Exécuter : votre code, vos règles d'accès
>     public function __invoke(array $args): array
>     {
>         $order = $this->orders->find($args['order_id']);
>         return ['status' => $order?->status ?? 'inconnue'];
>     }
> }
> ```
>
> **Piège fréquent.** On lit souvent « l'IA a supprimé la commande ». Non :
> votre application l'a supprimée, parce qu'elle a exécuté sans vérifier ce
> que le modèle proposait. Le contrôle d'accès se fait dans `__invoke`, pas
> dans le prompt.
>
> **À vous.** La description devient « Gère les commandes ». Que risque-t-il
> de se passer quand le client écrit « annule ma commande 1042 » ? Notez votre
> réponse avant de lire la suite.
>
> **À retenir.** Le modèle propose, l'application exécute. La description
> d'un outil est une spécification : elle se relit comme du code. Les droits
> se vérifient côté code, jamais dans le prompt. Dans la section suivante,
> vous écrivez la boucle qui renvoie le résultat au modèle.

Ce que l'exemple applique : problème vécu (P3), définition au moment où elle
sert, sous-objectifs dans le code (P5), piège tiré d'une confusion réelle
(P15), prédiction (P11), récap sous forme de règles (P14). Le code est un
exemple de démonstration (interface `Tool` maison, conforme au choix « sans
SDK ») à adapter au dépôt réel.

### 2.4 Encarts

- **« Si vous connaissez déjà »** : renvoi pour sauter un rappel (P6).
- **« Pour aller plus loin »** : approfondissements non évalués (déjà prévu
  dans la scénarisation). Une phrase pour dire pourquoi c'est utile, un lien.
- **« Côté SDK »** : comparaison avec le Laravel AI SDK et Spring AI, toujours
  _après_ que l'apprenant a écrit sa version (P4, P5).

## 3. Scripts vidéo naturels

La skill `script-video` couvre déjà le parlé (une phrase par souffle, « vous »
dès la première phrase, concret avant abstrait, listes dites en phrases, fin sur
une action, lecture chronométrée). Ce qui suit la complète sur cinq points :
le débit, la durée et le découpage, la structure selon le format, le live
coding, et le lien avec l'écrit et les sous-titres.

### 3.1 Débit : garder 140 mots/min pour budgéter, ne pas ralentir à l'oral

La skill fixe 140 mots par minute pour calculer la longueur d'un script. On
garde ce chiffre comme **budget** : il laisse de la marge pour les silences,
les démonstrations et les incrustations. Mais il ne faut pas en faire une
consigne de diction. Dans l'étude edX, le débit allait de 48 à 254 mots/min
(moyenne 156) et, à durée égale, l'engagement augmentait avec le débit ; les
auteurs conseillent de rassurer les enseignants : inutile de ralentir
volontairement [Guo14].

Mesure faite pour ce document (nombre de mots de la transcription divisé par
la durée, transcriptions automatiques, donc ordre de grandeur seulement) :

| Vidéo | Langue | Mots | Durée | Débit approx. |
|---|---|---|---|---|
| Lior Chamla, « On recrée Symfony #1 » | fr | 5 578 | 25:45 | ~215 mots/min |
| Grafikart, TP Agence immo (Laravel 10) | fr | 8 908 | 45:03 | ~200 mots/min |
| ScienceEtonnante, ChatGPT | fr | ~5 300 | ~27 min | ~195 mots/min |
| Machine Learnia, ML#1 | fr | 1 339 | 7:31 | ~180 mots/min (musique comprise) |
| Laracasts, 30 Days Ep 01 | en | 1 506 | 8:40 | ~175 mots/min (musique comprise) |
| Fireship, Laravel in 100 Seconds | en | 471 | 2:21 | ~200 mots/min |
| Karpathy, Intro to LLMs | en | 12 151 | 59:48 | ~205 mots/min |

Conséquence pratique : un script de 6 minutes à 140 mots/min (840 mots) dit
naturellement durera plutôt 4 min 30 à 5 min. Tant mieux : la marge sert aux
démonstrations. En screencast, on compte uniquement le texte parlé et on
ajoute le temps de frappe et d'exécution, estimé en répétant la démo.

### 3.2 Durée et découpage

- **Cible 4 à 6 minutes**, plafond FYC 8 minutes. Au-delà de 6 minutes, la
  médiane de visionnage ne progresse plus, et au-delà de 9 minutes on regarde
  souvent moins de la moitié [Guo14].
- **Une vidéo = un objectif.** Si le script a deux « ce qu'il faut retenir »,
  on fait deux vidéos.
- **Points de vigilance dans la scénarisation actuelle.** S3.3 prévoit
  20 minutes de « correction guidée » et S5.3 une vidéo de correction du cas
  pratique de 15 minutes : avec le plafond de 8 minutes, il faut découper en
  deux ou trois vidéos chapitrées (par exemple : instrumentation, plan de
  repli, ce qu'on voit quand on coupe le réseau), le reste du temps étant de
  l'auto-évaluation. À signaler au groupe.
- **Tutoriels : prévoir la reprise.** Les tutoriels sont revus et parcourus
  plus que les cours [Guo14] : chapitres horodatés dans la description,
  titres de sous-étapes à l'écran, et rappel dans le support écrit du
  minutage (« la gestion du timeout est à 3:40 »).

### 3.3 Structure selon le format

**Face caméra (présentation, intro de séquence, conclusion).**
Ouverture par une situation ou une contradiction (ScienceEtonnante ouvre sur
deux avis caricaturaux opposés sur ChatGPT, section 6), puis la promesse de
la vidéo en une phrase, une seule idée développée, et une action. Le visage
aide l'engagement quand il alterne avec les diapositives [Guo14], et des
gestes et un regard naturels favorisent l'apprentissage (principe
d'incarnation) [Mayer23]. Le cadre peut être simple : un tournage informel
n'est pas moins efficace qu'un studio [Guo14].

**Screencast de démonstration ou de correction.** Trame observée chez
Grafikart et Lior Chamla, et cohérente avec Merrill [Merrill02] :

1. Montrer le résultat final (Grafikart présente l'application terminée
   avant d'écrire une ligne).
2. Dire l'objectif et inviter à mettre en pause pour essayer d'abord
   (Grafikart : « essayer de faire une partie ou la totalité de cet exercice
   par vous-même », avec des chapitres pour retrouver un passage).
3. Construire par petits pas, en exécutant souvent.
4. Provoquer le problème avant d'apporter la solution (Lior Chamla lance le
   code naïf, montre la notice PHP puis le test PHPUnit qui échoue, et
   seulement ensuite introduit HttpFoundation).
5. Récapituler ce qui a changé et annoncer la suite.

**Schéma animé ou tableau.** Dessiner pendant qu'on parle plutôt que montrer
un schéma déjà complet : le principe d'incarnation cite une étude où voir
l'enseignant dessiner en parlant donne de meilleurs résultats que des gestes
vers un schéma déjà dessiné [Mayer23]. Guo observe aussi que les tutoriels
dessinés à la tablette (style Khan) sont plus regardés que des diapositives ou
des screencasts de code, et recommande du mouvement et un flux visuel
continu [Guo14]. Pour nous : le schéma de la boucle d'agent se construit
flèche par flèche, synchronisé avec la voix (contiguïté temporelle).

### 3.4 Live coding enregistré

Règles tirées de Wilson [Wilson19], adaptées à la vidéo :

- **Pas de copier-coller de gros blocs** : on tape, ou on révèle le code
  bloc par bloc en le commentant. Un copier-coller fait aller trop vite.
- **Dire ce qu'on fait, puis montrer le résultat** : « j'ajoute le timeout à
  10 secondes… je relance… et voilà l'exception ».
- **Garder les erreurs qui enseignent**, couper celles qui n'enseignent rien
  (faute de frappe sans intérêt). Raisonner à voix haute : lire le message
  d'erreur, formuler une hypothèse, vérifier. Karpathy, dans « Let's build
  GPT », annonce que le code « ne va pas tourner », montre le message
  d'erreur, puis ouvre la documentation de PyTorch pour comprendre.
- **Erreurs volontaires prévues au script** quand elles sont le sujet :
  appel à l'IA dans le contrôleur qui bloque (S1.2), retry infini (S3.3),
  injection indirecte qui passe (S4.2). On les marque `[Erreur voulue]`
  dans le script pour que le monteur ne les coupe pas.
- **Faire prédire** avant d'exécuter : « avant que je lance, à votre avis,
  combien d'appels partent ? ». Une pause, puis l'exécution [Brown18].
- **Environnement de l'apprenant** : Wilson demande un environnement qui
  ressemble à celui des apprenants (pas de prompt de terminal personnalisé ni
  de raccourcis exotiques) et une police agrandie, quitte à n'avoir que 60 à
  70 colonnes à l'écran en salle [Wilson19]. Pour nos vidéos, notre réglage
  (non tiré d'une source) : Laravel par défaut, thème clair ou très
  contrasté, police de l'éditeur autour de 18 à 20 pt.
- **Revenir en arrière à l'écran** si la sortie a fait défiler le code.

### 3.5 Signaler sans réciter

La skill interdit « Un : … Deux : … » et les titres lus. Le principe de
signalement demande pourtant un plan annoncé et des mots-clés accentués
[Mayer23]. Les deux se concilient : on annonce le chemin en une phrase
naturelle (« on va casser ce contrôleur, comprendre pourquoi, puis le
réparer »), et la structure numérotée va à l'écran, pas dans la bouche.

### 3.6 Écrit et vidéo : qui fait quoi

- La **vidéo** sert ce que l'écrit montre mal : un flux qui bouge (boucle
  d'agent), un comportement dans le temps (timeout, coupure réseau), une
  démarche de diagnostic, une personne qui justifie un choix.
- L'**écrit** porte les définitions, le code de référence, les tableaux de
  comparaison et les corrigés détaillés.
- Chaque vidéo est **annoncée dans l'écrit** par sa question et suivie d'une
  question de vérification (P11) [Brame16].
- Le **script sert de base aux sous-titres** : il est relu contre la
  transcription automatique, avec une liste de termes à vérifier
  (« Laravel », « pgvector », « Ollama », « embedding », « retry »). Les
  sous-titres restent activables (P17).

## 4. Évaluations

### 4.1 Règles communes

- **Chaque item est rattaché à un objectif** de la scénarisation et à un
  niveau de Bloom révisée, noté dans un commentaire Markdown au-dessus de la
  question (`<!-- obj: S3.1 / appliquer -->`) [Biggs14][Krathwohl02].
- **On écrit le corrigé avant les distracteurs** [Unisciel22].
- **Aucune question ne porte sur ce qui n'a pas été enseigné ni pratiqué**
  [Wilson19].
- **Situations nouvelles** pour viser plus que la mémoire : on reformule, on
  change le contexte métier (« une application de réservation » plutôt que
  l'exemple exact du cours) [Haladyna02].

### 4.2 Test de positionnement

- **But double** : vérifier les pré-requis (PHP objet, injection de
  dépendances Laravel, HTTP et REST, Git) et amorcer le cours par l'effet de
  prétest (quelques questions sur des notions du cours) [Richland09].
- **12 à 15 questions, 10 minutes, non noté.** On le dit en tête : « Il est
  normal de ne pas savoir répondre aux questions 10 à 15 ».
- **Une option « Je ne sais pas »** sur les questions de contenu, pour ne pas
  pousser au hasard ; Wilson la recommande pour les évaluations formatives
  [Wilson19].
- **Retour orienté action** : pour chaque bloc raté, un renvoi précis
  (« revoyez l'injection de dépendances : documentation Laravel, section
  Service Container ») [Hattie07].

### 4.3 Exercice de fin de chapitre (au moins 2 non-QCM)

Formats adaptés à des développeurs, du plus guidé au plus ouvert :

| Format | Exemple dans le cours | Niveau visé |
|---|---|---|
| Prédiction | Que renvoie la boucle d'agent si l'outil lève une exception ? | Comprendre |
| Problème de Parsons | Remettre dans l'ordre les lignes du retry avec délai croissant | Appliquer |
| Exemple estompé | Compléter l'adaptateur Ollama à partir de l'adaptateur en ligne | Appliquer |
| Diagnostic sur traces | Trouver dans ces logs pourquoi la requête a coûté 0,40 € | Analyser |
| Classement argumenté | Quels outils exposeriez-vous à l'agent ? Pourquoi ? | Évaluer |
| Production courte | Rédiger l'entrée « stratégie de test » de la fiche d'architecture | Créer |

Les problèmes de Parsons demandent moins de temps pour des résultats
équivalents [Wilson19]. Format de fichier : celui de `guide-de-style.md`
(Objectif, Durée, Énoncé, Corrigé).

### 4.4 QCM (chapitres et test final)

Règles issues de la revue de Haladyna et al. [Haladyna02] et du guide
Unisciel [Unisciel22] :

1. **Un seul acquis par question**, et l'idée centrale dans l'énoncé, pas
   dans les réponses.
2. **Une vraie question**, courte, à la forme active, sans négation. Si une
   négation est indispensable, elle est en gras et en capitales (« Lequel
   n'est **PAS** … ? »).
3. **Pas de décor inutile** dans l'énoncé, mais tous les éléments nécessaires
   pour répondre.
4. **Trois ou quatre propositions.** Haladyna juge trois options suffisantes
   dans la plupart des cas, l'effort pour un troisième distracteur plausible
   ne valant souvent pas la peine ; Unisciel conseille au plus quatre
   propositions et deux distracteurs sauf bonne raison. Le format de la
   charte (A à D) reste possible, mais on ne force pas un quatrième choix
   absurde.
5. **Des distracteurs plausibles tirés d'erreurs réelles**, chacun
   correspondant à une conception erronée identifiable (« pouvoir
   diagnostique ») [Wilson19]. Exemple : « le RAG empêche les
   hallucinations » est un bon distracteur, parce que c'est une croyance
   répandue que le cours combat.
6. **Ni « toutes les réponses » ni « aucune des réponses »**, pas de question
   piège, propositions homogènes et de longueur comparable, bonne réponse
   placée à des positions variées.
7. **L'explication couvre la bonne réponse et chaque distracteur** : pourquoi
   il est tentant, pourquoi il est faux [Unisciel22].
8. **Humour : à éviter dans les réponses.** Wilson note que les réponses
   « drôles » n'apportent rien au diagnostic et font rarement rire
   [Wilson19].

Exemple :

```markdown
## Question 12
<!-- obj: S3.1 / appliquer -->

Votre agent appelle une IA en ligne facturée à l'appel. La politique de retry
est : 3 tentatives, délai doublé à chaque échec. Un incident chez le
fournisseur provoque des réponses 500 pendant 2 minutes. Quel est l'effet
principal de cette politique pendant l'incident ?

- [ ] Aucun coût supplémentaire, car les appels en erreur ne sont jamais facturés.
- [x] Jusqu'à trois fois plus d'appels sortants par requête utilisateur, sans garantie de succès.
- [ ] Le coupe-circuit s'ouvre automatiquement après la troisième tentative.
- [ ] Les requêtes utilisateur sont mises en file d'attente jusqu'au retour du service.

**Explication :** un retry multiplie les appels sortants. La facturation des
appels en erreur dépend du fournisseur : ne jamais la supposer nulle. Le
coupe-circuit et la file d'attente sont d'autres mécanismes, qu'il faut
ajouter explicitement : le retry seul ne les fournit pas.
```

### 4.5 Test final (~40 QCM)

- **Matrice de spécification** avant d'écrire : 8 questions par séance
  environ, réparties par niveau (par exemple 10 % se souvenir, 25 %
  comprendre, 35 % appliquer, 30 % analyser et évaluer). Haladyna demande que
  chaque item corresponde à la grille de spécification du test
  [Haladyna02].
- **Chaque question part d'une situation** (c'est déjà la règle de la
  scénarisation) et les questions sont **mélangées entre séances** (P12).
- **Items indépendants** : la réponse à une question ne doit pas en révéler
  une autre [Haladyna02].
- **Relecture par un membre du groupe** qui répond sans le corrigé :
  toute question où il hésite entre deux réponses est réécrite.

### 4.6 Cas pratique et corrigé vidéo

- **Grille critériée publiée avec l'énoncé**, alignée sur les objectifs :
  architecture, stratégie de test, sécurité, coût, et pour chacun la qualité
  de la justification (choix, alternative écartée, raison) [Biggs14].
- **Distinguer décrire et justifier** dans la grille par des descripteurs
  concrets : « décrit » = dit ce qui est fait ; « justifie » = dit pourquoi
  et contre quelle alternative.
- **Corrigé vidéo** (découpé en vidéos de 8 min max, voir 3.2) : une fiche de
  référence commentée, les trois erreurs les plus fréquentes, et un passage
  où l'on réécrit une phrase descriptive en phrase justifiée. Le corrigé
  montre une démarche, pas seulement un résultat [Hattie07].

### 4.7 Corrigés (tous types)

Gabarit pour `### Corrigé` :

1. **La solution** (code ou réponse).
2. **Pourquoi** : la démarche, étape par étape, avec des sous-titres si le
   raisonnement a plusieurs étapes [Unisciel22].
3. **Erreurs fréquentes** et ce qu'elles révèlent.
4. **Comment vérifier soi-même** (commande de test, trace à observer).
5. **Et ensuite** : quoi revoir en cas d'échec, ou quel prolongement si
   c'est réussi (le « feed forward » de Hattie et Timperley [Hattie07]).

Pas de félicitations génériques : elles n'apportent rien [Hattie07].

## 5. Comment les cours de référence ordonnent le sujet

Plans relevés sur les pages officielles le 24/11/2026.

| Ordre | Hugging Face Agents Course [HF] | DeepLearning.AI, Agentic AI (A. Ng) [DLAI25] | Anthropic Academy, Building with the Claude API [Anth26] | Kaggle et Google, 5-Day AI Agents Intensive [Kaggle25] |
|---|---|---|---|---|
| 1 | Onboarding (outils, plateforme) | Introduction aux workflows agentiques | Accéder à l'API (requêtes, multi-tours, prompt système, sortie structurée) | Introduction aux agents, différence avec une appli LLM classique |
| 2 | Fondamentaux : outils, pensées, actions, observations ; messages et templates de chat ; fonctions Python comme outils | Pattern « réflexion » | **Évaluation de prompts** (jeu de test, notation par code et par modèle) | Outils et interopérabilité (MCP) |
| 3 | Frameworks (smolagents, LangGraph, LlamaIndex) | Utilisation d'outils | Techniques de prompt | Ingénierie du contexte : sessions et mémoire |
| 4 | Cas d'usage | Conseils pratiques pour construire de l'IA agentique | Tool use (13 leçons) | Qualité : observabilité, logs, traces, métriques, évaluation |
| 5 | Devoir final sur benchmark, classement | Patterns pour agents très autonomes (sans doute planification et multi-agents, déduit de la liste des quatre patterns annoncés) | RAG et recherche agentique | Du prototype à la production (déploiement, A2A) |
| 6 | Bonus : fine-tuning pour l'appel de fonctions ; observabilité et évaluation ; agents dans les jeux | | Fonctionnalités Claude, puis MCP, puis Claude Code et computer use, puis agents et workflows (chaînage, routage, parallélisation) | |
| Format | Unités théoriques, notebooks, devoirs, certificat | Construction « from first principles » avant les frameworks ; évaluation et analyse d'erreurs « tissées » dans tout le cours | 67 leçons, 9 h, un quiz par section | Livres blancs, codelabs, discussions en direct |

Le dépôt d'Anthropic sur GitHub (archivé) propose un ordre proche : bases de
l'API, prompt engineering, prompting en conditions réelles, **évaluations**,
puis tool use [AnthGH24].

Notre plan : S1 architecture, cinq caractéristiques de l'IA, environnement ;
S2 tool calling, boucle d'agent, RAG ; S3 résilience et observabilité ;
S4 tests, sécurité, comparaison ; S5 production et cas pratique.

Ce que la comparaison montre :

1. **Outils avant autonomie, partout.** Les quatre cours enseignent l'appel
   d'outil avant les agents autonomes ou multi-agents. Notre S2.1 avant S2.2
   suit la même logique.
2. **Principes avant framework.** DeepLearning.AI construit chaque pattern
   « from first principles » avant les frameworks ; Hugging Face fait les
   fondamentaux avant smolagents et LangGraph. Notre « sans SDK, puis
   comparaison » est dans la même ligne : c'est un argument à citer dans le
   support.
3. **L'évaluation arrive plus tôt ailleurs.** Anthropic place l'évaluation
   de prompts en deuxième section, avant même les techniques de prompt ;
   DeepLearning.AI dit tisser l'évaluation tout au long du cours. Chez nous
   elle arrive en S4.1. Recommandation : en S2.4, transformer le « journal
   des comportements observés » en 5 cas de référence écrits par l'apprenant,
   réutilisés en S4.1 et en S5.1. On ne déplace pas de séquence, on plante la
   graine plus tôt.
4. **Observabilité puis production**, comme Kaggle (jour 4 qualité et
   traces, jour 5 production). Notre S3.2 puis S5 suit cet ordre.
5. **Nos deux différences** : aucun des quatre plans ne commence par
   l'architecture logicielle (ports et adaptateurs), et aucun ne consacre un
   module entier à la sécurité dans les plans que j'ai lus. Ce sont nos
   points forts, à défendre en soutenance.
6. **Absents de notre plan** : MCP (Anthropic, Kaggle), mémoire et ingénierie
   du contexte (Kaggle), multi-agents (DeepLearning.AI, Kaggle). Ils ont leur
   place dans la vidéo de conclusion « pour aller plus loin ».
7. **Format** : un quiz par section (Anthropic) correspond à notre
   « 1 exercice par chapitre » ; le devoir final sur benchmark (Hugging Face)
   correspond à notre cas pratique.

Limite : je n'ai lu que les plans et descriptions publics, pas le contenu
des leçons.

## 6. Ton : comment enseignent des vulgarisateurs et formateurs reconnus

Dix personnes, cinq en français et cinq en anglais (dont deux
ingénieurs-conférenciers). Pour chacune : une vidéo précise, ce que j'ai pu
vérifier, et ce qu'on observe. Les débits sont mes mesures (voir 3.1).

### 6.1 Grafikart (Laravel, PHP), français

- **Vidéo** : « Découverte de Laravel 10 : TP : Agence immo, gestion des
  biens », 12/04/2023, 45:03 [GrafikartTP].
- **Vérifié** : transcription automatique complète.
- **Ouverture** : situe la vidéo dans la formation (« on ne va pas
  forcément voir de nouvelles choses aujourd'hui… mise en pratique histoire
  d'asseoir les compétences »), puis montre le site terminé avant d'écrire
  du code.
- **Adresse** : vouvoiement (« je vous propose »), « on » pour l'action
  commune. Le « tu » n'apparaît que quand il parle au code (« je veux que tu
  affiches une div »).
- **Rythme** : environ 200 mots/min, continu, sans musique.
- **Code à l'écran** : presque tout le temps ; il refactorise en direct
  (création de petits composants de formulaire) en disant pourquoi
  (éviter la duplication).
- **Erreurs** : corrigées dans le flux, sans dramatiser, avec la cause :
  « ici je me suis trompé, j'ai oublié de lui préciser que la requête… »,
  « petit oubli de ma part… la méthode était POST ».
- **Exercice** : invite explicitement à faire le TP seul avant de regarder
  la correction, chapitres à l'appui.
- **Conclusion** : bilan honnête de ce qui a pris du temps, puis programme
  précis du chapitre suivant.

### 6.2 Lior Chamla (PHP, Symfony), français

- **Vidéo** : « On recrée Symfony : épisode #1 : HTTP Foundation »,
  07/08/2020, 25:45 [Chamla20].
- **Vérifié** : transcription automatique complète.
- **Ouverture** : salutation, puis rassurance (« vous inquiétez pas c'est pas
  si compliqué que ça ») et trois buts : comprendre ce qu'est un framework,
  pourquoi on en utilise un, ce qui se passe « sous le capot ». C'est
  exactement la logique de notre TP sans SDK.
- **Source assumée** : il suit le tutoriel officiel de Fabien Potencier,
  donne le lien et invite à mettre pause pour le lire.
- **Problème d'abord** : il écrit le code naïf, montre la notice PHP, puis un
  test PHPUnit qui échoue à cause des en-têtes, et seulement après introduit
  HttpFoundation.
- **Adresse et registre** : vouvoiement collectif (« salut à tous »), très
  familier (« pourquoi est-ce qu'on se fait chier à avoir un framework ») ;
  il fait parler PHP (« écoute, tu n'as pas passé de name »).
- **Rythme** : environ 215 mots/min, le plus rapide de l'échantillon.
- **Conclusion** : une leçon générale (« même la plus petite des
  applications… c'est pas si simple »), puis appel à s'abonner.
- **Pour nous** : reprendre la structure, pas le registre (la charte demande
  un ton direct, pas familier).

### 6.3 Machine Learnia (Guillaume Saint-Cirgue), français

- **Vidéo** : « Formation Machine Learning (2019) : ML#1 », 19/06/2019,
  7:31 [MLearnia19].
- **Vérifié** : début de la transcription (environ les deux premières
  minutes) et métadonnées. Le reste n'a pas pu être récupéré.
- **Ouverture** : une question (« qu'est-ce que c'est le machine
  learning ? »), trois exemples du quotidien (recherche Google,
  reconnaissance de visages sur Facebook, recommandations YouTube, Netflix,
  Amazon), puis la définition en une phrase.
- **Adresse** : vouvoiement, « ça vous concerne ».
- **Motivation** : une phrase personnelle (« mon rêve ça serait de pouvoir
  aider les gens à acquérir cette nouvelle compétence »), puis « c'est
  parti ».
- **Analogie** : on apprend une langue à partir d'exemples de traduction,
  pour introduire l'apprentissage supervisé.
- **Ce qu'on retient** : trois exemples concrets, puis la définition. C'est
  « concret avant abstrait » appliqué à la lettre.

### 6.4 ScienceEtonnante (David Louapre), français

- **Vidéo** : « Ce qui se cache derrière le fonctionnement de ChatGPT »,
  environ 27 min [SE23]. Date : avril 2023 d'après le billet compagnon du
  14/04/2023 [SEblog23] ; date exacte de mise en ligne non vérifiée.
- **Vérifié** : transcription complète et ponctuée (vraisemblablement son
  script : on y lit la note de tournage « POSE MINIATURE »).
- **Ouverture** : deux avis caricaturaux opposés (« C'est incroyable… » /
  « C'est nul… »), puis « Oui, je sais, tout le monde a déjà beaucoup parlé
  de ChatGPT », et la promesse : distinguer GPT, le modèle, de ChatGPT, le
  produit.
- **Humour** : un faux placement de produit (« je voudrais vous parler d'un
  super VPN… non je déconne ») pour glisser l'annonce du Discord.
- **Explication par le mécanisme** : les références inventées par ChatGPT
  sont expliquées par son fonctionnement (il « se contente de générer des
  textes plausibles »), et il évoque le couplage avec une recherche dans des
  bases de données, c'est-à-dire l'idée du RAG.
- **Adresse** : vouvoiement.
- **Approfondissement délégué** : dans le billet, il dit avoir renoncé à une
  partie technique sur les transformers et renvoie vers Karpathy.
- **Conclusion** : remerciements, abonnement, Discord.

### 6.5 Laracasts (Jeffrey Way), anglais

- **Vidéo** : « 30 Days to Learn Laravel, Ep 01 : Hello, Laravel »,
  10/04/2024, 8:40 [Laracasts24].
- **Vérifié** : transcription automatique complète.
- **Ouverture** : autodérision. Il explique qu'il n'écrit presque jamais de
  script, commence à lire une intro guindée, s'interrompt (« it's so
  boring »), puis se présente naturellement : plus de dix ans de Laravel,
  intervenant au tout premier Laracon. La crédibilité passe par l'expérience,
  et la parodie illustre la règle de la skill : un script se dit, il ne se
  lit pas.
- **Adresse** : « you », « let's work through it together ».
- **Report explicite** : Composer est mentionné, puis « don't worry, we will
  cover it when we get to it ».
- **Preuve immédiate** : « don't believe me? let me show you ».
- **Alternatives nommées** : Windows, Docker et Sail, autres outils.
- **Conclusion** : « in the next video you are going to create your first
  route ».
- **Rythme** : environ 175 mots/min.

### 6.6 Andrej Karpathy, anglais

- **Vidéos** : « [1hr Talk] Intro to Large Language Models », 23/11/2023,
  59:48 [Karpathy23b] ; « Let's build GPT: from scratch, in code, spelled
  out. », 17/01/2023, 1:56:20 [Karpathy23a].
- **Vérifié** : transcription complète de la première via un site tiers ;
  premiers 50 000 caractères de la transcription de la seconde.
- **Ouverture (Let's build GPT)** : démonstration en direct de ChatGPT,
  puis la même requête relancée qui donne une réponse différente, pour
  conclure que c'est « un système probabiliste ». C'est exactement notre
  S1.2 (l'IA ne répond jamais deux fois pareil), montré au lieu d'être dit.
- **Démystification (Intro to LLMs)** : « a large language model is just
  two files ». Analogie du fichier zip d'Internet, aussitôt corrigée : ce
  n'est pas exactement un zip, car le zip est sans perte et ici la
  compression est avec perte. Plus loin : le LLM comme « processus noyau
  d'un système d'exploitation émergent », la fenêtre de contexte jouant le
  rôle de la RAM.
- **Erreurs en direct** : « this won't actually run, we get an error
  message », puis lecture de la documentation PyTorch à l'écran ; il garde
  un « oops ».
- **Adresse** : « you », « we », « let's ». Ton calme, humour discret dans
  les exemples (un article de presse sur une feuille qui tombe d'un arbre).
- **Rythme** : environ 205 mots/min (Intro to LLMs).

### 6.7 Fireship (Jeff Delaney), anglais

- **Vidéo** : « Laravel in 100 Seconds », 23/09/2022, 2:21 [Fireship22].
- **Vérifié** : transcription automatique complète.
- **Ouverture** : aucune salutation ; la définition est la première phrase.
- **Structure** : il suit une requête de bout en bout (index.php, noyau HTTP,
  middleware, routeur, contrôleur, Eloquent, Blade). C'est un bon modèle pour
  raconter notre flux contrôleur, service, domaine en S1.1.
- **Rythme** : environ 200 mots/min, très dense, extraits de code brefs à
  l'écran.
- **Conclusion** : « this has been Laravel in 100 seconds », appel à liker.
- **Limite** : format d'accroche, sans exercice ni erreur. Je n'ai pas
  vérifié l'humour visuel (mèmes) qu'on lui prête souvent : la transcription
  n'en dit rien.

### 6.8 3Blue1Brown (Grant Sanderson), anglais

- **Vidéo** : « Transformers, the tech behind LLMs | Deep Learning Chapter 5 »
  (titre initial « But what is a GPT? Visual intro to transformers »
  d'après des pages tierces), 01/04/2024, 27:14 [3B1B24].
- **Vérifié** : début de la transcription et version texte complète de la
  leçon sur 3blue1brown.com [3B1Blesson24].
- **Ouverture** : il décompose le sigle GPT mot par mot, puis « the variant
  that you and I will focus on ».
- **Contraste** : GPT-2 produit une histoire incohérente, GPT-3 une histoire
  sensée, avec le même procédé. Il avoue : « it really doesn't feel like this
  should actually work ».
- **Structure** : vue d'ensemble d'abord, puis les connaissances préalables,
  puis le détail ; report explicite (« We'll go into the details of the
  Attention Block in the next chapter »).
- **Analogie prudente** : la « température » ressemble « vaguement » à celle
  de la thermodynamique.
- **Code** : aucun ; animations continues.

### 6.9 Simon Willison, anglais (ingénieur, conférence)

- **Conférence** : « Catching up on the weird world of LLMs », North Bay
  Python, fin juillet 2023 ; version écrite annotée publiée le 03/08/2023
  [Willison23].
- **Vérifié** : version écrite complète (diapositives, notes, transcription).
- **Ouverture** : humilité (« give you the last few years of LLMs
  developments in 35 minutes. This is impossible »), puis un plan.
- **Analogie** : des extraterrestres ont laissé une clé USB qu'on « pique
  avec un bâton » pour comprendre ce qu'elle fait (il cite son auteur, Alex
  Komoroske), puis tout de suite le concret : un fichier de 4,2 Go sur son
  ordinateur.
- **Honnêteté** : « nobody knows why » sur l'émergence des capacités ; sur
  l'injection de prompt : l'assistant est « inherently gullible » et « we
  don't know how to fix this vulnerability yet! ».
- **Exemple d'attaque concret** : un e-mail demande à l'assistant « Marvin »
  de transférer les e-mails de réinitialisation de mot de passe à
  l'attaquant. C'est le genre de scénario à reprendre en S4.2.
- **Format** : la conférence devient un support écrit annoté. C'est notre
  couple vidéo et écrit.

### 6.10 Hamel Husain, anglais (ingénieur, évaluation des LLM)

- **Vidéo** : « AI Eval Concepts Explained in 15 Minutes », 10/11/2026,
  environ 14 min [Hamel26] ; billet « Your AI Product Needs Evals »,
  29/03/2024 [Hamel24].
- **Vérifié** : chapitres et description de la vidéo (transcription non
  récupérable) ; billet complet.
- **Structure de la vidéo** : distinguer évaluation produit et benchmarks de
  modèles, puis traces, analyse d'erreurs, échantillonnage des traces,
  évaluations automatiques, pièges courants, amélioration du produit. On
  regarde les données avant d'automatiser.
- **Billet** : part d'une étude de cas (Lucy, assistante immobilière chez
  Rechat), pose le problème (« comment améliorer l'IA de façon
  systématique ? »), puis trois niveaux d'évaluation. Exemple de test
  unitaire concret : une regex vérifie que la réponse ne contient pas d'UUID.
- **Ton** : affirmatif, prescriptif (« it is essential not to skip this
  step »), crédibilité par le cas réel.
- **Pour nous** : modèle direct pour S4.1 (assertions déterministes d'abord,
  jugement humain ou par modèle ensuite).

### 6.11 Non retenus ou non vérifiés

- **Underscore_** : seule la description d'une émission (« L'IA a
  discrètement franchi une étape historique », 03/07/2025, avec les
  chercheurs du benchmark GAIA) a pu être lue ; la transcription n'était
  pas accessible. Format talk-show avec invités, peu transposable à un cours
  enregistré seul. Non analysé.
- **Grafikart, vidéo d'introduction Laravel 10** (03/04/2023, 2:55) :
  transcription non récupérée, remplacée par le TP ci-dessus.
- Le téléchargement direct des sous-titres YouTube était bloqué depuis
  notre machine ; les transcriptions viennent de l'extraction de pages
  (YouTube ou site tiers). Ce sont des transcriptions automatiques, avec
  des erreurs de mots.

### 6.12 Règles de ton pour nos supports et scripts

1. **Ouvrir sur un cas ou une contradiction, pas sur un « bonjour » ni sur le
   titre.** ScienceEtonnante (deux avis opposés), Machine Learnia (trois
   usages quotidiens), Fireship (la définition dès la première phrase).
2. **Montrer le phénomène avant de l'expliquer.** Karpathy relance la même
   requête et obtient deux réponses ; Chamla fait échouer le test avant
   d'introduire la solution. Chez nous : le vrai timeout de S1.2, la vraie
   injection de S4.2.
3. **Faire construire ce qu'on utilisera ensuite.** Chamla recrée Symfony
   pour comprendre Symfony, Karpathy recode GPT. C'est la justification de
   notre TP sans SDK : la dire à l'apprenant dès S1.
4. **Donner l'analogie, puis sa limite.** Karpathy (zip, mais avec perte),
   3Blue1Brown (température « vaguement » thermodynamique). Une analogie sans
   limite devient une idée fausse.
5. **Dire ce qu'on reporte, et quand on y revient.** Jeffrey Way (« we will
   cover it when we get to it »), 3Blue1Brown (« in the next chapter »).
6. **Dire ce qu'on ne sait pas.** Simon Willison sur l'injection de prompt
   (pas de correctif connu), 3Blue1Brown (« it doesn't feel like this should
   work »). En sécurité et en évaluation, l'honnêteté est un contenu.
7. **Assumer les erreurs en direct, avec leur cause.** Grafikart (« ici je
   me suis trompé, j'ai oublié… »), Karpathy (message d'erreur, puis
   documentation). Pas d'excuse, pas de drame : erreur, cause, correction.
8. **Inviter à essayer avant de montrer la solution.** Grafikart propose de
   faire le TP seul, chapitres à l'appui. Nos vidéos de correction
   commencent par « si vous n'avez pas encore essayé, mettez en pause ».
9. **Raconter une architecture en suivant une requête.** Fireship (de
   index.php à Blade), Karpathy (le LLM comme système d'exploitation). Notre
   S1.1 suit une requête du contrôleur au domaine, puis jusqu'à l'adaptateur
   IA.
10. **Asseoir la crédibilité sur l'expérience concrète, pas sur des titres.**
    Jeffrey Way (dix ans de Laravel), Hamel Husain (le cas Rechat), Simon
    Willison (il a nommé l'injection de prompt). Pour nous : « dans notre
    fil rouge, cet appel a coûté… », des mesures réelles.
11. **Un humour léger, rare, au service du propos ; de l'autodérision plutôt
    que des blagues.** Jeffrey Way (le script lu qui l'ennuie lui-même),
    ScienceEtonnante (le faux sponsor). Jamais dans les QCM [Wilson19], et
    sans le registre familier de Chamla, contraire à notre charte.
12. **Vouvoyer l'apprenant, dire « on » pour l'action commune, finir sur
    l'étape suivante.** Les quatre francophones analysés vouvoient leur
    public ; le « tu » ne sert qu'à faire parler le code (Grafikart,
    Chamla). Fin : Laracasts et Grafikart annoncent précisément la vidéo
    suivante. Sur Teams, l'appel à s'abonner n'a pas de sens : on le
    remplace par l'action à faire.

## 7. Sources

Format demandé par le groupe : `Nom I. (année), Titre, Éditeur/Support.`
puis URL, type, date, consultation, apport. Toutes les sources ont été
ouvertes et lues (au moins partiellement, ce qui est précisé) le 24/11/2026.
Vérifier la conformité finale avec `ressources/normes-bibliographie.pdf`,
que je n'ai pas lu.

### 7.1 Recherche et guides pédagogiques

- **[Atkinson00]** Atkinson R. K., Derry S. J., Renkl A., Wortham D. (2000),
  Learning from Examples: Instructional Principles from the Worked Examples
  Research, Review of Educational Research.
  https://assess.ucr.edu/sites/default/files/2019-02/atkinsonderryrenklwortham_2000.pdf
  Article de revue (écrit), 2000, consulté le 24/11/2026.
  Apport : au moins deux exemples par type de problème, exemple suivi d'un
  problème semblable, sous-objectifs étiquetés.
- **[Biggs14]** Biggs J. (2014), Constructive alignment in university
  teaching, HERDSA Review of Higher Education, vol. 1.
  https://www.tru.ca/__shared/assets/Constructive_Alignment36087.pdf
  Article (écrit), 2014 (année déduite du volume 1, références jusqu'en
  2013), consulté le 24/11/2026.
  Apport : un verbe par acquis visé, activités et évaluation alignées sur ce
  verbe.
- **[Brame16]** Brame C. J. (2016), Effective Educational Videos: Principles
  and Guidelines for Maximizing Student Learning from Video Content,
  CBE: Life Sciences Education.
  https://www.lifescied.org/doi/10.1187/cbe.16-03-0125
  Article (écrit), 2016, consulté le 24/11/2026.
  Apport : tableau pratique (signalement, segmentation, vidéos de 6 min ou
  moins, langage conversationnel, questions associées à la vidéo).
- **[Brown18]** Brown N. C. C., Wilson G. (2018), Ten quick tips for teaching
  programming, PLOS Computational Biology.
  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006023
  Article (écrit), 05/04/2018, consulté le 24/11/2026.
  Apport : live coding, prédictions, exemples travaillés avec sous-objectifs,
  problèmes de Parsons, tâches authentiques.
- **[Clark12]** Clark R., Kirschner P. A., Sweller J. (2012), Putting Students
  on the Path to Learning: The Case for Fully Guided Instruction, American
  Educator.
  https://research.ou.nl/ws/portalfiles/portal/1027501/Putting%20students%20on%20the%20path%20-%20American%20Educator%20-%20Clark-Kirschner-Sweller.pdf
  Article de synthèse (écrit), 2012, lu partiellement (extraits), consulté
  le 24/11/2026.
  Apport : guidage explicite pour le contenu nouveau ; les projets servent à
  pratiquer.
- **[Dunlosky13]** Dunlosky J., Rawson K. A., Marsh E. J., Nathan M. J.,
  Willingham D. T. (2013), Improving Students' Learning With Effective
  Learning Techniques, Psychological Science in the Public Interest.
  https://acs.ist.psu.edu/ist521/dunloskyRMNW13.pdf
  Revue (écrit), 2013, lu partiellement (le PDF consulté est un extrait ;
  les notes d'utilité attribuées à chaque technique n'y figuraient pas et
  ne sont donc pas citées ici), consulté le 24/11/2026.
  Apport : les dix techniques étudiées, dont test de pratique et pratique
  distribuée ; exercices trop souvent regroupés en fin de chapitre.
- **[Gernsbacher15]** Gernsbacher M. A. (2015), Video Captions Benefit
  Everyone, Policy Insights from the Behavioral and Brain Sciences.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5214590/
  Article (écrit), 2015, consulté le 24/11/2026.
  Apport : plus de cent études sur l'effet positif des sous-titres sur la
  compréhension, l'attention et la mémoire.
- **[Guo14]** Guo P. J., Kim J., Rubin R. (2014), How Video Production Affects
  Student Engagement: An Empirical Study of MOOC Videos, Proceedings of the
  First ACM Conference on Learning @ Scale.
  https://www.cs.rochester.edu/hci/pubs/pdfs/edX-MOOC-video-production-and-engagement_LAS-2014.pdf
  Article de conférence (papier), 03/2014, consulté le 24/11/2026.
  Apport : 6,9 millions de sessions edX ; durée, débit, format, différence
  cours et tutoriel.
- **[Haladyna02]** Haladyna T. M., Downing S. M., Rodriguez M. C. (2002),
  A Review of Multiple-Choice Item-Writing Guidelines for Classroom
  Assessment, Applied Measurement in Education.
  https://cmapspublic3.ihmc.us/rid=1P2XTLCSS-11K09T9-BD5/Haladyna_2002_-Appl_Meas_Educ.pdf
  Revue (écrit), 2002, consulté le 24/11/2026.
  Apport : 31 règles de rédaction de QCM et leur validité ; trois options
  souvent suffisantes.
- **[Hattie07]** Hattie J., Timperley H. (2007), The Power of Feedback, Review
  of Educational Research.
  https://assess.ucr.edu/sites/default/files/2019-02/hattietimperley_2007.pdf
  Revue (écrit), 2007, consulté le 24/11/2026.
  Apport : les trois questions du retour et ses quatre niveaux ; faible
  effet de l'éloge.
- **[Kalyuga03]** Kalyuga S., Ayres P., Chandler P., Sweller J. (2003), The
  Expertise Reversal Effect, Educational Psychologist.
  https://rob.co.bb/the-expertise-reversal-effect-kalyuga-2003.pdf
  Article (écrit), 2003, consulté le 24/11/2026.
  Apport : ce qui aide le novice gêne l'expert ; estomper le guidage.
- **[Krathwohl02]** Krathwohl D. R. (2002), A Revision of Bloom's Taxonomy:
  An Overview, Theory Into Practice.
  https://centreforfacdev.ca/pdf/TLC%20Resources/A%20Revision%20of%20Bloom_s%20Taxonomy%20-%20An%20Overview.pdf
  Article (écrit), 2002, consulté le 24/11/2026.
  Apport : six processus, quatre types de connaissances, table de taxonomie.
- **[Mayer23]** Mayer R. E. (2023), Research-Based Principles for Designing
  Multimedia Instruction, in Overson C. E. et al. (dir.), In Their Own Words,
  Division 2 de l'American Psychological Association.
  https://www.unh.edu/teaching-learning-resource-hub/sites/default/files/media/2023-06/itow-research-based-principles-for-designing-multimedia-instruction-mayer.pdf
  Chapitre d'ouvrage (écrit), 2023, consulté le 24/11/2026.
  Apport : principes multimédia avec nombre de tests et tailles d'effet
  (cohérence, signalement, redondance, segmentation, personnalisation,
  incarnation, activité générative).
- **[Merrill02]** Merrill M. D. (2002), First Principles of Instruction,
  Educational Technology Research and Development.
  https://mdavidmerrill.wordpress.com/wp-content/uploads/2019/04/firstprinciplesbymerrill.pdf
  Article (écrit), 2002, consulté le 24/11/2026.
  Apport : enseignement centré sur un problème en quatre phases (activation,
  démonstration, application, intégration).
- **[Richland09]** Richland L. E., Kornell N., Kao L. S. (2009), The Pretesting
  Effect: Do Unsuccessful Retrieval Attempts Enhance Learning?, Journal of
  Experimental Psychology: Applied.
  http://learninglab.uchicago.edu/Publications_files/RichlandKornellKao.pdf
  Article (écrit), 09/2009, résumé et introduction lus, consulté le
  24/11/2026.
  Apport : répondre (même faux) avant d'étudier améliore l'apprentissage ;
  fonde notre test de positionnement.
- **[Roediger06]** Roediger H. L., Karpicke J. D. (2006), Test-Enhanced
  Learning: Taking Memory Tests Improves Long-Term Retention, Psychological
  Science.
  https://learninglab.psych.purdue.edu/downloads/2006/2006_Roediger_Karpicke_PsychSci.pdf
  Article (écrit), 2006, consulté le 24/11/2026.
  Apport : effet de test ; relire rassure mais retient moins à une semaine.
- **[Unisciel22]** Unisciel (2022), Rédiger des QCM efficaces : un guide
  Unisciel, Unisciel (diffusé sur le Moodle de l'INSA Lyon).
  https://moodle.insa-lyon.fr/pluginfile.php/267595/mod_data/content/217480/G_UNISCIEL_QCM_2022.pdf
  Guide universitaire en français (écrit), 2022, liste des 26 conseils et
  extraits lus, consulté le 24/11/2026.
  Apport : règles concrètes en français (corrigé avant les propositions,
  quatre propositions au plus, distracteurs issus d'erreurs réelles,
  explication de chaque erreur).
- **[Wilson19]** Wilson G. (2019), Teaching Tech Together: How to create and
  deliver lessons that work and build a teaching community around them,
  Taylor & Francis (version en ligne gratuite).
  https://teachtogether.tech/en/index.html
  Livre (écrit), 2019, chapitres live coding, évaluation formative,
  motivation et charge cognitive lus, consulté le 24/11/2026.
  Apport : règles de live coding, distracteurs à pouvoir diagnostique,
  exemples estompés, problèmes de Parsons, tâches authentiques.

### 7.2 Cours de référence sur les agents et LLM

- **[Anth26]** Anthropic (2026), Building with the Claude API, Claude Academy.
  https://academy.claude.com/courses/building-with-the-claude-api
  Cours en ligne (page de plan), consulté le 24/11/2026 (date de création
  non indiquée).
  Apport : ordre des sections, évaluation de prompts en deuxième position,
  un quiz par section.
- **[AnthGH24]** Anthropic (2024), Anthropic's educational courses, GitHub.
  https://github.com/anthropics/courses
  Dépôt de cours (écrit, notebooks), créé le 30/05/2024, archivé, consulté
  le 24/11/2026.
  Apport : ordre conseillé des cinq cours (API, prompting, prompting réel,
  évaluations, tool use).
- **[DLAI25]** DeepLearning.AI, Ng A. (2025), Agentic AI, DeepLearning.AI.
  https://www.deeplearning.ai/courses/agentic-ai
  Cours en ligne vidéo (page de plan), année non affichée sur la page (2025
  d'après la période de lancement, non vérifié), consulté le 24/11/2026.
  Apport : cinq modules, patterns construits « from first principles »
  avant les frameworks, évaluation tout au long du cours.
- **[HF]** Hugging Face (s. d.), AI Agents Course, unité 0 : Welcome to the
  course, Hugging Face Learn.
  https://huggingface.co/learn/agents-course/unit0/introduction.md
  Cours en ligne (écrit et notebooks), date non affichée, consulté le 24/11/2026.
  Apport : progression fondamentaux, frameworks, cas d'usage, devoir final ;
  observabilité et évaluation en bonus.
- **[Kaggle25]** Kaggle, Google (2025), 5-Day AI Agents Intensive Course with
  Google, Kaggle Learn Guide.
  https://www.kaggle.com/learn-guide/5-day-agents
  Cours (livres blancs, codelabs, vidéos), tenu en direct du 10 au
  14/11/2025, consulté le 24/11/2026.
  Apport : progression en cinq jours, de l'introduction à la production,
  qualité et observabilité au jour 4.

### 7.3 Vidéos et conférences analysées

- **[GrafikartTP]** Grafikart (2023), Découverte de Laravel 10 : TP : Agence
  immo, gestion des biens, YouTube.
  https://www.youtube.com/watch?v=vSdEqLPyTDk
  Vidéo (screencast), 12/04/2023, 45:03, transcription complète lue,
  consulté le 24/11/2026.
  Apport : TP présenté par le résultat final, invitation à essayer seul,
  erreurs corrigées en direct.
- **[Chamla20]** Chamla L. (2020), On recrée Symfony : épisode #1 : HTTP
  Foundation, YouTube (chaîne Lior CHAMLA, Web Develop Me).
  https://www.youtube.com/watch?v=RIZiOGjOsQI
  Vidéo (live coding), 07/08/2020, 25:45, transcription complète lue,
  consulté le 24/11/2026.
  Apport : recréer un framework pour le comprendre ; montrer le problème
  avant la solution.
- **[MLearnia19]** Saint-Cirgue G. (2019), Formation Machine Learning
  (2019) : ML#1, YouTube (chaîne Machine Learnia).
  https://www.youtube.com/watch?v=EUD07IiviJg
  Vidéo (face caméra et schémas), 19/06/2019 (date lue dans les résultats
  de recherche), 7:31, début de la
  transcription lu, consulté le 24/11/2026.
  Apport : exemples quotidiens avant la définition, analogie avec
  l'apprentissage humain.
- **[SE23]** Louapre D. (2023), Ce qui se cache derrière le fonctionnement de
  ChatGPT, YouTube (chaîne ScienceEtonnante).
  https://www.youtube.com/watch?v=7ell8KEbhJo
  Vidéo (vulgarisation), avril 2023 (date exacte non vérifiée), environ
  27 min, transcription complète lue, consulté le 24/11/2026.
  Apport : ouverture par une contradiction, limites expliquées par le
  mécanisme, humour bref.
- **[SEblog23]** Louapre D. (2023), Comment fonctionne ChatGPT ?, Science
  étonnante (blog).
  https://scienceetonnante.com/blog/2023/04/14/comment-fonctionne-chatgpt/
  Billet de blog (écrit), 14/04/2023, consulté le 24/11/2026.
  Apport : billet compagnon de la vidéo ; renvoi assumé vers Karpathy pour
  la partie technique.
- **[Laracasts24]** Way J. (2024), 30 Days to Learn Laravel, Ep 01 : Hello,
  Laravel, YouTube (chaîne Laracasts).
  https://www.youtube.com/watch?v=1NjOWtQ7S2o
  Vidéo (face caméra et screencast), 10/04/2024, 8:40, transcription
  complète lue, consulté le 24/11/2026.
  Apport : autodérision sur le script lu, report explicite des notions,
  fin sur la vidéo suivante.
- **[Karpathy23a]** Karpathy A. (2023), Let's build GPT: from scratch, in
  code, spelled out., YouTube.
  https://www.youtube.com/watch?v=kCc8FmEb1nY
  Vidéo (live coding), 17/01/2023, 1:56:20, début de la transcription lu
  (50 000 caractères), consulté le 24/11/2026.
  Apport : non-déterminisme montré en direct, erreurs et documentation
  lues à l'écran.
- **[Karpathy23b]** Karpathy A. (2023), [1hr Talk] Intro to Large Language
  Models, YouTube.
  https://www.youtube.com/watch?v=zjkBMFhNj_g
  Vidéo (conférence enregistrée), 23/11/2023, 59:48, transcription lue via
  https://getyoutubetranscript.com/transcript/zjkBMFhNj_g/en (site tiers),
  consulté le 24/11/2026.
  Apport : analogies (zip avec perte, système d'exploitation) avec leurs
  limites.
- **[Fireship22]** Fireship (2022), Laravel in 100 Seconds, YouTube.
  https://www.youtube.com/watch?v=rIfdg_Ot-LI
  Vidéo (animation et code), 23/09/2022, 2:21, transcription complète lue,
  consulté le 24/11/2026.
  Apport : expliquer un framework en suivant une requête.
- **[3B1B24]** Sanderson G. (2024), Transformers, the tech behind LLMs | Deep
  Learning Chapter 5, YouTube (chaîne 3Blue1Brown).
  https://www.youtube.com/watch?v=wjZofJX0v4M
  Vidéo (animation), 01/04/2024, 27:14, début de la transcription lu,
  consulté le 24/11/2026.
  Apport : vue d'ensemble avant le détail, contraste GPT-2 et GPT-3, report
  explicite.
- **[3B1Blesson24]** Sanderson G. (2024), Transformers, the tech behind LLMs
  (version texte de la leçon), 3blue1brown.com.
  https://www.3blue1brown.com/lessons/gpt
  Leçon écrite, 2024, consulté le 24/11/2026.
  Apport : structure complète de la leçon et analogie prudente de la
  température.
- **[Willison23]** Willison S. (2023), Catching up on the weird world of LLMs,
  Simon Willison's Weblog (conférence North Bay Python, version annotée).
  https://simonwillison.net/2023/Aug/3/weird-world-of-llms/
  Conférence (vidéo) et version écrite annotée, 03/08/2023, version écrite
  complète lue, consulté le 24/11/2026.
  Apport : analogie avec auteur cité, honnêteté sur les problèmes non
  résolus, exemple concret d'injection de prompt.
- **[Hamel24]** Husain H. (2024), Your AI Product Needs Evals, hamel.dev.
  https://hamel.dev/blog/posts/evals/
  Billet de blog (écrit), 29/03/2024, consulté le 24/11/2026.
  Apport : enseignement par étude de cas, trois niveaux d'évaluation,
  assertions concrètes.
- **[Hamel26]** Husain H. (2026), AI Eval Concepts Explained in 15 Minutes,
  YouTube.
  https://www.youtube.com/watch?v=3rlYBCDK0K4
  Vidéo, 10/11/2026, environ 14 min, chapitres et description lus
  (transcription non disponible), consulté le 24/11/2026.
  Apport : ordre pédagogique de l'évaluation (traces et analyse d'erreurs
  avant l'automatisation).

Total : 37 entrées (18 recherche et guides, 5 cours, 14 vidéos et écrits
de vulgarisateurs). C'est au-dessus de la fourchette visée de 15 à 30,
parce que la section 6 exige une source par vidéo analysée. Pour la
bibliographie du cours, on peut ne garder que 7.1 et 7.2, soit 23 entrées.
