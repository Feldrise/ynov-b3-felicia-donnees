# Fonctions communes aux scripts du dépôt. À sourcer depuis la racine du dépôt.
# Le nom du projet Docker Compose vient de COMPOSE_PROJECT_NAME (par défaut « felicia »).
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-felicia}"
dc() { docker compose -f compose.yaml "$@"; }
pg() { dc exec -T postgres psql -U felicia -d felicia -v ON_ERROR_STOP=1 -q "$@"; }
mg() { dc exec -T mongo mongosh --quiet felicia "$@"; }
rd() { dc exec -T redis redis-cli -e "$@"; }
cq() { dc exec -T cassandra cqlsh --request-timeout=120 "$@"; }
ne() { dc exec -T neo4j cypher-shell -u neo4j -p felicia-neo4j --format plain "$@"; }
titre() { printf '\n== %s\n' "$*"; }
