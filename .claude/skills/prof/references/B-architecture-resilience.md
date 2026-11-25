# Thème B : architecture d'une application web intégrant un LLM, résilience, IA locale ou en ligne, état des SDK

Séquences couvertes : S1.1, S1.2, S1.3, S1.4, S2.2 (exposition API), S3.1, S4.3.
Recherche faite le 24/11/2026. Toutes les sources ont été ouvertes et lues (pages web,
fichiers de documentation bruts sur GitHub, code source des packages au tag indiqué).
Les limites de vérification sont signalées dans chaque entrée.

## 0. État des versions au 24/11/2026 (à jour, à corriger dans la bibliographie du cours)

| Élément | Version actuelle vérifiée | Ce que dit `livrables/bibliographie.md` | Action |
|---|---|---|---|
| Laravel AI SDK (`laravel/ai`) | **v1.4.2** (tag GitHub publié le 24/11/2026). v1.0.0 le 23/09/2026. v0.1.0 le 05/02/2026 | « version 0.x » | **Obsolète** : passer à 1.x, signaler les ruptures de la 1.0 |
| Laravel framework | 13.44.1 (24/11/2026). Laravel 13 sorti le 17/03/2026, PHP 8.3 à 8.5 | Laravel 13 | OK |
| Spring AI | **2.1.0 GA** (20/11/2026, sur Spring Boot 4.2) ; 2.0.3 en parallèle | « version 2.0.1 » | **Obsolète** : passer à 2.1.0 |
| Ollama | **v0.40.18** (24/11/2026) | « version 0.34.0 » | **Obsolète** |
| Resilience4j | 2.4.0, publiée le **14/03/2026** | « (2024), version 2.4.0 » | Corriger l'année (2026) |
| Prism PHP | v0.103.0 (07/11/2026), toujours en 0.x | absent | Ajouter si cité ; `laravel/ai` ne dépend plus de Prism depuis v0.6.1 (21/04/2026) |

## 1. Savoir de référence

1. **Ports et adaptateurs : l'intention d'origine est la testabilité, pas le dessin.** Cockburn
   formule l'intention ainsi : permettre à l'application d'être pilotée aussi bien par des
   utilisateurs que par des programmes, des tests automatisés ou des scripts batch, et d'être
   développée et testée isolément de ses périphériques et bases de données. Un port est une
   « conversation qui a un but » ; plusieurs adaptateurs peuvent se brancher sur le même port,
   dont un adaptateur de test en mémoire. Il distingue côté primaire (acteurs qui pilotent
   l'application) et côté secondaire (acteurs pilotés : base, fournisseur d'IA). La forme
   hexagonale n'a pas de signification : elle laisse simplement de la place pour dessiner les
   ports [Cockburn 2005].

2. **Cockburn ne prescrit rien sur l'intérieur de l'hexagone, et il ajoute le « configurateur ».**
   Dans sa conférence de 2023, il précise que l'intérieur peut être « une grosse boule de boue,
   des couches ou de l'onion », ce qui compte est un jeu d'interfaces serré avec des tests
   dessus ; la Clean Architecture et l'Onion ajoutent des règles sur l'intérieur. Il nomme
   « configurateur » (composition root) l'endroit qui choisit les adaptateurs, absent de
   l'article de 2005, et liste les coûts : un paramètre de constructeur par acteur piloté, les
   interfaces requises à déclarer en langage typé [Cockburn 2023]. Pour le cours : le port
   `LlmClient` (côté secondaire) et son binding dans un ServiceProvider Laravel sont l'exemple
   direct ; le choix « Ollama ou OpenAI par une ligne de configuration » de S1.3 est exactement
   le rôle du configurateur.

3. **CQRS est un outil ponctuel, à présenter comme tel.** Fowler définit CQRS comme
   l'utilisation d'un modèle différent pour écrire et pour lire, et avertit : « pour la plupart
   des systèmes, CQRS ajoute une complexité risquée » ; il conseille de ne l'appliquer qu'à
   certaines parties d'un système (bounded contexts) [Fowler 2011]. Dans une appli avec LLM, la
   séparation utile est souvent plus modeste : commande « demander une analyse » (asynchrone,
   payante) et requête « lire le résultat » (synchrone, depuis la base). Le classement de CQRS
   en encart d'approfondissement dans la scénarisation est cohérent avec cet avertissement.

4. **Event Sourcing et appels externes : le rejeu ne doit jamais rappeler le LLM.** Fowler
   (texte de 2005, resté en brouillon de son propre aveu) explique que le rejeu d'événements
   pose problème dès qu'un système externe est appelé, et qu'il faut envelopper tout système
   externe dans une Gateway capable de se désactiver pendant le rejeu, sans que le domaine le
   sache [Fowler 2005]. Transposé : la réponse d'un LLM doit être stockée comme un fait
   (événement « réponse reçue »), car la rappeler donnerait une autre réponse et une autre
   facture. Les événements Laravel (dispatch, listeners en file) suffisent pour le cours ; le
   SDK `laravel/ai` émet lui-même des événements (`PromptingAgent`, `AgentPrompted`,
   `AgentFailedOver`, `ProviderFailedOver`, `ToolInvoked`, etc.) [Laravel AI SDK doc].

5. **Toute requête distante a un timeout, et le timeout se choisit sur des mesures.** AWS pose
   comme règle un timeout de connexion et un timeout de requête sur tout appel distant, et
   propose de partir d'un taux acceptable de faux timeouts (ex. 0,1 %) puis de lire le
   percentile correspondant de latence du service appelé (p99,9) [Brooker 2019]. Côté Laravel :
   le client HTTP a un timeout par défaut de 30 s et un timeout de connexion de 10 s ; le
   dépassement lève `ConnectionException` [Laravel 13 http-client]. Côté SDK : l'attribut
   `#[Timeout]` d'un agent `laravel/ai` vaut 60 s par défaut [Laravel AI SDK doc]. Anthropic
   recommande le streaming pour les requêtes longues, surtout au-delà de 10 minutes, et ses SDK
   refusent les requêtes non streamées censées dépasser 10 minutes [Anthropic errors].

6. **Les délais d'une file Laravel doivent être cohérents entre eux, sinon le job tourne deux
   fois (donc l'appel LLM est payé deux fois).** Le worker a `--timeout` (60 s par défaut), la
   connexion a `retry_after` ; la doc avertit que `--timeout` doit être plus court de quelques
   secondes que `retry_after`, sinon le job peut être traité deux fois. Par défaut un job n'est
   tenté qu'une fois [Laravel 13 queues]. Point d'inférence (non écrit tel quel dans les docs) :
   avec un agent au `#[Timeout]` de 60 s exécuté dans un worker au `--timeout` de 60 s, le worker
   risque d'être tué avant la levée propre de l'exception ; il faut l'ordre
   `timeout HTTP < timeout du job < retry_after`.

7. **Retry : borné, à un seul niveau de la pile, avec backoff exponentiel plafonné et jitter.**
   AWS qualifie les retries d'« égoïstes » ; avec 5 couches qui réessaient 3 fois chacune, la
   charge sur la base est multipliée par 243 ; la bonne pratique est de réessayer à un seul
   point de la pile [Brooker 2019]. Le SRE book donne le même calcul et propose un budget de
   retries par processus (ex. 60 par minute), au-delà duquel on échoue sans réessayer [Ulrich
   2016]. Le jitter évite que tous les clients réessaient en même temps ; dans la simulation
   d'AWS, « Full Jitter » (attente aléatoire entre 0 et le plafond exponentiel) fait le moins de
   travail, « Equal Jitter » est le perdant [Brooker 2015]. Nuance importante : le backoff
   n'aide que contre les pics courts ou quand les clients sont peu nombreux et séquentiels
   (workers d'une file) ; il ne réduit pas une surcharge longue [Brooker 2022].

8. **Ne réessayer que ce qui peut réussir, et respecter `Retry-After`.** Les erreurs 4xx ne se
   réessaient pas avec la même requête [Brooker 2019]. OpenAI demande de suivre `Retry-After`
   s'il est présent, sinon backoff exponentiel avec jitter, en limitant le nombre de tentatives
   et le temps total ; les requêtes en échec comptent dans les limites par minute [OpenAI rate
   limits]. Anthropic : 429 `rate_limit_error`, 500 `api_error`, 504 `timeout_error`, 529
   `overloaded_error` ; un 429 dû au plafond de dépense mensuel n'a pas d'en-tête `retry-after`
   et échouera jusqu'à la reprise : le réessayer est inutile ; le SDK officiel réessaie 2 fois
   par défaut [Anthropic errors]. Les limites Anthropic sont en RPM, ITPM et OTPM, gérées par
   token bucket (recharge continue), et les tokens lus en cache ne comptent pas dans l'ITPM
   [Anthropic rate limits].

9. **Idempotence : condition préalable à tout retry d'une opération à effet de bord.** Un
   timeout ne prouve pas que l'effet n'a pas eu lieu [Brooker 2019]. AWS recommande un
   identifiant de requête fourni par l'appelant, enregistré atomiquement avec l'effet, une
   réponse sémantiquement équivalente en cas de rejeu, et une erreur si le même identifiant
   arrive avec des paramètres différents [Featonby s.d.]. Stripe applique ce modèle avec
   l'en-tête `Idempotency-Key` (UUID v4 conseillé, clés purgeables après 24 h, comparaison des
   paramètres) [Stripe]. Pour l'API de S2.2 : `POST /analyses` avec `Idempotency-Key`, et un
   outil d'agent qui écrit (ex. créer un ticket) doit être idempotent, car la boucle d'agent ou
   le job peut le rappeler. Côté Laravel, `ShouldBeUnique` et les verrous atomiques du cache
   aident mais ne remplacent pas une clé métier.

10. **Coupe-circuit : trois états, et un coût caché.** Popularisé par Nygard dans *Release It!*,
    le coupe-circuit enveloppe un appel protégé, s'ouvre après un seuil d'échecs et renvoie une
    erreur sans faire l'appel, puis tente un appel d'essai après un délai (demi-ouvert)
    [Fowler 2014 ; Nygard 2018]. Resilience4j l'implémente comme une machine à états CLOSED,
    OPEN, HALF_OPEN (plus DISABLED, METRICS_ONLY, FORCED_OPEN) avec fenêtre glissante par nombre
    ou par durée, seuil de taux d'échec **et** seuil d'appels lents, et un nombre minimal
    d'appels avant calcul [Resilience4j]. Microsoft distingue retry (« ça va finir par marcher »)
    et coupe-circuit (« inutile d'essayer ») [Microsoft patterns]. AWS met en garde : le
    coupe-circuit introduit un comportement modal difficile à tester et peut rallonger la
    reprise ; AWS lui préfère souvent un token bucket local de retries [Brooker 2019]. Pour un
    LLM, compter les réponses lentes comme des échecs est pertinent (latence très variable).

11. **Bulkhead (cloisonnement) : isoler les ressources par dépendance.** Microsoft le décrit
    comme le partitionnement des ressources (pools de connexions, instances) pour qu'une
    dépendance défaillante n'épuise pas tout [Microsoft patterns]. Resilience4j propose un
    `SemaphoreBulkhead` (`maxConcurrentCalls` 25 par défaut, `maxWaitDuration` 0) et un
    `FixedThreadPoolBulkhead` [Resilience4j]. En Laravel, l'équivalent pratique est une file
    dédiée aux jobs IA avec un nombre de workers borné, et le middleware de job `RateLimited`
    [Laravel 13 queues]. Ollama a son propre cloisonnement : `OLLAMA_NUM_PARALLEL`, et au-delà de
    `OLLAMA_MAX_QUEUE` il répond 503 [Ollama FAQ].

12. **Repli à plusieurs niveaux et dégradation gracieuse : le chemin rarement emprunté est celui
    qui ne marche pas.** Le SRE book recommande de servir des résultats de moindre qualité et
    moins coûteux en cas de surcharge, mais prévient que le mode dégradé, peu utilisé, est mal
    connu et risqué, et qu'il faut l'exercer régulièrement et pouvoir le couper vite [Ulrich
    2016]. Il conseille aussi de vérifier le délai restant (deadline) avant chaque étape d'un
    traitement en plusieurs étapes, ce qui s'applique à chaque tour d'une boucle d'agent.
    Cela valide le « mode sans IA qui rend un vrai service » de S3.1 et impose de le tester
    (panne simulée) et non seulement de l'écrire.

13. **Laravel 13 offre les briques, pas de coupe-circuit intégré.** Briques vérifiées :
    `Http::retry($times, $sleepMs|closure|array, $when)` (délais fixes ou calculés par
    closure, pas de jitter natif, `RequestException` après échec final) [Laravel 13
    http-client] ; pour les jobs : `#[Backoff([10, 30, 60])]`, `releaseUsingBackoff()`,
    `retryUntil()`, `#[MaxExceptions]`, `FailOnException`, `dontRetry`, et surtout le
    middleware `ThrottlesExceptions` (après N exceptions, les tentatives suivantes sont
    différées d'un intervalle) qui joue un rôle proche d'un coupe-circuit par job ; la file
    `failover` (Laravel 13) bascule l'**envoi** de jobs vers une autre connexion de file, pas
    vers un autre fournisseur d'IA [Laravel 13 queues]. Le mot « circuit breaker » n'apparaît
    pas dans la doc Laravel 13 ; un coupe-circuit maison se construit avec le cache (compteur +
    verrous atomiques) ou `RateLimiter`.

14. **Exposition API d'une tâche IA : trois modes, trois contrats.** (a) Requête synchrone :
    simple mais soumise aux timeouts du client HTTP, du proxy et de PHP. (b) Streaming SSE :
    Laravel 13 fournit `response()->eventStream()` qui renvoie du `text/event-stream`, et les
    paquets `@laravel/stream-react|vue|svelte` (`useEventStream`) côté client [Laravel 13
    responses] ; le SDK fait la même chose avec `->stream()` renvoyé depuis une route, et
    propose les protocoles Vercel AI SDK et AG-UI [Laravel AI SDK doc]. (c) File d'attente :
    `POST` qui renvoie un identifiant, job en arrière-plan, résultat consulté ou poussé par
    broadcasting ; le SDK offre `->queue()->then()->catch()` et `broadcastOnQueue()` (événement
    `stream_failed` si le job échoue) [Laravel AI SDK doc]. Piège SSE : Anthropic peut envoyer
    une erreur **après** un statut 200, au milieu du flux ; la gestion d'erreur HTTP classique ne
    la voit pas [Anthropic errors].

15. **IA locale via API compatible OpenAI : même port, mais pas le même contrat exact.** Ollama
    expose `http://localhost:11434/v1/` (`/v1/chat/completions`, `/v1/embeddings`,
    `/v1/responses` sans état depuis v0.13.3, `/v1/models`) ; la clé API est « requise mais
    ignorée ». Fonctions présentes : streaming, mode JSON, vision, tools ; **non supportés** :
    `tool_choice`, `logit_bias`, `n`, logprobs, images par URL [Ollama OpenAI compat]. La
    fenêtre de contexte par défaut d'Ollama est de 4096 tokens (`OLLAMA_CONTEXT_LENGTH` pour la
    changer), ce qui casse silencieusement un RAG qui injecte beaucoup de contexte [Ollama FAQ].
    Ollama propose aussi un accès « cloud » (`https://ollama.com/v1`, `OLLAMA_API_KEY`) : « Ollama »
    n'est donc plus synonyme de « local » [Ollama OpenAI compat]. Prism recommande d'augmenter le
    timeout pour les modèles locaux [Prism doc].

16. **`laravel/ai` en v1 : ce qui existe vraiment (vérifié dans la doc et le code v1.4.2).**
    Agents = classes PHP implémentant `Laravel\Ai\Contracts\Agent` avec le trait `Promptable` ;
    interfaces optionnelles `Conversational`, `HasTools`, `HasStructuredOutput`,
    `HasMiddleware` ; `php artisan make:agent` et `make:tool`. Un outil implémente
    `Laravel\Ai\Contracts\Tool` (`description()`, `handle(Request)`, `schema(JsonSchema)`), avec
    validation des arguments renvoyée au modèle, `#[RepairToolCalls]`, `withTools()` à
    l'exécution, outils fournisseur (`WebSearch`, `WebFetch`, `FileSearch`, `CodeExecution`),
    outils MCP, sous-agents, approbation humaine (`Approvable`). Attributs : `#[Provider]`,
    `#[Model]`, `#[MaxSteps]`, `#[MaxTokens]`, `#[Temperature]`, `#[Timeout]`, `#[TopP]`,
    `#[UseCheapestModel]`, `#[UseSmartestModel]`. Middleware d'agent appelé à **chaque étape**
    de la boucle (changement de la v1.0) et `Stop::when()/unless()` pour arrêter un run (ex.
    budget de tokens) [Laravel AI SDK doc ; Laravel blog v1.0]. La 1.0 contient des ruptures
    (stockage des conversations, middleware, usage des tokens, protocoles de stream) [Laravel
    blog v1.0].

17. **Bascule de fournisseur du SDK (« failover ») : réelle, mais étroite.** On passe un tableau
    de fournisseurs (`provider: [Lab::OpenAI, Lab::Anthropic]`, ou fournisseur => modèle). La
    bascule n'a lieu que sur une `FailoverableException` : `RateLimitedException` (429),
    `ProviderOverloadedException` (502, 503, 504, 520, 522, 524 par défaut, codes propres à
    certains gateways comme Anthropic), `InsufficientCreditsException` (402 ou 429 de quota), et,
    d'après le code mais pas la doc, `ProviderConnectionException` (connexion impossible ou
    timeout). Une erreur 400 ou une clé invalide (401) ne bascule pas. Avant de basculer, le code
    fait **une seule** nouvelle tentative, et seulement si l'en-tête `Retry-After` est présent et
    vaut au plus 10 s ; il n'y a **ni backoff exponentiel, ni jitter, ni coupe-circuit** : chaque
    nouvelle requête retente d'abord le fournisseur principal en panne. En streaming, la bascule
    n'est possible que si rien n'a encore été envoyé au client [code source `laravel/ai`
    v1.4.2 : `HandlesFailoverErrors`, `StreamsText` ; Laravel AI SDK doc].

18. **Tests avec le SDK : `Agent::fake()` est une notation, l'appel réel se fait sur la classe
    concrète.** La doc montre `SalesCoach::fake()` (réponse fixe), `fake([...])` (liste),
    `fake(fn (AgentPrompt $p) => ...)`, des données structurées générées depuis le schéma,
    `preventStrayPrompts()`, et les assertions `assertPrompted`, `assertPromptedTimes`,
    `assertNotPrompted`, `assertNeverPrompted`, `assertQueued`... ; la note de la doc écrit
    `Agent::fake()` de façon générique, mais `Agent` est une interface : la méthode statique
    `fake()` vient du trait `Promptable` [Laravel AI SDK doc ; code source v1.4.2]. Il existe
    aussi `Image::fake()`, `Embeddings::fake()`, `Stores::fake()`, `Files::fake()`. Prism a son
    équivalent `Prism::fake()` [Prism doc].

19. **Recherche vectorielle côté Laravel : trois choses différentes à ne pas confondre.**
    (a) Le cœur Laravel 13 : colonne `vector` en migration et clause `whereVectorSimilarTo`
    (cosinus, `minSimilarity`) sur PostgreSQL + pgvector ou MariaDB 11.7+ [Laravel 13 queries,
    cité via doc SDK]. (b) L'outil d'agent `SimilaritySearch::usingModel(Document::class,
    'embedding')` qui branche cette recherche sur un agent. (c) `Laravel\Ai\Stores` : des
    « vector stores » **hébergés chez le fournisseur** (OpenAI, Gemini...) utilisés par l'outil
    `FileSearch`, pas une abstraction de pgvector [Laravel AI SDK doc]. Il n'existe pas de classe
    `VectorStore` dans `laravel/ai`.

20. **Spring AI 2.1 : `VectorStore` et `@Tool` existent tels quels ; l'Evaluator n'est pas une
    doublure.** `VectorStore extends DocumentWriter, VectorStoreRetriever` avec
    `similaritySearch(SearchRequest)` (topK, seuil, filtre) et une vingtaine d'implémentations
    dont pgvector [Spring AI ref vectordbs]. Les outils se déclarent par `@Tool(description=...)`,
    `MethodToolCallback` ou `FunctionToolCallback`, passés via `ChatClient.tools(...)` ; la 2.0
    a supprimé la résolution de simples beans `Function` par nom [Spring AI ref tools].
    L'interface `Evaluator` (`EvaluationResponse evaluate(EvaluationRequest)`), avec
    `RelevancyEvaluator` et `FactCheckingEvaluator`, fait juger une réponse **par un autre
    modèle** (LLM juge) : c'est un outil d'évaluation (S4.1, IA juge), pas l'équivalent de
    `Agent::fake()` [Spring AI ref testing]. La 2.1 ajoute l'API Session (qui remplace
    `ChatMemory`, déprécié pour suppression en 3.0.0), l'approbation humaine des appels d'outils,
    une limite d'appels d'outils par tour, `DecisionModel`, MCP 2026-07-28 ; un projet
    « Spring AI Agent » doit démarrer en incubation début décembre 2026 [Tzolov 2026].

21. **Résilience et observabilité dans Spring AI : retry intégré, pas de bascule intégrée.**
    Spring AI 2.x s'appuie sur `org.springframework.core.retry` (Spring Framework 7) et non plus
    sur spring-retry. Valeurs par défaut lues dans le code 2.1.0 : 10 tentatives max, délai
    initial 2 s, multiplicateur 5, délai max 3 min, sur `TransientAiException` et
    `ResourceAccessException`, **sans jitter** ; les erreurs client 4xx ne sont pas réessayées
    par défaut [code Spring AI 2.1.0, `RetryUtils`, `SpringAiRetryProperties`]. La doc cite le
    repli entre modèles comme cas d'usage de plusieurs `ChatClient`, mais ne fournit pas de
    bascule automatique : on la code soi-même ou avec Resilience4j [Spring AI ref chatclient].
    Observabilité : observations Micrometer sur `ChatClient`, advisors, `ChatModel`, outils,
    `EmbeddingModel`, `VectorStore`, avec attributs `gen_ai.*` ; prompts et complétions non
    exportés par défaut (risque de données sensibles) [Spring AI ref observability]. `laravel/ai`
    n'a pas d'export OpenTelemetry : l'observabilité passe par ses événements et l'objet `usage`
    (tokens en cache, de raisonnement, etc.) [Laravel AI SDK doc].

22. **Commencer simple : workflow codé avant agent autonome.** Anthropic distingue les
    *workflows* (LLM et outils orchestrés par du code prédéfini) et les *agents* (le LLM dirige
    lui-même son processus), recommande la solution la plus simple possible et met en garde
    contre les couches d'abstraction des frameworks qui masquent prompts et réponses ; l'article
    (19/12/2024) porte désormais une note indiquant que l'outillage décrit a beaucoup changé
    [Schluntz et Zhang 2024]. Cela soutient le choix du cours : TP sans SDK d'abord, comparaison
    ensuite, et l'étude de cas S2.2 « une seule étape sur trois a besoin de l'IA ».

## 2. Ordre d'enseignement recommandé

**Ordre conseillé pour le thème B** (et justification) :

1. Couches, séparation des responsabilités, ports et adaptateurs (S1.1) : prérequis de tout le
   reste, car retry, coupe-circuit, repli et doublure de test sont **des adaptateurs ou des
   décorateurs du port LLM**. Sans le port, chacun de ces mécanismes finit dans le contrôleur.
2. Caractéristiques du LLM (S1.2) : non-déterminisme, latence variable, coût par appel,
   dépendance externe, plus **limites de débit** (RPM/TPM) qui manquent dans la liste actuelle
   et justifient à elles seules file d'attente et repli.
3. IA locale et en ligne derrière le même port (S1.3), puis TP de refactorisation (S1.4).
   L'ordre S1.3 avant S1.4 est bon : la démo « deux adaptateurs, une ligne de config » motive le
   TP. Signaler dès S1.3 les écarts de contrat (pas de `tool_choice` sur Ollama, contexte 4096).
4. Timeouts et traitement asynchrone (files, workers) **avant** retry : un retry sans timeout
   ne se déclenche jamais, et un retry en arrière-plan suppose la file. Aujourd'hui la file
   n'apparaît vraiment qu'en S2.2 (5 min) puis en S3.1 ; il faut au minimum poser en S1.2 ou
   S1.4 la cohérence `timeout HTTP < timeout job < retry_after`.
5. Idempotence **avant** retry (manque dans S3.1) : AWS et Stripe la posent comme condition
   préalable au retry d'une opération à effet de bord.
6. Retry borné avec backoff exponentiel + jitter, à un seul niveau, avec respect de
   `Retry-After` et classement des erreurs réessayables.
7. Coupe-circuit, puis cloisonnement (bulkhead, approfondissement).
8. Repli multi-niveaux (en ligne, local, sans IA) en dernier, car il s'appuie sur le
   coupe-circuit (savoir que le fournisseur est « ouvert ») et sur le port (changer
   d'adaptateur).
9. Comparaison SDK (S1.4 grille, S3.1, S4.3) seulement **après** avoir écrit soi-même : c'est
   l'ordre du cours, et c'est l'ordre défendu par Anthropic.

**Comparaison avec des cours et guides de référence :**

- *Microsoft, Generative AI for Beginners* (21 leçons) : installation (00), LLM (01-02), IA
  responsable (03), prompts (04-05), applications texte et chat (06-07), recherche vectorielle
  (08), function calling (11), sécurité (13), cycle de vie (14), RAG (15), modèles open source
  (16), agents (17). Différences : ce cours ne traite quasiment pas d'architecture ni de
  résilience, et place le function calling **après** la recherche vectorielle ; notre ordre
  (outil S2.1, puis RAG S2.3) est plus logique pour un agent qui utilise le RAG comme outil.
- *Microsoft, AI Agents for Beginners* : intro, frameworks (02) puis patterns (03), tool use
  (04), RAG agentique (05), confiance (06)... production (10), déploiement à l'échelle (16),
  agents locaux (17), sécurité (18). Il présente les frameworks **avant** d'écrire quoi que ce
  soit et ne traite la production et le local qu'à la fin. Notre cours fait l'inverse
  (local dès S1.3, production en S3), ce qui est plus adapté à un public de développeurs web.
- *Anthropic, Building effective agents* : brique de base « LLM augmenté » (récupération,
  outils, mémoire), puis workflows de plus en plus complexes, puis agents autonomes ; conseil
  de commencer par les API directement. Notre progression S2.1 (outil) → S2.2 (boucle,
  machine à états) → S2.3 (RAG) → S2.4 (agent) suit la même montée.
- Côté résilience, l'ordre timeout → retry/backoff → jitter → idempotence → coupe-circuit est
  celui de l'article AWS de référence [Brooker 2019] et du SRE book (chap. 22) ; seul point à
  adapter : AWS traite l'idempotence dans le même article que le retry, le cours doit l'enseigner
  **avant** de faire écrire un retry.

## 3. Erreurs et idées reçues fréquentes

1. **« Le Laravel AI SDK gère la résilience à notre place. »** Faux en partie : il bascule vers
   un autre fournisseur sur certaines erreurs, mais ne fait ni backoff exponentiel, ni jitter,
   ni coupe-circuit, et refrappe le fournisseur en panne à chaque requête. La phrase de la
   scénarisation S3.1 « Le SDK gère nativement le changement de fournisseur » est juste, mais il
   faut ajouter « pas le retry ni le coupe-circuit ».
2. **« `Agent::fake()` »** écrit tel quel dans un test : ne fonctionne pas, on appelle
   `MonAgent::fake()`. Dans les supports, écrire « la méthode statique `fake()` des agents
   (`SalesCoach::fake()`) ».
3. **« L'Evaluator API de Spring AI est l'équivalent de la doublure (fake). »** Faux : c'est un
   LLM juge (S4.1). La page « Evaluation Testing » de la référence Spring AI ne propose pas de faux `ChatModel` prêt à l'emploi ; on écrit un
   mock de `ChatModel` (Mockito) ou on teste contre Ollama via Testcontainers. La comparaison de
   S4.1 doit être corrigée : doublure maison ↔ `Agent::fake()` ↔ mock de `ChatModel` ; IA juge ↔
   `Evaluator`.
4. **« Les VectorStore de Spring AI et ceux du Laravel AI SDK, c'est pareil. »** Non : Spring AI
   abstrait votre base (pgvector, etc.) ; `Laravel\Ai\Stores` gère des stores hébergés chez le
   fournisseur. L'équivalent pgvector côté Laravel est `whereVectorSimilarTo` +
   `SimilaritySearch`.
5. **« Laravel AI SDK version 0.x, bêta. »** Obsolète depuis le 23/09/2026 (v1.0.0) ; la
   version au 24/11/2026 est v1.4.2. Il ne repose plus sur Prism depuis v0.6.1.
6. **« Spring AI 2.0.1 », « `ChatMemory` »** : 2.1.0 est sortie le 20/11/2026 et `ChatMemory`
   y est déprécié au profit de l'API Session.
7. **« Réessayer, c'est toujours bien. »** Les retries amplifient la charge (×243 sur 5
   couches), un 429 de plafond de dépense ne passera jamais, et chaque retry d'un LLM est
   refacturé. Il faut un budget de retries et un seul niveau de retry (attention : SDK
   fournisseur qui réessaie déjà 2 fois + `Http::retry` + `tries` du job = multiplication).
8. **« Le backoff exponentiel suffit. »** Sans jitter, les clients se resynchronisent ; et le
   backoff ne réduit pas une surcharge longue avec beaucoup de clients indépendants [Brooker
   2015, 2022].
9. **« Ajouter un coupe-circuit rend le système plus simple. »** Il ajoute un mode à tester et
   peut retarder la reprise [Brooker 2019] ; avec plusieurs workers PHP, son état doit être
   partagé (cache Redis), sinon chaque worker a son propre disjoncteur.
10. **« Hexagonal = trois couches / Clean Architecture. »** Cockburn ne dit rien de l'intérieur ;
    ce sont les ports, les adaptateurs et les tests aux frontières qui comptent.
11. **« CQRS est une bonne pratique par défaut. »** Fowler dit l'inverse pour la plupart des
    systèmes.
12. **« Ollama = local » et « compatible OpenAI = interchangeable »** : Ollama a un mode cloud,
    et sa compatibilité est partielle (`tool_choice` absent, contexte par défaut 4096).
13. **« Le timeout de la file et celui de l'appel HTTP sont indépendants. »** Mal réglés, ils
    produisent un double traitement (double facture) ou un worker tué.
14. **« Le streaming règle le problème de lenteur. »** Il améliore la latence perçue mais garde
    une connexion ouverte par utilisateur, complique les erreurs (erreur après 200) et empêche
    la bascule de fournisseur une fois le premier morceau envoyé.
15. **« Un retry de requête POST est sans risque. »** Pas sans clé d'idempotence ; c'est vrai
    aussi des outils d'agent qui écrivent.

## 4. Sources

1. Cockburn A. (2005), *Hexagonal Architecture* (HaT Technical Report 2005.02, v0.9 du 04/09/2005), alistair.cockburn.us.
   https://alistair.cockburn.us/hexagonal-architecture/ ; article en ligne ; consulté le 24/11/2026 ; [S1.1, S1.4].
   Intention du pattern (testabilité, pilotage par tests), ports primaires et secondaires, adaptateur « mock » en mémoire.

2. Cockburn A. (2023), *Hexagonal Architecture from its Inventor*, Craft Conference 2023 (CraftHub Events, YouTube, 42 min, 24/05/2023).
   https://www.youtube.com/watch?v=Gsgisj1Ns40 ; vidéo (transcription lue) ; consulté le 24/11/2026 ; [S1.1, S1.4].
   Configurateur (composition root), coûts du pattern, différence avec Clean et Onion (« l'intérieur n'est pas mon souci »).

3. Fowler M. (2011), *CQRS*, martinfowler.com (bliki, 14/07/2011).
   https://martinfowler.com/bliki/CQRS.html ; article ; consulté le 24/11/2026 ; [S1.1].
   Définition et avertissement : « pour la plupart des systèmes, CQRS ajoute une complexité risquée ».

4. Fowler M. (2005), *Event Sourcing*, martinfowler.com (Further EAA, 12/12/2005, brouillon non mis à jour).
   https://martinfowler.com/eaaDev/EventSourcing.html ; article ; consulté le 24/11/2026 ; [S1.1].
   Rejeu d'événements et systèmes externes : Gateway désactivable pendant le rejeu.

5. Fowler M. (2014), *CircuitBreaker*, martinfowler.com (bliki, 06/03/2014).
   https://martinfowler.com/bliki/CircuitBreaker.html ; article ; consulté le 24/11/2026 ; [S3.1].
   Principe, seuil, alerte, état demi-ouvert par réessai après délai ; attribution à Nygard.

6. Nygard M. (2018), *Release It! Design and Deploy Production-Ready Software*, 2e éd., Pragmatic Bookshelf.
   https://pragprog.com/titles/mnee2/release-it-second-edition/ ; livre (page éditeur et vidéo de présentation éditeur https://www.youtube.com/watch?v=gO30OfS1Mq8 lues, livre non relu en entier pour cette fiche) ; 2e éd. ; consulté le 24/11/2026 ; [S3.1].
   Référence d'origine des patterns de stabilité (coupe-circuit, cloisons) ; 2e éd. ajoute cloud-native et chaos engineering.

7. Software Engineering Radio (2009), *Episode 134: Release It with Michael Nygard*, IEEE Software / SE Radio.
   https://se-radio.net/2009/05/episode-134-release-it-with-michael-nygard/ ; podcast (page d'épisode et notes lues, audio non écouté) ; mai 2009 ; consulté le 24/11/2026 ; [S3.1].
   Entretien sur la 1re édition : planification de capacité, reprise, exploitation ; ressource audio d'appoint, ancienne.

8. Brooker M. (2019), *Timeouts, retries, and backoff with jitter*, Amazon Builders' Library.
   https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ ; billet d'ingénierie ; 05/12/2019 ; consulté le 24/11/2026 ; [S1.2, S3.1].
   Choix du timeout par percentile, amplification ×243, retry à un seul niveau, limites des coupe-circuits, token bucket, jitter.

9. Brooker M. (2015), *Exponential Backoff and Jitter*, AWS Architecture Blog.
   https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/ ; billet avec simulation ; 04/03/2015 ; consulté le 24/11/2026 ; [S3.1].
   Comparaison Full / Equal / Decorrelated Jitter ; Full Jitter fait le moins de travail.

10. Brooker M. (2022), *What is Backoff For?*, Marc's Blog.
    https://brooker.co.za/blog/2022/08/11/backoff.html ; billet ; 11/08/2022 ; consulté le 24/11/2026 ; [S3.1].
    Le backoff aide contre les pics courts et les clients séquentiels (workers), pas contre une surcharge longue.

11. Featonby M. (s.d.), *Making retries safe with idempotent APIs*, Amazon Builders' Library.
    https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/ ; billet d'ingénierie ; date non affichée sur la page ; consulté le 24/11/2026 ; [S2.2, S3.1].
    Identifiant de requête fourni par le client, enregistrement atomique, réponse sémantiquement équivalente, erreur si paramètres différents.

12. Stripe (2026), *Idempotent requests*, Stripe API Reference.
    https://docs.stripe.com/api/idempotent_requests ; documentation officielle ; consulté le 24/11/2026 ; [S2.2, S3.1].
    En-tête `Idempotency-Key`, UUID v4, purge après 24 h, comparaison des paramètres : modèle concret pour l'API de S2.2.

13. Ulrich M. ; Forero Cuervo A. (2016), *Site Reliability Engineering*, chap. 22 « Addressing Cascading Failures » et chap. 21 « Handling Overload », O'Reilly / Google (édition en ligne).
    https://sre.google/sre-book/addressing-cascading-failures/ et https://sre.google/sre-book/handling-overload/ ; livre en ligne ; 2016 ; consulté le 24/11/2026 ; [S1.2, S3.1].
    Budget de retries, amplification multi-niveaux, deadlines et propagation, délestage et dégradation gracieuse à exercer.

14. Microsoft (2026), *Circuit Breaker pattern* et *Bulkhead pattern*, Azure Architecture Center.
    https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker et https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead ; documentation de référence ; consulté le 24/11/2026 ; [S3.1].
    Retry vs coupe-circuit, états Closed / Open / Half-Open, cloisonnement des ressources par consommateur.

15. Resilience4j (2026), *Resilience4j User Guide* (CircuitBreaker, Bulkhead, Retry), v2.4.0 (14/03/2026).
    https://resilience4j.readme.io/docs/circuitbreaker ; documentation officielle (+ https://github.com/resilience4j/resilience4j/releases) ; consulté le 24/11/2026 ; [S3.1, S4.3].
    États et fenêtres glissantes, seuil d'appels lents, `SemaphoreBulkhead`, Retry (3 tentatives, 500 ms par défaut, `IntervalFunction`).

16. Laravel LLC (2026), *Laravel 13.x Documentation* : Queues, HTTP Client, HTTP Responses (Event Streams), Release Notes, Queries.
    https://laravel.com/docs/13.x/queues (source lue : https://github.com/laravel/docs/tree/13.x) ; documentation officielle ; framework v13.44.1 au 24/11/2026 ; consulté le 24/11/2026 ; [S1.2, S2.2, S3.1].
    `--timeout` vs `retry_after`, `#[Backoff]`, `ThrottlesExceptions`, file `failover`, `Http::retry`, timeouts par défaut, `eventStream()` SSE, `whereVectorSimilarTo`.

17. Laravel LLC (2026), *Laravel AI SDK* (package `laravel/ai`), documentation, dépôt GitHub et billets « Introducing the Laravel AI SDK » (05/02/2026) et « Introducing Laravel AI SDK v1.0 » (23/09/2026).
    https://laravel.com/docs/ai-sdk ; https://github.com/laravel/ai (releases, code au tag v1.4.2 lu) ; https://laravel.com/blog/introducing-laravel-ai-sdk-v1 ; documentation, code source, blog ; v1.4.2 ; consulté le 24/11/2026 ; [S1.4, S2.2, S3.1, S4.3].
    Agents, outils, `tools()`, failover exact (exceptions, Retry-After ≤ 10 s), `fake()`, stream/queue/broadcast, événements, Stores, ruptures de la 1.0.

18. VMware Tanzu / Broadcom (2026), *Spring AI Reference Documentation* (ChatClient, Tool Calling, Vector Databases, Evaluation Testing, Observability, Ollama Chat, OpenAI Chat) et code source.
    https://docs.spring.io/spring-ai/reference/ (sources lues au tag v2.1.0 : https://github.com/spring-projects/spring-ai/tree/v2.1.0) ; documentation officielle et code ; 2.1.0 ; consulté le 24/11/2026 ; [S1.4, S3.1, S4.3].
    `VectorStore`, `@Tool`, `Evaluator` (LLM juge), retry par défaut sans jitter, absence de bascule intégrée, observations `gen_ai.*`, Ollama via client OpenAI.

19. Tzolov C. (2026), *Spring AI 2.1.0 GA and 2.0.3 GA Available Now*, Spring Blog (20/11/2026).
    https://spring.io/blog/2026/11/20/spring-ai-2-1-0-GA-available-now/ ; billet éditeur ; consulté le 24/11/2026 ; [S4.3].
    Nouveautés 2.1 (Session remplace ChatMemory, approbation d'outils, DecisionModel, MCP 2026-07-28), Spring Boot 4.2, projet Spring AI Agent annoncé.

20. Ollama (2026), *OpenAI compatibility* et *FAQ*, Ollama Documentation.
    https://docs.ollama.com/api/openai-compatibility (source : https://github.com/ollama/ollama/tree/main/docs) ; documentation officielle ; v0.40.18 (24/11/2026) ; consulté le 24/11/2026 ; [S1.3, S3.1].
    Endpoints `/v1/*`, champs non supportés (`tool_choice`...), contexte 4096 par défaut, `OLLAMA_NUM_PARALLEL`, 503 au-delà de `OLLAMA_MAX_QUEUE`, mode cloud.

21. Anthropic (2026), *Errors* et *Rate limits*, Claude API Docs.
    https://docs.claude.com/en/api/errors et https://docs.claude.com/en/api/rate-limits ; documentation officielle ; consulté le 24/11/2026 ; [S1.2, S3.1].
    Codes 429/500/504/529, 429 de plafond sans `retry-after`, erreurs en plein flux SSE, 2 retries SDK, RPM/ITPM/OTPM et token bucket.

22. OpenAI (2026), *Rate limits*, OpenAI Platform Docs.
    https://platform.openai.com/docs/guides/rate-limits ; documentation officielle ; consulté le 24/11/2026 ; [S1.2, S3.1].
    RPM/TPM/RPD, en-têtes `x-ratelimit-*`, suivre `Retry-After` sinon backoff exponentiel avec jitter, bornes de tentatives et de durée.

23. Schluntz E., Zhang B. (2024), *Building effective agents*, Anthropic Engineering.
    https://www.anthropic.com/engineering/building-effective-agents ; billet d'ingénierie ; 19/12/2024 (note ajoutée : outillage changé depuis) ; consulté le 24/11/2026 ; [S2.2, S4.3].
    Workflows vs agents, commencer simple, prudence face aux frameworks : appui de l'approche « sans SDK d'abord ».

24. Prism PHP (2026), *Prism Documentation* (Testing, Error handling, Rate limits, Ollama), dépôt prism-php/prism.
    https://prismphp.com/ (sources lues : https://github.com/prism-php/prism/tree/main/docs) ; documentation ; v0.103.0 (07/11/2026) ; consulté le 24/11/2026 ; [S4.3].
    `Prism::fake()`, exceptions `PrismRateLimitedException` / `PrismProviderOverloadedException`, `withClientRetry` (client HTTP Laravel), pas de failover intégré.

25. Microsoft (2026), *Generative AI for Beginners* et *AI Agents for Beginners*, dépôts GitHub microsoft.
    https://github.com/microsoft/generative-ai-for-beginners et https://github.com/microsoft/ai-agents-for-beginners ; cours ouverts (README et plan lus) ; consulté le 24/11/2026 ; [ordre d'enseignement].
    Plans de référence utilisés pour comparer l'ordre des notions (function calling, RAG, agents, production, local).

### Sources repérées mais non retenues faute de lecture complète
- AWS re:Invent 2024, *Try again: The tools and techniques behind resilient systems* (ARC403, M. Brooker), https://www.youtube.com/watch?v=rvHd4Y76-fs : seule la description a été lue, pas la transcription. Pertinente pour S3.1 (retries, coupe-circuits) si quelqu'un la visionne.
