---
title: Architecture polyglotte et Patch Day
soustitre: Une base par besoin, une source de vérité par donnée
surtitre: Séance 4 · Vendredi 13 novembre, 13h00 à 16h00
public: Support étudiant
---

## La Séance en un coup d'œil

::: bloc
| Heure | Bloc | Ce que vous faites |
|--------------|------------------------------------------|------------------------------------------------------------|
| 13h00 | Apport théorique [30 min]{.duree} | l'architecture polyglotte de Félicia, un exemple d'ADR, la matrice de décision |
| 13h30 | Note 2, conception de la V1 [1 h 30]{.duree} | en trinôme, sur votre Sujet de Note 2 ; dépôt de la V1 à 15h00 ; pause libre |
| 15h00 | Patch Day [45 min]{.duree} | une carte tirée au sort, une V2 adaptée et son ADR |
| 15h45 | Rendu et clôture [15 min]{.duree} | dépôt final sur Moodle, retour à chaud sur le module |
:::

Rien n'est à préparer avant la Séance ni à finir après : tout se fait ici. Les consignes et la grille de la Note 2 sont dans « Note 2 : consignes et grille ».

## De quatre paradigmes à une architecture

Ce matin, chaque paradigme a trouvé son besoin dans Félicia. Il reste à les faire tenir ensemble, et la règle de départ de la grille de choix ne change pas : le relationnel est **le choix par défaut**, et on n'en sort que lorsqu'un critère chiffré l'exige.

::: coupable
Reprenons le tableau « Félicia en production » de la Séance 3, en y ajoutant la décision du studio Griffe & Grimoire :

| Besoin | Chiffres prévus en production | Base retenue | Ligne de la grille |
|------------------------|--------------------------------------|--------------------------|------------|
| Les Trésors | 4,5 millions de Trésors, six natures aux attributs différents, une nouvelle nature à chaque Saison | MongoDB, pour les fiches des Trésors | 1 · structure |
| Classement et Vies | 45 000 Héros connectés le soir, 2 000 gains de Renommée par seconde, classement affiché en moins de 50 ms | Redis, pour le classement et l'affichage des Vies restantes | 3 · latence |
| Télémétrie des Vies perdues | environ 2 milliards de lignes par Saison, trois régions, jamais modifiées | Cassandra | 2 · volume |
| Réseau des Clans | 9 000 Clans, 25 000 alliances, chemins à profondeur variable | PostgreSQL aujourd'hui ; Neo4j quand le chemin diplomatique sera demandé (ADR-005) | 5 · relations |
| Joueurs, Héros, Clans, bourse de Pelotes d'or, boutique, Vies perdues | quelques millions de lignes, des achats à garantir tout ou rien | PostgreSQL, **source de vérité** | 4 · transactions |
:::

Le studio n'a pas cinq bases parce qu'il y a cinq paradigmes : il en a quatre, et la cinquième attend un besoin chiffré.

## La source de vérité

Une même donnée vit souvent à plusieurs endroits : la Renommée d'un Héros est dans PostgreSQL et dans le classement Redis, le nom de son Clan est recopié dans MongoDB. Il faut alors décider **quelle copie fait foi** en cas de désaccord.

::: coupable
::: bloc
**Une donnée, une source de vérité.** Pour chaque donnée, une seule base l'écrit en premier et fait foi. Les autres en gardent une **copie**, alimentée depuis la source et jamais modifiée à la main. Si une copie est perdue, on la reconstruit depuis la source.
:::

| Donnée de Félicia | Source de vérité | Copies | Pourquoi là |
|----------------------|------------|--------------------|----------------------------------------------|
| Joueurs, Héros, Clans, alliances | PostgreSQL | MongoDB (nom du Clan dans chaque Héros), Neo4j plus tard | règles de gestion à garantir : un Clan d'au plus cinquante Héros, un chef membre de son Clan |
| Bourse et mouvements de Pelotes d'or | PostgreSQL | aucune | une bourse jamais négative, un achat tout ou rien |
| Vies perdues (le fait : qui, quand, où, numéro) | PostgreSQL | Redis (Vies restantes), Cassandra (entrée de la télémétrie) | au plus 9 par Héros et par Saison : la règle exige une transaction, et elle borne le volume à quelques millions de lignes par Saison |
| Trace des 30 dernières secondes avant une Vie perdue | Cassandra | aucune | 2 milliards de lignes par Saison : seule Cassandra les absorbe |
| Attributs des Trésors, selon leur nature | MongoDB | aucune | attributs variables selon la nature, une nature nouvelle à chaque Saison ; le **propriétaire** et l'historique des propriétaires d'un légendaire, eux, restent dans PostgreSQL, puisqu'ils changent par un achat ou un échange, et sont recopiés dans la fiche MongoDB |
| Renommée et classement de la Saison | PostgreSQL | Redis (classement) | Redis trie, PostgreSQL garde la valeur qui fait foi pour les récompenses de fin de Saison |
| Convalescence (60 secondes) | Redis | aucune | une donnée éphémère, qui expire seule ; la perdre au redémarrage ne coûte qu'une minute d'attente évitée |
:::

Le cas des Vies montre la règle à l'œuvre. Le compteur de Vies restantes est dans Redis, parce qu'il s'affiche 45 000 fois par seconde ; mais la décision « ce Héros perd-il sa dernière Vie ? » se prend dans PostgreSQL, en transaction, parce qu'un Héros ne doit jamais perdre une dixième Vie. C'est la ligne du tableau CAP de la Séance 3 : cohérence pour la dernière Vie, disponibilité pour le classement.

::: {.encadre .astuce}
### À vérifier dans votre Codespace (facultatif)

Moustique le Gourmand (Héros 3426) a perdu une Vie dans la Saison 4. La source et ses deux copies le disent toutes les trois :

- dans `make psql` : `SELECT count(*) FROM vie_perdue WHERE id_heros = 3426 AND id_saison = 4;` donne 1 ;
- dans `make redis-cli` : `HGET heros:3426 vies_restantes` donne 8 ;
- dans `make cqlsh` : `SELECT count(*) FROM vies_par_heros WHERE id_heros = 3426 AND id_saison = 4;` donne 1.

Le jeu de données a été chargé d'un coup, donc les trois sont d'accord. En production, la copie Redis et la copie Cassandra suivent la source avec un léger retard : c'est la cohérence à terme.
:::

## La synchronisation par événements

Comment les copies suivent-elles la source ? La solution naïve, la **double écriture**, fait écrire l'application dans PostgreSQL puis dans Redis. Si la seconde écriture échoue (Redis redémarre, le réseau coupe), la copie diverge sans que personne le sache.

Félicia procède autrement, en trois temps :

1. **La source écrit, et note l'événement dans la même transaction.** Quand Moustique perd une Vie, PostgreSQL enregistre la ligne de `vie_perdue` et, dans la même transaction, une ligne dans une table d'événements à publier : « ViePerdue, Héros 3426, Saison 4, numéro 2 ». Les deux réussissent ou échouent ensemble.
2. **Un relais publie l'événement** dans une file d'événements (Kafka, RabbitMQ ou Redis Streams, par exemple), puis le marque comme publié.
3. **Chaque copie s'abonne** aux événements qui la concernent et se met à jour : Redis décrémente les Vies restantes, Cassandra ajoute l'entrée de télémétrie. Un abonné qui reçoit deux fois le même événement (son identifiant le trahit) l'ignore : on peut rejouer la file sans risque.

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

La trace des 30 dernières secondes ne passe pas par PostgreSQL : le serveur de jeu l'écrit directement dans Cassandra, qui en est la source. Faire transiter 2 milliards de lignes par Saison par la source relationnelle reviendrait à lui rendre le problème qu'on voulait lui enlever.

## La cohérence à terme

Entre l'écriture dans la source et la mise à jour d'une copie, il s'écoule un délai : quelques millisecondes d'habitude, quelques secondes sous forte charge, davantage si un abonné est en panne. Pendant ce délai, la copie est périmée. Elle finira par rattraper la source, une fois les événements appliqués : c'est la **cohérence à terme**.

Elle se choisit **copie par copie**, en répondant à deux questions : quel retard est acceptable, et que voit le joueur pendant ce retard ?

| Copie | Retard accepté | Ce que voit le Joueur pendant le retard | Acceptable ? |
|----------------------|------------|------------------------------|------------------------------------|
| Classement de la Saison (Redis) | quelques secondes | son rang d'il y a deux secondes | oui : personne ne s'en aperçoit |
| Vies restantes affichées (Redis) | une seconde | 2 Vies au lieu d'une, juste après sa chute | oui, pour l'affichage seulement : l'autorisation de continuer à jouer exige la valeur exacte, décidée dans PostgreSQL |
| Télémétrie (Cassandra) | quelques minutes | rien : seuls les concepteurs la lisent | oui |
| Alliances (Neo4j, plus tard) | une minute | un chemin diplomatique qui passe par une alliance rompue | oui, si la rupture est revérifiée dans PostgreSQL avant toute action |
| Bourse de Pelotes d'or | aucun | | **non** : pas de copie, on lit la source |

C'est la conclusion laissée en suspens par « Demande au Familier » ce matin : parmi les coûts d'une copie graphe, le Familier citait « la gestion des retards, erreurs et incohérences de cette copie », sans les chiffrer. Le travail du concepteur est de **chiffrer** ce décalage et de dire ce qu'il coûte au Joueur.

## Le coût d'exploitation

::: compact
Chaque base ajoutée se paie tous les mois, longtemps après la décision. Voici, en ordres de grandeur, ce que le studio a estimé pour Félicia (des chiffres fictifs, mais réalistes) :

| Base | Ce qu'il faut faire tourner | Exploitation estimée |
|---------------------|-----------------------------------------------------|--------------------------|
| PostgreSQL | un serveur principal et deux réplicas, sauvegardes, montées de version | 2 jours par mois |
| MongoDB | un jeu de trois serveurs répliqués, index, sauvegardes | 1,5 jour par mois |
| Redis | deux serveurs (principal et secours) ; rien à sauvegarder, tout se reconstruit depuis PostgreSQL | 1 jour par mois |
| Cassandra | six serveurs sur trois régions, réparations régulières, ajout de serveurs au fil de la Saison | 4 jours par mois |
| Neo4j (s'il est ajouté) | un serveur et son abonné à la file d'événements | 1,5 jour par mois |
| File d'événements et relais | un service de plus, à surveiller comme une base | 1 jour par mois |
:::

À ces jours s'ajoutent des coûts moins visibles : une compétence de plus à recruter ou à former, une astreinte de plus la nuit, un abonné de plus qui peut tomber en panne. C'est pourquoi Neo4j attend : tant que la seule question posée est celle des alliés d'alliés (profondeur 2), la requête SQL y répond en quelques millisecondes, même à 9 000 Clans et 25 000 alliances, et 1,5 jour par mois n'achète rien.

::: bloc
**La question à se poser pour chaque base** : quel critère chiffré de la grille l'exige, et le gain vaut-il ses jours d'exploitation ? Si vous ne savez pas répondre, la donnée reste dans la source relationnelle.
:::

## L'ADR et la matrice

::: compact
Deux documents accompagnent une architecture :

- **La matrice « besoin → paradigme → justification »**, une ligne par besoin : elle montre que chaque base répond à un critère chiffré.
- **L'ADR** (*Architecture Decision Record*, ou fiche de décision d'architecture) : une page par décision importante, qui garde la trace du contexte, des options écartées et de ce qu'on a accepté de perdre. Dans six mois, quand quelqu'un demandera « pourquoi Neo4j ? », la réponse sera écrite.
:::

L'exemple d'ADR rédigé sur Félicia, le modèle d'ADR et le modèle de matrice sont dans « ADR et matrice de décision », avec les deux fichiers Word à remplir pendant la Note 2.

## Le Patch Day et le Familier {.nouvelle-page}

À 15h00, chaque groupe tire une carte : un événement imprévu, chiffré, que le studio de votre jeu annonce. Le Familier peut vous aider à explorer des pistes ; donnez-lui les chiffres de la carte et ceux de votre sujet, et demandez-lui ses hypothèses (les règles de la Clinique de ce matin). Mais l'ADR justifie le choix par **vos** contraintes, et le Journal du Familier dit ce que vous avez gardé, rejeté ou modifié, et pourquoi.
