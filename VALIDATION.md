# Vérifications de génération — 0.1.0-beta.2

- 10 fichiers Python : syntaxe analysée avec ast.parse.
- JSON et YAML : lecture réussie.
- 27 tests purs exécutés et réussis : départements, exclusions vides, désactivation automatique par défaut,
  validité et limites horaires, formes JSON, icônes, couleurs et signatures.
- Outil de préparation des métadonnées exécuté dans une copie isolée, avec propriétaire/dépôt fictifs de test.
- Icônes PNG et source SVG incluses ; archive contrôlée après création.

## Non effectué

- Exécution dans un vrai Home Assistant, import complet de ses dépendances.
- Validation des parcours UI/Options/Réauthentification.
- Requête authentifiée Météo-France avec une vraie clé.
- Livraison de notification réelle à partir de cette intégration.
- Tests de redémarrage, déchargement, stockage et concurrence dans Home Assistant.
- Workflows GitHub, validation HACS et hassfest.
- Confirmation des formats de capteur et du rendu sur toutes versions Android/iOS.

Les workflows sont fournis pour aider à ces étapes, sans prétendre qu'ils sont déjà réussis.
Cette archive est une bêta prête à être déposée sur GitHub, PAS une version certifiée ou garantie sans défaut.

## Sortie réelle des tests

```text
test_apostrophe (test_logic.LogicTests.test_apostrophe) ... ok
test_bad_api_shape (test_logic.LogicTests.test_bad_api_shape) ... ok
test_bad_dates (test_logic.LogicTests.test_bad_dates) ... ok
test_coastal_not_department (test_logic.LogicTests.test_coastal_not_department) ... ok
test_corsica (test_logic.LogicTests.test_corsica) ... ok
test_default_automatic_disabled (test_logic.LogicTests.test_default_automatic_disabled) ... ok
test_default_no_exclusion (test_logic.LogicTests.test_default_no_exclusion) ... ok
test_department (test_logic.LogicTests.test_department) ... ok
test_department_list_complete_and_unique (test_logic.LogicTests.test_department_list_complete_and_unique) ... ok
test_direct_api_shape (test_logic.LogicTests.test_direct_api_shape) ... ok
test_end_exclusive (test_logic.LogicTests.test_end_exclusive) ... ok
test_exclusions (test_logic.LogicTests.test_exclusions) ... ok
test_expired_period (test_logic.LogicTests.test_expired_period) ... ok
test_foreign (test_logic.LogicTests.test_foreign) ... ok
test_green (test_logic.LogicTests.test_green) ... ok
test_highest_priority (test_logic.LogicTests.test_highest_priority) ... ok
test_invalid_level (test_logic.LogicTests.test_invalid_level) ... ok
test_missing_attributes (test_logic.LogicTests.test_missing_attributes) ... ok
test_missing_zone (test_logic.LogicTests.test_missing_zone) ... ok
test_naive_dates_rejected (test_logic.LogicTests.test_naive_dates_rejected) ... ok
test_no_default_phone (test_logic.LogicTests.test_no_default_phone) ... ok
test_signature_changes_with_window (test_logic.LogicTests.test_signature_changes_with_window) ... ok
test_signature_ignores_publication (test_logic.LogicTests.test_signature_ignores_publication) ... ok
test_tied_level (test_logic.LogicTests.test_tied_level) ... ok
test_valid_period (test_logic.LogicTests.test_valid_period) ... ok
test_wind_icon_color_and_time (test_logic.LogicTests.test_wind_icon_color_and_time) ... ok
test_wrapped_api_shape (test_logic.LogicTests.test_wrapped_api_shape) ... ok

----------------------------------------------------------------------
Ran 27 tests in 0.003s

OK
```
