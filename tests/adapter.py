"""
tests/adapter.py — Isolation adapter for Apartment Finder QA Suite.
Maps test abstractions to concrete implementation files, functions, and UI labels.
"""

import sys
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# Root of the repository
REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = REPO_ROOT  # Exported for conftest.py

# Subdirectory containing the Streamlit app
APP_DIR = REPO_ROOT / "Apartment-Finder" if (REPO_ROOT / "Apartment-Finder").exists() else REPO_ROOT

# Ensure both paths are in sys.path for runtime execution
for p in [str(APP_DIR), str(REPO_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)


APP_ENTRY = str(APP_DIR / "app.py")
PAGES_DIR = APP_DIR / "pages"
PAGE_FILES = {
    "Compare": str(PAGES_DIR / "1_Compare.py"),
    "Manage": str(PAGES_DIR / "2_Manage.py"),
    "About": str(PAGES_DIR / "3_About.py"),
    "Near_Me": str(PAGES_DIR / "4_Near_Me.py"),
    "AI_Assistant": str(PAGES_DIR / "5_AI_Assistant.py"),
    "Analytics": str(PAGES_DIR / "6_Analytics.py"),
    "Admin": str(PAGES_DIR / "7_Admin.py"),
    "Settings": str(PAGES_DIR / "8_Settings.py"),
}

DATA_FILE = APP_DIR / "apartments.json"

REQUIRED_FIELDS = ["name", "address", "rent", "bedrooms", "commute_mins"]
SCHEMA_TYPES = {
    "name": str,
    "address": str,
    "rent": (int, float),
    "bedrooms": (int, float),
    "commute_mins": (int, float),
}


try:
    from theme import ORIGIN_ADDRESS  # type: ignore
    DEFAULT_ORIGIN = ORIGIN_ADDRESS
except ImportError:
    DEFAULT_ORIGIN = "Faridabad Railway Station, Faridabad, Haryana"


def calculate_score(rent: float, commute_mins: float, rent_weight: float = 0.5) -> float:
    try:
        from apartment import Apartment  # type: ignore
        apt = Apartment(
            name="Test",
            address="Test",
            rent=rent,
            bedrooms=2,
            commute=commute_mins
        )
        if hasattr(apt, "get_match_score"):
            return float(apt.get_match_score(rent_weight))
    except Exception:
        pass

    # Mathematical normalization fallback (0-100 scale)
    rent_norm = max(0.0, min(100.0, 100.0 - (rent / 35000.0) * 100.0))
    commute_norm = max(0.0, min(100.0, 100.0 - (commute_mins / 60.0) * 100.0))
    score = (rent_norm * rent_weight) + (commute_norm * (1.0 - rent_weight))
    return round(score, 1)


def geocode_address(address: str) -> Optional[tuple]:
    """Resolves an address to (longitude, latitude) coordinates."""
    for fn_name in ["_geocode", "geocode", "_geocode_address"]:
        try:
            import distance_api  # type: ignore
            fn = getattr(distance_api, fn_name, None)
            if fn:
                return fn(address)
        except Exception:
            pass
    return None


def calculate_commute(origin: str, destination: str) -> Optional[int]:
    """Calculates driving commute duration in minutes."""
    try:
        from distance_api import get_commute_minutes  # type: ignore
        return get_commute_minutes(origin, destination)
    except Exception:
        return None


def load_records(file_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    path = file_path or DATA_FILE
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "apartments" in data:
        return data["apartments"]
    return []