# Vidéo : Lecture guidée des deux dépôts : Laravel et Spring Boot

- Durée cible : environ 3 à 4 min (budget de 5 min dans `livrables/budget-video.md`, limite FYC : 8 min). Elle précède 5 min de lecture autonome.
- Intervenant : Quentin Bauduin, voix sur écran, pas de face caméra. Ton : celui d'un collègue qui montre son écran, calme, sans effet de présentation.
- Format : screencast, police 18 pt au moins, thème contrasté, une seule fenêtre à la fois (deux fenêtres côte à côte quand le script le dit). Actions et incrustations entre crochets, elles ne se lisent pas.
- Mots : 281 (140 mots par minute). La voix tient en 120 secondes, le reste est de la lecture de code.
- Place dans le parcours : S1.1, dernière étape (10 min : 5 min de vidéo, 5 min de lecture), après le support écrit. L'apprenant a lu les sections 1.1 à 1.4 : couches, port, adaptateur, branchement par la configuration, et la section 1.4 lui a annoncé la comparaison avec Spring. Il connaît PHP et Laravel, pas forcément Java : la vidéo le dit et ne lui demande pas de lire du Java en détail. Il n'y a pas de TP Spring.
- Ce que le spectateur doit retenir : le cœur du métier est le même d'un framework à l'autre, seuls les adaptateurs et la façon de les brancher changent. Il repart avec une méthode : chercher le framework dans le domaine, et classer chaque différence en « framework » ou « métier ».
- Source : les dépôts de Timothé ([sorantino/notion-lite-laravel](https://github.com/sorantino/notion-lite-laravel) et [sorantino/notion-lite-spring](https://github.com/sorantino/notion-lite-spring), branches `main`). Vérifié sur les deux dépôts clonés pour ce script : `grep -rn Illuminate app/Domain` ne renvoie rien, aucun import `springframework` ni `jakarta` dans le package `domain` de Spring, mêmes constantes (120) et mêmes messages d'erreur dans `NoteTitle` et `NoteRuleViolation`, `SummarizeNote` identique dans les étapes avec `@Service` et `@Transactional` en plus côté Spring, `match` dans `AppServiceProvider` côté Laravel et `@ConditionalOnProperty` sur chaque adaptateur côté Spring. Les noms de fichiers à l'écran sont à revérifier si les dépôts bougent avant le tournage.

## Script

[Écran : deux éditeurs côte à côte, `notion-lite-laravel` à gauche, `notion-lite-spring` à droite, arborescences dépliées jusqu'au dossier du domaine]

Même gestionnaire de notes, écrit deux fois : en Laravel, et en Spring Boot. Vous n'avez pas besoin de savoir lire du Java. On cherche une seule chose : ce qui appartient au framework, et ce qui appartient au métier.

Avant de regarder, faites une prédiction. Si j'ouvre le dossier du domaine dans les deux projets, qu'est-ce qui va changer ?

[Écran : silence de 5 secondes, les deux dossiers du domaine à l'écran]

[Écran : `NoteTitle.php` à gauche, `NoteTitle.java` à droite, la constante 120 surlignée, puis les deux messages d'erreur]

Presque rien. La syntaxe, bien sûr. Mais la règle est la même : un titre est obligatoire, cent vingt caractères au plus, et le message d'erreur est mot pour mot le même.

[Terminal à gauche : `grep -rn Illuminate app/Domain`. Terminal à droite : `grep -rn "springframework\|jakarta" src/main/java/com/example/notionlite/domain`. Aucune sortie des deux côtés, laisser 3 secondes]

Pour le vérifier, on cherche le framework dans le domaine. Dans Laravel, rien. Dans Spring, rien non plus. Le domaine ne sait pas dans quel framework il tourne.

[Écran : `SummarizeNote.php` et `SummarizeNote.java` côte à côte, les deux annotations `@Service` et `@Transactional` surlignées à droite]

Le cas d'usage « résumer une note » est construit de la même façon : il reçoit le dépôt de notes et le port vers l'IA, il retrouve la note, demande le résumé et l'enregistre. La seule différence visible, ce sont deux annotations de Spring au-dessus de la classe. En PHP, la classe ne contient aucune ligne du framework.

[Écran : `AppServiceProvider.php`, le `match` sur `config('llm.provider')`, puis `OllamaAdapter.java`, l'annotation `@ConditionalOnProperty`]

Là où ça diffère vraiment, c'est le branchement. Laravel choisit l'adaptateur à un seul endroit, un `match` dans le fournisseur de services. Spring le déclare sur chaque adaptateur, avec une annotation qui dit « j'existe seulement si le fournisseur configuré est celui-ci ». Deux mécaniques, une même idée : le choix vit dans la configuration, pas dans le métier.

[Écran : le tableau « Ce qui change d'un framework à l'autre… et ce qui ne change pas » du README Spring, dernière ligne surlignée]

Ce tableau résume tout. Sa dernière ligne dit l'essentiel : les règles métier sont identiques.

À vous. Cinq minutes : ouvrez les deux dépôts, parcourez ce tableau, et notez trois différences. Pour chacune, demandez-vous si elle vient du framework ou du métier.

## Plan de montage

| Temps | Plan | Écran |
|-------|------|-------|
| 0:00 | Screencast | Deux éditeurs côte à côte, arborescences dépliées jusqu'au domaine |
| 0:30 | Screencast | Silence de 5 s sur les deux dossiers du domaine |
| 0:35 | Screencast | `NoteTitle.php` et `NoteTitle.java`, constante 120 surlignée, puis les deux messages d'erreur |
| 0:55 | Screencast | Deux terminaux, les deux `grep` sans sortie, laisser 3 s |
| 1:16 | Screencast | `SummarizeNote.php` et `.java` côte à côte, `@Service` et `@Transactional` surlignés |
| 1:52 | Screencast | `AppServiceProvider.php` (le `match`), puis `OllamaAdapter.java` (`@ConditionalOnProperty`) |
| 2:32 | Incrustation | Tableau du README Spring, dernière ligne surlignée |
| 2:47 | Carton | « À vous : trois différences, framework ou métier ? » |

## À faire au tournage

- Prérequis : les deux dépôts clonés, ouverts dans deux fenêtres. Rien à lancer : on ne montre que du code et deux commandes `grep`. Vérifier que les deux `grep` sont vides au moment de la prise (le dépôt Laravel contient bien `Illuminate` dans `app/Application/NoteService.php` pour `DB::transaction`, hors du domaine : ne pas chercher dans `app/` en entier).
- Ne pas expliquer la syntaxe Java : dire « vous n'avez pas besoin de savoir lire du Java » est dans le script, et on s'y tient.
- Relire à voix haute en chronométrant. Toute phrase où l'on bute est réécrite.

Sous-titres : vérifier les noms propres et le code lu à voix haute dans la transcription automatique.

Minutages calés sur 140 mots par minute et sur des temps d'écran estimés : à recaler sur la première prise.
