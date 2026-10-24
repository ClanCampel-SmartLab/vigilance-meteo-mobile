# Obtenir votre clé API Météo-France

1. Ouvrez https://portail-api.meteofrance.fr/ depuis le lien du formulaire.
2. Créez un compte ou connectez-vous et terminez sa validation si demandée.
3. Recherchez l’API Vigilance / Données publiques Vigilance correspondant à DPVigilance.
4. Lisez les conditions d’utilisation et activez votre accès selon la procédure du portail.
5. Générez une API Key autorisée pour cette API ; vérifiez durée de validité et quotas.
6. Collez uniquement sa valeur dans l’intégration, sans `!secret`.

Les libellés du portail peuvent évoluer ; sa documentation prévaut. Un compte ne donne pas forcément accès à toutes les API.
Cette intégration utilise une API Key dans l’en-tête `apikey`, pas un jeton OAuth Bearer.

```text
GET https://public-api.meteofrance.fr/public/DPVigilance/v1/cartevigilance/encours
accept: application/json
apikey: VOTRE_CLE
```

Le bulletin national est partagé entre les profils. Votre adresse et vos coordonnées ne sont pas placées dans la requête.
Timeout de 30 secondes. Les tests et les anciens scripts utilisant la même clé peuvent consommer votre quota.

## En cas d’erreur

- 401/403 : vérifier clé, validité, type d’authentification et autorisation API.
- 429 : respecter les quotas et augmenter l’intervalle si nécessaire.
- 5xx/timeout : réessayer ultérieurement. Aucun faux bulletin vert n’est créé.
- 200 avec structure non reconnue : contenu rejeté.

## Remplacer la clé

Utilisez Reconfigurer sur l’entrée ou le parcours de réauthentification proposé par Home Assistant.
La clé reste dans le stockage local de configuration, sans chiffrement supplémentaire par l’intégration.
Protégez votre instance et ses sauvegardes. Révoquez toute clé exposée.
Ni secrets.yaml ni configuration.yaml ne sont modifiés ; aucun rest_command n’est nécessaire.
