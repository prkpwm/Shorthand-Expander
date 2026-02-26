# Shorthand Expander

A modern, beautiful text expansion tool for Windows that automatically expands your custom shortcuts into full text as you type.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Features

✨ **Modern UI** - Beautiful, VS Code-inspired interface with gradient backgrounds and smooth animations

⚡ **Real-time Expansion** - Automatically expands shortcuts as you type in any application

📚 **Easy Management** - Add, edit, and delete shortcuts through an intuitive GUI

🔍 **Quick Search** - Find shortcuts instantly with the built-in search box

📊 **Statistics** - Track total shortcuts and expansion count

⏸️ **Pause/Resume** - Press Pause key to temporarily disable expansions

🖥️ **Fullscreen Mode** - Press F11 to toggle fullscreen view

## Screenshots

### Main Interface
Modern sidebar layout with statistics and shorthand management.

### Add/Edit Dialog
Clean dialog for adding or editing shortcuts.

## Installation

### Option 1: Run from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shorthand-expander.git
cd shorthand-expander
```

2. Install dependencies:
```bash
pip install -r requirements_gui.txt
```

3. Run the application:
```bash
python run.py
```

### Option 2: Build Executable

1. Build the standalone executable:
```bash
./build.bat
```

2. The executable will be created in the `dist` folder
3. A desktop shortcut will be created automatically
4. Run `dist/ShorthandExpander.exe`

## Usage

### Adding Shortcuts

1. Click the **Add** button
2. Enter your shorthand (e.g., `abt`)
3. Enter the expansion (e.g., `about`)
4. Click **OK**

### Using Shortcuts

Simply type your shorthand followed by a space or punctuation in any application, and it will automatically expand.

Example:
- Type: `abt ` → Expands to: `about `
- Type: `impl` → Expands to: `implements`

### Keyboard Shortcuts

- **F11** - Toggle fullscreen mode
- **Pause** - Pause/resume expansion
- **Double-click** - Edit a shorthand from the list

### Managing Shortcuts

- **Edit** - Select a shorthand and click Edit (or double-click)
- **Delete** - Select a shorthand and click Delete
- **Search** - Use the search box to filter shortcuts

## Configuration

Shortcuts are stored in `shorthand/shorthands.txt` in tab-separated format:

```
shorthand[TAB]expansion
abt[TAB]about
impl[TAB]implements
cfg[TAB]configure
```

You can edit this file directly or use the GUI.

## Building from Source

### Requirements

- Python 3.9 or higher
- PyQt5
- pynput
- PyInstaller (for building executable)

### Build Steps

1. Install build dependencies:
```bash
pip install pyinstaller
```

2. Run the build script:
```bash
./build.bat
```

3. Create shortcut (if not created automatically):
```bash
powershell -ExecutionPolicy Bypass -File create_shortcut.ps1
```

## Project Structure

```
shorthand-expander/
├── shorthand/
│   ├── core/
│   │   ├── expander.py      # Shorthand expansion logic
│   │   └── listener.py      # Keyboard listener
│   ├── ui/
│   │   ├── main_window.py   # Main GUI window
│   │   ├── dialog.py        # Add/Edit dialog
│   │   └── styles.py        # UI stylesheets
│   ├── main.py              # Application entry point
│   ├── shorthands.txt       # Shorthand dictionary
│   └── icon.ico             # Application icon
├── run.py                   # Launcher script
├── build.bat                # Build script
├── build_exe.spec           # PyInstaller configuration
└── README.md                # This file
```

## Technical Details

### Architecture

- **GUI Framework**: PyQt5 with custom styling
- **Keyboard Monitoring**: pynput library
- **Text Expansion**: Real-time keyboard event processing
- **Data Storage**: Plain text file (tab-separated values)

### Features Implementation

- **Sidebar Layout**: VS Code-inspired vertical sidebar with stats
- **Modern Styling**: Gradient backgrounds, smooth transitions, hover effects
- **Frameless Window**: Custom title bar with drag, resize, and window controls
- **Auto-save**: Changes are immediately saved to file
- **Thread-safe**: Keyboard listener runs in separate thread

## Troubleshooting

### Application won't start
- Make sure all dependencies are installed: `pip install -r requirements_gui.txt`
- Check if Python 3.9+ is installed: `python --version`

### Shortcuts not expanding
- Press Pause key to check if expansion is paused
- Verify shortcuts are loaded (check the count in sidebar)
- Make sure `shorthands.txt` exists and is readable

### Build fails
- Install PyInstaller: `pip install pyinstaller`
- Clear previous builds: Delete `build` and `dist` folders
- Run build again: `./build.bat`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with PyQt5
- Keyboard monitoring powered by pynput
- Inspired by text expansion tools like TextExpander and AutoHotkey

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ by [Your Name]
