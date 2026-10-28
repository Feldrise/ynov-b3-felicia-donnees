#!/usr/bin/env bash
# Charge le jeu de données Félicia dans les cinq bases (déjà démarrées).
# Les cinq chargements tournent en parallèle ; le journal de chacun est dans build/journaux/.
set -euo pipefail
cd "$(dirname "$0")/.."
source outils/commun.sh
D=build/donnees
J=build/journaux
mkdir -p "$J"
[ -f "$D/resume.json" ] || python3 donnees/generer.py "$D" >/dev/null

charger_postgres() {
  pg < bases/postgres/schema.sql
  dc exec -T postgres rm -rf /tmp/felicia
  dc cp "$D/csv" postgres:/tmp/felicia
  pg -1 < bases/postgres/charger.sql
  pg < bases/postgres/contraintes.sql
  dc exec -T postgres rm -rf /tmp/felicia
}

charger_mongo() {
  dc exec -T mongo rm -rf /tmp/felicia
  dc cp "$D/mongo" mongo:/tmp/felicia
  for c in heros clans tresors; do
    dc exec -T mongo mongoimport --quiet --db felicia --collection "$c" --drop --file "/tmp/felicia/$c.json"
  done
  mg --file /dev/stdin < bases/mongo/index.js
  dc exec -T mongo rm -rf /tmp/felicia
}

charger_redis() {
  local sortie
  sortie="$(dc exec -T redis redis-cli --pipe < "$D/redis/charger.resp")"
  echo "$sortie"
  grep -q 'errors: 0' <<< "$sortie"
}

charger_cassandra() {
  cq < bases/cassandra/schema.cql
  dc exec -T cassandra rm -rf /tmp/felicia
  dc cp "$D/cassandra" cassandra:/tmp/felicia
  cq < bases/cassandra/charger.cql
  dc exec -T cassandra rm -rf /tmp/felicia
}

charger_neo4j() {
  dc exec -T neo4j sh -c 'rm -rf /var/lib/neo4j/import/* && mkdir -p /var/lib/neo4j/import'
  for f in csv/ile csv/joueur csv/clan csv/heros csv/alliance csv/tresor neo4j/duels; do
    dc cp "$D/$f.csv" neo4j:/var/lib/neo4j/import/
  done
  ne < bases/neo4j/charger.cypher
}

pids=()
for base in postgres mongo redis cassandra neo4j; do
  ( debut=$SECONDS; "charger_$base" > "$J/charger-$base.log" 2>&1; echo "  $base chargé en $((SECONDS - debut)) s" ) &
  pids+=("$!:$base")
done
echec=0
for p in "${pids[@]}"; do
  if ! wait "${p%%:*}"; then
    echo "ÉCHEC du chargement de ${p#*:} : voir $J/charger-${p#*:}.log" >&2
    tail -n 20 "$J/charger-${p#*:}.log" >&2 || true
    echec=1
  fi
done
exit $echec
