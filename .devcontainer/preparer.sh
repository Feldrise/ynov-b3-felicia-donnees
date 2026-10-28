#!/usr/bin/env bash
# Exécuté une fois, à la création du Codespace : attend Docker puis tire les images des cinq bases,
# pour que le premier `make up` démarre sans téléchargement.
set -uo pipefail
for _ in $(seq 1 60); do
  docker info >/dev/null 2>&1 && break
  sleep 2
done
docker compose -f compose.yaml pull --quiet || echo "Tirage des images incomplet : make up le terminera."
