import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication

class MyApp(QMainWindow):

  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    buttonOk = QPushButton('Ok', self)
    buttonOk.clicked.connect(lambda :self.actionOk())
    buttonCancel = QPushButton('Cancel', self)
    buttonCancel.clicked.connect(QCoreApplication.instance().quit)

    hori_box = QHBoxLayout()
    hori_box.addStretch(2)
    hori_box.addWidget(buttonOk)
    hori_box.addWidget(buttonCancel)
    hori_box.addStretch(1)

    vert_box = QVBoxLayout()
    vert_box.addStretch(1)
    vert_box.addLayout(hori_box)
    vert_box.addStretch(1)

    self.widget = QWidget()
    self.widget.setLayout(vert_box)
    self.setCentralWidget(self.widget)


    self.setWindowTitle('Box Layout')
    self.setGeometry(300, 300, 400, 200)
    self.show()

  def actionOk(self):
    self.msg = QMessageBox()
    self.msg.setIcon(QMessageBox.Information)
    self.msg.setText('Clicked Ok')
    self.msg.setInformativeText("MessageBox Pop-up")
    self.msg.setWindowTitle("Info")
    self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    self.msg.buttonClicked.connect(self.msgButton)

    retval = self.msg.exec_()
    print('Return ', retval)

  def msgButton(self, i):
    print("Click ", i.text())

if __name__ == '__main__':
  app = QApplication(sys.argv)
  mains = MyApp()
  mains.show()
  sys.exit(app.exec_())