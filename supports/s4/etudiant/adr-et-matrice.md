---
title: ADR et matrice de décision
soustitre: Un exemple d'ADR rédigé sur Félicia, et les deux modèles de la Note 2
surtitre: Séance 4 · Apport théorique et Note 2
public: Support étudiant
---

## À quoi sert un ADR

Un **ADR** (*Architecture Decision Record*, fiche de décision d'architecture) garde sur une page la trace d'**une** décision importante : le contexte qui l'a imposée, le choix, les options écartées et ce qu'on a accepté de perdre. Quand la décision change, on ne le réécrit pas : on en écrit un nouveau, qui le **remplace**.

::: bloc
Un bon ADR a un contexte chiffré, qu'un lecteur absent comprend ; une décision, en une ou deux phrases ; au moins deux options écartées, chacune avec sa raison, sans quoi on ne voit pas qu'il y a eu un choix ; et des conséquences honnêtes : le gain, la perte acceptée, le coût d'exploitation.
:::

## Le modèle d'ADR

Le modèle du Patch Day est sur Moodle (`adr-modele.docx`) : il reprend les rubriques de l'exemple ci-dessous et dit quoi écrire dans chacune. Le vôtre peut tenir **en puces**, une idée par puce avec ses chiffres. Titrez-le « ADR-1 · » suivi de la décision (« La boutique reste dans PostgreSQL et... »), et faites répondre la décision à la ligne « L'ADR doit trancher » de votre carte.

## Un exemple rédigé : ADR-005 de Félicia

Il prolonge la « Demande au Familier » de la Séance 3 : pour le chemin diplomatique, le Familier jugeait PostgreSQL suffisant, à condition de « valider son temps de réponse sur des données représentatives ». La mesure a été faite.

::: encadre
### ADR-005 · Le réseau des Clans est copié dans Neo4j pour le chemin diplomatique

**Statut** : accepté, au lancement de la Saison 5. Ne remplace aucun ADR.

**Contexte.** La Saison 5 ouvre les ambassades : un Clan peut envoyer un émissaire à n'importe quel autre Clan, à condition qu'une chaîne d'alliances les relie, et le jeu affiche la chaîne la plus courte. En production : 9 000 Clans, 25 000 alliances, environ 300 demandes par minute le soir, réponse attendue en moins de 200 ms. La profondeur n'est pas limitée. Aujourd'hui, les alliances sont dans PostgreSQL, source de vérité, et la requête des alliés d'alliés (profondeur 2) y répond en quelques millisecondes.

**Décision.** Le réseau des Clans (Clans, alliances) est copié dans Neo4j, qui calcule le chemin le plus court. PostgreSQL reste la source de vérité : Neo4j est alimenté par les événements AllianceConclue, AllianceRompue, ClanFondé et ClanDissous, publiés par la file d'événements existante. Le retard accepté est d'une minute. Avant d'envoyer l'émissaire, le jeu revérifie dans PostgreSQL chaque alliance du chemin.

**Options écartées.**

1. *Requête récursive dans PostgreSQL* (`WITH RECURSIVE`) : à 25 000 alliances, le nombre de chemins explorés croît très vite avec la profondeur ; au-delà de quatre niveaux, nos essais dépassent la seconde. Grille, ligne 5 · relations.
2. *Table précalculée de toutes les distances entre Clans*, dans PostgreSQL : 9 000 Clans donnent jusqu'à 40 millions de paires, à recalculer en partie à chaque alliance conclue ou rompue, soit plusieurs fois par minute le soir.
3. *Calcul dans le serveur de jeu*, sur les alliances chargées en mémoire : rapide, mais chaque serveur garde sa propre copie, sans mécanisme commun de mise à jour ; c'est une base cachée, sans sauvegarde ni surveillance.

**Conséquences.**

- *Gain* : le chemin le plus court en quelques millisecondes, quelle que soit sa longueur.
- *Perte acceptée* : jusqu'à une minute de retard sur les alliances ; un chemin peut passer par une alliance rompue depuis moins d'une minute, ce que la revérification dans PostgreSQL rattrape.
- *Coût* : 1,5 jour d'exploitation par mois, un abonné de plus à surveiller. Si l'abonné tombe en panne, la copie se fige : une alerte se déclenche au-delà de 5 minutes de retard, et la copie se reconstruit entièrement depuis PostgreSQL en quelques minutes.

**Familier.** Sa réponse au prompt chiffré de la Séance 3 concluait que PostgreSQL suffisait, sous réserve de mesurer (Journal du Familier, ligne 2 : modifiée, parce que la mesure dépasse la seconde au-delà de quatre niveaux). Les coûts de la copie qu'il listait sans les chiffrer (synchronisation, retards, incohérences) sont repris dans les conséquences : une minute de retard, une revérification, une alerte.
:::

## La matrice « besoin → paradigme → justification » {.nouvelle-page}

Le modèle de la V1 est sur Moodle : `matrice-de-decision-modele.docx`. Voici deux lignes pour Félicia ; la première reprend l'exemple de justification de la grille de choix.

| N° | Besoin : la question et sa fréquence | Chiffres décisifs | Paradigme et base | Justification : ligne de la grille et chiffre | Source de vérité et synchronisation | Ce qu'on accepte de perdre |
|---|-------------------|--------------|----------|----------------------|------------------|--------------|
| 1 | Télémétrie des Vies perdues : « où meurt-on sur cette Île cette Saison ? », « le journal d'un Héros » | 2 milliards de lignes par Saison, trois régions, jamais modifiées | colonne, Cassandra | 2 · volume : 2 milliards de lignes ; 1 · structure : questions connues, d'où les clés de partition ; 4 · disponibilité préférée | Cassandra pour la trace ; l'entrée de chaque Vie arrive de PostgreSQL par événement, moins de 5 s | une question imprévue demande une nouvelle table ; chaque Vie est écrite deux fois |
| 2 | Bourse de Pelotes d'or : débiter un achat, 3 000 achats par heure le soir | une bourse jamais négative, tout ou rien | relationnel, PostgreSQL | 4 · transactions : débit, attribution du Trésor et vente, tout ou rien ; 2 · volume modeste, moins d'un achat par seconde | PostgreSQL, source de vérité ; aucune copie | rien : c'est le choix par défaut |

::: {.encadre .attention}
### Les erreurs de matrice les plus fréquentes

- Une justification **sans chiffre** (« MongoDB est flexible ») ou **sans ligne de la grille** (« c'est plus rapide »).
- Une base par besoin, sans se demander si la source relationnelle suffisait.
- Une « source de vérité » vide : deux bases écrivent la même donnée, laquelle croire ?
- « Rien » dans « ce qu'on accepte de perdre » pour un autre paradigme que le relationnel : chaque choix a un prix.
:::
