from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QApplication
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QCursor, QColor, QPainter, QBrush, QPen

class FloatingWindow(QWidget):
    # Signals
    start_monitoring_signal = Signal()
    stop_monitoring_signal = Signal()
    open_history_signal = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.dragging = False
        self.offset = QPoint()
        self.is_monitoring = False

    def init_ui(self):
        # Window flags
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Fixed size
        self.resize(300, 150)

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Content Container (for rounded corners and background)
        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.container_layout = QVBoxLayout(self.container)
        self.layout.addWidget(self.container)

        # Header (Title + Close Button)
        header_layout = QHBoxLayout()
        self.title_label = QLabel("智能监控助手")
        self.title_label.setObjectName("title")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.clicked.connect(QApplication.instance().quit)
        header_layout.addWidget(self.close_btn)
        
        self.container_layout.addLayout(header_layout)

        # Status Label
        self.status_label = QLabel("等待启动...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setObjectName("status_label")
        self.container_layout.addWidget(self.status_label)

        # Control Buttons
        btn_layout = QHBoxLayout()
        
        self.toggle_btn = QPushButton("开始监控")
        self.toggle_btn.setObjectName("action_btn")
        self.toggle_btn.clicked.connect(self.toggle_monitoring)
        btn_layout.addWidget(self.toggle_btn)

        self.history_btn = QPushButton("历史记录")
        self.history_btn.setObjectName("action_btn")
        self.history_btn.clicked.connect(self.open_history_signal.emit)
        btn_layout.addWidget(self.history_btn)

        self.container_layout.addLayout(btn_layout)

    def toggle_monitoring(self):
        self.is_monitoring = not self.is_monitoring
        if self.is_monitoring:
            self.toggle_btn.setText("停止监控")
            self.status_label.setText("正在监听屏幕...")
            self.toggle_btn.setStyleSheet("background-color: #ff4d4f; color: white;")
            self.start_monitoring_signal.emit()
        else:
            self.toggle_btn.setText("开始监控")
            self.status_label.setText("监控已暂停")
            self.toggle_btn.setStyleSheet("")
            self.stop_monitoring_signal.emit()

    def update_status(self, text):
        self.status_label.setText(text)

    # --- Dragging Logic ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def paintEvent(self, event):
        # Custom painting for rounded background
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Semi-transparent background
        painter.setBrush(QBrush(QColor(30, 30, 30, 220)))
        painter.setPen(Qt.NoPen)
        
        rect = self.rect()
        painter.drawRoundedRect(rect, 15, 15)
