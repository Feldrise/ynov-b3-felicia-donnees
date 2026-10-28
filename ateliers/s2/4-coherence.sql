-- Atelier de dénormalisation (Séance 2) · Script 4 : ce que l'on paie en cohérence et en écriture.
-- Sorbet Pelage-d'Or (Héros 8) termine une quête et gagne 500 Pelotes d'or. Que montrent les trois écrans ?
-- Tout se passe dans une transaction annulée à la fin : la base reste intacte pour vos voisins de Codespace.
-- À lancer après les scripts 2 et 3. Exécution : make sql F=ateliers/s2/4-coherence.sql

\timing on

BEGIN;

INSERT INTO transaction_pelotes (id_transaction, id_heros, date_heure, montant, motif)
VALUES ((SELECT max(id_transaction) + 1 FROM transaction_pelotes), 8, now(), 500, 'quête');

-- 1. La requête multi-jointures recalcule tout : elle voit la quête.
SELECT 'jointures' AS source, coalesce(sum(montant), 0) AS bourse FROM transaction_pelotes WHERE id_heros = 8
UNION ALL
-- 2. La table dénormalisée n'a pas bougé : personne ne l'a mise à jour.
SELECT 'table dénormalisée', bourse FROM profil_heros WHERE id_heros = 8
UNION ALL
-- 3. La vue matérialisée non plus : elle attend son REFRESH.
SELECT 'vue matérialisée', bourse FROM profil_heros_vue WHERE id_heros = 8;

-- Remettre la table à jour : c'est à l'application (ou à un déclencheur) de le faire, à chaque mouvement.
UPDATE profil_heros SET bourse = bourse + 500 WHERE id_heros = 8;

-- Remettre la vue à jour : PostgreSQL recalcule les 7 013 profils, pas seulement celui de Sorbet.
REFRESH MATERIALIZED VIEW CONCURRENTLY profil_heros_vue;

SELECT 'jointures' AS source, coalesce(sum(montant), 0) AS bourse FROM transaction_pelotes WHERE id_heros = 8
UNION ALL
SELECT 'table dénormalisée', bourse FROM profil_heros WHERE id_heros = 8
UNION ALL
SELECT 'vue matérialisée', bourse FROM profil_heros_vue WHERE id_heros = 8;

ROLLBACK;
