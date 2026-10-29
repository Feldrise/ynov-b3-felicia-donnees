---
title: Ouvrir son Codespace
soustitre: Les cinq bases de Félicia dans ton navigateur, en 20 minutes, sans rien installer
surtitre: Séance 2 · Mise en place de l'environnement
public: Support étudiant
---

## Le Codespace du module

Un **Codespace** est un poste de développement hébergé par GitHub, dans ton navigateur. Celui du module contient les cinq bases de Félicia (PostgreSQL, MongoDB, Redis, Cassandra, Neo4j) et le jeu de données du Fil rouge : 7 013 Héros, leurs Clans, leurs Trésors et leurs Vies perdues. Il te faut un navigateur récent et un compte GitHub, à créer sur place si besoin.

::: bloc
### Quatre étapes, quatre repères

| Étape | Durée | Au plus tard à la |
|-----------------------------------------------|-----------------|-----------------------|
| 1. Se connecter à GitHub, ou créer son compte | 1 ou 4 min | 6e minute |
| 2. Créer le Codespace du module | 2 min | 9e minute |
| 3. Démarrer les bases avec `make up` | 2 min | 12e minute |
| 4. Vérifier PostgreSQL et la base Félicia | 2 min | 15e minute |

Compte 7 minutes avec un compte existant, 10 avec un compte à créer ; les repères ajoutent une marge. Un repère dépassé ? Lève la main et passe à la procédure de secours, en fin de document.
:::

## 1. Se connecter à GitHub, ou créer son compte [1 ou 4 min]{.duree}

Avec un compte, connecte-toi sur **github.com** et passe à l'étape 2. Sinon :

1. Ouvre **github.com/signup**.
2. Saisis une adresse lue pendant la Séance (celle de l'école convient), un mot de passe et un nom d'utilisateur.
3. Résous la vérification anti-robot, saisis le code reçu par courriel, puis passe les questions sur tes préférences.

::: encadre
Un compte gratuit suffit : environ 30 heures par mois sur la machine 4 cœurs, les Séances 2 et 3 en consomment moins de 10. Un Codespace arrêté occupe encore 6 Go de ton quota : supprime-le sur **github.com/codespaces** après la Séance 4.
:::

## 2. Créer le Codespace du module [2 min]{.duree}

1. Ouvre le lien du dépôt du module, donné sur Moodle.
2. Clique sur le bouton vert **Code**, puis sur l'onglet **Codespaces**.
3. Clique sur **Create codespace on main**.
4. Si GitHub demande un type de machine, prends **4-core**.

En une minute environ, un éditeur proche de VS Code s'ouvre, avec un **terminal** en bas. C'est prêt quand le terminal affiche la liste des commandes `make`.

::: {.encadre .attention}
Toujours pas ouvert à la 9e minute ? Laisse l'onglet se préparer et applique la solution de secours 1 : tu retrouveras ton Codespace à la pause.
:::

## 3. Démarrer les bases [2 min]{.duree}

Dans le terminal du Codespace :

```bash
make up
```

Elle démarre les cinq bases et y charge le jeu de données, en une à deux minutes. Elle se termine par :

```text
== Chargement du jeu de données Félicia
  redis chargé en 1 s
  ...
  environnement prêt en 75 s
```

Elle affiche **ÉCHEC**, ou tourne encore à la 12e minute ? Procédure de secours.

## 4. Vérifier PostgreSQL et la base Félicia [2 min]{.duree}

```bash
make etat
```

Les cinq bases doivent être **healthy**. Puis, dans PostgreSQL :

```bash
make psql
```

```sql
SELECT count(*) FROM heros;
```

::: bloc
### C'est prêt quand...

`make etat` montre cinq bases **healthy** et la requête renvoie **7013** (`\q` pour quitter). Place à l'atelier de dénormalisation.
:::

## Les autres commandes utiles

| Commande | Ce qu'elle fait |
|-----------------------------------|-----------------------------------------------------------------|
| `make aide` | Liste toutes les commandes. |
| `make psql` | Terminal SQL sur PostgreSQL. |
| `make sql F=<script>` | Exécute un script SQL dans PostgreSQL (atelier de la Séance 2). |
| `make mongosh`, `make redis-cli`, `make cqlsh`, `make cypher-shell` | Terminal de MongoDB, Redis, Cassandra ou Neo4j (Séance 3). |
| `make charger` | Recharge le jeu de données d'origine, si tu as tout cassé. |
| `make down` | Arrête et détruit les bases ; `make up` les recrée. |

## En fin de Séance : arrêter le Codespace

Un Codespace ouvert consomme ton quota, même inactif. En partant, sur **github.com/codespaces**, ouvre le menu (les trois points) du Codespace du module et choisis **Stop codespace**. Ne le supprime pas : en Séance 3, tu le rouvriras d'ici et tu relanceras `make up`.

## Procédure de secours

::: {.encadre .attention}
### Règle d'or : si ça bloque, on ne reste pas seul

Au premier repère dépassé, ou après 3 minutes de blocage sur une étape, fais-moi signe et applique la première solution qui marche.
:::

### Les problèmes fréquents

| Symptôme | Solution |
|--------------------------------------------------|--------------------------------------------------|
| Le code de GitHub n'arrive pas | Regarde dans les indésirables, ou change d'adresse. |
| `Cannot connect to the Docker daemon` | Le Codespace finit de démarrer : attends une minute et relance la commande. |
| `make: command not found` ou `No rule to make target` | Tu n'es pas dans le terminal du Codespace ou pas à la racine : tape `cd /workspaces/*` et recommence. |
| `make up` tourne encore à la 12e minute | `make down` puis `make up`, une seule fois ; si ça recommence, solution de secours 1. |
| Une base est **Exited** dans `make etat` | Tape `docker compose logs mongo` (ou le nom de la base concernée) et montre-moi le message. |
| GitHub refuse la machine 4 cœurs ou annonce un quota épuisé | Solution de secours 1. |
| Le Codespace affiche encore sa préparation à la 9e minute | Laisse l'onglet ouvert et passe à la solution de secours 1. |

### Si le Codespace ne fonctionne toujours pas

1. **À deux sur un Codespace** : rejoins un voisin dont le Codespace fonctionne ; vous mesurez sur son poste, chacun rédige ses réponses. Si le tien était seulement lent, il t'attend à la pause sur **github.com/codespaces**.
2. **Docker déjà installé sur ton ordinateur** (ne l'installe pas en Séance) : récupère le dépôt et tape `make up` à sa racine, via WSL sous Windows.
3. **Suivre sur mon écran** : tu notes les mesures que je projette et tu mènes l'analyse comme les autres.
