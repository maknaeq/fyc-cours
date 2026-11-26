# Exercices : chapitre 01

## Exercice 1 : Fiche de réponse, trois parades pour le contrôleur fourre-tout

**Objectif :** relier chaque point de rupture de l'étude de cas (section 2.1
du cours) à une famille de solutions, sans encore les mettre en œuvre.
**Durée :** 15 min

### Énoncé

Relisez l'étude de cas de la section 2.1 et la liste des points de rupture de
la section 2.3. Remplissez la fiche ci-dessous. Pour chaque parade, une ou
deux phrases suffisent. Il n'y a pas une seule bonne réponse : ce qui compte,
c'est que chaque parade réponde à un incident précis et que vous sachiez dire
ce qu'elle ne résout pas.

| | Incident visé | Parade proposée | Ce qu'elle ne résout pas |
|---|---|---|---|
| Parade 1 | | | |
| Parade 2 | | | |
| Parade 3 | | | |

Question bonus : parmi vos trois parades, laquelle peut se mettre en place
sans toucher au code métier, uniquement dans l'adaptateur ou la configuration ?

### Corrigé

Le corrigé passe en revue les quatre familles de parades les plus courantes.
Vos trois réponses en font probablement partie. Chaque famille sera construite
en séance 3, ici on se contente de comprendre ce qu'elle apporte et ce qu'elle
laisse ouvert.

**Traitement en arrière-plan.** Le contrôleur ne fait plus l'appel lui-même :
il crée un _job_ dans une file d'attente et répond tout de suite « résumé en
cours ». Un processus séparé, le _worker_, traite les jobs un par un. Incident
visé : le blocage de 9 h, le site reste réactif quel que soit le nombre de
clics. Ce qu'il ne résout pas : l'appel a toujours lieu, coûte toujours, et
peut toujours échouer. Il faut aussi prévoir comment l'utilisateur récupère le
résultat (rafraîchissement, notification, ou flux temps réel).

**File d'attente avec limite de concurrence.** Prolongement du précédent : on
limite le nombre de workers qui appellent l'IA en même temps, par exemple
trois. Incident visé : le fournisseur qui ralentit sous la charge, et la
protection du reste de l'application. Ce qu'il ne résout pas : si le
fournisseur est en panne, la file grossit sans fin. Il faut un coupe-circuit,
vu en séance 3.

**Limite de temps côté application.** On choisit un délai maximal sur l'appel
HTTP vers le fournisseur, par exemple quinze secondes, plus court que celui du
serveur web et du proxy, au lieu d'hériter des trente secondes du framework,
et on gère l'échec proprement. Le délai de PHP ne joue pas ce rôle : il ne
compte pas le temps passé à attendre le réseau. Incident visé : les requêtes
de 9 h 01 qui occupent un processus trente secondes ou plus pour rien. Ce
qu'il ne résout pas : l'appel interrompu est peut-être quand même facturé côté
fournisseur, et réessayer immédiatement coûte deux fois. La politique de
réessai est un sujet en soi.

**Cache et limites d'entrée.** Deux mesures simples. Le cache : si la note
n'a pas changé, on renvoie le résumé déjà calculé au lieu de rappeler l'IA. La
limite d'entrée : on refuse ou on tronque une note au-delà d'une taille donnée
avant de construire le prompt. Incident visé : le document de deux cents pages
de 9 h 05, et plus largement la facture. Ce qu'il ne résout pas : la qualité
du résumé d'un texte tronqué, et le cas du texte qui change à chaque fois.

**Ce qu'aucune de ces parades ne résout.** L'incident de mardi. Les résumés en
anglais viennent d'un changement de modèle chez le fournisseur. Aucune file
d'attente, aucun délai, aucun cache ne le détecte. Il faut utiliser un
identifiant de modèle figé (pas un alias), mesurer la qualité des réponses
dans le temps, et prévoir la migration : un modèle figé finit toujours par
être retiré. C'est la séance 5.

**Question bonus.** La limite de temps et le cache se mettent en place dans
l'adaptateur `HttpLlmAdapter` ou dans sa configuration, sans que
`SummarizeNote` change. Le traitement en arrière-plan, lui, change le contrat
du cas d'usage : il ne renvoie plus un résumé mais un accusé de réception.
C'est une décision d'architecture, pas un réglage d'adaptateur.

**Erreurs fréquentes.** Proposer « un réessai automatique » contre le blocage de
9 h : il relance un appel lent et payant, il aggrave la charge au lieu de la
réduire. Proposer « plus de processus PHP-FPM » : cela repousse le seuil (mini-exercice
de la section 2.1), le problème revient avec plus de clics. Laisser vide la
colonne « ce qu'elle ne résout pas » : une parade sans limite connue est le
signe que l'incident visé n'est pas clair.

**Comment vérifier votre fiche.** Pour chaque ligne, l'incident cité (9 h,
9 h 01, 9 h 05 ou mardi) doit se retrouver dans la section 2.1, la parade doit
répondre à cet incident et pas à un autre, et la dernière colonne doit nommer
ce qui reste ouvert. Une parade qui ne vise aucun incident précis est trop
vague.

**Et ensuite.** Si vous avez manqué le blocage de 9 h, relisez les sections 2.1
et 2.2 (latence). Pour le délai, relisez 2.3. Pour le coût et pour l'incident de
mardi, relisez 2.2 (coût, dépendance). Les parades se construisent en séance 3,
et le TP S1.3 vous en fait déjà poser deux : un délai choisi sur l'appel et le
modèle épinglé dans la configuration.
