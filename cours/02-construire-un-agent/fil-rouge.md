# Fil rouge : NoteFlow, une app de notes avec agent

> Projet que l'apprenant fait évoluer de S2.4 à S5.3. Le contenu complet des
> 26 notes est livré avec la séquence S2.3 et le dépôt de départ avec le TP
> S2.4 : cette page présente le cas au mentor.

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
| `chercher_notes` | Recherche dans l'index de notes (plein texte, puis similarité, S2.3), limitée aux notes que l'utilisateur courant a le droit de lire | une question en langage naturel | une liste de notes (titre, extrait, score) |
| `creer_tache` | Crée une tâche liée à une note source | titre de la tâche, note source, échéance optionnelle | la tâche créée |
| `lister_taches_ouvertes` | Liste les tâches déjà ouvertes, pour éviter les doublons avant d'en créer une | filtre de projet optionnel | une liste de tâches |
| `etoffer_note` | Propose une version plus étoffée d'un brouillon court (auto-complétion), sans jamais l'enregistrer elle-même | le brouillon de note | une proposition de texte plus complet |

`creer_tache` est le seul outil qui modifie une donnée, mais ce n'est pas le
seul qui demande des droits. `chercher_notes` lit des données privées : la
recherche est filtrée par les droits de l'utilisateur courant dans la requête
SQL elle-même, jamais par une consigne dans le prompt. Et comme les notes
indexées sont du contenu non fiable, la réponse de l'agent ne doit pas pouvoir
faire sortir de données (pas d'image externe dans le rendu Markdown). Enfin,
`creer_tache` écrit en base : il est idempotent (clé d'idempotence, S3.1),
pour qu'un nouvel essai (S3.2) ne crée pas de doublon.

## 3. Jeu de notes à indexer (RAG, S2.3)

26 notes réalistes, réparties par thème. Les titres ci-dessous servent de plan
pour rédiger le contenu complet, livré avec la séquence S2.3 (le TP S2.4 les
indexe).

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
| S2.3 (récupération) | Le recall@5 est calculé sur cinq questions de référence, en comparant la recherche plein texte et la recherche vectorielle. |
| S2.4 (agent + recherche) | Pour une question test (« qu'a-t-on décidé pour la base de données ? »), `chercher_notes` retourne la note « Décision : choix de PostgreSQL plutôt que MongoDB » parmi les résultats, et seulement parmi les notes que l'utilisateur a le droit de lire. L'agent s'arrête à un plafond d'étapes. Il peut créer une tâche via `creer_tache` à partir d'une note contenant une action explicite, après une confirmation qui montre l'action exacte. Sa réponse cite la note source ou dit « je ne sais pas ». Cinq cas de référence sont écrits. L'agent remplit les mêmes critères avec l'IA en ligne et l'IA locale, sans changer le cœur métier : seuls l'adaptateur et sa configuration changent (par exemple la taille de contexte d'Ollama). |
| S3.4 (suivi + plan de secours) | Chaque requête produit une trace avec un identifiant commun, un span par appel au modèle, par outil et par recherche, avec sa durée, ses tokens et son coût. En coupant l'accès à l'IA en ligne, l'agent bascule sur l'IA locale puis, si elle aussi est indisponible, sur un mode sans IA qui reste capable de retrouver des notes par recherche plein texte. Rejouer un même appel à `creer_tache` ne crée pas de doublon. Deux cas de référence tirés des traces s'ajoutent aux cinq de S2.4. |
| S4.3 (tests + injections) | Les tests déterministes couvrent le cas normal avec une doublure de fournisseur. Un test d'injection directe (dans la question posée à l'agent) et un test d'injection indirecte (texte piégé caché dans une note indexée) vérifient que, lorsque la doublure simule une demande de `creer_tache` issue du texte piégé, le code de l'application refuse l'appel ou le soumet à la validation de l'utilisateur. Deux autres tests vérifient que la sortie ne contient pas d'image externe et que la recherche ne renvoie pas les notes d'un autre projet. Rejoués contre un vrai modèle sur plusieurs essais, les mêmes cas donnent un taux (pass^k), pas une preuve. |
| S5.3 (cas pratique final) | La fiche d'architecture justifie, sur ce cas précis, les choix de découpage du pipeline RAG, la politique de résilience retenue, le coût mensuel estimé pour l'équipe de 5 à 10 personnes, le choix entre un SDK et du code maison, la raison d'avoir un agent plutôt qu'un workflow, et les mesures de sécurité effectivement en place face aux deux types d'injection testés en S4.3. |

## 5. Fourni à l'apprenant vs construit par l'apprenant

Rappel : le cours n'utilise pas de SDK d'IA (Laravel AI SDK, Spring AI). Ils
n'apparaissent qu'en comparaison, jamais dans le code de l'apprenant.

**Fourni**
- Le dépôt de départ Laravel réorganisé en S1.3 (architecture en ports et
  adaptateurs, sans logique d'IA), étendu pour S2.4 sur la branche
  `fyc-tp-s2` de [xKaan/fyc-tp](https://github.com/xKaan/fyc-tp/tree/fyc-tp-s2) :
  port de tool calling et adaptateurs normalisés, outil d'exemple
  `lister_taches_ouvertes`, confirmation des actions, tests du TP.
- Le schéma de base de données des notes, étiquettes, projets et tâches.
- Le jeu des 26 notes à indexer (contenu complet, livré avec la séquence S2.3).
- Le script de panne simulée utilisé en S3.4.
- Les squelettes de tests et les textes piégés utilisés en S4.3.

**Construit par l'apprenant**
- L'adaptateur vers le fournisseur d'IA (en ligne et local).
- Le contrat des quatre outils et la boucle d'agent qui les enchaîne.
- Le pipeline RAG complet : recherche plein texte, découpage des notes,
  vectorisation, indexation et recherche sur pgvector, avec le filtrage par
  droits.
- La clé d'idempotence de `creer_tache`, le retry, le coupe-circuit et le plan
  de repli à trois niveaux.
- La doublure de fournisseur et la suite de tests, y compris les cas
  d'injection directe et indirecte.
