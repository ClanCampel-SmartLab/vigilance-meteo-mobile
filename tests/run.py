"""Tests purs et runtime simulé, sans installation Home Assistant."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
root = Path(__file__).resolve().parents[1]
for name, path in [("custom_components", root / "custom_components"), ("custom_components.vigilance_meteo_mobile", root / "custom_components/vigilance_meteo_mobile")]:
    module = types.ModuleType(name)
    module.__path__ = [str(path)]
    sys.modules[name] = module
suite = unittest.TestSuite()
for path in sorted((root / "tests").glob("test_*.py")):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
