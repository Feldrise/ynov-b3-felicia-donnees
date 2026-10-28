-- Séance 3, démonstration 4 (comparaison) : les alliés d'alliés du Cercle de l'Aube en SQL (PostgreSQL).
-- Ouvrir le terminal : make psql. Même résultat que l'étape 2 de 4-neo4j-clans.cypher.
-- L'alliance est rangée une seule fois par paire : il faut d'abord la rendre symétrique, puis joindre la table à elle-même.
-- Une alliance de plus dans la question, c'est une jointure de plus dans la requête.
WITH a AS (SELECT id_clan_1 AS x, id_clan_2 AS y FROM alliance UNION SELECT id_clan_2, id_clan_1 FROM alliance)
SELECT DISTINCT c.nom
FROM a a1 JOIN a a2 ON a2.x = a1.y JOIN clan c ON c.id_clan = a2.y
WHERE a1.x = 1 AND a2.y <> 1 AND a2.y NOT IN (SELECT y FROM a WHERE x = 1);
