# Test de positionnement

Dix questions pour vérifier que vous avez les pré-requis du cours : PHP
orienté objet, bases de Laravel, HTTP et API REST, Git. Une seule bonne
réponse par question, correction automatique, aucune note enregistrée. Comptez
dix minutes.

Le test ne porte pas sur l'intelligence artificielle : aucune connaissance
n'est attendue dans ce domaine.

## Question 1 : PHP orienté objet

Que garantit une classe qui déclare `implements LlmPort` ?

- [ ] Qu'elle hérite du code de `LlmPort`
- [x] Qu'elle fournit une implémentation de chaque méthode déclarée dans l'interface `LlmPort`
- [ ] Qu'elle ne peut pas être instanciée
- [ ] Qu'elle est chargée automatiquement par Composer

**Explication :** une interface décrit un contrat, des signatures de méthodes
sans corps. La classe qui l'implémente s'engage à fournir chacune d'elles.
C'est le mécanisme sur lequel repose tout le cours : le cœur métier dépend de
l'interface, jamais de la classe concrète.

## Question 2 : PHP orienté objet

Dans ce constructeur, que fait la syntaxe utilisée ?

```php
public function __construct(private LlmPort $llm) {}
```

- [ ] Elle rend la classe abstraite
- [ ] Elle déclare une méthode privée nommée `llm`
- [x] Elle déclare une propriété privée `$llm` et l'initialise avec l'argument reçu
- [ ] Elle interdit de passer un argument au constructeur

**Explication :** c'est la promotion de propriétés du constructeur, disponible
depuis PHP 8. Une ligne remplace la déclaration de la propriété et son
affectation. Vous la verrez dans presque toutes les classes du cours.

## Question 3 : Laravel

Dans une application Laravel, où déclare-t-on qu'une requête `POST /notes`
doit être traitée par la méthode `store` de `NoteController` ?

- [ ] Dans `config/app.php`
- [x] Dans `routes/web.php` ou `routes/api.php`
- [ ] Dans le constructeur de `NoteController`
- [ ] Dans une migration

**Explication :** les fichiers de routes associent une méthode HTTP et un
chemin à une action de contrôleur. Le contrôleur ne sait pas lui-même quelle
URL le déclenche.

## Question 4 : Laravel

Vous écrivez `Note::where('user_id', $id)->get()`. À quelle brique de Laravel
faites-vous appel ?

- [ ] Blade
- [ ] Le conteneur de dépendances
- [x] Eloquent, l'ORM
- [ ] Artisan

**Explication :** Eloquent fait correspondre une classe PHP à une table et
traduit les appels en requêtes SQL. Les TP s'en servent pour lire les notes
et enregistrer les résumés.

## Question 5 : Laravel

Vous demandez `LlmPort $llm` dans le constructeur d'un service, et Laravel
vous fournit une instance sans que vous ayez écrit `new`. Quel mécanisme est
à l'œuvre ?

- [x] L'injection de dépendances par le conteneur de services
- [ ] L'héritage
- [ ] Le cache de configuration
- [ ] Les middlewares

**Explication :** le conteneur de services de Laravel résout les dépendances
déclarées dans les constructeurs. Quand il s'agit d'une interface, il faut lui
dire quelle classe fournir : c'est le rôle des `bind` dans un service
provider, et c'est là que se branchent les adaptateurs dans ce cours.

## Question 6 : HTTP

Un appel HTTP renvoie le code 504 après trente secondes d'attente. Que
s'est-il passé ?

- [ ] La ressource demandée n'existe pas
- [ ] Le client n'est pas autorisé
- [x] Un serveur intermédiaire n'a pas obtenu de réponse à temps du serveur en amont
- [ ] La requête est mal formée

**Explication :** 504 signifie *Gateway Timeout*. Le serveur qui vous répond
attendait lui-même une réponse d'un autre serveur, et a renoncé. C'est le
symptôme typique d'un appel trop long vers un fournisseur externe, sujet
central de la première séance.

## Question 7 : HTTP et API REST

Une API REST expose `GET /notes/42/summary`. Que fait cette requête ?

- [x] Elle lit le résumé de la note 42, sans rien modifier
- [ ] Elle crée un résumé pour la note 42
- [ ] Elle supprime le résumé de la note 42
- [ ] Elle remplace la note 42 par son résumé

**Explication :** en REST, `GET` lit une ressource et ne doit avoir aucun
effet de bord. La création passerait par `POST`, la suppression par
`DELETE`. Cette distinction compte quand une action déclenche un appel à une
IA : lent et coûteux, il ne doit jamais se cacher derrière un `GET`.

## Question 8 : HTTP

Dans une requête HTTP vers une API, à quoi sert l'en-tête `Authorization` ?

- [ ] À indiquer le format de la réponse attendue
- [x] À transmettre un jeton ou des identifiants qui prouvent qui fait la requête
- [ ] À fixer la durée maximale de la requête
- [ ] À choisir la langue de la réponse

**Explication :** les fournisseurs d'IA s'appellent avec une clé d'API
transmise dans cet en-tête, en général sous la forme `Bearer <clé>`. Cette clé
ne doit jamais apparaître dans le code : elle vit dans la configuration.

## Question 9 : Git

Vous avez modifié trois fichiers et vous voulez en enregistrer l'état dans
l'historique du projet. Quelle suite de commandes est correcte ?

- [ ] `git commit` puis `git add .`
- [x] `git add .` puis `git commit -m "message"`
- [ ] `git push` puis `git commit`
- [ ] `git clone` puis `git commit`

**Explication :** on prépare d'abord les fichiers (`add`), on enregistre
ensuite (`commit`). `push` envoie les commits vers le dépôt distant, `clone`
récupère un dépôt. Chaque TP vous demandera de commiter votre travail.

## Question 10 : Git

Chaque TP part d'un dépôt fourni. Vous voulez travailler dessus sans toucher
à la version de référence. Que faites-vous ?

- [ ] Vous modifiez directement les fichiers sur GitHub
- [x] Vous clonez le dépôt puis vous créez une branche pour votre travail
- [ ] Vous téléchargez le zip et vous supprimez le dossier `.git`
- [ ] Vous copiez les fichiers dans un autre projet sans Git

**Explication :** cloner puis créer une branche garde l'historique et permet
de comparer votre travail au corrigé, qui sera lui aussi une branche du même
dépôt.

## Votre résultat

- **9 ou 10 bonnes réponses :** vous avez les pré-requis. Commencez la séance
  1 après avoir suivi le guide d'installation.
- **6 à 8 :** vous pouvez suivre le cours. Relisez les explications des
  questions ratées et gardez sous la main la documentation de Laravel pour
  les points concernés, en particulier le conteneur de services (question 5),
  qui revient à chaque séance.
- **5 ou moins :** le cours risque d'être difficile à suivre. Avant de
  commencer, prenez le temps de revoir les bases de PHP objet et de Laravel
  (routes, contrôleurs, Eloquent, conteneur), et de refaire un premier
  projet simple avec Git. Les ressources sont indiquées dans la
  bibliographie, section documentation technique.
