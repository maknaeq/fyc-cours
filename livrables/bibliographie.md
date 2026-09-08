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

Les champs « _à compléter_ » sont à renseigner par le groupe après vérification
de la source. Ne pas inventer de date ni d'URL.
(★) = lecture prioritaire pour l'apprenant. [Sx.y] = séquence qui s'en sert.
-->

# Ouvrages

- Nygard M. (2018), _Release It! Design and Deploy Production-Ready Software_,
  2e édition, Raleigh, Pragmatic Bookshelf. [S3.1]
  _Coupe-circuit, bulkhead, timeouts : les bases de la résilience._

# Publications scientifiques

## Évaluation des LLM et des pipelines RAG

- Zheng L., Chiang W.-L., Sheng Y., Zhuang S., Wu Z., Zhuang Y., Lin Z., Li Z.,
  Li D., Xing E.P., Zhang H., Gonzalez J.E. et Stoica I. (2023), Judging
  LLM-as-a-Judge with MT-Bench and Chatbot Arena, in _Advances in Neural
  Information Processing Systems 36 (NeurIPS 2023)_, 46595-46623. [S4.1]
  _Protocole de référence pour faire juger les réponses d'un LLM par un autre
  LLM : accord avec le jugement humain, biais connus (position, verbosité,
  auto-préférence)._
- Es S., James J., Espinosa Anke L. et Schockaert S. (2024), RAGAs: Automated
  Evaluation of Retrieval Augmented Generation, in _Proceedings of the 18th
  Conference of the European Chapter of the Association for Computational
  Linguistics: System Demonstrations_, 150-158. [S2.3, S4.1]
  _Évalue un pipeline RAG (fidélité de la génération, pertinence de la
  récupération) sans jeu de réponses de référence._

## Le RAG comme pipeline de données

- Lewis P., Perez E., Piktus A., Petroni F., Karpukhin V., Goyal N.,
  Küttler H., Lewis M., Yih W., Rocktäschel T., Riedel S. et Kiela D. (2020),
  Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, in
  _Advances in Neural Information Processing Systems 33 (NeurIPS 2020)_,
  9459-9474. [S2.3]
  _Article fondateur du RAG : combine un modèle de récupération dense et un
  générateur pré-entraîné._
- Karpukhin V., Oguz B., Min S., Lewis P., Wu L., Edunov S., Chen D. et
  Yih W. (2020), Dense Passage Retrieval for Open-Domain Question Answering,
  in _Proceedings of the 2020 Conference on Empirical Methods in Natural
  Language Processing (EMNLP)_, 6769-6781. [S2.3]
  _Fondement technique de la recherche par similarité sur des vecteurs denses,
  utilisée sur pgvector._
- Gao Y., Xiong Y., Gao X., Jia K., Pan J., Bi Y., Dai Y., Sun J., Wang M. et
  Wang H. (2023), Retrieval-Augmented Generation for Large Language Models:
  A Survey, arXiv:2312.10997. [S2.3]
  _Panorama des architectures RAG et de leurs limites : qualité de la
  récupération, contenu non pertinent ou contradictoire, coût et latence._

## Injections de prompt

- Perez F. et Ribeiro I. (2022), Ignore Previous Prompt: Attack Techniques
  For Language Models, in _NeurIPS 2022 ML Safety Workshop_, arXiv:2211.09527.
  [S4.2]
  _Démonstration d'origine du détournement d'objectif et de la fuite de
  prompt par injection directe._
- Greshake K., Abdelnabi S., Mishra S., Endres C., Holz T. et Fritz M. (2023),
  Not what you've signed up for: Compromising real-world LLM-integrated
  applications with indirect prompt injection, in _Proceedings of the 16th ACM
  Workshop on Artificial Intelligence and Security (AISec '23)_, Copenhague,
  ACM, 79-90, https://doi.org/10.1145/3605764.3623985. [S4.2]
  _Démonstration d'origine de l'injection indirecte via des documents
  récupérés._
- Liu Y., Deng G., Li Y., Wang K., Wang Z., Wang X., Zhang T., Liu Y.,
  Wang H., Zheng Y. et Liu Y. (2023), Prompt Injection attack against
  LLM-integrated Applications, arXiv:2306.05499. [S4.2]
  _Étude empirique sur 36 applications réelles intégrant un LLM : 31 se sont
  révélées vulnérables à l'injection de prompt._

## Tests de systèmes probabilistes / non déterministes

- Zhang J.M., Harman M., Ma L. et Liu Y. (2022), Machine Learning Testing:
  Survey, Landscapes and Horizons, _IEEE Transactions on Software
  Engineering_, 48, 1, 1-36. [S4.1]
  _Panorama des propriétés testées (correction, robustesse, équité) et des
  méthodes de test adaptées aux systèmes ML, dont le problème de l'oracle
  face à la non-déterminicité._
- Ribeiro M.T., Wu T., Guestrin C. et Singh S. (2020), Beyond Accuracy:
  Behavioral Testing of NLP Models with CheckList, in _Proceedings of the
  58th Annual Meeting of the Association for Computational Linguistics_,
  4902-4912. [S4.1]
  _Méthode concrète pour construire un jeu de tests de référence organisé par
  comportement attendu plutôt que par exactitude stricte._

# Référentiels et standards

<!-- MENTOR : préciser l'édition exacte, distinguer LLM Applications et Agentic Applications. -->

- OWASP Foundation (2025), _OWASP Top 10 for LLM Applications_, édition 2025
  (v2025), URL _à compléter_, consulté le _à compléter_. (★) [S4.2]
- OWASP Foundation (_année à compléter_), _OWASP Top 10 for Agentic
  Applications_, édition _à compléter_, URL _à compléter_, consulté le
  _à compléter_. [S4.2]
- OpenTelemetry (_année à compléter_), _Semantic Conventions for Generative AI
  systems_, version _à compléter_, URL _à compléter_, consulté le _à compléter_. [S3.2]

# Documentation technique

## Architecture logicielle

- Cockburn A. (2005), _Hexagonal Architecture_, article en ligne,
  URL _à compléter_, consulté le _à compléter_. [S1.1]
- Fowler M. (2011), _CQRS_, article en ligne (martinfowler.com),
  consulté le _à compléter_. [S1.1]

## Frameworks et SDK

<!-- MENTOR : distinguer la documentation Laravel 13 de celle du Laravel AI SDK ;
sourcer officiellement la date de sortie du Laravel AI SDK. -->

- VMware / Broadcom (_année_), _Spring AI Reference Documentation_, version
  _à compléter_, URL _à compléter_, consulté le _à compléter_. (★) [S2.1, S2.3, S3.2, S4.1]
- Laravel LLC (_année_), _Laravel AI SDK Documentation_ (package `laravel/ai`),
  version _à compléter_, URL _à compléter_, consulté le _à compléter_. (★)
  [S2.1, S2.3, S3.1, S4.1]
  _Date de sortie annoncée en V1 : février 2026, à relier à une source officielle._
- Laravel LLC (_année_), _Laravel 13 Documentation_, URL _à compléter_,
  consulté le _à compléter_. [S1.1]
- Resilience4j (_année_), _Resilience4j User Guide_, version _à compléter_,
  URL _à compléter_, consulté le _à compléter_. [S3.1]

## Outils

- Ollama (_année_), _Ollama Documentation_, version _à compléter_,
  URL _à compléter_, consulté le _à compléter_. (★) [S1.3]
- pgvector (_année_), _pgvector: Open-source vector similarity search for
  Postgres_, version _à compléter_, URL _à compléter_, consulté le _à compléter_. [S2.3]
