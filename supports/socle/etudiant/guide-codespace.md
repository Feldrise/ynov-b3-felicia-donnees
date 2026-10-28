---
title: Ouvrir son Codespace
soustitre: Les cinq bases de Félicia dans votre navigateur, en 20 minutes, sans rien installer
surtitre: Séance 2 · Mise en place de l'environnement
public: Support étudiant
---

## Ce que vous allez obtenir

Un **Codespace** est un poste de développement qui tourne chez GitHub et s'ouvre dans votre navigateur. Celui du module contient les cinq bases de données de Félicia : PostgreSQL, MongoDB, Redis, Cassandra et Neo4j, avec le jeu de données du Fil rouge (7 013 Héros, leurs Clans, leurs Trésors et leurs Vies perdues).

Vous n'installez rien sur votre ordinateur. Il vous faut seulement un navigateur récent et un compte GitHub. Si vous n'en avez pas, vous le créez pendant la Séance, à l'étape 1.

::: bloc
### Le déroulé des 20 minutes

| Étape | Durée prévue | Au plus tard à la |
|-----------------------------------------------|-----------------|-----------------------|
| 1. Se connecter à GitHub, ou créer son compte | 1 ou 4 min | 6e minute |
| 2. Créer le Codespace du module | 2 min | 9e minute |
| 3. Démarrer les bases avec `make up` | 2 min | 12e minute |
| 4. Vérifier PostgreSQL et la base Félicia | 2 min | 15e minute |

L'ensemble est prévu en 7 minutes avec un compte GitHub existant, en 10 minutes avec un compte à créer ; les repères ajoutent une marge. **Un repère dépassé ?** Levez la main et passez à la procédure de secours, en fin de document : vous n'attendez pas la 20e minute.
:::

## 1. Se connecter à GitHub, ou créer son compte [1 ou 4 min]{.duree}

**Vous avez déjà un compte GitHub** : connectez-vous sur **github.com**, puis passez directement à l'étape 2.

**Vous n'avez pas de compte** :

1. Ouvrez **github.com/signup**.
2. Saisissez une adresse électronique que vous consultez pendant la Séance (celle de l'école convient), un mot de passe et un nom d'utilisateur.
3. Résolvez la vérification anti-robot, puis saisissez le code reçu par courriel.
4. Passez les questions de GitHub sur vos préférences.

::: encadre
Un compte gratuit suffit. Il donne droit chaque mois à un quota d'utilisation des Codespaces : avec la machine 4 cœurs du module, cela représente environ 30 heures (conditions de GitHub à la date de rédaction). Les Séances 2 et 3 en consomment moins de 10.
:::

## 2. Créer le Codespace du module [2 min]{.duree}

1. Ouvrez le lien du dépôt du module, donné sur Moodle.
2. Cliquez sur le bouton vert **Code**, puis sur l'onglet **Codespaces**.
3. Cliquez sur **Create codespace on main**.
4. Si GitHub demande de choisir un type de machine, prenez **4-core**.

Le formateur a préparé le dépôt pour que le Codespace s'ouvre en une minute environ, bases déjà téléchargées. Un éditeur ressemblant à VS Code s'ouvre dans le navigateur, avec un **terminal** en bas de l'écran. La préparation est terminée quand le terminal affiche la liste des commandes `make` disponibles.

::: {.encadre .attention}
Le Codespace n'est toujours pas ouvert à la 9e minute ? Laissez l'onglet se préparer et appliquez la solution de secours 1 : vous reviendrez à votre propre Codespace à la pause.
:::

## 3. Démarrer les bases [2 min]{.duree}

Dans le terminal du Codespace, tapez :

```bash
make up
```

La commande démarre les cinq bases, attend qu'elles soient prêtes, puis charge le jeu de données de Félicia dans chacune. Comptez une à deux minutes. Elle se termine par :

```text
== Chargement du jeu de données Félicia
  redis chargé en 1 s
  ...
  environnement prêt en 75 s
```

Les durées varient d'un Codespace à l'autre. Si la commande affiche **ÉCHEC**, ou si elle tourne encore à la 12e minute, voyez la procédure de secours.

## 4. Vérifier PostgreSQL et la base Félicia [2 min]{.duree}

D'abord une vue d'ensemble :

```bash
make etat
```

Les cinq bases doivent apparaître avec l'état **healthy**, suivies d'un effectif par base. Ouvrez ensuite un terminal SQL sur PostgreSQL :

```bash
make psql
```

Puis tapez la requête suivante :

```sql
SELECT count(*) FROM heros;
```

La réponse attendue est **7013**. Pour quitter le terminal SQL, tapez `\q`.

::: bloc
### C'est prêt quand...

- `make etat` montre cinq bases **healthy** ;
- `SELECT count(*) FROM heros;` renvoie **7013**.

Vous pouvez alors attaquer l'atelier de dénormalisation.
:::

## Les autres commandes utiles

| Commande | Ce qu'elle fait |
|-----------------------------------|-----------------------------------------------------------------|
| `make aide` | Liste toutes les commandes. |
| `make psql` | Terminal SQL sur PostgreSQL. |
| `make sql F=<script>` | Exécute un script SQL dans PostgreSQL (atelier de la Séance 2). |
| `make mongosh`, `make redis-cli`, `make cqlsh`, `make cypher-shell` | Terminal de MongoDB, Redis, Cassandra ou Neo4j (Séance 3). |
| `make charger` | Recharge le jeu de données d'origine, si vous avez tout cassé. |
| `make down` | Arrête et détruit les bases ; `make up` les recrée. |

## En fin de Séance : arrêter le Codespace

Un Codespace ouvert consomme votre quota, même si vous ne faites rien. En partant :

1. ouvrez **github.com/codespaces** ;
2. sur la ligne du Codespace du module, ouvrez le menu (les trois points) et choisissez **Stop codespace**.

Ne le supprimez pas : en Séance 3, vous le rouvrirez depuis la même page, puis vous relancerez `make up`.

## Procédure de secours

::: {.encadre .attention}
### Règle d'or : personne ne reste bloqué

Au premier repère dépassé, ou au bout de 3 minutes de blocage sur une même étape, prévenez le formateur et appliquez la première solution qui marche. L'atelier ne doit pas attendre votre environnement.
:::

### Les problèmes fréquents

| Symptôme | Solution |
|--------------------------------------------------|--------------------------------------------------|
| Le compte GitHub ne reçoit pas son code par courriel | Vérifiez les courriels indésirables, ou créez le compte avec une autre adresse. |
| `Cannot connect to the Docker daemon` | Le Codespace finit de démarrer : attendez une minute et relancez la commande. |
| `make: command not found` ou `No rule to make target` | Vous n'êtes pas dans le terminal du Codespace, ou pas à la racine du dépôt : tapez `cd /workspaces/*` puis recommencez. |
| `make up` tourne encore à la 12e minute | Tapez `make down` puis `make up` une seule fois ; si cela recommence, passez à la solution de secours 1. |
| Une base apparaît en **Exited** dans `make etat` | Tapez `docker compose logs mongo` (en remplaçant `mongo` par la base concernée) et montrez le message au formateur. |
| GitHub refuse la machine 4 cœurs ou annonce un quota épuisé | Passez à la solution de secours 1. |
| Le Codespace affiche encore sa préparation à la 9e minute | Laissez l'onglet ouvert et passez à la solution de secours 1. |

### Si le Codespace ne fonctionne toujours pas

1. **Travailler à deux sur un Codespace** : rejoignez un voisin dont le Codespace fonctionne. Vous faites les mesures sur son poste et vous rédigez chacun vos propres réponses. Si votre propre Codespace était seulement lent, il sera prêt à la pause : vous le retrouverez sur **github.com/codespaces**.
2. **Docker déjà installé sur votre ordinateur** (ne l'installez pas pendant la Séance) : récupérez le dépôt du module, puis tapez `make up` à sa racine. Sous Windows, passez par WSL. Les commandes sont les mêmes que dans le Codespace.
3. **Suivre sur l'écran du formateur** : le formateur projette son propre environnement ; vous notez les mesures affichées et vous menez l'analyse comme les autres.
