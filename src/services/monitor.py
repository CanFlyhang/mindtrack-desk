import time
import win32gui
from PySide6.QtCore import QThread, Signal

class WindowWatcher(QThread):
    """
    Background thread to monitor active window changes.
    Emits signal only when the window has been active/stable for a certain duration.
    """
    window_changed = Signal(int, str)  # hwnd, title

    def __init__(self, debounce_seconds=1.5):
        super().__init__()
        self.running = False
        self.debounce_seconds = debounce_seconds
        self.last_reported_hwnd = 0
        self.pending_hwnd = 0
        self.pending_start_time = 0

    def run(self):
        self.running = True
        while self.running:
            try:
                current_hwnd = win32gui.GetForegroundWindow()
                
                # If current window is different from what we last reported
                if current_hwnd != self.last_reported_hwnd:
                    # If it's also different from what we are currently pending/watching
                    if current_hwnd != self.pending_hwnd:
                        # Start watching this new window
                        self.pending_hwnd = current_hwnd
                        self.pending_start_time = time.time()
                    else:
                        # We are already watching this window, check if it has been stable enough
                        if time.time() - self.pending_start_time >= self.debounce_seconds:
                            # Stable! Report it.
                            title = win32gui.GetWindowText(current_hwnd)
                            # Filter out empty titles or Program Manager (desktop)
                            if title and title != "Program Manager": 
                                self.last_reported_hwnd = current_hwnd
                                self.window_changed.emit(current_hwnd, title)
                else:
                    # We are back to the reported window, reset pending
                    self.pending_hwnd = 0
            
            except Exception as e:
                print(f"Error in WindowWatcher: {e}")

            time.sleep(0.2)

    def stop(self):
        self.running = False
        self.wait()
