---
title: "Concevoir une application web maintenable intégrant un agent IA : architecture, tests, sécurité et mise en production"
subtitle: "Document de scénarisation, version 2 (jalon du 02/12/2026)"
author: "Quentin Bauduin, Timothé Geoffroy, Kaan Topkaya, Erwin Gossin"
date: "25 novembre 2026"
---

<!--
Version 2 : applique le cadrage du 25/11/2026 (FYC-96). La version finale du
09/09/2026 reste dans l'historique git. Changements : installation déplacée
dans le chapitre 00, séances 1 à 5 réorganisées, 20 séquences pour 15 h pile,
8 objectifs observables, budget vidéo de 8 min au plus par vidéo.
-->

# Titre du module

**Concevoir une application web maintenable intégrant un agent IA : architecture, tests, sécurité et mise en production.**

Parcours technique : Laravel (PHP). Le Laravel AI SDK et Spring AI (Java) servent de points de comparaison dans les supports.

# Problématique

> **Comment intégrer un agent IA dans une application web sans dégrader sa maintenabilité, sa testabilité, sa sécurité et sa maîtrise en production ?**

La démarche qui y conduit (opinion admise, constats, questions soulevées,
délimitation du cours) est développée dans le document de présentation de la
problématique, remis avec cette scénarisation.

# Synoptique de l'intervention

Ce cours se déroule en un chapitre d'ouverture de 45 minutes et 5 séances
(135 minutes pour la première, 3 heures pour chacune des quatre autres), soit
15 heures. Le but : apprendre à construire une appli web qui utilise une IA,
sans que ça devienne un bazar impossible à maintenir.

On ne va pas traiter l'IA comme une fonctionnalité magique qu'on branche et qui
marche toute seule. Mais on ne va pas non plus la traiter comme un composant
comme un autre. Un agent IA se branche comme une dépendance technique, derrière
une interface, au même titre qu'une base de données ou un service de paiement.
Son comportement, lui, n'a rien d'ordinaire : rien ne garantit qu'il réponde
deux fois pareil, il met un temps variable à répondre, chaque appel coûte de
l'argent, il dépend d'un fournisseur que vous ne contrôlez pas, et il ouvre une
surface d'attaque nouvelle. Ce sont ces cinq caractéristiques qui structurent le
cours : chacune oblige à adapter l'architecture, les tests, l'observabilité, la
sécurité ou la mise en production.

Le cours suit un seul parcours technique, Laravel (PHP), et un seul projet
fil rouge, NoteFlow, que vous faites évoluer de séance en séance jusqu'à sa mise
en ligne. Chaque séance mélange trois choses : un peu de théorie sur
l'architecture, un TP, et une comparaison.

Un choix pédagogique structure les TP : **vous n'utilisez pas de SDK d'IA**.
Vous écrivez vous-même l'adaptateur vers le fournisseur, le contrat d'outil, la
boucle d'agent, le pipeline de récupération, le retry et le plan de secours, les
doublures de test. À la fin de chaque étape, la comparaison montre côte à côte
ce que vous venez de construire, comment le Laravel AI SDK le fait, et comment
Spring AI le fait côté Java. L'objectif est d'arriver, à la fin du cours, à une
architecture qui ressemble à celle d'un SDK, en ayant compris pourquoi chaque
pièce existe. La comparaison est une méthode d'étude, pas la finalité : elle
sert à séparer ce qui vient du framework de ce qui relève de principes
d'architecture valables quel que soit le langage.

Avant la première séance, le chapitre 00 vous fait installer une IA qui tourne
directement sur votre ordinateur, en plus de celle disponible sur internet.
Comme ça, si vous voulez, vous pouvez faire tous les TP sans payer et sans clé
d'accès. C'est aussi un bon exemple concret : le code doit pouvoir marcher avec
l'IA en ligne ou l'IA locale sans qu'on ait à le réécrire, on change juste
« l'adaptateur » branché derrière. Une ligne de configuration change
l'adaptateur, pas le contrat : Ollama n'accepte pas tous les paramètres
d'OpenAI et limite le contexte à 4096 tokens par défaut, ce que le TP de la
séance 1 fait constater.

# Objectifs de la formation

À la fin du module, vous serez capables de :

- **O1.** Isoler le fournisseur d'IA derrière un port et y brancher par
  configuration trois adaptateurs : en ligne, local et doublure de test.
- **O2.** Concevoir la boucle d'un agent (contrat d'outils, conditions d'arrêt,
  budget, validation humaine) et justifier quand un workflow suffit.
- **O3.** Construire un pipeline de récupération (lexical et vectoriel sur
  pgvector) et en mesurer la qualité (recall@k).
- **O4.** Rendre résilient l'appel à l'IA : délais enchaînés, idempotence, retry
  borné, coupe-circuit, repli à trois niveaux.
- **O5.** Instrumenter l'agent : une trace par requête, le coût par requête, le
  modèle et la version de prompt dans chaque trace.
- **O6.** Tester l'agent avec une doublure, des assertions de propriétés et un
  jeu de référence, en exprimant le résultat en taux sur N essais (pass^k).
- **O7.** Analyser les risques de l'agent (OWASP LLM 2026, règle de deux) et
  mettre en place des défenses qui bornent l'impact, testées de façon
  déterministe.
- **O8.** Mettre en production : CI à deux étages, déploiement du worker,
  alertes de dérive, obligations minimales (article 50 de l'AI Act, journaux).

Le choix technique (framework, outil, fournisseur) se justifie à chaque étape :
c'est le critère transversal de la fiche d'architecture finale (chaque rubrique
donne le choix, l'alternative écartée et la raison).

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
- Une clé d'accès chez un fournisseur d'IA en ligne (lequel sera précisé dans
  le guide d'installation du chapitre 00). Elle est facultative.
- Ou en alternative gratuite : une IA installée en local (par exemple avec
  Ollama), pour faire tous les TP sans payer. Machine recommandée : 16 Go de
  RAM, valeur à confirmer par une mesure sur le modèle retenu pour le cours.
- Un endroit pour stocker des « embeddings » (des bouts de texte transformés en
  listes de nombres, pour pouvoir chercher par ressemblance) : pgvector, dans
  une image Docker dont la version est épinglée, pour les TP sur la récupération
  d'information.

# Plan du cours

Durée totale : **15 h**, chapitre 00 compris (45 + 135 + 4 × 180 minutes).

| N° | Durée | Titre | Ce qu'on apprend | Équipement & matériel |
|-----|------|-----------------|----------------------------------------|--------------|
| 00.1 | 5 min | Présentation, accroche, pré-requis | Ce que le cours promet, qui l'a construit, ce qu'il faut savoir avant | Vidéo unique de présentation, texte d'accroche, page d'accueil |
| 00.2 | 10 min | Test de positionnement | Mesurer ses pré-requis, et rencontrer 3 à 5 questions de contenu qu'il est normal de rater | Test corrigé, option « je ne sais pas » |
| 00.3 | 30 min | Installer et vérifier son environnement | Installer Ollama et un modèle, pgvector épinglé, la clé en ligne facultative ; régler la fenêtre de contexte d'Ollama ; vérifier que tout est en place | Guide d'installation, docker-compose pgvector, script de vérification, modèle de secours |
| S1.1 | 40 min | Architectures web : les bases | Couches, dépendances vers l'intérieur, ports et adaptateurs, appliqués au flux contrôleur → service → domaine | Vidéo d'intro, support écrit, dépôts d'exemple Laravel et Spring Boot |
| S1.2 | 40 min | Pourquoi l'IA complique les architectures classiques | Les cinq caractéristiques d'un agent IA (et les limites de débit) et leurs points de rupture | Support écrit, étude de cas (dépôt + vidéo du timeout), fiche de réponse, corrigé |
| S1.3 | 55 min | TP : un port, trois adaptateurs | Isoler le fournisseur : adaptateur HTTP en ligne, adaptateur Ollama, doublure de test ; prompt versionné, modèle épinglé en configuration | Vidéo de démo, dépôt de départ Laravel avec tests, branche corrigée, grille comparative |
| S2.1 | 40 min | Le contrat d'outil | Sortie structurée et schéma JSON, contrat d'outil, « le modèle propose, le code décide », moindre privilège | Support écrit, squelette de contrat d'outil et adaptateur de tool calling, liste d'outils à classer |
| S2.2 | 30 min | Workflow ou agent ? La boucle et ses arrêts | Quand un workflow suffit, boucle d'agent, conditions d'arrêt, budget, validation humaine | Vidéo d'explication, support écrit, étude de cas en trois étapes |
| S2.3 | 45 min | Récupérer l'information, et le mesurer | Recherche plein texte puis vectorielle sur pgvector, filtrage par droits, mesure par recall@5 | Vidéo, support écrit, jeu de 26 notes, squelette d'indexation, 5 questions de référence |
| S2.4 | 65 min | TP : l'agent NoteFlow | Agent unique avec deux outils et une recherche, plafond d'étapes, confirmation, citation de la source ; 5 premiers cas de référence | Fiche du fil rouge, squelette fourni, dépôt NoteFlow, branche « état fin S2 » |
| S3.1 | 25 min | Délais, files et idempotence | Exposer une tâche IA (synchrone, file, streaming), délais enchaînés, clé d'idempotence | Support écrit, agent en job |
| S3.2 | 40 min | Retry, coupe-circuit, repli | Retry avec jitter et `Retry-After`, coupe-circuit à état partagé, repli à trois niveaux | Support écrit, doublure qui renvoie 429 et 503, squelettes, extraits SDK et Resilience4j |
| S3.3 | 35 min | Observer l'agent | Une trace par requête, modèle et prompt servis, coût par requête, alertes | Support écrit, exemple de trace, grille de coût mensuel |
| S3.4 | 80 min | TP : instrumentation et panne simulée | Instrumenter, couper le réseau, lire les traces, tirer 2 cas de référence | Agent « état fin S2 », fiche pas à pas, correction en 3 vidéos |
| S4.1 | 45 min | Tester un système non déterministe | Température 0 n'est pas déterministe, assertions de propriétés, jeu de référence, pass^k | Support écrit, squelette de doublure PHPUnit/Pest, modèle de jeu de référence |
| S4.2 | 55 min | Risques et sécurité d'un agent | Injection directe et indirecte, exfiltration par image Markdown, règle de deux appliquée à NoteFlow, OWASP LLM 2026 | Vidéo d'explication, support écrit, référentiel OWASP, document piégé |
| S4.3 | 80 min | TP : la suite de tests de l'agent | Tests déterministes des garde-fous, suite contre un vrai modèle sur k essais | Agent « état fin S3 », fiche pas à pas, squelettes, textes piégés, vidéo |
| S5.1 | 25 min | Exploiter une IA en production | Épinglage et migration de modèle, version de prompt, dérive, transparence (AI Act art. 50) | Support écrit, dépôt de prompts versionnés, modèle d'alertes |
| S5.2 | 40 min | CI et déploiement | CI à deux étages écrite et lancée, déploiement du worker | Support écrit, workflow GitHub Actions, check-list de déploiement |
| S5.3 | 115 min | Cas pratique, test final, conclusion | Fiche d'architecture en 6 rubriques, test final, ouverture | Modèle de fiche, grille, 2 vidéos de correction, test final de 40 QCM, vidéo de conclusion |

# Périmètre : notions centrales et approfondissements

Pour tenir en 15 h avec du temps de manipulation, chaque notion est classée.
Une notion **centrale** est expliquée, manipulée dans un TP et évaluée. Une
notion en **approfondissement** est présentée en quelques minutes, illustrée
dans les supports (encart « pour aller plus loin ») mais ni manipulée ni
évaluée. Un encart n'a pas de temps apprenant dédié, sauf mention contraire.

| Séance | Notions centrales | Approfondissements |
|--------|-------------------------------|-----------------------|
| 0 | Installer et vérifier l'environnement, épingler les versions | Modèle de secours pour machines faibles |
| 1 | Couches et séparation des responsabilités, ports et adaptateurs, les cinq caractéristiques d'un agent IA, IA locale, IA en ligne et doublure derrière un même port | CQRS et événements (encart), équivalent Java des exemples |
| 2 | Contrat d'outil, boucle d'agent avec arrêts et budget, validation humaine, recherche plein texte et vectorielle sur pgvector, recall@5 | MCP, machine à états et annulation (saga), streaming de la réponse, fusion de rangs (RRF) et index approximatif (HNSW) |
| 3 | Délais enchaînés, idempotence, retry avec jitter, coupe-circuit, repli à trois niveaux, trace et coût par requête | Limite de requêtes en parallèle (bulkhead), budget et alertes de coût avancés |
| 4 | Doublure de fournisseur, jeu de référence, pass^k, injection directe et indirecte, règle de deux, défenses qui bornent l'impact | IA-juge et détection de dérive sémantique, LangChain/LangGraph et service Python séparé |
| 5 | Épinglage du modèle, versionnement des prompts, CI à deux étages, transparence (AI Act article 50), fiche d'architecture | Migration de version de modèle, RGPD détaillé et calendrier complet de l'AI Act, IA locale en CI (encart de 3 min) |

# Détails des séquences

Chaque séance suit la même trame : un peu de théorie, un TP en Laravel sans
SDK, puis une comparaison avec le Laravel AI SDK et Spring AI. Les durées sont
indicatives.

## Chapitre 00 (45 min) : Présentation du cours

### 00.1 : Présentation, accroche, pré-requis (5 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 3 min | Vidéo unique : le cours, l'équipe, les pré-requis | Donner envie : une accroche, pas un « Bonjour » | Regarde | Vidéo de présentation (sous-titrée) |
| 2 min | Texte d'accroche et page d'accueil : objectifs, plan, mode d'emploi | Dire où sont les TP, le fil rouge, les corrigés | Lit | Page d'accueil, texte d'accroche |

### 00.2 : Test de positionnement (10 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 10 min | Dix questions de pré-requis, plus 3 à 5 questions de contenu annoncées comme « normales à rater », avec l'option « je ne sais pas » | Le test n'est pas noté : il oriente vers les ressources de mise à niveau. Les questions de contenu ouvrent la curiosité (effet de prétest) | Répond, lit le corrigé, repère ses lacunes | Test de positionnement corrigé |

### 00.3 : Installer et vérifier son environnement (30 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 20 min | Installer PHP 8.3+, Composer, Docker avec pgvector (image dont la version est épinglée), Ollama et un petit modèle ; configurer en parallèle une clé d'accès à une IA en ligne si on en veut une | La fenêtre de contexte d'Ollama est de 4096 tokens par défaut : la régler (`OLLAMA_CONTEXT_LENGTH`). Prévoir un modèle de secours pour les machines moins puissantes | Installe, télécharge un modèle, lance un premier appel | Guide d'installation pas à pas, docker-compose pgvector |
| 10 min | Vérifier que tout est en place avec un script, un message clair par point | Un script vert est la condition d'entrée en séance 1 | Lance le script et corrige ce qui est rouge | Script de vérification, modèle de secours pour machines faibles |

## Séance 1 (135 min) : Les bases de l'architecture web, et pourquoi l'IA les bouscule

### S1.1 : Architectures web : les bases (40 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 6 min | Vidéo d'intro : où placer un appel à une IA dans une appli en couches, sans polluer le cœur du métier ? | Poser la question avant d'y répondre : laisser les étudiants proposer des idées | Regarde et se fait une première idée | Vidéo d'intro (sous-titrée) |
| 24 min | Support écrit : les couches, la séparation des responsabilités, les dépendances qui vont vers l'intérieur, les ports et adaptateurs, appliqués au flux contrôleur → service → domaine | Chaque notion est illustrée par un exemple en PHP. CQRS, événements et équivalent Java sont en encart (approfondissement) | Lit le support et essaie les exemples fournis | Support écrit, dépôt d'exemples Laravel |
| 10 min | Lecture guidée du même besoin métier en Laravel puis en Spring Boot (5 min de vidéo, 5 min de lecture), pour repérer ce qui vient du framework et ce qui vient du métier | Le cœur du métier doit rester identique d'un framework à l'autre. Pas de TP Spring | Compare les deux versions et note les différences | Vidéo de lecture guidée, les deux dépôts d'exemple |

### S1.2 : Pourquoi l'IA complique les architectures classiques (40 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Étude de cas : un appel à une IA fait en direct dans un contrôleur web, ce qui casse (timeout, worker bloqué, facture imprévisible) | Montrer un vrai timeout et chercher où il coupe réellement (client HTTP, serveur web, worker), pas seulement dans PHP | Analyse le cas et repère les points de rupture | Dépôt de l'étude de cas, vidéo de 3 min du timeout réel |
| 15 min | Les cinq caractéristiques : rien ne garantit une réponse identique, un temps variable, un coût à chaque appel, un fournisseur externe (avec ses limites de débit), une surface d'attaque nouvelle | Partir des incidents de l'étude de cas (trois caractéristiques sur cinq y apparaissent), puis relier chaque caractéristique à sa conséquence concrète sur l'architecture | Prend des notes organisées par caractéristique et classe trois situations dans un mini-exercice | Support écrit S1.2 |
| 10 min | Fiche de réponse : proposer trois parades possibles, puis lire le corrigé commenté qui passe en revue les pistes (traitement en arrière-plan, file d'attente, limite de temps, cache) et leurs limites | Le corrigé ne tranche pas : les solutions sont construites en séance 3 | Rédige sa fiche, la compare au corrigé, note les écarts | Modèle de fiche, corrigé commenté |

### S1.3 : TP : un port, trois adaptateurs (55 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 5 min | Vidéo « une ligne de config, deux fournisseurs » : brancher l'IA locale et celle en ligne au même endroit du code | C'est le moment où l'idée de « ports et adaptateurs » devient concrète. Une ligne de configuration change l'adaptateur, pas le contrat : Ollama n'accepte pas tous les paramètres d'OpenAI | Regarde | Vidéo de démo (sous-titrée) |
| 45 min | Réorganisation guidée pas à pas d'un contrôleur « fourre-tout » qui appelle directement l'API HTTP du fournisseur : sortir le cœur métier, écrire un adaptateur HTTP en ligne, un adaptateur Ollama et une doublure de test ; mettre le prompt dans un fichier versionné et épingler le modèle en configuration | Pas de SDK : l'adaptateur est une classe PHP qui appelle l'API HTTP du fournisseur. La doublure vient dès ce TP : elle sert à tous les tests suivants | Réorganise le code et fait passer les tests fournis avec la doublure | Dépôt de départ Laravel, tests fournis, fiche pas à pas, branche corrigée |
| 5 min | Grille comparative : ce que l'apprenant a écrit, ce que le Laravel AI SDK impose, ce que Spring AI impose, ce qui est commun | Faire ressortir les principes qui restent vrais peu importe le framework | Remplit la colonne « mon code », puis lit le corrigé | Grille vierge, corrigé |

## Séance 2 (3 h) : Un agent IA, ça se construit comme un composant

### S2.1 : Le contrat d'outil (40 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 12 min | Sortie structurée et schéma JSON, puis tool calling : un contrat entre l'IA et le code (nom, description, schéma) ; le modèle propose, le code décide ; les formats d'appel diffèrent d'un fournisseur à l'autre | Insister : l'IA n'exécute rien elle-même, elle demande. Moindre privilège et validation par du code | Prend des notes sur le déroulement d'un appel | Support écrit S2.1, schéma d'un appel d'outil |
| 3 min | Encart MCP : un standard pour transporter des outils d'une application à l'autre | MCP ne remplace pas votre contrat d'outil, il le transporte. Approfondissement, non évalué | Lit | Support écrit S2.1 |
| 15 min | Un outil entièrement écrit (interface PHP, schéma JSON, dispatch), un second à trous à compléter ; comparaison avec la méthode `tools()` du Laravel AI SDK et les annotations de Spring AI (5 min au plus) | Mettre les trois versions côte à côte sur le même outil | Complète le second outil, le teste, repère ce que le SDK ajoute | Squelette du contrat et adaptateur de tool calling, extraits SDK et Spring AI |
| 10 min | Point sécurité : un outil, c'est une porte ouverte vers le code métier ; donner le minimum de droits nécessaire | Annonce la séance 4 sans trop en dire | Classe une liste d'outils et justifie ceux qu'il n'exposerait pas | Liste d'outils à classer (exercice), corrigé |

### S2.2 : Workflow ou agent ? La boucle et ses arrêts (30 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 6 min | Vidéo d'explication n° 1 : la boucle d'un agent dessinée pas à pas | Premier des deux sujets complexes filmés. Montrer que la boucle s'arrête sur une raison, pas sur un hasard | Regarde et suit le schéma | Vidéo d'explication (sous-titrée) |
| 12 min | Workflow contre agent (cinq patterns) ; la boucle `while` sur la raison d'arrêt ; plafond d'étapes et budget de tokens ; une erreur d'outil renvoyée au modèle ; l'état « en attente d'approbation » ; vocabulaire : harness, ingénierie du contexte | Distinguer ce qui est décidé à l'avance de ce qui est décidé par l'IA. Machine à états, saga et streaming : encart | Dessine la boucle de son futur agent avec ses arrêts | Support écrit S2.2, schéma de la boucle d'agent |
| 12 min | Étude de cas : une tâche en trois étapes où une seule a vraiment besoin de l'IA | Montrer qu'on limite ce qu'on confie à l'IA | Repère où l'IA est utile, et où un workflow suffit | Étude de cas écrite, corrigé |

### S2.3 : Récupérer l'information, et le mesurer (45 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Pourquoi récupérer (et quand ne pas le faire) ; la recherche plein texte de PostgreSQL ; les embeddings, avec le même modèle à l'indexation et à la recherche ; pgvector en recherche exacte (`<=>`, `ORDER BY … LIMIT`) ; le filtrage par droits dans le `WHERE` ; les limites (inventions, document piégé) | Le RAG est un pipeline de données traité avec la même rigueur. Lexical d'abord : c'est aussi le repli de la séance 3. Index approximatif et fusion de rangs : encart | Dessine le pipeline en entier | Support écrit S2.3, schéma du pipeline |
| 6 min | Vidéo : pgvector et la mesure du recall | La mesure vient avant l'optimisation | Regarde | Vidéo (sous-titrée) |
| 24 min | Indexer les 26 notes du fil rouge, comparer la recherche plein texte et la recherche vectorielle sur 5 questions de référence, calculer le recall@5 ; comparaison avec `whereVectorSimilarTo` (Laravel 13), l'outil `SimilaritySearch` du Laravel AI SDK et le `VectorStore` de Spring AI | Sans SDK : l'apprenant écrit la requête SQL lui-même ; l'aide du framework n'apparaît que dans la comparaison | Indexe, interroge, calcule son recall@5 | PostgreSQL + pgvector (Docker), jeu de 26 notes, squelette d'indexation, 5 questions de référence, extraits |

### S2.4 : TP : l'agent NoteFlow (65 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 5 min | Présentation du cas fil rouge NoteFlow, réutilisé jusqu'à la séance 5 | Cas simple, compréhensible sans expertise préalable | Découvre le cas, les outils et les critères de réussite | Fiche du fil rouge |
| 50 min | Construire un agent unique : l'outil `chercher_notes` (qui ne lit que les notes autorisées), l'outil `creer_tache` avec confirmation montrant l'action exacte, plafond d'étapes, citation de la note source ou « je ne sais pas » | Le squelette fourni contient l'adaptateur de tool calling déjà normalisé ; l'apprenant écrit les outils et la boucle. Le cœur métier ne dépend d'aucun fournisseur ; l'IA locale reste utilisable | Code, teste à la main, versionne son travail | Squelette fourni, dépôt du fil rouge, notes à indexer |
| 10 min | Point d'étape : transformer le journal des comportements observés en 5 premiers cas de référence | Les échecs notés servent en séances 3 et 4 | Écrit 5 cas de référence (entrée, comportement attendu) | Modèle de cas de référence, branche corrigée « état fin S2 » |

## Séance 3 (3 h) : Rendre son appli fiable et surveillable

### S3.1 : Délais, files et idempotence (25 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 10 min | Exposer une tâche IA : réponse synchrone, file d'attente ou streaming ; les délais s'emboîtent (`timeout HTTP < timeout du job < retry_after`) ; la clé d'idempotence, et pourquoi `creer_tache` doit l'être | Un retry sans idempotence rejoue une écriture. Relier au problème de lenteur de S1.2 | Prend des notes et choisit un mode d'exposition | Support écrit S3.1, tableau des trois modes d'exposition |
| 15 min | Passer l'agent en job de file, rejouer un même appel, constater qu'il n'y a pas de doublon | Le rejeu se vérifie en base, pas à l'œil | Implémente la clé d'idempotence et rejoue | Agent du fil rouge, squelette de job |

### S3.2 : Retry, coupe-circuit, repli (40 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 12 min | Réessayer seulement les erreurs qui peuvent réussir, avec un délai croissant et aléatoire (jitter), en respectant `Retry-After`, et seulement si l'opération est idempotente ; un seul niveau de retry ; coupe-circuit à état partagé (le cache) ; repli à trois niveaux : IA en ligne, IA locale, mode sans IA (la recherche plein texte de S2.3) | Un retry après timeout peut payer deux fois le même appel : le budget de retries fait partie du coût. Un 429 dû au plafond de dépense ne passe jamais. Le mode sans IA rend un vrai service. Limite de requêtes en parallèle : encart | Estime le coût d'une politique de retry | Support écrit S3.2, grille d'estimation du coût d'un retry |
| 23 min | Implémenter retry, coupe-circuit et repli avec la file et le cache de Laravel, contre la doublure qui renvoie 429 et 503 | Le repli est construit une seule fois | Implémente et rejoue la panne simulée | Doublure de panne (script), squelettes retry, coupe-circuit, repli |
| 5 min | Comparaison : le Laravel AI SDK bascule de fournisseur sur certaines erreurs, mais ne fait ni backoff, ni jitter, ni coupe-circuit ; Spring AI réessaie déjà par défaut (sans jitter), Resilience4j apporte le coupe-circuit | Mesurer ce que le SDK évite d'écrire et ce qu'il laisse à votre charge ; attention au double niveau de retry | Lit et note ce qui reste à sa charge | Extraits SDK et Resilience4j |

### S3.3 : Observer l'agent (35 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Une trace par requête, un span par appel au modèle, par outil et par recherche ; le modèle demandé et le modèle servi ; la version de prompt ; les tokens par catégorie et le coût ; le contenu des prompts en opt-in et masqué | Une trace doit permettre de comprendre après coup pourquoi l'agent a fait ce choix. Ne pas journaliser les prompts complets par défaut | Repère ce qu'il faut tracer sur son propre agent | Support écrit S3.3, exemple de trace complète |
| 10 min | Choisir ses indicateurs : vitesse par étape, tokens, coût par requête, taux d'échec, taux de recours au repli ; budget et alertes | Instrumenter soi-même avec les événements Laravel, puis comparer au suivi natif de Spring AI et aux événements du Laravel AI SDK | Choisit ses indicateurs et explique pourquoi | Extraits SDK et Spring AI |
| 10 min | Exercice : diagnostic sur traces (« pourquoi cette requête a coûté 0,40 € ? ») et grille de coût mensuel | Un coût qu'on ne mesure pas est un coût qu'on ne maîtrise pas | Diagnostique des traces et estime le coût mensuel de son agent | Traces à lire, grille de calcul du coût mensuel |

### S3.4 : TP : instrumentation et panne simulée (80 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 45 min | Ajouter à l'agent de la séance 2 : trace complète, coût, puis retry, coupe-circuit, repli et clé d'idempotence ; couper vraiment le réseau vers l'IA en ligne et observer la bascule | Vérifier le repli en coupant le réseau, pas en le supposant | Instrumente, provoque la panne, observe | Agent du fil rouge (état fin S2), script de panne simulée, fiche pas à pas |
| 15 min | Analyse des traces produites : où passe le temps, où part l'argent ; ajouter 2 cas de référence tirés des traces | Comparer ses intuitions de la séance 1 aux vraies mesures | Commente ses résultats, ajoute 2 cas | Grille d'analyse des traces |
| 20 min | Correction guidée en 3 vidéos de 5 à 7 min (instrumentation, panne simulée, cas de référence), puis auto-évaluation avec la grille | Montrer les erreurs classiques : logs sans identifiant de requête, repli qui retente à l'infini | Compare son code au corrigé, coche la grille, corrige ce qui manque | 3 vidéos de correction (sous-titrées), dépôt corrigé « état fin S3 », grille d'auto-évaluation |

## Séance 4 (3 h) : Bien tester, et se méfier des attaques

### S4.1 : Tester un système non déterministe (45 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | Température 0 ne rend pas une réponse reproductible ; la pyramide de tests (le code autour de l'IA se teste à 100 % avec la doublure) ; assertions de propriétés ; jeu de référence issu des traces ; pass@k et pass^k ; capacité contre régression ; IA-juge et dérive en encart | Rien ne garantit une réponse identique : séparer ce qui est prévisible (le code) de ce qui ne l'est pas (la réponse). Une IA-juge n'est pas fiable à 100 % : non évaluée | Classe les parties de son agent en prévisibles ou non | Support écrit S4.1 |
| 30 min | Consolider les cas de référence (10 au total), écrire 3 assertions de propriétés et un premier test avec sa doublure ; comparaison avec la méthode `fake()` des agents du Laravel AI SDK (`MonAgent::fake()`, `assertPrompted`, `preventStrayPrompts()`) et, côté Spring AI, un mock de `ChatModel` | L'Evaluator API de Spring AI fait juger une réponse par un autre modèle : c'est de l'IA-juge, pas une doublure | Écrit ses assertions et lance sa suite | Squelette de doublure PHPUnit/Pest, modèle de jeu de référence (10 cas), extraits SDK et Spring AI |

### S4.2 : Risques et sécurité d'un agent (55 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | La cause racine : instructions et données passent par le même canal ; injection directe et indirecte, et la différence avec le jailbreak ; exfiltration par une image Markdown ; trifecta (données privées, contenu non fiable, communication externe) puis règle de deux ; le Top 10 OWASP des applications LLM, édition 2026, où l'injection de prompt reste première comme dans toutes les éditions, complété par le Top 10 OWASP des applications agentiques | La grille des dix risques suit l'édition 2026. Aucune défense ne règle l'injection de façon fiable | Situe son agent face à chacun des dix risques | Support écrit S4.2, référentiel OWASP (lien, édition citée en bibliographie), grille des dix risques |
| 6 min | Vidéo d'explication n° 2 : une injection indirecte en direct sur l'index de NoteFlow | Second des deux sujets complexes filmés. Garder une erreur en direct si on explique sa cause | Regarde | Vidéo d'explication (sous-titrée) |
| 20 min | Écrire un texte piégé, l'ajouter à l'index et le tester sur son agent ; vérifier si une image Markdown peut faire fuiter des données | Montrer une vraie injection indirecte sur l'index construit en séance 2 | Écrit le texte piégé et observe ce que fait son agent | Document piégé fourni, agent du fil rouge avec index de S2 |
| 14 min | Situer NoteFlow sur la règle de deux, puis classer des défenses : celles qui bornent l'impact (minimum de droits aux outils, autorisation vérifiée par le code, validation humaine montrant l'action exacte, pas d'images externes dans les réponses) et celles qui réduisent la probabilité (filtrer les entrées et les sorties, marquer le contenu non fiable) | Aucune mesure ne suffit seule, et elles ne se valent pas : celles qui bornent l'impact résistent à un attaquant qui s'adapte, les filtres non | Classe les défenses et choisit celles qu'il met en place | Liste des défenses avec exemples de code, exercice de classement |

### S4.3 : TP : la suite de tests de l'agent (80 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 6 min | Vidéo : tester les garde-fous (outil sensible non appelé, sortie assainie, filtrage par droits) | Tester le contrôle, pas « le modèle refuse » | Regarde | Vidéo (sous-titrée) |
| 54 min | Écrire les tests déterministes des garde-fous contre la doublure : outil sensible jamais appelé sans confirmation, sortie assainie (pas d'image externe), filtrage par droits entre projets ; au moins deux tentatives d'injection, directe et indirecte | Un test d'injection qui passe du premier coup est probablement mal écrit | Écrit les tests, les fait échouer, puis corrige l'agent | Agent du fil rouge (état fin S3), fiche pas à pas, squelettes de tests, textes piégés |
| 20 min | Une suite séparée contre un vrai modèle, jouée sur k essais, résultat exprimé en taux (pass^k) ; intégrer au dépôt et mesurer la durée de la suite | La durée conditionne la CI de la séance 5 | Commit, lance les deux suites, note le taux et la durée | Commande de lancement, gabarit de relevé de durée, branche corrigée « état fin S4 » |

## Séance 5 (3 h) : Mettre en prod et conclure

### S5.1 : Exploiter une IA en production (25 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 10 min | Ce que l'épinglage d'un modèle garantit ou non (un modèle peut être retiré) ; évaluer avant de migrer ; promouvoir une version de prompt et revenir en arrière ; dérive lente contre incident ponctuel | Une mise à jour du modèle côté fournisseur est un déploiement qu'on ne contrôle pas. Épingler n'est pas optionnel en prod | Repère ce qu'il faut versionner et épingler dans son projet | Support écrit S5.1, exemple de dépôt de prompts versionnés |
| 5 min | Transparence : depuis le 2 août 2026, l'article 50 de l'AI Act impose d'informer l'utilisateur qu'il échange avec une IA, sans condition de haut risque ; RGPD minimal : avec un fournisseur en ligne, ce qui part dans le contexte quitte l'entreprise, d'où l'IA locale (chapitre 00) et ne pas journaliser les prompts complets | Le calendrier de l'AI Act a été modifié par le règlement (UE) 2026/1744 : ne pas annoncer le haut risque pour 2026. Calendrier complet et RGPD détaillé : approfondissement | Note les données qui passent par son agent | Support écrit S5.1 |
| 10 min | Définir trois alertes et leurs seuils ; ajouter le bandeau « assistant IA » à NoteFlow | Distinguer un incident ponctuel d'une dérive lente | Définit ses alertes et ajoute le bandeau | Modèle de définition d'alertes, agent du fil rouge |

### S5.2 : CI et déploiement (40 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 15 min | CI à deux étages : l'étage 1 bloque (doublure, sans secret), l'étage 2 est planifié ou lancé à la main (vrai modèle, pass^k) ; pièges des déclencheurs `schedule` et des secrets des forks ; déploiement du worker de file (`queue:restart` ou `reload`, Supervisor, route `/up`) ; l'IA locale en CI en encart de 3 min | L'IA locale en CI vérifie que la chaîne fonctionne (formats, appels d'outils, garde-fous) ; elle ne remplace pas l'évaluation de qualité sur le modèle de production, car les résultats d'un modèle ne se transposent pas à un autre | Repère ce qui bloque et ce qui tourne à côté | Support écrit S5.2 |
| 25 min | Écrire et lancer le workflow GitHub Actions de l'étage 1 avec la doublure ; parcourir la check-list de déploiement du worker | Faire tourner l'évaluation coûteuse à côté du chemin principal, mais la faire quand même tourner | Écrit son workflow, le lance, le voit passer au vert | Workflow GitHub Actions à deux étages, check-list de déploiement, docker-compose |

### S5.3 : Cas pratique, test final, conclusion (115 min)

| Durée | Contenu | Point d'attention | Ce que fait l'apprenant | Ressources |
|-----|------------------------|------------------|------------------|----------|
| 50 min | Cas pratique final : rédiger la fiche d'architecture du fil rouge (2 pages, 6 rubriques, dont « SDK ou code maison » et « pourquoi un agent ») : architecture choisie, stratégie de test, mesures de sécurité, coût estimé, et pour chaque rubrique le choix, l'alternative écartée et la raison | L'apprenant doit défendre des choix, pas décrire ce qu'il a codé. La fiche est déposée sur Teams et évaluée avec une grille fournie. Elle intègre la comparaison entre le code construit, le Laravel AI SDK, Spring AI et les outils dédiés (LangGraph en encart) | Rédige sa fiche à partir de son agent et de ses mesures des séances 3 et 4, la dépose | Modèle de fiche, grille d'évaluation, agent du fil rouge |
| 15 min | Correction du cas pratique en 2 vidéos de 7 min : une fiche de référence commentée, les erreurs fréquentes, ce qui distingue une justification d'une description ; mise en regard avec l'architecture du Laravel AI SDK | Mêmes principes, mêmes pièces | Regarde, s'auto-évalue avec la grille, note ce qu'il aurait changé | 2 vidéos de correction (sous-titrées), fiche de référence |
| 40 min | Test final : 40 QCM couvrant les huit objectifs (environ 5 questions par objectif, mélangées entre séances), corrigé avec explication par option | Vérifier les acquis, pas la mémoire : chaque question part d'une situation concrète | Passe le test, lit les explications de ses erreurs | Test final déposé sur Teams (format à confirmer), corrigé |
| 10 min | Vidéo de conclusion « pour aller plus loin » (8 min) : MCP, agents multiples, IA-juge validé contre des humains, CaMeL ; ce qui vient de l'architecture, du framework, du modèle | Conclure sur l'idée principale : l'agent IA s'isole comme une dépendance technique, mais son comportement oblige à adapter tests, observabilité et sécurité. L'évaluation continue n'est pas un sujet non couvert : elle est abordée par le jeu de référence et les alertes | Regarde, note ce qu'il retient et ce qu'il ferait différemment | Vidéo de conclusion (sous-titrée), bibliographie |

# Alignement des objectifs et de l'évaluation

Chaque objectif est enseigné, pratiqué dans un TP et évalué. Le test final de
S5.3 les couvre tous.

| Objectif | Évalué par |
|----------|------------|
| O1 Isoler le fournisseur | Tests fournis du TP S1.3, QCM du chapitre 01, rubrique 1 de la fiche |
| O2 Concevoir la boucle d'un agent | Critères du TP S2.4, QCM du chapitre 02, rubrique 2 de la fiche |
| O3 Construire et mesurer la récupération | Exercice du chapitre 02 (recall@5 calculé), critères du TP S2.4, rubrique 3 de la fiche |
| O4 Rendre résilient | Critères du TP S3.4 (panne simulée), QCM du chapitre 03 |
| O5 Instrumenter | Exercice du chapitre 03 (diagnostic sur traces), critères du TP S3.4, rubrique 4 de la fiche |
| O6 Tester | Critères du TP S4.3, QCM du chapitre 04 |
| O7 Analyser les risques et défendre | Exercice du chapitre 04 (classer les défenses), critères du TP S4.3, rubrique 5 de la fiche |
| O8 Mettre en production | Workflow de CI écrit en S5.2, rubrique 6 de la fiche, test final |

# Budget vidéo

Environ 86 minutes, toutes de 8 minutes au plus, sous-titrées.

| Vidéo | Durée | Séquence |
|-------|-------|----------|
| Présentation du cours, de l'équipe et des pré-requis | 3 min | 00.1 |
| Où placer un appel à une IA dans une appli en couches | 6 min | S1.1 |
| Lecture guidée des deux dépôts Laravel et Spring Boot | 5 min | S1.1 |
| Le timeout réel d'un appel d'IA dans un contrôleur | 3 min | S1.2 |
| Un port, deux fournisseurs, une ligne de config | 5 min | S1.3 |
| La boucle d'agent dessinée pas à pas (sujet complexe n° 1) | 6 min | S2.2 |
| pgvector et la mesure du recall | 6 min | S2.3 |
| Correction du TP instrumentation, 3 parties | 18 min | S3.4 |
| Injection indirecte en direct sur l'index (sujet complexe n° 2) | 6 min | S4.2 |
| Tester les garde-fous | 6 min | S4.3 |
| Correction du cas pratique, 2 parties | 14 min | S5.3 |
| Conclusion « pour aller plus loin » | 8 min | S5.3 |

La marge d'environ 4 minutes sous l'enveloppe de 1 h 30 reste disponible pour
un éventuel live coding (piste bonus du mentor).
