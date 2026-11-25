# Chapitre 01 : Les bases de l'architecture web, et pourquoi l'IA les bouscule

> Durée estimée : 2 h 15 (dont 1 h 20 de lecture et d'étude de cas, et 55 min de TP) · Objectifs : reconnaître les couches d'une application web et la place du cœur métier, isoler une dépendance externe derrière un port et y brancher trois adaptateurs (en ligne, local et doublure de test), nommer les cinq caractéristiques qui distinguent un agent IA d'un composant classique et en déduire les conséquences sur l'architecture.

Ce support couvre les séquences S1.1 et S1.2. Le TP de la séquence S1.3
(« un port, trois adaptateurs ») a son propre énoncé, dans le dépôt
[xKaan/fyc-tp](https://github.com/xKaan/fyc-tp) (branche `fyc-tp-s1`, corrigé
sur `fyc-tp-s1-correction`). L'installation de l'environnement (Ollama, Docker)
se fait avant, au chapitre 00.

## 1. Architectures web : les bases

### 1.1 Pourquoi on découpe en couches

Une application web reçoit des requêtes HTTP, fait quelque chose avec, et
renvoie des réponses. Tant qu'elle tient dans un fichier, personne ne se pose
la question de son organisation. Le problème arrive quand plusieurs personnes
la modifient, quand il faut la tester, ou quand une brique externe change.

La réponse classique est le **découpage en couches** : on range le code selon
sa responsabilité, et chaque couche ne parle qu'à ses voisines. Dans une
application Laravel, on retrouve presque toujours trois niveaux.

| Couche | Rôle | Dans Laravel |
|--------|------|--------------|
| Présentation | Recevoir la requête, valider les entrées, renvoyer la réponse | Routes, contrôleurs, _Form Requests_, ressources JSON |
| Application ou service | Enchaîner les étapes d'un cas d'usage | Classes de service, _actions_, _jobs_ |
| Domaine | Les règles du métier, indépendantes de tout framework | Entités, objets valeur, interfaces |

En dessous de ces trois couches, il y a l'**infrastructure** : base de données,
envoi d'e-mails, appels HTTP vers des services externes. C'est là que vivra
l'appel à une IA.

La règle qui compte : **les dépendances vont vers l'intérieur**. Le contrôleur
connaît le service, le service connaît le domaine, mais le domaine ne connaît
personne. Un objet métier ne sait pas qu'il existe une base de données, encore
moins un fournisseur d'IA.

```php
// app/Http/Controllers/NoteController.php : couche présentation
final class NoteController
{
    public function summarize(Note $note, SummarizeNote $summarizeNote): RedirectResponse
    {
        $summarizeNote($note);

        return redirect()->route('notes.show', $note)->with('status', 'Résumé généré.');
    }
}
```

Le contrôleur ne fait que traduire HTTP en appel de service, puis renvoyer
l'utilisateur sur la note avec un message. Laravel lui fournit la note,
retrouvée à partir de l'URL, et le service `SummarizeNote`, en paramètres de
la méthode. Le contrôleur ne contient aucune
règle métier. Si demain le résumé est déclenché par une commande Artisan au
lieu d'une requête HTTP, le service ne change pas.

### 1.2 Séparer les responsabilités

Le découpage en couches est une conséquence d'un principe plus général : la
**séparation des responsabilités**. Une classe a une raison de changer, et une
seule. Le contrôleur change si l'API HTTP change. Le service change si le cas
d'usage change. L'entité change si la règle métier change.

Le test le plus simple pour repérer une violation : essayer d'écrire un test
unitaire. Si tester une règle métier oblige à démarrer une base de données ou
à appeler un service externe, c'est que la règle est collée à son
infrastructure.

Voici un contrôleur qui échoue à ce test. C'est un extrait, simplifié, du code
de départ du TP S1.3.

```php
// Ce qu'on ne veut PAS : tout au même endroit
public function summarize($id, Request $request)
{
    $note = Note::where('id', $id)->first();

    if (env('LLM_PROVIDER', 'ollama') == 'http') {
        $reponse = Http::withToken(env('LLM_HTTP_API_KEY'))
            ->post('https://api.mistral.ai/v1/chat/completions', [
                'model' => 'mistral-small-latest',
                'messages' => [[
                    'role' => 'user',
                    'content' => "Résume la note suivante en 3 phrases maximum.\n\n"
                        .$note->title."\n".$note->content,
                ]],
            ]);
        $resume = $reponse->json()['choices'][0]['message']['content'];
    } else {
        // ... le même bloc, réécrit pour l'API d'Ollama
    }

    $note->summary = $resume;
    $note->save();

    return redirect('/notes/'.$id);
}
```

Tout y est mélangé : l'accès aux données, le choix du fournisseur, l'appel
HTTP, le prompt, le format de réponse propre à chaque fournisseur, et la
persistance. La consigne et le contenu de la note sont collés dans le même
message. Changer de fournisseur, tester le résumé sans réseau, ou réutiliser
le résumé ailleurs que dans une réponse HTTP, tout cela demande de réécrire la
méthode.

### 1.3 L'architecture hexagonale : ports et adaptateurs

L'**architecture hexagonale** pousse la séparation un cran plus loin. Elle
place le cœur métier au centre et le protège de tout ce qui est extérieur :
base de données, interface web, services distants. Le cœur ne parle au monde
extérieur qu'à travers des **ports**, c'est-à-dire des interfaces qu'il
définit lui-même. Chaque technologie concrète est branchée sur un port par un
**adaptateur**.

On distingue deux sortes de ports :

- Les **ports d'entrée** : ce que le cœur sait faire. Un cas d'usage comme
  « résumer une note » est un port d'entrée. Le contrôleur HTTP est un
  adaptateur qui l'appelle.
- Les **ports de sortie** : ce dont le cœur a besoin. « Obtenir une
  complétion de texte » est un port de sortie. La classe qui appelle l'API
  d'un fournisseur d'IA est un adaptateur qui l'implémente.

En PHP, un port est une interface :

```php
// app/Domain/Ports/LlmPort.php : port de sortie, défini par le cœur métier
interface LlmPort
{
    /**
     * @param non-empty-list<Message> $messages
     * @throws LlmCallFailed quelle que soit la cause de la panne
     */
    public function complete(array $messages): string;
}
```

Le port prend une liste de messages, chacun avec un rôle : la consigne de
l'application en rôle `system`, le texte fourni par l'utilisateur en rôle
`user`. C'est la forme commune aux API de modèles actuelles, et elle tiendra
jusqu'à la boucle d'agent de la séance 2, où l'historique et les résultats
d'outils s'ajouteront à la liste sans changer la signature. Mais `Message` est
un type de l'application, pas le tableau JSON d'un fournisseur :

```php
// app/Domain/Ports/Message.php : un message, dans le vocabulaire de l'application
final class Message
{
    private function __construct(
        public readonly Role $role,       // enum : System, User, Assistant
        public readonly string $content,
    ) {}

    public static function system(string $content): self { return new self(Role::System, $content); }
    public static function user(string $content): self { return new self(Role::User, $content); }
}
```

Et l'adaptateur est une classe d'infrastructure qui l'implémente :

```php
// app/Infrastructure/Llm/HttpLlmAdapter.php : adaptateur pour un fournisseur en ligne
final class HttpLlmAdapter implements LlmPort
{
    public function __construct(
        private readonly string $baseUrl,
        private readonly ?string $apiKey,
        private readonly string $model,
        private readonly int $timeout,
    ) {}

    public function complete(array $messages): string
    {
        $reponse = Http::timeout($this->timeout)
            ->when($this->apiKey, fn (PendingRequest $requete) => $requete->withToken($this->apiKey))
            ->post(rtrim($this->baseUrl, '/').'/chat/completions', [
                'model' => $this->model,
                'messages' => array_map(
                    fn (Message $m) => ['role' => $m->role->value, 'content' => $m->content],
                    $messages,
                ),
            ]);

        $texte = $reponse->json('choices.0.message.content');

        if ($reponse->failed() || ! is_string($texte)) {
            throw LlmCallFailed::rejected('http', $reponse->status());
        }

        return trim($texte);
    }
}
```

Tout ce qui est propre au fournisseur est ici : l'adresse `/chat/completions`,
la clé, le délai d'attente, la traduction des messages en JSON et le chemin du
texte dans la réponse. Une erreur HTTP ou une réponse de forme inattendue
devient une `LlmCallFailed`, l'exception du port : le reste de l'application
l'attrape sans rien savoir du fournisseur.

Le service métier ne connaît que l'interface :

```php
// app/Application/SummarizeNote.php : cas d'usage
final class SummarizeNote
{
    public function __construct(
        private readonly LlmPort $llm,
        private readonly Prompt $prompt,   // la consigne, lue dans un fichier versionné
    ) {}

    public function __invoke(Note $note): void
    {
        $note->summary = $this->llm->complete([
            Message::system($this->prompt->text),
            Message::user($note->title."\n".$note->content),
        ]);

        $note->save();
    }
}
```

La consigne et la note partent dans deux messages distincts. Ce n'est pas une
défense suffisante contre l'injection de prompt (séance 4), mais aucune
défense n'est possible sans cette séparation.

Vous remarquerez qu'il n'y a pas de port devant la base de données : le cas
d'usage manipule directement le modèle Eloquent `Note`. C'est un choix. L'IA
justifie un port : service externe, lent, faillible, facturé, remplaçable.
Eloquent est un choix stable du framework, déjà testable avec une base SQLite
en mémoire ; un port de plus coûterait des classes en double pour un bénéfice
nul ici. On pose un port là où l'instabilité et le coût de test le
justifient, pas partout.

Le branchement se fait dans le conteneur de dépendances de Laravel. C'est le
seul endroit qui connaît à la fois le port et les adaptateurs :

```php
// app/Providers/LlmServiceProvider.php
$this->app->bind(LlmPort::class, fn (): LlmPort => match (config('llm.provider')) {
    'fake' => new FakeLlmAdapter,
    'http' => new HttpLlmAdapter(
        config('llm.http.base_url'),
        config('llm.http.api_key'),
        config('llm.http.model'),
        config('llm.http.timeout'),
    ),
    'ollama' => new OllamaAdapter(
        config('llm.ollama.host'),
        config('llm.ollama.model'),
        config('llm.ollama.timeout'),
    ),
    default => throw new InvalidArgumentException('Fournisseur LLM inconnu : '.config('llm.provider')),
});
```

La valeur vient de `config/llm.php`, alimenté par la variable d'environnement
`LLM_PROVIDER`. Par défaut, elle vaut `fake` : la doublure `FakeLlmAdapter`
renvoie une réponse fixe sans aucune requête réseau, et l'application tourne
sans clé ni modèle local. Le même fichier épingle le modèle en ligne sur un
identifiant daté (`mistral-small-2603`), et non sur un alias comme
`mistral-small-latest`, qui change de modèle sans prévenir.

Changer de fournisseur, c'est changer une valeur de configuration. Tester
`SummarizeNote`, c'est lui passer la doublure et vérifier ce qu'elle a reçu.
Vous écrirez ces trois adaptateurs au TP S1.3, et la doublure servira dans
tous les tests du cours.

**Pour aller plus loin : le même principe en Java.** Dans Spring Boot, le port
est aussi une interface, l'adaptateur une classe annotée `@Component`, et le
branchement se fait par injection de dépendances avec `@ConditionalOnProperty`
ou un `@Bean` dans une classe de configuration. Le vocabulaire change, le
découpage est le même. C'est ce que montre la démo de S1.1 : le cœur métier
est identique dans les deux versions, seuls les adaptateurs et la façon de les
brancher diffèrent.

**Les dépôts d'exemple.** La démo s'appuie sur un même besoin métier, un petit
gestionnaire de notes en Markdown (arborescence, étiquettes, corbeille), codé
deux fois avec les mêmes couches :

- [notion-lite-laravel](https://github.com/sorantino/notion-lite-laravel) :
  la version de référence, à lancer et à explorer.
- [notion-lite-spring](https://github.com/sorantino/notion-lite-spring) : la
  même chose en Spring Boot, à lire seulement.

Le README de chaque dépôt range les fichiers en deux colonnes : ce qui vient du
framework, ce qui vient du métier. Comparez les deux dossiers du domaine : ils
ne contiennent aucune référence à Laravel ni à Spring, et leurs règles sont
identiques.

### 1.4 Pour aller plus loin : CQRS et événements

Deux notions complètent le tableau. Elles sont présentées ici parce que vous
les croiserez dans la littérature et dans les SDK, mais elles ne sont pas
manipulées dans ce cours.

**CQRS** (_Command Query Responsibility Segregation_, séparation des
responsabilités entre commandes et requêtes) sépare le code qui modifie l'état
(les commandes) de celui qui le lit (les requêtes). Une commande « résumer la
note 42 » et une requête « donner le résumé de la note 42 » passent par des
chemins différents, éventuellement avec des modèles de données différents.
Intérêt pour nous : une commande qui appelle une IA est lente et coûteuse,
une requête qui lit un résumé déjà calculé est instantanée. Les séparer permet
de traiter la première en arrière-plan.

Les **événements** permettent à une couche d'annoncer qu'il s'est passé quelque
chose (« la note 42 a été résumée ») sans savoir qui écoute. Laravel les
propose nativement. En séance 3, l'instrumentation de l'agent s'appuiera sur
ce mécanisme : chaque appel à l'IA émet un événement, et un écouteur mesure le
temps et le coût.

### 1.5 Ce qu'il faut retenir de S1.1

- Le cœur métier ne dépend d'aucune technologie. Les dépendances vont vers
  l'intérieur.
- Une dépendance externe se cache derrière un port (une interface) que le cœur
  définit, et se branche par un adaptateur.
- Le branchement est un détail de configuration, pas une décision prise dans
  le code métier.
- Le test unitaire est le juge de paix : si une règle ne se teste pas sans
  réseau ni base de données, elle est mal placée.

## 2. Pourquoi l'IA complique les architectures classiques

Avec l'architecture hexagonale, on pourrait croire que le sujet est clos : un
fournisseur d'IA est une dépendance externe, on le met derrière un port, et
on passe à autre chose. C'est vrai pour le branchement. C'est faux pour tout
le reste. Un agent IA a cinq caractéristiques qu'aucune base de données ni
aucun service de paiement ne présente ensemble.

### 2.1 Cinq caractéristiques et leurs conséquences

**Non-déterminisme.** Posez deux fois la même question à un modèle de langage,
vous obtiendrez deux réponses différentes. Même avec une température à zéro,
le fournisseur peut changer de version de modèle sans prévenir. Conséquence :
un test qui compare la réponse à une chaîne attendue échouera un jour sur
deux. Il faut tester autrement, c'est la séance 4.

**Latence variable et élevée.** Un appel à un modèle prend entre une et
trente secondes selon la longueur de la réponse, la charge du fournisseur et
le modèle choisi. Une requête SQL prend quelques millisecondes. Conséquence :
un appel à l'IA fait dans le fil d'une requête HTTP bloque un processus PHP
pendant tout ce temps. Avec quelques utilisateurs simultanés, le serveur ne
répond plus à personne.

**Coût par appel.** Chaque appel est facturé, en général au nombre de
_tokens_ (les morceaux de mots) envoyés et reçus. Une base de données ne
coûte rien de plus quand on l'interroge une fois de trop. Conséquence : une
boucle d'agent mal bornée, une politique de réessai naïve ou un utilisateur
malveillant peuvent faire exploser la facture sans qu'aucune erreur ne se
produise.

**Dépendance à un fournisseur externe.** Le modèle, sa disponibilité, ses
tarifs, ses conditions d'utilisation et ses mises à jour échappent à votre
équipe. Conséquence : une panne chez le fournisseur est une panne chez vous,
et une mise à jour du modèle est un déploiement que vous n'avez pas décidé.
Le fournisseur impose aussi des limites de débit, en requêtes et en tokens par
minute : au-delà, il refuse les appels (erreur 429), même quand tout va bien
chez lui. Il faut prévoir un plan de repli, c'est la séance 3.

**Nouvelle surface d'attaque.** Le modèle reçoit les instructions et les
données par le même canal, du texte. Il ne peut pas distinguer une consigne
de l'application d'une consigne glissée dans un document par un attaquant.
Conséquence : tout texte qui entre dans le contexte du modèle est une entrée
non fiable, y compris vos propres documents indexés. C'est la séance 4.

| Caractéristique | Ce qui casse si on l'ignore | Réponse du cours |
|-----------------|-----------------------------|------------------|
| Non-déterminisme | Tests fragiles, régressions invisibles | Doublures, jeu de référence (S4.1) |
| Latence | Workers bloqués, timeouts | Délais, traitement en arrière-plan, files (S3.1) |
| Coût | Facture imprévisible | Budget de l'agent, coupe-circuit, mesure du coût (S2.2, S3.2, S3.3) |
| Dépendance | Panne, limite de débit, changement subi | Adaptateurs, modèle épinglé, plan de repli (S1.3, S3.2, S5.1) |
| Surface d'attaque | Injection de prompt, fuite de données | Défense en couches (S4.2) |

### 2.2 Étude de cas : un appel d'IA dans un contrôleur

Reprenons le contrôleur fourre-tout de la section 1.2 et regardons ce qui se
passe quand on le déploie tel quel. Le scénario est celui d'une application
de prise de notes où un bouton « Résumer » appelle cette route.

**Lundi, 9 h.** Dix utilisateurs cliquent sur « Résumer » en même temps. Le
serveur PHP-FPM a huit processus. Chaque appel à l'IA dure huit secondes. Les
huit premiers processus sont occupés, les deux autres requêtes attendent. Un
onzième utilisateur veut simplement ouvrir la page d'accueil : il attend
aussi, parce qu'aucun processus n'est libre. Pour lui, le site est en panne.

**Lundi, 9 h 01.** Le fournisseur ralentit. Les appels prennent maintenant
plus d'une minute. L'équipe comptait sur le délai maximal de PHP
(`max_execution_time`, trente secondes) pour couper. Il ne coupe pas : sous
Linux, il ne compte que le temps passé à exécuter le script, pas le temps
passé à attendre le réseau. Ce qui coupe, c'est le client HTTP de Laravel :
sans consigne, il abandonne toute requête au bout de trente secondes et lève
une exception, d'où une erreur 500. Ce délai, personne ne l'a choisi, le
contrôleur en hérite du framework. Si un proxy plus pressé est placé devant
(nginx attend soixante secondes par défaut, un répartiteur de charge parfois
moins), c'est lui qui renvoie une erreur 504 en premier, pendant que le
processus PHP continue d'attendre un fournisseur que plus personne n'écoute.
Dans tous les cas, l'appel vers le fournisseur a bien été envoyé et sera
probablement facturé, selon le fournisseur, même si personne n'attend plus la
réponse. Les utilisateurs recliquent. Chaque clic relance un appel qui
échouera et peut être facturé.

Ces deux premiers incidents se reproduisent sur votre machine : le dossier
`etude/` de la branche `fyc-etude-s1-2` du dépôt
[xKaan/fyc-tp](https://github.com/xKaan/fyc-tp/tree/fyc-etude-s1-2/etude)
fait tourner ce contrôleur derrière nginx et huit processus PHP-FPM, face à un
faux fournisseur dont on règle la lenteur. La vidéo « Le timeout réel d'un
appel d'IA dans un contrôleur » en montre l'exécution.

**Lundi, 9 h 05.** Un utilisateur colle dans une note un document de deux
cents pages, puis clique sur « Résumer ». Le corps de la note part en entier
dans le prompt. Cet appel coûte cent fois plus que les autres. Rien dans le
code ne l'a empêché.

**Mardi.** Le fournisseur déploie une nouvelle version du modèle. Les résumés
sont maintenant en anglais une fois sur cinq. Aucun commit n'a été fait, aucun
test n'a échoué, aucun log ne montre d'erreur. Ce sont les utilisateurs qui
signalent le problème.

Chacun de ces incidents correspond à une des cinq caractéristiques. Aucun
n'est un bug au sens habituel : le code fait exactement ce qu'il dit. C'est
l'architecture qui n'a pas prévu le comportement de la dépendance.

### 2.3 Les points de rupture à repérer

Dans l'étude de cas, cherchez les endroits où le code prend une décision
implicite qu'il ne devrait pas prendre :

- **L'appel est synchrone.** Le contrôleur attend la réponse. C'est le point
  de rupture de 9 h.
- **Aucune limite de temps n'est choisie pour l'appel lui-même.** Le délai de
  PHP ne compte pas l'attente réseau. Ce qui coupe, ce sont des délais posés
  par d'autres couches (le client HTTP du framework, le serveur web, le
  proxy), sans rapport avec le temps qu'un utilisateur accepte d'attendre, et
  l'appel est probablement facturé. C'est le point de rupture de 9 h 01.
- **Aucune limite de taille ni de coût.** Le prompt contient tout ce que
  l'utilisateur a saisi. C'est le point de rupture de 9 h 05.
- **Le modèle n'est pas figé.** Le code dit `mistral-small-latest`, un alias :
  c'est le fournisseur qui décide du modèle que ce nom désigne. C'est le point
  de rupture de mardi.
- **Rien n'est mesuré.** Ni durée, ni coût, ni taux d'échec. On découvre les
  problèmes par les plaintes.

Vous allez maintenant proposer des parades dans la fiche de réponse de
l'exercice 1 de ce chapitre. Ne cherchez pas la solution parfaite : en
séance 3, vous construirez ces parades une par une. L'objectif ici est de
relier chaque point de rupture à une famille de solutions.

### 2.4 Ce qu'il faut retenir de S1.2

- Un agent IA se branche comme une dépendance ordinaire, mais ne se comporte
  pas comme une dépendance ordinaire.
- Non-déterminisme, latence, coût, dépendance au fournisseur et surface
  d'attaque : chaque caractéristique casse quelque chose de précis si on
  l'ignore.
- Le contrôleur fourre-tout n'a pas de bug. Il a une architecture qui suppose
  une dépendance rapide, gratuite, fiable et prévisible. Aucune de ces
  hypothèses ne tient.
- Le reste du cours construit, séance après séance, les réponses à chacune de
  ces caractéristiques.
