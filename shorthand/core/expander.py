"""Shorthand expansion logic"""
import os
import sys
from typing import Dict


class ShorthandExpander:
    """Manages shorthand dictionary and file operations"""
    
    def __init__(self):
        self.shorthands: Dict[str, str] = {}
        self.max_length = 0
        self.loaded_file_path = None
    
    def _get_data_dir(self):
        """Get the directory for storing user data"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            # Save to user's AppData folder
            app_data = os.path.join(os.environ.get('APPDATA', ''), 'ShorthandExpander')
            os.makedirs(app_data, exist_ok=True)
            return app_data
        else:
            # Running from source
            return os.path.join(os.path.dirname(__file__), '..')
    
    def _get_bundled_file(self, filename):
        """Get path to bundled file in PyInstaller"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = sys._MEIPASS
            return os.path.join(base_path, 'shorthand', filename)
        else:
            return None
    
    def load_from_file(self, filename: str = "shorthands.txt") -> bool:
        """Load shorthands from file"""
        self.shorthands = {}
        self.max_length = 0
        
        # Try user data directory first (for saved changes)
        data_dir = self._get_data_dir()
        user_file = os.path.join(data_dir, filename)
        
        # Try bundled file (for initial load)
        bundled_file = self._get_bundled_file(filename)
        
        possible_paths = [
            user_file,  # User's saved file (highest priority)
            bundled_file,  # Bundled with exe
            filename,
            os.path.join(os.path.dirname(__file__), '..', filename),
            os.path.join(os.path.dirname(__file__), '..', '..', filename),
        ]
        
        file_path = None
        for path in possible_paths:
            if path and os.path.exists(path):
                file_path = os.path.abspath(path)
                break
        
        if not file_path:
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split('\t') if '\t' in line else line.split()
                    if len(parts) >= 2:
                        shorthand = parts[0].strip()
                        expansion = ' '.join(parts[1:]).strip()
                        self.shorthands[shorthand] = expansion
                        self.max_length = max(self.max_length, len(shorthand))
            
            # Always save to user data directory
            self.loaded_file_path = os.path.join(data_dir, filename)
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def save_to_file(self, filename: str = None) -> bool:
        """Save shorthands to file"""
        if filename is None:
            if self.loaded_file_path:
                filename = self.loaded_file_path
            else:
                data_dir = self._get_data_dir()
                filename = os.path.join(data_dir, 'shorthands.txt')
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# Shorthand Expander Dictionary\n")
                f.write("# Format: shorthand[TAB]expansion\n\n")
                for shorthand, expansion in sorted(self.shorthands.items()):
                    f.write(f"{shorthand}\t{expansion}\n")
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def add(self, shorthand: str, expansion: str) -> bool:
        """Add a new shorthand"""
        if shorthand in self.shorthands:
            return False
        self.shorthands[shorthand] = expansion
        self.max_length = max(self.max_length, len(shorthand))
        return True
    
    def update(self, old_shorthand: str, new_shorthand: str, new_expansion: str) -> bool:
        """Update an existing shorthand"""
        if old_shorthand not in self.shorthands:
            return False
        if new_shorthand != old_shorthand and new_shorthand in self.shorthands:
            return False
        
        del self.shorthands[old_shorthand]
        self.shorthands[new_shorthand] = new_expansion
        self.max_length = max((len(s) for s in self.shorthands.keys()), default=0)
        return True
    
    def delete(self, shorthand: str) -> bool:
        """Delete a shorthand"""
        if shorthand not in self.shorthands:
            return False
        del self.shorthands[shorthand]
        self.max_length = max((len(s) for s in self.shorthands.keys()), default=0)
        return True
    
    def get(self, shorthand: str) -> str:
        """Get expansion for a shorthand"""
        return self.shorthands.get(shorthand, '')
    
    def exists(self, shorthand: str) -> bool:
        """Check if shorthand exists"""
        return shorthand in self.shorthands
    
    def count(self) -> int:
        """Get total number of shorthands"""
        return len(self.shorthands)
    
    def items(self):
        """Get all shorthand items"""
        return self.shorthands.items()
