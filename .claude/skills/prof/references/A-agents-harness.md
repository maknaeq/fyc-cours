# Thème A : ingénierie agentique, harness, context engineering, tool calling, MCP

Fiche de référence du prof FYC pour S2.1 (tool calling), S2.2 (boucle d'agent,
machine à états), S2.4 (TP agent) et le cadrage général du cours.
Recherche faite le 24/11/2026 ; 26 sources (une de plus que la cible haute, la 26e apporte le format audio) ; chaque source listée a été ouverte et lue ce
jour-là (texte intégral, sauf mention contraire). Les numéros [n] renvoient à la
section 4.

## 1. Savoir de référence

1. **Workflow contre agent : la distinction fondatrice.** Un workflow orchestre
   LLM et outils par des chemins de code prédéfinis ; un agent laisse le LLM
   diriger dynamiquement son processus et ses appels d'outils. La recommandation
   est de chercher la solution la plus simple et de n'ajouter de la complexité
   que si elle améliore des résultats mesurés : souvent, un seul appel de LLM
   optimisé avec récupération (RAG) et exemples suffit. LangGraph et OpenAI
   reprennent la même opposition. [1][9]

2. **Les cinq patterns de workflow à connaître par leur nom.** Brique de base :
   le « LLM augmenté » (récupération, outils, mémoire). Puis prompt chaining (avec
   « gate » programmatique entre étapes), routing, parallélisation (sectioning ou
   voting), orchestrator-workers, evaluator-optimizer. Ces patterns ne sont pas
   prescriptifs, ils se combinent. C'est le vocabulaire commun du métier en 2026 ;
   l'étude de cas S2.2 (« trois étapes dont une seule a besoin de l'IA ») est
   exactement un prompt chaining avec gates déterministes. [1][13]

3. **Définition opérationnelle d'un agent : « des outils dans une boucle ».**
   Anthropic a convergé (sept. 2025) vers « LLMs autonomously using tools in a
   loop » ; Simon Willison formule « An LLM agent runs tools in a loop to achieve
   a goal », en insistant sur la condition d'arrêt (pas de boucle infinie) et en
   nommant « harness » le code qui exécute les actions demandées. Chip Huyen part
   de la définition classique de Russell et Norvig (percevoir un environnement et
   agir dessus) : l'environnement détermine les outils possibles. [2][21][17]

4. **Le tool calling est un contrat : le modèle demande, l'application exécute.**
   Le modèle n'exécute jamais rien lui-même : il émet une requête structurée (nom
   d'outil + arguments JSON), l'application exécute et renvoie le résultat dans la
   conversation. Spring AI le dit explicitement (« the model never receives direct
   access to the APIs behind your tools, a critical security consideration »),
   Anthropic aussi (« The model never runs anything on its own »). Le flux OpenAI
   en cinq étapes (requête avec outils, appel d'outil reçu, exécution côté
   application, seconde requête avec le résultat, réponse finale ou nouveaux
   appels) est le meilleur schéma pour S2.1. Les exceptions sont les outils
   exécutés côté serveur du fournisseur (recherche web, exécution de code), à
   présenter comme un cas à part. [8][10][23]

5. **Formats concrets : les fournisseurs diffèrent, d'où l'adaptateur.** OpenAI
   (Responses API) : items `function_call` avec `call_id`, retour en
   `function_call_output`. Anthropic : bloc `tool_use` et `stop_reason:
   "tool_use"`, retour en bloc `tool_result`. Ollama : messages `role: "tool"`
   avec `tool_name`, sans identifiant d'appel dans l'exemple documenté. Ces écarts
   justifient le port « fournisseur de modèle » et l'adaptateur écrits à la main
   en S1.4/S2.1 : le cœur métier manipule un type `ToolCall` neutre. [8][10][25]

6. **Le schéma JSON des paramètres : strict ou « best effort ».** OpenAI
   recommande `strict: true`, qui impose `additionalProperties: false` et tous
   les champs en `required` (optionnels via `null`) ; sans `strict`, Chat
   Completions reste non strict, et Responses tente de normaliser le schéma.
   Anthropic propose aussi `strict` et `input_examples`. MCP accepte désormais tout
   JSON Schema 2020-12 (`inputSchema`, `outputSchema` optionnel). Même avec un
   schéma strict, l'application doit valider les arguments (règles métier, droits) :
   le Laravel AI SDK renvoie les messages de validation au modèle comme résultat
   d'outil pour qu'il corrige. [10][8][14][24]

7. **Écrire de bons outils, c'est concevoir une interface pour un agent
   (« ACI »).** Principes vérifiés chez Anthropic et OpenAI : peu d'outils, ciblés
   sur des tâches à fort impact plutôt qu'un wrapper par endpoint
   (`search_contacts` plutôt que `list_contacts`) ; noms et paramètres sans
   ambiguïté (`user_id` plutôt que `user`) ; « test du stagiaire » ; enums pour
   rendre les états invalides impossibles ; ne pas faire remplir au modèle un
   argument que le code connaît déjà ; fusionner les fonctions toujours appelées
   en séquence ; espaces de noms (`crm_…`) ; réponses économes en tokens
   (pagination, troncature, Claude Code limite à 25 000 tokens par réponse
   d'outil) ; messages d'erreur actionnables. OpenAI donne « moins de 20 fonctions
   au départ d'un tour » comme indication souple ; OpenAI note aussi que le
   problème est la similarité entre outils plus que leur nombre. [3][1][10][9]

8. **Les définitions d'outils coûtent des tokens et du contexte.** Elles sont
   injectées dans le prompt système et facturées en tokens d'entrée. Réponse de
   l'industrie en 2025-2026 : chargement différé et « tool search » (OpenAI
   `defer_loading` à partir de gpt-5.4, Anthropic Tool Search, Laravel
   `ToolSearch`, Spring AI `ToolSearchToolCallingAdvisor` avec 34 à 64 % de tokens
   économisés selon Spring), et « code execution with MCP » où l'agent écrit du
   code qui appelle les outils (exemple d'Anthropic : 150 000 tokens réduits à
   2 000). À présenter comme approfondissement, pas comme base du TP. [10][7][24]

9. **La boucle d'agent minimale est un `while` sur la raison d'arrêt.** Chez
   Anthropic : tant que `stop_reason == "tool_use"`, exécuter les outils et
   relancer ; sortir sur `end_turn`, `max_tokens`, `stop_sequence`, `refusal`.
   OpenAI : une « run » boucle jusqu'à une condition de sortie (outil de sortie
   finale, réponse sans appel d'outil, erreur, nombre maximal de tours). Le harness
   doit toujours ajouter un plafond d'itérations et un budget (tokens, temps,
   appels par outil) : Spring AI 2.0 a des plafonds par défaut
   (`maxCallsPerTool`, `maxTotalToolCalls`), Laravel `#[MaxSteps]` et le
   middleware `Stop`. [8][9][24][23]

10. **« Harness » : le mot central de 2025-2026, avec deux sens à ne pas
    confondre.** (a) Le code qui entoure le modèle dans un agent : boucle, routage
    des appels d'outils, contexte, mémoire, garde-fous ; « Agent = Model +
    Harness » (Böckeler). C'est ce que les apprenants écrivent en S2.4.
    (b) L'environnement qu'on construit autour d'un agent de code pour
    développer (AGENTS.md, linters, tests structurels, « guides » feedforward et
    « sensors » feedback) : c'est le « harness engineering » d'OpenAI (fév. 2026)
    et de martinfowler.com. Le cours traite (a) ; (b) concerne l'outillage du
    développeur et ne doit pas être mélangé au TP. [19][11][6]

11. **Un harness encode des hypothèses sur ce que le modèle ne sait pas faire,
    et elles périment.** Anthropic (2026) : les « context resets » ajoutés pour
    Sonnet 4.5 (« context anxiety ») sont devenus du poids mort avec Opus 4.5 ; les
    sprints nécessaires avec Opus 4.5 ont été retirés avec Opus 4.6, en enlevant
    un composant à la fois pour mesurer. Inversement, Jain (oct. 2026) montre qu'un
    harness à base de tests n'apporte rien à un modèle de pointe (10/10 dans les
    deux cas, pour environ 7 fois le coût) mais fait passer un modèle économique
    de 3/10 à 10/10. Leçon pour le cours : le harness se dimensionne selon le
    modèle, et c'est un argument fort pour l'IA locale de S1.3. [5][6][20]

12. **Architecture : séparer cerveau, mains et journal de session.** Anthropic
    Managed Agents (avril 2026) découple le « cerveau » (modèle + harness), les
    « mains » (bacs à sable et outils, interface unique `execute(name, input) →
    string`) et la « session » (journal d'événements append-only, hors de la
    fenêtre de contexte). Le harness devient sans état et remplaçable
    (`wake(sessionId)`, reprise au dernier événement), et les identifiants ne
    passent jamais par le modèle (coffre + proxy MCP). C'est l'architecture
    hexagonale de S1.1 appliquée à l'agent, et l'argument « industriel » pour
    l'interface d'outil écrite à la main. [6]

13. **Posséder son flux de contrôle, son contexte et son état (12-Factor
    Agents).** Facteurs clés pour S2.2 : outils = sorties structurées interprétées
    par du code déterministe (facteur 4) ; posséder son contexte (3) et son flux
    de contrôle (8), par exemple casser la boucle pour une validation humaine
    avant une action risquée ; unifier état d'exécution et état métier (5) ;
    lancer, mettre en pause et reprendre via des API simples (6) ; compacter les
    erreurs dans le contexte (9) ; petits agents focalisés (10) ; agent comme
    « stateless reducer » (12). Horthy constate que la plupart des agents en
    production « weren't that agentic at all. They were mostly just software » :
    des boucles de 3 à 10 étapes insérées dans un graphe déterministe. [12][13]

14. **Machine à états et annulation : s'appuyer sur la saga.** La boucle d'agent
    se modélise comme une machine à états (en attente du modèle, appel d'outil,
    attente d'approbation humaine, terminé, échoué) dont l'état est persisté
    (facteurs 5-6) ; Laravel et Spring AI implémentent la pause pour approbation
    humaine (`Approvable`, « Tool Call Confirmation »). Pour annuler proprement une
    tâche multi-étapes, le pattern de référence est la saga : une suite de
    transactions locales avec transactions de compensation, orchestrée ou
    chorégraphiée. Le modèle ne doit pas décider seul de la compensation : c'est
    du code déterministe. [12][22][23][24]

15. **Context engineering : le contexte est une ressource finie.** Définition
    Anthropic : l'ensemble des stratégies pour sélectionner et maintenir le
    meilleur ensemble de tokens pendant l'inférence (prompt système, outils,
    exemples, historique, données externes). « Context rot » : la précision de
    rappel baisse quand le contexte grossit ; principe directeur : « the smallest
    possible set of high-signal tokens ». Lance Martin regroupe les techniques en
    quatre familles : écrire (notes, mémoire), sélectionner, compresser (résumé,
    compaction), isoler (sous-agents, état hors contexte). [2][26]

16. **Récupération « juste à temps » contre RAG pré-calculé : hybride.** Les
    agents récents gardent des références légères (chemins, requêtes) et chargent
    les données via des outils au moment voulu, au lieu de tout injecter par
    recherche vectorielle avant inférence ; Anthropic recommande souvent un
    hybride (une partie pré-chargée, le reste exploré). Pour S2.4, la recherche par
    similarité exposée comme outil de l'agent (et non injectée systématiquement)
    illustre cet hybride ; le Laravel AI SDK fournit d'ailleurs un outil
    `SimilaritySearch`. [2][24]

17. **Mémoire et tâches longues : compaction, notes structurées, sous-agents.**
    Compaction (résumer l'historique proche de la limite, effacer les résultats
    d'outils anciens), prise de notes persistantes (fichier de progression,
    liste de fonctionnalités en JSON car moins souvent écrasée que du Markdown,
    commits git), sous-agents qui ne renvoient qu'un résumé de 1 000 à 2 000
    tokens. Ces techniques débordent du TP mais justifient de persister
    l'historique de conversation côté application (Spring AI : l'ordre du
    `MessageChatMemoryAdvisor` par rapport au `ToolCallingAdvisor` décide si les
    appels d'outils sont mémorisés). [2][4][24]

18. **MCP : un protocole d'intégration, pas une alternative au tool calling.**
    MCP (JSON-RPC 2.0, hôtes / clients / serveurs, inspiré du Language Server
    Protocol) standardise la découverte et l'appel d'outils, ressources et prompts
    exposés par des serveurs ; à la fin, le modèle fait toujours du tool calling
    classique. Prakash (Thoughtworks) : MCP apporte la découverte dynamique des
    outils au prix d'une complexité supplémentaire, justifiée seulement dans
    certains cas. Laravel (`laravel/mcp`) et Spring AI (`@McpTool`) savent exposer
    et consommer des outils MCP avec la même interface que les outils locaux. [14][18][23][24]

19. **MCP a beaucoup changé : version 2026-07-28.** Donné en décembre 2025 à
    l'Agentic AI Foundation (Linux Foundation, co-fondée par Anthropic, Block et
    OpenAI). La révision 2026-07-28 rend le protocole sans état : suppression du
    handshake `initialize` et de l'en-tête `Mcp-Session-Id`, ajout de
    `server/discover`, pattern « Multi Round-Trip Requests » à la place des
    requêtes initiées par le serveur, tâches longues sorties en extension,
    dépréciation de Roots, Sampling et Logging, du transport HTTP+SSE et de
    l'enregistrement dynamique OAuth au profit des Client ID Metadata Documents.
    Tout support décrivant la poignée de main `initialize` ou le sampling comme
    fonctionnement standard est daté. [14]

20. **Garde-fous : défense en couches et moindre privilège.** OpenAI : garde-fous
    combinés (classifieurs de pertinence et de sécurité, filtre PII, règles
    déterministes, validation de sortie) et notation du risque de chaque outil
    (lecture ou écriture, réversibilité, permissions, impact financier) qui
    déclenche une validation humaine. OWASP LLM06:2025 « Excessive Agency » :
    fonctionnalités, permissions et autonomie excessives ; parades : minimiser les
    outils, éviter les outils ouverts (shell, URL libre), exécuter dans le contexte
    de l'utilisateur, approbation humaine, « complete mediation » (l'autorisation
    se vérifie dans le système aval, jamais par le LLM). La spécification MCP
    demande un humain capable de refuser un appel d'outil et considère les
    annotations d'outils comme non fiables. [9][15][14]

21. **Erreurs d'outil : les renvoyer au modèle, pas planter.** MCP distingue les
    erreurs de protocole des erreurs d'exécution d'outil (`isError: true`), ces
    dernières devant être renvoyées au modèle pour qu'il se corrige. Laravel :
    erreurs de validation renvoyées comme résultat, `#[RepairToolCalls]` pour un
    outil inconnu. Spring AI : `RETURN_ERROR_RESPONSE` en cas de dépassement de
    plafond. 12-Factor (facteur 9) : compacter les erreurs et limiter les
    tentatives consécutives. C'est le lien entre S2.4 et S3.1 (résilience). [14][24][23][12]

22. **Multi-agents : à repousser.** OpenAI recommande de maximiser un agent unique
    avant d'en ajouter (patterns manager et handoff décentralisé) ; Anthropic voit
    un gain sur la recherche parallèle grâce à l'isolation des contextes, au prix
    de beaucoup plus de tokens. Pour un cours de 15 h, un agent unique bien outillé
    suffit ; le multi-agent est un approfondissement. [9][2]

23. **Erreurs composées : pourquoi borner l'autonomie.** Avec 95 % de réussite par
    étape, on tombe à environ 60 % sur 10 étapes et 0,6 % sur 100 (Huyen). Les
    agents ont aussi des enjeux plus élevés car ils agissent. ReAct (Yao et al.,
    ICLR 2023) est l'origine scientifique de l'entrelacement raisonnement / action
    / observation qui fonde la boucle ; Anthropic insiste pour obtenir à chaque
    étape une « vérité terrain » de l'environnement (résultat d'outil, test). [17][16][1]

24. **Frameworks : comprendre ce qu'il y a dessous.** Anthropic : commencer avec
    l'API directe, beaucoup de patterns tiennent en quelques lignes ; les
    frameworks masquent prompts et réponses, et les fausses hypothèses sur leur
    fonctionnement sont une source d'erreur fréquente. Horthy : les frameworks
    amènent à 70-80 % de qualité, au-delà il faut rétro-ingénierer. Spring AI 2.0
    (juin 2026) a justement sorti sa boucle d'outils de chaque implémentation de
    modèle pour en faire un advisor composable (`ToolCallingAdvisor`), et permet de
    reprendre la main sur la boucle (`toolCallingAdvisorAutoRegister(false)`). Cela
    valide la démarche « sans SDK d'abord, SDK ensuite ». [1][12][13][24]

25. **État des SDK au 24/11/2026 (à corriger dans la bibliographie).** `laravel/ai`
    est en v1.4.2 (24/11/2026 ; v1.0.0 publiée le 23/09/2026), plus en 0.x : outils
    par `make:tool` (méthodes `description`, `schema`, `handle`), `tools()` sur
    l'agent, `withTools`, approbation humaine, outils MCP, sous-agents, middleware.
    Spring AI est en v2.1.0 (20/11/2026 ; 2.0.0 le 12/06/2026) : `@Tool`,
    `ToolCallback`, `ToolCallingManager`, `returnDirect`. Ollama est en v0.40.18
    (24/11/2026). [24][23][25]

## 2. Ordre d'enseignement recommandé

Ordre conseillé pour la séance 2 et ses prérequis :

1. **(S1.2, déjà prévu) Propriétés du LLM** : non-déterminisme, latence, coût au
   token, dépendance externe. Prérequis pour comprendre le coût des définitions
   d'outils, les erreurs composées et le plafond d'itérations.
2. **(S1.4) Port + adaptateur du modèle** sans outils. Prérequis indispensable :
   le tool calling ajoute un type de message (appel d'outil / résultat) au port ;
   l'introduire avant que le port existe mélange deux difficultés.
3. **Sorties structurées / schéma JSON** (5 min en début de S2.1) : un appel
   d'outil n'est qu'une sortie structurée (12-Factor, facteur 4). Comprendre le
   schéma avant le contrat d'outil.
4. **S2.1 Tool calling, un seul aller-retour** : contrat (nom, description,
   schéma), le modèle demande, l'application exécute, résultat renvoyé. Puis
   qualité des outils (ACI) et moindre privilège (OWASP LLM06).
5. **Workflow contre agent et patterns de workflow** (début de S2.2) : à placer
   AVANT la boucle autonome, pour que l'apprenant sache qu'on peut s'arrêter à un
   workflow. C'est l'ordre d'Anthropic [1] (LLM augmenté, workflows, puis agents)
   et de LangGraph (« Workflows and agents »).
6. **S2.2 Boucle d'agent** : `while` sur la raison d'arrêt, conditions de sortie,
   plafonds ; puis machine à états persistée, pause pour approbation humaine,
   saga pour l'annulation (approfondissement).
7. **S2.3 RAG** comme pipeline, puis **exposé comme outil** de l'agent (lien avec
   la récupération « juste à temps »).
8. **S2.4 TP** : agent unique, un ou deux outils + outil de recherche, plafond
   d'itérations, erreurs d'outil renvoyées au modèle.
9. **Plus tard (S3-S5) ou en approfondissement** : context engineering avancé
   (compaction, mémoire, sous-agents), MCP, multi-agents, tool search.

Comparaison avec des références :

- **Anthropic, « Building effective agents » [1]** : LLM augmenté, puis cinq
  workflows de complexité croissante, puis agents, puis annexe sur l'écriture
  d'outils. Même logique « du plus simple au plus autonome » que le cours ; seule
  différence, Anthropic met l'écriture d'outils en annexe alors que le cours la
  met en premier (S2.1), ce qui est défendable car le TP sans SDK exige d'écrire
  le contrat avant la boucle.
- **OpenAI, « A practical guide to building agents » [9]** : quand construire un
  agent, puis fondations (modèle, outils, instructions), orchestration (agent
  unique puis multi-agents), garde-fous en dernier. Le cours a raison de garder la
  sécurité dans S2.1 (moindre privilège) en plus de S4.2 : chez OpenAI, la notation
  de risque des outils n'arrive qu'à la fin, ce qui est tardif pour un TP.
- **Chip Huyen, « AI Engineering », chap. 6 [17]** : RAG d'abord, puis agents
  (environnement et outils, planification, modes d'échec et évaluation). Ce
  séquençage RAG puis agents est l'inverse de S2.1-S2.3 ; l'ordre du cours
  (outils, boucle, RAG, TP combiné) reste cohérent si le RAG est présenté comme un
  outil parmi d'autres.
- **12-Factor Agents [12]** : part de « langage naturel vers appel d'outil »,
  puis prompts, contexte, outils = sorties structurées, état, contrôle du flux.
  Confirme de faire « sortie structurée et contrat » avant « boucle ».

Point d'ordre à surveiller dans la scénarisation : S2.2 ne dure que 25 min pour
boucle + machine à états + annulation + exposition API. La boucle et ses
conditions d'arrêt sont un prérequis dur du TP S2.4 ; la machine à états et la
saga peuvent rester en approfondissement comme prévu.

## 3. Erreurs et idées reçues fréquentes

- **« Le modèle appelle la fonction / exécute l'API. »** Faux : il émet une
  demande structurée ; l'application valide, autorise et exécute. Formulation à
  bannir des supports. [8][23]
- **« Un agent, c'est forcément autonome et multi-agents. »** La plupart des
  agents en production sont du logiciel déterministe avec quelques décisions de
  LLM ; commencer par un workflow ou un agent unique. [1][13][9]
- **« Un schéma strict suffit à sécuriser l'outil. »** Le schéma garantit la
  forme, pas le droit ni la cohérence métier : validation et autorisation dans le
  code (complete mediation). [15][10]
- **« Plus d'outils = agent plus capable. »** Faux : outils redondants ou
  ambigus dégradent le choix, et chaque définition coûte des tokens. [3][10]
- **« Un outil = un endpoint REST existant. »** Les wrappers 1:1 d'API marchent
  mal ; concevoir des outils orientés tâche. [3]
- **« Il suffit d'une fenêtre de contexte plus grande. »** Context rot :
  la qualité baisse avec la taille ; il faut curer le contexte. [2]
- **« Context engineering = prompt engineering renommé. »** Le premier couvre
  tout l'état passé au modèle à chaque tour (outils, historique, données), le
  second l'écriture des instructions. [2]
- **Boucle sans plafond.** Toujours un nombre maximal d'itérations et un budget ;
  c'est aussi un garde-fou de coût (S1.2). [1][9][24]
- **MCP présenté avec la poignée de main `initialize`, les sessions, le
  sampling ou le transport HTTP+SSE comme fonctionnement actuel** : daté depuis la
  révision 2026-07-28 (et HTTP+SSE est déprécié depuis 2025-03-26). Ne pas dire
  non plus que MCP « remplace » le tool calling. [14]
- **« MCP est le protocole d'Anthropic. »** Depuis le 9/12/2025, il est gouverné
  au sein de l'Agentic AI Foundation (Linux Foundation). [14]
- **Laravel AI SDK présenté comme 0.x / expérimental, Spring AI 1.x avec boucle
  d'outils interne à chaque `ChatModel`** : daté (laravel/ai v1.x depuis le
  23/09/2026 ; Spring AI 2.0 a déplacé la boucle dans `ToolCallingAdvisor`).
  La bibliographie actuelle du projet (laravel/ai « 0.x », Spring AI « 2.0.1 »)
  est à mettre à jour. [24][23]
- **Confondre « harness engineering » (outillage d'un agent de code qui écrit
  le projet) et harness de l'agent intégré à l'application.** [11][19]
- **Croire qu'un bon harness d'hier reste bon** : chaque composant encode une
  hypothèse sur une faiblesse du modèle ; à re-tester à chaque changement de
  modèle (y compris passage en local). [5][6][20]
- **Ignorer les différences de format entre fournisseurs** (`call_id` OpenAI,
  `tool_use_id` Anthropic, `tool_name` Ollama) : l'adaptateur doit les normaliser,
  sinon le « sans dépendance au fournisseur » du TP est faux. [10][8][25]
- **Citer « Building effective agents » sans signaler la mise à jour** : la page
  porte désormais une note indiquant que l'outillage décrit a beaucoup changé
  depuis décembre 2024 et renvoie à Claude Managed Agents ; les patterns restent
  valables, la liste de frameworks non. [1]
- **Chiffres de produits à ne pas généraliser** : « moins de 20 fonctions »
  (OpenAI, indication souple), 25 000 tokens (réglage de Claude Code), 98,7 %
  d'économie (un exemple d'Anthropic) ne sont pas des lois. [10][3][7]

## 4. Sources

1. Schluntz E. et Zhang B. (2024), _Building effective agents_, Anthropic
   (blog Engineering).
   https://www.anthropic.com/engineering/building-effective-agents ; écrit ;
   publié le 19/12/2024, page mise à jour depuis (note sur Claude Managed Agents,
   mention de Claude Agent SDK et Haiku 4.5) ; consulté le 24/11/2026 ;
   [S2.1, S2.2, S2.4, cadrage]. Référence de la distinction workflow / agent, des
   cinq patterns, de l'ACI et du conseil « API directe avant framework ».
2. Rajasekaran P., Dixon E., Ryan C. et Hadfield J. (2025), _Effective context
   engineering for AI agents_, Anthropic (blog Engineering).
   https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents ;
   écrit ; 29/09/2025 ; consulté le 24/11/2026 ; [S2.2, S2.3, S2.4, S5.1].
   Définition du context engineering, context rot, récupération juste à temps,
   compaction, notes, sous-agents ; définition « tools in a loop ».
3. Aizawa K. (2025), _Writing effective tools for AI agents, with AI agents_,
   Anthropic (blog Engineering).
   https://www.anthropic.com/engineering/writing-tools-for-agents ; écrit ;
   11/09/2025 ; consulté le 24/11/2026 ; [S2.1, S2.4, S4.1]. Principes concrets de
   conception d'outils et évaluation des outils par des boucles d'agent simples.
4. Young J. (2025), _Effective harnesses for long-running agents_, Anthropic
   (blog Engineering).
   https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents ;
   écrit ; 26/11/2025 ; consulté le 24/11/2026 ; [S2.2, approfondissement].
   Harness multi-sessions : agent initialiseur, fichier de progression, liste de
   fonctionnalités JSON, commits, tests de bout en bout.
5. Rajasekaran P. (2026), _Harness design for long-running application
   development_, Anthropic (blog Engineering).
   https://www.anthropic.com/research/harness-design-long-running-apps ; écrit ;
   24/03/2026 ; consulté le 24/11/2026 ; [S2.2, S4.1, cadrage]. Planner /
   generator / evaluator, biais d'auto-évaluation, et méthode pour simplifier un
   harness quand le modèle progresse.
6. Martin L., Cemaj G. et Cohen M. (2026), _Scaling Managed Agents: Decoupling
   the brain from the hands_, Anthropic (blog Engineering).
   https://www.anthropic.com/research/managed-agents ; écrit ; 08/04/2026 ;
   consulté le 24/11/2026 ; [S1.1, S2.2, S5.1]. Session / harness / sandbox comme
   interfaces découplées ; harness sans état, identifiants hors du modèle.
7. Jones A. et Kelly C. (2025), _Code execution with MCP: Building more efficient
   agents_, Anthropic (blog Engineering).
   https://www.anthropic.com/engineering/code-execution-with-mcp ; écrit ;
   04/11/2025 ; consulté le 24/11/2026 ; [S2.1 approfondissement]. Coût en tokens
   des définitions et résultats d'outils ; divulgation progressive par le code.
8. Anthropic (2026), _How tool use works_ et _Define tools_, Claude Platform
   Docs. https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works
   et https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools ;
   doc officielle ; version en ligne (sans numéro) ; consulté le 24/11/2026 ;
   [S2.1, S2.2, S2.4]. Contrat d'outil, outils client / serveur, boucle sur
   `stop_reason`, quand ne pas utiliser d'outil.
9. OpenAI (2025), _A practical guide to building agents_, OpenAI (guide PDF).
   https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf ;
   écrit ; non daté dans le document, fichier modifié le 11/04/2025 (en-tête
   HTTP) ; consulté le 24/11/2026 ; [S2.1, S2.2, S4.2, cadrage]. Modèle / outils /
   instructions, run et conditions de sortie, agent unique d'abord, garde-fous en
   couches, notation de risque des outils, intervention humaine.
10. OpenAI (2026), _Function calling_, OpenAI API documentation.
    https://platform.openai.com/docs/guides/function-calling ; doc officielle ;
    version en ligne (mentionne gpt-5.4, Responses API) ; consulté le
    24/11/2026 ; [S2.1, S2.4]. Flux en cinq étapes, `call_id`, `strict`,
    `tool_choice`, appels parallèles, espaces de noms, tool search, bonnes
    pratiques (moins de 20 fonctions, test du stagiaire).
11. Lopopolo R. (2026), _Harness engineering: leveraging Codex in an agent-first
    world_, OpenAI. https://openai.com/index/harness-engineering/ ; écrit ;
    11/02/2026 ; consulté le 24/11/2026 ; [cadrage, S5.2]. Sens « environnement
    pour agents de code » du mot harness : AGENTS.md comme carte, linters et tests
    structurels, dépôt comme source de vérité.
12. Horthy D. (2025), _12-Factor Agents: Principles for building reliable LLM
    applications_, GitHub (HumanLayer).
    https://github.com/humanlayer/12-factor-agents ; écrit ; dépôt créé le
    30/03/2025, mis à jour depuis ; consulté le 24/11/2026 ; [S2.1, S2.2, S2.4,
    S3.1]. Douze principes : outils = sorties structurées, posséder contexte et
    flux de contrôle, état unifié, pause / reprise, petits agents.
13. Horthy D. (2025), _12-Factor Agents: Patterns of reliable LLM applications_,
    AI Engineer World's Fair 2025 (conférence filmée).
    https://www.youtube.com/watch?v=8kMaTybvDUw (transcription et synthèse lues
    sur https://ai.engineer/talks/8kMaTybvDUw-12-factor-agents) ; vidéo ; 2025 ;
    consulté le 24/11/2026 ; [S2.2, cadrage]. « La plupart des agents en
    production sont surtout du logiciel » ; boucles de 3 à 10 étapes dans un
    graphe déterministe ; exemple d'agent de déploiement.
14. Model Context Protocol (2026), _Specification, version 2026-07-28_ (avec
    _Key Changes_ et _Server Features: Tools_), modelcontextprotocol.io ; et
    Anthropic (2025), _Donating the Model Context Protocol and establishing the
    Agentic AI Foundation_.
    https://modelcontextprotocol.io/specification/2026-07-28 (changelog :
    https://modelcontextprotocol.io/specification/2026-07-28/changelog) et
    https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation ;
    référentiel ; révision publiée le 28/07/2026 (précédente : 2025-11-25),
    annonce du 09/12/2025 ; consulté le 24/11/2026 ; [S2.1, S4.2, approfondissement].
    Architecture, définition d'un outil, erreurs `isError`, exigences de sécurité,
    passage au sans-état et dépréciations ; gouvernance AAIF.
15. OWASP Foundation (2025), _LLM06:2025 Excessive Agency_, OWASP Top 10 for LLM
    Applications 2025. https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ ;
    référentiel ; édition 2025 ; consulté le 24/11/2026 ; [S2.1, S4.2]. Trois
    causes (fonctionnalités, permissions, autonomie) et huit parades dont
    « complete mediation » ; base de l'exercice « outils à ne pas exposer ».
16. Yao S., Zhao J., Yu D., Du N., Shafran I., Narasimhan K. et Cao Y. (2023),
    ReAct: Synergizing Reasoning and Acting in Language Models, in _International
    Conference on Learning Representations (ICLR 2023)_, arXiv:2210.03629.
    https://arxiv.org/abs/2210.03629 ; article scientifique ; v3 du 10/03/2023 ;
    consulté le 24/11/2026 (résumé lu) ; [S2.2]. Origine de la boucle
    raisonnement / action / observation ; +34 et +10 points sur ALFWorld et
    WebShop.
17. Huyen C. (2025), _AI Engineering: Building Applications with Foundation
    Models_, Sebastopol, O'Reilly Media ; chapitre 6 adapté en billet _Agents_.
    https://huyenchip.com/2025/01/07/agents.html (page du livre :
    https://huyenchip.com/books/) ; livre + écrit ; billet du 07/01/2025 ;
    consulté le 24/11/2026 (billet lu en entier ; la page O'Reilly a refusé
    l'accès, livre non relu) ; [S2.1, S2.2, cadrage]. Agent = environnement +
    actions, types d'outils, planification, erreurs composées, modes d'échec.
18. Prakash K. (2025), _Function calling using LLMs_, martinfowler.com.
    https://martinfowler.com/articles/function-call-LLM.html ; écrit ;
    06/05/2025 ; consulté le 24/11/2026 ; [S2.1]. Exemple complet d'agent
    d'achat (Thoughtworks), le LLM n'exécute pas la fonction, place de MCP.
19. Böckeler B. (2026), _Harness engineering for coding agent users_,
    martinfowler.com. https://martinfowler.com/articles/harness-engineering.html ;
    écrit ; 02/04/2026 ; consulté le 24/11/2026 ; [cadrage]. « Agent = Model +
    Harness » ; guides (feedforward) et sensors (feedback), contrôles
    computationnels contre inférentiels.
20. Jain N. (2026), _Are Harnesses Worth the Cost?_, martinfowler.com.
    https://martinfowler.com/articles/are-harnesses-worth-the-cost.html ; écrit ;
    13/10/2026 ; consulté le 24/11/2026 ; [S1.3, S4.1, cadrage]. Expérience
    chiffrée : harness inutile et coûteux pour un modèle de pointe, décisif pour
    un modèle économique.
21. Willison S. (2025), _I think "agent" may finally have a widely enough agreed
    upon definition to be useful jargon now_, simonwillison.net.
    https://simonwillison.net/2025/Sep/18/agents/ ; écrit ; 18/09/2025 ;
    consulté le 24/11/2026 ; [cadrage, S2.2]. Définition « tools in a loop to
    achieve a goal », condition d'arrêt, usage du mot harness.
22. Richardson C. (s. d.), _Pattern: Saga_, microservices.io.
    https://microservices.io/patterns/data/saga.html ; écrit ; page non datée ;
    consulté le 24/11/2026 ; [S2.2]. Transactions locales et compensations,
    orchestration contre chorégraphie : base du « pattern pour annuler
    proprement ».
23. Tzolov C. (2026), _Tool Calling in Spring AI 2.0: A Composable, Agentic
    Architecture_, spring.io ; et VMware / Broadcom (2026), _Spring AI Reference:
    Tool Calling_. https://spring.io/blog/2026/06/15/spring-ai-composable-tool-calling/
    et https://docs.spring.io/spring-ai/reference/api/tools.html ; écrit + doc
    officielle ; billet du 15/06/2026, Spring AI v2.1.0 publiée le 20/11/2026 ;
    consulté le 24/11/2026 ; [S2.1, S2.2, S4.3]. `@Tool`, `ToolCallingAdvisor`
    récursif, plafonds d'appels, mémoire dans ou hors boucle, exécution contrôlée
    par l'utilisateur, `@McpTool`.
24. Laravel LLC (2026), _Laravel AI SDK_ (package `laravel/ai`), documentation
    Laravel 13.x. https://laravel.com/docs/ai-sdk (Markdown lu :
    https://laravel.com/framework/docs/13.x/ai-sdk.md) ; doc officielle ;
    v1.4.2 publiée le 24/11/2026 (v1.0.0 le 23/09/2026) ; consulté le
    24/11/2026 ; [S2.1, S2.3, S2.4, S4.3]. Contrat `Tool` (`description`,
    `schema`, `handle`), validation renvoyée au modèle, `RepairToolCalls`,
    `MaxSteps`, `Stop`, approbation humaine, outils MCP, `ToolSearch`.
25. Ollama (2026), _Tool calling_, Ollama Documentation.
    https://docs.ollama.com/capabilities/tool-calling ; doc officielle ; Ollama
    v0.40.18 publiée le 24/11/2026 ; consulté le 24/11/2026 ; [S1.3, S2.1, S2.4].
    Format local des appels (`role: "tool"`, `tool_name`), appels parallèles,
    boucle d'agent multi-tours, conseil de dire au modèle qu'il est dans une
    boucle.
26. Martin L. (2025), _Context Engineering for Agents_, blog personnel
    (rlancemartin.github.io) ; et Latent Space (2025), _Context Engineering for
    Agents, Lance Martin, LangChain_, podcast Latent Space: The AI Engineer
    Podcast. https://rlancemartin.github.io/2025/06/23/context_engineering/ et
    https://latent.space/p/context-engineering-for-agents-lance/ ; écrit + audio /
    vidéo ; billet du 23/06/2025, épisode du 11/09/2025 (58 min) ; consulté le
    24/11/2026 (billet lu en entier ; pour l'épisode, seuls la description, les
    liens et le minutage détaillé ont été lus, pas la transcription) ; [S2.2,
    S2.3, S5.1]. Quatre familles de techniques (écrire, sélectionner, compresser,
    isoler) ; l'épisode relie context engineering, recherche agentique contre RAG
    classique, MCP et « bitter lesson » appliquée aux frameworks.

Sources lues mais non retenues comme entrées (pour mémoire) : LangChain,
_Workflows and agents_ (docs LangGraph, même distinction qu'Anthropic) ;
Yan W. (2025), _Don't Build Multi-Agents_, Cognition (12/06/2025) ;
Subramaniam B. et Fowler M. (2025), _Emerging Patterns in Building GenAI
Products_ (patterns RAG / garde-fous / evals, ne traite pas des agents).
