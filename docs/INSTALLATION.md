# Installation guidée : du téléphone à l'intégration

Les intitulés varient selon Android/iOS, Companion, HACS et la langue de l'interface.
Ne pas confondre activation d'une entité côté serveur et activation de la collecte sur le téléphone.

## 1. Vérifier le bon serveur

Ouvrir Companion sur le téléphone et choisir le serveur qui exécutera l'intégration.
Avec deux maisons, vérifier le serveur du tableau de bord ET celui sélectionné dans les paramètres des capteurs.
Sur ce serveur, le téléphone doit apparaître dans Paramètres → Appareils et services → Mobile App.
Pour les déplacements, configurer un accès distant sûr et fonctionnel. Ne pas exposer Home Assistant sur Internet sans protection.

## 2. Android : activer le capteur

1. Dans les paramètres Android de l'application Home Assistant, autoriser les notifications.
2. Autoriser la localisation précise et en arrière-plan si nécessaire et si vous acceptez ce fonctionnement.
3. Vérifier que la localisation du téléphone est activée.
4. Dans Companion : Paramètres → Application Companion → Gérer les capteurs / Manage sensors.
5. Chercher « Geocoded location » / « Localisation géocodée » et activer le capteur.
6. Si plusieurs serveurs sont configurés, ouvrir les réglages par serveur de ce capteur et activer l'envoi au bon serveur.
7. Vérifier également les capteurs/options « Background location » et la confidentialité d'envoi des capteurs.
8. Revenir dans l'application, attendre une mise à jour et vérifier côté serveur.

Le mode GPS haute précision permanent n'est pas requis ; éviter de l'activer sans comprendre son coût en batterie.
Si les données s'arrêtent en arrière-plan, examiner les restrictions de batterie du constructeur et la documentation Companion.

## 3. iPhone : activation et limites

Dans Réglages iOS → Applications → Home Assistant (ou Réglages → Home Assistant), vérifier les autorisations de notification et de localisation.
Pour le suivi en arrière-plan, vérifier « Toujours » et « Position exacte » si proposés et acceptés.
Dans Companion : Paramètres → Application Companion → Capteurs / Sensors → Geocoded location.
Sélectionner le bon serveur et vérifier les options de confidentialité d'envoi.
Les mises à jour dépendent d'iOS. La bêta attend `iso_country_code` et `sub_administrative_area` : vérifier leur présence.
Tous les formats de capteur iOS ne sont pas pris en charge ; icônes/couleurs de notification différentes d'Android.

## 4. Vérifier le capteur côté Home Assistant

1. Sur le bon serveur : Outils de développement → États.
2. Filtrer avec `geocoded` ou chercher le nom du téléphone.
3. Lire la colonne Appareil pour ne pas confondre les téléphones.
4. Exemple d'identifiant : `sensor.mon_telephone_geocoded_location`.
5. Vérifier qu'il n'est pas unknown/unavailable et qu'il contient :

```yaml
iso_country_code: FR
sub_administrative_area: Morbihan
```

Exemple uniquement ; ne pas forcer ces valeurs. Le département doit être celui de la dernière position.
Un device_tracker n'est pas le capteur géocodé attendu.
Si l'entité est désactivée : Paramètres → Appareils et services → Entités → inclure les entités désactivées et activer celle du téléphone.
Il faut AUSSI activer le capteur dans Companion. Ne pas partager une capture complète contenant votre adresse.

## 5. Vérifier l'action de notification

Ce n'est pas un « capteur de notification ».

1. Outils de développement → Actions (anciennement Services).
2. Rechercher `notify.mobile_app_`.
3. Choisir l'action du téléphone. Le suffixe n'est pas forcément identique au nom du capteur.
4. Tester en adaptant :

```yaml
action: notify.mobile_app_mon_telephone
data:
  message: "Test de notification Home Assistant"
```

5. Vérifier quel téléphone reçoit réellement le message. Refaire pour chaque appareil.
6. Corriger l'association si le mauvais téléphone reçoit.

Cette bêta utilise les actions Companion pour transmettre notification_icon et color. Une action générique notify.send_message ne les remplace pas automatiquement.

## 6. Installer

### HACS

Ajouter l'URL du dépôt comme dépôt personnalisé, catégorie Intégration. Télécharger la préversion voulue si nécessaire.
Redémarrer Home Assistant, puis Ajouter une intégration dans Appareils et services.
L'ajout du dépôt HACS n'ajoute pas à lui seul une entrée configurée.

### Localement pour validation

Copier `custom_components/vigilance_meteo_mobile` dans `/config/custom_components/`, sans niveau supplémentaire.
Le manifeste doit être `/config/custom_components/vigilance_meteo_mobile/manifest.json`.
Sauvegarder avant copie et redémarrer Home Assistant.

## 7. Assistant de configuration

1. La première page contient le guide API et le portail officiel. Saisir la valeur de votre clé.
2. Ajouter un téléphone/une position.
3. Choisir dans la liste un capteur géocodé identifiable : les batteries et autres capteurs ne sont pas proposés.
4. Un capteur actif encore unknown peut apparaître avec « position pas encore reçue ». Il ne sera pas notifié avant une position exploitable.
5. Choisir une destination Companion. Plusieurs destinations cochées reçoivent toutes le bulletin de la MÊME position.
6. Nom facultatif : Papa, Maman ou n'importe quel libellé. Vide = nom du téléphone. Pas besoin de créer une personne Home Assistant.
7. Pour deux personnes qui peuvent voyager séparément, ajouter deux profils avec leurs positions respectives.
8. Les réglages avancés sont séparés. Aucune exclusion par défaut ; automatique désactivé.
9. Vérifier le récapitulatif et valider pour enregistrer.

Si aucun capteur ou aucune action n'est disponible, l'écran d'aide explique les prérequis et permet de réessayer.
La détection peut échouer sur un format non reconnu : il faut alors corriger/compléter la compatibilité, pas choisir un faux capteur.

## 8. Tester

Ouvrir la fiche virtuelle de votre profil et appuyer sur Envoyer une notification de test.
Le dernier résultat est visible dans les attributs du capteur et dans l'exemple de carte.
Automatique à activer seulement après vérification du département, des destinations et des exclusions.

## Références officielles

- https://companion.home-assistant.io/docs/core/sensors/
- https://companion.home-assistant.io/docs/core/location/
- https://companion.home-assistant.io/docs/notifications/notifications-basic/
