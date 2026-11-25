#!/usr/bin/env python3
"""Create .venv, upgrade pip, and install requirements.txt."""

import os
import subprocess
import sys
from pathlib import Path

VENV_DIR = Path(".venv")
REQUIREMENTS = Path("requirements.txt")


def venv_python(venv_dir: Path) -> Path:
    scripts = "Scripts" if os.name == "nt" else "bin"
    executable = "python.exe" if os.name == "nt" else "python"
    return venv_dir / scripts / executable


def run(command: list[str]) -> None:
    print(f"+ {' '.join(command)}")
    subprocess.run(command, check=True)


def main() -> None:
    if not REQUIREMENTS.exists():
        sys.exit(f"Missing {REQUIREMENTS.resolve()}")

    if not VENV_DIR.exists():
        run([sys.executable, "-m", "venv", str(VENV_DIR)])
        print(f"Created virtual environment: {VENV_DIR.resolve()}")
    else:
        print(f"Using existing virtual environment: {VENV_DIR.resolve()}")

    python = venv_python(VENV_DIR)
    if not python.exists():
        sys.exit(f"Virtual-environment interpreter not found: {python}")

    # Upgrade pip inside the venv
    run([str(python), "-m", "pip", "install", "--upgrade", "pip"])

    # Install dependencies
    run([str(python), "-m", "pip", "install", "-r", str(REQUIREMENTS)])

    print("\nSetup complete.")
    if os.name == "nt":
        print(f"Activate with: .\\{VENV_DIR}\\Scripts\\Activate.ps1")
    else:
        print(f"Activate with: source {VENV_DIR}/bin/activate")


if __name__ == "__main__":
    main()