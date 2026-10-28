// Séance 3, démonstration 1 : les Trésors en document (MongoDB), 9 minutes.
// Ouvrir le terminal : make mongosh. Copier les étapes une par une.
// Chaque requête est rejouée par `make verify` (verification/requetes/04-s3-demonstrations.toml).

// 1. Un Trésor est un document : ses attributs, son propriétaire et son historique sont rangés ensemble.
//    La Griffe d'Aube du cahier des charges : trois Héros l'ont eue entre les pattes.
db.tresors.findOne({_id: 12})

// 2. L'inventaire de Moustique le Gourmand (Héros 3426, Sorcier du Cercle de l'Aube) :
//    sept Trésors de six natures (deux potions), six formes d'attributs différentes, dans une seule collection.
db.tresors.find({"proprietaire.id_heros": 3426}, {nom: 1, nature: 1, attributs: 1})

// 3. On interroge un attribut propre à une nature, même rangé dans une liste :
//    combien de grimoires contiennent le sort « Griffe de foudre » ?
db.tresors.countDocuments({nature: "grimoire", "attributs.sorts": "Griffe de foudre"})

// 4. Agrégation : dégâts moyens des armes selon leur élément.
//    La ligne « null » regroupe les armes qui n'ont pas d'élément : l'attribut est absent, pas vide.
db.tresors.aggregate([{$match: {nature: "arme"}}, {$group: {_id: "$attributs.element", degats_moyens: {$avg: "$attributs.degats"}, nombre: {$sum: 1}}}, {$sort: {nombre: -1}}])

// 5. Le studio ajoute un éclat aux Trésors de l'Aube : nouvel attribut, aucune migration de schéma.
db.tresors.updateOne({_id: 12}, {$set: {"attributs.eclat": "aube dorée"}})
db.tresors.findOne({_id: 12}, {nom: 1, attributs: 1})

// 6. La limite : le nom du Clan est recopié dans chaque document Héros (pas de jointure).
//    Renommer le Cercle de l'Aube, c'est modifier tous ces documents, et la cohérence est à la charge de l'application.
db.heros.countDocuments({"clan.id_clan": 1})

// Remise en état (à la fin de la démonstration, pour la rejouer à l'identique).
db.tresors.updateOne({_id: 12}, {$unset: {"attributs.eclat": ""}})
