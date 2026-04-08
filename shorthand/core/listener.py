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
            if self._handle_pause(key):
                return
            if self.paused or self.is_expanding:
                return
            if self._is_ctrl(key):
                return
            if time.time() - self.last_expansion_time < 0.1:
                return
            self._handle_key(key)
        except Exception:
            self.current_word = []

    def _handle_pause(self, key) -> bool:
        if key != Key.pause:
            return False
        self.paused = not self.paused
        self.pause_signal.emit(self.paused)
        if self.paused:
            self.current_word = []
        return True

    def _is_ctrl(self, key) -> bool:
        if key in (Key.ctrl_l, Key.ctrl_r):
            self.ctrl_pressed = True
            return True
        return False

    def _handle_key(self, key):
        if key == Key.backspace:
            if self.current_word:
                self.current_word.pop()
        elif key == Key.delete:
            self.current_word = []
        elif key == Key.space:
            self._try_expand()
            self.current_word = []
        elif key in (Key.enter, Key.tab, Key.home, Key.end,
                     Key.up, Key.down, Key.left, Key.right):
            self.current_word = []
        elif hasattr(key, 'char') and key.char:
            if key.char.isalnum():
                self.current_word.append(key.char.lower())
            else:
                self.current_word = []

    def _try_expand(self):
        if not self.current_word:
            return
        word = ''.join(self.current_word)
        match = self.find_matching_shorthand(word)
        if match:
            self.current_word = []
            self._do_expand(word, match)

    def find_matching_shorthand(self, word):
        """Find matching shorthand - exact match only"""
        if self.expander.exists(word):
            return (word, '', self.expander.get(word))
        return None

    def _do_expand(self, typed_word, match_result):
        """Perform the expansion using clipboard paste"""
        _, prefix, expansion = match_result
        full_expansion = prefix + expansion

        self.expansion_signal.emit(typed_word, full_expansion)
        self.is_expanding = True

        # Delete typed word + space
        for _ in range(len(typed_word) + 1):
            self.kbd.tap(Key.backspace)

        # Save, set, paste, restore clipboard
        try:
            old_clipboard = pyperclip.paste()
        except Exception:
            old_clipboard = ""

        pyperclip.copy(full_expansion + ' ')
        time.sleep(0.02)

        with self.kbd.pressed(Key.ctrl):
            self.kbd.tap('v')

        time.sleep(0.08)

        try:
            pyperclip.copy(old_clipboard)
        except Exception:
            pass

        self.last_expansion_time = time.time()
        self.is_expanding = False

    def on_release(self, key):
        """Handle key release events"""
        if key in (Key.ctrl_l, Key.ctrl_r):
            self.ctrl_pressed = False

    def stop(self):
        """Stop the listener"""
        self.running = False
        if self.listener:
            self.listener.stop()
