# Dépôt du cours « Conception architecture des données » : Fil rouge Neuf Vies : Les Îles de Félicia.
# `make` seul affiche l'aide.
SHELL := /bin/bash
export COMPOSE_PROJECT_NAME ?= felicia
PYTHON ?= python3
DC := docker compose -f compose.yaml

.DEFAULT_GOAL := aide
.PHONY: aide up charger etat down psql sql mongosh redis-cli cqlsh cypher-shell donnees outils schemas pdf lint export verify

aide: ## affiche cette aide
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-13s %s\n", $$1, $$2}'

up: ## démarre les cinq bases et charge le jeu de données Félicia
	@bash outils/demarrer.sh

charger: donnees ## recharge le jeu de données dans les bases déjà démarrées
	@bash outils/charger.sh

etat: ## affiche l'état des bases et quelques effectifs
	@bash outils/etat.sh

down: ## arrête et détruit les bases (les données seront rechargées au prochain make up)
	$(DC) down -v --remove-orphans --timeout 5

psql: ## ouvre un terminal SQL sur PostgreSQL
	$(DC) exec postgres psql -U felicia -d felicia

sql: ## exécute un script SQL dans PostgreSQL : make sql F=ateliers/s2/1-profil-jointures.sql
	@test -n "$(F)" || { echo "Indiquez le script : make sql F=ateliers/s2/1-profil-jointures.sql"; exit 2; }
	$(DC) exec -T postgres psql -U felicia -d felicia < $(F)

mongosh: ## ouvre un terminal MongoDB
	$(DC) exec mongo mongosh felicia

redis-cli: ## ouvre un terminal Redis
	$(DC) exec redis redis-cli

cqlsh: ## ouvre un terminal Cassandra (keyspace felicia)
	$(DC) exec cassandra cqlsh -k felicia

cypher-shell: ## ouvre un terminal Neo4j
	$(DC) exec neo4j cypher-shell -u neo4j -p felicia-neo4j

donnees: build/donnees/resume.json ## génère le jeu de données dans build/donnees

build/donnees/resume.json: donnees/generer.py
	$(PYTHON) donnees/generer.py build/donnees

outils: .venv/bin/mocodo ## installe Mocodo dans .venv (formateur)

.venv/bin/mocodo: requirements.txt
	$(PYTHON) -m venv .venv
	.venv/bin/pip install -q -r requirements.txt
	@touch $@

schemas: outils ## génère diagrammes, MLD et SQL des schémas Mocodo, sans base de données (formateur)
	$(PYTHON) outils/controle_mocodo.py --sans-sql

pdf: schemas ## régénère tous les PDF dans build/pdf et contrôle leurs polices (formateur)
	$(PYTHON) pdf/construire.py --tout

lint: ## lint du vocabulaire du glossaire et de la charte sur les supports (formateur)
	$(PYTHON) outils/lint_vocabulaire.py

export: ## construit l'export étudiant dans build/export-etudiant, sans corrigé (formateur)
	$(PYTHON) outils/exporter.py

verify: ## contrôle de fin complet, de bases neuves jusqu'à leur destruction
	$(PYTHON) outils/verifier.py
