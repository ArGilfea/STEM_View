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
from QuantumMechanics.QuantumMechanicsGUI import QuantumMechanicsWindow
from Mechanics.MechanicsGUI import MechanicsWindow
import MetaGUIStrings

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

        self.setWindowTitle(MetaGUIStrings.GUITitle[f"{self.language}"])

        self._createAnalysisButton()
        self._createCalculusButton()
        self._createMechanicsButton()
        self._createPhysMedButton()
        self._createQMButton()
        self._createWavesAndOpticsButton()
        self._createExitButton()

    def _createAnalysisButton(self):
        """Creates the button for the Analysis GUI"""
        self.Analysis = QPushButton(MetaGUIStrings.Analysis[f"{self.language}"])
        self.Analysis.setToolTip(MetaGUIStrings.OpenWindow1[f"{self.language}"] + 
                             MetaGUIStrings.Analysis[f"{self.language}"] + 
                             MetaGUIStrings.OpenWindow2[f"{self.language}"] +
                             " (Ctrl+A)")
        self.Analysis.setShortcut("Ctrl+A")
        self.Analysis.clicked.connect(self.openAnalysis)
        self.generalLayout.addWidget(self.Analysis) 

    def _createCalculusButton(self):
        """Creates the button for the Calculus GUI"""
        self.Calc = QPushButton(MetaGUIStrings.Calculus[f"{self.language}"])
        self.Calc.setToolTip(MetaGUIStrings.OpenWindow1[f"{self.language}"] + 
                             MetaGUIStrings.Calculus[f"{self.language}"] + 
                             MetaGUIStrings.OpenWindow2[f"{self.language}"] +
                             " (Ctrl+C)")
        self.Calc.setShortcut("Ctrl+C")
        self.Calc.clicked.connect(self.openCalc)
        self.generalLayout.addWidget(self.Calc)  

    def _createWavesAndOpticsButton(self):
        """Creates the button for the Waves and Optics GUI"""

        self.WavesOptics = QPushButton(MetaGUIStrings.WavesAndOptics[f"{self.language}"])
        self.WavesOptics.setToolTip(MetaGUIStrings.OpenWindow1[f"{self.language}"] + 
                             MetaGUIStrings.WavesAndOptics[f"{self.language}"] + 
                             MetaGUIStrings.OpenWindow2[f"{self.language}"] +
                             " (Ctrl+W)")
        self.WavesOptics.setShortcut("Ctrl+W")
        self.WavesOptics.clicked.connect(self.openWavesOptics)
        self.generalLayout.addWidget(self.WavesOptics)  

    def _createPhysMedButton(self):
        """Creates the button for the Medical Physics GUI"""
        self.PhysMed = QPushButton(MetaGUIStrings.MedicalPhysics[f"{self.language}"])
        self.PhysMed.setToolTip(MetaGUIStrings.OpenWindow1[f"{self.language}"] + 
                             MetaGUIStrings.MedicalPhysics[f"{self.language}"] + 
                             MetaGUIStrings.OpenWindow2[f"{self.language}"] +
                             " (Ctrl+M)")
        self.PhysMed.clicked.connect(self.openPhysMed)
        self.PhysMed.setShortcut("Ctrl+M")
        self.generalLayout.addWidget(self.PhysMed)  

    def _createMechanicsButton(self):
        """Creates the button for the Mechanics GUI"""
        self.Mechanics = QPushButton(MetaGUIStrings.Mechanics[f"{self.language}"])
        self.Mechanics.setToolTip(MetaGUIStrings.OpenWindow1[f"{self.language}"] + 
                             MetaGUIStrings.Mechanics[f"{self.language}"] + 
                             MetaGUIStrings.OpenWindow2[f"{self.language}"] +
                             " (Ctrl+N)")
        self.Mechanics.clicked.connect(self.openMechanics)
        self.Mechanics.setShortcut("Ctrl+N")
        self.generalLayout.addWidget(self.Mechanics)  

    def _createQMButton(self):
        """Creates the button for the Quantum Mechanics GUI"""
        self.QM = QPushButton(MetaGUIStrings.QuantumMechanics[f"{self.language}"])
        self.QM.setToolTip(MetaGUIStrings.OpenWindow1[f"{self.language}"] + 
                             MetaGUIStrings.QuantumMechanics[f"{self.language}"] + 
                             MetaGUIStrings.OpenWindow2[f"{self.language}"] +
                             " (Ctrl+S)")
        self.QM.clicked.connect(self.openQM)
        self.QM.setShortcut("Ctrl+S")
        self.generalLayout.addWidget(self.QM)  

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

        self.exit = QPushButton(MetaGUIStrings.Exit[f"{self.language}"])
        self.exit.setToolTip(MetaGUIStrings.ExitTooltip[f"{self.language}"] + " (Ctrl + E)")
        self.exit.setShortcut("Ctrl+E")
        self.exit.clicked.connect(self.close)

        layout.addWidget(self.languageBox)
        layout.addWidget(self.exit)

        self.generalLayout.addWidget(subWidget)  

    def openAnalysis(self):
        "Opens the Analysis GUI"
        window = AnalysisWindow(self,language= self.language)
        window.show()

    def openCalc(self):
        "Opens the Calculus GUI"
        window = CalculusWindow(self,language= self.language)
        window.show()

    def openWavesOptics(self):
        "Opens the Waves and Optics GUI"
        window = WavesAndOpticsWindow(self,language= self.language)
        window.show()

    def openMechanics(self):
        "Opens the Mechanics GUI"
        window = MechanicsWindow(self,language= self.language)
        window.show()

    def openPhysMed(self):
        "Opens the Medical Physics GUI"
        window = MedPhysWindow(self,language= self.language)
        window.show()

    def openQM(self):
        "Opens the Quantum Mechanics GUI"
        window = QuantumMechanicsWindow(self,language= self.language)
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