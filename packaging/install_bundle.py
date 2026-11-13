"""Offline, per-user Windows installation. Run with the enclosed Python."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def verify(root):
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    for name, expected in manifest.items():
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise RuntimeError('Missing package file: ' + name)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Damaged package file: ' + name)
    print('Package verified:', len(manifest), 'files', flush=True)


def check_runtime(root):
    code = '''
import tkinter, customtkinter, psutil, pywinauto, win32api, pythoncom
import onnxruntime, uiautomator2, PIL
from rapidocr import RapidOCR
from playwright.sync_api import sync_playwright
from amazon_android.otp import browser_launch_options
import amazon_android.desktop
engine = RapidOCR()
with sync_playwright() as p:
    with p.chromium.launch(**browser_launch_options('chrome'), headless=True) as browser:
        page = browser.new_page()
        page.set_content('<title>offline-check</title>')
        assert page.title() == 'offline-check'
print('Python, GUI, OCR models, UiAutomator2 and browser: OK')
'''
    subprocess.run([str(root / 'runtime/python.exe'), '-s', '-c', code], cwd=root, check=True)


def main():
    if '--check' in sys.argv:
        verify(ROOT)
        check_runtime(ROOT)
        return
    print('Swarmote Tool - offline setup for Windows x64', flush=True)
    verify(ROOT)
    # A new directory avoids replacing files belonging to an open session.
    target = Path(os.environ['LOCALAPPDATA']) / 'Programs' / 'SwarmoteTool' / time.strftime('%Y%m%d-%H%M%S')
    print('Installing to:', target, flush=True)
    shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('__pycache__'))
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64') as key:
            vc_installed = winreg.QueryValueEx(key, 'Installed')[0] == 1
    except OSError:
        vc_installed = False
    if not vc_installed:
        print('Installing Microsoft Visual C++ Runtime. Confirm the Microsoft installer if prompted.', flush=True)
        result = subprocess.run([str(target / 'installers/vc_redist.x64.exe'), '/install', '/passive', '/norestart'])
        if result.returncode not in (0, 1638, 3010):
            raise RuntimeError('Microsoft runtime installer failed: ' + str(result.returncode))
        if result.returncode == 3010:
            print('Microsoft runtime requests a Windows restart after setup.', flush=True)
    check_runtime(target)
    swarmote = Path(os.environ['LOCALAPPDATA']) / 'Programs/Swarmote/Swarmote.exe'
    if not swarmote.is_file():
        print('Complete the included Swarmote installer, then return here.', flush=True)
        subprocess.run([str(target / 'installers/Swarmote-1.2.0.exe')], check=True)
    adb = swarmote.parent / 'resources/adb/bin/win/adb.exe'
    if not swarmote.is_file() or not adb.is_file():
        raise RuntimeError('Swarmote/ADB missing. Install Swarmote for this Windows user, then run setup again.')
    subprocess.run([str(adb), 'version'], check=True)
    shortcut_code = '''
from pathlib import Path
from win32com.shell import shell, shellcon
from amazon_android.windows_identity import create_shortcut
desktop = Path(shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOPDIRECTORY, None, 0))
programs = Path(shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAMS, None, 0))
create_shortcut(desktop / 'Swarmote Tool.lnk')
create_shortcut(programs / 'Swarmote Tool.lnk')
'''
    subprocess.run([str(target / 'runtime/pythonw.exe'), '-s', '-c', shortcut_code], cwd=target, check=True)
    print('Installed. Open Swarmote Tool from Desktop. Sign in to your own Swarmote account.', flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('SETUP FAILED:', error, flush=True)
        sys.exit(1)
