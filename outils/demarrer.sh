#!/usr/bin/env bash
# Démarre les cinq bases, attend qu'elles soient prêtes, puis charge le jeu de données.
set -euo pipefail
cd "$(dirname "$0")/.."
source outils/commun.sh
debut=$SECONDS
titre "Démarrage des cinq bases (projet $COMPOSE_PROJECT_NAME)"
dc up -d --wait --wait-timeout 300
echo "  bases prêtes en $((SECONDS - debut)) s"
titre "Chargement du jeu de données Félicia"
bash outils/charger.sh
echo "  environnement prêt en $((SECONDS - debut)) s"
