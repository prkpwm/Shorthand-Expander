# Build Instructions for Shorthand Expander

## Prerequisites
Make sure you have all dependencies installed:
```bash
pip install -r requirements_gui.txt
pip install pyinstaller
```

## Build Methods

### Method 1: Using the build script (Recommended)
Simply run:
```bash
./build.bat
```

### Method 2: Using PyInstaller directly
```bash
pyinstaller build_exe.spec
```

### Method 3: One-line command
```bash
pyinstaller --name=ShorthandExpander --onefile --windowed --icon=shorthand/icon.ico --add-data="shorthand/shorthands.txt;shorthand" --add-data="shorthand/icon.ico;shorthand" --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtWidgets --hidden-import=pynput.keyboard --hidden-import=pynput.keyboard._win32 run.py
```

## Output
The executable will be created in the `dist` folder:
- `dist/ShorthandExpander.exe`

## Notes
- The executable includes the shorthands.txt file
- The icon is embedded in the executable
- No console window will appear (GUI only)
- First run may take a few seconds to start

## Troubleshooting
If you get errors about missing modules:
1. Make sure all requirements are installed
2. Try adding the missing module to hiddenimports in build_exe.spec
3. Rebuild using the spec file

## File Size
The executable will be approximately 20-30 MB due to PyQt5 and Python runtime.
