import mss
import mss.tools
import base64
from io import BytesIO
from PIL import Image
import win32gui
import datetime
import os

class ScreenCapture:
    def __init__(self, save_dir="logs/images"):
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def capture_active_window(self, hwnd):
        """
        Captures the area of the active window or full screen if fails.
        Returns PIL Image.
        """
        try:
            rect = win32gui.GetWindowRect(hwnd)
            x, y, x2, y2 = rect
            w = x2 - x
            h = y2 - y
            
            if w <= 0 or h <= 0:
                return self.capture_full_screen()

            with mss.mss() as sct:
                monitor = {"top": y, "left": x, "width": w, "height": h}
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                return img
        except Exception as e:
            print(f"Window capture failed, falling back to full screen: {e}")
            return self.capture_full_screen()

    def capture_full_screen(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1] # Primary monitor
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            return img

    def save_image(self, img, prefix="cap"):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.jpg"
        path = os.path.join(self.save_dir, filename)
        img.save(path, "JPEG")
        return path

    def to_base64(self, img):
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=70) # Compress slightly for API
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
