COPY felicia.heros (id_heros, nom, id_joueur, lignee, niveau, id_clan) FROM '/tmp/felicia/heros.csv' WITH HEADER = TRUE;
COPY felicia.clans (id_clan, nom, id_ile_repaire, nb_membres) FROM '/tmp/felicia/clans.csv' WITH HEADER = TRUE;
COPY felicia.tresors_par_heros (id_heros, id_tresor, nom, nature, rarete) FROM '/tmp/felicia/tresors_par_heros.csv' WITH HEADER = TRUE;
COPY felicia.vies_par_heros (id_heros, id_saison, numero, date_heure, ile, zone, cause, id_heros_vainqueur) FROM '/tmp/felicia/vies_par_heros.csv' WITH HEADER = TRUE;
COPY felicia.vies_par_ile (id_ile, id_saison, zone, date_heure, id_heros, numero, cause, id_clan) FROM '/tmp/felicia/vies_par_ile.csv' WITH HEADER = TRUE;
