# Copier sur GitHub et publier

L'affichage « ClanCampel — SmartLab » n'est pas utilisé pour deviner un identifiant GitHub.
Le workflow lit le véritable `GITHUB_REPOSITORY`, par exemple propriétaire/nom-du-dépôt, au moment de la publication.

## 1. Créer le dépôt

1. Se connecter à GitHub avec votre compte.
2. New repository → nom conseillé `vigilance-meteo-mobile` (libre de changer).
3. Choisir Public si le dépôt doit être distribué publiquement par HACS.
4. Créer le dépôt. Ne pas téléverser la clé API ni des fichiers personnels Home Assistant.

## 2. Copier les fichiers

1. Décompresser l'archive.
2. Copier le CONTENU du dossier du projet à la racine du dépôt.
3. La racine doit montrer README.md, hacs.json, custom_components, assets, docs, tests, tools et .github.
4. Ne pas téléverser uniquement le ZIP, ni créer un niveau de dossier projet supplémentaire.
5. Attention : .github et .gitignore sont cachés dans certains explorateurs. Ils doivent être inclus.
6. Dans l'interface Web GitHub : Add file → Upload files, déposer les dossiers/fichiers puis valider le commit.
   Si le navigateur ne transmet pas les fichiers cachés, utiliser GitHub Desktop ou git.

## 3. Préparer automatiquement les métadonnées

Le workflow « Préparer les métadonnées GitHub » s'exécute lors du dépôt des fichiers.
Il remplace les URLs OWNER provisoires de manifest.json avec le vrai propriétaire et le vrai dépôt,
renseigne codeowners et crée un commit. Il ne change PAS le nom public « by clan'campel ».

1. Ouvrir Actions et autoriser les workflows si GitHub le demande.
2. Vérifier la réussite de « Préparer les métadonnées GitHub ».
3. Vérifier que manifest.json ne contient plus OWNER et que codeowners contient le compte propriétaire.
4. En cas de refus du push (droits/protection de branche), utiliser la méthode manuelle ci-dessous.
5. Sur un fork, le workflow automatique est volontairement désactivé ; utiliser la méthode manuelle.

### Méthode manuelle de secours

```bash
python tools/prepare_repository.py VRAI_IDENTIFIANT/VRAI_DEPOT
```

Committer puis pousser le manifest modifié. Ou éditer documentation, issue_tracker et codeowners directement sur GitHub.
Ne pas publier une release ni ajouter à HACS tant que les marqueurs OWNER ne sont pas remplacés.
Un nom d'affichage contenant des espaces n'est pas un identifiant GitHub valide.

## 4. Tests et validations

1. Dans Actions, vérifier « Tests de logique et syntaxe ».
2. Installer localement sur une instance de validation : ajout, options, clé refusée, deux téléphones, position inconnue, exclusion, rechargement et redémarrage.
3. Exécuter manuellement « Validation HACS et hassfest (manuelle) » depuis Actions.
4. Les workflows sont fournis mais n'ont PAS été exécutés lors de la génération de l'archive.
5. Corriger tout échec. La vérification brands est ignorée dans le job HACS car les images locales sont incluses pour Home Assistant 2026.3+ ; cela ne garantit pas l'acceptation au catalogue.
6. Effectuer une revue de code avant de conseiller l'activation automatique à d'autres utilisateurs.

## 5. Créer une release

Après préparation des métadonnées et validation : Releases → Draft a new release.
Tag proposé : v0.1.0-beta.2, marquer comme préversion. Conserver manifest.version = 0.1.0-beta.2.
Sur HACS, l'utilisateur peut devoir autoriser les versions bêta/préreleases.
Une release n'est pas créée automatiquement et l'archive générée n'a rien publié sur votre compte.

## 6. Ajouter comme dépôt personnalisé HACS

Dans HACS : menu des dépôts personnalisés → URL de votre dépôt → catégorie Intégration.
Télécharger puis redémarrer Home Assistant. Ajouter ensuite l'intégration dans Appareils et services.
Les libellés HACS peuvent évoluer. Suivre sa documentation officielle si nécessaire.

L'ajout au catalogue HACS par défaut est distinct et nécessite sa procédure d'acceptation.
Aucune validation HACS ni inscription au catalogue n'est revendiquée pour cette archive.

## Licence et identité

Code fourni sous licence MIT avec attribution « clan'campel / ClanCampel — SmartLab ».
L'identité visuelle demandée porte exactement la signature « by clan'campel ».
Les PNG et SVG fournis constituent une déclinaison vectorielle intégrable, pas une garantie de reproduction pixel pour pixel d'une maquette générée dans une conversation.
Le logo GitHub du dépôt peut être ajouté manuellement à sa présentation ; cette intégration ne modifie pas l'avatar de votre compte GitHub.
Les données Météo-France gardent leurs propres conditions d'usage ; ce n'est pas un produit officiel Météo-France.
