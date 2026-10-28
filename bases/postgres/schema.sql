-- MPD du jeu de données Félicia (PostgreSQL).
-- Les clés étrangères et les index sont posés après le chargement (contraintes.sql).
SET client_min_messages = warning;
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

CREATE TABLE lignee (
  id_lignee    SMALLINT PRIMARY KEY,
  nom          VARCHAR(30) NOT NULL UNIQUE,
  description  TEXT NOT NULL
);

CREATE TABLE ile (
  id_ile         SMALLINT PRIMARY KEY,
  nom            VARCHAR(40) NOT NULL UNIQUE,
  niveau_requis  SMALLINT NOT NULL CHECK (niveau_requis BETWEEN 1 AND 60)
);

CREATE TABLE zone (
  id_zone  SMALLINT PRIMARY KEY,
  id_ile   SMALLINT NOT NULL,
  nom      VARCHAR(60) NOT NULL,
  UNIQUE (id_ile, nom)
);

CREATE TABLE saison (
  id_saison   SMALLINT PRIMARY KEY,
  nom         VARCHAR(60) NOT NULL UNIQUE,
  date_debut  DATE NOT NULL,
  date_fin    DATE NOT NULL,
  CHECK (date_fin > date_debut)
);

CREATE TABLE joueur (
  id_joueur         INTEGER PRIMARY KEY,
  pseudo            VARCHAR(40) NOT NULL UNIQUE,
  courriel          VARCHAR(120) NOT NULL UNIQUE,
  pays              CHAR(2) NOT NULL,
  date_inscription  DATE NOT NULL
);

CREATE TABLE clan (
  id_clan         INTEGER PRIMARY KEY,
  nom             VARCHAR(60) NOT NULL UNIQUE,
  devise          VARCHAR(160),
  date_fondation  DATE NOT NULL,
  id_ile_repaire  SMALLINT NOT NULL,
  id_heros_chef   INTEGER NOT NULL
);

-- Héritage des Lignées traduit en table unique : les attributs propres à chaque Lignée
-- sont des colonnes facultatives, contrôlées par id_lignee.
CREATE TABLE heros (
  id_heros          INTEGER PRIMARY KEY,
  nom               VARCHAR(60) NOT NULL UNIQUE,
  id_joueur         INTEGER NOT NULL,
  id_lignee         SMALLINT NOT NULL,
  niveau            SMALLINT NOT NULL CHECK (niveau BETWEEN 1 AND 60),
  renommee          INTEGER NOT NULL DEFAULT 0 CHECK (renommee >= 0),
  date_creation     DATE NOT NULL,
  id_clan           INTEGER,
  date_adhesion     DATE,
  id_mentor         INTEGER,
  date_debut_mentorat DATE,
  element           VARCHAR(20),
  furtivite         SMALLINT CHECK (furtivite BETWEEN 1 AND 100),
  rempart           SMALLINT CHECK (rempart BETWEEN 1 AND 100),
  recettes_connues  SMALLINT CHECK (recettes_connues >= 0),
  CHECK (id_mentor <> id_heros),
  CHECK ((id_mentor IS NULL) = (date_debut_mentorat IS NULL)),
  CHECK ((id_clan IS NULL) = (date_adhesion IS NULL)),
  CHECK ((id_lignee = 1) = (element IS NOT NULL)),
  CHECK ((id_lignee = 2) = (furtivite IS NOT NULL)),
  CHECK ((id_lignee = 3) = (rempart IS NOT NULL)),
  CHECK ((id_lignee = 4) = (recettes_connues IS NOT NULL))
);

CREATE TABLE alliance (
  id_clan_1      INTEGER NOT NULL,
  id_clan_2      INTEGER NOT NULL,
  date_alliance  DATE NOT NULL,
  PRIMARY KEY (id_clan_1, id_clan_2),
  CHECK (id_clan_1 < id_clan_2)
);

CREATE TABLE tresor (
  id_tresor              INTEGER PRIMARY KEY,
  nom                    VARCHAR(80) NOT NULL,
  nature                 VARCHAR(20) NOT NULL CHECK (nature IN ('arme', 'armure', 'grimoire', 'potion', 'relique', 'parure')),
  rarete                 VARCHAR(12) NOT NULL CHECK (rarete IN ('commun', 'rare', 'épique', 'légendaire')),
  attributs              JSONB NOT NULL,
  id_heros_proprietaire  INTEGER NOT NULL
);

-- Association ternaire : un Héros obtient un Trésor sur une île.
CREATE TABLE obtention (
  id_tresor       INTEGER PRIMARY KEY,
  id_heros        INTEGER NOT NULL,
  id_ile          SMALLINT NOT NULL,
  date_obtention  TIMESTAMPTZ NOT NULL
);

-- Historique des propriétaires des Trésors légendaires.
CREATE TABLE possession_tresor (
  id_tresor   INTEGER NOT NULL,
  id_heros    INTEGER NOT NULL,
  date_debut  TIMESTAMPTZ NOT NULL,
  date_fin    TIMESTAMPTZ,
  PRIMARY KEY (id_tresor, date_debut),
  CHECK (date_fin IS NULL OR date_fin >= date_debut)
);

-- Règle des 9 Vies : au plus 9 Vies perdues par Héros et par saison, numérotées de 1 à 9.
CREATE TABLE vie_perdue (
  id_vie              INTEGER PRIMARY KEY,
  id_heros            INTEGER NOT NULL,
  id_saison           SMALLINT NOT NULL,
  numero              SMALLINT NOT NULL CHECK (numero BETWEEN 1 AND 9),
  date_heure          TIMESTAMPTZ NOT NULL,
  id_zone             SMALLINT NOT NULL,
  cause               VARCHAR(30) NOT NULL
                      CHECK (cause IN ('chute dans le vide', 'sortilège', 'gardien d''île', 'duel', 'piège', 'brume toxique')),
  id_heros_vainqueur  INTEGER,
  UNIQUE (id_heros, id_saison, numero),
  CHECK ((cause = 'duel') = (id_heros_vainqueur IS NOT NULL)),
  CHECK (id_heros_vainqueur <> id_heros)
);

-- Pelotes d'or : chaque mouvement de la bourse d'un Héros (gain positif, dépense négative).
CREATE TABLE transaction_pelotes (
  id_transaction  INTEGER PRIMARY KEY,
  id_heros        INTEGER NOT NULL,
  date_heure      TIMESTAMPTZ NOT NULL,
  montant         INTEGER NOT NULL CHECK (montant <> 0),
  motif           VARCHAR(30) NOT NULL
                  CHECK (motif IN ('quête', 'revente de Trésor', 'récompense de saison', 'achat en boutique',
                                   'cotisation de Clan', 'achat avec argent réel'))
);
