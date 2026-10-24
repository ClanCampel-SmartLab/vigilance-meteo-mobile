# Ajouter une carte intuitive au tableau de bord

Aucune carte n'est ajoutée automatiquement sans votre accord.
Deux possibilités : cartes natives en interface ou exemple YAML fourni ; aucune extension frontend obligatoire.

## Simple, sans YAML

1. Paramètres → Appareils et services → Vigilance météo mobile.
2. Ouvrir la fiche virtuelle du profil voulu.
3. Sélectionner son capteur Vigilance et utiliser Ajouter au tableau de bord si proposé.
4. Ou ouvrir le tableau de bord → Modifier → Ajouter une carte → Tuile et choisir ce capteur.
5. Ajouter une carte Bouton avec le bouton Envoyer une notification de test du même profil.
6. Ajouter si souhaité le bouton central Actualiser le bulletin.

Les intitulés et possibilités de sélection varient selon la version Home Assistant.
La tuile native simple ne promet pas automatiquement la présentation détaillée ou la couleur dynamique de l'exemple.

## Carte détaillée native

L'exemple complet est dans `examples/carte-vigilance.yaml`.

1. Dans les outils de développement → États, retrouver le capteur de vigilance du profil et copier son entity_id.
2. Retrouver le bouton de test de ce même profil et copier son entity_id.
3. Retrouver le bouton commun Actualiser le bulletin et copier son entity_id.
4. Ouvrir le fichier d'exemple et remplacer TOUTES les occurrences des trois entity_id d'exemple.
5. Dans le tableau de bord : Modifier → Ajouter une carte → Manuel, coller le YAML adapté.
6. Prévisualiser et enregistrer.

Les entity_id sont attribués par Home Assistant et peuvent conserver les anciens noms après migration. Ne pas les deviner.
L'exemple utilise Markdown, vertical-stack et button natifs. Il contient une confirmation avant l'envoi du test.
Cette confirmation de CARTE n'est pas une confirmation de fermeture de l'assistant de configuration.

## Affichage

- Nom du profil.
- Couleur représentée par un symbole de niveau et nom de vigilance.
- Département et code, sans adresse complète ni coordonnées.
- Phénomènes et créneaux horaires.
- Statut de position/données/exclusion.
- Dernier résultat de test si disponible.
- Boutons Tester et Actualiser.

Les détails viennent des attributs department, department_name, level, level_name, phenomena, recipient_name et last_test_status.
La carte n'est PAS une carte géographique avec suivi GPS et ne publie pas l'adresse du téléphone.
Le niveau signifie maximum d'aujourd'hui, pas alerte active à l'instant présent.

Le YAML et ses gabarits ont été vérifiés syntaxiquement, pas rendus dans un vrai frontend Home Assistant pendant la génération.
