import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

class MyApp(QMainWindow):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    actionExit = QAction(QIcon('exit.png'),'Exit',self)
    actionExit.setShortcut('Ctrl+Q')
    actionExit.setStatusTip('Exit Application')
    actionExit.triggered.connect(qApp.quit)

    self.statusBar()

    self.menuBar().setNativeMenuBar(False)
    menubarFile = self.menuBar().addMenu('&File')
    menubarFile.addAction(actionExit)
    
    self.setWindowTitle('Menubar')
    self.setGeometry(300,300,300,300)
    self.show()


if __name__=="__main__":
  app = QApplication(sys.argv)
  ex = MyApp()
  sys.exit(app.exec_())
