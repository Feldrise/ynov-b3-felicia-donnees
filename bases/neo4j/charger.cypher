// Graphe Félicia : Joueurs, Héros, Clans, îles, Trésors. Les CSV sont copiés dans /var/lib/neo4j/import.
MATCH (n) CALL { WITH n DETACH DELETE n } IN TRANSACTIONS OF 10000 ROWS;
CREATE CONSTRAINT joueur_id IF NOT EXISTS FOR (j:Joueur) REQUIRE j.id_joueur IS UNIQUE;
CREATE CONSTRAINT heros_id IF NOT EXISTS FOR (h:Heros) REQUIRE h.id_heros IS UNIQUE;
CREATE CONSTRAINT clan_id IF NOT EXISTS FOR (c:Clan) REQUIRE c.id_clan IS UNIQUE;
CREATE CONSTRAINT ile_id IF NOT EXISTS FOR (i:Ile) REQUIRE i.id_ile IS UNIQUE;
CREATE CONSTRAINT tresor_id IF NOT EXISTS FOR (t:Tresor) REQUIRE t.id_tresor IS UNIQUE;

LOAD CSV WITH HEADERS FROM 'file:///ile.csv' AS l
CREATE (:Ile {id_ile: toInteger(l.id_ile), nom: l.nom, niveau_requis: toInteger(l.niveau_requis)});

LOAD CSV WITH HEADERS FROM 'file:///joueur.csv' AS l
CALL { WITH l CREATE (:Joueur {id_joueur: toInteger(l.id_joueur), pseudo: l.pseudo, pays: l.pays}) } IN TRANSACTIONS OF 5000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///clan.csv' AS l
MATCH (i:Ile {id_ile: toInteger(l.id_ile_repaire)})
CREATE (c:Clan {id_clan: toInteger(l.id_clan), nom: l.nom, devise: l.devise})-[:A_SON_REPAIRE_SUR]->(i);

LOAD CSV WITH HEADERS FROM 'file:///heros.csv' AS l
CALL {
  WITH l
  MATCH (j:Joueur {id_joueur: toInteger(l.id_joueur)})
  CREATE (j)-[:INCARNE]->(h:Heros {id_heros: toInteger(l.id_heros), nom: l.nom, niveau: toInteger(l.niveau),
          lignee: CASE l.id_lignee WHEN '1' THEN 'Sorcier' WHEN '2' THEN "Rôdeur d'ombre" WHEN '3' THEN 'Gardien' ELSE 'Alchimiste' END})
} IN TRANSACTIONS OF 5000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///heros.csv' AS l
WITH l WHERE l.id_clan IS NOT NULL
MATCH (h:Heros {id_heros: toInteger(l.id_heros)}), (c:Clan {id_clan: toInteger(l.id_clan)})
CREATE (h)-[:MEMBRE_DE {depuis: date(l.date_adhesion)}]->(c);

LOAD CSV WITH HEADERS FROM 'file:///heros.csv' AS l
WITH l WHERE l.id_mentor IS NOT NULL
MATCH (a:Heros {id_heros: toInteger(l.id_heros)}), (m:Heros {id_heros: toInteger(l.id_mentor)})
CREATE (m)-[:MENTOR_DE {depuis: date(l.date_debut_mentorat)}]->(a);

LOAD CSV WITH HEADERS FROM 'file:///clan.csv' AS l
MATCH (h:Heros {id_heros: toInteger(l.id_heros_chef)}), (c:Clan {id_clan: toInteger(l.id_clan)})
CREATE (h)-[:CHEF_DE]->(c);

LOAD CSV WITH HEADERS FROM 'file:///alliance.csv' AS l
MATCH (a:Clan {id_clan: toInteger(l.id_clan_1)}), (b:Clan {id_clan: toInteger(l.id_clan_2)})
CREATE (a)-[:ALLIE_A {depuis: date(l.date_alliance)}]->(b);

LOAD CSV WITH HEADERS FROM 'file:///tresor.csv' AS l
CALL {
  WITH l
  MATCH (h:Heros {id_heros: toInteger(l.id_heros_proprietaire)})
  CREATE (h)-[:POSSEDE]->(:Tresor {id_tresor: toInteger(l.id_tresor), nom: l.nom, nature: l.nature, rarete: l.rarete})
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///duels.csv' AS l
MATCH (v:Heros {id_heros: toInteger(l.id_vainqueur)}), (p:Heros {id_heros: toInteger(l.id_vaincu)})
CREATE (v)-[:A_PRIS_UNE_VIE_A {fois: toInteger(l.nb)}]->(p);
