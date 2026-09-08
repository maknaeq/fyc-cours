---
title: "Présentation de la problématique"
subtitle: "Projet FYC 2026-2027"
author: "Quentin Bauduin, Timothé Geoffroy, Kaan Topkaya, Erwin Gossin"
date: "9 septembre 2026"
---

# Constitution du groupe

| Nom | Prénom | Filière |
|-----|--------|---------|
| Bauduin | Quentin | _à compléter_ |
| Geoffroy | Timothé | _à compléter_ |
| Topkaya | Kaan | _à compléter_ |
| Gossin | Erwin | _à compléter_ |

# Sujet

**Concevoir une application web maintenable intégrant un agent IA :
architecture, tests, sécurité et mise en production.**

Le cours traite l'intégration d'un agent IA dans une application web comme un
problème d'ingénierie logicielle, et non comme une fonctionnalité que l'on
branche. Il s'appuie sur deux parcours techniques au choix, Spring AI (Java) et
Laravel AI SDK (PHP), pour faire ressortir les principes d'architecture qui
restent valables quel que soit le framework.

# Élaboration de la problématique

Méthode (voir `ressources/rediger-une-problematique.pdf`) : partir d'une
opinion couramment admise, la confronter à des constats, puis formuler la
question qui en résulte.

## Opinion couramment admise

Ajouter de l'IA à une application web serait simple : les fournisseurs
exposent une API, les frameworks proposent un SDK, il suffirait d'appeler un
modèle depuis un contrôleur et d'afficher la réponse. L'agent IA serait un
composant comme un autre, au même titre qu'une base de données ou un service
de paiement.

## Constats

Le comportement d'un agent IA diffère de celui des composants classiques sur
plusieurs points, et chacun a des conséquences directes sur l'architecture.

- **Non-déterminisme.** À entrée identique, la réponse d'un modèle varie. Les
  tests fondés sur l'égalité exacte ne fonctionnent plus, et la qualité peut
  baisser sans qu'une ligne de code ait changé.
- **Latence variable et élevée.** Un appel à un modèle prend souvent plusieurs
  secondes. Fait en direct dans une requête HTTP, il bloque un worker, provoque
  des timeouts et dégrade l'expérience de tous les utilisateurs.
- **Coût par appel.** Chaque requête est facturée, souvent au token. Une boucle
  d'agent mal bornée ou une politique de réessai naïve peut multiplier la
  facture sans que rien ne l'arrête.
- **Dépendance à un fournisseur externe.** Le modèle, ses versions, sa
  disponibilité et ses tarifs échappent à l'équipe. Une mise à jour côté
  fournisseur est un déploiement que l'on ne contrôle pas.
- **Nouvelle surface d'attaque.** Les instructions et les données passent par
  le même canal textuel. L'injection de prompt, directe ou indirecte via un
  document indexé, occupe la première place du référentiel OWASP Top 10 pour
  les applications fondées sur des LLM, et aucune mesure isolée ne la règle.
- **Outillage jeune et hétérogène.** Les SDK d'intégration (Spring AI, Laravel
  AI SDK, LangChain) sont récents, évoluent vite et proposent des abstractions
  différentes pour les mêmes besoins : outils, RAG, observabilité, tests.

Isolé derrière une interface, l'agent IA se branche comme une dépendance
technique. Mais son comportement oblige à repenser les tests, l'observabilité,
la sécurité et le cycle de mise en production.

## Questions soulevées

- Où placer l'appel à l'IA dans une architecture en couches pour que le cœur
  métier n'en dépende pas, et pour pouvoir changer de fournisseur ou basculer
  sur un modèle local sans réécrire l'application ?
- Comment tester un composant dont la sortie n'est jamais garantie identique,
  et comment détecter une régression de qualité en production ?
- Comment rendre l'application résiliente aux pannes, aux lenteurs et aux
  dérives de coût d'un service externe ?
- Comment se protéger d'un utilisateur ou d'un document qui manipule l'agent,
  alors que le modèle ne distingue pas les instructions des données ?
- Que faut-il versionner, surveiller et évaluer en continu quand une partie du
  comportement de l'application vit dans un prompt et dans un modèle tiers ?
- Ces réponses dépendent-elles du framework choisi, ou existe-t-il des
  principes communs que la comparaison Spring AI / Laravel AI SDK permet de
  dégager ?

# Problématique

> **Comment intégrer un agent IA dans une application web sans dégrader sa
> maintenabilité, sa testabilité, sa sécurité et sa maîtrise en production ?**

# Délimitation et pré-requis

**Ce que le cours couvre.** L'architecture d'intégration (ports et adaptateurs,
CQRS, événements), la construction d'un agent avec outils et RAG, la
résilience et l'observabilité des appels IA, les stratégies de test d'un
composant non déterministe, les risques de sécurité propres aux LLM et leurs
parades, et l'adaptation du cycle de mise en production. Chaque notion est
mise en pratique sur un fil rouge que l'apprenant fait évoluer d'une séance à
l'autre, dans le parcours de son choix.

**Ce que le cours ne couvre pas.** L'entraînement ou le fine-tuning de
modèles, la théorie des réseaux de neurones, le choix d'un modèle sur des
critères de performance brute, et l'apprentissage des frameworks Spring Boot
ou Laravel eux-mêmes.

**À qui il s'adresse.** Développeurs de niveau première année de mastère,
à l'aise en programmation orientée objet (Java ou PHP), connaissant un
framework web, les API REST et Git. Aucune connaissance préalable en IA
n'est requise.

**Comparaison des frameworks.** Spring AI et Laravel AI SDK ne sont pas
l'objet du cours mais sa méthode. Confronter deux implémentations du même
besoin permet de séparer ce qui vient du framework de ce qui relève de
principes d'architecture indépendants du langage.
