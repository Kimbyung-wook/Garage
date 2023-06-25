import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QLabel
from PyQt5.QtCore import Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.cos = False
        self.sin = False
        self.tan = False
        self.str = "String"
        self.str..

        self.initUI()

    def initUI(self):
        label = QLabel()

        cb_sin = QCheckBox('Sin', self)
        cb_sin.move(20, 50)
        cb_sin.stateChanged.connect(self.changeTitle)
        # cb_sin.toggle()

        cb_cos = QCheckBox('Cos', self)
        cb_cos.move(20, 100)
        cb_cos.stateChanged.connect(self.changeTitle)

        cb_tan = QCheckBox('Tan', self)
        cb_tan.move(20, 150)
        cb_tan.stateChanged.connect(self.changeTitle)



        self.setWindowTitle('QCheckBox')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def updateSin(self, state):
    def updateCos(self, state):
    def updateTan(self, state):
    def changeTitle(self, state):
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle(' ')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())