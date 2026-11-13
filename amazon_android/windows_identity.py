"""Stable Windows taskbar identity and explicit relaunch target."""
import ctypes
import subprocess
import sys
from pathlib import Path

APP_ID = "Swarmote.AmazonWorkspace"
APP_NAME = "Swarmote Tool"
ROOT = Path(__file__).resolve().parent.parent


def runtime() -> Path:
    candidate = ROOT / ".venv" / "Scripts" / "pythonw.exe"
    return candidate if candidate.is_file() else Path(sys.executable)


def relaunch_command() -> str:
    return subprocess.list2cmdline([str(runtime()), "-m", "amazon_android.desktop"])


def set_process_identity() -> None:
    if sys.platform == "win32":
        function = ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID
        function.argtypes = [ctypes.c_wchar_p]
        function.restype = ctypes.c_long
        function(APP_ID)


def set_window_identity(hwnd: int) -> None:
    if sys.platform != "win32":
        return
    import win32gui
    from win32com.propsys import propsys, pscon

    hwnd = win32gui.GetAncestor(hwnd, 2) or hwnd
    store = propsys.SHGetPropertyStoreForWindow(hwnd, propsys.IID_IPropertyStore)
    # Relaunch properties must precede AppUserModel.ID (which refreshes pinning).
    for key, value in ((pscon.PKEY_AppUserModel_RelaunchCommand, relaunch_command()),
                       (pscon.PKEY_AppUserModel_RelaunchDisplayNameResource, APP_NAME),
                       (pscon.PKEY_AppUserModel_RelaunchIconResource,
                        str(ROOT / "amazon_android" / "assets" / "swarmote_tool.ico") + ",0"),
                       (pscon.PKEY_AppUserModel_ID, APP_ID)):
        store.SetValue(key, propsys.PROPVARIANTType(value))
    store.Commit()


def create_shortcut(path: Path) -> None:
    import pythoncom
    from win32com.shell import shell
    from win32com.propsys import propsys, pscon

    link = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None,
        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    link.SetPath(str(runtime()))
    link.SetArguments("-m amazon_android.desktop")
    link.SetWorkingDirectory(str(ROOT))
    link.SetDescription(APP_NAME)
    icon = ROOT / "amazon_android" / "assets" / "swarmote_tool.ico"
    if icon.is_file():
        link.SetIconLocation(str(icon), 0)
    store = link.QueryInterface(propsys.IID_IPropertyStore)
    store.SetValue(pscon.PKEY_AppUserModel_ID, propsys.PROPVARIANTType(APP_ID))
    store.Commit()
    link.QueryInterface(pythoncom.IID_IPersistFile).Save(str(path), True)
