# v1.0.0 — Vigilance météo mobile

Vos alertes météo vous accompagnent dans vos déplacements.
Une intégration Home Assistant signée **by clan'campel**.

## Fonctionnalités

- Bulletins de vigilance Météo-France selon la dernière position géocodée.
- Plusieurs profils avec leurs positions et destinations personnelles.
- Notifications avec icône et couleur dynamiques.
- Seuil, fréquence et exclusions facultatives ; aucun département exclu par défaut.
- Configuration graphique, liens API et aide Companion intégrés.
- Boutons de test individuels, actualisation commune et exemple de carte native.
- Limitation des doublons par profil et destination.

## Installation et mise à jour

Ajouter le dépôt dans HACS, télécharger v1.0.0 puis redémarrer Home Assistant.
Pour une installation existante, conserver l’entrée et vérifier les options après mise à jour.
Garder l’automatique désactivé jusqu’au contrôle du premier test.

## Couverture

France métropolitaine et Corse, zones départementales, bulletin d’aujourd’hui.
Sous-zones littorales et outre-mer non couverts. Dernière position connue, pas de suivi GPS instantané garanti.
Consulter le README pour les limites détaillées et les bulletins officiels.

La publication stable du projet est distincte de son acceptation au catalogue HACS par défaut.
