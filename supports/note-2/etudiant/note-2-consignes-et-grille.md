---
title: "Note 2 : consignes et grille"
soustitre: Concevoir une architecture polyglotte, puis l'adapter au Patch Day
surtitre: Note 2 · Séance 4, vendredi 13 novembre, 13h30 à 16h00
public: Support étudiant
---

## L'essentiel

::: bloc
- **En trinôme** (binôme toléré), sur le Sujet de Note 2 tiré en Séance 2. La Note 2 compte pour **60 %** de la moyenne du module.
- **Tout se fait en Séance 4** : 1 h 30 pour la V1, 45 minutes pour le Patch Day, 15 minutes pour le rendu. Rien à préparer avant.
- **Documents et Familier autorisés**, sans restriction. Je note votre jugement : chaque choix se justifie par les contraintes chiffrées de **votre** sujet, pas par l'avis du Familier.
- **Rendu sur Moodle, en PDF**, un dépôt par groupe : la V1 à **15h00**, le reste à **15h55** au plus tard. Un PDF par pièce, inutile de les assembler.
:::

## Le déroulé

| Heure | Ce que vous faites | Ce que vous déposez |
|--------|------------------------------------------------------------|------------------------|
| 13h30 | rappel de ces consignes (3 minutes) | |
| 13h33 | conception de la **V1** : schéma, matrice, modèle de données de la brique principale ; « 10 minutes » annoncé à 14h40 | |
| 14h50 | export en PDF et dépôt | **V1**, avant 15h00 |
| 15h00 | tirage de la carte **Patch Day** par votre représentant | |
| 15h03 | **V2** adaptée et **ADR** | |
| 15h45 | bilan du Journal du Familier, export et dépôt | **V2, ADR, Journal du Familier**, avant 15h55 |
| 15h55 | retour à chaud sur le module | |

La V1 déposée à 15h00 ne se modifie plus : c'est elle qui est notée, et d'elle que part l'adaptation. Pendant la V1, chacun prend sa pause quand il veut, sans arrêter le trinôme.

## La V1 : trois pièces

1. **Le schéma d'architecture** : une boîte par base et son contenu, les flux (qui écrit, qui lit, comment les copies sont alimentées) avec le délai accepté par copie, et la **source de vérité** de chaque donnée, marquée. Outil libre : draw.io (diagrams.net), un autre outil, ou une feuille photographiée lisiblement.
2. **La matrice « besoin → paradigme → justification »**, une ligne par besoin, sur `matrice-de-decision-modele.docx` : chaque justification cite au moins une ligne de la grille de choix et un chiffre du sujet.
3. **Le modèle de données de la brique principale**, la base qui porte l'essentiel des données et la source de vérité : 5 à 8 tables, collections ou familles de clés, avec nom, attributs principaux, clé et liens, sans les types. Les règles de gestion du sujet qui pèsent dessus s'écrivent à côté.

## Le Patch Day : deux pièces

À 15h00, votre représentant tire une **carte Patch Day** : un événement imprévu et chiffré. Vous avez 42 minutes. La ligne **« L'ADR doit trancher »** de la carte donne la question à laquelle l'ADR répond.

1. **La V2**, sans tout refaire : une copie annotée du **schéma** de la V1, où ce qui change est **repéré** d'un coup d'œil (couleur, encadré ou mention « V2 ») ; dans la **matrice**, les seules lignes qui changent ou s'ajoutent, marquées « V2 » ; la partie modifiée du modèle de la brique principale, s'il change.
2. **L'ADR**, sur `adr-modele.docx`, **en puces** si vous voulez : le contexte chiffré, la décision, au moins deux options écartées et pourquoi, les conséquences (gain, perte acceptée, coût d'exploitation). Le Familier peut proposer des pistes, mais le choix se justifie par les contraintes de la carte et de votre sujet.

## Le Journal du Familier

Un Journal par groupe (`journal-du-familier-modele.docx`), tenu **au fil de l'eau** : une ligne par prompt, copié tel quel ou en lien de partage, et votre décision (gardé, rejeté, modifié) avec son « parce que... ». Le bilan, trois lignes d'une phrase, s'écrit à 15h45. Un groupe qui n'a pas sollicité le Familier rend quand même le Journal, en expliquant ce choix de méthode : il est noté d'après cette explication et ne perd aucun point pour ne pas s'en être servi.

## La grille de la Note 2 {.nouvelle-page}

| Critère | Ce qui est attendu | Points |
|--------------------------------|----------------------------------------------------------------------|--------|
| **A · La V1 de l'architecture** | | **40** |
| A1 · Matrice | une ligne par besoin ; chaque paradigme justifié par une ligne de la grille et un chiffre du sujet ; le relationnel reste le choix par défaut, aucune base n'est ajoutée sans critère chiffré ; ce qu'on accepte de perdre est écrit | 16 |
| A2 · Schéma d'architecture | chaque base et son rôle ; une source de vérité par donnée ; les flux de synchronisation et le délai accepté pour chaque copie ; un nombre de bases défendable au regard de leur coût d'exploitation | 12 |
| A3 · Modèle de la brique principale | 5 à 8 tables, collections ou familles de clés, avec clés et liens ; les règles de gestion du sujet y sont traduites ou écrites à côté | 12 |
| **B · Le Patch Day et l'ADR** | | **40** |
| B1 · Analyse de l'impact | les besoins et les bases touchés sont nommés ; les chiffres de la carte sont repris et confrontés à ceux de la V1 | 8 |
| B2 · V2 adaptée | une adaptation proportionnée (ni rien changer, ni tout refaire), cohérente avec la V1, aux changements repérés | 14 |
| B3 · ADR | contexte chiffré ; décision claire ; au moins deux options écartées, avec leur raison ; conséquences (gain, perte acceptée, coût d'exploitation) ; justification par les contraintes du sujet et de la carte | 18 |
| **C · Le Journal du Familier** | | **20** |
| C1 · Les prompts | copiés tels quels ou en lien de partage, pendant la V1 et le Patch Day | 6 |
| C2 · Les décisions | gardé, rejeté ou modifié, avec un « parce que... » rattaché au sujet (une règle, un chiffre, une erreur repérée) | 10 |
| C3 · Le bilan | où le Familier a aidé, où il a trompé, ce que vous changeriez | 4 |
| **Total** | | **100** |

La note sur 20 est le total divisé par 5. Tous les membres du groupe reçoivent la même note.

::: {.encadre .astuce}
### Répartir le travail du trinôme

Mon conseil : pour la V1, un membre par pièce, et toutes les 20 minutes chacun relit celle d'un autre. Au Patch Day, cinq minutes à trois sur la carte, puis l'un rédige l'ADR pendant que les deux autres font la V2. À 15h45, l'un écrit le bilan du Journal, les deux autres exportent. Le Journal se tient par celui qui envoie le prompt.
:::
