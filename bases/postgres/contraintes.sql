-- Clés étrangères et index, posés après le chargement.
ALTER TABLE zone ADD FOREIGN KEY (id_ile) REFERENCES ile (id_ile);
ALTER TABLE clan ADD FOREIGN KEY (id_ile_repaire) REFERENCES ile (id_ile);
ALTER TABLE clan ADD FOREIGN KEY (id_heros_chef) REFERENCES heros (id_heros);
ALTER TABLE heros ADD FOREIGN KEY (id_joueur) REFERENCES joueur (id_joueur);
ALTER TABLE heros ADD FOREIGN KEY (id_lignee) REFERENCES lignee (id_lignee);
ALTER TABLE heros ADD FOREIGN KEY (id_clan) REFERENCES clan (id_clan);
ALTER TABLE heros ADD FOREIGN KEY (id_mentor) REFERENCES heros (id_heros);
ALTER TABLE alliance ADD FOREIGN KEY (id_clan_1) REFERENCES clan (id_clan);
ALTER TABLE alliance ADD FOREIGN KEY (id_clan_2) REFERENCES clan (id_clan);
ALTER TABLE tresor ADD FOREIGN KEY (id_heros_proprietaire) REFERENCES heros (id_heros);
ALTER TABLE obtention ADD FOREIGN KEY (id_tresor) REFERENCES tresor (id_tresor);
ALTER TABLE obtention ADD FOREIGN KEY (id_heros) REFERENCES heros (id_heros);
ALTER TABLE obtention ADD FOREIGN KEY (id_ile) REFERENCES ile (id_ile);
ALTER TABLE possession_tresor ADD FOREIGN KEY (id_tresor) REFERENCES tresor (id_tresor);
ALTER TABLE possession_tresor ADD FOREIGN KEY (id_heros) REFERENCES heros (id_heros);
ALTER TABLE vie_perdue ADD FOREIGN KEY (id_heros) REFERENCES heros (id_heros);
ALTER TABLE vie_perdue ADD FOREIGN KEY (id_saison) REFERENCES saison (id_saison);
ALTER TABLE vie_perdue ADD FOREIGN KEY (id_zone) REFERENCES zone (id_zone);
ALTER TABLE vie_perdue ADD FOREIGN KEY (id_heros_vainqueur) REFERENCES heros (id_heros);
ALTER TABLE transaction_pelotes ADD FOREIGN KEY (id_heros) REFERENCES heros (id_heros);

-- Index des clés étrangères les plus consultées.
-- Volontairement absent : transaction_pelotes (id_heros). Calculer la bourse d'un Héros parcourt
-- toute la table ; c'est le point de départ de l'atelier de dénormalisation de S2.
CREATE INDEX ON heros (id_joueur);
CREATE INDEX ON heros (id_clan);
CREATE INDEX ON tresor (id_heros_proprietaire);
CREATE INDEX ON obtention (id_heros);

ANALYZE;
