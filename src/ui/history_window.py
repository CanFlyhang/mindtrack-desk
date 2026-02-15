from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                               QLabel, QScrollArea, QListWidgetItem, QSplitter)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
import os

class HistoryWindow(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.setWindowTitle("历史监控记录")
        self.resize(900, 600)
        self.init_ui()

    def init_ui(self):
        # Dark theme for history window
        self.setStyleSheet("""
            QWidget { background-color: #2b2b2b; color: #ffffff; }
            QListWidget { background-color: #333333; border: 1px solid #444; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #444; }
            QListWidget::item:selected { background-color: #1890ff; }
            QLabel { font-size: 14px; }
            QSplitter::handle { background-color: #444; }
        """)

        layout = QHBoxLayout(self)
        
        splitter = QSplitter(Qt.Horizontal)
        
        # Left: List
        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(300)
        self.list_widget.itemClicked.connect(self.load_details)
        splitter.addWidget(self.list_widget)
        
        # Right: Details
        self.details_container = QWidget()
        details_layout = QVBoxLayout(self.details_container)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title (Time + App)
        self.title_label = QLabel("选择左侧记录查看详情")
        self.title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("color: #40a9ff; margin-bottom: 10px;")
        self.content_layout.addWidget(self.title_label)
        
        # Image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #1e1e1e; border-radius: 8px; padding: 10px;")
        self.content_layout.addWidget(self.image_label)
        
        # Summary
        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("margin-top: 15px; line-height: 1.6;")
        self.summary_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.content_layout.addWidget(self.summary_label)
        
        self.content_layout.addStretch()
        
        self.scroll_area.setWidget(self.content_widget)
        details_layout.addWidget(self.scroll_area)
        
        splitter.addWidget(self.details_container)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        
        self.refresh_data()

    def refresh_data(self):
        self.list_widget.clear()
        records = self.data_manager.get_recent_records()
        # record: (id, timestamp, title, summary, image_path)
        for record in records:
            timestamp = record[1]
            title = record[2]
            # Truncate title if too long
            display_title = (title[:25] + '..') if len(title) > 25 else title
            
            item = QListWidgetItem(f"[{timestamp}]\n{display_title}")
            item.setData(Qt.UserRole, record)
            self.list_widget.addItem(item)

    def load_details(self, item):
        record = item.data(Qt.UserRole)
        # record: (id, timestamp, title, summary, image_path)
        
        self.title_label.setText(f"{record[1]}\n{record[2]}")
        self.summary_label.setText(f"AI 总结：\n{record[3]}")
        
        img_path = record[4]
        if img_path and os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            # Scale to fit width of scroll area (approx)
            target_width = self.scroll_area.width() - 60
            if pixmap.width() > target_width:
                pixmap = pixmap.scaledToWidth(target_width, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.show()
        else:
            self.image_label.clear()
            self.image_label.setText("图片文件不存在")
