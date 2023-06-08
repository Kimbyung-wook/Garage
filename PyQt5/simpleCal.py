import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QAction, qApp, QFileDialog, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, Qt

class MyApp(QMainWindow):
  def __init__(self):
    super().__init__()
    self.button_width = 30
    self.button_height = 30
    self.clearance = 7
    self.initUI()

  def initUI(self):
    # self.textEdit
    self._setMenubar()
    self._setDisplay()
    self._setButtons()
    
    self.setWindowTitle('Menubar')
    self.setGeometry(300,300,400,300)
    self.setMinimumSize(300,200)
    self.show()

  def _setDisplay(self):
    self.textEdit = QTextEdit(self)
    self.textEdit.move(self.clearance, 20+self.clearance)
    self.textEdit.resize((self.button_height+self.clearance)*4-self.clearance,
                          self.button_height*2-self.clearance*2)


  def _setMenubar(self):
    self.statusBar()
    menubar = self.menuBar()
    menubar.setNativeMenuBar(False)

    menubarFile = menubar.addMenu('&File')
    menubarFile.addAction(self._buttonExit())

  def _buttonExit(self):
    button = QAction(QIcon('exit.png'),'Exit',self)
    button.setShortcut('Ctrl+Q')
    button.setStatusTip('Exit Application')
    button.triggered.connect(qApp.quit)
    return button
    
  def _setButtons(self):
    self.numberbutton = dict()
    for i in range(1,10):
      self.numberbutton[i]= QPushButton("{:}".format(i), self)
      self.numberbutton[i].move(  (self.button_width+self.clearance)*((i-1)%3)+self.clearance,
                                  (self.button_height+self.clearance)*round((i-2)/3)+self.button_height*2+20)
      self.numberbutton[i].resize(self.button_width,
                                  self.button_height)
      # self.numberbutton[i].triggered.clicked()
    self.numberbutton[0] = QPushButton("0", self)
    self.numberbutton[0].move(  (self.button_width+self.clearance)*1+self.clearance,
                                (self.button_height+self.clearance)*3+self.button_height*2+20)
    self.numberbutton[0].resize(self.button_width,
                                self.button_height)

                                
    self.numberbutton['+'] = QPushButton("+", self)
    self.numberbutton['+'].move(  (self.button_width+self.clearance)*3+self.clearance,
                                  (self.button_height+self.clearance)*0+self.button_height*2+20)
    self.numberbutton['+'].resize(self.button_width,
                                  self.button_height)

    self.numberbutton['-'] = QPushButton("-", self)
    self.numberbutton['-'].move(  (self.button_width+self.clearance)*3+self.clearance,
                                  (self.button_height+self.clearance)*1+self.button_height*2+20)
    self.numberbutton['-'].resize(self.button_width,
                                  self.button_height)

    self.numberbutton['x'] = QPushButton("x", self)
    self.numberbutton['x'].move(  (self.button_width+self.clearance)*3+self.clearance,
                                  (self.button_height+self.clearance)*2+self.button_height*2+20)
    self.numberbutton['x'].resize(self.button_width,
                                  self.button_height)

    self.numberbutton['/'] = QPushButton("/", self)
    self.numberbutton['/'].move(  (self.button_width+self.clearance)*3+self.clearance,
                                  (self.button_height+self.clearance)*3+self.button_height*2+20)
    self.numberbutton['/'].resize(self.button_width,
                                  self.button_height)

    self.numberbutton['='] = QPushButton("=", self)
    self.numberbutton['='].move(  (self.button_width+self.clearance)*2+self.clearance,
                                  (self.button_height+self.clearance)*3+self.button_height*2+20)
    self.numberbutton['='].resize(self.button_width,
                                  self.button_height)
    self.numberbutton['='].clicked.connect(self.getResult)

  def getResult(self):
    print(self.textEdit.toPlainText())
if __name__=="__main__":
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())
