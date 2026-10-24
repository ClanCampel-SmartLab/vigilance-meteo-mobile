# Votre carte de vigilance

Aucun tableau de bord n’est modifié automatiquement. Aucune extension frontend n’est requise pour les cartes proposées.

## Sans YAML

1. Appareils et services → Vigilance météo mobile → fiche du profil.
2. Sélectionner son capteur, puis Ajouter au tableau de bord si proposé.
3. Ou tableau de bord → Modifier → Ajouter une carte → Tuile, sélectionner le capteur.
4. Ajouter une carte Bouton pour le test individuel, puis une autre pour l’actualisation commune si souhaité.

Le capteur principal reprend le nom de sa fiche, par exemple Vigilance météo — Micki.
Si la carte a un nom personnalisé fixe, il reste prioritaire : l’effacer pour reprendre le nom de l’entité.
Une tuile simple ne garantit pas automatiquement une couleur ou une présentation détaillée.

## Exemple détaillé

Le fichier examples/carte-vigilance.yaml est fourni dans le dépôt.

1. Copier les identifiants réels du capteur du profil, de son bouton test et du bouton central Actualiser.
2. Remplacer toutes leurs occurrences dans l’exemple.
3. Tableau de bord → Modifier → Ajouter une carte → Manuel : coller le YAML adapté.
4. Prévisualiser et enregistrer.

Ne pas deviner les entity_id : Home Assistant peut conserver les anciens après mise à jour.
La carte affiche nom, département, niveau, phénomènes/horaires, statut et dernier test.
Elle comporte une confirmation avant envoi du test ; cela ne modifie pas la fermeture de l’assistant de configuration.
Pas d’adresse complète, de coordonnées ni de carte géographique imposée.
Le maximum du bulletin n’est pas nécessairement la vigilance active à cet instant.
