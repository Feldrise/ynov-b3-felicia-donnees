-- Atelier de dénormalisation (Séance 2) · Script 1 : l'écran de profil, tel qu'il est écrit aujourd'hui.
-- Huit lectures pour un seul écran : le Héros, son Joueur, sa Lignée, son Clan, son mentor,
-- ses Vies perdues de la Saison en cours, sa bourse de Pelotes d'or et ses Trésors.
-- Exécution : make sql F=ateliers/s2/1-profil-jointures.sql   (ou copier la requête dans make psql)

\timing on

SELECT h.id_heros, h.nom AS heros, j.pseudo AS joueur, l.nom AS lignee, h.niveau, h.renommee,
       c.nom AS clan, m.nom AS mentor,
       9 - (SELECT count(*) FROM vie_perdue v WHERE v.id_heros = h.id_heros AND v.id_saison = 4) AS vies_restantes,
       (SELECT coalesce(sum(t.montant), 0) FROM transaction_pelotes t WHERE t.id_heros = h.id_heros) AS bourse,
       (SELECT count(*) FROM tresor r WHERE r.id_heros_proprietaire = h.id_heros) AS nb_tresors
FROM heros h
JOIN joueur j ON j.id_joueur = h.id_joueur
JOIN lignee l ON l.id_lignee = h.id_lignee
LEFT JOIN clan c ON c.id_clan = h.id_clan
LEFT JOIN heros m ON m.id_heros = h.id_mentor
WHERE h.id_heros = 8;

-- Mesurer : relancer la même requête précédée de EXPLAIN ANALYZE, et relever « Execution Time ».
EXPLAIN ANALYZE
SELECT h.id_heros, h.nom AS heros, j.pseudo AS joueur, l.nom AS lignee, h.niveau, h.renommee,
       c.nom AS clan, m.nom AS mentor,
       9 - (SELECT count(*) FROM vie_perdue v WHERE v.id_heros = h.id_heros AND v.id_saison = 4) AS vies_restantes,
       (SELECT coalesce(sum(t.montant), 0) FROM transaction_pelotes t WHERE t.id_heros = h.id_heros) AS bourse,
       (SELECT count(*) FROM tresor r WHERE r.id_heros_proprietaire = h.id_heros) AS nb_tresors
FROM heros h
JOIN joueur j ON j.id_joueur = h.id_joueur
JOIN lignee l ON l.id_lignee = h.id_lignee
LEFT JOIN clan c ON c.id_clan = h.id_clan
LEFT JOIN heros m ON m.id_heros = h.id_mentor
WHERE h.id_heros = 8;
