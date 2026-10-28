---
title: Groupe expert clé-valeur
soustitre: Classement et Vies de Félicia dans Redis, quatre Tickets du Game Designer guidés
surtitre: Séance 3 · Groupes experts, 9h10 à 10h10
public: Support étudiant
---

## Votre heure

::: bloc
| Quand | Quoi |
|---------------|--------------------------------------------------------------|
| 9h10 [5 min]{.duree} | Codespace ouvert, bases démarrées (`make etat`), terminal Redis ouvert, lecture de la fiche |
| 9h15 [35 min]{.duree} | Tickets 1 à 4, chacun sur son Codespace, en s'entraidant ; le Ticket bonus si vous avez fini |
| 9h50 [15 min]{.duree} | fiche synthèse du groupe : cas d'usage, requête type, limites |
| 10h05 [5 min]{.duree} | chacun répète à voix haute le début de sa présentation de 8 minutes |
:::

Ouvrez le terminal Redis avec `make redis-cli`. Pour sortir : `exit`. Une commande par ligne ; les `___` sont à remplacer.

::: encadre
### Rappel du modèle

Tout se lit par la clé. `heros:<id>` est un hash (nom, Lignée, niveau, `id_clan`, `vies_restantes`, `renommee`, `pelotes`) ; `classement:saison:4` est un ensemble trié des identifiants de Héros, rangés par Renommée ; `clan:<id>:membres` est l'ensemble des Héros d'un Clan ; `tresor:<id>` et `heros:<id>:tresors` suivent le même principe. Les commandes utiles : `HGET`, `HGETALL`, `HINCRBY`, `ZREVRANGE`, `ZREVRANK`, `ZINCRBY`, `SET`, `EXPIRE`, `TTL`, `DEL`.
:::

## Ticket 1 · Le podium, avec les noms [7 min]{.duree}

> « L'écran d'accueil affiche le podium de la Saison : le nom des trois premiers Héros et leur Renommée. »
> — le studio

1. Les trois premiers et leur Renommée :

```
ZREVRANGE classement:saison:4 0 ___ WITHSCORES
```

2. Le classement ne contient que des identifiants : lisez le nom de chacun des trois.

```
HGET heros:___ nom
```

**Pour vérifier** : le premier a 3 381 de Renommée et s'appelle Bergamote.

**Pour la fiche** : combien d'allers-retours vers Redis pour afficher le podium ? Qu'aurait fait une seule requête SQL ?

## Ticket 2 · La dernière Vie d'Orchidée [8 min]{.duree}

> « Orchidée Oreille-Fendue (Héros 42) tombe du Port aux Nuages, sur l'Île de Velours. Retirez-lui une Vie et dites-nous si elle s'endort jusqu'à la fin de la Saison. »
> — le studio

```
HGET heros:42 vies_restantes
HINCRBY heros:42 vies_restantes ___
```

**Pour vérifier** : il lui restait une Vie ; `HINCRBY` renvoie la nouvelle valeur.

Remettez la base en état : `HINCRBY heros:42 vies_restantes 1`.

**Pour la fiche** : deux chutes arrivent à la même milliseconde. Que se passe-t-il si le serveur du jeu lit la valeur, retire 1, puis écrit le résultat ? Pourquoi `HINCRBY` évite-t-il ce problème ? Et qu'est-ce qui empêche `vies_restantes` de passer sous zéro ?

## Ticket 3 · Le classement interne du Cercle de l'Aube [10 min]{.duree}

> « Chaque Clan veut son propre classement. Commencez par le Cercle de l'Aube (Clan 1) : les trois meilleurs de ses membres. »
> — le studio

1. Croisez le classement de la Saison avec l'ensemble des membres du Clan, et rangez le résultat dans une nouvelle clé (le poids 0 ignore le score de l'ensemble des membres) :

```
ZINTERSTORE classement:clan:1 2 classement:saison:4 clan:1:membres WEIGHTS 1 0
```

2. Lisez les trois premiers de `classement:clan:1`, avec leur Renommée.
3. Ce classement vieillit dès qu'un membre gagne un combat : faites-le expirer dans 5 minutes avec `EXPIRE classement:clan:1 ___`, puis suivez le temps restant avec `TTL classement:clan:1`.

**Pour vérifier** : l'étape 1 renvoie 39, le nombre de membres classés ; Moustique le Gourmand (3426) est premier.

**Pour la fiche** : ce classement est une copie qu'on recalcule. Quand accepte-t-on qu'une donnée soit un peu périmée ?

## Ticket 4 · Un seul essai par minute contre le Gardien d'île [8 min]{.duree}

> « Les Héros attaquent le Gardien de l'Île de Brume en boucle. Une tentative par minute et par Héros, pas plus. »
> — le studio

`SET ... NX` n'écrit que si la clé n'existe pas encore ; `EX` la fait expirer seule.

```
SET heros:3426:essai-gardien 1 NX EX ___
```

Lancez la commande deux fois de suite. Notez les deux réponses. Supprimez la clé avec `DEL heros:3426:essai-gardien`.

**Pour vérifier** : la première réponse est `OK`, la seconde est vide.

**Pour la fiche** : comment feriez-vous la même chose en SQL ? Qui supprimerait les vieilles lignes ?

## Ticket bonus · Ce que Redis ne sait pas faire

> « Combien de Héros dépassent 1 000 de Renommée ? Et quels Héros sont endormis cette Saison ? »
> — le studio

La première question se règle avec `ZCOUNT classement:saison:4 1000 +inf`. La seconde n'a pas de commande : cherchez pourquoi, et proposez une clé que le serveur de Félicia tiendrait à jour à chaque Vie perdue pour y répondre.

## Votre fiche synthèse [15 min]{.duree}

Remplissez la fiche synthèse (document à part) : deux cas d'usage sur Félicia, une requête type que vous savez expliquer, deux forces, deux limites, et un besoin pour lequel vous **ne** choisiriez **pas** le clé-valeur. C'est votre support pour les 8 minutes de la redistribution.
