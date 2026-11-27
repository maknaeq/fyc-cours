# Exercices : chapitre 02

## Exercice 1 : Quels outils exposer à l'agent ?

**Objectif :** appliquer les règles de la section 1.6 (outils étroits, droits de l'utilisateur, accord avant d'écrire) à une liste d'outils candidats.
**Durée :** 10 min

### Énoncé

Un collègue propose huit outils pour l'agent de NoteFlow. Le besoin de l'agent
est le suivant : retrouver des notes, éviter les doublons et proposer de créer
des tâches à partir d'une note. Il n'enregistre aucune modification sans la
validation de l'utilisateur (voir `fil-rouge.md`).

Pour chaque outil, choisissez un statut et justifiez-le en une phrase :

- **Exposé** : l'agent peut l'appeler, avec les droits de l'utilisateur courant.
- **Exposé avec accord** : l'agent propose l'appel, et l'utilisateur confirme
  l'action exacte avant qu'elle s'exécute.
- **Non exposé** : l'agent n'y a pas accès.

| Outil | Ce qu'il fait | Statut | Pourquoi |
|---|---|---|---|
| `chercher_notes(question)` | Cherche dans les notes | | |
| `lister_taches_ouvertes(projet)` | Liste les tâches ouvertes d'un projet | | |
| `creer_tache(titre, note_source, echeance)` | Crée une tâche liée à une note | | |
| `modifier_note(note_id, contenu)` | Remplace le contenu d'une note | | |
| `executer_sql(requete)` | Exécute une requête SQL sur la base | | |
| `lire_notes_utilisateur(utilisateur_id)` | Renvoie les notes d'un utilisateur | | |
| `envoyer_email(destinataire, objet, texte)` | Envoie un e-mail | | |
| `supprimer_projet(projet_id)` | Supprime un projet et ses tâches | | |

### Indices

1. Pour chaque outil, posez trois questions : NoteFlow en a-t-il besoin ? Que
   peut faire le modèle si l'appel est inattendu ? Qui décide de ce qui
   s'exécute, le code ou le modèle ?
2. Relisez la liste des quatre règles de la section 1.6.

### Corrigé

| Outil | Statut | Pourquoi |
|---|---|---|
| `chercher_notes` | Exposé | Lecture seule, et nécessaire au besoin. La requête filtre par les droits de l'utilisateur courant. |
| `lister_taches_ouvertes` | Exposé | Lecture seule, nécessaire pour éviter les doublons. Même filtre par droits, et un nombre de résultats limité. |
| `creer_tache` | Exposé avec accord | Elle écrit en base. L'utilisateur confirme l'action exacte (titre, note source, échéance) avant l'exécution. |
| `modifier_note` | Non exposé | Le fil rouge interdit à l'agent de modifier une note. Le besoin est couvert par `etoffer_note`, qui propose un texte sans l'enregistrer. |
| `executer_sql` | Non exposé | Outil ouvert : l'agent pourrait lire ou modifier n'importe quelle table, sans filtre par droits. |
| `lire_notes_utilisateur` | Non exposé | L'identité est un argument rempli par le modèle, donc il pourrait demander les notes d'un autre utilisateur. |
| `envoyer_email` | Non exposé | Aucun besoin dans le cas métier. Un texte piégé lu par l'agent pourrait lui faire envoyer des données à l'extérieur. |
| `supprimer_projet` | Non exposé | Action irréversible, sans lien avec le besoin. |

**La démarche.** Le critère de départ est le besoin, pas le danger : un outil
qui ne sert à rien dans le cas métier n'est pas exposé, même s'il est pratique.
Parmi les outils utiles, on regarde ensuite s'ils lisent ou s'ils écrivent. Une
lecture est exposée avec les droits de l'utilisateur, une écriture demande son
accord. Les trois racines d'*Excessive Agency* d'OWASP se retrouvent dans la
liste : trop de fonctionnalités (`executer_sql`), trop de permissions
(`lire_notes_utilisateur`), trop d'autonomie (`supprimer_projet`, `modifier_note`
sans validation). Le scénario « assistant e-mail détourné » de la page
[LLM03:2026](https://genai.owasp.org/llm2026/llm032026-excessive-agency/)
correspond à `envoyer_email`.

**Erreurs fréquentes.**

- Garder un outil dangereux en ajoutant une consigne dans le prompt (« n'utilise
  `supprimer_projet` que si on te le demande »). Une consigne ne bloque rien
  (voir 1.6).
- Penser qu'une lecture est sans risque. Sans filtre par droits dans la requête,
  `chercher_notes` donnerait accès à toutes les notes.
- Remplacer la vérification du code par l'accord de l'utilisateur. L'accord
  s'ajoute à la validation des arguments et aux droits, il ne les remplace pas.

**Pour vérifier.** Pour chaque outil que vous avez gardé, vous devez pouvoir
citer la règle de la section 1.6 qui s'applique. Si ce n'est pas le cas, vous
avez probablement trop exposé.

**Et ensuite.** Au TP de la séquence S2.4, vous écrivez `chercher_notes` et
`creer_tache` avec ces règles. La confirmation de l'action revient en S2.2, et
le cas d'un texte piégé dans une note en séance 4.
