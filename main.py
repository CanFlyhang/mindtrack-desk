import sys
import os
from PySide6.QtWidgets import QApplication
from src.ui.floating_window import FloatingWindow
from src.app_controller import AppController

def main():
    # Set High DPI scaling
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_API"] = "pyside6"
    
    app = QApplication(sys.argv)
    
    # Load stylesheet
    try:
        with open("src/ui/styles.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: styles.qss not found")

    # Create UI
    window = FloatingWindow()
    
    # Initialize Controller (wires logic to UI)
    controller = AppController(window)
    
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
