# Dépannage

## Capteur introuvable

- Vérifier le serveur actuellement ouvert : téléphone et navigateur peuvent pointer vers deux instances différentes.
- Activer Geocoded location DANS l'application Companion, pas seulement l'entité côté Home Assistant.
- Vérifier la sélection du serveur pour l'envoi des capteurs.
- Dans Paramètres → Appareils et services → Entités, inclure les entités désactivées.
- Chercher geocoded, le nom de l'appareil ou le nom traduit. Ne pas inventer un entity_id.

## Capteur unknown/unavailable ou sans département

- Vérifier localisation système, autorisations, réseau et accès au serveur.
- Rouvrir Companion et actualiser ; attendre une remontée. Les données ne sont pas instantanées.
- Vérifier les réglages de confidentialité des capteurs et localisation pour ce serveur.
- Android : examiner les restrictions de batterie si les mises à jour cessent en arrière-plan.
- iOS : vérifier le format d'attributs et les limites de compatibilité de cette bêta.
- Ne pas remplacer une position inconnue par le département du domicile : cela enverrait un faux bulletin en voyage.

## Action notify introuvable

- Connecter l'application officielle au serveur qui exécute l'intégration.
- Vérifier la présence du téléphone dans Mobile App.
- Outils de développement → Actions → rechercher notify.mobile_app_.
- Réouvrir l'application et laisser Home Assistant terminer son chargement.
- Si l'action a été renommée/supprimée, retirer puis recréer le destinataire dans les options.

## Pas de notification

1. Tester d'abord directement notify.mobile_app_… avec un message simple.
2. Vérifier les autorisations et canaux de notification, le mode Ne pas déranger et la connexion du téléphone.
3. Vérifier les attributs du capteur source.
4. Examiner le capteur de vigilance : status et department.
5. Vérifier exclusions, niveau minimum, activation automatique et validité du bulletin.
6. Utiliser le service test, puis lire sa réponse ou l'événement de résultat.
7. Un test ignore le seuil et la désactivation automatique, mais pas une exclusion ou une position inconnue.

## Mauvais téléphone notifié

Désactiver l'automatique. Tester chaque notify séparément puis corriger l'association dans les options.
Le nom du capteur et celui de l'action n'ont pas forcément le même suffixe.

## Problème API

Voir [API.md](API.md). Une clé expirée/refusée demande une réauthentification ou reconfiguration.
Augmenter l'intervalle si quota limité. Les anciens scripts utilisant la même clé consomment aussi ce quota.
Les données en cache ne sont pas utilisées pour notifier après un échec de récupération signalé par le coordinateur.

## Intégration absente après copie

- Vérifier l'arborescence : custom_components/vigilance_meteo_mobile/manifest.json.
- Redémarrer complètement Home Assistant, puis rechercher Vigilance météo mobile dans Ajouter une intégration.
- Consulter Paramètres → Système → Journaux.
- Vérifier la version Home Assistant minimale déclarée et les erreurs Python.
- Cette bêta n'a pas encore été exécutée dans un vrai Home Assistant : un défaut d'intégration reste possible.

## Icône/couleur différente

Android et les constructeurs choisissent le rendu ; le thème peut modifier la perception du jaune.
Le logo du dépôt n'est pas la petite icône système. Sur iOS, ne pas attendre le même rendu qu'Android.
Les images locales brand sont prévues pour Home Assistant 2026.3+.

## Ouvrir un ticket sans données privées

Indiquer version Home Assistant, Companion, Android/iOS, version de l'intégration, étapes et erreur pertinente.
Ne pas partager clé API, adresse exacte, coordonnées GPS, fichiers .storage, sauvegardes ou captures non masquées.
Masquer aussi les noms/identifiants de destinataires si vous ne souhaitez pas les publier.
