# Dépannage

## Pas de capteur dans la liste

- Bon serveur dans Companion et dans le navigateur ?
- Geocoded location activé sur le téléphone ET envoi au bon serveur ?
- Entité activée côté Home Assistant ? Inclure les entités désactivées dans la recherche.
- Le filtre utilise nom/identifiant géocodé, registre et attributs attendus. Un format particulier peut nécessiter une adaptation du code.
- Une simple batterie ou un device_tracker n'est pas proposé, volontairement.

## Position inconnue

Vérifier autorisations de localisation, réseau, accès distant, confidentialité des capteurs et restrictions batterie.
Rouvrir Companion et attendre une mise à jour. Ne pas forcer un département fixe pour contourner l'erreur.
Sur iOS, vérifier les attributs réellement envoyés et les limites décrites dans l'installation.

## Pas d'action Companion

Le téléphone doit être enregistré dans Mobile App sur ce serveur.
Outils de développement → Actions → notify.mobile_app_. Tester un message direct.
Après renommage/suppression d'une action, modifier le profil dans les options.

## Pas de message après test

- Vérifier les permissions et canaux de notification, le mode Ne pas déranger et le réseau du téléphone.
- Vérifier le BON profil et ses destinations.
- Lire last_test_status du capteur, réponse d'action ou événement vigilance_meteo_mobile_result.
- Le test respecte les exclusions ; une exclusion ou une position inconnue n'est pas une panne.
- Bouton Actualiser différent du bouton Envoyer une notification de test.

## Mauvais téléphone

Désactiver l'automatique, tester les actions Companion séparément et corriger l'association.
Plusieurs destinations d'un profil reçoivent la MÊME position. Pour deux positions indépendantes, créer deux profils.

## Ancien formulaire après mise à jour

Vérifier version 0.1.0-beta.3 dans le manifeste installé, téléchargement de la bonne préversion et redémarrage complet.
Actualiser ensuite le navigateur ou rouvrir Companion. Ne pas supprimer d'abord l'entrée : conserver la possibilité de migration.
Les options migrées peuvent conserver le nom saisi en bêta 2 ; le nom facultatif concerne les nouveaux champs, pas un effacement de votre choix.

## Pas de fiche ou bouton

La nouvelle version doit être chargée après redémarrage. Les fiches sont virtuelles et apparaissent dans les appareils associés à l'intégration.
Consulter les journaux si le chargement des plateformes sensor/button échoue.
Les boutons n'ont pas d'état marche/arrêt ; leur état est l'heure de la dernière pression et peut être unknown avant la première.

## API

Voir API.md : clé, souscription, quota et timeout. Les anciens scripts utilisant la même clé consomment aussi le quota.
Une récupération échouée ne permet pas de notifier en prenant silencieusement un ancien bulletin comme neuf.

## Icône

Les PNG sont dans custom_components/vigilance_meteo_mobile/brand.
L'icône d'Appareils et services peut fonctionner même si une version de HACS affiche Icon not available.
Ne pas confondre logo de l'intégration et petites icônes météo des notifications.

## Ticket public

Fournir versions Home Assistant/Companion/système/intégration et erreur pertinente.
Ne pas publier clé, adresse, coordonnées, .storage, secrets.yaml ou sauvegarde.
Cette bêta reste à valider dans Home Assistant ; un défaut du code est possible malgré les tests locaux.
