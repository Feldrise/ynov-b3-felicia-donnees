-- Chargement des CSV copiés dans le conteneur sous /tmp/felicia (voir outils/charger.sh).
COPY lignee FROM '/tmp/felicia/lignee.csv' WITH (FORMAT csv, HEADER true);
COPY ile FROM '/tmp/felicia/ile.csv' WITH (FORMAT csv, HEADER true);
COPY zone FROM '/tmp/felicia/zone.csv' WITH (FORMAT csv, HEADER true);
COPY saison FROM '/tmp/felicia/saison.csv' WITH (FORMAT csv, HEADER true);
COPY joueur FROM '/tmp/felicia/joueur.csv' WITH (FORMAT csv, HEADER true);
COPY clan FROM '/tmp/felicia/clan.csv' WITH (FORMAT csv, HEADER true);
COPY heros FROM '/tmp/felicia/heros.csv' WITH (FORMAT csv, HEADER true);
COPY alliance FROM '/tmp/felicia/alliance.csv' WITH (FORMAT csv, HEADER true);
COPY tresor FROM '/tmp/felicia/tresor.csv' WITH (FORMAT csv, HEADER true);
COPY obtention FROM '/tmp/felicia/obtention.csv' WITH (FORMAT csv, HEADER true);
COPY possession_tresor FROM '/tmp/felicia/possession_tresor.csv' WITH (FORMAT csv, HEADER true);
COPY vie_perdue FROM '/tmp/felicia/vie_perdue.csv' WITH (FORMAT csv, HEADER true);
COPY transaction_pelotes FROM '/tmp/felicia/transaction_pelotes.csv' WITH (FORMAT csv, HEADER true);
