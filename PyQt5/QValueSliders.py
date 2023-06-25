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
        self.setMinimumSize(300,200) # Set minimum window size

        hori_slider1 = QHValueSlider("Label1")
        hori_slider2 = QHValueSlider()
        hori_slider3 = QHValueSlider()

        vert_box = QVBoxLayout()
        vert_box.addStretch(1)
        vert_box.addLayout(hori_slider1)
        vert_box.addLayout(hori_slider2)
        vert_box.addLayout(hori_slider3)
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

    def __init__(self, name:str=None):
        super().__init__()

        self.slider = QSlider(Qt.Horizontal)

        self.slider_res = 100.0
        self.slider_min_val = -10.5
        self.slider_max_val = +8.3
        self.slider_val = (self.slider_min_val+self.slider_max_val)/2

        self.slider.setMinimum(int(self.slider_min_val*self.slider_res))
        self.slider.setMaximum(int(self.slider_max_val*self.slider_res))
        self.slider.setValue(int(self.slider_val*self.slider_res))
        self.slider.valueChanged.connect(self.value_changed)

        self.label_slider_val = QLabel("%.2f" % self.slider_val)
        self.label_slider_min = QLabel("%.2f" % self.slider_min_val)
        self.label_slider_max = QLabel("%.2f" % self.slider_max_val)

        if(name is not None):
            self.label = QLabel(name)
            self.addWidget(self.label)
        self.addWidget(self.label_slider_val)
        self.addWidget(self.label_slider_min)
        self.addWidget(self.slider)
        self.addWidget(self.label_slider_max)
        
    def value_changed(self, i):
        self.slider_val = (float(i)/self.slider_res)
        self.label_slider_val.setText("%.2f" % self.slider_val)
    
    def setMininum(self, minimum : float):
        self.slider_min_val = minimum
        self.slider.setMinimum(int(self.slider_min_val*self.slider_res))

    def setMaxinum(self, minimum : float):
        self.slider_max_val = minimum
        self.slider.setMaximum(int(self.slider_max_val*self.slider_res))

    def getValue(self):
        return self.slider_val

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()