import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider,
    QHBoxLayout, QVBoxLayout, QWidget,
    QTabWidget
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui_mainWindow()
        self.ui_tabWidgets()
        # self.setCentralWidget(slider)
    
    def ui_mainWindow(self):
        self.setWindowTitle("My App")
        print('Window Size : ', self.geometry().x(), self.geometry().y())
        self.setGeometry(300, 300, 500, 500)
        self.setMinimumSize(400,300) # Set minimum window size
        print('Window Size : ', self.geometry().x(), self.geometry().y())
        self.show()

    def ui_tabWidgets(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab_test(),'Test')
        self.tabs.addTab(self.tab_pils(),'PILS')
        self.setCentralWidget(self.tabs)
    
    def tab_test(self):
        parent = QWidget()

        self.hori_slider1 = QHValueSlider("Label1", parent = parent)
        print('1')
        self.hori_slider2 = QHValueSlider("TEst", parent = parent)
        print('2')
        # hori_slider3 = QHValueSlider(parent = parent)
        # print('3')

        vert_box = QVBoxLayout(parent)
        vert_box.addStretch(1)
        print('1')
        vert_box.addLayout(self.hori_slider1)
        vert_box.addStretch(1)
        print('2')
        vert_box.addLayout(self.hori_slider2)
        vert_box.addStretch(1)
        print('3')
        # vert_box.addLayout(hori_slider3)
        # vert_box.addStretch(1)

        parent.setLayout(vert_box)
        self.setCentralWidget(parent)
        return parent

    def tab_pils(self):
        parent = QWidget(self)
        print("PILS")
        label = QLabel("PILS")

        hori_box = QHBoxLayout()
        hori_box.addWidget(label)

        vert_box = QVBoxLayout()
        vert_box.addStretch(1)
        vert_box.addLayout(hori_box)
        vert_box.addStretch(1)

        parent.setLayout(vert_box)
        return parent


class QHValueSlider(QHBoxLayout):

    def __init__(self, name:str=None, parent = None):
        super().__init__(parent)

        self.slider = QSlider(Qt.Horizontal, parent)

        self.slider_res = 100.0
        self.slider_min_val = -10.5
        self.slider_max_val = +8.3
        self.slider_val = (self.slider_min_val+self.slider_max_val)/2

        self.slider.setMinimum(int(self.slider_min_val*self.slider_res))
        self.slider.setMaximum(int(self.slider_max_val*self.slider_res))
        self.slider.setValue(int(self.slider_val*self.slider_res))
        self.slider.valueChanged.connect(self.value_changed)

        self.label_slider_val = QLabel("%.2f" % self.slider_val,        parent)
        self.label_slider_min = QLabel("%.2f" % self.slider_min_val,    parent)
        self.label_slider_max = QLabel("%.2f" % self.slider_max_val,    parent)

        if(name is not None):
            self.label = QLabel(name, parent)
            self.addWidget(self.label)
        self.addWidget(self.label_slider_val)
        self.addWidget(self.label_slider_min)
        self.addWidget(self.slider)
        self.addWidget(self.label_slider_max)
        
    def value_changed(self, i):
        # print(i)
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