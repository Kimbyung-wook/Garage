import sys

#
import numpy as np
import random

# Qt Design libs
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QCheckBox, QLabel, QAction, qApp, QFileDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# For Figures
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation

class Trigonal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui_tab_widget()
        self.ui_mainWindow()

    # UI Functions
    def ui_tab_widget(self):
        tabs = QTabWidget()
        tabs.addTab(self.tab_figure(), 'Sin')
        tabs.addTab(self.tab_buttons(), 'Actions')
        tabs.addTab(QWidget(), 'Cos')
        self.setCentralWidget(tabs)

    def ui_mainWindow(self):
        self.setWindowTitle('Main Window')
        print('Window Size : ', self.geometry().x(), self.geometry().y())
        self.setGeometry(300, 300, 500, 500)
        self.setMinimumSize(400,300)
        print('Window Size : ', self.geometry().x(), self.geometry().y())
        self.show()

    
    # Figure Tab Window
    def tab_figure(self):
        parent = QWidget()

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        vbox.addWidget(self.animation_windows(parent))

        buttonStart = QPushButton("Start", parent)
        buttonStop  = QPushButton("Stop", parent)
        buttonStart.clicked.connect(lambda : self.runFigure())
        buttonStop.clicked.connect(lambda : self.stopFigure())
        hbox.addWidget(buttonStart)
        hbox.addWidget(buttonStop)
        vbox.addLayout(hbox)
        parent.setLayout(vbox)

        return parent

    def tab_buttons(self):
        parent = QWidget()
        buttonOpen = QPushButton('Open', parent=parent)
        buttonOpen.setGeometry(50,20,50,20)
        buttonOpen.clicked.connect(lambda : self.showDialogFileOpen())

        buttonClose = QPushButton('Close', parent=parent)
        buttonClose.setGeometry(150,20,50,20)
        buttonClose.clicked.connect(lambda : qApp.quit)

        return parent

    def showDialogFileOpen(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            print('Open ',fname)
            f = open(fname[0],'r')
            with f:
                data = f.read()
                print(data)
        else:
            print('Canceled')



    # Muli-figure setting
    def animation_windows(self, parent):
        self.canvas = MyMplCanvas(parent, width=10, height=8, dpi=100)
        x = np.arange(50)
        y = np.ones(50, dtype=np.float)
        self.line1_fig = []
        self.line1_fig.append(self.canvas.axis.plot(x, y, animated=True, color='red', lw=2)[0])
        self.line1_fig.append(self.canvas.axis.plot(x, y, animated=True, color='blue', lw=2)[0])
        print(self.line1_fig)
        # self.line1_fig = self.canvas.axis.plot(x, y, animated=True, color='red', lw=2)

        return self.canvas

    def runFigure(self):
        self.anime = animation.FuncAnimation(self.canvas.figure,
                                            self.update_figure,
                                            blit=True, interval=25)

    def update_figure(self, i):
        for fig in self.line1_fig:
            y = random.randint(0,1000)
            old_y = fig.get_ydata()
            new_y = np.r_[old_y[1:], y]
            fig.set_ydata(new_y)

        return self.line1_fig

    def stopFigure(self):
        self.anime._stop()

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axis = fig.add_subplot(111, xlim=(0,50), ylim=(0, 1024))
        self.axis.grid()

        self.compute_initial_figure()
        FigureCanvas.__init__(self, figure=fig)
        self.setParent(parent)

    def compute_initial_figure(self):
        pass

    def setXlim(self, boundary:tuple):
        self.axis.Xlim(boundary)

    def setYlim(self, boundary:tuple):
        self.axis.ylim(boundary)

    def setXlabel(self, label:str):
        self.axis.xlabel(label)

    def setYlabel(self, label:str):
        self.axis.ylabel(label)

    def setLegend(self, legend:list):
        self.axis.legend(legend, loc='best')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Trigonal()
    sys.exit(app.exec_())