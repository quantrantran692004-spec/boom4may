"""First-run prerequisite check and launcher for the Swarmote desktop tool."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
VENV_PYTHON = VENV / "Scripts" / "python.exe"
VENV_PYTHONW = VENV / "Scripts" / "pythonw.exe"
READY_FILE = VENV / ".swarmote_tool_ready.json"

DOWNLOADS = {
    "Python 3.11+": "https://www.python.org/downloads/windows/",
    "Google Chrome": "https://www.google.com/chrome/",
    "Microsoft Edge": "https://www.microsoft.com/edge/download",
    "Swarmote": "https://www.swarmote.com/web/download",
}


def _app_paths(app: str) -> list[Path]:
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    program_files = Path(os.environ.get("PROGRAMFILES", r"C:\Program Files"))
    program_files_x86 = Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"))
    if app == "Google Chrome":
        return [
            program_files / "Google/Chrome/Application/chrome.exe",
            program_files_x86 / "Google/Chrome/Application/chrome.exe",
            local / "Google/Chrome/Application/chrome.exe",
        ]
    if app == "Microsoft Edge":
        return [
            program_files / "Microsoft/Edge/Application/msedge.exe",
            program_files_x86 / "Microsoft/Edge/Application/msedge.exe",
            local / "Microsoft/Edge/Application/msedge.exe",
        ]
    if app == "Swarmote":
        return [local / "Programs/Swarmote/Swarmote.exe"]
    raise ValueError(app)


def _app_installed(app: str) -> bool:
    if any(path.is_file() for path in _app_paths(app)):
        return True
    executable = {
        "Google Chrome": "chrome.exe",
        "Microsoft Edge": "msedge.exe",
        "Swarmote": "Swarmote.exe",
    }[app]
    return shutil.which(executable) is not None


def _ready_file_matches() -> bool:
    if not READY_FILE.is_file():
        return False
    try:
        state = json.loads(READY_FILE.read_text(encoding="utf-8"))
        return (state.get("root") == str(ROOT)
                and state.get("pyproject_mtime_ns") == (ROOT / "pyproject.toml").stat().st_mtime_ns)
    except (OSError, ValueError, AttributeError):
        return False


def _runtime_imports_work() -> bool:
    code = (
        "import psutil, pywinauto, customtkinter, playwright, PIL, rapidocr, onnxruntime, uiautomator2; "
        "from importlib.metadata import version; version('amazon-android-tool')"
    )
    result = subprocess.run([str(VENV_PYTHON), "-c", code], cwd=ROOT,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0


def _offer_downloads(missing: list[str]) -> None:
    print("Required software is missing:")
    for name in missing:
        print(f"  - {name}: {DOWNLOADS[name]}")
    print("Install the missing software, then run this launcher again.")
    answer = input("Open the official download pages now? [Y/n] ").strip().casefold()
    if answer in {"", "y", "yes"}:
        for name in missing:
            webbrowser.open(DOWNLOADS[name])


def _check_external_apps() -> bool:
    missing = []
    if not any(_app_installed(browser)
               for browser in ("Google Chrome", "Microsoft Edge")):
        # One installed browser is enough; list both supported options.
        print("OTP reading needs Google Chrome or Microsoft Edge; neither was found.")
        for name in ("Google Chrome", "Microsoft Edge"):
            print(f"  - {name}: {DOWNLOADS[name]}")
        answer = input("Open the official browser download pages now? [Y/n] ").strip().casefold()
        if answer in {"", "y", "yes"}:
            for name in ("Google Chrome", "Microsoft Edge"):
                webbrowser.open(DOWNLOADS[name])
        missing.append("browser")
    if not _app_installed("Swarmote"):
        missing.append("Swarmote")
    if "Swarmote" in missing:
        _offer_downloads(["Swarmote"])
    return not missing


def _install_python_dependencies() -> bool:
    if VENV_PYTHON.is_file() and _ready_file_matches() and _runtime_imports_work():
        print("Python dependencies: ready")
        return True

    print("Project Python dependencies are missing or need repair.")
    print("The installer will create .venv and download the declared packages from PyPI.")
    answer = input("Install them now? [Y/n] ").strip().casefold()
    if answer not in {"", "y", "yes"}:
        print("Setup stopped. Run this launcher again after choosing to install dependencies.")
        return False

    if not VENV_PYTHON.is_file():
        result = subprocess.run([sys.executable, "-m", "venv", str(VENV)], cwd=ROOT)
        if result.returncode:
            print("Could not create the project virtual environment.")
            return False

    result = subprocess.run([str(VENV_PYTHON), "-m", "pip", "install", "-e", "."],
                            cwd=ROOT)
    if result.returncode:
        print("Dependency installation failed; the desktop app was not started.")
        return False
    if not _runtime_imports_work():
        print("Installed packages could not be imported; the desktop app was not started.")
        return False

    READY_FILE.write_text(json.dumps({
        "root": str(ROOT),
        "pyproject_mtime_ns": (ROOT / "pyproject.toml").stat().st_mtime_ns,
    }, indent=2), encoding="utf-8")
    print("Python dependencies: installed")
    return True


def main() -> int:
    if sys.version_info < (3, 11):
        print("Python 3.11 or newer is required.")
        _offer_downloads(["Python 3.11+"])
        return 1
    if not _check_external_apps():
        print("Setup stopped until the required browser and Swarmote are installed.")
        return 1
    if not _install_python_dependencies():
        return 1
    print("Starting Swarmote Tool. In Swarmote, open Terminal > ADB Shell on a running Profile to connect its phone.")
    subprocess.Popen([str(VENV_PYTHONW), "-m", "amazon_android.desktop"], cwd=ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
