---
title: Groupe expert document
soustitre: Les Trésors de Félicia dans MongoDB, quatre Tickets du Game Designer guidés
surtitre: Séance 3 · Groupes experts, 9h10 à 10h10
public: Support étudiant
---

## Votre heure

::: bloc
| Quand | Quoi |
|---------------|--------------------------------------------------------------|
| 9h10 [5 min]{.duree} | Codespace ouvert, bases démarrées (`make etat`), terminal MongoDB ouvert, lecture de la fiche |
| 9h15 [35 min]{.duree} | Tickets 1 à 4, chacun sur son Codespace, en s'entraidant ; le Ticket bonus si vous avez fini |
| 9h50 [15 min]{.duree} | fiche synthèse du groupe : cas d'usage, requête type, limites |
| 10h05 [5 min]{.duree} | chacun répète à voix haute le début de sa présentation de 8 minutes |
:::

Ouvrez le terminal MongoDB avec `make mongosh`. Pour sortir : `exit`. Une requête s'écrit sur une ligne ; les `___` sont à remplacer.

::: encadre
### Rappel du modèle

La collection `tresors` range un document par Trésor : `_id` (le même identifiant que dans PostgreSQL), `nom`, `nature`, `rarete`, `attributs` (différents selon la nature), `proprietaire` (`id_heros`, `nom`), `obtention` (`id_heros`, `ile`, `date`) et, pour les légendaires qui ont changé de pattes, `historique`. Les collections `heros` et `clans` suivent le même principe. Pour voir un document : `db.tresors.findOne({nature: "potion"})`.
:::

## Ticket 1 · Les potions d'invisibilité longues [7 min]{.duree}

> « Pour l'événement de la Lune Rousse, on veut offrir une récompense aux Héros qui possèdent une potion d'invisibilité d'au moins 5 minutes. Combien de potions sont concernées ? »
> — le studio

```js
db.tresors.countDocuments({nature: "potion", "attributs.effet": ___, "attributs.duree_s": {$gte: ___}})
```

**Pour vérifier** : vous obtenez un nombre entre 250 et 350.

**Pour la fiche** : `duree_s` n'existe que dans les potions. Que se passe-t-il pour les autres Trésors quand on filtre dessus ? Faut-il une colonne `duree_s` vide pour les armes ?

## Ticket 2 · Qui a eu la Griffe d'Aube entre les pattes ? [8 min]{.duree}

> « Un Joueur affirme que son Héros a possédé la Griffe d'Aube (Trésor 12) avant qu'on la lui vole. Sortez-nous la liste des propriétaires successifs, avec les dates. »
> — le studio

1. Regardez d'abord le document entier : `db.tresors.findOne({_id: 12})`.
2. Puis dépliez la liste `historique` : une ligne par propriétaire.

```js
db.tresors.aggregate([{$match: {_id: 12}}, {$unwind: "$___"}, {$project: {_id: 0, id_heros: "$historique.id_heros", debut: "$historique.debut", fin: "$historique.fin"}}])
```

**Pour vérifier** : trois lignes ; la dernière a une `fin` vide, c'est le propriétaire actuel.

**Pour la fiche** : en Séance 1, cet historique était une association entre Héros et Trésor, donc une table à part. Pourquoi est-il ici rangé **dans** le document ? Jusqu'à quelle taille de liste est-ce raisonnable ?

## Ticket 3 · L'Île la plus généreuse [8 min]{.duree}

> « On rééquilibre les Îles pour la prochaine Saison. Sur quelle Île les Héros ont-ils obtenu le plus de Trésors légendaires ? »
> — le studio

```js
db.tresors.aggregate([{$match: {rarete: ___}}, {$group: {_id: "$obtention.___", nombre: {$sum: 1}}}, {$sort: {nombre: -1}}, {$limit: 1}])
```

**Pour vérifier** : une seule ligne, une Île de bas niveau. Enlevez `{$limit: 1}` pour voir le classement complet.

**Pour la fiche** : l'agrégation est une suite d'étapes (`$match`, `$group`, `$sort`...). À quelle requête SQL correspond-elle ?

## Ticket 4 · Une nouvelle nature : les montures [10 min]{.duree}

> « La Saison 5 introduit les montures : des Trésors qui ont une vitesse, un nombre de places et qui volent ou non. On en offre une à Moustique le Gourmand (Héros 3426) pour la tester. »
> — le studio

1. Ajoutez la monture, sans rien déclarer avant :

```js
db.tresors.insertOne({_id: 900001, nom: "Chat-ailé des Nuages", nature: "monture", rarete: "épique", attributs: {vitesse: 12, places: 2, vole: true}, proprietaire: {id_heros: 3426, nom: "Moustique le Gourmand"}})
```

2. Retrouvez-la avec `countDocuments` sur la nature `"monture"` : vous devez obtenir 1.
3. Écrivez la même commande avec une faute de frappe (`atributs` au lieu de `attributs`, `_id: 900002`). MongoDB l'accepte-t-il ?
4. Remettez la base en état : `db.tresors.deleteMany({_id: {$in: [900001, 900002]}})`.

**Pour la fiche** : en PostgreSQL, que faudrait-il faire avant d'ajouter une monture ? La souplesse que vous venez de voir est-elle une force, un danger, ou les deux ?

## Ticket bonus · Les légendaires du Cercle de l'Aube

> « Quels Trésors légendaires sont aux mains des Héros du Cercle de l'Aube (Clan 1) ? »
> — le studio

Les Trésors et les Héros sont dans deux collections. MongoDB sait les rapprocher avec `$lookup`, une étape d'agrégation :

```js
db.heros.aggregate([{$match: {"clan.id_clan": 1}}, {$lookup: {from: "tresors", localField: "_id", foreignField: "proprietaire.id_heros", as: "tresors"}}, {$unwind: "$tresors"}, {$match: {"tresors.rarete": "légendaire"}}, {$project: {_id: 0, heros: "$nom", tresor: "$tresors.nom"}}])
```

**Pour la fiche** : comparez avec la jointure SQL équivalente. Si cette question revient à chaque affichage, que feriez-vous du modèle ?

## Votre fiche synthèse [15 min]{.duree}

Remplissez la fiche synthèse (document à part) : deux cas d'usage sur Félicia, une requête type que vous savez expliquer, deux forces, deux limites, et un besoin pour lequel vous **ne** choisiriez **pas** le document. C'est votre support pour les 8 minutes de la redistribution.
