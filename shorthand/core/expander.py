"""Shorthand expansion logic"""
import os
from typing import Dict


class ShorthandExpander:
    """Manages shorthand dictionary and file operations"""
    
    def __init__(self):
        self.shorthands: Dict[str, str] = {}
        self.max_length = 0
    
    def load_from_file(self, filename: str = "shorthands.txt") -> bool:
        """Load shorthands from file"""
        self.shorthands = {}
        self.max_length = 0
        
        possible_paths = [
            filename,
            os.path.join(os.path.dirname(__file__), '..', filename),
            os.path.join(os.path.dirname(__file__), '..', '..', filename),
        ]
        
        file_path = None
        for path in possible_paths:
            if os.path.exists(path):
                file_path = path
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
            
            return True
        except Exception:
            return False
    
    def save_to_file(self, filename: str = None) -> bool:
        """Save shorthands to file"""
        if filename is None:
            filename = os.path.join(os.path.dirname(__file__), '..', 'shorthands.txt')
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# Shorthand Expander Dictionary\n")
                f.write("# Format: shorthand[TAB]expansion\n\n")
                for shorthand, expansion in sorted(self.shorthands.items()):
                    f.write(f"{shorthand}\t{expansion}\n")
            return True
        except Exception:
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
