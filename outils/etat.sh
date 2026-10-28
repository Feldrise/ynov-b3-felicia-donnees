#!/usr/bin/env bash
# Affiche l'état des cinq bases et un effectif par base : de quoi vérifier que tout est chargé.
set -uo pipefail
cd "$(dirname "$0")/.."
source outils/commun.sh
dc ps --format 'table {{.Service}}\t{{.Status}}'
titre "Effectifs"
printf '  %-11s %s\n' "PostgreSQL" "$(pg -At -c 'SELECT count(*) FROM heros' 2>/dev/null || echo 'indisponible') Héros"
printf '  %-11s %s\n' "MongoDB" "$(mg --eval 'db.tresors.countDocuments()' 2>/dev/null || echo 'indisponible') Trésors"
printf '  %-11s %s\n' "Redis" "$(rd ZCARD classement:saison:4 2>/dev/null || echo 'indisponible') Héros au classement"
printf '  %-11s %s\n' "Cassandra" "$(cq -e 'SELECT count(*) FROM felicia.vies_par_heros' 2>/dev/null | sed -n '4p' | tr -d ' ' || echo 'indisponible') Vies perdues"
printf '  %-11s %s\n' "Neo4j" "$(ne 'MATCH (c:Clan) RETURN count(c)' 2>/dev/null | tail -n 1 || echo 'indisponible') Clans"
