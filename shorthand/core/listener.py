"""Keyboard listener for shorthand expansion"""
import time
import pyperclip
from PyQt5.QtCore import QThread, pyqtSignal
from pynput import keyboard
from pynput.keyboard import Key, Controller


class KeyboardListenerThread(QThread):
    """Background thread for keyboard listening"""
    expansion_signal = pyqtSignal(str, str)
    status_signal = pyqtSignal(str)
    pause_signal = pyqtSignal(bool)
    
    def __init__(self, expander):
        super().__init__()
        self.expander = expander
        self.running = True
        self.paused = False
        self.listener = None
        self.kbd = Controller()
        self.current_word = []
        self.is_expanding = False
        self.suppress_next_chars = 0
        self.ctrl_pressed = False
        self.last_expansion_time = 0
    
    def run(self):
        """Start keyboard listener"""
        try:
            with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release,
                suppress=False
            ) as self.listener:
                self.listener.join()
        except Exception as e:
            self.status_signal.emit(f"Error: {e}")
    
    def on_press(self, key):
        """Handle key press events"""
        try:
            if key == Key.pause:
                self.paused = not self.paused
                self.pause_signal.emit(self.paused)
                if self.paused:
                    self.current_word = []
                return
            
            if self.paused:
                return
            
            if key == Key.ctrl_l or key == Key.ctrl_r:
                self.ctrl_pressed = True
                return
            
            # Suppress input during and shortly after expansion
            if self.is_expanding:
                return
            
            current_time = time.time()
            if current_time - self.last_expansion_time < 0.3:
                return
            
            if key == Key.backspace:
                if self.current_word:
                    self.current_word.pop()
                return
            
            if key == Key.delete:
                self.current_word = []
                return
            
            if key == Key.space:
                if self.current_word:
                    word = ''.join(self.current_word)
                    match_result = self.find_matching_shorthand(word)
                    if match_result:
                        self.expand_shorthand_with_prefix(word, match_result)
                        return
                self.current_word = []
                return
            
            if hasattr(key, 'char') and key.char:
                char = key.char
                if char.isalnum():
                    self.current_word.append(char.lower())
                else:
                    if self.current_word:
                        word = ''.join(self.current_word)
                        match_result = self.find_matching_shorthand(word)
                        if match_result:
                            self.expand_shorthand_with_prefix(word, match_result)
                            return
                    self.current_word = []
            elif key in [Key.enter, Key.tab, Key.home, Key.end, Key.up, Key.down, Key.left, Key.right]:
                self.current_word = []
        
        except Exception:
            self.current_word = []
    
    def find_matching_shorthand(self, word):
        """Find matching shorthand by checking suffixes"""
        # First check exact match
        if self.expander.exists(word):
            return (word, '', self.expander.get(word))
        
        # Check suffixes from longest to shortest
        for i in range(1, len(word)):
            suffix = word[i:]
            if self.expander.exists(suffix):
                prefix = word[:i]
                expansion = self.expander.get(suffix)
                return (suffix, prefix, expansion)
        
        return None
    
    def expand_shorthand_with_prefix(self, typed_word, match_result):
        """Expand shorthand with prefix handling"""
        shorthand, prefix, expansion = match_result
        
        # Full expansion includes prefix
        full_expansion = prefix + expansion
        
        self.expansion_signal.emit(typed_word, full_expansion)
        
        self.is_expanding = True
        self.current_word = []
        
        time.sleep(0.05)
        
        # Delete the typed word + trigger character
        chars_to_delete = len(typed_word) + 1
        for _ in range(chars_to_delete):
            self.kbd.press(Key.backspace)
            self.kbd.release(Key.backspace)
            time.sleep(0.005)
        
        # Always use clipboard for pasting (faster and more reliable)
        try:
            old_clipboard = pyperclip.paste()
        except:
            old_clipboard = ""
        
        pyperclip.copy(full_expansion + ' ')
        
        time.sleep(0.03)
        
        # Paste using Ctrl+V
        self.kbd.press(Key.ctrl)
        time.sleep(0.01)
        self.kbd.press('v')
        time.sleep(0.01)
        self.kbd.release('v')
        time.sleep(0.01)
        self.kbd.release(Key.ctrl)
        
        time.sleep(0.15)
        
        # Restore old clipboard
        try:
            pyperclip.copy(old_clipboard)
        except:
            pass
        
        self.last_expansion_time = time.time()
        self.is_expanding = False
    
    def on_release(self, key):
        """Handle key release events"""
        if key == Key.ctrl_l or key == Key.ctrl_r:
            self.ctrl_pressed = False
    
    def expand_shorthand(self, shorthand: str):
        """Replace typed shorthand with expansion"""
        expansion = self.expander.get(shorthand)
        self.expansion_signal.emit(shorthand, expansion)
        
        self.is_expanding = True
        self.current_word = []
        
        time.sleep(0.05)
        
        # Delete the typed shorthand + trigger character
        chars_to_delete = len(shorthand) + 1
        for _ in range(chars_to_delete):
            self.kbd.press(Key.backspace)
            self.kbd.release(Key.backspace)
            time.sleep(0.005)
        
        # Always use clipboard for pasting (faster and more reliable)
        try:
            old_clipboard = pyperclip.paste()
        except:
            old_clipboard = ""
        
        pyperclip.copy(expansion + ' ')
        
        time.sleep(0.03)
        
        # Paste using Ctrl+V
        self.kbd.press(Key.ctrl)
        time.sleep(0.01)
        self.kbd.press('v')
        time.sleep(0.01)
        self.kbd.release('v')
        time.sleep(0.01)
        self.kbd.release(Key.ctrl)
        
        time.sleep(0.15)
        
        # Restore old clipboard
        try:
            pyperclip.copy(old_clipboard)
        except:
            pass
        
        self.last_expansion_time = time.time()
        self.is_expanding = False
    
    def stop(self):
        """Stop the listener"""
        self.running = False
        if self.listener:
            self.listener.stop()
