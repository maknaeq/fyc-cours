---
title: "Budget vidéo"
subtitle: "Projet FYC 2026-2027"
---

<!--
Suivi du budget vidéo (FYC-61). Source du découpage : « Budget vidéo » de
livrables/scenarisation.md (trame V2). Une ligne par vidéo, une issue Linear
par ligne. Mis à jour par la personne qui tourne la vidéo, à chaque vidéo
montée : durée réelle relevée sur le fichier final, au format « 5 min 40 ».
-->

# Contrainte

- Environ 1 h 30 de vidéo au total (consigne FYC), 8 minutes au plus par
  vidéo, vidéos sous-titrées.
- Budget de la trame V2 : **86 minutes** en 15 vidéos, soit
  4 minutes de marge sous l'enveloppe de 90 minutes. La vidéo la
  plus longue dure 8 minutes (conclusion).

# Liste des vidéos

| Ch. | Vidéo | Séq. | Issue | Qui tourne | Échéance | Durée cible | Durée réelle |
|-----|-------|------|-------|------------|----------|-------------|--------------|
| 00 | Présentation du cours, de l'équipe et des pré-requis | 00.1 | FYC-30 | Quentin | fait (12/09) | 3 min | à relever sur le fichier monté |
| 01 | Où placer un appel à une IA dans une appli en couches | S1.1 | FYC-45 | Quentin | 30/11 | 6 min |  |
| 01 | Lecture guidée des deux dépôts Laravel et Spring Boot | S1.1 | FYC-46 | Quentin | 30/11 | 5 min |  |
| 01 | Le timeout réel d'un appel d'IA dans un contrôleur | S1.2 | FYC-47 | Quentin | 30/11 | 3 min |  |
| 01 | Un port, deux fournisseurs, une ligne de config | S1.3 | FYC-48 | Kaan | 30/11 | 5 min |  |
| 02 | La boucle d'agent dessinée pas à pas (sujet complexe n° 1) | S2.2 | FYC-119 | Timothé | 30/11 | 6 min |  |
| 02 | pgvector et la mesure du recall | S2.3 | FYC-120 | Erwin | 30/11 | 6 min |  |
| 03 | Correction du TP, partie 1 (instrumentation) | S3.4 | FYC-72 | Kaan | 30/12 | 6 min |  |
| 03 | Correction du TP, partie 2 (panne simulée) | S3.4 | FYC-121 | Kaan | 30/12 | 6 min |  |
| 03 | Correction du TP, partie 3 (cas de référence) | S3.4 | FYC-122 | Kaan | 30/12 | 6 min |  |
| 04 | Injection indirecte en direct sur l'index (sujet complexe n° 2) | S4.2 | FYC-123 | Timothé | 30/12 | 6 min |  |
| 04 | Tester les garde-fous | S4.3 | FYC-124 | Kaan | 30/12 | 6 min |  |
| 05 | Correction du cas pratique, partie 1 | S5.3 | FYC-93 | Quentin | 30/12 | 7 min |  |
| 05 | Correction du cas pratique, partie 2 | S5.3 | FYC-125 | Quentin | 30/12 | 7 min |  |
| 05 | Conclusion « pour aller plus loin » | S5.3 | FYC-85 | Quentin | 30/12 | 8 min |  |
| | **Total** | | | | | **86 min** | |

Les échéances sont celles de Linear au 26/11/2026 : les vidéos des
chapitres 01 et 02 sont attendues pour la séance 3 (02/12/2026), les autres
pour le dépôt de janvier. Quentin écrit les scripts (`/script-video`) et monte
toutes les vidéos ; chaque membre tourne celles de ses séquences.

# Règles de suivi

- Une vidéo dépasse 8 minutes : on la coupe, ou on la scinde en deux lignes
  de ce tableau.
- Le total des durées réelles ne doit pas dépasser 90 minutes. Si les durées
  réelles dépassent les durées cibles, la marge fond : on la relit à chaque
  mise à jour.
- Le script de chaque vidéo est dans `cours/NN-slug/videos/` (format du guide
  de style).

# Bonus live coding (FYC-36)

Piste suggérée par le mentor (séance 2) : une vidéo de live coding par TP. Il
y a quatre TP (S1.3, S2.4, S3.4, S4.3) pour 4 minutes de marge,
soit une minute par TP si les durées cibles sont tenues. La marge ne permet donc
au mieux qu'une seule vidéo courte, sur un seul TP. Proposition : FYC-36 reste
en réserve, et on ne la rouvre que si le total réel des vidéos tournées
laisse au moins 8 minutes de marge au moment du dernier tournage.
