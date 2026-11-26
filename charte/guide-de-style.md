# Guide de style

Conventions d'écriture du cours. La mise en page Word vient de `reference.docx`,
ce guide couvre le fond et la structure Markdown.

## Charte graphique

Décidée le 08/09/2026 avec la page « Charte FYC », reportée dans `reference.docx`.

| Élément | Valeur |
|---|---|
| Police titres et corps | Arial, corps 11 pt, interligne 1,3 |
| Police code | Consolas (présente dans Word) |
| Titres | Noir `#111111`, gras, numérotés, niveau 1 en capitales, sans filet |
| Accent | Bleu pétrole `#14526D` : liens, filet gauche des citations |
| Tableaux | Bordures `#999999`, en-tête fond `#EFEFEF` en gras, lignes alternées `#F5F7F9`, texte 9 pt |
| Page de titre | Alignée à gauche, sans bandeau |
| Logos | `charte/logos/` (à ajouter) |

Pour changer une valeur : rouvrir la page Charte FYC, enregistrer, puis
reporter dans `reference.docx` (styles Word) et ici.

## Structure d'un fichier `cours.md`

```markdown
# Chapitre N : Titre

> Durée estimée : X min · Objectifs : ...

## 1. Section
### 1.1 Sous-section
```

- Un seul `#` (titre de niveau 1) par fichier.
- Le chapitre se termine par une section `## Pour aller plus loin` : 3 à 6
  liens commentés (documentation officielle d'abord, puis article, vidéo ou
  talk), chacun avec une ligne qui dit ce que l'apprenant y trouvera.

### Déroulé d'une section

Chaque section (`## N.` ou `### N.M`) porte **une seule notion nouvelle** et
suit ce déroulé. On n'écrit pas les étapes comme intitulés : c'est la
progression du texte.

1. **Le problème concret** (3 à 6 lignes) : une situation que l'apprenant
   reconnaît, qui se termine par la question à laquelle la section répond.
   On n'ouvre jamais sur « Dans cette section, nous allons voir ».
2. **L'explication** : une idée par paragraphe, le terme en **gras** à sa
   première apparition. Une analogie est suivie de sa limite.
3. **L'exemple travaillé** : 20 à 40 lignes de code au plus, découpées en
   étapes commentées, avec ce que l'exécution affiche.
4. **Le piège fréquent** : « On voit souvent… Le problème, c'est que…
   À la place… ».
5. **Le mini-exercice** (2 à 5 min) : une question ou un petit code à
   compléter, réponse juste après (bloc `> **Réponse :** …`).
6. **Le récap** : trois règles d'action au plus, puis une phrase vers la
   suite.

Ce qu'on reporte, on le dit : « on y revient en séance 4 ». Ce qui n'est pas
réglé dans le domaine (injection de prompt, IA juge), on le dit aussi.
- Les titres de niveau 2 sont numérotés à la main (`## 1.`, `## 2.`) pour
  garder la numérotation cohérente entre Markdown et docx.
- Pas de titre de niveau 4 ou plus.

## Écriture

- Vouvoiement de l'apprenant, ton direct et concret.
- Phrases courtes. Un paragraphe = une idée.
- Chaque notion nouvelle est définie à sa première apparition, en **gras**.
- Les termes techniques anglais sont en _italique_ à la première occurrence,
  avec une traduction ou explication.
- Les exemples de code ont un langage déclaré : ```` ```python ````.
- Les schémas sont dans `assets/` du chapitre, référencés avec une légende :
  `![Légende du schéma](assets/nom.png)`.

## Ressources externes et renvois

Le cours suppose des connaissances que l'apprenant n'a pas forcément
(demande du mentor, séance 2). Chaque notion extérieure qu'on manipule sans
l'enseigner renvoie vers une ressource qu'il peut consulter s'il ne la
connaît pas. Deux endroits, qui ne se remplacent pas :

- **La rubrique « Ressources » du `README.md` du chapitre** : une ligne par
  notion extérieure manipulée dans le chapitre, au format ci-dessous. Elle
  sert avant ou pendant le chapitre.
- **Le renvoi en ligne**, dans un support ou un énoncé de TP, à la première
  occurrence de la notion, à l'étape qui la manipule : « Si vous ne connaissez
  pas le routeur de Laravel : [Routing, Laravel 13.x](https://laravel.com/docs/13.x/routing). »
  Une seule fois par notion et par document.

La section `## Pour aller plus loin` de `cours.md` reste à part : elle sert
après le chapitre, pour approfondir (3 à 6 liens commentés), pas pour
rattraper un pré-requis.

Format de la rubrique du `README.md` :

```markdown
## Ressources

| Notion | Ressource officielle | À consulter si… |
|--------|----------------------|-----------------|
| Routage Laravel | [Routing, Laravel 13.x](https://laravel.com/docs/13.x/routing) | vous n'avez jamais déclaré une route |
```

Règles :

- Documentation officielle d'abord, à la version utilisée par le cours. À
  défaut, un article ou une vidéo gratuits, sans compte.
- On renvoie, on ne recopie pas (limite des 15 % de contenu reproduit).
- Chaque ressource citée remonte dans `livrables/bibliographie.md`
  (catégorie « Documentation technique », balise `[Sx.y]` de la séquence,
  date de consultation).
- Une notion enseignée dans le chapitre n'a pas de ligne : elle est
  définie dans le texte.

## Exercices et QCM

Format d'un exercice (`exercices.md`) :

```markdown
## Exercice N : Titre

**Objectif :** ...
**Durée :** X min

### Énoncé
...

### Indices
1. (facultatif, du plus léger au plus direct)

### Corrigé
...
```

Le corrigé explique la démarche, pas seulement le résultat, et cite les
erreurs les plus probables.

Format d'une question (`qcm.md`) :

```markdown
## Question N

Énoncé de la question ?

- [ ] Réponse A
- [x] Réponse B (bonne réponse)
- [ ] Réponse C
- [ ] Réponse D

**Explications :**

- A : pourquoi c'est faux (quelle erreur de raisonnement y mène).
- B : pourquoi c'est juste.
- C : …
- D : …
```

Règles d'une question : un seul objectif testé, ancré dans une situation
concrète ; les mauvaises réponses viennent d'erreurs réelles et sont
plausibles ; pas de « toutes / aucune des réponses », pas d'indice par la
longueur ou la formulation ; la position de la bonne réponse varie. Le test
de positionnement ajoute une option « Je ne sais pas » et n'est pas noté.

## Sources et citations

- Toute reprise de contenu externe est citée : `(Auteur, année)` dans le texte
  et entrée complète dans `livrables/bibliographie.md`.
- Limite : 15 % de contenu reproduit sur l'ensemble du cours.
- Format des références : voir `ressources/normes-bibliographie.pdf`.

## Vidéos

Un fichier par vidéo dans `cours/NN-slug/videos/` :

```markdown
# Vidéo : Titre

- Durée cible : X min (max 8)
- Intervenant : ...
- Format : face caméra / screencast / live-coding

## Script
...

## Plan de montage
...
```

Les sous-titres (`.srt` ou `.vtt`) sont dans le même dossier.
