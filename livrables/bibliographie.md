---
title: "Bibliographie"
subtitle: "Projet FYC 2026-2027"
---

<!--
Reprise de la bibliographie V1 (livrables/archives/2026-07-08-scenarisation-v1.pdf)
réorganisée selon les retours du mentor (retours-mentor/2026-07-08-seance-1.md) :
- catégories : ouvrages / publications scientifiques / documentation technique
- chaque entrée : auteur ou organisme, titre complet, date, version, URL, consulté le
- normes : ressources/normes-bibliographie.pdf

Chaque entrée a été vérifiée à la source le 8 septembre 2026. Les versions et
les référentiels ont été revérifiés le 24 novembre 2026 (audit B3, FYC-96) :
la date « consulté le » de chaque entrée dit laquelle des deux s'applique.
Les versions sont à revérifier avant chaque dépôt sur Teams.
[Sx.y] = séquence qui s'en sert, selon la trame V2 (00.3 = installation).
-->

# Ouvrages

- Nygard M. (2018), _Release It! Design and Deploy Production-Ready Software_,
  2e édition, Raleigh, Pragmatic Bookshelf. [S3.2]
  _Coupe-circuit, bulkhead, timeouts : les bases de la résilience._

# Publications scientifiques

## Évaluation des LLM et des pipelines RAG

- Zheng L., Chiang W.-L., Sheng Y., Zhuang S., Wu Z., Zhuang Y., Lin Z., Li Z.,
  Li D., Xing E.P., Zhang H., Gonzalez J.E. et Stoica I. (2023), Judging
  LLM-as-a-judge with MT-Bench and Chatbot Arena, in A. Oh, T. Naumann,
  A. Globerson, K. Saenko, M. Hardt et S. Levine (coord.), _Advances in Neural
  Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks
  Track_, [lieu à compléter], Curran Associates, 46595-46623. [S4.1]
  _Protocole de référence pour faire juger les réponses d'un LLM par un autre
  LLM : accord avec le jugement humain, biais connus (position, verbosité,
  auto-préférence)._
- Es S., James J., Espinosa Anke L. et Schockaert S. (2024), RAGAs: automated
  evaluation of retrieval augmented generation, in N. Aletras et O. De Clercq
  (coord.), _Proceedings of the 18th Conference of the European Chapter of the
  Association for Computational Linguistics: System Demonstrations_, St. Julians
  (Malte), Association for Computational Linguistics, 150-158. [S2.3, S4.1]
  _Évalue un pipeline RAG (fidélité de la génération, pertinence de la
  récupération) sans jeu de réponses de référence._

## Le RAG comme pipeline de données

- Lewis P., Perez E., Piktus A., Petroni F., Karpukhin V., Goyal N.,
  Küttler H., Lewis M., Yih W., Rocktäschel T., Riedel S. et Kiela D. (2020),
  Retrieval-augmented generation for knowledge-intensive NLP tasks, in
  H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan et H. Lin (coord.),
  _Advances in Neural Information Processing Systems 33 (NeurIPS 2020)_,
  [lieu à compléter], Curran Associates, 9459-9474. [S2.3]
  _Article fondateur du RAG : combine un modèle de récupération dense et un
  générateur pré-entraîné._
- Karpukhin V., Oguz B., Min S., Lewis P., Wu L., Edunov S., Chen D. et
  Yih W. (2020), Dense passage retrieval for open-domain question answering,
  in B. Webber, T. Cohn, Y. He et Y. Liu (coord.), _Proceedings of the 2020
  Conference on Empirical Methods in Natural Language Processing (EMNLP)_,
  en ligne, Association for Computational Linguistics, 6769-6781. [S2.3]
  _Fondement technique de la recherche par similarité sur des vecteurs denses,
  utilisée sur pgvector._
- Gao Y., Xiong Y., Gao X., Jia K., Pan J., Bi Y., Dai Y., Sun J., Wang M. et
  Wang H. (2023), Retrieval-augmented generation for large language models:
  a survey, papier de recherche, arXiv:2312.10997 (v5 du 27 mars 2024). [S2.3]
  _Panorama des architectures RAG et de leurs limites : qualité de la
  récupération, contenu non pertinent ou contradictoire, coût et latence._
- Liu N.F., Lin K., Hewitt J., Paranjape A., Bevilacqua M., Petroni F. et
  Liang P. (2024), Lost in the middle: how language models use long contexts,
  _Transactions of the Association for Computational Linguistics_, 12,
  157-173. [S2.3]
  _Plus de contexte n'est pas mieux : l'information placée au milieu d'un long
  contexte est moins bien exploitée._

## Injections de prompt

- Perez F. et Ribeiro I. (2022), Ignore previous prompt: attack techniques for
  language models, papier présenté au ML Safety Workshop de NeurIPS 2022,
  arXiv:2211.09527. [S4.2]
  _Démonstration d'origine du détournement d'objectif et de la fuite de
  prompt par injection directe._
- Greshake K., Abdelnabi S., Mishra S., Endres C., Holz T. et Fritz M. (2023),
  Not what you've signed up for: compromising real-world LLM-integrated
  applications with indirect prompt injection, in [coordinateurs à compléter]
  (coord.), _Proceedings of the 16th ACM Workshop on Artificial Intelligence
  and Security (AISec '23)_, New York, ACM, 79-90,
  https://doi.org/10.1145/3605764.3623985. [S4.2]
  _Démonstration d'origine de l'injection indirecte via des documents
  récupérés. Atelier tenu à Copenhague ; lieu d'édition ACM : New York, d'après
  Crossref._
- Liu Y., Deng G., Li Y., Wang K., Wang Z., Wang X., Zhang T., Liu Y.,
  Wang H., Zheng Y., Zhang L.Y. et Liu Y. (2023), Prompt injection attack
  against LLM-integrated applications, papier de recherche, arXiv:2306.05499
  (v3 du 29 décembre 2025). [S4.2]
  _Étude empirique sur 36 applications réelles intégrant un LLM : 31 se sont
  révélées vulnérables à l'injection de prompt._

## Tests de systèmes probabilistes / non déterministes

- Zhang J.M., Harman M., Ma L. et Liu Y. (2022), Machine learning testing:
  survey, landscapes and horizons, _IEEE Transactions on Software
  Engineering_, 48, 1, 1-36. [S4.1]
  _Panorama des propriétés testées (correction, robustesse, équité) et des
  méthodes de test adaptées aux systèmes ML, dont le problème de l'oracle
  face à la non-déterminicité._
- Ribeiro M.T., Wu T., Guestrin C. et Singh S. (2020), Beyond accuracy:
  behavioral testing of NLP models with CheckList, in D. Jurafsky, J. Chai,
  N. Schluter et J. Tetreault (coord.), _Proceedings of the 58th Annual Meeting
  of the Association for Computational Linguistics_, en ligne, Association for
  Computational Linguistics, 4902-4912. [S4.1]
  _Méthode concrète pour construire un jeu de tests de référence organisé par
  comportement attendu plutôt que par exactitude stricte._

# Référentiels et standards

- OWASP GenAI Security Project (2026), _OWASP GenAI LLM Top 10 2026_, édition
  2026 (ressource datée du 3 août 2026),
  https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/, consulté le
  24 novembre 2026. [S4.2]
  _Grille des dix risques de S4.2. L'injection de prompt est en première place
  dans toutes les éditions (2023, 2025, 2026)._
- OWASP GenAI Security Project (2026), _LLM01:2026 Prompt Injection_, édition
  2026, https://genai.owasp.org/llm2026/llm012026-prompt-injection/, consulté
  le 24 novembre 2026. [S1.2, S4.2, S4.3]
  _Fiche du risque n° 1 : pas de mécanisme de prévention fiable à ce jour,
  d'où la priorité aux mesures qui bornent l'impact._
- OWASP GenAI Security Project (2025), _OWASP Top 10 for Agentic Applications
  for 2026_, publié le 9 décembre 2025,
  https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/,
  consulté le 24 novembre 2026. [S4.2]
- Commission européenne (2026), _Transparency obligations under Article 50 of
  the AI Act_ (FAQ), mise à jour du 24 juillet 2026,
  https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act,
  consulté le 24 novembre 2026. [S5.1, S5.3]
  _Obligation d'informer l'utilisateur qu'il échange avec une IA, applicable
  depuis le 2 août 2026._
- OpenTelemetry (2026), _Semantic Conventions for Generative AI systems_,
  spécification en évolution continue, pas de numéro de version stable,
  https://github.com/open-telemetry/semantic-conventions-genai, consulté le
  8 septembre 2026. [S3.3]

# Documentation technique

## Architecture logicielle

- Cockburn A. (2005), _Hexagonal Architecture_ (HaT Technical Report 2005.02),
  article en ligne, https://alistair.cockburn.us/hexagonal-architecture/,
  consulté le 8 septembre 2026. [S1.1]
- Fowler M. (2011), _CQRS_, article en ligne (martinfowler.com),
  https://martinfowler.com/bliki/CQRS.html, consulté le 8 septembre 2026.
  [S1.1]
- Martin R.C. (2014), _The single responsibility principle_, billet en ligne
  (The Clean Code Blog), 8 mai 2014,
  https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html,
  consulté le 24 novembre 2026. [S1.1]

## Agents, résilience et sécurité : billets de référence

- Schluntz E. et Zhang B. (2024), _Building effective agents_, billet en ligne
  (Anthropic Engineering), 19 décembre 2024, mis à jour depuis,
  https://www.anthropic.com/engineering/building-effective-agents, consulté le
  24 novembre 2026. [S2.1, S2.2, S5.3]
  _Distinction workflow / agent et patterns de base ; argument pour commencer
  sans framework._
- Willison S. (2025), _The lethal trifecta for AI agents: private data,
  untrusted content, and external communication_, billet en ligne
  (simonwillison.net), 16 juin 2025,
  https://simonwillison.net/2025/jun/16/the-lethal-trifecta/, consulté le
  24 novembre 2026. [S2.1, S4.2]
  _Les trois ingrédients qui rendent un agent exploitable ; base de la règle de
  deux appliquée à NoteFlow en S4.2._
- He H. et Thinking Machines Lab (2025), _Defeating nondeterminism in LLM
  inference_, billet de recherche (Connectionism), septembre 2025,
  doi:10.64434/tml.20250910,
  https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/,
  consulté le 24 novembre 2026. [S1.2, S4.1]
  _Pourquoi température 0 ne garantit pas une réponse identique._
- Brooker M. (2019), _Timeouts, retries, and backoff with jitter_, Amazon
  Builders' Library, 5 décembre 2019,
  https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/,
  consulté le 24 novembre 2026. [S1.2, S3.1, S3.2]
- Fowler M. (2014), _CircuitBreaker_, article en ligne (martinfowler.com),
  6 mars 2014, https://martinfowler.com/bliki/CircuitBreaker.html, consulté le
  24 novembre 2026. [S3.2]

## Frameworks et SDK

- VMware / Broadcom (2026), _Spring AI Reference Documentation_, version 2.1.0
  (publiée le 20 novembre 2026), https://docs.spring.io/spring-ai/reference/,
  consulté le 24 novembre 2026. [S2.1, S2.3, S3.2, S3.3, S4.1]
- Laravel LLC (2026), _Laravel AI SDK Documentation_ (package `laravel/ai`),
  version 1.4.2 (publiée le 24 novembre 2026 ; v1.0.0 le 23 septembre 2026,
  github.com/laravel/ai/releases), https://laravel.com/docs/ai-sdk, consulté
  le 24 novembre 2026. [S2.1, S2.3, S3.2, S4.1]
- Laravel LLC (2026), _Laravel 13 Documentation_, version 13.x (framework
  v13.44.1 au 24 novembre 2026), https://laravel.com/docs/13.x, consulté le
  24 novembre 2026. [S1.1, S1.2, S2.3, S3.1, S5.2]
  _Documentation distincte de celle du Laravel AI SDK (`laravel.com/docs/ai-sdk`,
  package `laravel/ai` séparé)._
- Resilience4j (2026), _Resilience4j User Guide_, version 2.4.0 (publiée le
  14 mars 2026), https://resilience4j.readme.io/, consulté le 24 novembre 2026.
  [S3.2]
- The PHP Group (2026), _PHP Manual : set_time_limit_ (note sur
  `max_execution_time`), https://www.php.net/manual/en/function.set-time-limit.php,
  consulté le 24 novembre 2026. [S1.2]

## Fournisseurs de modèles

- Mistral AI (2026), _Models Overview_ et _Mistral Small 4_, Mistral AI
  Documentation, https://docs.mistral.ai/models et
  https://docs.mistral.ai/models/mistral-small-4-0-26-03, consulté le
  25 novembre 2026. [S1.1, S1.3]
  _Identifiant daté `mistral-small-2603` et alias `mistral-small-latest` ;
  `mistral-small-2506` déprécié._
- Anthropic (2026), _Model IDs and versioning_ et _Model deprecations_, Claude
  Platform Docs,
  https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions
  et https://platform.claude.com/docs/en/about-claude/model-deprecations,
  consulté le 24 novembre 2026. [S1.2, S5.1]
  _Épinglage d'un identifiant de modèle et calendrier de retrait des modèles._

## Outils

- Ollama (2026), _Ollama Documentation_, version 0.40.18 (publiée le
  24 novembre 2026), https://docs.ollama.com/, consulté le 24 novembre 2026.
  [00.3]
- pgvector (2026), _pgvector: open-source vector similarity search for
  Postgres_, version 0.8.7 (publiée le 1er octobre 2026),
  https://github.com/pgvector/pgvector, consulté le 24 novembre 2026. [00.3,
  S2.3]
