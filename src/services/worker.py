from PySide6.QtCore import QThread, Signal

class AnalysisWorker(QThread):
    finished = Signal(str, str) # summary, image_path

    def __init__(self, hwnd, title, capture_service, ai_service, storage_service):
        super().__init__()
        self.hwnd = hwnd
        self.title = title
        self.capture = capture_service
        self.ai = ai_service
        self.storage = storage_service

    def run(self):
        try:
            # Capture
            img = self.capture.capture_active_window(self.hwnd)
            img_path = self.capture.save_image(img)
            b64 = self.capture.to_base64(img)
            
            # AI
            summary = self.ai.analyze_image(b64)
            
            # Save
            self.storage.add_record(self.title, summary, img_path)
            
            self.finished.emit(summary, img_path)
        except Exception as e:
            print(f"Worker Error: {e}")
            self.finished.emit(f"Error: {e}", "")
