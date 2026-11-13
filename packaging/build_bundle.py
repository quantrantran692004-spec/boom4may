"""Build an offline ZIP using the current tested Windows x64 runtime."""
from pathlib import Path
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    name = 'SwarmoteTool-Windows-x64-' + time.strftime('%Y%m%d-%H%M%S')
    output = ROOT / 'dist'
    stage = output / name
    stage.mkdir(parents=True)
    # Include all source, documentation and images; never copy user profiles.
    ignore = shutil.ignore_patterns('.git', '.venv', 'dist', 'build', '__pycache__', '.test_tmp', '*.egg-info')
    shutil.copytree(ROOT, stage, dirs_exist_ok=True, ignore=ignore)
    base = Path(sys.base_prefix)
    runtime = stage / 'runtime'
    runtime.mkdir()
    for filename in ('python.exe', 'pythonw.exe', 'python3.dll', 'python312.dll', 'vcruntime140.dll', 'vcruntime140_1.dll', 'LICENSE.txt'):
        shutil.copy2(base / filename, runtime / filename)
    for folder in ('DLLs', 'Lib', 'tcl'):
        shutil.copytree(base / folder, runtime / folder,
                        ignore=shutil.ignore_patterns('site-packages', '__pycache__'))
    site = runtime / 'Lib/site-packages'
    shutil.copytree(ROOT / '.venv/Lib/site-packages', site,
                    ignore=shutil.ignore_patterns('__pycache__', '__editable__*'))
    (runtime / 'Lib/sitecustomize.py').write_text('''from pathlib import Path
import os, sys
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = str(root / 'browsers')
browser = next((root / 'browsers').glob('chromium-*/chrome-win64/chrome.exe'), None)
if browser:
    os.environ['SWARMOTE_BUNDLED_BROWSER'] = str(browser)
''', encoding='utf-8')
    # Use exactly the Chromium revision requested by this installed Playwright.
    browser_spec = json.loads((site / 'playwright/driver/package/browsers.json').read_text())
    revision = next(b['revision'] for b in browser_spec['browsers'] if b['name'] == 'chromium')
    browser_name = 'chromium-' + revision
    browser_source = ROOT / '.test_tmp/bundle-browsers' / browser_name
    if not browser_source.is_dir():
        browser_source = Path(os.environ['LOCALAPPDATA']) / 'ms-playwright' / browser_name
    shutil.copytree(browser_source, stage / 'browsers' / browser_name)
    installer = Path(os.environ['LOCALAPPDATA']) / 'swarmote-clint-updater/installer.exe'
    expected = 'BQ2X+YzxG+2LwmayuCfYdDUizVibGGat2vZ8Ulxmy4j6rUxtE84UNA1PU0SpK8OS1WYVJwkQFfsGQLQ+/g/LGw=='
    if base64.b64encode(hashlib.sha512(installer.read_bytes()).digest()).decode() != expected:
        raise RuntimeError('Swarmote installer differs from official release SHA512')
    (stage / 'installers').mkdir()
    shutil.copy2(installer, stage / 'installers/Swarmote-1.2.0.exe')
    shutil.copy2(ROOT / '.test_tmp/vc_redist.x64.exe', stage / 'installers/vc_redist.x64.exe')
    shutil.copy2(ROOT / 'packaging/install_bundle.py', stage / 'install_bundle.py')
    (stage / 'CAI_DAT.bat').write_text('@echo off\ncd /d "%~dp0"\nset PYTHONHOME=\nset PYTHONPATH=\n"%~dp0runtime\\python.exe" -s "%~dp0install_bundle.py"\npause\n', encoding='ascii')
    (stage / 'MO_TOOL.bat').write_text('@echo off\ncd /d "%~dp0"\nset PYTHONHOME=\nset PYTHONPATH=\nstart "" "%~dp0runtime\\pythonw.exe" -s -m amazon_android.desktop\n', encoding='ascii')
    (stage / 'DOC_TRUOC.txt').write_text('''SWARMOTE TOOL - WINDOWS 11 x64 (khuyen nghi)
1. Giai nen TOAN BO ZIP vao thu muc tren o dia. Khong chay trong cua so ZIP.
2. Chay CAI_DAT.bat. Python, OCR, UiAutomator2 va Chromium da kem san.
3. Neu may chua co Swarmote, hoan thanh cua so cai Swarmote di kem.
4. Mo Swarmote Tool tren Desktop. Tu dang nhap Swarmote bang tai khoan cua ban.
Can Internet, quyen cloud phone/Profile va proxy/du lieu dau vao cua ban.
Khong kem tai khoan, cookie, OTP, session dang nhap hoac profile tu may nguon.
Lan cai moi tao thu muc rieng; khong ghi de phien dang chay.
Runtime duoc kiem tra import, OCR va trinh duyet offline truoc khi tao shortcut.
Chua kiem thu tren Windows sach/12 dien thoai that. Dong goi khong sua loi luong.
Swarmote 1.2.0: checksum SHA512 doi chieu may chu cap nhat chinh thuc.
''', encoding='utf-8')
    versions = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--format=json'], text=True)
    (stage / 'RUNTIME_VERSIONS.json').write_text(versions, encoding='utf-8')
    files = sorted(p for p in stage.rglob('*') if p.is_file())
    manifest = {p.relative_to(stage).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (stage / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('Built folder:', stage, flush=True)
    env = dict(os.environ)
    env.pop('PYTHONHOME', None)
    env.pop('PYTHONPATH', None)
    subprocess.run([str(runtime / 'python.exe'), '-s', str(stage / 'install_bundle.py'), '--check'], cwd=stage, env=env, check=True)
    archive = output / (name + '.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for path in stage.rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                bundle.write(path, Path(name) / path.relative_to(stage))
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(digest + '  ' + archive.name + '\n')
    print('ZIP:', archive, 'bytes:', archive.stat().st_size, 'SHA256:', digest, flush=True)


if __name__ == '__main__':
    main()
