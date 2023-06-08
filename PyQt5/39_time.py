import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QDate, QTime, Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')

        now = QDate.currentDate()
        print(now.toString())
        print(now.toString('dd.MM.yyyy'))
        print(now.toString('dd.MM.yy'))
        print(now.toString(Qt.ISODate))
        print(now.toString(Qt.DefaultLocaleLongDate))
        
        now = QTime.currentTime()
        print(now.toString())
        print(now.toString('ss.mm.hh'))
        print(now.toString('hh.mm.ss.zzz'))
        print(now.toString(Qt.DefaultLocaleLongDate))

        self.setGeometry(300, 300, 400, 200)
        self.show()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())