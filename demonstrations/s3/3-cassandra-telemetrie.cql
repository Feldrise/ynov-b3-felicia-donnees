-- Séance 3, démonstration 3 : la télémétrie des Vies perdues en colonne (Cassandra), 9 minutes.
-- Ouvrir le terminal : make cqlsh. Copier les requêtes une par une.
-- Chaque requête est rejouée par `make verify` (verification/requetes/04-s3-demonstrations.toml).

-- 1. Une table par requête. La clé de partition (id_ile, id_saison) dit sur quel nœud vivent les données ;
--    les colonnes de regroupement (zone, date_heure...) disent dans quel ordre elles y sont rangées.
DESCRIBE TABLE vies_par_ile;

-- 2. La question pour laquelle la table a été dessinée : où les Héros perdent-ils leurs Vies sur l'Île de Brume cette Saison ?
SELECT zone, count(*) FROM vies_par_ile WHERE id_ile = 1 AND id_saison = 4 GROUP BY zone;

-- 3. Les cinq dernières Vies perdues dans la Falaise des Soupirs : lecture dans l'ordre de rangement, à l'envers.
SELECT zone, date_heure, id_heros, cause FROM vies_par_ile WHERE id_ile = 1 AND id_saison = 4 AND zone = 'Falaise des Soupirs' ORDER BY zone DESC, date_heure DESC LIMIT 5;

-- 4. La même donnée, rangée autrement, pour une autre question : le journal de la Saison de Moustique le Gourmand.
SELECT numero, date_heure, ile, zone, cause FROM vies_par_heros WHERE id_heros = 3426 AND id_saison = 4;

-- 5. Moustique tombe de la Falaise : on écrit l'événement dans les deux tables à la fois (dénormalisation assumée).
BEGIN BATCH INSERT INTO vies_par_heros (id_heros, id_saison, numero, date_heure, ile, zone, cause) VALUES (3426, 4, 2, '2026-11-13 08:40:00+0000', 'Brume', 'Falaise des Soupirs', 'chute dans le vide'); INSERT INTO vies_par_ile (id_ile, id_saison, zone, date_heure, id_heros, numero, cause, id_clan) VALUES (1, 4, 'Falaise des Soupirs', '2026-11-13 08:40:00+0000', 3426, 2, 'chute dans le vide', 1); APPLY BATCH;
SELECT numero, date_heure, ile, zone, cause FROM vies_par_heros WHERE id_heros = 3426 AND id_saison = 4;

-- 6. Les limites : une question que la table n'a pas prévue est refusée.
--    Regrouper par cause : la cause ne fait pas partie de la clé primaire.
SELECT cause, count(*) FROM vies_par_ile WHERE id_ile = 1 AND id_saison = 4 GROUP BY cause;
--    Chercher les duels sur tout l'archipel : il faudrait lire toutes les partitions.
SELECT * FROM vies_par_ile WHERE cause = 'duel';

-- Remise en état (à la fin de la démonstration, pour la rejouer à l'identique).
BEGIN BATCH DELETE FROM vies_par_heros WHERE id_heros = 3426 AND id_saison = 4 AND numero = 2; DELETE FROM vies_par_ile WHERE id_ile = 1 AND id_saison = 4 AND zone = 'Falaise des Soupirs' AND date_heure = '2026-11-13 08:40:00+0000' AND id_heros = 3426 AND numero = 2; APPLY BATCH;
