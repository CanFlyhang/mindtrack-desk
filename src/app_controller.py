from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication
from src.services.monitor import WindowWatcher
from src.services.capture import ScreenCapture
from src.services.ai_client import ArkClient
from src.services.storage import DataManager
from src.services.worker import AnalysisWorker


class AppController(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.monitor = WindowWatcher()
        self.capture = ScreenCapture()
        self.ai = ArkClient()
        self.storage = DataManager()
        self.workers = []
        self.window.start_monitoring_signal.connect(self.start_monitoring)
        self.window.stop_monitoring_signal.connect(self.stop_monitoring)
        self.window.open_history_signal.connect(self.open_history)
        self.monitor.window_changed.connect(self.handle_window_change)
        app = QApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(self.cleanup)

    @Slot()
    def start_monitoring(self):
        if not self.monitor.isRunning():
            self.monitor.start()

    @Slot()
    def stop_monitoring(self):
        if self.monitor.isRunning():
            self.monitor.stop()

    @Slot(int, str)
    def handle_window_change(self, hwnd, title):
        self.window.update_status(f"正在分析: {title[:15]}...")
        worker = AnalysisWorker(hwnd, title, self.capture, self.ai, self.storage)
        self.workers.append(worker)
        worker.finished.connect(self.handle_analysis_finished)
        worker.start()

    @Slot(str, str)
    def handle_analysis_finished(self, summary, img_path):
        short_summary = (summary[:20] + "..") if len(summary) > 20 else summary
        self.window.update_status(f"完成: {short_summary}")
        sender = self.sender()
        if sender in self.workers:
            self.workers.remove(sender)
        sender.deleteLater()

    @Slot()
    def open_history(self):
        if not hasattr(self, "history_window") or self.history_window is None:
            from src.ui.history_window import HistoryWindow

            self.history_window = HistoryWindow(self.storage)
        self.history_window.refresh_data()
        self.history_window.show()
        self.history_window.raise_()

    @Slot()
    def cleanup(self):
        if self.monitor.isRunning():
            self.monitor.stop()
        for worker in list(self.workers):
            if worker.isRunning():
                worker.wait()
            worker.deleteLater()
        self.workers.clear()
