// Séance 3, démonstration 4 : le réseau des Clans en graphe (Neo4j), 9 minutes.
// Ouvrir le terminal : make cypher-shell. Copier les requêtes une par une.
// Chaque requête est rejouée par `make verify` (verification/requetes/04-s3-demonstrations.toml).

// 1. Les alliés du Cercle de l'Aube : on dessine le motif, nœud - relation - nœud.
MATCH (c:Clan {id_clan: 1})-[:ALLIE_A]-(allie:Clan) RETURN allie.nom;

// 2. Les alliés d'alliés : les Clans à deux alliances du nôtre, sans compter nos alliés directs.
//    Le *2 suffit à suivre deux relations ; la même question en SQL est dans 4-postgres-alliances.sql.
MATCH (c:Clan {id_clan: 1})-[:ALLIE_A*2]-(autre:Clan) WHERE autre <> c AND NOT (c)-[:ALLIE_A]-(autre) RETURN DISTINCT autre.nom;

// 3. Le chemin diplomatique le plus court vers les Enfants des Étoiles Filantes (Clan 2), quelle que soit sa longueur.
MATCH p = shortestPath((a:Clan {id_clan: 1})-[:ALLIE_A*]-(b:Clan {id_clan: 2})) RETURN length(p) AS alliances, [c IN nodes(p) | c.nom] AS chemin;

// 4. Un motif plus riche : les Joueurs qui ont un Héros dans le Cercle de l'Aube et un autre dans un Clan ni allié ni le nôtre.
//    Un espion possible : Joueur, Héros, Clans et alliances dans une seule requête.
MATCH (j:Joueur)-[:INCARNE]->(:Heros)-[:MEMBRE_DE]->(c:Clan {id_clan: 1}), (j)-[:INCARNE]->(:Heros)-[:MEMBRE_DE]->(autre:Clan) WHERE autre <> c AND NOT (c)-[:ALLIE_A]-(autre) RETURN count(DISTINCT j) AS joueurs;

// 5. La limite : le graphe ne garde que les relations utiles. Les Vies perdues n'y sont pas, seulement les duels agrégés :
//    « où les Héros perdent-ils leurs Vies ? » n'est pas une question pour lui. Il sait dire qui a déjà pris une Vie
//    à Moustique en duel, toutes Saisons confondues, mais pas où ni quand.
MATCH (v:Heros)-[r:A_PRIS_UNE_VIE_A]->(:Heros {id_heros: 3426}) RETURN v.nom, r.fois;
