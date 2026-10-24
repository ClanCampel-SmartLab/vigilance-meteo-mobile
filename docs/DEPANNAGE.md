# Dépannage

## Capteur absent ou inconnu

Vérifier le bon serveur, l’activation de Geocoded location dans Companion, son envoi vers ce serveur et l’entité activée dans Home Assistant.
Vérifier autorisations, localisation système, accès distant et restrictions de batterie. Rouvrir l’application et attendre une mise à jour.
La détection utilise les noms/identifiants géocodés et les attributs attendus. Un format particulier non reconnu peut demander une adaptation.
Ne pas forcer un département fixe pour contourner une position inconnue.

## Notification absente ou mauvais téléphone

Tester directement notify.mobile_app_… depuis les outils de développement.
Vérifier autorisations, canaux, mode Ne pas déranger, réseau et association du profil.
Deux destinations d’un profil reçoivent le bulletin de la même position. Créer deux profils pour des positions indépendantes.
Lire last_test_status, la réponse d’action ou l’événement de résultat. Exclusion/position inconnue n’est pas nécessairement une panne.

## Mise à jour et affichage

Vérifier la version installée, télécharger la bonne release et redémarrer complètement Home Assistant.
Actualiser le navigateur ou rouvrir Companion si les textes sont anciens.
Conserver l’entrée pour permettre la migration ; vérifier ses options avant réactivation de l’automatique.

## Capteurs, boutons et carte

Les fiches sont virtuelles et associées à l’intégration. Le bouton test est dans les contrôles du profil.
L’heure de pression du bouton n’est pas une confirmation de livraison.
Un nom de carte personnalisé peut masquer le nom du profil : l’effacer ou le corriger.
Pour l’exemple de carte, remplacer les entity_id par les vrais, y compris ceux des boutons.

## Icônes

Images locales : custom_components/vigilance_meteo_mobile/brand.
Une version de HACS peut afficher Icon not available même si l’image fonctionne dans Appareils et services.
Dans le README, l’image utilise une URL brute absolue pour éviter les problèmes de chemins relatifs.
Les icônes/couleurs de notification dépendent du système et ne sont pas le logo du dépôt.

## API

Consulter API.md. Vérifier clé, souscription et quota. Les scripts parallèles consomment aussi ce quota.
Une récupération échouée ne déclenche pas un faux bulletin vert.

## Signaler un problème

Fournir versions, étapes et erreur utile, sans clé, adresse, coordonnées, sauvegarde ou fichier .storage.
Conserver l’ancienne release pour permettre une investigation et un retour contrôlé si nécessaire.
