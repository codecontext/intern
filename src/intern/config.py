from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = Path(
    os.getenv("INTERN_DATA_DIR", PROJECT_ROOT / "data")
)

STORAGE_DIR = Path(
    os.getenv("INTERN_STORAGE_DIR", PROJECT_ROOT / "storage")
)
