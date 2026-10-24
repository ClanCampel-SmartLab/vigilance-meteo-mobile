# Réglages, tests et limites

## Options disponibles

Paramètres → Appareils et services → entrée Vigilance météo mobile → Configurer/Options (selon version).

| Réglage | Défaut | Fonction |
|---|---|---|
| Actualisation | 30 min | De 15 à 1440 minutes ; adapter aux quotas API et au délai accepté. |
| Niveau minimum automatique | Jaune | Vert, jaune, orange ou rouge. Ne s'applique pas au test manuel. |
| Départements exclus | Vide | Codes séparés par des virgules, sans obligation de remplir. Liste commune à tous les destinataires. |
| Notifications automatiques | Désactivées | Activer seulement après test. Peut provoquer un premier envoi immédiat. |
| Destinataires | Aucun | Ajouter au moins un téléphone et associer capteur/action. |

Aucun département n'est exclu par défaut et aucun téléphone n'est imposé.
Pour changer le capteur ou l'action d'un destinataire existant, le retirer puis le recréer ; son identifiant et sa mémoire de notification changent.
Les changements ne sont enregistrés qu'après Terminer et enregistrer. L'intégration est ensuite rechargée.

## Test manuel de tous les téléphones configurés

```yaml
action: vigilance_meteo_mobile.test
data: {}
```

Ce test envoie réellement une notification. Il ignore le seuil minimum et la désactivation des envois automatiques.
Il respecte TOUJOURS : exclusions, position inconnue, pays non couvert, département absent et validité du bulletin.
S'il ne peut pas envoyer, il retourne un motif plutôt que d'inventer une position.

## Test manuel d'un seul téléphone

1. Dans Outils de développement → États, ouvrir le capteur `Vigilance météo …` créé pour le destinataire.
2. Copier son attribut `recipient_id`.
3. Adapter :

```yaml
action: vigilance_meteo_mobile.test
data:
  recipient_id: IDENTIFIANT_COPIE_DANS_LE_CAPTEUR
```

Ce n'est ni le nom de la personne, ni le nom du téléphone, ni son entity_id.
Pour éviter tout envoi automatique pendant les premiers essais, conserver l'automatique désactivé.

## Résultats du test

Le service accepte une réponse facultative contenant les résultats par identifiant.
L'événement `vigilance_meteo_mobile_result` fournit également les motifs ; l'écouter dans Outils de développement → Événements si nécessaire.

| Motif | Signification |
|---|---|
| test_envoye | Appel de notification accepté ; ne garantit pas la lecture ni la livraison physique. |
| envoye | Notification automatique appelée. |
| position_inconnue | Capteur absent, unknown ou unavailable. |
| departement_non_pris_en_charge | Pays/attributs non reconnus ou territoire non couvert. |
| departement_exclu | Code présent dans les exclusions choisies par l'utilisateur. |
| bulletin_perime | Aucune période J actuellement valide. |
| departement_absent | Zone départementale absente du bulletin. |
| bulletin_invalide | Niveau, dates ou structure de zone non interprétables. |
| api_indisponible | Pas de récupération réussie disponible. |
| sous_le_seuil | Niveau inférieur au seuil automatique. |
| deja_envoye | Dernière signature identique pour ce destinataire. |
| automatique_desactive | Aucun envoi automatique autorisé. |
| action_notification_absente | Action notify supprimée ou non chargée. |
| erreur_notification | Erreur signalée par Home Assistant pendant l'appel. |

Un capteur inconnu n'entraîne pas nécessairement une erreur rouge : il peut être ignoré normalement.

## Actualisation

```yaml
action: vigilance_meteo_mobile.refresh
data: {}
```

Actualise le bulletin. Si l'automatique est activé, les règles habituelles peuvent déclencher un envoi.
Une mise à jour du capteur de position réévalue les destinataires avec le bulletin en cache s'il est encore valide.
Ce n'est pas une promesse de notification immédiate après chaque déplacement.

## Doublons

Le dernier bulletin envoyé est mémorisé par destinataire dans le stockage local Home Assistant.
La signature inclut le département, la période, le niveau et les créneaux des phénomènes, pas uniquement l'heure de publication.
Une simple republication à l'identique ne suffit donc pas à renvoyer le même message.
Une nouvelle journée, un changement de département ou des niveaux/horaires peut déclencher un nouvel envoi.
Il s'agit de la DERNIÈRE signature, pas d'un historique illimité : après un autre bulletin, un retour peut notifier à nouveau.

Les messages ont un tag par destinataire pour remplacer le précédent visuellement. Un tag ne garantit pas l'absence de son/vibration.
Le test utilise un tag séparé et ne modifie pas la mémoire des envois automatiques.

## Icônes et couleurs

Vent : vent ; pluie : pluie ; orages : éclair ; crues : vagues ; neige : neige ; canicule : thermomètre haut ; grand froid : thermomètre bas ; avalanches : alerte.
Un seul phénomène au niveau le plus élevé : son icône. Plusieurs à égalité : alerte. Aucun phénomène au-dessus du vert : nuage/éclaircie.
La couleur suit le maximum départemental vert/jaune/orange/rouge. Le jaune peut varier selon l'écran/thème.
Android décide où appliquer la couleur ; l'icône de la barre d'état peut rester monochrome. iOS ne garantit pas ce rendu.
L'icône du dépôt avec la signature est distincte de ces petites icônes de notification.

## Limites de couverture et de temps

- Métropole et Corse, 96 départements ; pas d'outre-mer.
- Zones départementales uniquement, pas les sous-zones littorales séparées. Aucune couverture complète vagues-submersion n'est revendiquée.
- Bulletin J seulement ; pas de notifications dédiées à demain.
- Le maximum d'aujourd'hui n'est pas nécessairement actif maintenant. Les créneaux déjà passés peuvent encore apparaître.
- Horaires convertis selon le fuseau configuré dans Home Assistant, pas nécessairement le fuseau du téléphone.
- Le département est issu de `iso_country_code` et `sub_administrative_area`. Pas de géocodage de coordonnées par l'intégration.
- Les variantes non reconnues d'attributs, notamment selon iOS, ne sont pas garanties.
- Pas de contrôle fiable de l'ancienneté GPS : une dernière position peut être ancienne sans état unknown.
- Pas de plages silencieuses, répétitions d'urgence, accusés de lecture ni annonce Google dans cette bêta.
- La disponibilité des données/API et de la notification mobile n'est pas garantie.

## Désinstallation

1. Désactiver les envois automatiques et supprimer l'entrée dans Appareils et services.
2. Supprimer l'intégration via HACS, ou retirer son dossier après arrêt approprié de Home Assistant.
3. Redémarrer.
4. Vérifier les éventuels capteurs orphelins dans le registre des entités.
5. Le stockage de déduplication peut subsister dans .storage. Ne pas modifier .storage à chaud ; sa suppression ne doit être faite qu'avec sauvegarde et connaissance du fonctionnement de Home Assistant.
6. Révoquer la clé au portail Météo-France si elle ne sert plus.
