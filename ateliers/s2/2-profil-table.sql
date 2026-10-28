-- Atelier de dénormalisation (Séance 2) · Script 2 : une table dénormalisée, une ligne par Héros.
-- Tout ce que l'écran de profil affiche est calculé une fois pour toutes et recopié dans profil_heros.
-- Exécution : make sql F=ateliers/s2/2-profil-table.sql

\timing on

DROP TABLE IF EXISTS profil_heros;

-- Construction : on paie ici, une fois, le calcul de tous les profils.
CREATE TABLE profil_heros AS
SELECT h.id_heros, h.nom AS heros, j.pseudo AS joueur, l.nom AS lignee, h.niveau, h.renommee,
       c.nom AS clan, m.nom AS mentor,
       9 - coalesce(v.nb, 0) AS vies_restantes,
       coalesce(t.bourse, 0) AS bourse,
       coalesce(r.nb, 0) AS nb_tresors
FROM heros h
JOIN joueur j ON j.id_joueur = h.id_joueur
JOIN lignee l ON l.id_lignee = h.id_lignee
LEFT JOIN clan c ON c.id_clan = h.id_clan
LEFT JOIN heros m ON m.id_heros = h.id_mentor
LEFT JOIN (SELECT id_heros, count(*) AS nb FROM vie_perdue WHERE id_saison = 4 GROUP BY id_heros) v
       ON v.id_heros = h.id_heros
LEFT JOIN (SELECT id_heros, sum(montant) AS bourse FROM transaction_pelotes GROUP BY id_heros) t
       ON t.id_heros = h.id_heros
LEFT JOIN (SELECT id_heros_proprietaire AS id_heros, count(*) AS nb FROM tresor GROUP BY id_heros_proprietaire) r
       ON r.id_heros = h.id_heros;

ALTER TABLE profil_heros ADD PRIMARY KEY (id_heros);
ANALYZE profil_heros;

-- L'écran de profil devient une lecture d'une seule ligne, par sa clé.
SELECT * FROM profil_heros WHERE id_heros = 8;

EXPLAIN ANALYZE
SELECT * FROM profil_heros WHERE id_heros = 8;
