---
title: Groupe expert graphe
soustitre: Le réseau des Clans de Félicia dans Neo4j, quatre Tickets du Game Designer guidés
surtitre: Séance 3 · Groupes experts, 9h10 à 10h10
public: Support étudiant
---

## Votre heure

::: bloc
| Quand | Quoi |
|---------------|--------------------------------------------------------------|
| 9h10 [5 min]{.duree} | Codespace ouvert, bases démarrées (`make etat`), terminal Neo4j ouvert, lecture de la fiche |
| 9h15 [35 min]{.duree} | Tickets 1 à 4, chacun sur son Codespace, en s'entraidant ; le Ticket bonus si vous avez fini |
| 9h50 [15 min]{.duree} | fiche synthèse du groupe : cas d'usage, requête type, limites |
| 10h05 [5 min]{.duree} | chacun répète à voix haute le début de sa présentation de 8 minutes |
:::

Ouvrez le terminal Neo4j avec `make cypher-shell`. Pour sortir : `:exit`. Chaque requête se termine par un point-virgule ; les `___` sont à remplacer.

::: encadre
### Rappel du modèle

Nœuds : `Joueur`, `Heros`, `Clan`, `Ile`, `Tresor`, chacun avec son identifiant (`id_heros`, `id_clan`...) et son `nom` (`pseudo` pour un Joueur).
Relations : `(Joueur)-[:INCARNE]->(Heros)`, `(Heros)-[:MEMBRE_DE]->(Clan)`, `(Heros)-[:CHEF_DE]->(Clan)`, `(Clan)-[:ALLIE_A]-(Clan)`, `(Heros)-[:MENTOR_DE {depuis}]->(Heros)` (du mentor vers l'apprenti, avec la date de début du mentorat), `(Heros)-[:POSSEDE]->(Tresor)`, `(Heros)-[:A_PRIS_UNE_VIE_A {fois}]->(Heros)` (duels, toutes Saisons confondues), `(Clan)-[:A_SON_REPAIRE_SUR]->(Ile)`.
Une alliance n'a pas de sens : on l'écrit sans flèche, `-[:ALLIE_A]-`.
:::

## Ticket 1 · Quels Clans sont à deux alliances du nôtre ? [8 min]{.duree}

> « Les Ronronneurs d'Argent (Clan 4) préparent une grande expédition. Ils veulent savoir qui sont leurs alliés, puis les alliés de leurs alliés, pour leur proposer de se joindre à eux. »
> — le studio

1. Les alliés directs :

```cypher
MATCH (c:Clan {id_clan: ___})-[:ALLIE_A]-(allie:Clan) RETURN allie.nom;
```

2. Les Clans à deux alliances exactement, sans le Clan lui-même ni ses alliés directs :

```cypher
MATCH (c:Clan {id_clan: 4})-[:ALLIE_A*___]-(autre:Clan) WHERE autre <> c AND NOT (c)-[:ALLIE_A]-(autre) RETURN DISTINCT autre.nom;
```

**Pour vérifier** : deux alliés, puis six Clans.

**Pour la fiche** : que faut-il changer pour aller à trois alliances ? Et en SQL (voir `demonstrations/s3/4-postgres-alliances.sql`) ?

## Ticket 2 · Les mentors venus d'ailleurs [8 min]{.duree}

> « Certains apprentis du Cercle de l'Aube (Clan 1) sont formés par un mentor qui n'est pas de leur Clan. Le chef veut la liste : apprenti et mentor. »
> — le studio

```cypher
MATCH (m:Heros)-[:MENTOR_DE]->(a:Heros)-[:MEMBRE_DE]->(c:Clan {id_clan: 1}) WHERE NOT (m)-[:___]->(c) RETURN a.nom AS apprenti, m.nom AS mentor;
```

**Pour vérifier** : huit lignes.

**Pour la fiche** : lisez la requête à voix haute, de gauche à droite. Combien de jointures faudrait-il en SQL ?

## Ticket 3 · Le chemin diplomatique [7 min]{.duree}

> « Les Ronronneurs d'Argent (Clan 4) veulent approcher le Cercle de l'Aube (Clan 1), avec qui ils n'ont aucune alliance. Par quels Clans passer, au plus court ? »
> — le studio

```cypher
MATCH p = shortestPath((a:Clan {id_clan: 4})-[:ALLIE_A*]-(b:Clan {id_clan: ___})) RETURN length(p) AS alliances, [c IN nodes(p) | c.nom] AS chemin;
```

**Pour vérifier** : six alliances.

**Pour la fiche** : le `*` sans limite suit autant d'alliances qu'il le faut. En SQL, une requête récursive (`WITH RECURSIVE`) y arrive aussi : pourquoi est-elle plus coûteuse à écrire, et à exécuter ?

## Ticket 4 · Les alliances trahies [10 min]{.duree} {.nouvelle-page}

> « On soupçonne des duels entre Clans alliés. Sur tout l'archipel, combien de Vies des Héros ont-ils prises en duel à des Héros d'un Clan allié au leur ? »
> — le studio

Dessinez le motif : la victime est membre d'un Clan, le vainqueur d'un autre Clan, et ces deux Clans sont alliés. Additionnez la propriété `fois` de la relation de duel.

```cypher
MATCH (cv:Clan)<-[:MEMBRE_DE]-(victime:Heros)<-[r:A_PRIS_UNE_VIE_A]-(vainqueur:Heros)-[:MEMBRE_DE]->(ca:Clan)-[:___]-(cv) RETURN sum(r.___) AS vies;
```

**Pour vérifier** : un nombre entre 30 et 40.

**Pour la fiche** : ce motif relie cinq éléments. Quelle partie de la question relève du graphe, et quelle partie relèverait plutôt de la télémétrie des Vies perdues ?

## Ticket bonus · Les Clans isolés

> « Quels Clans n'ont aucune alliance ? On veut leur proposer un parrainage. »
> — le studio

Cherchez les Clans pour lesquels le motif `(c)-[:ALLIE_A]-()` n'existe pas (`WHERE NOT ...`). Puis comptez les duels entre membres d'un **même** Clan.

## Votre fiche synthèse [15 min]{.duree}

Remplissez la fiche synthèse (document à part) : deux cas d'usage sur Félicia, une requête type que vous savez expliquer, deux forces, deux limites, et un besoin pour lequel vous **ne** choisiriez **pas** le graphe. C'est votre support pour les 8 minutes de la redistribution.
