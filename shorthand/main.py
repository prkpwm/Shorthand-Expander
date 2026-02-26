"""Main entry point for shorthand expander"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from shorthand.ui import ShorthandExpanderGUI


def main():
    """Run the application"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = ShorthandExpanderGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
