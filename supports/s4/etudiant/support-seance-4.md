---
title: Architecture polyglotte et Patch Day
soustitre: Une base par besoin, une source de vérité par donnée
surtitre: Séance 4 · Vendredi 13 novembre, 13h00 à 16h00
public: Support étudiant
---

## Au programme

Apport (30 min), V1 de la Note 2 en trinôme (1 h 30, pause libre, **dépôt à 15h00**), Patch Day (45 min), rendu et retour à chaud (15 min).

Rien à préparer avant, rien à finir après. Consignes et grille : « Note 2 : consignes et grille ».

## De quatre paradigmes à une architecture

Ce matin, chaque paradigme a trouvé son besoin dans Félicia. Reste à les faire tenir ensemble, sans oublier que le relationnel est **le choix par défaut**.

::: coupable
Le tableau « Félicia en production » de la Séance 3, avec la décision du studio :

| Besoin | Chiffres prévus en production | Base retenue | Ligne de la grille |
|------------------------|--------------------------------------|--------------------------|------------|
| Les Trésors | 4,5 millions de Trésors, six natures aux attributs différents, une nouvelle nature à chaque Saison | MongoDB, pour les fiches des Trésors | 1 · structure |
| Classement et Vies | 45 000 Héros connectés le soir, 2 000 gains de Renommée par seconde, classement affiché en moins de 50 ms | Redis, pour le classement et l'affichage des Vies restantes | 3 · latence |
| Télémétrie des Vies perdues | environ 2 milliards de lignes par Saison, trois régions, jamais modifiées | Cassandra | 2 · volume |
| Réseau des Clans | 9 000 Clans, 25 000 alliances, chemins à profondeur variable | PostgreSQL aujourd'hui ; Neo4j quand le chemin diplomatique sera demandé (ADR-005) | 5 · relations |
| Joueurs, Héros, Clans, bourse de Pelotes d'or, boutique, Vies perdues | quelques millions de lignes, des achats à garantir tout ou rien | PostgreSQL, **source de vérité** | 4 · transactions |
:::

Cinq paradigmes, quatre bases : la cinquième attend un besoin chiffré.

## La source de vérité

La Renommée d'un Héros est dans PostgreSQL et dans Redis. Si les deux divergent, laquelle croire ?

::: coupable
::: bloc
**Une donnée, une source de vérité.** Une seule base écrit la donnée et fait foi. Les autres en gardent une **copie**, alimentée depuis la source, jamais modifiée à la main, reconstruite depuis la source si on la perd.
:::

| Donnée de Félicia | Source de vérité | Copies | Pourquoi là |
|----------------------|------------|--------------------|----------------------------------------------|
| Joueurs, Héros, Clans, alliances | PostgreSQL | MongoDB (nom du Clan dans chaque Héros), Neo4j plus tard | règles de gestion à garantir : un Clan d'au plus cinquante Héros, un chef membre de son Clan |
| Bourse et mouvements de Pelotes d'or | PostgreSQL | aucune | une bourse jamais négative, un achat tout ou rien |
| Vies perdues (le fait : qui, quand, où, numéro) | PostgreSQL | Redis (Vies restantes), Cassandra (entrée de la télémétrie) | au plus 9 par Héros et par Saison : une transaction, et quelques millions de lignes par Saison au plus |
| Trace des 30 dernières secondes avant une Vie perdue | Cassandra | aucune | 2 milliards de lignes par Saison : seule Cassandra les absorbe |
| Attributs des Trésors, selon leur nature | MongoDB | aucune | attributs variables selon la nature, une nature nouvelle à chaque Saison ; le **propriétaire** et l'historique des propriétaires d'un légendaire restent dans PostgreSQL (ils changent par un achat ou un échange) et sont recopiés dans la fiche |
| Renommée et classement de la Saison | PostgreSQL | Redis (classement) | Redis trie, PostgreSQL garde la valeur qui fait foi pour les récompenses de fin de Saison |
| Convalescence (60 secondes) | Redis | aucune | éphémère, elle expire seule ; la perdre au redémarrage ne coûte qu'une minute d'attente évitée |
:::

Prends les Vies : Redis affiche le compteur (45 000 fois par seconde), PostgreSQL décide de la dernière en transaction, pour qu'aucun Héros n'en perde une dixième. C'est le CAP de la Séance 3 : cohérence pour la dernière Vie, disponibilité pour le classement.

::: {.encadre .astuce}
### À vérifier dans votre Codespace (facultatif)

Moustique le Gourmand (Héros 3426) a perdu une Vie en Saison 4. La source et ses deux copies le disent :

- dans `make psql` : `SELECT count(*) FROM vie_perdue WHERE id_heros = 3426 AND id_saison = 4;` donne 1 ;
- dans `make redis-cli` : `HGET heros:3426 vies_restantes` donne 8 ;
- dans `make cqlsh` : `SELECT count(*) FROM vies_par_heros WHERE id_heros = 3426 AND id_saison = 4;` donne 1.

Le jeu de données a été chargé d'un coup, donc les trois sont d'accord. En production, Redis et Cassandra suivent la source avec un léger retard : c'est la cohérence à terme.
:::

## La synchronisation par événements

Écrire dans PostgreSQL puis dans Redis, la **double écriture**, est un piège : si la seconde échoue, la copie diverge en silence. Félicia procède en trois temps :

1. **La source écrit la donnée et l'événement dans la même transaction** : la ligne de `vie_perdue` et « ViePerdue, Héros 3426, Saison 4, numéro 2 » réussissent ou échouent ensemble.
2. **Un relais publie l'événement** dans une file (Kafka, RabbitMQ, Redis Streams…).
3. **Chaque copie s'abonne** et se met à jour. Un événement reçu deux fois se reconnaît à son identifiant et s'ignore : on peut rejouer la file sans risque.

```
  serveur de jeu ──écrit──> PostgreSQL (source de vérité)
                              │  même transaction : vie_perdue + événement à publier
                              ▼
                            relais ──publie──> file d'événements
                                                 │
                     ┌───────────────────────────┼───────────────────────┐
                     ▼                           ▼                       ▼
            Redis : Vies restantes     Cassandra : télémétrie     Neo4j : alliances
            et classement (< 1 s)      (< 5 s)                    (plus tard, < 1 min)
```

La trace des 30 dernières secondes va directement dans Cassandra, qui en est la source : la faire passer par PostgreSQL lui rendrait les 2 milliards de lignes qu'on voulait lui enlever.

## La cohérence à terme

Entre la source et la copie, il s'écoule quelques millisecondes, quelques secondes sous charge, plus si un abonné tombe : la copie est périmée, puis rattrape la source. C'est la **cohérence à terme**, et elle se choisit copie par copie : quel retard accepter, que voit le Joueur pendant ce temps ?

| Copie | Retard accepté | Ce que voit le Joueur pendant le retard | Acceptable ? |
|----------------------|------------|------------------------------|------------------------------------|
| Classement de la Saison (Redis) | quelques secondes | son rang d'il y a deux secondes | oui : personne ne s'en aperçoit |
| Vies restantes affichées (Redis) | une seconde | 2 Vies au lieu d'une, juste après sa chute | oui, pour l'affichage seulement : l'autorisation de continuer à jouer exige la valeur exacte, décidée dans PostgreSQL |
| Télémétrie (Cassandra) | quelques minutes | rien : seuls les concepteurs la lisent | oui |
| Alliances (Neo4j, plus tard) | une minute | un chemin diplomatique qui passe par une alliance rompue | oui, si la rupture est revérifiée dans PostgreSQL avant toute action |
| Bourse de Pelotes d'or | aucun | | **non** : pas de copie, on lit la source |

Ce matin, le Familier citait « la gestion des retards, erreurs et incohérences de cette copie » sans les chiffrer. Ton travail, c'est de les **chiffrer**.

## Le coût d'exploitation

::: compact
Chaque base se paie tous les mois, longtemps après la décision. Les estimations du studio (fictives, mais réalistes) :

| Base | Ce qu'il faut faire tourner | Exploitation estimée |
|---------------------|-----------------------------------------------------|--------------------------|
| PostgreSQL | un serveur principal et deux réplicas, sauvegardes, montées de version | 2 jours par mois |
| MongoDB | un jeu de trois serveurs répliqués, index, sauvegardes | 1,5 jour par mois |
| Redis | deux serveurs (principal et secours) ; rien à sauvegarder, tout se reconstruit depuis PostgreSQL | 1 jour par mois |
| Cassandra | six serveurs sur trois régions, réparations régulières, ajout de serveurs au fil de la Saison | 4 jours par mois |
| Neo4j (s'il est ajouté) | un serveur et son abonné à la file d'événements | 1,5 jour par mois |
| File d'événements et relais | un service de plus, à surveiller comme une base | 1 jour par mois |
:::

Plus une compétence à former, une astreinte de nuit, un abonné qui peut tomber. D'où l'attente de Neo4j : tant que la seule question est celle des alliés d'alliés (profondeur 2), le SQL répond en quelques millisecondes, et 1,5 jour par mois n'achète rien. Un chat ne remplit pas neuf gamelles « au cas où ».

::: bloc
**Pour chaque base** : quel critère chiffré de la grille l'exige, et le gain vaut-il ses jours d'exploitation ? Sans réponse, la donnée reste dans le relationnel.
:::

## L'ADR et la matrice

La **matrice « besoin → paradigme → justification »** montre que chaque base répond à un critère chiffré. L'**ADR** (*Architecture Decision Record*) garde sur une page le contexte d'une décision, les options écartées et ce qu'on a accepté de perdre. Exemple et modèles Word : « ADR et matrice de décision ».

## Le Patch Day et le Familier

À 15h00, chaque groupe tire une carte : un événement imprévu et chiffré. Donnez au Familier les chiffres de la carte et du sujet, il vous ouvrira des pistes ; mais l'ADR justifie le choix par **vos** contraintes, et le Journal du Familier dit ce que vous en avez gardé, rejeté ou modifié, et pourquoi.
