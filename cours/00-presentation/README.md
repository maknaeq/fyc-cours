# 00 : Présentation du cours

Bloc d'ouverture du cours sur Teams. Ne contient pas de chapitre de fond.

- Durée apprenant : 45 min
- Séquences (trame V2, `livrables/scenarisation.md`) :
  - 00.1 Présentation, accroche, pré-requis (5 min)
  - 00.2 Test de positionnement (10 min)
  - 00.3 Installer et vérifier son environnement (30 min)
- Contenu :
  - Une seule vidéo : présentation du cours, de l'équipe et des pré-requis (3 min max), décision du 08/09/2026
  - Texte des pré-requis à côté de la vidéo sur Teams (repris de l'accroche et du guide d'installation)
  - Page d'accueil (`accueil.md`) : objectifs, plan des séances, pré-requis, mode d'emploi, première page lue sur Teams
  - Texte d'accroche (`livrables/accroche.md`)
  - Test de positionnement : dix questions de pré-requis corrigées (résultat sur 10), plus quatre questions de contenu annoncées comme normales à rater, option « Je ne sais pas » partout
  - Guide d'installation et script de vérification (Ollama, pgvector épinglé, clé en ligne facultative)
- Objectifs pédagogiques : aucun objectif de fond ; la sortie du chapitre est un environnement vérifié par le script (condition d'entrée en séance 1)
- Vidéos : présentation (3 min)
- Auteurs : Quentin Bauduin (00.1, 00.2), Erwin Gossin (00.3)

## Ressources

Une ligne par pré-requis annoncé. Si une question du test de positionnement vous a
posé problème, la ressource de la même ligne est la plus rapide pour vous remettre à niveau.

| Notion | Ressource officielle | À consulter si… |
|--------|----------------------|-----------------|
| Interfaces PHP (`implements`) | [Interfaces d'objet, manuel PHP](https://www.php.net/manual/fr/language.oop5.interfaces.php) | vous ne savez pas ce que garantit `implements` (question 1 du test) |
| Promotion de propriétés dans le constructeur | [Constructeurs et destructeurs, manuel PHP](https://www.php.net/manual/fr/language.oop5.decon.php#language.oop5.decon.constructor.promotion) | la syntaxe `__construct(private LlmPort $llm)` vous est inconnue (question 2) |
| Routes Laravel | [Routing, Laravel 13.x](https://laravel.com/docs/13.x/routing) | vous ne savez pas où déclarer qu'une requête `POST /notes` appelle une méthode de contrôleur (question 3) |
| Contrôleurs Laravel | [Controllers, Laravel 13.x](https://laravel.com/docs/13.x/controllers) | vous n'avez jamais écrit de contrôleur |
| Eloquent | [Eloquent: Getting Started, Laravel 13.x](https://laravel.com/docs/13.x/eloquent) | `Note::where('user_id', $id)->get()` ne vous dit rien (question 4) |
| Conteneur de services | [Service Container, Laravel 13.x](https://laravel.com/docs/13.x/container#binding-interfaces-to-implementations) | vous ne savez pas comment Laravel fournit une instance à un constructeur, ni comment il choisit la classe derrière une interface (question 5) |
| Codes de réponse HTTP | [Codes de réponse HTTP, MDN](https://developer.mozilla.org/fr/docs/Web/HTTP/Reference/Status) | vous ne savez pas distinguer un 4xx d'un 5xx, ni ce que signifie un 504 (question 6) |
| Méthodes HTTP et API REST | [Méthodes de requête HTTP, MDN](https://developer.mozilla.org/fr/docs/Web/HTTP/Reference/Methods) | vous hésitez sur ce que fait `GET` par rapport à `POST` ou `DELETE` (question 7) |
| En-tête `Authorization` | [Authorization, MDN](https://developer.mozilla.org/fr/docs/Web/HTTP/Reference/Headers/Authorization) | vous n'avez jamais envoyé de clé d'API dans une requête (question 8) |
| Enregistrer des modifications avec Git | [Enregistrer des modifications dans le dépôt, Pro Git](https://git-scm.com/book/fr/v2/Les-bases-de-Git-Enregistrer-des-modifications-dans-le-dépôt) | l'ordre `git add` puis `git commit` n'est pas clair (question 9) |
| Cloner un dépôt et créer une branche | [Les branches en bref, Pro Git](https://git-scm.com/book/fr/v2/Les-branches-avec-Git-Les-branches-en-bref) | vous ne savez pas comment partir d'un dépôt fourni sans toucher à la version de référence (question 10). Pour le clonage : [Démarrer un dépôt Git](https://git-scm.com/book/fr/v2/Les-bases-de-Git-Démarrer-un-dépôt-Git) |
| Vue d'ensemble de HTTP | [Un aperçu de HTTP, MDN](https://developer.mozilla.org/fr/docs/Web/HTTP/Guides/Overview) | vous voulez revoir les bases du protocole avant les questions 6 à 8 |

<!-- Suivi interne, non exporté : FYC-10 (chapitre), séquences FYC-100 (00.1), FYC-101 (00.2), FYC-97 (00.3) ; FYC-30 (vidéo), FYC-44 (page d'accueil), FYC-117 (questions de contenu), FYC-29 (installation), FYC-38 (script de vérification) -->
