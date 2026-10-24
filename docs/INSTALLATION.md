# Installation complète

Les intitulés varient selon les versions et langues de Home Assistant, Companion et du système mobile.

## 1. Vérifier le serveur

Ouvrez Companion sur chaque téléphone et choisissez le serveur qui exécutera l’intégration.
Avec plusieurs maisons, vérifiez également les réglages d’envoi des capteurs au serveur concerné.
Sur celui-ci, le téléphone doit apparaître dans l’intégration Mobile App.
Un accès distant sûr et fonctionnel est nécessaire pour remonter les données en déplacement hors du réseau local.

## 2. Activer Geocoded location sur Android

1. Autorisez les notifications dans les paramètres Android de Home Assistant.
2. Vérifiez la localisation système et les autorisations précise/en arrière-plan adaptées à votre usage.
3. Dans Companion : Paramètres → Application Companion → Gérer les capteurs / Manage sensors.
4. Recherchez Geocoded location / Localisation géocodée et activez-le.
5. Avec plusieurs serveurs, activez l’envoi du capteur au bon serveur.
6. Vérifiez également les réglages Background location et la confidentialité des capteurs.
7. Rouvrez l’application et attendez une mise à jour côté serveur.

L’activation d’une entité dans Home Assistant ne suffit pas si la collecte est désactivée dans le téléphone.
Le mode GPS haute précision permanent n’est pas requis. Si les remontées cessent en arrière-plan, consultez les restrictions de batterie du constructeur.

## 3. iPhone

Dans Réglages iOS → Applications → Home Assistant (ou Réglages → Home Assistant), vérifiez les autorisations de notification et de localisation.
Pour les remontées en arrière-plan, examinez Toujours et Position exacte si proposés et acceptés.
Dans Companion : Paramètres → Application Companion → Capteurs / Sensors → Geocoded location.
Choisissez le bon serveur et vérifiez l’envoi des capteurs.

iOS décide en partie des moments de mise à jour. L’intégration attend `iso_country_code` et `sub_administrative_area` ; tous les formats ne sont pas garantis.
Les icônes/couleurs n’ont pas nécessairement le rendu Android.

## 4. Vérifier le capteur géocodé

1. Sur le bon serveur : Outils de développement → États.
2. Recherchez geocoded ou le nom du téléphone.
3. Vérifiez l’appareil associé pour ne pas confondre les téléphones.
4. Le capteur doit fournir un pays et un département ; exemple :

```yaml
iso_country_code: FR
sub_administrative_area: Morbihan
```

Ceci n’est pas une configuration à forcer. Le département doit correspondre à la dernière position reçue.
Le `device_tracker` n’est pas le capteur géocodé demandé.
Si l’entité est désactivée : Paramètres → Appareils et services → Entités → inclure les entités désactivées puis l’activer, en plus de l’activation dans Companion.
Un état unknown/unavailable ne permet pas d’envoyer un bulletin fiable.
Ne partagez pas de capture avec l’adresse complète.

## 5. Vérifier la notification

Il s’agit d’une action, pas d’un capteur de notification.
Outils de développement → Actions → rechercher notify.mobile_app_.
Testez chaque téléphone avec son action exacte :

```yaml
action: notify.mobile_app_mon_telephone
data:
  message: "Test de notification Home Assistant"
```

Vérifiez physiquement le téléphone qui reçoit. Ne devinez pas les correspondances d’après les suffixes.
Cette intégration utilise les actions Companion pour les options avancées ; notify.send_message n’est pas automatiquement interchangeable ici.

## 6. Installer via HACS

Tant que le dépôt n’est pas accepté au catalogue par défaut :

1. HACS → menu → Dépôts personnalisés.
2. Ajouter https://github.com/ClanCampel-SmartLab/vigilance-meteo-mobile, catégorie Intégration.
3. Télécharger la version publiée, puis redémarrer Home Assistant.
4. Paramètres → Appareils et services → Ajouter une intégration → Vigilance météo mobile.

Pour une installation locale, copier le dossier custom_components/vigilance_meteo_mobile dans /config/custom_components/ et redémarrer.
Éviter un niveau de sous-dossier supplémentaire. Sauvegarder avant toute installation ou mise à jour.

## 7. Configurer

1. Saisir la clé API ; les liens d’aide sont sur cette page.
2. Ajouter un profil et choisir la position géocodée dans la liste.
3. Choisir une ou plusieurs destinations de notification.
4. Nom facultatif : libre, sans lien avec une personne Home Assistant. Vide = nom du téléphone.
5. Deux personnes voyageant séparément : deux profils. Une position et deux destinations = un même bulletin copié aux deux.
6. Régler le seuil, la fréquence et les exclusions facultatives. Rien n’est exclu par défaut.
7. Conserver l’automatique désactivé pour le premier test.
8. Valider le récapitulatif final pour enregistrer.

Fermer la fenêtre avant cette validation abandonne les changements. Le clic extérieur est géré par Home Assistant ; l’intégration n’intercepte pas cette fermeture.

## 8. Tester

Ouvrir la fiche virtuelle du profil et appuyer sur Envoyer une notification de test.
Vérifier destinataire, département et horaires avant d’activer l’automatique.
Le test respecte exclusions et positions inconnues.

## Références

- https://companion.home-assistant.io/docs/core/sensors/
- https://companion.home-assistant.io/docs/core/location/
- https://companion.home-assistant.io/docs/notifications/notifications-basic/
