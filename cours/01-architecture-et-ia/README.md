# 01 : Les bases de l'architecture web, et pourquoi l'IA les bouscule

- Durée apprenant : 135 min
- Séquences (trame V2, `livrables/scenarisation.md`) :
  - S1.1 Architectures web : les bases (40 min) : support écrit, section 1, dépôts d'exemple [notion-lite-laravel](https://github.com/sorantino/notion-lite-laravel) et [notion-lite-spring](https://github.com/sorantino/notion-lite-spring)
  - S1.2 Pourquoi l'IA complique les architectures classiques (40 min) : support écrit, section 2, étude de cas `etude/` sur [xKaan/fyc-tp](https://github.com/xKaan/fyc-tp/tree/fyc-etude-s1-2/etude), branche `fyc-etude-s1-2`, et exercice 1
  - S1.3 TP : un port, trois adaptateurs (55 min) : énoncé `TP-S1-enonce.md` sur [xKaan/fyc-tp](https://github.com/xKaan/fyc-tp), branche `fyc-tp-s1`, corrigé sur `fyc-tp-s1-correction` ; fusion des anciennes S1.3 et S1.4, l'installation est passée au chapitre 00
- Objectifs pédagogiques :
  - Reconnaître les couches d'une application web et la place du cœur métier
  - Isoler une dépendance externe derrière un port et la brancher par un adaptateur : en ligne, local et doublure de test (O1)
  - Analyser un contrôleur qui appelle une IA et relier chacun de ses points de rupture à l'une des cinq caractéristiques d'un agent IA
- Vidéos : intro S1.1 (où placer l'appel à l'IA), lecture guidée des dépôts Laravel et Spring Boot, timeout réel (S1.2), « un port, deux fournisseurs » (S1.3)
- Exercices : un mini-exercice à la fin de chaque section du support (réponse juste après), exercice 1 (fiche de réponse, corrigé), QCM de 7 questions
- Objectifs, activités et évaluations :

| Objectif | Activité | Évaluation |
|----------|----------|------------|
| Reconnaître les couches et la place du cœur métier | Sections 1.1 et 1.2 | Mini-exercices 1.1 et 1.2, QCM 1 |
| Isoler une dépendance derrière un port et un adaptateur | Sections 1.3 et 1.4, TP S1.3 | Mini-exercices 1.3 et 1.4, QCM 2, 3, 6 et 7, tests du TP |
| Analyser un contrôleur qui appelle une IA | Sections 2.1 à 2.3 | Mini-exercices 2.1 et 2.2, exercice 1, QCM 4 et 5 |
- Auteurs : Quentin Bauduin (S1.1, S1.2), Kaan Topkaya (S1.3)

## Ressources

Les pré-requis de base (routes, contrôleurs, Eloquent, conteneur de services, HTTP, Git)
sont dans la rubrique du chapitre 00. Ci-dessous, ce que le chapitre 01 manipule en plus.

| Notion | Ressource officielle | À consulter si… |
|--------|----------------------|-----------------|
| Route model binding | [Route Model Binding, Laravel 13.x](https://laravel.com/docs/13.x/routing#route-model-binding) | vous ne voyez pas comment le contrôleur de la section 1.1 reçoit la `Note` à partir de l'URL |
| Form Requests | [Form Request Validation, Laravel 13.x](https://laravel.com/docs/13.x/validation#form-request-validation) | la couche présentation de la section 1.1 cite les _Form Requests_ et vous ne les avez jamais utilisés |
| Conteneur de services : lier une interface à une classe | [Binding Interfaces to Implementations, Laravel 13.x](https://laravel.com/docs/13.x/container#binding-interfaces-to-implementations) | le `bind` de la section 1.4 ne vous est pas familier (pour l'injection automatique : [Zero Configuration Resolution](https://laravel.com/docs/13.x/container#zero-configuration-resolution)) |
| Service providers | [Service Providers, Laravel 13.x](https://laravel.com/docs/13.x/providers) | vous ne savez pas où s'enregistre `LlmServiceProvider` |
| Configuration et variables d'environnement | [Configuration, Laravel 13.x](https://laravel.com/docs/13.x/configuration) | vous ne savez pas comment `config/llm.php` lit `LLM_PROVIDER`, ni pourquoi `env()` ne s'appelle que dans `config/` (voir « Configuration Caching ») |
| Client HTTP de Laravel | [HTTP Client, Laravel 13.x](https://laravel.com/docs/13.x/http-client) | vous n'avez jamais utilisé `Http::post()`, ni réglé `timeout()` (sections 1.3 et 2.1) |
| Tests Laravel | [HTTP Tests, Laravel 13.x](https://laravel.com/docs/13.x/http-tests) | vous n'avez jamais écrit de test de fonctionnalité (les 10 tests du TP S1.3) |
| Remplacer une dépendance dans un test | [Mocking, Laravel 13.x](https://laravel.com/docs/13.x/mocking) | vous ne savez pas comment un test substitue la doublure à l'adaptateur réel dans le conteneur |
| Artisan | [Artisan Console, Laravel 13.x](https://laravel.com/docs/13.x/artisan) | la commande Artisan de la section 1.1 ou `sail artisan test` du TP ne vous dit rien |
| Laravel Sail | [Laravel Sail, Laravel 13.x](https://laravel.com/docs/13.x/sail) | vous ne savez pas lancer le dépôt de départ du TP avec `./vendor/bin/sail up -d` |
| Événements Laravel | [Events, Laravel 13.x](https://laravel.com/docs/13.x/events) | la section 1.5 évoque les événements et vous ne savez pas ce qu'est un écouteur (ils servent en séance 3) |
| Énumérations PHP | [Énumérations, manuel PHP](https://www.php.net/manual/fr/language.enumerations.php) | l'enum `Role` du port (section 1.3) vous est inconnue |
| Propriétés en lecture seule | [Propriétés, manuel PHP](https://www.php.net/manual/fr/language.oop5.properties.php#language.oop5.properties.readonly-properties) | vous ne savez pas ce que fait `public readonly` dans la classe `Message` |
| Délai d'exécution de PHP | [set_time_limit, manuel PHP](https://www.php.net/manual/en/function.set-time-limit.php) | vous pensez que `max_execution_time` coupe un appel réseau trop long (section 2.1) |
| Délai d'attente de nginx devant PHP-FPM | [Module ngx_http_fastcgi_module, nginx](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html) | vous ne savez pas d'où vient le 504 de l'étude de cas (directive `fastcgi_read_timeout`) |
| API chat des fournisseurs en ligne | [Chat Completions, API Mistral](https://docs.mistral.ai/api/endpoint/chat) | vous voulez voir le format de requête et de réponse que `HttpLlmAdapter` traduit |
| API chat d'Ollama | [Generate a chat message, Ollama](https://docs.ollama.com/api/chat) | vous voulez voir le format de requête et de réponse que `OllamaAdapter` traduit |
| Compatibilité d'Ollama avec l'API OpenAI | [OpenAI compatibility, Ollama](https://docs.ollama.com/api/openai-compatibility) | vous vous demandez pourquoi le TP écrit un adaptateur Ollama à part au lieu de réutiliser `HttpLlmAdapter` |
| Injection de dépendances en Spring Boot | [Introduction to the Spring IoC Container and Beans, Spring Framework](https://docs.spring.io/spring-framework/reference/core/beans/introduction.html) | vous lisez le dépôt notion-lite-spring et ne connaissez pas `@Component` ni `@Bean` |

<!-- Suivi interne, non exporté : FYC-5 (chapitre), séquences FYC-102 (S1.1), FYC-103 (S1.2), FYC-98 (S1.3) ; FYC-26 (support S1.1 et S1.2), FYC-27 (dépôt TP), FYC-39 (dépôts d'exemple S1.1) ; les corrections B3 et B4 du chapitre viennent dans une PR à part -->
