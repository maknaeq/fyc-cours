---
title: "Concevoir une application web maintenable intégrant un agent IA : architecture, tests, sécurité et mise en production"
subtitle: "Document de scénarisation, version finale (séance 2, 09/09/2026)"
author: "Quentin Bauduin, Timothé Geoffroy, Kaan Topkaya, Erwin Gossin"
date: "9 septembre 2026"
---

# Titre du module

**Concevoir une application web maintenable intégrant un agent IA : architecture, tests, sécurité et mise en production.**

Parcours technique : Laravel (PHP). Le Laravel AI SDK et Spring AI (Java) servent de points de comparaison dans les supports.

# Problématique

> **Comment intégrer un agent IA dans une application web sans dégrader sa maintenabilité, sa testabilité, sa sécurité et sa maîtrise en production ?**

La démarche complète (opinion admise, constats, questions, délimitation) est
dans `livrables/problematique.md`.

# Synoptique de l'intervention

Ce cours se déroule en 5 séances de 3 heures. Le but : apprendre à construire
une appli web qui utilise une IA, sans que ça devienne un bazar impossible à
maintenir.

On ne va pas traiter l'IA comme une fonctionnalité magique qu'on branche et qui
marche toute seule. Mais on ne va pas non plus la traiter comme un composant
comme un autre. Un agent IA se branche comme une dépendance technique, derrière
une interface, au même titre qu'une base de données ou un service de paiement.
Son comportement, lui, n'a rien d'ordinaire : il ne répond jamais deux fois
pareil, il met un temps variable à répondre, chaque appel coûte de l'argent, il
dépend d'un fournisseur que vous ne contrôlez pas, et il ouvre une surface
d'attaque nouvelle. Ce sont ces cinq caractéristiques qui structurent le cours :
chacune oblige à adapter l'architecture, les tests, l'observabilité, la sécurité
ou la mise en production.

Le cours suit un seul parcours technique, Laravel (PHP), et un seul projet
fil rouge que vous faites évoluer de séance en séance jusqu'à sa mise en
ligne. Chaque séance mélange trois choses : un peu de théorie sur
l'architecture, un TP, et une comparaison.

Un choix pédagogique structure les TP : **vous n'utilisez pas de SDK d'IA**.
Vous écrivez vous-même l'adaptateur vers le fournisseur, le contrat d'outil, la
boucle d'agent, le pipeline RAG, le retry et le plan de secours, les doublures
de test. À la fin de chaque étape, la comparaison montre côte à côte ce que
vous venez de construire, comment le Laravel AI SDK le fait, et comment Spring
AI le fait côté Java. L'objectif est d'arriver, à la fin du cours, à une
architecture qui ressemble à celle d'un SDK, en ayant compris pourquoi chaque
pièce existe. La comparaison est une méthode d'étude, pas la finalité : elle
sert à séparer ce qui vient du framework de ce qui relève de principes
d'architecture valables quel que soit le langage.

Dès la première séance, on installe aussi une IA qui tourne directement sur
votre ordinateur, en plus de celle disponible sur internet. Comme ça, si vous
voulez, vous pouvez faire tous les TP sans payer et sans clé d'accès. C'est
aussi un bon exemple concret : le code doit pouvoir marcher avec l'IA en ligne
ou l'IA locale sans qu'on ait à le réécrire, on change juste « l'adaptateur »
branché derrière.

# Objectifs de la formation

À la fin du module, vous serez capables de :

- Isoler un agent IA derrière une interface comme une dépendance technique,
  tout en tenant compte de ce qui le distingue : non-déterminisme, latence
  variable, coût par appel, dépendance à un fournisseur, nouveaux risques.
- Choisir une bonne façon d'organiser son code (architecture hexagonale, CQRS,
  événements) pour ajouter de l'IA sans tout coller ensemble.
- Construire soi-même les briques d'intégration d'une IA (adaptateur de
  fournisseur, outils, boucle d'agent, RAG, résilience) puis les comparer à ce
  qu'offrent un SDK (Laravel AI SDK, Spring AI) avec des critères concrets :
  est-ce facile de changer de fournisseur, facile à surveiller, combien ça coûte.
- Tester une application dont les réponses ne sont jamais garanties identiques
  (l'IA ne répond pas toujours pareil, contrairement à du code classique).
- Repérer et limiter les risques : quelqu'un qui manipule l'IA avec un texte
  piégé, l'IA qui invente des choses fausses, des données confidentielles qui
  fuient, une facture qui explose, des réponses trop lentes.
- Justifier un choix technique (framework, outil, fournisseur d'IA) avec de
  vrais arguments d'ingénieur, pas juste parce que « c'est à la mode ».

# Pré-requis

- Programmer en orienté objet en PHP et connaître les bases de Laravel
  (routes, contrôleurs, Eloquent, injection de dépendances).
- Savoir ce qu'est une API REST et comment marche une requête/réponse HTTP.
- Avoir une petite idée de ce qu'est une architecture logicielle (des couches,
  séparer les responsabilités).
- Savoir utiliser Git/GitHub au quotidien.

# Environnement nécessaire à la formation

- Un IDE, Git, PHP 8.3+ et Composer, Docker pour PostgreSQL. Aucune
  connaissance de Java n'est nécessaire : les extraits Spring AI se lisent,
  ils ne s'exécutent pas.
- Une clé d'accès chez un fournisseur d'IA en ligne (lequel sera précisé plus tard).
- Ou en alternative gratuite : une IA installée en local (par exemple avec
  Ollama), pour faire tous les TP sans payer. Machine recommandée : 16 Go de
  RAM, avec un petit modèle.
- Un endroit pour stocker des « embeddings » (des bouts de texte transformés en
  listes de nombres, pour pouvoir chercher par ressemblance), par exemple
  pgvector, pour les TP sur le RAG.

# Plan du cours

Durée totale : **15 h** (5 séances de 3 h).

| N° | Durée | Titre | Ce qu'on apprend | Équipement & matériel |
|-----|------|-----------------|----------------------------------------|--------------|
| S1.1 | 45 min | Architectures web : les bases | Revoir les couches, la séparation des responsabilités, l'architecture hexagonale (isoler le cœur du code des outils externes) et le pattern CQRS (séparer lecture et écriture des données), appliqués à une appli web (contrôleur → service → domaine) | Vidéo d'intro, support écrit, dépôt d'exemples Laravel et Spring Boot |
| S1.2 | 45 min | Pourquoi l'IA complique les architectures classiques | Comprendre l'effet du fait qu'une IA ne répond jamais exactement pareil, met un temps variable à répondre, coûte à chaque appel, et dépend d'un service externe | Support écrit, étude de cas (dépôt + vidéo du timeout), fiche de réponse, corrigé |
| S1.3 | 40 min | Installer son environnement : IA en ligne ou IA en local | Installer et configurer une IA en local (ex. Ollama) comme alternative à une IA en ligne ; brancher l'une ou l'autre au même endroit du code, et voir ce que ça change (prix, vitesse, confidentialité, TP faisables sans connexion) | Guide d'installation, docker-compose pgvector, Ollama + modèle, clé API, script de vérification |
| S1.4 | 50 min | TP : réorganiser un code « fourre-tout » | Transformer un contrôleur Laravel qui fait tout vers une architecture plus propre (« ports/adapters »), sans SDK, puis comparer avec ce qu'imposent le Laravel AI SDK et Spring AI à l'aide d'une grille corrigée | Dépôt de départ Laravel avec tests, branche corrigée, grille comparative et corrigé |
| S2.1 | 45 min | Function / tool calling | Comprendre comment une IA peut « demander » à du code métier d'exécuter une action (nom, description, format des paramètres) ; écrire ce contrat soi-même, puis le comparer à celui du Laravel AI SDK et de Spring AI | Support écrit, squelette de contrat d'outil, extraits Laravel AI SDK et Spring AI |
| S2.2 | 25 min | Organiser le travail d'un agent | Mettre en place une « machine à états » pour un agent, un enchaînement d'appels, et un pattern pour annuler proprement en cas d'échec, pour une tâche en plusieurs étapes exposée par une API | Support écrit, étude de cas en trois étapes, schéma de boucle d'agent |
| S2.3 | 45 min | Le RAG comme pipeline de données | Concevoir : récupérer des documents, les découper, les transformer en vecteurs, les indexer, puis aller les rechercher pour les donner en contexte à l'IA ; le construire sur pgvector, puis le comparer aux VectorStore de Spring AI et à la recherche du Laravel AI SDK | PostgreSQL + pgvector (Docker), jeu de documents à indexer, squelette d'indexation, extraits SDK |
| S2.4 | 65 min | TP : agent avec outils + recherche par similarité | Construire un agent (qui utilise des outils + une recherche par ressemblance) sur un cas simple, en Laravel et sans SDK | Présentation du fil rouge, dépôt du fil rouge, documents à indexer, critères de réussite |
| S3.1 | 55 min | Rendre son appli solide face à l'incertitude | Mettre en place : réessayer un appel qui échoue, un « coupe-circuit » qui bloque les appels si ça part en vrille, et un plan de repli (IA locale, puis mode sans IA) | Support écrit, script de panne simulée, squelettes retry et coupe-circuit, extraits SDK et Resilience4j |
| S3.2 | 50 min | Surveiller ce que fait l'agent | Suivre chaque appel à l'IA, avoir des logs bien structurés, et des chiffres utiles (coût, vitesse, taux d'échec) dans une appli web | Support écrit, exemple de logs structurés, extraits SDK et Spring AI, grille de coût |
| S3.3 | 1 h 15 | TP : suivi + plan de secours | Ajouter le suivi et un mode de secours à l'agent construit en séance 2, puis se corriger avec la vidéo de correction guidée | Agent du fil rouge (état fin S2), script de panne simulée, vidéo de correction, corrigé |
| S4.1 | 55 min | Tester un système qui ne répond jamais pareil | Simuler les réponses de l'IA, créer un jeu de tests de référence, utiliser une IA pour juger une autre IA, détecter quand la qualité baisse | Support écrit, squelette de doublure PHPUnit/Pest, modèle de jeu de tests de référence |
| S4.2 | 50 min | Risques et sécurité | Comprendre et limiter : les tentatives de manipuler l'IA avec un texte piégé (directement ou caché dans un document), les fuites de données, les inventions de l'IA dans un contexte sensible | Support écrit, référentiel OWASP (lien), document piégé pour l'injection indirecte, liste de parades |
| S4.3 | 15 min | Comparer les approches | Comparer ce que l'apprenant a construit, le Laravel AI SDK, Spring AI et des outils dédiés (LangChain/LangGraph) sur : facilité à changer de fournisseur, facilité à surveiller, coût, maturité | Grille de comparaison vierge et corrigée, cas de décision |
| S4.4 | 60 min | TP : écrire une série de tests pour l'agent | Écrire des tests (cas normal + tentatives de piégeage par texte) pour l'agent | Agent du fil rouge (état fin S3), squelettes de tests, corrigé |
| S5.1 | 35 min | Gérer une IA en prod, différent du logiciel classique | Comprendre : versionner ses prompts, évaluer en continu, surveiller en prod, des choses qu'un cycle de dev classique ne prévoit pas | Support écrit, exemple de dépôt de prompts versionnés, modèle d'alertes |
| S5.2 | 45 min | Mise en prod et intégration continue adaptées | Adapter sa pipeline de tests automatiques à des résultats jamais parfaitement identiques, bien gérer les données ; déployer une application Laravel avec son worker de file d'attente | Support écrit, exemple de pipeline CI (GitHub Actions) en deux étapes, docker-compose de déploiement |
| S5.3 | 1 h 40 | Cas pratique final et conclusion | Rédiger la fiche d'architecture du fil rouge (choix, tests, sécurité, coût, chaque choix justifié), la confronter au corrigé vidéo, passer le test final, puis ouvrir sur la suite | Modèle de fiche, vidéo de correction, test final (QCM), vidéo de conclusion |

# Périmètre : notions centrales et approfondissements

Pour tenir en 15 h avec du temps de manipulation, chaque notion est classée.
Une notion **centrale** est expliquée, manipulée dans un TP et évaluée. Une
notion en **approfondissement** est présentée en quelques minutes, illustrée
dans les supports (encart « pour aller plus loin ») mais ni manipulée ni
évaluée. Les blocs concernés sont marqués « approfondissement » dans les
tableaux ci-dessous.

Ce classement libère du temps : 40 minutes sont reprises sur les blocs
théoriques (S2.2, S4.3, S5.1) et rendues aux manipulations (S2.4, S4.4 et la
rédaction de la fiche en S5.3). Le total reste à 15 h, chaque séance à 3 h.

| Séance | Notions centrales | Approfondissements |
|--------|-------------------------------|-----------------------|
| 1 | Couches et séparation des responsabilités, ports et adaptateurs, les cinq caractéristiques d'un agent IA, IA locale et IA en ligne derrière un même port | CQRS et événements (encart), équivalent Java des exemples |
| 2 | Contrat d'outil, boucle d'agent simple, RAG comme pipeline de données sur pgvector | Machine à états et annulation (saga) pour les tâches longues, streaming de la réponse |
| 3 | Retry avec délai croissant, coupe-circuit, plan de repli à trois niveaux, tracing et coût par requête | Limite de requêtes en parallèle (bulkhead), budget et alertes de coût avancés |
| 4 | Doublure de fournisseur, jeu de tests de référence, injection directe et indirecte, défense en couches | IA-juge et détection de dérive sémantique, LangChain/LangGraph et service Python séparé |
| 5 | Versionner ses prompts et figer le modèle, pipeline CI en deux étapes, fiche d'architecture | Migration de version de modèle, contraintes légales détaillées, IA locale en CI |

# Détails des séquences

Chaque séance suit la même trame : un peu de théorie, un TP en Laravel sans
SDK, puis une comparaison avec le Laravel AI SDK et Spring AI. Les durées sont
indicatives.

## Séance 1 (3 h) : Les bases de l'architecture web, et pourquoi l'IA les bouscule

### S1.1 : Architectures web : les bases (45 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 10 min | Vidéo d'intro : où placer un appel à une IA dans une appli en couches, sans polluer le cœur du métier ? | Poser la question avant d'y répondre : laisser les étudiants proposer des idées | Regarde et se fait une première idée | Vidéo d'intro (sous-titrée) |
| 20 min | Support écrit : les couches, la séparation des responsabilités, l'architecture hexagonale, le pattern CQRS, appliqués au flux contrôleur → service → domaine | Chaque notion est illustrée par un exemple en PHP. CQRS, les événements et l'équivalent Java sont en encart (approfondissement) | Lit le support et essaie les exemples fournis | Support écrit, dépôt d'exemples Laravel |
| 15 min | Démo : le même besoin métier codé en Laravel, puis lecture de la version Spring Boot fournie, pour repérer ce qui vient du framework et ce qui vient du métier | Le cœur du métier doit rester identique d'un framework à l'autre | Compare les deux versions et note les différences | Vidéo de démo, les deux dépôts d'exemple |

### S1.2 : Pourquoi l'IA complique les architectures classiques (45 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Le fait qu'une IA ne répond jamais exactement pareil, met un temps variable à répondre, coûte à chaque appel, et dépend d'un service externe | Relier chaque caractéristique à sa conséquence concrète sur l'architecture | Prend des notes organisées par caractéristique | Support écrit S1.2 |
| 15 min | Étude de cas : un appel à une IA fait en direct dans un contrôleur web, ce qui casse (timeout, worker bloqué, facture imprévisible) | Montrer un vrai cas de timeout, pas juste le décrire | Analyse le cas et repère les points de rupture | Dépôt de l'étude de cas, vidéo courte du timeout réel |
| 15 min | Fiche de réponse : à partir de l'étude de cas, proposer trois parades possibles, puis lire le corrigé commenté qui passe en revue les pistes (traitement en arrière-plan, file d'attente, limite de temps, cache) et leurs limites | Le corrigé ne tranche pas : les solutions seront construites en séance 3 | Rédige sa fiche, la compare au corrigé, note les écarts | Modèle de fiche, corrigé commenté |

### S1.3 : Installer son environnement : IA en ligne ou IA en local (40 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 10 min | Pourquoi une IA en local ? Pas de coût par appel, données qui restent chez soi, TP réutilisables sans connexion, contre une qualité et une vitesse différentes | Présenter le compromis honnêtement, sans dire que l'un est meilleur que l'autre | Écoute et identifie ce dont il a besoin | Support écrit S1.3, tableau comparatif local / en ligne |
| 20 min | Atelier : installer une IA en local (ex. Ollama) et un petit modèle ; configurer en parallèle une clé d'accès à une IA en ligne | Prévoir une solution de secours pour les machines moins puissantes ; possibilité de bosser en binôme | Installe, télécharge un modèle et teste un premier appel | Guide d'installation pas à pas, script de vérification, modèle de secours pour machines faibles |
| 10 min | Démo clé : brancher l'IA locale et celle en ligne au même endroit du code, deux façons différentes, un seul cœur métier | C'est le moment où l'idée de « ports & adapters » devient concrète | Change de fournisseur d'IA en changeant une seule ligne de configuration | Vidéo de démo, dépôt d'exemple avec les deux adaptateurs |

### S1.4 : TP : réorganiser le code (50 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 10 min | Présentation du code de départ : un contrôleur « fourre-tout » qui appelle directement le SDK du fournisseur d'IA | Le code fourni doit être réaliste, pas exagéré | Lit le code et repère les endroits trop liés entre eux | Dépôt de départ Laravel, README |
| 30 min | Réorganisation guidée : sortir le cœur métier, écrire un adaptateur pour le fournisseur d'IA, isoler le métier | Pas de SDK : l'adaptateur est une classe PHP qui appelle l'API HTTP du fournisseur | Réorganise le code et fait passer les tests fournis | Dépôt de départ Laravel et tests |
| 10 min | Grille comparative : ce que l'apprenant a écrit, ce que le Laravel AI SDK impose, ce que Spring AI impose, ce qui est commun | Faire ressortir les principes qui restent vrais peu importe le framework | Remplit la colonne « mon code », puis lit le corrigé qui remplit les autres | Grille vierge, corrigé |

## Séance 2 (3 h) : Un agent IA, ça se construit comme un composant

### S2.1 : Function / tool calling (45 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Le tool calling : un contrat entre l'IA et le code (nom, description, format des paramètres) ; l'IA propose, l'appli exécute | Insister : l'IA n'exécute rien elle-même, elle demande | Prend des notes sur le déroulement d'un appel | Support écrit S2.1, schéma d'un appel d'outil |
| 20 min | Écrire le contrat d'outil soi-même (interface PHP, schéma JSON des paramètres, dispatch), puis comparaison avec la méthode tools() du Laravel AI SDK et les annotations de Spring AI | Mettre les trois versions côte à côte sur le même outil | Écrit son contrat, le teste, repère ce que le SDK ajoute | Squelette du contrat, extraits SDK et Spring AI |
| 10 min | Point sécurité : un outil, c'est une porte ouverte vers le code métier, donner le minimum de droits nécessaire | Annonce la séance 4 sans trop en dire | Liste les outils qu'il n'exposerait pas | Liste d'outils à classer (exercice) |

### S2.2 : Organiser le travail d'un agent (25 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 10 min | La boucle d'un agent, la machine à états, l'enchaînement d'appels et un pattern pour annuler proprement en cas d'échec, pour des tâches en plusieurs étapes | Distinguer ce qui est décidé à l'avance de ce qui est décidé par l'IA. Machine à états et annulation : approfondissement, présentés sans TP | Dessine la machine à états d'un exemple simple | Support écrit S2.2, schéma de la boucle d'agent |
| 10 min | Étude de cas : une tâche en trois étapes où une seule a vraiment besoin de l'IA | Montrer qu'on limite ce qu'on confie à l'IA | Repère où l'IA est utile, et où elle ne l'est pas | Étude de cas écrite, corrigé |
| 5 min | Exposer ça via une API web : requête longue, streaming, ou file d'attente | Relier au problème de lenteur vu en S1.2. Le streaming est un approfondissement | Choisit une méthode et explique pourquoi | Tableau comparatif des trois modes d'exposition |

### S2.3 : Le RAG comme pipeline de données (45 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Le RAG, ce n'est pas une fonctionnalité magique de l'IA, mais un pipeline de données : récupérer, découper, transformer en vecteurs, indexer, rechercher, donner en contexte | Traiter ça avec la même rigueur qu'un pipeline de données classique | Dessine le pipeline en entier | Support écrit S2.3, schéma du pipeline |
| 20 min | Construire l'indexation et la recherche sur pgvector avec Eloquent et une requête SQL de similarité, puis comparaison avec la recherche du Laravel AI SDK et les VectorStore de Spring AI | Montrer que la base vectorielle n'est qu'un adaptateur de plus | Indexe un petit ensemble de documents et fait une recherche | PostgreSQL + pgvector (Docker), jeu de documents, extraits SDK |
| 10 min | Les limites : le RAG n'empêche ni les inventions de l'IA, ni le risque qu'un document piégé la manipule | Semer le doute avant la séance 4 | Trouve une question à laquelle son index répond mal | Jeu de questions pièges sur l'index |

### S2.4 : TP : agent avec outils + recherche (65 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 10 min | Présentation du cas fil rouge, réutilisé jusqu'à la séance 5 | Cas simple, compréhensible sans expertise préalable | Découvre le cas et les critères de réussite | Fiche du fil rouge : cas métier, outils, critères de réussite par séance |
| 50 min | Construire un agent avec un ou deux outils, plus une recherche par similarité sur un ensemble de documents fourni | Sans SDK : le cœur métier ne doit dépendre d'aucun fournisseur d'IA en particulier ; l'IA locale doit rester utilisable | Code, teste à la main, versionne son travail | Dépôt du fil rouge, documents à indexer |
| 5 min | Point d'étape : ce qui marche, ce qui échoue de façon imprévisible | Noter les échecs : ils serviront en S3 et S4 | Note les comportements bizarres observés | Journal des comportements observés (modèle) |

## Séance 3 (3 h) : Rendre son appli fiable et surveillable

### S3.1 : Rendre son appli solide face à l'incertitude (55 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Réessayer un appel qui échoue (avec délai qui augmente), coupe-circuit, limite de requêtes en parallèle, et la question du plan de secours | Réessayer un appel payant coûte deux fois : le rappeler. La limite de requêtes en parallèle est un approfondissement | Prend des notes et estime le coût d'une politique de réessai | Support écrit S3.1, grille d'estimation du coût d'un réessai |
| 20 min | Écrire le retry avec délai croissant et le coupe-circuit avec les files d'attente et le cache de Laravel, puis comparaison avec la bascule automatique de fournisseur du Laravel AI SDK et Resilience4j côté Spring | Le SDK gère nativement le changement de fournisseur : mesurer ce que ça évite d'écrire | Implémente, compare sur la même panne simulée | Panne simulée (script), extraits SDK et Resilience4j |
| 20 min | Construire un plan de repli à trois niveaux : IA en ligne → IA locale → mode sans IA | Le mode sans IA doit rendre un vrai service, pas juste afficher une erreur | Définit ce que fait son appli quand toute IA est indisponible | Squelette du plan de repli, modèle de « mode sans IA » |

### S3.2 : Surveiller ce que fait l'agent (50 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Le suivi (« tracing ») appliqué à une chaîne d'appels IA (un suivi par appel, par outil, par recherche), logs bien structurés, tout relié par un identifiant de requête | Un suivi doit permettre de comprendre après coup pourquoi l'agent a fait ce choix | Repère ce qu'il faut suivre sur son propre agent | Support écrit S3.2, exemple de trace complète |
| 20 min | Les chiffres qui comptent : vitesse par étape, nombre de tokens utilisés, coût par requête, taux d'échec, taux de recours au plan de secours | Instrumenter soi-même avec les événements Laravel et des logs structurés, puis comparer au suivi natif de Spring AI et aux événements du Laravel AI SDK | Choisit ses indicateurs et explique pourquoi | Extraits SDK et Spring AI |
| 15 min | Le coût comme contrainte d'architecture : budget par requête, plafond, alerte si ça dérape | Un coût qu'on ne mesure pas est un coût qu'on ne maîtrise pas | Estime le coût mensuel de son agent pour un usage donné | Grille de calcul du coût mensuel |

### S3.3 : TP : suivi + plan de secours (1 h 15)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 40 min | Ajouter à l'agent de la séance 2 : suivi complet de la chaîne, logs structurés, chiffres de coût/vitesse, puis le plan de secours à trois niveaux | Vérifier le plan de secours en coupant vraiment le réseau vers l'IA en ligne | Instrumente, provoque la panne, observe ce qui se passe | Agent du fil rouge (état fin S2), script de panne simulée, squelettes |
| 15 min | Analyse des traces produites : où passe le temps, où part l'argent | Comparer ses intuitions de la séance 1 aux vraies mesures | Commente ses propres résultats et trouve une piste d'amélioration | Grille d'analyse des traces |
| 20 min | Correction guidée du TP : vidéo de correction pas à pas (instrumentation, plan de repli, ce qu'on voit quand on coupe le réseau), puis auto-évaluation avec la grille | C'est l'un des deux sujets complexes du cours filmés en vidéo. Montrer les erreurs classiques : logs sans identifiant de requête, plan de repli qui retente à l'infini | Compare son code au corrigé, coche la grille, corrige ce qui manque | Vidéo de correction (sous-titrée), dépôt corrigé, grille d'auto-évaluation |

## Séance 4 (3 h) : Bien tester, et se méfier des attaques

### S4.1 : Tester un système qui ne répond jamais pareil (55 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Pourquoi vérifier une égalité exacte ne suffit plus ; revoir la pyramide de tests pour un composant imprévisible | Séparer ce qui est prévisible (le code) de ce qui ne l'est pas (la réponse de l'IA) | Classe les parties de son agent en prévisibles ou non | Support écrit S4.1 |
| 20 min | Techniques : simuler les réponses de l'IA, créer un jeu de tests de référence, utiliser une IA comme « juge », tester si le sens des réponses dérive, définir une marge de tolérance | Une IA-juge n'est elle-même pas fiable à 100 % : ne pas s'y fier aveuglément. IA-juge et dérive sémantique : approfondissement, non évalués | Crée dix cas de test de référence sur son propre sujet | Modèle de jeu de tests de référence (10 cas) |
| 20 min | Écrire sa propre doublure de fournisseur (fake) avec PHPUnit ou Pest, puis comparaison avec Agent::fake() du Laravel AI SDK et l'Evaluator API de Spring AI | Le simulateur « prêt à l'emploi » du SDK fait ce que l'apprenant vient d'écrire : le montrer | Écrit un premier test avec sa doublure | Squelette de test, extraits SDK et Spring AI |

### S4.2 : Risques & sécurité (50 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Le référentiel OWASP Top 10 pour les applis IA, avec l'injection de prompt (manipulation par texte piégé) en première place depuis deux éditions | La cause : les instructions et les données passent par le même canal | Situe son agent face à chacun des dix risques | Support écrit S4.2, lien vers le référentiel OWASP (édition citée en bibliographie), grille des dix risques |
| 20 min | Injection directe (l'utilisateur écrit l'attaque lui-même) et indirecte (un document indexé la contient) ; fuite de données via le contexte ; outils avec trop de droits | Montrer une vraie injection indirecte sur l'index construit en séance 2 | Écrit un texte piégé et le teste sur son propre agent | Document piégé fourni, agent du fil rouge avec index de S2 |
| 15 min | Se défendre sur plusieurs niveaux à la fois : vérifier les entrées, filtrer les sorties, donner le minimum de droits aux outils, séparer le contenu non fiable, faire valider par un humain les actions sensibles | Aucune mesure seule ne suffit : c'est le cumul qui compte | Choisit deux mesures et les met en place | Liste des parades avec exemples de code |

### S4.3 : Comparer les approches (15 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 10 min | Grille de comparaison : le code construit pendant le cours, le Laravel AI SDK, Spring AI, LangChain/LangGraph ; facilité à changer de fournisseur, suivi natif, facilité à tester, maturité, écosystème | Comparer sur des critères techniques, jamais sur la mode | Remplit la grille pour son propre projet | Grille vierge, corrigé |
| 5 min | Cas de décision : quand une seule stack suffit, et quand un service Python séparé se justifie vraiment | Un service séparé a un vrai coût de fonctionnement : le nommer. Approfondissement | Défend un choix et répond aux objections | Cas de décision écrit, corrigé argumenté |

### S4.4 : TP : écrire une série de tests (60 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 45 min | Écrire une série de tests : cas normal avec réponses simulées, cas dégradé, et au moins deux tentatives d'injection (directe et indirecte) | Un test d'injection qui passe du premier coup est probablement mal écrit | Écrit les tests, les fait échouer, puis corrige l'agent | Agent du fil rouge (état fin S3), squelettes de tests, textes piégés |
| 15 min | Intégrer au dépôt et lancer toute la suite | Mesurer le temps d'exécution : ça conditionne la CI de la séance 5 | Commit, exécute, note la durée | Commande de lancement de la suite, gabarit de relevé de durée |

## Séance 5 (3 h) : Mettre en prod et présenter son travail

### S5.1 : Gérer une IA en prod (35 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Ce que le cycle classique ne couvre pas : le prompt est aussi un fichier à versionner, l'évaluation est continue, la qualité peut baisser sans qu'on touche au code | Une mise à jour du modèle côté fournisseur est un déploiement qu'on ne contrôle pas | Repère ce qu'il faut versionner dans son projet | Support écrit S5.1 |
| 10 min | Versionner ses prompts, gérer les versions de modèle, figer une version, prévoir une migration en cas de changement | Figer la version du modèle n'est pas optionnel en prod. La migration de version est un approfondissement | Met en place un versionnage de ses prompts | Exemple de dépôt de prompts versionnés |
| 10 min | Surveillance en prod : baisse de qualité, dérive du coût, retours des utilisateurs | Distinguer un incident ponctuel d'une dérive lente | Définit trois alertes et leurs seuils | Modèle de définition d'alertes |

### S5.2 : Mise en prod & CI/CD adaptées (45 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 20 min | Adapter sa pipeline : quels tests bloquent la mise en prod, lesquels tournent en arrière-plan ? Gérer le coût et la lenteur des tests qui appellent une vraie IA | Faire tourner l'évaluation coûteuse à côté du chemin principal, mais la faire quand même tourner | Conçoit sa pipeline en deux étapes | Exemple de pipeline GitHub Actions en deux étapes |
| 15 min | L'IA locale comme outil de CI : évaluer sans clé d'accès ni facture, au prix d'une fidélité un peu moindre | Ça rejoint la séance 1 : l'architecture par adaptateurs paie ici | Évalue si cette option est utile pour son projet | Exemple de job CI avec Ollama |
| 10 min | Gestion des données, traçabilité des prompts et réponses, contraintes légales ; déploiement Laravel avec worker de file d'attente et migration pgvector | Ce qui part dans le contexte de l'IA quitte l'entreprise : le rappeler une dernière fois | Note quelles données passent par son agent | Check-list données et traçabilité, docker-compose de déploiement |

### S5.3 : Cas pratique final et conclusion (1 h 40)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 55 min | Cas pratique final : rédiger la fiche d'architecture du fil rouge (2 pages max) : architecture choisie, stratégie de test, mesures de sécurité, coût estimé, et pour chaque point pourquoi ce choix plutôt qu'un autre | L'apprenant doit défendre des choix, pas décrire ce qu'il a codé. La fiche est déposée sur Moodle et évaluée avec une grille fournie | Rédige sa fiche à partir de son agent et de ses mesures des séances 3 et 4, la dépose | Modèle de fiche, grille d'évaluation, agent du fil rouge |
| 15 min | Vidéo de correction du cas pratique : une fiche de référence commentée, avec les erreurs fréquentes et ce qui distingue une justification d'une description | Mettre en regard l'architecture construite et celle du Laravel AI SDK : mêmes principes, mêmes pièces | Regarde, s'auto-évalue avec la grille, note ce qu'il aurait changé | Vidéo de correction (sous-titrée), fiche de référence |
| 20 min | Test final : QCM d'une quarantaine de questions couvrant les cinq séances, corrigé automatique avec explication par question | Vérifier les acquis, pas la mémoire : chaque question part d'une situation concrète | Passe le test, lit les explications de ses erreurs | Test final sur Moodle, corrigé |
| 10 min | Vidéo de conclusion « pour aller plus loin » : ce qui vient de l'architecture, ce qui vient du framework, ce qui vient du modèle ; les sujets non couverts (évaluation continue, agents multiples, choix de modèle) et par où continuer | Conclure sur l'idée principale : l'agent IA s'isole comme une dépendance technique, mais son comportement oblige à adapter tests, observabilité et sécurité | Regarde, note ce qu'il retient et ce qu'il ferait différemment | Vidéo de conclusion (sous-titrée), bibliographie |
