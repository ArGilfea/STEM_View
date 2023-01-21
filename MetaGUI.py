import os
import time

###
import time
###
import sys
from PyQt5.QtWidgets import *
###
from MedPhys.MedPhysGUI import MedPhysWindow

class MetaGUI(QMainWindow):
    def __init__(self,parent=None):
        """Initializes the GUI Window"""
        self.tabs = QWidget()
        self.BUTTON_SIZE = 40
        self.DISPLAY_HEIGHT = 35
        self.current_line = 1
        super().__init__(parent=None)
        self.setMinimumSize(300, 200)
        self.setWindowTitle("My GUI")

        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        self._createCalculusButton()
        self._createWavesAndOpticsButton()
        self._createPhysMedButton()
        self._createExitButton()

    def _createCalculusButton(self):
        """Creates the button for the Calculus GUI"""
        self.Calc = QPushButton("Calculus")
        self.Calc.setToolTip("TBA")
        self.Calc.clicked.connect(self.openCalc)
        self.generalLayout.addWidget(self.Calc)  

    def _createWavesAndOpticsButton(self):
        """Creates the button for the Waves and Optics GUI"""
        self.WavesOptics = QPushButton("Waves & Optics")
        self.WavesOptics.setToolTip("TBA")
        self.WavesOptics.clicked.connect(self.openWavesOptics)
        self.generalLayout.addWidget(self.WavesOptics)  

    def _createPhysMedButton(self):
        """Creates the button for the Medical Physics GUI"""
        self.PhysMed = QPushButton("Medical Physics")
        self.PhysMed.setToolTip("Opens the Medical Physics Section")
        self.PhysMed.clicked.connect(self.openPhysMed)
        self.generalLayout.addWidget(self.PhysMed)  

    def _createExitButton(self):
        """Create an exit button"""
        self.exit = QPushButton("Exit")
        self.exit.setToolTip("Closes the GUI and its dependencies")
        self.exit.clicked.connect(self.closing_button)
        self.generalLayout.addWidget(self.exit)  

    def openCalc(self):
        "Opens a the Calculus GUI"
        pass

    def openWavesOptics(self):
        "Opens a the Waves and Optics GUI"
        pass

    def openPhysMed(self):
        "Opens a the Medical Physics GUI"
        window = MedPhysWindow(self)
        window.show()

    def closing_button(self):
        """Closes the App"""
        self.close()



###
if __name__ == "__main__":
    os.system('clear')
    print(f"Starting program at {time.strftime('%H:%M:%S')}")
    initial = time.time()
    app = QApplication([])
    window=MetaGUI()
    window.show()
    sys.exit(app.exec())