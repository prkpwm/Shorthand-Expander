@echo off
echo Building Shorthand Expander...
echo.

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the executable
pyinstaller build_exe.spec

echo.
echo Build complete! Executable is in the dist folder.
echo.

REM Create shortcut in current directory
if exist "dist\ShorthandExpander.exe" (
    echo Creating shortcut in project folder...
    set "EXE_PATH=%CD%\dist\ShorthandExpander.exe"
    set "SHORTCUT_DIR=%CD%"
    cscript //nologo create_shortcut.vbs "%EXE_PATH%" "%SHORTCUT_DIR%"
    echo.
    echo Done! Shortcut created: Shorthand Expander.lnk
) else (
    echo Error: ShorthandExpander.exe not found in dist folder.
)

echo.
pause
