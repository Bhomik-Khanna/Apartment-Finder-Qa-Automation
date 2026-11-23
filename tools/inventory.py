

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# Look inside 'Apartment-Finder' subfolder if it exists, otherwise root
APP_DIR = REPO_ROOT / "Apartment-Finder" if (REPO_ROOT / "Apartment-Finder").exists() else REPO_ROOT


def inspect_file(file_path: Path):
    if not file_path.exists():
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            node = ast.parse(f.read(), filename=str(file_path))
    except Exception as e:
        return {"error": str(e)}

    classes = [n.name for n in ast.walk(node) if isinstance(n, ast.ClassDef)]
    functions = [n.name for n in ast.walk(node) if isinstance(n, ast.FunctionDef)]
    return {"classes": classes, "functions": functions}


def run_inventory():
    print("=" * 60)
    print(f"  APARTMENT FINDER — PROJECT INVENTORY")
    print(f"  Scanning: {APP_DIR.name}/")
    print("=" * 60)

    key_files = [
        "app.py",
        "Landing.py",
        "theme.py",
        "apartment.py",
        "distance_api.py",
        "storage.py",
        "apartments.json",
    ]

    for fname in key_files:
        p = APP_DIR / fname
        status = "EXISTS" if p.exists() else "MISSING"
        print(f"[{status:7s}] {fname}")
        if p.suffix == ".py" and p.exists():
            info = inspect_file(p)
            if info and "functions" in info:
                funcs = ", ".join(info["functions"][:6])
                if len(info["functions"]) > 6:
                    funcs += f" (+{len(info['functions']) - 6} more)"
                print(f"           Functions: {funcs or 'None'}")
                if info["classes"]:
                    print(f"           Classes:   {', '.join(info['classes'])}")

    
    pages_dir = APP_DIR / "pages"
    if pages_dir.exists():
        pages = list(pages_dir.glob("*.py"))
        print(f"\n[FOUND]   {len(pages)} pages in pages/ directory:")
        for pg in sorted(pages):
            print(f"           - {pg.name}")
    else:
        print("\n[MISSING] pages/ directory")

    print("=" * 60)


if __name__ == "__main__":
    run_inventory()