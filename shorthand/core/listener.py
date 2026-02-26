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
            
            if self.is_expanding or self.suppress_next_chars > 0:
                if self.suppress_next_chars > 0:
                    self.suppress_next_chars -= 1
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
                    if self.expander.exists(word):
                        self.expand_shorthand(word)
                self.current_word = []
                return
            
            if hasattr(key, 'char') and key.char:
                char = key.char
                if char.isalnum():
                    self.current_word.append(char.lower())
                else:
                    self.current_word = []
            elif key in [Key.enter, Key.tab, Key.home, Key.end, Key.up, Key.down, Key.left, Key.right]:
                self.current_word = []
        
        except Exception:
            self.current_word = []
    
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
        self.suppress_next_chars = 3
        
        time.sleep(0.05)
        
        chars_to_delete = len(shorthand) + 1
        for _ in range(chars_to_delete):
            self.kbd.press(Key.backspace)
            self.kbd.release(Key.backspace)
            time.sleep(0.005)
        
        if any(ord(char) > 127 for char in expansion):
            old_clipboard = pyperclip.paste()
            pyperclip.copy(expansion + ' ')
            self.kbd.press(Key.ctrl)
            self.kbd.press('v')
            self.kbd.release('v')
            self.kbd.release(Key.ctrl)
            time.sleep(0.1)
            pyperclip.copy(old_clipboard)
        else:
            for char in expansion:
                self.kbd.press(char)
                self.kbd.release(char)
                time.sleep(0.005)
            self.kbd.press(Key.space)
            self.kbd.release(Key.space)
        
        time.sleep(0.05)
        self.is_expanding = False
        self.suppress_next_chars = 0
    
    def stop(self):
        """Stop the listener"""
        self.running = False
        if self.listener:
            self.listener.stop()
