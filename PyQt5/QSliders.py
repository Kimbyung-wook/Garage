import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,
    QHBoxLayout, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        slider = QSlider(Qt.Horizontal)

        self.slider_res = 100.0
        slider_min_val = -10.5
        slider_max_val = +8.3

        slider.setMinimum(int(slider_min_val*self.slider_res))
        slider.setMaximum(int(slider_max_val*self.slider_res))
        slider.setValue(int((slider_min_val+slider_max_val)*self.slider_res/2))
        # Or: slider.setRange(-10,3)
        # slider.setSingleStep(3)
        slider.valueChanged.connect(self.value_changed)
        slider.sliderMoved.connect(self.slider_position)
        slider.sliderPressed.connect(self.slider_pressed)
        slider.sliderReleased.connect(self.slider_released)

        self.slider_val = QLabel("%d" % slider.value())
        self.slider_min = QLabel("%.2f" % slider_min_val)
        self.slider_max = QLabel("%.2f" % slider_max_val)


        hori_box = QHBoxLayout()
        hori_box.addWidget(self.slider_val)
        hori_box.addWidget(self.slider_min)
        hori_box.addWidget(slider)
        hori_box.addWidget(self.slider_max)

        vert_box = QVBoxLayout()
        vert_box.addStretch(1)
        vert_box.addLayout(hori_box)
        vert_box.addStretch(1)

        self.widget = QWidget()
        self.widget.setLayout(vert_box)
        self.setCentralWidget(self.widget)
        # self.setCentralWidget(slider)

    def value_changed(self, i):
        print(i)
        self.slider_val.setText("%.2f" % (float(i)/self.slider_res))

    def slider_position(self, p):
        print("position", p)

    def slider_pressed(self):
        print("Pressed!")

    def slider_released(self):
        print("Released")

class QHValueSlider(QHBoxLayout):

    def __init__(self):
        super.__init__()

        slider = QSlider(Qt.Horizontal)

        self.slider_res = 100.0
        self.slider_min_val = -10.5
        self.slider_max_val = +8.3
        self.slider_val = (self.slider_min_val+self.slider_max_val)/2

        slider.setMinimum(int(self.slider_min_val*self.slider_res))
        slider.setMaximum(int(self.slider_max_val*self.slider_res))
        slider.setValue(int(self.slider_val*self.slider_res))
        # Or: slider.setRange(-10,3)
        # slider.setSingleStep(3)
        slider.valueChanged.connect(self.value_changed)
        # slider.sliderMoved.connect(self.slider_position)
        # slider.sliderPressed.connect(self.slider_pressed)
        # slider.sliderReleased.connect(self.slider_released)

        self.slider_val = QLabel("%.2f" % self.slider_val)
        self.slider_min = QLabel("%.2f" % self.slider_min_val)
        self.slider_max = QLabel("%.2f" % self.slider_max_val)

        hori_box = QHBoxLayout()
        hori_box.addWidget(self.slider_val)
        hori_box.addWidget(self.slider_min)
        hori_box.addWidget(self.slider)
        hori_box.addWidget(self.slider_max)
        
    def value_changed(self, i):
        self.slider_val.setText("%.2f" % (float(i)/self.slider_res))

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()