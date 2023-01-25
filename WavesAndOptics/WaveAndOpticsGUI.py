import os
import time

###
import sys
import numpy as np
import time
###
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from functools import partial
###
try:
    import GUIParametersWaveAndOptics
except:
    import WavesAndOptics.GUIParametersWaveAndOptics as GUIParametersWaveAndOptics


size_Image = 200

class WavesAndOpticsWindow(QMainWindow):
    """
    Main window of the GUI.
    """    
    def __init__(self,parent=None,language= "En"):
        """Initializes the GUI Window"""
        self.language = language
        self.parameters = GUIParametersWaveAndOptics.GUIParameters()
        self.tabs = QTabWidget()
        self.current_lineIntegral = 1
        super().__init__(parent=parent)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Waves and Optics")

        self.generalLayoutSHM = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()

        centralWidgetSHM = QWidget(self)
        centralWidgetReadMe = QWidget(self)

        centralWidgetSHM.setLayout(self.generalLayoutSHM)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)

        self.tabs.addTab(centralWidgetSHM,"SHM")
        self.tabs.addTab(centralWidgetReadMe,"ReadMe")

        self.setCentralWidget(self.tabs)

###
if __name__ == "__main__":
    os.system('clear')
    print(f"Starting program at {time.strftime('%H:%M:%S')}")
    initial = time.time()
    app = QApplication([])
    window=WavesAndOpticsWindow()
    window.show()
    sys.exit(app.exec())