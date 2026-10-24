"""Renseigne les métadonnées depuis GITHUB_REPOSITORY ou un argument owner/repo."""
import json
import os
import re
import sys
from pathlib import Path
repo = sys.argv[1] if len(sys.argv) > 1 else os.getenv("GITHUB_REPOSITORY", "")
if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
    raise SystemExit("Usage : python tools/prepare_repository.py identifiant/depot")
root = Path(__file__).resolve().parents[1]
p = root / "custom_components/vigilance_meteo_mobile/manifest.json"
data = json.loads(p.read_text(encoding="utf-8"))
data.update(documentation=f"https://github.com/{repo}", issue_tracker=f"https://github.com/{repo}/issues", codeowners=["@" + repo.split("/")[0]])
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
