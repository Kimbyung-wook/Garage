import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout()
        widgets = [
            QCheckBox,          # 0
            QComboBox,          # 1
            QDateEdit,          # 2
            QDateTimeEdit,      # 3
            QDial,              # 4
            QDoubleSpinBox,     # 5
            QFontComboBox,      # 6
            QLCDNumber,         # 7
            QLabel,             # 8
            QLineEdit,          # 9
            QProgressBar,       # 10
            QPushButton,        # 1
            QRadioButton,       # 2
            QSlider,            # 3
            QSpinBox,           # 4
            QTimeEdit,          # 5
        ]

        widgets[8]().setText("Test")

        for w in widgets:
            layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()