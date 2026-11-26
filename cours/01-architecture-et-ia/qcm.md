# QCM : chapitre 01

Sept questions sur les séquences S1.1, S1.2 et S1.3. Une seule bonne réponse par
question. Chaque question part d'une situation concrète, et l'explication
revient sur chaque option.

## Question 1
<!-- obj: S1.1 / appliquer -->

Dans une application en couches, une classe du domaine (par exemple l'entité
`Note`) a besoin de connaître la date du jour pour savoir si une note est
périmée. Quelle solution respecte la règle « les dépendances vont vers
l'intérieur » ?

- [ ] L'entité appelle directement `now()` de Laravel
- [x] L'entité reçoit la date en paramètre
- [ ] L'entité lit la date dans la base de données via Eloquent
- [ ] Le contrôleur calcule la péremption et la passe à l'entité

**Explications :**

- A : tentant parce que c'est la ligne la plus courte, mais le domaine dépend
  alors du framework et ne se teste plus sans lui.
- B : juste. Le domaine reçoit ce dont il a besoin et reste testable sans
  Laravel. Une variante équivalente : dépendre d'un port `Clock` que le domaine
  définit lui-même.
- C : le domaine dépendrait de l'infrastructure (la base) pour une simple date.
- D : la règle métier (« périmée ») quitte le domaine pour la couche
  présentation, où on ne la retrouve plus et où elle ne se réutilise pas.

## Question 2
<!-- obj: S1.1 / appliquer -->

Vous devez pouvoir basculer entre un fournisseur d'IA en ligne et un modèle
local avec Ollama. Où doit se prendre la décision de brancher l'un ou l'autre ?

- [ ] Dans le contrôleur, qui instancie le bon adaptateur
- [ ] Dans l'adaptateur en ligne, qui appelle Ollama en cas d'échec
- [ ] Dans le service `SummarizeNote`, avec un `if` sur la configuration
- [x] Dans le conteneur de dépendances, en liant l'interface `LlmPort` à l'adaptateur choisi

**Explications :**

- A : le contrôleur connaîtrait toutes les classes concrètes : le couplage que
  l'architecture hexagonale cherche à supprimer revient par la présentation.
- B : c'est une stratégie de repli (que faire quand le service tombe), pas un
  choix de branchement. Le repli est un autre sujet, en séance 3.
- C : le service connaîtrait les adaptateurs. Il ne doit connaître que le port.
- D : juste. Le branchement est un détail de configuration, et le conteneur est
  le seul endroit qui connaît à la fois le port et les adaptateurs.

## Question 3
<!-- obj: S1.1 / analyser -->

Un test unitaire de `SummarizeNote` passe une implémentation de `LlmPort` qui
renvoie toujours la chaîne « résumé de test » et garde en mémoire les messages
qu'elle a reçus. Qu'est-ce que ce test peut vérifier ?

- [x] Que le service construit le bon prompt, appelle le port et enregistre le résultat
- [ ] Que le modèle produit un bon résumé
- [ ] Que l'appel HTTP vers le fournisseur fonctionne
- [ ] Que le temps de réponse est acceptable

**Explications :**

- A : juste. Avec une doublure, on teste l'orchestration du cas d'usage. Pour
  vérifier le prompt, la doublure doit enregistrer ce qu'elle reçoit : une
  doublure qui renvoie seulement une chaîne fixe ne le permettrait pas.
- B : croyance courante. La doublure répond toujours la même chose : elle ne
  dit rien de la qualité du modèle (séance 4).
- C : aucun appel réseau n'a lieu. L'adaptateur HTTP se teste ailleurs.
- D : la doublure répond instantanément. La latence se mesure sur le vrai
  appel (séance 3).

## Question 4
<!-- obj: S1.2 / analyser -->

Une application de réservation de salles propose un bouton « Suggérer un
créneau » : le contrôleur appelle une IA et attend sa réponse, environ 10
secondes. Le serveur a 6 processus PHP-FPM. Un lundi matin, 6 personnes
cliquent sur ce bouton presque en même temps. Une seconde plus tard, une
septième ouvre la page « Mes réservations », qui n'appelle pas l'IA. Que
constate-t-elle ?

- [ ] La page s'affiche normalement, puisqu'elle ne fait aucun appel à l'IA.
- [ ] La page renvoie une erreur 429, car le fournisseur limite les appels simultanés.
- [x] La page met plusieurs secondes à s'afficher, le temps qu'un processus se libère.

**Explications :**

- A : l'erreur la plus courante. On raisonne par fonctionnalité (« cette page
  n'utilise pas l'IA »), alors que la ressource partagée est le processus, pas
  la fonctionnalité.
- B : une limite du fournisseur toucherait les appels à l'IA, pas une page qui
  ne l'appelle jamais. Et un 429 revient vite : il ne bloquerait pas les
  processus.
- C : juste. Un processus PHP-FPM traite une requête à la fois et reste occupé
  pendant toute l'attente réseau. Les six processus attendent l'IA, la septième
  requête attend son tour, quel que soit son contenu.

Si vous vous êtes trompé, relisez l'incident de 9 h dans la section 2.1. La
parade, le traitement en arrière-plan, se construit en séance 3.

## Question 5
<!-- obj: S1.2 / analyser -->

Une application de tri de tickets de support appelle un modèle par son alias
`…-latest`. Un matin, la part de tickets mal classés passe de 5 % à 15 %, et
elle y reste les jours suivants. Vous n'avez rien déployé, aucun test n'a échoué
et aucun log n'affiche d'erreur. Quelle caractéristique de l'agent IA est la
plus probablement en cause ?

- [ ] La latence variable
- [x] La dépendance à un fournisseur externe
- [ ] Le non-déterminisme
- [ ] La nouvelle surface d'attaque

**Explications :**

- A : une latence plus élevée ralentirait les réponses, elle ne changerait pas
  leur contenu.
- B : juste. Un alias désigne le modèle que le fournisseur décide, et une mise à
  jour chez lui est un déploiement que vous n'avez pas fait. Les parades :
  appeler un identifiant de modèle figé plutôt qu'un alias, mesurer la qualité
  des réponses dans le temps et préparer la migration, car un modèle figé est
  retiré un jour (séance 5).
- C : le plus tentant, car le non-déterminisme aussi fait varier les réponses.
  Mais il fait varier deux appels identiques, au hasard. Ici le niveau
  d'erreur change d'un coup et reste à son nouveau niveau : c'est un
  changement de modèle.
- D : une attaque (texte piégé dans un ticket) donnerait des réponses aberrantes
  sur certains tickets, pas une dérive générale du taux d'erreur.

## Question 6
<!-- obj: S1.3 / appliquer -->

Votre `LlmServiceProvider` lit `env('LLM_PROVIDER', 'fake')`, et `.env` contient
`LLM_PROVIDER=ollama`. En production, après `php artisan config:cache`, tous les
appels partent vers la doublure. Pourquoi ?

- [ ] Ollama n'est pas démarré sur le serveur de production
- [ ] `config:cache` désactive les service providers
- [ ] La doublure est toujours prioritaire sur les adaptateurs réels
- [x] Une fois la configuration en cache, `env()` ne lit plus le fichier `.env`

**Explications :**

- A : si Ollama était arrêté, l'adaptateur Ollama échouerait (erreur ou
  exception du port), il ne basculerait pas silencieusement sur la doublure.
- B : les service providers continuent de s'exécuter. C'est la lecture de
  `.env` qui change.
- C : rien dans le code ne donne cette priorité : la doublure n'est choisie que
  parce que la valeur par défaut `fake` est utilisée.
- D : juste. La documentation Laravel précise qu'avec la configuration en
  cache `env()` ne renvoie que les variables d'environnement du système.
  `env()` ne s'appelle que dans `config/`, le reste du code lit `config()`.

## Question 7
<!-- obj: S1.3 / appliquer -->

Dans `config/llm.php`, vous choisissez le modèle en ligne à utiliser. Quelle
valeur retenez-vous, et pourquoi ?

- [x] L'identifiant daté (`mistral-small-2603`), parce que le fournisseur ne change pas ce qu'il désigne sans prévenir
- [ ] L'alias `mistral-small-latest`, parce qu'il donne toujours la dernière version, donc la meilleure
- [ ] L'alias `mistral-small-latest`, parce qu'un identifiant daté n'est jamais retiré
- [ ] Peu importe : la version du modèle n'a pas d'effet sur les réponses

**Explications :**

- A : juste. Un identifiant daté désigne un modèle précis, ce qui rend les
  régressions attribuables et les tests plus stables. Cela ne suffit pas : le
  modèle sera retiré un jour, il faudra migrer (séance 5).
- B : « la dernière version » n'est pas « la meilleure pour votre usage », et le
  changement arrive sans test ni validation de votre côté.
- C : faux. Chaque modèle a une date de retrait, après laquelle les requêtes
  échouent.
- D : la version change le style, la qualité et parfois le format des réponses.
  C'est la leçon de l'incident de mardi (section 2.1).
