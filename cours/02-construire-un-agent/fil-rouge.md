# Fil rouge : NoteFlow, une app de notes avec agent

> Projet que l'apprenant fait évoluer de S2.4 à S5.3. Le dépôt de code arrive
> en séance 3 : cette page présente le cas au mentor pour la séance 2.

## 1. Cas métier

**NoteFlow** est une application de prise de notes façon Notion, utilisée par
une petite équipe produit (5 à 10 personnes) pour centraliser ses réunions,
ses décisions et ses spécifications. Chaque utilisateur écrit des notes
courtes en markdown, organisées par projet et par étiquette (tag), sans
structure imposée. Avec le temps, l'équipe accumule des dizaines de notes que
plus personne ne relit, et des actions décidées en réunion restent sans
suite. L'agent est là pour trois choses : retrouver une note pertinente parmi
toutes les autres à partir d'une question posée en langage naturel, aider
à rédiger une note en l'étoffant à partir d'un brouillon, et proposer de créer
une tâche quand une note contient une action non suivie. L'agent ne modifie
jamais une note ni ne crée une tâche sans validation explicite de
l'utilisateur.

## 2. Outils exposés par l'agent

| Outil | Ce qu'il fait | Entrée | Sortie |
|---|---|---|---|
| `chercher_notes` | Recherche par similarité dans l'index de notes (RAG, S2.3) | une question en langage naturel | une liste de notes (titre, extrait, score) |
| `creer_tache` | Crée une tâche liée à une note source | titre de la tâche, note source, échéance optionnelle | la tâche créée |
| `lister_taches_ouvertes` | Liste les tâches déjà ouvertes, pour éviter les doublons avant d'en créer une | filtre de projet optionnel | une liste de tâches |
| `etoffer_note` | Propose une version plus étoffée d'un brouillon court (auto-complétion), sans jamais l'enregistrer elle-même | le brouillon de note | une proposition de texte plus complet |

`chercher_notes` et `etoffer_note` sont en lecture ou en proposition seule.
Seul `creer_tache` modifie une donnée : c'est le seul outil qui justifie,
en séance 4, un point d'attention sur les droits qu'on lui accorde.

## 3. Jeu de notes à indexer (RAG, S2.3)

26 notes réalistes, réparties par thème. Les titres ci-dessous servent de plan
pour rédiger le contenu complet au moment du dépôt de code (séance 3).

**Onboarding et équipe (4)**
- Bienvenue dans l'équipe : outils et accès
- Organigramme et rôles au 09/2026
- Charte de communication asynchrone
- Trombinoscope et disponibilités

**Réunions et décisions (7)**
- Compte-rendu : réunion de cadrage NoteFlow
- Compte-rendu : point hebdo du 01/09
- Décision : abandon du plan gratuit illimité
- Décision : choix de PostgreSQL plutôt que MongoDB
- Compte-rendu : rétrospective sprint 12
- Compte-rendu : point avec le client pilote
- Décision : report de la fonctionnalité export PDF

**Spécifications produit (6)**
- Spécification : recherche par similarité dans les notes
- Spécification : partage d'une note en lecture seule
- Spécification : étiquettes et projets
- Spécification : notifications de mention
- Spécification : historique des versions d'une note
- Spécification : mode hors ligne (brouillon)

**Bugs et incidents (4)**
- Incident : perte de mise en forme à l'export
- Bug : doublons de notes après synchronisation
- Incident : lenteur de recherche au-delà de 500 notes
- Bug : mentions qui ne notifient pas le bon utilisateur

**Process et runbooks (3)**
- Runbook : restaurer une note supprimée par erreur
- Process : revue de code avant mise en production
- Process : gestion des accès à la base de données

**Glossaire (2)**
- Glossaire : vocabulaire produit NoteFlow
- Glossaire : niveaux de priorité des tâches

## 4. Critères de réussite par séance

| Séance | Critère de réussite |
|---|---|
| S2.4 (agent + recherche) | Pour une question test (« qu'a-t-on décidé pour la base de données ? »), `chercher_notes` retourne la note « Décision : choix de PostgreSQL plutôt que MongoDB » parmi les résultats. L'agent peut créer une tâche via `creer_tache` à partir d'une note contenant une action explicite. L'agent fonctionne à l'identique avec l'IA en ligne et l'IA locale, sans changer le cœur métier. |
| S3.3 (suivi + plan de secours) | Chaque appel (recherche, outil, génération) est tracé avec un identifiant de requête commun, sa durée et son coût. En coupant l'accès à l'IA en ligne, l'agent bascule sur l'IA locale puis, si elle aussi est indisponible, sur un mode sans IA qui reste capable de retrouver des notes par recherche lexicale simple. |
| S4.4 (tests + injections) | La suite de tests couvre le cas normal avec une doublure de fournisseur. Au moins un test d'injection directe (dans la question posée à l'agent) et un test d'injection indirecte (texte piégé caché dans une note indexée) prouvent que `creer_tache` n'est jamais appelé sans une action réellement présente dans une note légitime. |
| S5.3 (cas pratique final) | La fiche d'architecture justifie, sur ce cas précis, les choix de découpage du pipeline RAG, la politique de résilience retenue, le coût mensuel estimé pour l'équipe de 5 à 10 personnes, et les mesures de sécurité effectivement en place face aux deux types d'injection testés en S4. |

## 5. Fourni à l'apprenant vs construit par l'apprenant

Rappel : le cours n'utilise pas de SDK d'IA (Laravel AI SDK, Spring AI). Ils
n'apparaissent qu'en comparaison, jamais dans le code de l'apprenant.

**Fourni**
- Le dépôt de départ Laravel réorganisé en S1.4 (architecture en ports et
  adaptateurs, sans logique d'IA).
- Le schéma de base de données des notes, étiquettes, projets et tâches.
- Le jeu des 26 notes à indexer (contenu complet, livré avec le dépôt de S3).
- Le script de panne simulée utilisé en S3.3.
- Les squelettes de tests et les textes piégés utilisés en S4.4.

**Construit par l'apprenant**
- L'adaptateur vers le fournisseur d'IA (en ligne et local).
- Le contrat des quatre outils et la boucle d'agent qui les enchaîne.
- Le pipeline RAG complet : découpage des notes, vectorisation, indexation
  et recherche sur pgvector.
- Le retry, le coupe-circuit et le plan de repli à trois niveaux.
- La doublure de fournisseur et la suite de tests, y compris les cas
  d'injection directe et indirecte.
