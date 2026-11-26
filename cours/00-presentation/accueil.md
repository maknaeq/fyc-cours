# Bienvenue dans le cours

Ce cours vous apprend à intégrer un agent IA dans une application web Laravel
sans la rendre impossible à maintenir, à tester, à sécuriser et à exploiter.
Vous faites évoluer un même projet, NoteFlow, une application de notes avec un
agent, de la deuxième séance jusqu'à sa mise en ligne.

Un choix structure les TP : vous n'utilisez pas de SDK d'IA. Vous écrivez
chaque brique vous-même, puis vous la comparez à ce que font le Laravel AI SDK
et Spring AI.

## Ce que vous saurez faire

À la fin du cours, vous saurez :

1. isoler le fournisseur d'IA derrière un port et y brancher trois adaptateurs
   (en ligne, local, doublure de test) ;
2. concevoir la boucle d'un agent et justifier quand un simple workflow suffit ;
3. construire un pipeline de récupération (plein texte et vectoriel sur
   pgvector) et en mesurer la qualité ;
4. rendre l'appel à l'IA résilient (délais, idempotence, réessai borné,
   coupe-circuit, repli) ;
5. instrumenter l'agent : une trace et un coût par requête ;
6. tester l'agent avec une doublure, des assertions de propriétés et un jeu de
   référence ;
7. analyser ses risques (OWASP LLM 2026, règle de deux) et poser des défenses
   qui bornent l'impact ;
8. le mettre en production : CI à deux étages, déploiement du worker, alertes
   de dérive.

## Le plan

Quinze heures au total, à votre rythme.

- **Chapitre 00 (45 min)** : présentation, test de positionnement, installation.
- **Séance 1 (2 h 15)** : les bases de l'architecture web, et pourquoi l'IA les
  bouscule.
- **Séance 2 (3 h)** : un agent IA, ça se construit comme un composant.
- **Séance 3 (3 h)** : rendre son appli fiable et surveillable.
- **Séance 4 (3 h)** : bien tester, et se méfier des attaques.
- **Séance 5 (3 h)** : mettre en prod et conclure, avec le cas pratique et le
  test final.

## Avant de commencer

Il vous faut les pré-requis suivants : PHP orienté objet, bases de Laravel
(routes, contrôleurs, Eloquent, conteneur de services), HTTP et API REST, Git.
Le test de positionnement de ce chapitre prend une dizaine de minutes
et n'est pas noté. La fiche du chapitre 00 donne, pour chaque question, une
ressource de mise à niveau.

Ensuite, le guide d'installation vous fait mettre en place l'environnement : un
modèle local gratuit (Ollama) suffit pour tous les TP, et une clé chez un
fournisseur en ligne est facultative. Un script vérifie que tout fonctionne :
c'est la condition d'entrée en séance 1.

## Comment suivre le cours

Chaque séance suit le même rythme : un support écrit et quelques vidéos courtes
(8 minutes au plus), un TP, puis des questions et un exercice.

- **Les mini-exercices.** Chaque section du support se termine par un
  mini-exercice. Répondez avant de lire la réponse, qui se trouve juste en
  dessous.
- **Les TP.** Chaque TP a un énoncé, un dépôt de départ et un corrigé. Essayez
  avant d'ouvrir le corrigé. Les dépôts sont cités dans la fiche de chaque
  chapitre.
- **Le fil rouge.** NoteFlow apparaît en séance 2 et sert de base aux TP des
  séances suivantes. La fiche du fil rouge, au chapitre 02, présente le cas.
- **Les ressources.** Chaque fiche de chapitre a une rubrique « Ressources » :
  elle renvoie vers la documentation officielle des notions qu'on manipule sans
  les enseigner.
- **L'évaluation.** Des questions et au moins un exercice par séance, un cas
  pratique et un test final d'environ 40 questions en séance 5. Les corrigés
  expliquent chaque réponse, pas seulement la bonne.
