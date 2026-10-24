"""Tests purs sans importer le runtime Home Assistant : python tests/run.py."""
import importlib.util
import sys
import types
import unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for name,path in [("custom_components",root/"custom_components"),("custom_components.vigilance_meteo_mobile",root/"custom_components/vigilance_meteo_mobile")]:
    module=types.ModuleType(name)
    module.__path__=[str(path)]
    sys.modules[name]=module
spec=importlib.util.spec_from_file_location("test_logic",root/"tests/test_logic.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(module))
raise SystemExit(not result.wasSuccessful())
