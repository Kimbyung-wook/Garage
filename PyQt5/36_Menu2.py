import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QFileDialog, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, Qt

class MyApp(QMainWindow):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.textEdit = QTextEdit(self)
    self.textEdit.move(100, 100)
    self.textEdit.resize(100, 100)
    # self.textEdit
    self._setMenubar()
    
    self.setWindowTitle('Menubar')
    self.setGeometry(300,300,400,300)
    self.setMinimumSize(300,200)
    self.show()

  def _setMenubar(self):
    self.statusBar()
    menubar = self.menuBar()
    menubar.setNativeMenuBar(False)

    menubarFile = menubar.addMenu('&File')
    menubarFile.addAction(self._buttonOpen())
    menubarFile.addAction(self._buttonExit())

    menubarFile = menubar.addMenu('&Help')
    menubarFile.addAction(self._buttonInfo())

  def _buttonExit(self):
    button = QAction(QIcon('exit.png'),'Exit',self)
    button.setShortcut('Ctrl+Q')
    button.setStatusTip('Exit Application')
    button.triggered.connect(qApp.quit)
    return button

  def _buttonOpen(self):
    button = QAction(QIcon('open.png'),'Open',self)
    button.setShortcut('Ctrl+O')
    button.setStatusTip('Open file')
    button.triggered.connect(lambda : self._showDialogFileOpen())
    return button

  def _showDialogFileOpen(self):
    fname = QFileDialog.getOpenFileName(self, 'Open file', './')
    if fname[0]:
      print('Open ',fname)
      f = open(fname[0],'r')
      with f:
        data = f.read()
        self.textEdit.setText(data)
    else:
      print('Canceled')

  def _buttonInfo(self):
    button = QAction(QIcon('info.png'),'Info',self)
    button.setStatusTip('Application Information')
    button.triggered.connect(lambda : self._showInfo())
    return button

  def _showInfo(self):
    QMessageBox.information(self, "Info", "MessageBox pop!")

if __name__=="__main__":
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())
