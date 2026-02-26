"""Dialog for adding/editing shorthands"""
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QFrame
from PyQt5.QtCore import Qt
from .styles import get_dialog_stylesheet


class ShorthandDialog(QDialog):
    """Dialog for adding/editing shorthands"""
    
    def __init__(self, parent=None, shorthand: str = "", expansion: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Add Shorthand" if not shorthand else "Edit Shorthand")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(300)
        self._init_ui(shorthand, expansion)
    
    def _init_ui(self, shorthand: str, expansion: str):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("✏️ " + ("Add New Shorthand" if not shorthand else "Edit Shorthand"))
        title.setObjectName("dialogTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setObjectName("separator")
        layout.addWidget(separator)
        
        # Shorthand field
        shorthand_label = QLabel("Shorthand:")
        shorthand_label.setObjectName("fieldLabel")
        layout.addWidget(shorthand_label)
        
        self.shorthand_input = QLineEdit()
        self.shorthand_input.setText(shorthand)
        self.shorthand_input.setPlaceholderText("e.g., abt, impl, cfg")
        self.shorthand_input.setObjectName("inputField")
        layout.addWidget(self.shorthand_input)
        
        layout.addSpacing(10)
        
        # Expansion field
        expansion_label = QLabel("Expansion:")
        expansion_label.setObjectName("fieldLabel")
        layout.addWidget(expansion_label)
        
        self.expansion_input = QLineEdit()
        self.expansion_input.setText(expansion)
        self.expansion_input.setPlaceholderText("e.g., about, implements, configure")
        self.expansion_input.setObjectName("inputField")
        layout.addWidget(self.expansion_input)
        
        layout.addStretch()
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setObjectName("buttonBox")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setStyleSheet(get_dialog_stylesheet())
        self.shorthand_input.setFocus()
    
    def get_values(self) -> tuple:
        """Get shorthand and expansion values"""
        return self.shorthand_input.text().strip(), self.expansion_input.text().strip()
