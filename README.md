# FYC : Find Your Course

Dépôt de travail du projet FYC (ESGI / Sciences-U Lyon, promo 2026-2027).
Le livrable final est un cours en ligne déposé sur Teams (changement de consigne de novembre 2026 : Moodle n'est plus utilisé). Ce dépôt sert à
écrire le contenu en Markdown, à le versionner, à suivre les retours du mentor
et à générer les documents Word (docx) avec la charte graphique du groupe.

> **Concevoir une application web maintenable intégrant un agent IA : architecture, tests, sécurité et mise en production.**
> Parcours Laravel (PHP), TP sans SDK d'IA. Le Laravel AI SDK et Spring AI servent de points de comparaison.
>
> Problématique : _Comment intégrer un agent IA dans une application web sans dégrader sa maintenabilité, sa testabilité, sa sécurité et sa maîtrise en production ?_
> Détail dans `livrables/problematique.md`.

## Équipe

| Nom | Prénom | Filière | Rôle |
|-----|--------|---------|------|
| Bauduin | Quentin | IW | Chef de projet, contenu transversal |
| Geoffroy | Timothé | IW | Fil rouge et comparaisons |
| Topkaya | Kaan | IW | TP Laravel |
| Gossin | Erwin | IW | Environnement & infrastructure |

## Contraintes du projet (résumé)

Source : `ressources/presentation-projet-fyc-26-27.pdf`.

- Durée apprenant : **10 à 15 h**. Minimum 1/3 écrit, 1/3 vidéo.
- Écrit : ~**30 pages** (1 page = 4 000 signes), 20 % max en illustrations/code.
  Schémas construits par nous. Reproduction citée et limitée à 15 %.
- Vidéo : ~**1 h 30** au total, **8 min max** par vidéo, **sous-titres obligatoires**.
  Vidéos imposées : cours, équipe et pré-requis (une seule vidéo, 3 min max),
  2 sujets complexes, conclusion « pour aller plus loin », correction du cas pratique.
- Évaluation apprenant : test de positionnement, 1 exercice par chapitre,
  au moins 2 exercices non-QCM, 1 cas pratique avec corrigé vidéo,
  test final (~40 QCM). Corrigés pour tout.
- Bibliographie aux normes de `ressources/normes-bibliographie.pdf`.
- Pas de drive. Dépôts GitHub publics autorisés, accessibles 5 ans.
- Toute génération IA automatique est considérée comme de la triche. Notre
  usage : aller-retour avec l'IA (proposition, rédaction, relecture), et
  vérification puis validation humaine de chaque contenu avant merge.
  Détail dans `CLAUDE.md`.

## Jalons

| Date | Séance | Attendu |
|------|--------|---------|
| 8 juil. 2026 | Séance 1 | Scénarisation V0 + ébauche biblio validées |
| 9 sept. 2026 | Séance 2 | Scénarisation finale, vidéo de présentation, biblio, 20 % des supports |
| 2 déc. 2026 | Séance 3 | 50 % du contenu sur Teams, test des QCM/exercices/vidéos |
| 6 janv. 2027 | Séance 4 | 100 % du contenu sur Teams, V0 du support de soutenance |
| 25 janv. 2027 (à confirmer) | Dépôt final sur Teams | Dépôt définitif |
| 3 févr. 2027 | Soutenance | 15 min présentation, 25 min Q&R |

## Organisation du dépôt

```
ressources/       Documents fournis par l'école (consigne, template, normes biblio)
cours/            Contenu du cours en Markdown, un dossier par chapitre
livrables/        Problématique, scénarisation, bibliographie, accroche, budget vidéo, avancement, soutenance
                  archives/ : les PDF tels que rendus à chaque séance
retours-mentor/   Compte-rendu de chaque séance avec le mentor
charte/           Charte graphique : reference.docx, logos, guide de style
scripts/          Outils de build (md → docx)
build/            Sorties générées (ignoré par git)
```

Chaque chapitre dans `cours/NN-slug/` contient :

```
README.md         Fiche du chapitre : objectifs, durée apprenant, pré-requis
cours.md          Le support écrit
exercices.md      Exercices non-QCM avec corrigés
qcm.md            Questions à choix multiples avec corrigés
videos/           Scripts des vidéos (un fichier par vidéo) et sous-titres
assets/           Schémas et images construits par nous
```

## Workflow

1. Une branche par tâche (nom généré par Linear, `prenom/fyc-nn-titre`), pull request vers `main`.
2. Chaque tâche a une issue Linear. Le titre de l'issue commence par le
   numéro du chapitre puis la séquence (`02 · S2.3 · …`). L'estimation est en
   **heures apprenant**, sur l'issue du chapitre seulement : la somme des
   estimations doit égaler la durée cible du cours.
3. Le contenu s'écrit en Markdown. Les conventions sont dans `charte/guide-de-style.md`.
4. Export docx : `scripts/build.sh` (voir ci-dessous).
5. Après chaque séance, on note les retours du mentor dans `retours-mentor/`
   et on crée les issues correspondantes.

## Export docx

Prérequis : [pandoc](https://pandoc.org) (`brew install pandoc`).

```bash
scripts/build.sh                      # tout le cours et tous les livrables
scripts/build.sh cours/01-architecture-et-ia   # un chapitre
scripts/build.sh livrables/scenarisation.md
```

Les fichiers sortent dans `build/`. La mise en page vient de
`charte/reference.docx` : modifier ce fichier dans Word change la charte de
tous les exports.

## Rendus par jalon

Les docx ne sont pas versionnés (`build/` est ignoré). À chaque jalon, on
publie une release GitHub qui contient tous les exports, et on archive une
copie datée dans `livrables/archives/` :

```bash
scripts/release.sh seance-2 "Séance 2 : scénarisation finale, biblio, 20 % des supports"
```

La release est l'endroit centralisé des rendus. Coller son lien dans le jalon
Linear et dans les issues concernées. `livrables/archives/` garde aussi les
PDF tels que déposés sur Teams.

## Avec Claude Code ou Codex

Le dépôt fonctionne avec les deux. Les fichiers de contexte et les skills sont
partagés :

| | Claude Code | Codex |
|---|---|---|
| Contexte du projet | `CLAUDE.md` | `AGENTS.md` (lien vers le même fichier) |
| Skills (`/ship`, `/chapitre`, `/retour-mentor`) | `.claude/skills/` | `.agents/skills/` (lien vers le même dossier) |
| Lint après chaque écriture | hook dans `.claude/settings.json` | pas d'équivalent : installer le hook git ci-dessous |
| Linear | `.mcp.json` du dépôt (connexion avec son propre compte via `/mcp`) | serveur MCP Linear à déclarer dans `~/.codex/config.toml` |
| Prof du cours | skill `prof` (`.claude/skills/prof/`, fiches de sources dans `references/`) | même skill via `.agents/skills/` |

Après le clonage, quel que soit l'outil :

```bash
scripts/install-hooks.sh   # refuse un commit qui viole charte/regles-redaction.md
```

### Travailler en local avec un abonnement Claude (repli de l'agent Discord)

L'agent FYC sur Discord tourne sur un budget API partagé. Quand il n'est pas
disponible, chacun peut travailler sur son PC avec Claude Code et son propre
abonnement Claude (Pro suffit pour rédiger, Max pour un usage intensif). Les
règles, les skills et le prof sont dans le dépôt : le résultat est le même.

1. Prérequis : `git`, `bash` (Git Bash sous Windows), `jq` (utilisé par le
   hook de lint), [pandoc](https://pandoc.org/installing.html) pour l'export,
   [Claude Code](https://docs.claude.com/en/docs/claude-code) connecté à son
   compte Claude (`claude` puis `/login`).
2. Cloner le dépôt, configurer son identité git (`git config user.name` et
   `user.email`, celle de son compte GitHub), puis `scripts/install-hooks.sh`.
3. Dans le dossier du dépôt, lancer `claude`, accepter le serveur `linear-server`
   proposé par `.mcp.json`, puis `/mcp` pour se connecter à Linear avec son
   propre compte : les commentaires et changements d'état sont à son nom.
4. Travailler comme avec l'agent : `/ship FYC-nn` pour une issue, ou
   « utilise la skill prof et rédige la section… ». Le lint tourne après
   chaque écriture.
5. Ce qui manque par rapport à l'agent : la mémoire partagée du groupe. Pour
   que les autres (et l'agent) soient au courant, laisser un commentaire sur
   l'issue Linear à la fin de chaque session (fait, reste à faire, décision).

## Suivi du projet

Le suivi se fait dans Linear : [projet FYC](https://linear.app/fyc/project/fyc-cours-ia-and-architecture-web-838bc16885f9).

- Un jalon par séance (S2, S3, S4, dépôt final sur Teams, soutenance).
- Une issue par chapitre (label `chapitre`, estimation = heures apprenant,
  Linear n'accepte que des entiers : le chapitre 00 vaut 1 pour 45 min réelles,
  le chapitre 01 vaut 3 pour 2 h 15). La durée de référence est dans les
  séquences.
- Sous chaque chapitre, une issue par séquence (`NN · Sx.y · …`, durée
  apprenant en description, 20 séquences pour 15 h), puis sous chaque séquence
  une sous-issue par ressource prévue dans la colonne « Ressources » de
  `livrables/scenarisation.md` (support écrit, dépôt, squelette, corrigé,
  vidéo), avec responsable et échéance.
- Le label `annexe` marque le travail hors contenu apprenant (dépôts de TP,
  outillage, Teams, avancement, soutenance, relectures) : il compte pour
  l'avancement individuel, pas dans le pourcentage du cours, calculé par
  séquence avec `scripts/avancement.py`. Un dépôt de TP `annexe` est rattaché à
  sa séquence, qui n'est Done qu'une fois le dépôt livré.
- Une issue par livrable transversal : test final, cas pratique, budget vidéo,
  dépôt sur Teams et document d'avancement de chaque jalon.
- Une PR qui modifie la scénarisation met Linear à jour et le dit. `/audit-plan`
  vérifie l'écart entre le plan et Linear ; `/retour-mentor` le lance après
  chaque séance.
- Une issue par action issue d'un retour du mentor (label `retour-mentor`).
- Labels `spring` / `laravel` pour les tâches propres à un parcours.
- Nomenclature complète (labels, jalons, priorités, statuts, définition de
  terminé) : [document Linear](https://linear.app/fyc/document/nomenclature-linear-comment-on-utilise-ce-projet-ef7b50633f27).
