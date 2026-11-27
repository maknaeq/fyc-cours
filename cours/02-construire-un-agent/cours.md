# Chapitre 02 : Un agent IA, ça se construit comme un composant

> Durée estimée : 3 h (dont 65 min de TP) · Objectifs : concevoir la boucle d'un agent (contrat d'outils, conditions d'arrêt, budget, validation humaine) et justifier quand un workflow suffit, puis construire un pipeline de récupération sur pgvector et en mesurer la qualité par le recall@5.

Ce support couvre les séquences S2.1 à S2.3. Les mini-exercices sont à faire
avant de lire la réponse. Le TP de la séquence S2.4 a son propre énoncé, dans
le dépôt [xKaan/fyc-tp](https://github.com/xKaan/fyc-tp) (branche `fyc-tp-s2`).
Le cas qui sert de fil rouge, NoteFlow, est présenté dans `fil-rouge.md`.

## 1. Le contrat d'outil

### 1.1 Une réponse formatée pour le code

Un utilisateur écrit à NoteFlow : « Rappelle-moi de relancer le client pilote
avant vendredi. » L'application veut extraire les informations importantes
comme la tâche, avec un titre et une date butoire. Le modèle répond : « Bien
sûr ! Je vous propose de créer la tâche "relancer le client pilote" pour
vendredi. » Un humain comprend. Votre code doit extraire les informations clés
comme le titre et la date, qui seront formulées autrement lors du prochain
appel.

Plutôt que de deviner, on donne au modèle un **schéma JSON** : la description
de la forme attendue, avec les champs, leurs types et ceux qui sont
obligatoires (voir la
[référence JSON Schema](https://json-schema.org/understanding-json-schema)). Le
modèle répond alors dans cette forme, c'est une **sortie structurée**, prête à
être ingérée.

```json
{
  "type": "object",
  "properties": {
    "titre": { "type": "string" },
    "echeance": { "type": "string", "description": "Date au format AAAA-MM-JJ" }
  },
  "required": ["titre"]
}
```

La réponse devient `{"titre": "Relancer le client pilote", "echeance":
"2026-12-04"}`, que le code décode champ par champ.

Le schéma garantit la forme, pas le contenu. Certains fournisseurs imposent le
schéma (OpenAI a un mode `strict`, voir
[Function calling](https://platform.openai.com/docs/guides/function-calling)),
d'autres le traitent comme une consigne que le modèle suit en général. Dans les
deux cas, `{"titre": "", "echeance": "2026-02-30"}` est conforme : le titre est
bien une chaîne et le 30 février a bien la forme d'une date. Vérifier que le
titre n'est pas vide et que la date existe, c'est le rôle du code, comme pour
les données d'un formulaire.

Une réponse en texte libre qu'on découpe avec une expression régulière
fonctionne en démonstration, mais elle casse dès que le modèle change sa
formulation. Il vaut mieux demander une structure, puis la valider.

### 1.2 Le principe du tool calling

Pour éviter les doublons, l'agent de NoteFlow doit pouvoir lire les tâches
ouvertes. Or un modèle ne peut pas accéder à la base de données, il génère
seulement du texte. C'est donc le code de l'application qui fait le lien, et
qui est responsable de ce qui s'exécute.

Un **outil** est une fonction de l'application que l'on décrit au modèle avec un
**contrat** : un nom, une description qui indique quand l'utiliser, et le
schéma JSON de ses arguments. Le modèle ne voit que ce contrat, jamais le code
de la fonction ni les données qu'elle manipule. Ce mécanisme s'appelle le
**tool calling** (ou *function calling*). La documentation d'Anthropic le dit
ainsi : « The model never runs anything on its own »
([How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)),
et celle de Spring AI parle d'une « critical security consideration »
([Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)).

Un appel d'outil se déroule en cinq temps :

1. L'application envoie la question de l'utilisateur et les contrats des outils.
2. Le modèle répond par une **demande d'appel** (un nom d'outil et des
   arguments) au lieu d'un texte.
3. L'application vérifie la demande : l'outil existe, les arguments sont
   valides, l'utilisateur a le droit. Si c'est le cas, elle exécute l'outil.
4. Elle renvoie le résultat au modèle.
5. Le modèle rédige sa réponse, ou demande un autre outil (c'est la boucle de
   S2.2).

<!-- Schéma à construire par l'équipe (FYC-60) : assets/appel-d-outil.png, structure proposée dans assets/appel-d-outil.mmd -->

Les sections 1.3 à 1.5 reprennent ces temps un par un, avec un outil réel du
TP.

**Mini-exercice (2 min).** Sur les cinq temps, lesquels sont faits par le
modèle et lesquels par le code de NoteFlow ?

> **Réponse.** Le modèle intervient aux temps 2 et 5. Les temps 1, 3 et 4 sont
> faits par le code de NoteFlow : il envoie, vérifie et exécute, puis renvoie le
> résultat. Le modèle ne touche jamais à la base de données.

### 1.3 Décrire l'outil au modèle

C'est le temps 1. Prenons l'outil `lister_taches_ouvertes`, fourni dans le dépôt
du TP (`app/Application/Agent/Tools/ListerTachesOuvertes.php`, branche
`fyc-tp-s2`). Voici son contrat, tel que le modèle le reçoit :

```php
public function definition(): ToolDefinition
{
    return new ToolDefinition(
        name: 'lister_taches_ouvertes',
        description: 'Liste les tâches encore ouvertes, pour vérifier qu\'une tâche n\'existe pas déjà. '
            .'Ne renvoie que les tâches des projets de l\'utilisateur.',
        parameters: [
            'type' => 'object',
            'properties' => ['projet' => ['type' => 'string', 'description' => 'Nom exact du projet. Facultatif.']],
            'additionalProperties' => false,
        ],
    );
}
```

Le contrat est la seule information dont dispose le modèle pour choisir un
outil. Un nom clair et une description précise sur le moment où l'utiliser
améliorent donc ses choix (voir
[Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)).
Les paramètres sont décrits avec un schéma JSON, comme en 1.1 : ici un seul,
`projet`, qui est facultatif.

### 1.4 La demande d'appel du modèle

C'est le temps 2. Pour la question « A-t-on déjà une tâche pour le client
pilote ? », le modèle ne répond pas par du texte mais par une demande d'appel.
En voici le contenu (valeurs d'exemple) :

```text
lister_taches_ouvertes {"projet": "Produit"}
```

Chaque fournisseur formate cette demande à sa façon, ainsi que le résultat qu'on
lui renvoie ensuite :

| Fournisseur | Demande d'appel | Résultat renvoyé |
|---|---|---|
| [Mistral](https://docs.mistral.ai/inference/conversations/function-calling) | `tool_calls` avec identifiant, arguments en chaîne JSON | message `tool` avec `tool_call_id` |
| [Ollama](https://docs.ollama.com/capabilities/tool-calling) | `tool_calls`, arguments en objet, sans identifiant | message `role: "tool"` avec `tool_name` |
| [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) | bloc `tool_use` avec identifiant, arguments en objet | bloc `tool_result` |

L'adaptateur de la séance 1 traduit ces formats en un type neutre, `ToolCall`.
Le cœur de l'application ne connaît que celui-ci, ce qui permet de changer de
fournisseur sans modifier l'agent.

### 1.5 Vérifier la demande et exécuter l'outil

Ce sont les temps 3 et 4, entièrement faits par le code. Il cherche d'abord
l'outil demandé dans une liste fermée, l'exécute, puis prépare le message de
retour pour le modèle :

```php
$tool = $toolbox->find($call->name);   // null si le modèle a inventé un nom

if ($tool === null) {
    $result = ToolResult::error('Outil inconnu. Disponibles : '.implode(', ', $toolbox->names()));
} else {
    try {
        $result = $tool->run($call->arguments, $user);
    } catch (InvalidToolArguments $e) {
        $result = ToolResult::error($e->getMessage());   // le modèle peut corriger
    }
}
$messages[] = Message::toolResult($call, $result->toJson());
```

Voici le code de `run()` pour notre outil, abrégé (la
[validation de Laravel](https://laravel.com/docs/13.x/validation) est
documentée à part) :

```php
public function run(array $arguments, User $user): ToolResult
{
    // 1. Valider les arguments, même si le schéma les décrit
    $validator = Validator::make($arguments, ['projet' => ['nullable', 'string', 'max:100']]);
    if ($validator->fails()) {
        throw InvalidToolArguments::fromValidator($validator);
    }

    // 2. Appliquer les droits dans la requête : seulement les projets de l'utilisateur
    $taches = Task::query()
        ->where('status', Task::OPEN)
        ->whereIn('project_id', $user->readableProjectIds())
        ->limit(20)->get();

    // 3. Renvoyer un résultat court : ce dont le modèle a besoin, rien de plus
    return ToolResult::ok(['taches' => $taches->map(fn (Task $t): array => [
        'id' => $t->id, 'titre' => $t->title, 'echeance' => $t->due_on?->format('Y-m-d'),
    ])->all()]);
}
```

`$user` vient de l'appelant, pas des arguments : le modèle ne choisit pas pour
quel utilisateur il travaille.

Pour notre exemple, le résultat renvoyé au modèle est (valeurs d'exemple) :

```text
{"taches": [{"id": 7, "titre": "Relancer le client pilote", "echeance": "2026-12-04"}]}
```

Une erreur (outil inconnu, arguments invalides) ne plante pas l'agent : elle est
renvoyée au modèle comme un résultat, et il corrige son appel au tour suivant.
Avec ce résultat, le modèle rédige sa réponse : c'est le temps 5.

**Mini-exercice (3 min).** Dans le TP, vous écrirez `chercher_notes` sur ce
modèle. Faut-il y mettre l'utilisateur courant comme argument du contrat ?

> **Réponse.** Non. Un argument est rempli par le modèle : c'est une proposition,
> donc il n'est pas fiable. L'identité de l'utilisateur vient du code, en
> paramètre de `run()`, et le filtre par droits se fait dans la requête.

### 1.6 Limiter les droits d'un outil

Un collègue propose d'ajouter l'outil `executer_sql(requete)` à l'agent de
NoteFlow, « pour qu'il réponde à toutes les questions ». Un seul outil
suffirait, sans limite à gérer. C'est pratique, mais c'est ce qu'il faut éviter.

Chaque outil donne au modèle un accès à votre code. Si le modèle produit un
appel inattendu, parce qu'il se trompe ou parce qu'un texte qu'il a lu l'a
manipulé, l'appel s'exécute avec tous les droits de l'outil. OWASP nomme ce
risque *Excessive Agency* et le classe 3e de son Top 10 des applications LLM
2026 ([LLM03:2026](https://genai.owasp.org/llm2026/llm032026-excessive-agency/)).
Il en distingue trois causes : trop de fonctionnalités, trop de permissions,
trop d'autonomie. On en tire quatre règles à appliquer dès le premier outil.

- Peu d'outils, et des outils étroits : `chercher_notes` plutôt que
  `executer_sql`. OWASP déconseille les outils ouverts, comme « lancer une
  commande » ou « lire n'importe quelle URL ».
- Les droits de l'utilisateur courant appliqués dans la requête, comme le fait
  `lister_taches_ouvertes` avec `readableProjectIds()`, pour que l'agent ne
  voie que ce que l'utilisateur voit.
- Une vérification dans le code à chaque appel (outil connu, arguments
  validés). L'autorisation est décidée par la logique de l'application, jamais
  par le modèle (OWASP parle de *complete mediation*).
- L'accord de l'utilisateur pour toute action qui écrit, sur l'action exacte et
  pas sur un résumé. C'est le rôle de `creer_tache` dans le TP (S2.2).

On rencontre parfois la solution inverse : écrire dans le prompt « ne lis jamais
les notes du projet Infra ». Une consigne ne bloque rien : le modèle peut
l'ignorer ou être manipulé pour la contourner. Si ces notes ne doivent pas
sortir, la requête ne doit pas les renvoyer.

Cela ne règle pas tout. Aucune défense connue ne rend un modèle insensible à
l'injection de prompt : OWASP écrit qu'il n'existe pas de prévention fiable
([LLM01:2026](https://genai.owasp.org/llm2026/llm012026-prompt-injection/)). On
limite donc ce qu'un modèle manipulé pourrait faire, et la séance 4 y revient.

**Mini-exercice (3 min).** On vous propose `lire_url(url)` pour que l'agent
ouvre les liens collés dans les notes. Qu'en pensez-vous ?

> **Réponse.** Une URL quelconque, c'est un outil ouvert que rien ne limite, et
> NoteFlow n'en a pas besoin pour son cas métier : c'est trop de fonctionnalités,
> au sens d'OWASP. On ne l'expose pas. Si le besoin devient réel, on propose un
> outil plus étroit, par exemple limité à une liste de domaines.

### 1.7 Le même outil avec un SDK

Dans les sections 1.3 à 1.5, le contrat, la validation et le traitement de la
demande sont écrits à la main. Le [Laravel AI SDK](https://laravel.com/docs/ai-sdk)
(`laravel/ai`) gère cette partie. Voici le même outil (extrait adapté de la
documentation, non exécuté) :

```php
class ListerTachesOuvertes implements Tool
{
    public function description(): Stringable|string
    {
        return 'Liste les tâches encore ouvertes, pour éviter un doublon.';
    }

    public function schema(JsonSchema $schema): array
    {
        return ['projet' => $schema->string()];
    }

    public function handle(Request $request): Stringable|string
    {
        $valide = $request->validate(['projet' => 'nullable|string|max:100']);
        // Les droits de l'utilisateur : à appliquer ici
        return json_encode($this->tachesOuvertes($valide['projet'] ?? null));
    }
}
```

Avec [Spring AI](https://docs.spring.io/spring-ai/reference/api/tools.html), une
méthode annotée `@Tool(description = "...")` joue le même rôle, et `@ToolParam`
décrit chaque paramètre. Dans les deux cas, le SDK génère le schéma, envoie les
contrats, reconnaît la demande, appelle la méthode et renvoie le résultat. Si la
validation échoue, le SDK Laravel renvoie les messages d'erreur au modèle pour
qu'il corrige son appel, comme notre `InvalidToolArguments`. En revanche, il ne
connaît pas les droits de l'utilisateur : ils restent à appliquer dans le code
de l'outil, comme en 1.6.

Anthropic recommande de commencer par l'API directe, car les frameworks
masquent les consignes et les réponses échangées, ce qui conduit souvent à de
fausses hypothèses sur leur fonctionnement
([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)).
C'est pour cette raison que le TP se fait sans SDK, et que la comparaison vient
ensuite.

### 1.8 Le protocole MCP (pour aller plus loin)

Le **Model Context Protocol** (MCP) est un protocole ouvert qui permet à une
application d'exposer ses outils à d'autres, sans réécrire le contrat pour
chaque agent. Le modèle fait toujours du tool calling comme ci-dessus : MCP
standardise la découverte et le transport des outils. Spring AI traite un outil
distant comme un outil local, et le Laravel AI SDK fait de même avec le paquet
`laravel/mcp`. Un outil MCP reste un accès à du code : les règles de 1.6
s'appliquent aussi aux outils que vous n'avez pas écrits. Le protocole évolue
vite (révision [2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
à la date d'écriture), il faut donc vérifier la version avant de suivre un
tutoriel. Ce point n'est ni manipulé en TP ni évalué.

### 1.9 Ce qu'il faut retenir de S2.1

- Une sortie structurée fixe la forme de la réponse, le code vérifie le contenu.
- Le modèle demande un appel d'outil. C'est le code qui valide les arguments,
  applique les droits de l'utilisateur, puis exécute.
- Un outil étroit, aux droits de l'utilisateur, vaut mieux qu'un outil large
  protégé par une consigne.

Un seul aller-retour ne fait pas encore un agent. En S2.2, le code rappelle le
modèle tant qu'il demande des outils, et il faut décider quand l'arrêter.

<!-- Sections à venir : 2. Workflow ou agent ? La boucle et ses arrêts (S2.2, Timothé, FYC-52) ; 3. Récupérer l'information, et le mesurer (S2.3, Erwin). -->
