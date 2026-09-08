# QCM : chapitre 01

Cinq questions sur les séquences S1.1 et S1.2. Une seule bonne réponse par
question. Chaque question part d'une situation concrète.

## Question 1

Dans une application en couches, une classe du domaine (par exemple l'entité
`Note`) a besoin de connaître la date du jour pour savoir si une note est
périmée. Quelle solution respecte la règle « les dépendances vont vers
l'intérieur » ?

- [ ] L'entité appelle directement `now()` de Laravel
- [ ] L'entité lit la date dans la base de données via Eloquent
- [x] L'entité reçoit la date en paramètre, ou dépend d'une interface `Clock` définie dans le domaine
- [ ] Le contrôleur calcule la péremption et la passe à l'entité

**Explication :** le domaine ne doit dépendre ni du framework ni de
l'infrastructure. Recevoir la date en paramètre, ou dépendre d'un port `Clock`
que le domaine définit lui-même, garde l'entité testable sans Laravel. Faire
le calcul dans le contrôleur déplace une règle métier dans la couche
présentation.

## Question 2

Vous devez pouvoir basculer entre un fournisseur d'IA en ligne et un modèle
local avec Ollama. Où doit se prendre la décision de brancher l'un ou l'autre ?

- [ ] Dans le service `SummarizeNote`, avec un `if` sur la configuration
- [x] Dans le conteneur de dépendances, en liant l'interface `LlmPort` à l'adaptateur choisi
- [ ] Dans le contrôleur, qui instancie le bon adaptateur
- [ ] Dans l'adaptateur en ligne, qui appelle Ollama en cas d'échec

**Explication :** le service ne connaît que le port. Le branchement est un
détail de configuration qui appartient au conteneur de dépendances. Un `if`
dans le service ou une instanciation dans le contrôleur recréent le couplage
que l'architecture hexagonale cherche à supprimer. Appeler Ollama en cas
d'échec est une stratégie de repli, ce n'est pas le même sujet.

## Question 3

Un test unitaire de `SummarizeNote` passe une implémentation de `LlmPort` qui
renvoie toujours la chaîne « résumé de test ». Qu'est-ce que ce test peut
vérifier ?

- [ ] Que le modèle produit un bon résumé
- [x] Que le service construit le bon prompt, appelle le port et enregistre le résultat
- [ ] Que l'appel HTTP vers le fournisseur fonctionne
- [ ] Que le temps de réponse est acceptable

**Explication :** avec une doublure, on teste l'orchestration du cas d'usage,
pas le comportement du modèle ni le réseau. C'est justement l'intérêt : ce
test est rapide, gratuit et déterministe. La qualité du résumé et la latence
se testent autrement, en séance 4 et en séance 3.

## Question 4

Le bouton « Résumer » d'une application appelle un fournisseur d'IA
directement dans le contrôleur. Dix utilisateurs cliquent en même temps, le
serveur a huit processus PHP, chaque appel dure huit secondes. Quel est le
premier effet observable ?

- [ ] Les dix résumés sont faux
- [ ] Le fournisseur refuse les appels
- [x] Les pages sans rapport avec le résumé ne répondent plus, faute de processus libre
- [ ] La facture double

**Explication :** les huit processus sont occupés à attendre le fournisseur.
Toute requête, même une page d'accueil, attend qu'un processus se libère.
C'est la conséquence de la latence : un appel synchrone à l'IA bloque un
processus pendant toute sa durée. Le traitement en arrière-plan est la parade.

## Question 5

Le fournisseur déploie une nouvelle version de son modèle. Les résumés
produits par votre application changent de style. Aucun test n'a échoué, aucun
log ne montre d'erreur. Quelle caractéristique de l'agent IA est en cause ?

- [ ] La latence variable
- [ ] Le coût par appel
- [x] La dépendance à un fournisseur externe
- [ ] La nouvelle surface d'attaque

**Explication :** la version du modèle est décidée par le fournisseur. Une mise
à jour chez lui est un déploiement que vous n'avez pas fait et que vos tests
n'ont pas vu. Les parades sont de figer explicitement la version du modèle
dans la configuration et de mesurer la qualité des réponses dans le temps,
sujets de la séance 5.
