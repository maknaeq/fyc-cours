# Thème D : tester, évaluer, observer et exploiter en production un système à base de LLM

Référence pour l'agent « prof » du cours FYC (ESGI). Séquences concernées : S3.2, S3.3, S4.1, S4.4, S5.1, S5.2.
Toutes les sources listées en section 4 ont été ouvertes et lues le 24/11/2026. Les numéros entre crochets renvoient à la section 4.

---

## 1. Savoir de référence

**D1. Séparer le prévisible de l'imprévisible, et tester le prévisible comme d'habitude.** Le code autour du modèle (adaptateur, contrat d'outil, boucle d'agent, retry, découpage RAG, calcul de coût) se teste de façon déterministe, avec une doublure du fournisseur. Google le formulait dès ses « Rules of ML » : encapsuler la partie apprise pour pouvoir tester toute l'infrastructure qui l'entoure (règle 5) [13]. Sculley et al. rappellent que le code ML n'est qu'une petite partie d'un système dont la dette se loge dans la colle, la configuration et les dépendances externes [12]. Conséquence pour S4.1 : la pyramide de tests reste valable pour 90 % du code ; seule la pointe (qualité de la réponse) demande des evals. [12][13]

**D2. Une doublure de fournisseur est un test de contrat, pas un test de qualité.** Écrire son propre fake (une implémentation de l'interface d'adaptateur qui renvoie des réponses scriptées, y compris des appels d'outils, des erreurs 429/503 et des réponses malformées) permet de tester la boucle d'agent, le retry et le mode dégradé sans réseau ni facture. Le Laravel AI SDK fournit exactement cela : `Agent::fake()` (réponses fixes, liste ordonnée ou closure selon le prompt), génération automatique de données conformes au schéma pour la sortie structurée, assertions `assertPrompted`, `assertPromptedTimes`, `assertNeverPrompted`, `assertQueued`, et `preventStrayPrompts()` qui fait échouer le test si un appel n'a pas de réponse simulée [20]. Le parallèle pédagogique (« ce que vous venez d'écrire, le SDK le fait ») est donc juste. Spring AI ne fournit pas de fake équivalent dans sa doc d'évaluation ; son « Evaluator API » (`RelevancyEvaluator`, `FactCheckingEvaluator`) relève de l'IA-juge, pas de la doublure [19]. [19][20]

**D3. Température 0 ne veut pas dire déterministe.** Même à température 0, les API de LLM ne sont pas reproductibles en pratique : Thinking Machines a obtenu 80 complétions distinctes sur 1 000 tirages à température 0 du même prompt, la cause principale étant l'absence d'« invariance au lot » des noyaux d'inférence (la sortie dépend de la charge des autres utilisateurs) [16]. Donc : aucune assertion d'égalité exacte sur un texte généré dans un test qui appelle un vrai modèle ; on vérifie des propriétés (format JSON valide, champ obligatoire présent, pas d'UUID ni de placeholder `{{...}}` dans la réponse, outil attendu appelé, refus présent) [1][24]. [1][16][24]

**D4. Les tests de propriétés et d'invariants sont le premier niveau d'eval, et le moins cher.** Husain appelle ces assertions le « niveau 1 » : des tests à portée limitée, écrits à partir des échecs réellement observés (exemple Rechat : une regex qui vérifie qu'aucun UUID interne n'apparaît dans la réponse), au nombre de plusieurs centaines dans un produit mûr [1][24]. La FAQ de Husain et Shankar insiste : si une regex ou une assertion attrape l'échec, c'est presque toujours rentable ; un juge LLM coûte 100+ exemples étiquetés et une maintenance hebdomadaire [2]. Anthropic recommande aussi des « graders » déterministes partout où c'est possible, des graders LLM seulement là où c'est nécessaire [9]. [1][2][9][24]

**D5. Le jeu de tests de référence (golden dataset) naît de l'analyse d'erreurs, pas d'une liste imaginée.** La démarche recommandée par Husain et Shankar : lire une centaine de traces variées, annoter soi-même au moins les 30 premières, regrouper les échecs en catégories (codage ouvert puis axial), puis seulement écrire les évaluateurs [2][25]. Anthropic : 20 à 50 tâches simples tirées d'échecs réels suffisent pour démarrer, une bonne tâche est une tâche sur laquelle deux experts donneraient indépendamment le même verdict, et un taux de 0 % sur de nombreux essais signale le plus souvent une tâche mal spécifiée plutôt qu'un agent incapable [9]. Les cas doivent couvrir le cas normal, les cas limites et les cas adverses (dont injections) et refléter la distribution réelle du trafic, sinon c'est un « biased design » selon OpenAI [10]. Pour les « 10 cas » de S4.1, c'est un bon début si chacun est rattaché à un échec observé ou à une exigence explicite. [2][9][10][25]

**D6. Préférer des verdicts binaires et un évaluateur par dimension.** Les échelles 1-5 sont difficiles à calibrer pour les humains comme pour les juges LLM (« qu'est-ce qui distingue un 3 d'un 4 ? ») ; Husain et Yan recommandent pass/fail (ou gagné/perdu/égalité pour les comparaisons) et déconseillent le « God Evaluator » qui note 5 à 10 dimensions dans un seul prompt [3][7]. Anthropic recommande aussi un juge isolé par dimension et une porte de sortie « Unknown » pour limiter les hallucinations du juge [9]. Les métriques génériques (ROUGE, BERTScore, similarité cosinus) sont jugées peu utiles pour la plupart des applications [2], et OpenAI les classe parmi les anti-patterns quand on s'appuie uniquement sur elles [10]. [2][3][7][9][10]

**D7. LLM-as-judge : utile, biaisé, à valider comme n'importe quel classifieur.** Zheng et al. (NeurIPS 2023) montrent qu'un juge fort atteint plus de 80 % d'accord avec les préférences humaines, soit le niveau d'accord entre humains, mais documentent les biais de position, de verbosité et d'auto-préférence (self-enhancement) ainsi que des limites de raisonnement [5]. Thoughtworks a fait reculer la technique de « Trial » à « Assess » en novembre 2025 à cause de ces biais et du risque de contamination quand le juge sert aussi à l'entraînement, et recommande une vérification humaine avant tout usage critique [11]. Pratiques de calibrage : séparer exemples d'alignement et de test (par exemple 75/25), mesurer précision/rappel (ou TPR/TNR) et kappa de Cohen contre des étiquettes humaines, viser au moins 50 à 100 cas d'échec sur 200+, inverser l'ordre des réponses dans les comparaisons pour neutraliser le biais de position [2][3][7]. Utiliser un modèle différent de celui évalué limite l'auto-préférence ; l'auto-évaluation est déconseillée [14]. Pour un panorama des variantes (comparaison par paires, juges affinés, critiques de la méthode), voir Yan [6]. [2][3][5][6][7][11][14]

**D8. « Who validates the validators? » : les critères bougent quand on regarde les sorties.** Shankar et al. (UIST 2024) ont observé la « dérive des critères » : on a besoin de critères pour noter les sorties, mais c'est en notant les sorties qu'on définit les critères ; certains critères dépendent des sorties observées et ne peuvent pas être fixés a priori [4]. Conséquence pédagogique : la grille d'évaluation et le jeu de référence sont des artefacts vivants, versionnés, révisés après chaque série d'annotation. Chip Huyen ajoute qu'un juge IA est lui-même itéré, donc ses scores ne sont pas comparables dans le temps si le juge change : il faut versionner le prompt et le modèle du juge [8]. [4][8]

**D9. Mesurer la variabilité : pass@k et pass^k, et des intervalles de confiance.** Anthropic distingue pass@k (au moins un succès sur k essais) et pass^k (k succès sur k) : avec 75 % de réussite par essai, la probabilité de réussir 3 fois sur 3 n'est que d'environ 42 % ; pour un agent face à des clients, c'est pass^k qui compte [9]. Yan rappelle l'ordre de grandeur statistique : 3 % de défauts observés sur 200 cas donne un intervalle d'environ ±2,4 points, et il faut quadrupler l'échantillon pour diviser la marge par deux [7]. Une « marge de tolérance » (S4.1) doit donc être exprimée en taux sur N cas et N essais, pas sur un seul passage. [7][9]

**D10. Evals de capacité et evals de non-régression : deux suites, deux rôles.** Les evals de capacité partent d'un taux bas et mesurent la progression ; les evals de régression doivent rester proches de 100 % et toute baisse signale une casse ; une eval de capacité qui atteint un taux élevé « gradue » en suite de régression [9]. Noter le chemin exact (ordre précis des appels d'outils) rend les tests fragiles : mieux vaut noter le résultat (état final, par exemple la réservation existe en base) que le chemin [9]. C'est directement applicable aux tests d'injection de S4.4 : vérifier l'effet (aucun outil sensible appelé, aucune donnée exfiltrée) plutôt que la formulation de la réponse. [9]

**D11. CI en deux étages : déterministe et bloquant à chaque commit, evals coûteuses à côté.** La FAQ Husain-Shankar : en CI, un petit jeu ciblé (souvent une centaine de cas : fonctionnalités cœur, régressions de bugs passés, cas limites connus), avec des assertions de préférence aux juges LLM parce que le coût par exécution compte ; en production, échantillonnage de traces et juges validés [2]. Fowler/Subramaniam : les evals tournent dans le pipeline mais ne sont pas binaires, on fixe des seuils et on surveille la baisse, « comme des tests de performance » [14]. Mise en œuvre GitHub Actions : étage 1 sur `push`/`pull_request` avec le fake (sans secret) ; étage 2 sur `schedule`, `workflow_dispatch` ou étiquette de PR. Pièges documentés : un `schedule` peut être retardé voire abandonné en période de forte charge (notamment en début d'heure), ne tourne que sur la branche par défaut, est désactivé après 60 jours d'inactivité dans un dépôt public ; et les secrets (clé d'API) ne sont pas transmis aux workflows déclenchés depuis un fork [22]. [2][14][22]

**D12. Observer un agent : une trace par requête, un span par appel modèle, par outil, par recherche.** Les conventions sémantiques OpenTelemetry GenAI définissent des spans d'inférence (nom `{gen_ai.operation.name} {gen_ai.request.model}`, par exemple `chat ...`), d'embeddings, de recherche (retrieval), d'exécution d'outil (`execute_tool {gen_ai.tool.name}`, span INTERNAL) et d'agent (`invoke_agent`) [17]. Attributs clés : `gen_ai.provider.name`, `gen_ai.request.model` et `gen_ai.response.model` (les deux, car le modèle réellement servi peut différer), `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, tokens de cache lus/écrits et tokens de raisonnement, `gen_ai.response.finish_reasons`, `gen_ai.conversation.id`, et désormais `gen_ai.prompt.name` / `gen_ai.prompt.version` pour relier une trace à une version de prompt [17]. Un span couvre l'opération logique, retries automatiques inclus [17]. En Laravel sans SDK, cela se traduit par un identifiant de requête propagé (contexte de log) et un événement/log structuré par étape ; avec le SDK, les événements `PromptingAgent`, `AgentPrompted`, `InvokingTool`, `ToolInvoked`, `StepCompleted`, `ProviderFailedOver`, `AgentFailedOver` servent de points d'accroche [20]. [17][20]

**D13. Statut des conventions OTel GenAI au 24/11/2026 : en développement, et déplacées.** Les conventions GenAI ont quitté le dépôt principal `open-telemetry/semantic-conventions` (la page y indique « has moved and is no longer maintained ») pour un dépôt dédié `open-telemetry/semantic-conventions-genai`, créé le 05/05/2026 ; tous les documents restent au statut « Development » [17]. Les noms bougent : les métriques de tokens d'inférence sont maintenant `gen_ai.client.inference.usage.input_tokens`, `...output_tokens`, etc., alors que Spring AI 2.1.0 et le billet OTel de mai 2026 utilisent encore `gen_ai.client.token.usage` et l'attribut `gen_ai.system` (remplacé par `gen_ai.provider.name`) [18][19]. À enseigner comme un vocabulaire de référence, pas comme un standard figé ; l'URL de la bibliographie actuelle (dépôt `semantic-conventions-genai`) est correcte. [17][18][19]

**D14. Le contenu des prompts n'est pas journalisé par défaut, et c'est voulu.** Dans OTel GenAI, `gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions` et les arguments/résultats d'outils sont « Opt-In » ; par défaut seuls les métadonnées (modèle, tokens, durées) sont capturées, car le contenu peut être sensible [17][18]. Spring AI 2.1.0 a `log-prompt` et `log-completion` à `false` par défaut et avertit du risque d'exposition de données [19]. Cela rejoint S5.2 (ce qui part dans le contexte quitte l'entreprise) : journaliser le contenu doit être une décision explicite, avec durée de rétention et masquage. [17][18][19]

**D15. Le coût par requête se calcule à partir des tokens par catégorie, pas du total.** Le Laravel AI SDK expose `usage->inputTokens`, `outputTokens`, et pour le texte `cacheReadInputTokens`, `cacheWriteInputTokens`, `reasoningTokens` et `uncachedInputTokens()` ; la doc précise que lectures de cache, écritures de cache et entrées non cachées sont facturées à des tarifs différents et doivent être valorisées séparément, et que les compteurs non fournis valent `null`, pas `0` [20]. OTel recommande d'agréger la consommation via les métriques (non affectées par l'échantillonnage des traces) et présente les compteurs de tokens comme une approximation du coût [17]. Anthropic note qu'une banque de tâches fixe donne « gratuitement » des lignes de base de latence, tokens, coût par tâche et taux d'erreur [9]. [9][17][20]

**D16. Une mise à jour du modèle est un déploiement que l'on ne contrôle pas : épingler, mais savoir ce que l'épinglage garantit.** Chen, Zaharia et Zou ont mesuré que GPT-4 « mars 2023 » et « juin 2023 » différaient fortement (84 % contre 51 % sur l'identification des nombres premiers), concluant à la nécessité d'une surveillance continue [15]. Chez Anthropic, depuis la génération 4.6, les identifiants sans date (`claude-sonnet-4-6`, `claude-opus-5`) sont des instantanés figés, pas des alias évolutifs ; les alias des générations antérieures (`claude-sonnet-4-5`) pointent, eux, vers le dernier instantané daté [23]. Même à identifiant constant, l'infrastructure de service (routeur, classifieurs de sécurité, échantillonnage) peut changer et produire de petites différences, et chaque modèle a une date de retrait (préavis d'au moins 60 jours pour les modèles publics) après laquelle les requêtes échouent [23]. Donc : épingler est nécessaire mais pas suffisant ; il faut une eval de migration prête et une surveillance. [15][23]

**D17. Versionner le prompt comme du code, et le relier aux traces.** Le prompt, les paramètres (modèle, température, outils exposés) et le prompt du juge font partie de la configuration à versionner ; Sculley et al. classent la configuration parmi les principales sources de dette des systèmes ML [12]. Les outils de gestion de prompts (exemple Langfuse : versions numérotées automatiquement, étiquettes `production`/`staging` pour promouvoir une version) offrent un modèle mental utile, mais un dépôt Git avec des fichiers de prompt et un identifiant de version propagé dans `gen_ai.prompt.version` suffit pour le cours [17] (Langfuse : voir le complément en fin de section 4). Prudence : Langfuse est un produit commercial (open source avec offre payante), à citer comme exemple, pas comme prescription. [12][17]

**D18. Détecter la dérive : distinguer incident ponctuel et dégradation lente.** Rule of ML n°10 : les systèmes ML échouent silencieusement et se dégradent progressivement (exemple Google Play : une table restée périmée 6 mois) ; suivre des statistiques sur les données et inspecter régulièrement à la main [13]. Pour un LLM, on surveille : taux de réussite des assertions en production, taux de recours au plan de secours, taux de refus, coût et tokens par requête, latence p95, retours utilisateurs, et un échantillon hebdomadaire de traces lu par un humain [9][2]. Anthropic résume la combinaison par le modèle du « gruyère suisse » : evals automatiques avant mise en prod et en CI, surveillance de production pour la dérive de distribution, tests A/B, retours utilisateurs et relecture humaine périodique pour calibrer les juges [9]. [2][9][13]

**D19. Les plateformes d'evals des fournisseurs sont volatiles : enseigner la méthode, pas l'outil.** OpenAI déprécie sa plateforme Evals (tableau de bord, API et graders) : lecture seule au 31/10/2026, fermeture le 30/11/2026, avec migration conseillée vers Promptfoo [10]. Tout support de cours qui renverrait vers l'Evals API d'OpenAI comme outil de TP serait obsolète dans la semaine. La FAQ Husain-Shankar et le billet fondateur de Husain recommandent d'ailleurs de commencer avec ce qu'on a déjà (tests unitaires, base de données, tableur, tableau de bord) avant d'acheter un outil [1][2][24]. [1][2][10][24]

**D20. Déployer Laravel avec ses workers : timeouts, retries, redémarrage.** Les workers de file sont des processus longue durée qui ne voient pas le nouveau code : redémarrage gracieux avec `php artisan queue:restart` (ou `horizon:terminate` avec Horizon), ou depuis Laravel 13 la commande unique `php artisan reload` qui termine workers, Reverb et Octane, un gestionnaire de processus (Supervisor) les relançant [21]. Le `timeout` d'un job doit être inférieur à `retry_after` (90 s par défaut pour Redis dans la config), sinon le job peut être exécuté deux fois : avec un appel LLM payant, cela double la facture et peut doubler une action d'outil [21]. Toujours fixer aussi un timeout côté client HTTP (Guzzle), car les E/S bloquantes peuvent ignorer le timeout du worker [21]. Autres points : `#[Tries]`, `#[Backoff([10, 30, 60])]`, `#[FailOnTimeout]`, `--max-jobs`/`--max-time` pour recycler les workers, `php artisan optimize` au déploiement, route de santé `/up` et événement `DiagnosingHealth` [21]. [21]

**D21. Versions à jour au 24/11/2026 (à corriger dans la bibliographie du cours).** `laravel/ai` n'est plus en 0.x : v1.0.0 publiée le 23/09/2026, v1.4.2 le 24/11/2026 (API GitHub releases) [20]. Laravel framework : v13.44.1 (24/11/2026). Spring AI : la doc de référence affiche 2.1.0 (la bibliographie cite 2.0.1) [19]. OTel GenAI : dépôt dédié, statut Development [17]. OpenAI Evals : fermeture le 30/11/2026 [10]. [10][17][19][20]

---

## 2. Ordre d'enseignement recommandé

### Ordre proposé pour les notions du thème D

1. **Mesurer avant de juger (S3.2 avant S4.1).** Traces et logs structurés d'abord, evals ensuite : l'analyse d'erreurs, point de départ de tout jeu de référence, consiste à lire des traces [2][25]. L'ordre du cours (observabilité en séance 3, tests en séance 4) est donc cohérent avec Husain-Shankar, à condition d'expliciter en S4.1 que le jeu de référence se construit à partir des traces produites en S3.3.
2. **Doublure et tests déterministes très tôt, pas seulement en S4.1.** Rules of ML n°5 et la pratique Laravel (`Agent::fake()`) poussent à tester l'infrastructure indépendamment du modèle dès qu'on écrit l'adaptateur [13][20]. Recommandation : introduire un fake minimal dès la séance 1 ou 2 (quand l'adaptateur et la boucle d'agent sont écrits), puis en S4.1 le formaliser et le comparer au SDK. Sinon les TP S2 et S3 (dont la panne simulée) sont testés à la main.
3. **Versionnement du prompt et épinglage du modèle avant l'instrumentation.** Pour qu'une trace de S3.2 soit exploitable, elle doit porter le modèle demandé, le modèle servi et la version du prompt [17]. S5.1 peut approfondir (migration, dépréciation), mais la règle « prompt dans un fichier versionné + identifiant de modèle épinglé en config » devrait apparaître dès la séance 2.
4. **Dans S4.1 : assertions et propriétés, puis jeu de référence, puis juge, puis dérive.** C'est l'ordre de coût croissant de la FAQ [2], de Husain (niveau 1 avant niveau 2) [1] et d'Anthropic (graders déterministes d'abord) [9]. Le juge LLM ne vient qu'une fois qu'on dispose d'étiquettes humaines pour le valider [3][7]. Le scénario actuel (IA-juge et dérive sémantique en approfondissement, non évalués) est conforme.
5. **S4.4 avant S5.2 : mesurer la durée de la suite avant de concevoir la CI.** Déjà prévu ; c'est la bonne dépendance (la CI à deux étages se justifie par le coût et la durée mesurés).
6. **S5.1 (production) : surveillance et dérive après les evals.** Les evals hors ligne deviennent la suite de régression, la surveillance de production prend le relais pour la dérive de distribution [9].

### Comparaison avec 3 références

| Référence | Ordre proposé | Ce qui converge avec le cours | Écart à signaler |
|---|---|---|---|
| Husain et Shankar, FAQ et cours « AI Evals » [2][3][25] | Analyse d'erreurs sur traces, puis évaluateurs (code d'abord, juge ensuite, validé contre humains), puis CI et surveillance | Traces avant evals, juge en dernier | Insistent sur l'annotation humaine (au moins 30 traces lues soi-même) : absente du scénario S4.1, à ajouter en 5 min |
| Anthropic, « Demystifying evals for AI agents » [9] | Commencer par ce qu'on teste à la main (20-50 tâches), tâches non ambiguës avec solution de référence, harnais isolé, graders, lecture des transcripts, puis surveillance de prod | Petits jeux, déterministe d'abord, CI puis prod | Distingue explicitement capacité et régression, et pass@k / pass^k : notions absentes du scénario |
| Huyen, « AI Engineering » chap. 3, 4, 10 [8] | Méthodologie d'évaluation (métriques exactes, similarité, IA-juge, comparaison) avant évaluation du système, retours utilisateurs en fin de parcours | Méthode avant pipeline | Approche plus « modèle » (choix de modèle, benchmarks publics contaminés) ; le cours est plus « application », ce qui est adapté à un public de développeurs |
| Google, Rules of ML [13] | Métriques et infrastructure d'abord, modèle simple, tester l'infrastructure indépendamment | Fake et tests d'infra avant evals | Ancien (ML classique), mais l'argument « surveiller les échecs silencieux » reste valable |

---

## 3. Erreurs et idées reçues fréquentes

1. **« Avec temperature=0 mes tests seront reproductibles. »** Faux en pratique, même en local avec vLLM [16]. Les tests qui appellent un vrai modèle vérifient des propriétés, sur plusieurs essais.
2. **Asserter l'égalité exacte d'un texte généré**, ou à l'inverse ne rien tester parce que « c'est non déterministe ». Le code autour se teste à 100 % avec une doublure [13][20].
3. **Tester le chemin plutôt que le résultat** (ordre exact des appels d'outils) : tests fragiles qui punissent des solutions valides [9]. Exception justifiée : vérifier qu'un outil sensible n'a pas été appelé (sécurité).
4. **Faire confiance à un juge LLM non validé**, ou faire juger un modèle par lui-même (biais d'auto-préférence) [5][11][14]. Un juge sans mesure d'accord avec des humains (précision/rappel, kappa) n'est pas une mesure [3][7].
5. **Noter sur une échelle 1-5 multi-critères dans un seul prompt** (« God Evaluator ») [3][7].
6. **Utiliser ROUGE/BERTScore/similarité cosinus comme métrique principale** de qualité d'une application [2][10]. La « détection de dérive sémantique par embeddings » peut servir d'alerte, pas de verdict.
7. **Construire le jeu de référence en imaginant des cas** sans lire de traces, ou uniquement avec des défauts synthétiques générés par un modèle fort, souvent hors distribution [2][7].
8. **Conclure sur un seul passage** de 10 cas : l'intervalle de confiance est énorme ; raisonner en taux, pass@k ou pass^k [7][9].
9. **Croire qu'épingler le modèle supprime toute dérive.** L'infrastructure de service change, les modèles sont retirés (préavis de 60 jours minimum chez Anthropic) et les alias de certaines générations évoluent [23]. À l'inverse, croire qu'un identifiant sans date est forcément un alias « latest » : faux chez Anthropic depuis la génération 4.6 [23].
10. **Journaliser tous les prompts et réponses par défaut** : contraire aux défauts d'OTel et de Spring AI, risque RGPD et fuite de secrets [17][19].
11. **Calculer le coût comme total de tokens × un prix unique** : faux dès qu'il y a cache de prompt ou tokens de raisonnement [20].
12. **Présenter OTel GenAI comme un standard stable**, ou citer l'ancien emplacement dans `semantic-conventions` : statut Development, dépôt dédié depuis mai 2026, noms de métriques qui changent [17].
13. **Un span par retry** comme seule trace : selon OTel le span d'inférence couvre l'opération logique retries compris ; tracer les tentatives comme événements ou attributs, et logguer le recours au plan de secours [17].
14. **Logs sans identifiant de requête / plan de repli qui retente à l'infini** (déjà dans S3.3) : à relier aux paramètres Laravel `tries`, `backoff`, `FailOnTimeout` [21].
15. **Oublier de redémarrer les workers après déploiement**, ou un `timeout` de job supérieur à `retry_after` : double exécution, donc double appel payant [21].
16. **Mettre les evals coûteuses dans le chemin bloquant de chaque PR**, ou au contraire ne jamais les lancer ; et compter sur `schedule` GitHub comme s'il était ponctuel, ou sur les secrets dans une PR venant d'un fork [2][22].
17. **S'appuyer sur la plateforme Evals d'OpenAI** dans un support : fermée le 30/11/2026 [10].
18. **Dire que `laravel/ai` est en 0.x** (bibliographie actuelle) : v1.x depuis le 23/09/2026 [20].
19. **« Les evals remplacent la surveillance »** ou l'inverse : il faut les deux, plus de la relecture humaine (modèle du gruyère suisse) [9].
20. **Annoncer 0 % de réussite comme preuve que l'agent est mauvais** : souvent une tâche ou un grader mal spécifié [9].

---

## 4. Sources

1. Husain H. (2024), Your AI Product Needs Evals, hamel.dev (blog).
   https://hamel.dev/blog/posts/evals/ ; billet de blog ; publié le 29/03/2024 ; consulté le 24/11/2026 ; [S4.1, S4.4, S5.2].
   Trois niveaux d'eval (assertions, évaluation humaine et par modèle, A/B) ; tests à portée limitée écrits à partir des échecs observés ; mesurer l'accord juge/humain.

2. Husain H. et Shankar S. (2025-2026), AI Evals FAQ (« Everything You Need to Know »), hamel.dev.
   https://hamel.dev/blog/posts/evals-faq/ ; FAQ en ligne mise à jour en continu (aussi en PDF) ; consulté le 24/11/2026 ; [S4.1, S5.1, S5.2].
   Analyse d'erreurs d'abord (100 traces, 30 annotées soi-même), hiérarchie de coût des évaluateurs, métriques génériques déconseillées, evals en CI (petit jeu, assertions) contre surveillance de prod.

3. Husain H. (2024), Using LLM-as-a-Judge For Evaluation: A Complete Guide, hamel.dev.
   https://hamel.dev/blog/posts/llm-judge/ ; billet de blog ; publié le 29/10/2024 ; consulté le 24/11/2026 ; [S4.1].
   « Critique shadowing » : un expert de domaine principal, verdicts pass/fail avec critiques, itérer le prompt du juge jusqu'à convergence ; contre les échelles 1-5.

4. Shankar S., Zamfirescu-Pereira J.D., Hartmann B., Parameswaran A.G. et Arawjo I. (2024), Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences, UIST 2024, ACM (doi:10.1145/3654777.3676450), arXiv:2404.12272.
   https://arxiv.org/abs/2404.12272 ; article de recherche ; 2024 ; consulté le 24/11/2026 ; [S4.1].
   Outil EvalGen ; notion de « dérive des critères » : les critères d'évaluation se définissent en regardant les sorties. Auteurs vérifiés sur la notice arXiv ; la page ACM n'a pas été ouverte, seulement repérée en recherche.

5. Zheng L., Chiang W.-L., Sheng Y. et al. (2023), Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena, NeurIPS 2023 Datasets and Benchmarks, arXiv:2306.05685.
   https://arxiv.org/abs/2306.05685 ; article de recherche ; v4 ; consulté le 24/11/2026 ; [S4.1].
   Plus de 80 % d'accord juge fort/humains ; biais de position, de verbosité, d'auto-préférence.

6. Yan E. (2024), Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge), eugeneyan.com.
   https://eugeneyan.com/writing/llm-evaluators ; synthèse de littérature ; publié le 18/08/2024 ; consulté le 24/11/2026 ; [S4.1].
   Panorama des usages, techniques (G-Eval, comparaison par paires), juges affinés et critiques ; cadrer le juge comme une tâche de classification.

7. Yan E. (2025), Product Evals in Three Simple Steps, eugeneyan.com.
   https://eugeneyan.com/writing/product-evals ; billet d'ingénierie ; publié le 23/11/2025 ; consulté le 24/11/2026 ; [S4.1, S5.2].
   Étiquettes binaires, 50-100 échecs sur 200+ cas, découpe 75/25, un évaluateur par dimension, biais de position, précision/rappel/kappa, calcul d'intervalle de confiance.

8. Huyen C. (2025), AI Engineering: Building Applications with Foundation Models, O'Reilly Media (résumés officiels des chapitres sur le dépôt GitHub de l'autrice).
   https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md ; livre (consulté via les résumés de chapitres de l'autrice, pas le texte intégral) ; édition 2025 ; consulté le 24/11/2026 ; [S4.1, S5.1].
   Chap. 3 (méthodologie : exact, similarité, IA-juge, comparatif), chap. 4 (pipeline d'évaluation, benchmarks contaminés), chap. 10 (retours utilisateurs) ; scores d'IA-juge non comparables dans le temps.

9. Anthropic (2026), Demystifying evals for AI agents, Anthropic Engineering.
   https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents ; billet d'ingénierie d'éditeur ; publié le 09/01/2026 ; consulté le 24/11/2026 ; [S4.1, S4.4, S5.1, S5.2].
   Graders code/modèle/humain, evals de capacité contre régression, pass@k et pass^k, 20-50 tâches pour démarrer, noter le résultat pas le chemin, lire les transcripts, modèle du gruyère suisse.

10. OpenAI (2026), Evaluation best practices et Deprecations, OpenAI API Docs.
    https://developers.openai.com/api/docs/guides/evaluation-best-practices et https://developers.openai.com/api/docs/deprecations ; documentation officielle ; consultée le 24/11/2026 ; [S4.1, S5.1, S5.2].
    Processus d'eval (objectif, jeu, métriques, comparaison, évaluation continue), anti-patterns ; annonce de la fermeture de la plateforme Evals (lecture seule 31/10/2026, arrêt 30/11/2026, migration vers Promptfoo).

11. Thoughtworks (2025), LLM as a judge, Technology Radar (Vol. 33).
    https://www.thoughtworks.com/radar/techniques/llm-as-a-judge ; référentiel de pratiques ; mis à jour le 05/11/2025 ; consulté le 24/11/2026 ; [S4.1].
    Passage de Trial (oct. 2024) à Assess (nov. 2025) : biais, faible robustesse, contamination ; piste « LLMs as a jury » ; vérification humaine.

12. Sculley D., Holt G., Golovin D. et al. (2015), Hidden Technical Debt in Machine Learning Systems, Advances in Neural Information Processing Systems 28 (NIPS 2015).
    https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html ; article de recherche ; 2015 ; consulté le 24/11/2026 (résumé) ; [S5.1].
    Dette propre aux systèmes ML : enchevêtrement, dépendances de données, configuration, changements du monde extérieur.

13. Zinkevich M. (2025), Rules of Machine Learning: Best Practices for ML Engineering, Google for Developers.
    https://developers.google.com/machine-learning/guides/rules-of-ml ; guide d'ingénierie ; mis à jour le 25/08/2025 ; consulté le 24/11/2026 ; [S4.1, S5.1].
    Règle 2 (métriques d'abord), règle 5 (tester l'infrastructure indépendamment du ML), règle 10 (échecs silencieux), règle 29/37 (écart entraînement/service).

14. Subramaniam B. et Fowler M. (2025), Emerging Patterns in Building GenAI Products, martinfowler.com.
    https://martinfowler.com/articles/gen-ai-patterns/ ; article d'ingénierie ; 25/02/2025 ; consulté le 24/11/2026 ; [S4.1, S5.2].
    Patron « Evals » : auto-évaluation déconseillée, juge d'un autre modèle, combinaison juge et humain ; evals dans le pipeline avec seuils, comme des tests de performance, et en production.

15. Chen L., Zaharia M. et Zou J. (2023), How is ChatGPT's behavior changing over time?, arXiv:2307.09009 (v3, 31/10/2023).
    https://arxiv.org/abs/2307.09009 ; article de recherche ; 2023 ; consulté le 24/11/2026 ; [S5.1].
    Variations fortes entre versions de mars et juin 2023 de GPT-3.5/GPT-4 ; argument fondateur pour épingler et surveiller.

16. He H. et Thinking Machines Lab (2025), Defeating Nondeterminism in LLM Inference, Thinking Machines Lab: Connectionism, doi:10.64434/tml.20250910.
    https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ ; billet de recherche ; septembre 2025 ; consulté le 24/11/2026 ; [S4.1].
    Température 0 non déterministe en pratique (80 complétions distinctes sur 1 000) ; cause : absence d'invariance au lot.

17. OpenTelemetry (2026), Semantic Conventions for Generative AI (client inference, execute tool, agent spans, metrics, token metrics), dépôt open-telemetry/semantic-conventions-genai, GitHub.
    https://github.com/open-telemetry/semantic-conventions-genai ; spécification ; statut Development, branche main, dépôt créé le 05/05/2026 ; consulté le 24/11/2026 ; [S3.2, S3.3, S5.1].
    Spans et attributs GenAI, contenu en Opt-In, `gen_ai.prompt.version`, métriques `gen_ai.client.inference.usage.*` ; l'ancien dossier du dépôt principal est marqué « moved ».

18. OpenTelemetry Authors (2026), Inside the LLM Call: GenAI Observability with OpenTelemetry, OpenTelemetry Blog.
    https://opentelemetry.io/blog/2026/genai-observability/ ; billet officiel ; publié le 14/05/2026, modifié le 14/09/2026 ; consulté le 24/11/2026 ; [S3.2].
    Démonstration bout en bout (export OTLP, Aspire Dashboard) ; rappelle que prompts et arguments d'outils ne sont pas capturés par défaut.

19. Broadcom / VMware (2026), Spring AI Reference : Observability et Evaluation Testing, version 2.1.0.
    https://docs.spring.io/spring-ai/reference/observability/index.html et https://docs.spring.io/spring-ai/reference/api/testing.html ; documentation officielle ; v2.1.0 ; consultée le 24/11/2026 ; [S3.2, S4.1].
    Observations `gen_ai.client.operation`, métrique `gen_ai.client.token.usage`, `log-prompt`/`log-completion` à false ; `Evaluator`, `RelevancyEvaluator`, `FactCheckingEvaluator`.

20. Laravel (2026), Laravel AI SDK (package laravel/ai) : Usage, Failover, Testing, Events, Laravel 13.x Documentation.
    https://laravel.com/docs/13.x/ai-sdk ; documentation officielle ; package v1.4.2 (24/11/2026), v1.0.0 (23/09/2026) d'après https://github.com/laravel/ai/releases ; consultée le 24/11/2026 ; [S3.2, S4.1, S4.4].
    `Agent::fake()`, assertions, `preventStrayPrompts()`, usage par catégorie de tokens, bascule de fournisseur, liste des événements.

21. Laravel (2026), Queues, Horizon et Deployment, Laravel 13.x Documentation (framework v13.44.1).
    https://laravel.com/docs/13.x/queues , https://laravel.com/docs/13.x/horizon , https://laravel.com/docs/13.x/deployment ; documentation officielle ; consultée le 24/11/2026 ; [S3.3, S5.2].
    Timeout inférieur à retry_after, tries/backoff/FailOnTimeout, queue:restart, horizon:terminate, nouvelle commande `reload`, Supervisor, optimize, route `/up`.

22. GitHub (2026), Events that trigger workflows, GitHub Actions Docs.
    https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows ; documentation officielle ; consultée le 24/11/2026 ; [S5.2].
    `schedule` (retards et abandons en charge, branche par défaut, désactivation après 60 jours, intervalle minimal 5 min), secrets non transmis aux PR de forks.

23. Anthropic (2026), Model IDs and versioning et Model deprecations, Claude Platform Docs.
    https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions et https://platform.claude.com/docs/en/about-claude/model-deprecations ; documentation officielle ; consultée le 24/11/2026 ; [S5.1].
    Identifiants sans date figés depuis la génération 4.6, alias évolutifs pour les générations antérieures, changements d'infrastructure possibles, préavis de retrait d'au moins 60 jours.

24. Husain H. et Sedgh E. (2024), How to construct domain-specific LLM evaluation systems, AI Engineer World's Fair 2024 (conférence filmée).
    https://ai.engineer/talks/eLXF0VojuSs-construct-domain-specific-llm-evaluation-systems (vidéo : https://www.youtube.com/watch?v=eLXF0VojuSs) ; vidéo, lue via la page de synthèse horodatée du site AI Engineer ; 2024 ; consulté le 24/11/2026 ; [S4.1, S4.4, S5.2].
    Cas Rechat : assertions issues d'échecs observés (action d'e-mail non effectuée, placeholders), lancées en CI, résultats stockés et suivis dans un tableau de bord.

25. Rachitsky L. (hôte), Husain H. et Shankar S. (invités) (2025), Why AI evals are the hottest new skill for product builders, Lenny's Podcast.
    https://www.lennysnewsletter.com/p/why-ai-evals-are-the-hottest-new-skill ; podcast audio (1 h 46) ; épisode du 25/09/2025 ; consulté le 24/11/2026 (page d'épisode et chapitrage, transcription complète réservée aux abonnés, non lue) ; [S4.1, S5.1].
    Commencer par l'analyse d'erreurs (16:51), codage ouvert et axial, code contre juge, « evals are the new PRDs » (1:00:51), environ 30 min par semaine après la mise en place.

Source mentionnée en complément (non comptée) : Langfuse (2026), Prompt Version Control, https://langfuse.com/docs/prompt-management/features/prompt-version-control , documentation d'un produit commercial (open source avec offre payante), consultée le 24/11/2026 [S5.1] : versions numérotées et étiquettes `production`/`staging`.
