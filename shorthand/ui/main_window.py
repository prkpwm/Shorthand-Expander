"""Main window for shorthand expander GUI"""
import os
import time
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTextEdit, QListWidget, 
                             QListWidgetItem, QLineEdit, QFrame, QSizeGrip, QMessageBox)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont, QIcon

from ..core import ShorthandExpander, KeyboardListenerThread
from .dialog import ShorthandDialog
from .styles import get_stylesheet


class ShorthandExpanderGUI(QMainWindow):
    """Main GUI window"""
    
    def __init__(self):
        super().__init__()
        self.expander = ShorthandExpander()
        self.listener_thread = None
        self.expansion_count = 0
        self.is_fullscreen = False
        self.normal_geometry = None
        self.settings = QSettings('ShorthandExpander', 'WindowSettings')
        self.resize_edge = None
        
        self.init_ui()
        self.restore_window_state()
        self.load_shorthands()
        self.start_listener()
        
        # Start fullscreen on first launch
        if not self.settings.value('has_launched_before', False):
            self.settings.setValue('has_launched_before', True)
            self.toggle_fullscreen()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Shorthand Expander")
        self.setGeometry(100, 100, 1200, 700)
        self.setMinimumSize(800, 500)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        main_widget = QWidget()
        main_widget.setObjectName("mainWidget")
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left sidebar
        main_layout.addWidget(self.create_sidebar())
        
        # Right content area
        right_widget = QWidget()
        right_widget.setObjectName("rightContent")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(15)
        
        right_layout.addWidget(self.create_title_bar())
        
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        content_layout.addWidget(self.create_shorthand_list(), 3)
        content_layout.addWidget(self.create_activity_log(), 2)
        right_layout.addLayout(content_layout)
        
        self.size_grip = QSizeGrip(right_widget)
        self.size_grip.setFixedSize(20, 20)
        self.size_grip.setStyleSheet("QSizeGrip { background: transparent; }")
        
        grip_layout = QHBoxLayout()
        grip_layout.addStretch()
        grip_layout.addWidget(self.size_grip)
        right_layout.addLayout(grip_layout)
        
        main_layout.addWidget(right_widget)
        
        self.setStyleSheet(get_stylesheet())
    
    def create_sidebar(self) -> QFrame:
        """Create left sidebar with stats and controls"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # App title
        app_title = QLabel("✨ Shorthand\nExpander")
        app_title.setObjectName("appTitle")
        app_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(app_title)
        
        # Separator
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        sep1.setObjectName("separator")
        layout.addWidget(sep1)
        
        # Stats section
        stats_label = QLabel("📊 Statistics")
        stats_label.setObjectName("sidebarHeader")
        layout.addWidget(stats_label)
        
        # Total shorthands stat
        total_container = QFrame()
        total_container.setObjectName("statCard")
        total_layout = QVBoxLayout(total_container)
        total_layout.setContentsMargins(15, 15, 15, 15)
        
        self.total_label = QLabel("0")
        self.total_label.setObjectName("statNumber")
        self.total_label.setAlignment(Qt.AlignCenter)
        
        total_text = QLabel("Total Shorthands")
        total_text.setObjectName("statLabel")
        total_text.setAlignment(Qt.AlignCenter)
        
        total_layout.addWidget(self.total_label)
        total_layout.addWidget(total_text)
        layout.addWidget(total_container)
        
        # Expansions stat
        exp_container = QFrame()
        exp_container.setObjectName("statCard")
        exp_layout = QVBoxLayout(exp_container)
        exp_layout.setContentsMargins(15, 15, 15, 15)
        
        self.expanded_label = QLabel("0")
        self.expanded_label.setObjectName("statNumber")
        self.expanded_label.setAlignment(Qt.AlignCenter)
        
        expanded_text = QLabel("Expansions")
        expanded_text.setObjectName("statLabel")
        expanded_text.setAlignment(Qt.AlignCenter)
        
        exp_layout.addWidget(self.expanded_label)
        exp_layout.addWidget(expanded_text)
        layout.addWidget(exp_container)
        
        # Separator
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setObjectName("separator")
        layout.addWidget(sep2)
        
        # Status section
        status_label = QLabel("⚙️ Status")
        status_label.setObjectName("sidebarHeader")
        layout.addWidget(status_label)
        
        self.status_label = QLabel("● Active")
        self.status_label.setObjectName("statusActive")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        return sidebar
    
    def create_title_bar(self) -> QFrame:
        """Create title bar with controls"""
        frame = QFrame()
        frame.setObjectName("titleBar")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(15, 10, 15, 10)
        
        title = QLabel("Shorthand Expander")
        title.setObjectName("title")
        layout.addWidget(title)
        layout.addStretch()
        
        fullscreen_btn = QPushButton("⛶")
        fullscreen_btn.setObjectName("controlBtn")
        fullscreen_btn.setToolTip("Fullscreen (F11)")
        fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        fullscreen_btn.setFixedSize(35, 35)
        layout.addWidget(fullscreen_btn)
        
        minimize_btn = QPushButton("−")
        minimize_btn.setObjectName("controlBtn")
        minimize_btn.clicked.connect(self.showMinimized)
        minimize_btn.setFixedSize(35, 35)
        layout.addWidget(minimize_btn)
        
        close_btn = QPushButton("×")
        close_btn.setObjectName("closeBtn")
        close_btn.clicked.connect(self.close)
        close_btn.setFixedSize(35, 35)
        layout.addWidget(close_btn)
        
        return frame
    
    def create_shorthand_list(self) -> QFrame:
        """Create shorthand list panel"""
        frame = QFrame()
        frame.setObjectName("glassPanel")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("📚 Loaded Shorthands")
        header.setObjectName("panelHeader")
        layout.addWidget(header)
        
        search_box = QLineEdit()
        search_box.setObjectName("searchBox")
        search_box.setPlaceholderText("🔍 Search shorthands...")
        search_box.textChanged.connect(self.filter_shorthands)
        layout.addWidget(search_box)
        
        self.shorthand_list = QListWidget()
        self.shorthand_list.setObjectName("shorthandList")
        self.shorthand_list.itemDoubleClicked.connect(self.edit_shorthand)
        layout.addWidget(self.shorthand_list)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        add_btn = QPushButton("➕ Add")
        add_btn.setObjectName("actionBtn")
        add_btn.clicked.connect(self.add_shorthand)
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setObjectName("actionBtn")
        edit_btn.clicked.connect(self.edit_selected_shorthand)
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setObjectName("deleteBtn")
        delete_btn.clicked.connect(self.delete_shorthand)
        btn_layout.addWidget(delete_btn)
        
        layout.addLayout(btn_layout)
        return frame
    
    def create_activity_log(self) -> QFrame:
        """Create activity log panel"""
        frame = QFrame()
        frame.setObjectName("glassPanel")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("⚡ Activity Log")
        header.setObjectName("panelHeader")
        layout.addWidget(header)
        
        self.activity_log = QTextEdit()
        self.activity_log.setObjectName("activityLog")
        self.activity_log.setReadOnly(True)
        layout.addWidget(self.activity_log)
        
        clear_btn = QPushButton("Clear Log")
        clear_btn.setObjectName("actionBtn")
        clear_btn.clicked.connect(self.activity_log.clear)
        layout.addWidget(clear_btn)
        
        return frame
    
    def load_shorthands(self):
        """Load shorthands from file"""
        if self.expander.load_from_file():
            print(f"Loaded from: {self.expander.loaded_file_path}")
            print(f"Total shorthands: {self.expander.count()}")
            self.total_label.setText(str(self.expander.count()))
            self.populate_shorthand_list()
            self.log_activity(f"✅ Loaded {self.expander.count()} shorthands")
        else:
            self.log_activity("⚠️ shorthand/shorthands.txt not found")
    
    def populate_shorthand_list(self):
        """Populate the shorthand list widget"""
        self.shorthand_list.clear()
        for shorthand, expansion in sorted(self.expander.items()):
            item_text = f"{shorthand}  →  {expansion}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, (shorthand, expansion))
            self.shorthand_list.addItem(item)
    
    def filter_shorthands(self, text: str):
        """Filter shorthand list by search text"""
        for i in range(self.shorthand_list.count()):
            item = self.shorthand_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())
    
    def add_shorthand(self):
        """Add new shorthand"""
        dialog = ShorthandDialog(self)
        if dialog.exec_() == ShorthandDialog.Accepted:
            shorthand, expansion = dialog.get_values()
            if shorthand and expansion:
                if self.expander.add(shorthand, expansion):
                    save_result = self.expander.save_to_file()
                    print(f"Save result: {save_result}")
                    print(f"Saved to: {self.expander.loaded_file_path}")
                    self.populate_shorthand_list()
                    self.total_label.setText(str(self.expander.count()))
                    self.log_activity(f"➕ Added: {shorthand} → {expansion}")
                else:
                    QMessageBox.warning(self, "Duplicate", f"Shorthand '{shorthand}' already exists!")
    
    def edit_selected_shorthand(self):
        """Edit selected shorthand"""
        current_item = self.shorthand_list.currentItem()
        if current_item:
            self.edit_shorthand(current_item)
    
    def edit_shorthand(self, item: QListWidgetItem):
        """Edit a shorthand"""
        data = item.data(Qt.UserRole)
        if not data:
            return
        old_shorthand, old_expansion = data
        
        dialog = ShorthandDialog(self, old_shorthand, old_expansion)
        if dialog.exec_() == ShorthandDialog.Accepted:
            new_shorthand, new_expansion = dialog.get_values()
            if new_shorthand and new_expansion:
                if self.expander.update(old_shorthand, new_shorthand, new_expansion):
                    self.expander.save_to_file()
                    self.populate_shorthand_list()
                    self.log_activity(f"✏️ Edited: {old_shorthand} → {new_shorthand}")
                else:
                    QMessageBox.warning(self, "Error", f"Shorthand '{new_shorthand}' already exists!")
    
    def delete_shorthand(self):
        """Delete selected shorthand"""
        current_item = self.shorthand_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a shorthand to delete!")
            return
        
        data = current_item.data(Qt.UserRole)
        if not data:
            return
        shorthand, _ = data
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete shorthand '{shorthand}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.expander.delete(shorthand)
            self.expander.save_to_file()
            self.populate_shorthand_list()
            self.total_label.setText(str(self.expander.count()))
            self.log_activity(f"🗑️ Deleted: {shorthand}")
    
    def start_listener(self):
        """Start keyboard listener thread"""
        self.listener_thread = KeyboardListenerThread(self.expander)
        self.listener_thread.expansion_signal.connect(self.on_expansion)
        self.listener_thread.status_signal.connect(self.log_activity)
        self.listener_thread.pause_signal.connect(self.on_pause_toggle)
        self.listener_thread.start()
    
    def on_expansion(self, shorthand: str, expansion: str):
        """Handle expansion event"""
        self.expansion_count += 1
        self.expanded_label.setText(str(self.expansion_count))
        self.log_activity(f"🚀 {shorthand} → {expansion}")
    
    def on_pause_toggle(self, paused: bool):
        """Handle pause toggle"""
        if paused:
            self.status_label.setText("⏸ Paused")
            self.status_label.setObjectName("statusPaused")
            self.log_activity("⏸ Paused (Press Pause key to resume)")
        else:
            self.status_label.setText("● Active")
            self.status_label.setObjectName("statusActive")
            self.log_activity("▶ Resumed")
        self.setStyleSheet(get_stylesheet())
    
    def log_activity(self, message: str):
        """Log activity message"""
        timestamp = time.strftime("%H:%M:%S")
        self.activity_log.append(f"[{timestamp}] {message}")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.is_fullscreen:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            if self.normal_geometry:
                self.setGeometry(self.normal_geometry)
            self.show()
            self.is_fullscreen = False
            self.log_activity("🪟 Exited fullscreen")
        else:
            self.normal_geometry = self.geometry()
            self.setWindowFlags(Qt.Window)
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.showFullScreen()
            self.is_fullscreen = True
            self.log_activity("🖥️ Entered fullscreen (Press F11 to exit)")
    
    def save_window_state(self):
        """Save window position and size"""
        if not self.is_fullscreen:
            self.settings.setValue('geometry', self.geometry())
    
    def restore_window_state(self):
        """Restore window position and size"""
        geometry = self.settings.value('geometry')
        if geometry:
            self.setGeometry(geometry)
    
    def closeEvent(self, event):
        """Handle window close"""
        self.save_window_state()
        if self.listener_thread:
            self.listener_thread.stop()
            self.listener_thread.wait()
        event.accept()
    
    def keyPressEvent(self, event):
        """Handle key press"""
        if event.key() == Qt.Key_F11:
            self.toggle_fullscreen()
        else:
            super().keyPressEvent(event)
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging/resizing"""
        if self.is_fullscreen:
            return
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.resize_edge = self.get_resize_edge(event.pos())
            if self.resize_edge:
                self.resize_start_pos = event.globalPos()
                self.resize_start_geometry = self.geometry()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging/resizing"""
        if self.is_fullscreen:
            self.setCursor(Qt.ArrowCursor)
            return
        if event.buttons() == Qt.LeftButton:
            if self.resize_edge and hasattr(self, 'resize_start_pos'):
                self.handle_resize(event.globalPos())
            elif hasattr(self, 'drag_position') and not self.resize_edge:
                self.move(event.globalPos() - self.drag_position)
            event.accept()
        else:
            edge = self.get_resize_edge(event.pos())
            if edge:
                if edge in ['top', 'bottom']:
                    self.setCursor(Qt.SizeVerCursor)
                elif edge in ['left', 'right']:
                    self.setCursor(Qt.SizeHorCursor)
                elif edge in ['top-left', 'bottom-right']:
                    self.setCursor(Qt.SizeFDiagCursor)
                elif edge in ['top-right', 'bottom-left']:
                    self.setCursor(Qt.SizeBDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if self.is_fullscreen:
            return
        self.resize_edge = None
        self.setCursor(Qt.ArrowCursor)
    
    def get_resize_edge(self, pos):
        """Determine which edge is being resized"""
        margin = 10
        rect = self.rect()
        
        left = pos.x() < margin
        right = pos.x() > rect.width() - margin
        top = pos.y() < margin
        bottom = pos.y() > rect.height() - margin
        
        if top and left:
            return 'top-left'
        elif top and right:
            return 'top-right'
        elif bottom and left:
            return 'bottom-left'
        elif bottom and right:
            return 'bottom-right'
        elif top:
            return 'top'
        elif bottom:
            return 'bottom'
        elif left:
            return 'left'
        elif right:
            return 'right'
        return None
    
    def handle_resize(self, global_pos):
        """Handle window resize"""
        delta = global_pos - self.resize_start_pos
        geo = self.resize_start_geometry
        new_geo = geo
        
        if 'left' in self.resize_edge:
            new_geo.setLeft(geo.left() + delta.x())
        if 'right' in self.resize_edge:
            new_geo.setRight(geo.right() + delta.x())
        if 'top' in self.resize_edge:
            new_geo.setTop(geo.top() + delta.y())
        if 'bottom' in self.resize_edge:
            new_geo.setBottom(geo.bottom() + delta.y())
        
        if new_geo.width() >= self.minimumWidth() and new_geo.height() >= self.minimumHeight():
            self.setGeometry(new_geo)
