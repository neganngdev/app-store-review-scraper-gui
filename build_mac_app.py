#!/usr/bin/env python3
"""
Build script to create a macOS .app bundle for App Store Review Scraper.
This creates a standalone application that can be moved to /Applications.
"""

import os
import shutil
import subprocess
import sys

APP_NAME = "App Store Review Scraper"
BUNDLE_ID = "com.huykgit98.appstorereviewscraper"
VERSION = "0.2.0"

def create_app_bundle():
    """Create the macOS .app bundle structure."""
    
    print("🚀 Building macOS Application Bundle...")
    
    # Clean previous build
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Install PyInstaller if needed
    print("📦 Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Create spec file for PyInstaller
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['app.engine', 'app.appstore_engine', 'app.ui_main', 'app.models'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{APP_NAME}',
)

app = BUNDLE(
    coll,
    name='{APP_NAME}.app',
    icon=None,
    bundle_identifier='{BUNDLE_ID}',
    version='{VERSION}',
    info_plist={{
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '{VERSION}',
    }},
)
'''
    
    with open('app_bundle.spec', 'w') as f:
        f.write(spec_content)
    
    # Build the app
    print("🔨 Building application bundle...")
    subprocess.run([
        "pyinstaller",
        "--clean",
        "--noconfirm",
        "app_bundle.spec"
    ], check=True)
    
    app_path = f"dist/{APP_NAME}.app"
    
    if os.path.exists(app_path):
        print(f"\n✅ SUCCESS! Application built at: {app_path}")
        print(f"\n📋 To install:")
        print(f"   1. Open Finder and navigate to: {os.path.abspath('dist')}")
        print(f"   2. Drag '{APP_NAME}.app' to your Applications folder")
        print(f"   3. Launch from Applications or Spotlight")
        print(f"\n⚠️  Note: First launch may show 'unidentified developer' warning.")
        print(f"   Go to System Settings > Privacy & Security and click 'Open Anyway'")
    else:
        print("❌ Build failed - .app bundle not found")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = create_app_bundle()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
