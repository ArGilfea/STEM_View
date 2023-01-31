import os
import time

###
import time
###
import sys
from PyQt5.QtWidgets import *
###
from MedPhys.MedPhysGUI import MedPhysWindow
from Calculus.CalculusGUI import CalculusWindow
from WavesAndOptics.WaveAndOpticsGUI import WavesAndOpticsWindow
from Analysis.AnalysisGUI import AnalysisWindow

class MetaGUI(QMainWindow):
    def __init__(self,parent=None):
        """Initializes the GUI Window"""
        self.tabs = QWidget()
        self.language = "En"
        self.BUTTON_SIZE = 40
        self.DISPLAY_HEIGHT = 35
        self.current_line = 1
        super().__init__(parent=None)
        self.setMinimumSize(300, 200)

        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        self.initializeGUI()

    def initializeGUI(self):
        titles = {
            "En" : "Science GUI",
            "Fr" : "GUI Sciences"
        }
        self.setWindowTitle(titles[f"{self.language}"])

        self._createAnalysisButton()
        self._createCalculusButton()
        self._createPhysMedButton()
        self._createWavesAndOpticsButton()
        self._createExitButton()

    def _createAnalysisButton(self):
        """Creates the button for the Analysis GUI"""
        titles = {
            "En" : "Analysis",
            "Fr" : "Analyse"
        }
        self.Analysis = QPushButton(titles[f"{self.language}"])
        self.Analysis.setToolTip("Opens the Analysis Section")
        self.Analysis.clicked.connect(self.openAnalysis)
        self.generalLayout.addWidget(self.Analysis) 

    def _createCalculusButton(self):
        """Creates the button for the Calculus GUI"""
        titles = {
            "En" : "Calculus",
            "Fr" : "Calcul"
        }
        self.Calc = QPushButton(titles[f"{self.language}"])
        self.Calc.setToolTip("Opens the Calculus Section")
        self.Calc.clicked.connect(self.openCalc)
        self.generalLayout.addWidget(self.Calc)  

    def _createWavesAndOpticsButton(self):
        """Creates the button for the Waves and Optics GUI"""
        titles = {
            "En" : "Waves and Optics",
            "Fr" : "Ondes et Optique"
        }
        self.WavesOptics = QPushButton(titles[f"{self.language}"])
        self.WavesOptics.setToolTip("TBA")
        self.WavesOptics.clicked.connect(self.openWavesOptics)
        self.generalLayout.addWidget(self.WavesOptics)  

    def _createPhysMedButton(self):
        """Creates the button for the Medical Physics GUI"""
        titles = {
            "En" : "Medical Physics",
            "Fr" : "Physique Médicale"
        }
        self.PhysMed = QPushButton(titles[f"{self.language}"])
        self.PhysMed.setToolTip("Opens the Medical Physics Section")
        self.PhysMed.clicked.connect(self.openPhysMed)
        self.generalLayout.addWidget(self.PhysMed)  

    def _createExitButton(self):
        """Create an exit button"""
        subWidget = QWidget()
        layout = QHBoxLayout()
        subWidget.setLayout(layout)

        self.languageBox = QComboBox()
        self.languageBox.addItem("En")
        self.languageBox.addItem("Fr")
        self.languageBox.setCurrentText(self.language)

        self.languageBox.activated[str].connect(self.update_Combo_Language)

        self.exit = QPushButton("Exit")
        self.exit.setToolTip("Closes the GUI and its dependencies")
        self.exit.clicked.connect(self.close)

        layout.addWidget(self.languageBox)
        layout.addWidget(self.exit)

        self.generalLayout.addWidget(subWidget)  

    def openAnalysis(self):
        "Opens a the Analysis GUI"
        window = AnalysisWindow(self,language= self.language)
        window.show()

    def openCalc(self):
        "Opens a the Calculus GUI"
        window = CalculusWindow(self,language= self.language)
        window.show()

    def openWavesOptics(self):
        "Opens a the Waves and Optics GUI"
        window = WavesAndOpticsWindow(self,language= self.language)
        window.show()

    def openPhysMed(self):
        "Opens a the Medical Physics GUI"
        window = MedPhysWindow(self,language= self.language)
        window.show()

    def update_Combo_Language(self):
        "Updates the Language of the GUI"
        self.language = self.languageBox.currentText()

        self.refreshGUI()

    def refreshGUI(self):
        """Erases all the GUI and reloads it"""
        if self.generalLayout is not None:
            while self.generalLayout.count():
                item = self.generalLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        self.initializeGUI()

###
if __name__ == "__main__":
    os.system('clear')
    print(f"Starting program at {time.strftime('%H:%M:%S')}")
    initial = time.time()
    app = QApplication([])
    window=MetaGUI()
    window.show()
    sys.exit(app.exec())