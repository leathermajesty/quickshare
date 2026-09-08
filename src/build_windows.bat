@echo off
echo Building QuickShare.exe...
python -m pip install --upgrade pyinstaller
python -m PyInstaller --onefile --name QuickShare quickshare.py
echo.
echo Done. The executable is in the dist folder:
echo dist\QuickShare.exe
pause
