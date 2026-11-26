# Chapitre 02 : Un agent IA, ça se construit comme un composant

> Durée estimée : 3 h (dont 65 min de TP) · Objectifs : concevoir la boucle d'un agent (contrat d'outils, conditions d'arrêt, budget, validation humaine) et justifier quand un workflow suffit, puis construire un pipeline de récupération sur pgvector et en mesurer la qualité par le recall@5.

Ce support couvre les séquences S2.1 à S2.3. Chaque section se termine par un
mini-exercice : faites-le avant de lire la réponse. Le TP de la séquence S2.4
(« l'agent NoteFlow ») a son propre énoncé, dans le dépôt
[xKaan/fyc-tp](https://github.com/xKaan/fyc-tp) (branche `fyc-tp-s2`). Le cas
qui sert de fil rouge, NoteFlow, est présenté dans `fil-rouge.md`.

## 1. Le contrat d'outil : ce que l'IA demande, ce que le code décide

### 1.1 Faire répondre le modèle dans un format que le code sait lire

Un utilisateur de NoteFlow écrit : « Rappelle-moi de relancer le client pilote
avant vendredi. » L'application doit en tirer une tâche, avec un titre et une
échéance. Le modèle répond : « Bien sûr ! Voici la tâche à créer : relancer le
client pilote, d'ici vendredi. » C'est lisible pour un humain, inutilisable
pour du code : où est le titre, dans quel format est la date ? Comment obtenir
une réponse que le code lit sans deviner ?

On demande au modèle de répondre selon un **schéma JSON** : une description de
la forme attendue (champs, types, champs obligatoires), elle-même écrite en
JSON (si vous ne l'avez jamais vu, voir la
[référence JSON Schema](https://json-schema.org/understanding-json-schema)).
Réponse obtenue de cette façon : une **sortie structurée**.

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

Avec ce schéma, le modèle ne renvoie plus une phrase mais un objet :
`{"titre": "Relancer le client pilote", "echeance": "2026-12-04"}`. Le code le
décode et lit chaque champ.

Le schéma décrit la forme, pas le sens. Certains fournisseurs proposent un
mode strict qui impose le schéma (OpenAI, voir
[Function calling](https://platform.openai.com/docs/guides/function-calling)),
d'autres le traitent comme une indication. Même en mode strict, rien ne
garantit que le titre ait un sens, que la date existe ou qu'elle soit à venir.
Le code valide donc toujours ce qu'il reçoit, comme il le ferait pour un
formulaire rempli par un inconnu.

**Piège.** On voit souvent extraire le titre de la phrase du modèle avec une
expression régulière. Le problème, c'est que la formulation change d'un appel
à l'autre (la séquence S1.2 l'a montré) et d'un modèle à l'autre. À la place :
demander une sortie structurée, puis la valider.

**Mini-exercice (3 min).** L'objet `{"titre": "", "echeance": "2026-02-30"}`
respecte le schéma ci-dessus. Qu'est-ce que le schéma ne détecte pas ?

> **Réponse :** un titre vide (c'est bien une chaîne de caractères) et une date
> qui n'existe pas (le 30 février a la forme d'une date). On pourrait durcir
> le schéma (longueur minimale, motif de date), mais seul le code, qui connaît
> le calendrier, détecte le 30 février.

### 1.2 Le modèle propose, le code décide

Pour que l'agent de NoteFlow évite de créer une tâche en double, il doit
pouvoir consulter les tâches ouvertes. Mais un modèle de langage ne se
connecte à rien : il produit du texte. Comment une suite de mots
déclenche-t-elle du code, et qui est responsable de ce qui s'exécute ?

Un **outil** (*tool*) est une fonction de votre application que vous décrivez
au modèle par un **contrat** : un nom, une description (quand s'en servir) et
le schéma JSON de ses arguments. Ce mécanisme s'appelle le **tool calling**
(ou *function calling*). Sa règle tient en une phrase : le modèle propose, le
code décide. Le modèle ne reçoit jamais le code de l'outil, ni l'accès à ce
qu'il touche. Anthropic l'écrit ainsi : « The model never runs anything on its
own » ([How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)) ;
la documentation de Spring AI parle d'une « critical security consideration »
([Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)).

Un appel d'outil se déroule en cinq temps :

1. L'application envoie la question de l'utilisateur et les contrats des
   outils disponibles.
2. Le modèle ne répond pas par un texte mais par une **demande d'appel** : un
   nom d'outil et des arguments.
3. L'application vérifie la demande (l'outil existe, les arguments sont
   valides, l'utilisateur a le droit) et, seulement alors, exécute la
   fonction.
4. L'application renvoie le résultat au modèle, dans un message dédié.
5. Le modèle rédige sa réponse, ou demande un autre appel (on y revient en
   S2.2 : c'est la boucle d'un agent).

<!-- Schéma à construire par l'équipe (FYC-60) : assets/appel-d-outil.png, structure proposée dans assets/appel-d-outil.mmd -->

Le modèle est comme un client qui remplit un bon de commande, et l'application
comme le magasinier qui contrôle le bon avant de sortir quoi que ce soit. La
limite de l'image : un client ne se laisse pas souffler son bon de commande par
une note qu'il vient de lire, alors qu'un modèle, si (séance 4).

Le contrat est lu par le modèle : c'est lui qui lui fait choisir l'outil et
ses arguments. Un nom sans ambiguïté, une description qui dit quand s'en
servir, peu d'outils : Anthropic détaille ces conseils dans
[Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents).
Chaque contrat est aussi envoyé à chaque appel, donc facturé en tokens.

**Mini-exercice (2 min).** Parmi les cinq temps, lesquels sont exécutés par le
modèle, lesquels par le code de NoteFlow ?

> **Réponse :** le modèle intervient aux temps 2 et 5 (il produit la demande,
> puis la réponse). Le code de NoteFlow intervient aux temps 1, 3 et 4 : il
> envoie, vérifie et exécute, renvoie le résultat. Rien de ce qui touche à la
> base de données n'est fait par le modèle.

### 1.3 Un outil entièrement écrit

Que devient ce contrat en code, et où se loge la décision ? Prenons l'outil
`lister_taches_ouvertes`, fourni dans le dépôt du TP
(`app/Application/Agent/Tools/ListerTachesOuvertes.php`, branche `fyc-tp-s2`).
Il a quatre temps. Le premier est le contrat :

```php
public function definition(): ToolDefinition
{
    return new ToolDefinition(
        name: 'lister_taches_ouvertes',
        description: 'Liste les tâches encore ouvertes, pour vérifier qu\'une tâche n\'existe pas déjà avant d\'en proposer une. '
            .'Ne renvoie que les tâches des projets de l\'utilisateur.',
        parameters: [
            'type' => 'object',
            'properties' => [
                'projet' => [
                    'type' => 'string',
                    'description' => 'Nom exact du projet pour filtrer. Facultatif.',
                ],
            ],
            'additionalProperties' => false,
        ],
    );
}
```

Les trois autres sont dans `run()`, que le code appelle après la demande du
modèle (si vous ne connaissez pas la validation de Laravel :
[Validation, Laravel 13.x](https://laravel.com/docs/13.x/validation)) :

```php
public function run(array $arguments, User $user): ToolResult
{
    // 2. Le code valide les arguments, même si le schéma les décrit.
    $validator = Validator::make($arguments, ['projet' => ['nullable', 'string', 'max:100']]);
    if ($validator->fails()) {
        throw InvalidToolArguments::fromValidator($validator);
    }

    // 3. Les droits sont dans la requête : seulement les projets de l'utilisateur.
    $taches = Task::query()
        ->where('status', Task::OPEN)
        ->whereIn('project_id', $user->readableProjectIds())
        ->limit(20)
        ->get();

    // 4. Un résultat court, avec ce dont le modèle a besoin et rien de plus.
    return ToolResult::ok(['taches' => $taches->map(fn (Task $t): array => [
        'id' => $t->id, 'titre' => $t->title, 'echeance' => $t->due_on?->format('Y-m-d'),
    ])->all()]);
}
```

(Extrait abrégé : le filtre par nom de projet est retiré.) L'utilisateur
courant arrive en argument de `run()`, fourni par le code. Il n'est jamais un
argument que le modèle remplit : le modèle ne choisit pas pour qui il travaille.

Reste à traiter la demande du modèle. Le code cherche l'outil dans une
liste blanche, l'appelle, et renvoie le résultat ou l'erreur :

```php
$tool = $toolbox->find($call->name);       // null si le modèle a inventé un nom

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

Une erreur n'arrête rien : elle repart au modèle comme un résultat, et il
corrige son appel au tour suivant. Voici l'échange pour la question « A-t-on
déjà une tâche pour le client pilote ? » (valeurs d'exemple) :

```text
demande du modèle :  lister_taches_ouvertes, {"projet": "Produit"}
résultat renvoyé  :  {"taches": [{"id": 7, "titre": "Relancer le client pilote",
                      "echeance": "2026-12-04"}]}
```

`$call` est un `ToolCall`, un type neutre. Chaque fournisseur a en effet son
format pour la même demande, et c'est l'adaptateur de la séance 1 qui le
traduit :

| Fournisseur | Demande d'appel | Résultat renvoyé |
|---|---|---|
| Mistral | `tool_calls` : identifiant, arguments en chaîne JSON | message `tool` avec `tool_call_id` |
| Ollama | `tool_calls` : arguments en objet, pas d'identifiant | message `role: "tool"` avec `tool_name` |
| Anthropic | bloc `tool_use` : identifiant, arguments en objet | bloc `tool_result` |

Sources : [Mistral](https://docs.mistral.ai/inference/conversations/function-calling),
[Ollama](https://docs.ollama.com/capabilities/tool-calling),
[Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works).
Le cœur métier ne manipule que le type neutre : un agent, trois fournisseurs.

**Piège.** On voit souvent faire confiance au schéma : « le modèle ne peut pas
envoyer autre chose, il est déclaré dans le contrat ». Le problème, c'est que le
schéma guide le modèle sans rien garantir. À la place : valider dans le code
comme au temps 2, et renvoyer un message d'erreur précis.

**Mini-exercice (3 min).** Dans le TP, vous écrirez `chercher_notes` sur ce
modèle. L'utilisateur courant doit-il être un argument de son contrat ?
Pourquoi ?

> **Réponse :** non. Un argument est rempli par le modèle, donc proposé, donc
> non fiable. L'identité de l'utilisateur est connue du code : elle arrive en
> paramètre de `run()`, et le filtre par droits se fait dans la requête.

### 1.4 Le même outil avec un SDK

Vous venez d'écrire à la main le contrat, la validation et le traitement de la
demande. Que fait un SDK à votre place, et que laisse-t-il à votre charge ?
Voici le même outil avec le [Laravel AI SDK](https://laravel.com/docs/ai-sdk)
(`laravel/ai`, extrait adapté de la documentation, non exécuté) :

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
        // Les droits de l'utilisateur : à vous de les appliquer ici.
        return json_encode($this->tachesOuvertes($valide['projet'] ?? null));
    }
}
```

Et avec [Spring AI](https://docs.spring.io/spring-ai/reference/api/tools.html),
où une annotation tient lieu de contrat :

```java
@Tool(description = "Liste les tâches encore ouvertes, pour éviter un doublon")
List<Tache> listerTachesOuvertes(
        @ToolParam(description = "Nom exact du projet", required = false) String projet) {
    return taches.ouvertes(projet);   // les droits : à vous
}
```

Dans les deux cas, le SDK construit le schéma JSON, envoie les contrats,
reconnaît la demande d'appel, appelle votre méthode et renvoie le résultat. Le
SDK de Laravel renvoie aussi les messages de validation au modèle pour qu'il
corrige son appel, comme le fait notre `InvalidToolArguments`. Il ne sait pas
en revanche ce que l'utilisateur a le droit de lire. Anthropic conseille de
commencer par l'API directe : les frameworks cachent les consignes et les
réponses échangées, et de fausses hypothèses sur leur fonctionnement sont une
source d'erreur fréquente
([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)).
D'où le TP sans SDK, et la comparaison ici.

**Mini-exercice (2 min).** Dans l'extrait Laravel, quelle ligne vérifie que
l'utilisateur a le droit de lire le projet demandé ?

> **Réponse :** aucune. `validate()` contrôle la forme des arguments, pas les
> droits. Le commentaire marque l'endroit où les appliquer, dans la requête,
> comme le fait `readableProjectIds()` dans la version écrite à la main.

### 1.5 Un outil est une porte : donner le minimum de droits

Un collègue propose d'ajouter à l'agent de NoteFlow l'outil
`executer_sql(requete)`, « pour qu'il réponde à toutes les questions ». Un
seul outil, aucune limite : c'est tentant. Quel est le prix ?

Chaque outil est une porte du modèle vers votre code métier. Si le modèle
produit un appel inattendu, parce qu'il se trompe ou parce qu'un texte lu
(une note, une page) l'a manipulé, ce que la porte laisse passer s'exécute.
OWASP appelle ce risque *Excessive Agency* (« délégation excessive »), n° 3
de son Top 10 pour les applications LLM 2026
([LLM03:2026](https://genai.owasp.org/llm2026/llm032026-excessive-agency/)).
Il a trois racines : trop de fonctionnalités, trop de permissions, trop
d'autonomie. D'où quatre habitudes à prendre dès le premier outil :

- **Peu d'outils, étroits.** `chercher_notes` plutôt que `executer_sql`.
  OWASP déconseille les outils ouverts (lancer une commande, lire une URL
  quelconque) : on en fait des outils plus précis.
- **Les droits de l'utilisateur courant, dans la requête.** L'agent ne voit
  que ce que l'utilisateur voit.
- **Chaque appel vérifié par le code.** OWASP parle de *complete mediation* :
  l'autorisation est décidée par la logique de l'application, jamais par le
  modèle.
- **Une action qui écrit demande l'accord de l'utilisateur**, qui voit
  l'action exacte (c'est le rôle de `creer_tache` dans le TP, voir S2.2).

**Piège.** On voit souvent écrire dans le prompt : « Ne lis jamais les notes du
projet Infra. » Le problème, c'est qu'une consigne n'est pas une barrière : le
modèle peut l'ignorer ou être manipulé. À la place : la requête ne renvoie
jamais ces notes, et le modèle ne peut pas lire ce que la base ne lui a pas
donné.

Ce n'est pas réglé pour autant : aucune défense connue ne rend un modèle
insensible à l'injection de prompt (OWASP écrit qu'il n'existe pas de
prévention fiable,
[LLM01:2026](https://genai.owasp.org/llm2026/llm012026-prompt-injection/)).
On limite donc ce qu'un modèle manipulé peut faire. Nous y revenons en séance 4.

**Mini-exercice (3 min).** On propose l'outil `lire_url(url)`, pour que l'agent
lise les liens collés dans les notes. Quelle racine de l'*Excessive Agency* est
en cause, et que répondez-vous ?

> **Réponse :** la fonctionnalité excessive. Une URL quelconque est un outil
> ouvert, que rien ne borne, et NoteFlow n'en a pas besoin pour son cas métier.
> On ne l'expose pas. Si le besoin devient réel, on propose un outil plus
> étroit (par exemple limité à une liste de domaines).

### 1.6 Encart : MCP, transporter les outils

Vous croiserez le **Model Context Protocol** (MCP) : un protocole ouvert qui
permet à une application d'exposer ses outils à d'autres applications, sans
réécrire le contrat pour chaque agent. Le modèle fait toujours du tool calling,
comme ci-dessus : MCP standardise seulement la découverte et le transport des
outils. Le Laravel AI SDK et Spring AI consomment des outils MCP avec la même
interface que les outils locaux (la documentation de Spring AI le dit en
toutes lettres). Donc MCP ne remplace pas votre contrat d'outil, il le
transporte : les règles de 1.5 s'appliquent aussi à un outil venu d'ailleurs.
Le protocole change vite : la révision en vigueur à la date d'écriture est la
[2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28),
vérifiez la version avant de suivre un tutoriel. Ce point est un
approfondissement : il n'est pas manipulé en TP ni évalué.

### 1.7 Ce qu'il faut retenir de S2.1

- Une sortie structurée donne la forme de la réponse. Le code vérifie le
  sens.
- Le modèle propose, le code décide : il valide les arguments, applique les
  droits de l'utilisateur, puis seulement exécute.
- Un outil étroit, aux droits de l'utilisateur courant, vaut mieux qu'un outil
  ouvert protégé par une consigne.

Un seul aller-retour ne fait pas un agent. La séquence S2.2 montre comment le
code rappelle le modèle tant qu'il demande des outils, et surtout quand il
doit s'arrêter.

<!-- Sections à venir : 2. Workflow ou agent ? La boucle et ses arrêts (S2.2, Timothé, FYC-52) ; 3. Récupérer l'information, et le mesurer (S2.3, Erwin). -->
