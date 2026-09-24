"""Apply migrations before serving; optional empty-database demo seed."""

import os
import subprocess
import sys

from app.config import settings


def main() -> None:
    """Fail startup if the schema cannot be upgraded."""
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)
    if settings.SEED_DEMO:
        subprocess.run([sys.executable, "-m", "app.seed"], check=True)
    os.execvp("uvicorn", ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])


if __name__ == "__main__":
    main()
