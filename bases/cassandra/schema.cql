-- Keyspace Félicia : une table par requête, données dénormalisées.
DROP KEYSPACE IF EXISTS felicia;
CREATE KEYSPACE felicia WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE felicia;

CREATE TABLE heros (
  id_heros int PRIMARY KEY,
  nom text,
  id_joueur int,
  lignee text,
  niveau int,
  id_clan int
);

CREATE TABLE clans (
  id_clan int PRIMARY KEY,
  nom text,
  id_ile_repaire int,
  nb_membres int
);

-- « Quels Trésors possède ce Héros ? »
CREATE TABLE tresors_par_heros (
  id_heros int,
  id_tresor int,
  nom text,
  nature text,
  rarete text,
  PRIMARY KEY ((id_heros), id_tresor)
);

-- Télémétrie : « comment ce Héros a-t-il perdu ses Vies pendant cette saison ? »
CREATE TABLE vies_par_heros (
  id_heros int,
  id_saison int,
  numero int,
  date_heure timestamp,
  ile text,
  zone text,
  cause text,
  id_heros_vainqueur int,
  PRIMARY KEY ((id_heros, id_saison), numero)
);

-- Télémétrie : « où les Héros perdent-ils leurs Vies sur cette île pendant cette saison ? »
CREATE TABLE vies_par_ile (
  id_ile int,
  id_saison int,
  zone text,
  date_heure timestamp,
  id_heros int,
  numero int,
  cause text,
  id_clan int,
  PRIMARY KEY ((id_ile, id_saison), zone, date_heure, id_heros, numero)
);
