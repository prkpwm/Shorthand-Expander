"""Stylesheet definitions for the UI"""


def get_stylesheet() -> str:
    """Get the main application stylesheet"""
    return """
        QWidget#mainWidget {
            background: transparent;
        }
        
        QFrame#sidebar {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(30, 41, 59, 0.98),
                stop:1 rgba(15, 23, 42, 0.98));
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
            border: 2px solid rgba(148, 163, 184, 0.2);
            border-right: 1px solid rgba(148, 163, 184, 0.3);
        }
        
        QWidget#rightContent {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(15, 23, 42, 0.98),
                stop:1 rgba(30, 41, 59, 0.98));
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
            border: 2px solid rgba(148, 163, 184, 0.2);
            border-left: none;
        }
        
        QLabel#appTitle {
            color: #f1f5f9;
            font-size: 26px;
            font-weight: bold;
            padding: 10px;
        }
        
        QLabel#sidebarHeader {
            color: #94a3b8;
            font-size: 16px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        QFrame#statCard {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(51, 65, 85, 0.6),
                stop:1 rgba(30, 41, 59, 0.6));
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        
        QFrame#separator {
            background: rgba(148, 163, 184, 0.2);
            max-height: 1px;
        }
        
        QLabel#versionLabel {
            color: rgba(148, 163, 184, 0.5);
            font-size: 14px;
        }
        
        QFrame#titleBar {
            background: transparent;
            border: none;
            padding: 5px;
        }
        
        QLabel#title {
            color: #f1f5f9;
            font-weight: bold;
            font-size: 32px;
        }
        
        QLabel#statusActive {
            color: #10b981;
            font-size: 26px;
            font-weight: bold;
            padding: 10px 20px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(16, 185, 129, 0.25),
                stop:1 rgba(5, 150, 105, 0.15));
            border-radius: 12px;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }
        
        QLabel#statusPaused {
            color: #f59e0b;
            font-size: 26px;
            font-weight: bold;
            padding: 10px 20px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(245, 158, 11, 0.25),
                stop:1 rgba(217, 119, 6, 0.15));
            border-radius: 12px;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }
        
        QPushButton#controlBtn, QPushButton#closeBtn {
            background: rgba(71, 85, 105, 0.5);
            border: 1px solid rgba(148, 163, 184, 0.3);
            border-radius: 18px;
            color: #e2e8f0;
            font-size: 28px;
            font-weight: bold;
        }
        
        QPushButton#controlBtn:hover {
            background: rgba(100, 116, 139, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.5);
        }
        
        QPushButton#closeBtn:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(239, 68, 68, 0.9),
                stop:1 rgba(220, 38, 38, 0.9));
            border: 1px solid rgba(239, 68, 68, 1);
        }
        
        QFrame#glassPanel {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(51, 65, 85, 0.5),
                stop:1 rgba(30, 41, 59, 0.5));
            border-radius: 18px;
            border: 1px solid rgba(148, 163, 184, 0.15);
        }
        
        QLabel#statNumber {
            color: #60a5fa;
            font-weight: bold;
            font-size: 46px;
        }
        
        QLabel#statLabel {
            color: rgba(226, 232, 240, 0.7);
            font-size: 24px;
            font-weight: 500;
        }
        
        QLabel#panelHeader {
            color: #f1f5f9;
            margin-bottom: 10px;
            font-weight: bold;
            font-size: 28px;
        }
        
        QLineEdit#searchBox {
            background: rgba(15, 23, 42, 0.6);
            border: 2px solid rgba(100, 116, 139, 0.3);
            border-radius: 12px;
            padding: 12px 18px;
            color: #f1f5f9;
            font-size: 26px;
            selection-background-color: rgba(96, 165, 250, 0.4);
        }
        
        QLineEdit#searchBox:focus {
            border: 2px solid rgba(96, 165, 250, 0.6);
            background: rgba(15, 23, 42, 0.8);
        }
        
        QListWidget#shorthandList {
            background: rgba(15, 23, 42, 0.6);
            border: 2px solid rgba(100, 116, 139, 0.2);
            border-radius: 12px;
            padding: 8px;
            color: #e2e8f0;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 24px;
        }
        
        QListWidget#shorthandList::item {
            padding: 12px 15px;
            border-radius: 8px;
            margin: 3px 2px;
            border: 1px solid transparent;
        }
        
        QListWidget#shorthandList::item:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(96, 165, 250, 0.15),
                stop:1 rgba(59, 130, 246, 0.15));
            border: 1px solid rgba(96, 165, 250, 0.3);
        }
        
        QListWidget#shorthandList::item:selected {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(96, 165, 250, 0.3),
                stop:1 rgba(59, 130, 246, 0.3));
            border: 1px solid rgba(96, 165, 250, 0.5);
            color: #ffffff;
        }
        
        QTextEdit#activityLog {
            background: rgba(15, 23, 42, 0.7);
            border: 2px solid rgba(100, 116, 139, 0.2);
            border-radius: 12px;
            padding: 12px;
            color: #cbd5e1;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 22px;
            line-height: 1.6;
        }
        
        QPushButton#actionBtn {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(96, 165, 250, 0.3),
                stop:1 rgba(59, 130, 246, 0.2));
            border: 2px solid rgba(96, 165, 250, 0.4);
            border-radius: 10px;
            padding: 12px 20px;
            color: #93c5fd;
            font-weight: bold;
            font-size: 26px;
        }
        
        QPushButton#actionBtn:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(96, 165, 250, 0.5),
                stop:1 rgba(59, 130, 246, 0.4));
            border: 2px solid rgba(96, 165, 250, 0.6);
            color: #dbeafe;
        }
        
        QPushButton#actionBtn:pressed {
            background: rgba(59, 130, 246, 0.6);
        }
        
        QPushButton#deleteBtn {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(239, 68, 68, 0.3),
                stop:1 rgba(220, 38, 38, 0.2));
            border: 2px solid rgba(239, 68, 68, 0.4);
            border-radius: 10px;
            padding: 12px 20px;
            color: #fca5a5;
            font-weight: bold;
            font-size: 26px;
        }
        
        QPushButton#deleteBtn:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(239, 68, 68, 0.5),
                stop:1 rgba(220, 38, 38, 0.4));
            border: 2px solid rgba(239, 68, 68, 0.6);
            color: #fee2e2;
        }
        
        QPushButton#deleteBtn:pressed {
            background: rgba(220, 38, 38, 0.6);
        }
        
        QScrollBar:vertical {
            background: rgba(15, 23, 42, 0.4);
            width: 12px;
            border-radius: 6px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(100, 116, 139, 0.5),
                stop:1 rgba(71, 85, 105, 0.5));
            border-radius: 6px;
            min-height: 30px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        
        QScrollBar::handle:vertical:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(148, 163, 184, 0.7),
                stop:1 rgba(100, 116, 139, 0.7));
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """


def get_dialog_stylesheet() -> str:
    """Get stylesheet for dialogs"""
    return """
        QDialog {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(30, 41, 59, 0.98),
                stop:1 rgba(51, 65, 85, 0.98));
            border-radius: 18px;
            border: 2px solid rgba(148, 163, 184, 0.3);
        }
        
        QLabel#dialogTitle {
            color: #f1f5f9;
            font-size: 30px;
            font-weight: bold;
        }
        
        QLabel#fieldLabel {
            color: #cbd5e1;
            font-size: 24px;
            font-weight: bold;
        }
        
        QFrame#separator {
            background: rgba(148, 163, 184, 0.2);
            max-height: 1px;
        }
        
        QLineEdit#inputField {
            background: rgba(15, 23, 42, 0.6);
            border: 2px solid rgba(100, 116, 139, 0.4);
            border-radius: 10px;
            padding: 12px 16px;
            color: #f1f5f9;
            font-size: 26px;
            selection-background-color: rgba(96, 165, 250, 0.4);
        }
        
        QLineEdit#inputField:focus {
            border: 2px solid rgba(96, 165, 250, 0.7);
            background: rgba(15, 23, 42, 0.8);
        }
        
        QDialogButtonBox QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(96, 165, 250, 0.3),
                stop:1 rgba(59, 130, 246, 0.2));
            border: 2px solid rgba(96, 165, 250, 0.4);
            border-radius: 10px;
            padding: 10px 24px;
            color: #93c5fd;
            font-weight: bold;
            font-size: 26px;
            min-width: 100px;
        }
        
        QDialogButtonBox QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(96, 165, 250, 0.5),
                stop:1 rgba(59, 130, 246, 0.4));
            border: 2px solid rgba(96, 165, 250, 0.6);
            color: #dbeafe;
        }
        
        QDialogButtonBox QPushButton:pressed {
            background: rgba(59, 130, 246, 0.6);
        }
    """
