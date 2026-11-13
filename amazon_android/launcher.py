"""Entry point shared by the Windows .pyw launcher and Python module runs."""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Use the project's installed dependencies when launched by a .pyw shortcut."""
    root = Path(__file__).resolve().parent.parent
    runtime = root / ".venv" / "Scripts" / "pythonw.exe"
    if runtime.is_file() and Path(sys.executable).resolve().parent != runtime.parent:
        subprocess.Popen(
            [str(runtime), "-m", "amazon_android.desktop"], cwd=root,
            **({"creationflags": subprocess.CREATE_NO_WINDOW} if sys.platform == "win32" else {}))
        return
    from .desktop import main as desktop_main

    desktop_main()


if __name__ == "__main__":
    main()
