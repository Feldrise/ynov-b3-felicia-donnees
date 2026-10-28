// Index des collections Félicia (après mongoimport).
db.heros.createIndex({ "clan.id_clan": 1 });
db.heros.createIndex({ "joueur.id_joueur": 1 });
db.tresors.createIndex({ "proprietaire.id_heros": 1 });
db.tresors.createIndex({ rarete: 1, nature: 1 });
print("index MongoDB : ok");
