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
    import QuantumMechanicsStrings
    import GUIParametersQuantumMechanics
    import WaveFunctions
except:
    import QuantumMechanics.QuantumMechanicsStrings as QuantumMechanicsStrings
    import QuantumMechanics.GUIParametersQuantumMechanics as GUIParametersQuantumMechanics
    import QuantumMechanics.WaveFunctions as WaveFunctions
try:
    import Constants
except:
    import sys
    import os
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    import Constants
###
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
import math
###
import markdown

size_Image = 200

class QuantumMechanicsWindow(QMainWindow):
    """
    Main window of the GUI.
    """    
    def __init__(self,parent=None,language = "Fr"):
        """Initializes the GUI Window"""
        self.parameters = GUIParametersQuantumMechanics.GUIParameters()
        self.tabs = QTabWidget()
        self.current_line1DWaveFunction = 1

        super().__init__(parent=parent)
        self.setMinimumSize(1200, 700)
        self.language = language
        self.setWindowTitle(QuantumMechanicsStrings.WindowName[f"{self.language}"])

        self.generalLayout1DWaveFunction = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()

        centralWidget1DWaveFunction = QWidget(self)
        centralWidgetReadMe = QWidget(self)

        centralWidget1DWaveFunction.setLayout(self.generalLayout1DWaveFunction)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)

        self.tabs.addTab(centralWidget1DWaveFunction,QuantumMechanicsStrings.WaveFunction1DTab[f"{self.language}"])
        self.tabs.addTab(centralWidgetReadMe,QuantumMechanicsStrings.ReadMeName[f"{self.language}"])

        self.setCentralWidget(self.tabs)
        ### 1D WaveFunction
        self._createWaveFunctionImage()
        self._createEnergyLevelImage()
        self._createTimeWaveFunction1DImage()
        self._createOptionsParametric2DFunctions()
        ### Exit
        self._createExitButton() 

        self.generalLayout1DWaveFunction.setColumnStretch(1,5)
        self.generalLayout1DWaveFunction.setColumnStretch(2,5)

################################
    def _createWaveFunctionImage(self):
        """Creates the Image for the Wave Function and the Potential"""
        self.WaveFunction1DImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.WaveFunction1DImage_cid = self.WaveFunction1DImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.WaveFunction1DImage))
        self.WaveFunction1DImage_cod = self.WaveFunction1DImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.WaveFunction1DImage))
        self.generalLayout1DWaveFunction.addWidget(self.WaveFunction1DImage,self.current_line1DWaveFunction,1)
        #self.current_line1DWaveFunction += 1

    def _createEnergyLevelImage(self):
        """Creates the Image for the Energy Levels"""
        self.EnergyLevel1DWaveFunctionImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.EnergyLevel1DWaveFunctionImage_cid = self.EnergyLevel1DWaveFunctionImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.EnergyLevel1DWaveFunctionImage))
        self.EnergyLevel1DWaveFunctionImage_cod = self.EnergyLevel1DWaveFunctionImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.EnergyLevel1DWaveFunctionImage))
        self.generalLayout1DWaveFunction.addWidget(self.EnergyLevel1DWaveFunctionImage,self.current_line1DWaveFunction,2)
        self.current_line1DWaveFunction += 1

    def _createTimeWaveFunction1DImage(self):
        """Creates the Image for the Energy Levels"""
        self.Time1DWaveFunctionImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.Time1DWaveFunctionImage_cid = self.Time1DWaveFunctionImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.Time1DWaveFunctionImage))
        self.Time1DWaveFunctionImage_cod = self.Time1DWaveFunctionImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.Time1DWaveFunctionImage))
        self.generalLayout1DWaveFunction.addWidget(self.Time1DWaveFunctionImage,self.current_line1DWaveFunction,1)
        self.updateWaveFunction1DImages()

    def _createOptionsParametric2DFunctions(self):
        """Creates the docks for the options of the 1D WaveFunction"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.WaveFunction1DCurveType = QComboBox()
        for _, names in QuantumMechanicsStrings.WaveFunction1DFunctions.items():
            self.WaveFunction1DCurveType.addItem(names[f"{self.language}"])
        self.WaveFunction1DCurveType.setCurrentText(self.parameters.WaveFunction1DType)
        self.WaveFunction1DCurveType.activated[str].connect(self.update_Combo_WaveFunction1DFunctions)

        self.WaveFunction1DMassType = QComboBox()
        for _, names in QuantumMechanicsStrings.MassType.items():
            self.WaveFunction1DMassType.addItem(names[f"{self.language}"])
        self.WaveFunction1DMassType.setCurrentText(self.parameters.massFactorType)
        self.WaveFunction1DMassType.activated[str].connect(self.update_Combo_WaveFunction1DMassType)

        self.LogEnergiesCheckBox = QCheckBox()
        self.SquaredWaveFunctionCheckBox = QCheckBox()
        self.LogEnergiesCheckBox.stateChanged.connect(self.updateCheckBoxes1DWaveFunctions)
        self.SquaredWaveFunctionCheckBox.stateChanged.connect(self.updateCheckBoxes1DWaveFunctions)

        self.WaveFunction1DMassLineEdit = QLineEdit()
        self.WaveFunction1DMassLineEdit.setFixedWidth(90)
        self.WaveFunction1DMassLineEdit.setText(f"{(self.parameters.mass):.2f}")
        self.WaveFunction1DMassLineEdit.editingFinished.connect(self.update_Combo_WaveFunction1DParameters)

        self.WaveFunction1DParametersLineEdit = QLineEdit()
        self.WaveFunction1DParametersLineEdit.setFixedWidth(90)
        self.WaveFunction1DParametersLineEdit.setText(f"{(self.parameters.WaveFunction1DParameters[0]):.2f}")
        self.WaveFunction1DParametersLineEdit.editingFinished.connect(self.update_Combo_WaveFunction1DParameters)

        self.WaveFunction1DEnergyLevelLineEdit = QLineEdit()
        self.WaveFunction1DEnergyLevelLineEdit.setFixedWidth(90)
        self.WaveFunction1DEnergyLevelLineEdit.setText(f"{(self.parameters.WaveFunction1DLevel)}")
        self.WaveFunction1DEnergyLevelLineEdit.editingFinished.connect(self.update_Combo_WaveFunction1DParameters)

        self.WaveFunction1DBoundsMinLineEdit = QLineEdit()
        self.WaveFunction1DBoundsMaxLineEdit = QLineEdit()
        self.WaveFunction1DBoundsMinLineEdit.setFixedWidth(90)
        self.WaveFunction1DBoundsMaxLineEdit.setFixedWidth(90)
        self.WaveFunction1DBoundsMinLineEdit.setText(f"{(self.parameters.WaveFunction1DXBounds[0]):.2f}")
        self.WaveFunction1DBoundsMaxLineEdit.setText(f"{(self.parameters.WaveFunction1DXBounds[1]):.2f}")
        self.WaveFunction1DBoundsMinLineEdit.editingFinished.connect(self.update_Combo_WaveFunction1DParameters)
        self.WaveFunction1DBoundsMaxLineEdit.editingFinished.connect(self.update_Combo_WaveFunction1DParameters)

        layout.addWidget(QLabel(QuantumMechanicsStrings.WaveFunctionGraphTitle[f"{self.language}"]),0,0)
        layout.addWidget(self.WaveFunction1DCurveType,0,1)

        layout.addWidget(QLabel(QuantumMechanicsStrings.Mass[f"{self.language}"]),1,0)
        layout.addWidget(self.WaveFunction1DMassLineEdit,1,1)
        layout.addWidget(self.WaveFunction1DMassType,1,2)

        layout.addWidget(QLabel(QuantumMechanicsStrings.Parameters[f"{self.language}"]),2,0)
        layout.addWidget(self.WaveFunction1DParametersLineEdit,2,1)

        layout.addWidget(QLabel(QuantumMechanicsStrings.EnergyLevel[f"{self.language}"]),3,0)
        layout.addWidget(self.WaveFunction1DEnergyLevelLineEdit,3,1)

        layout.addWidget(QLabel(QuantumMechanicsStrings.Bounds[f"{self.language}"]),4,0)
        layout.addWidget(self.WaveFunction1DBoundsMinLineEdit,4,1)
        layout.addWidget(self.WaveFunction1DBoundsMaxLineEdit,4,2)


        layout.addWidget(QLabel(QuantumMechanicsStrings.LogEnergies[f"{self.language}"]),10,0)
        layout.addWidget(self.LogEnergiesCheckBox,10,1)
        layout.addWidget(QLabel(QuantumMechanicsStrings.SquaredWaveFunction[f"{self.language}"]),11,0)
        layout.addWidget(self.SquaredWaveFunctionCheckBox,11,1)

        self.generalLayout1DWaveFunction.addWidget(subWidget,self.current_line1DWaveFunction,2)
        self.current_line1DWaveFunction += 1
################################
    def _createExitButton(self):
        """Creates an exit button"""
        self.exit1DWaveFunction = QPushButton(QuantumMechanicsStrings.ExitLabel[f"{self.language}"])

        self.exit1DWaveFunction.setToolTip(QuantumMechanicsStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        
        self.exit1DWaveFunction.setShortcut("Ctrl+Shift+E")

        self.exit1DWaveFunction.clicked.connect(self.close)

        self.generalLayout1DWaveFunction.addWidget(self.exit1DWaveFunction,self.current_line1DWaveFunction+1,3)  

        self.current_line1DWaveFunction += 1
################################
    def update_Combo_WaveFunction1DFunctions(self):
        """Updates the Curve Type"""
        name_tmp = self.WaveFunction1DCurveType.currentText()
        for dict, names in QuantumMechanicsStrings.WaveFunction1DFunctions.items():
            if name_tmp in names.values():
                self.parameters.WaveFunction1DType = dict

        self.updateCurveWaveFunction1D()

    def update_Combo_WaveFunction1DMassType(self):
        """Updates the Curve Type"""
        name_tmp = self.WaveFunction1DMassType.currentText()
        for dict, names in QuantumMechanicsStrings.MassType.items():
            if name_tmp in names.values():
                self.parameters.massFactorType = dict

        self.updateMassWaveFunction1D()

    def update_Combo_WaveFunction1DParameters(self):
        """Updates the parameters from the LineEdits"""

        try:
            self.parameters.mass = float(self.WaveFunction1DMassLineEdit.text())
        except:
            self.parameters.mass = 1.0
        try:
            self.parameters.WaveFunction1DParameters[0] = float(self.WaveFunction1DParametersLineEdit.text())
        except:
            self.parameters.WaveFunction1DParameters[0] = 1.0
        try:
            self.parameters.WaveFunction1DLevel = int(self.WaveFunction1DEnergyLevelLineEdit.text())
        except:
            self.parameters.WaveFunction1DLevel = 1
        try:
            self.parameters.WaveFunction1DXBounds[0] = float(self.WaveFunction1DBoundsMinLineEdit.text())
        except:
            self.parameters.WaveFunction1DXBounds[0] = -1.0
        try:
            self.parameters.WaveFunction1DXBounds[1] = float(self.WaveFunction1DBoundsMaxLineEdit.text())
        except:
            self.parameters.WaveFunction1DXBounds[1] = 1.0
            
        self.updateMassValueWaveFunction1D()

    def updateMassWaveFunction1D(self):
        """Updates the Mass type value"""
        if self.parameters.massFactorType == "electron":
            self.parameters.massFactorValue = Constants.electron_mass
        elif self.parameters.massFactorType == "proton":
            self.parameters.massFactorValue = Constants.proton_mass
        elif self.parameters.massFactorType == "neutron":
            self.parameters.massFactorValue = Constants.neutron_mass
        elif self.parameters.massFactorType == "kg":
            self.parameters.massFactorValue = 1
        self.updateMassValueWaveFunction1D()

    def updateMassValueWaveFunction1D(self):
        self.parameters.combinedMass = self.parameters.mass * self.parameters.massFactorValue

        self.updateValuesWaveFunction1DImages()

    def updateCurveWaveFunction1D(self):
        """Updates the WaveFunction Function"""
        if self.parameters.WaveFunction1DType == "InfiniteSquareWell":
            self.parameters.WaveFunction1DFunction = WaveFunctions.InfiniteSquareWell
        if self.parameters.WaveFunction1DType == "QuantumHarmonicOscillator":
            self.parameters.WaveFunction1DFunction = WaveFunctions.QuantumHarmonicOscillator
            
        self.updateValuesWaveFunction1DImages()

    def updateCheckBoxes1DWaveFunctions(self):
        """Updates the CheckBoxes for 1D WaveFunction"""
        if self.LogEnergiesCheckBox.isChecked():
            self.parameters.logScale1DEnergies = True
        else: 
            self.parameters.logScale1DEnergies = False
        if self.SquaredWaveFunctionCheckBox.isChecked():
            self.parameters.squaredWaveFunction = True
        else: 
            self.parameters.squaredWaveFunction = False
        self.updateWaveFunction1DImages()

    def updateValuesWaveFunction1DImages(self):
        """Updates the parameters of the 1D WaveFunction"""
        self.parameters.XAxis1D, self.parameters.WaveFunction1D, self.parameters.Energy1D, self.parameters.Potential1D = self.parameters.WaveFunction1DFunction(param = self.parameters.WaveFunction1DParameters, 
                                                                                                                                   level = self.parameters.WaveFunction1DLevel, 
                                                                                                                                   mass = self.parameters.combinedMass,
                                                                                                                                   bounds = self.parameters.WaveFunction1DXBounds)
        for i in range(self.parameters.EnergyLevelRange1D):
            _, _, self.parameters.EnergyLevelValues1D[i], _ = self.parameters.WaveFunction1DFunction(param = self.parameters.WaveFunction1DParameters, 
                                                                                                                                   level = i+1, 
                                                                                                                                   mass = self.parameters.combinedMass,
                                                                                                                                   bounds = self.parameters.WaveFunction1DXBounds,
                                                                                                                                   wholeComputations= False)
        self.parameters.TAxis1D, self.parameters.TimeWaveFunction1D = WaveFunctions.TimePart(bounds= self.parameters.WaveFunction1DTBounds, energy= self.parameters.Energy1D)


        self.updateWaveFunction1DImages()

    def updateWaveFunction1DImages(self):
        """Update the images for the 1D WaveFunction"""
        self.updateWaveFunctionImageWaveFunction1D()
        self.updateEnergyLevelImageWaveFunction1D()
        self.updateTimeImageWaveFunction1D()

    def updateWaveFunctionImageWaveFunction1D(self):
        """Updates the 1D WaveFunction Image"""
        try:
            self.WaveFunction1DImage.axes.cla()
        except:
            pass
        
        if self.parameters.squaredWaveFunction:
            self.WaveFunction1DImage.axes.plot(self.parameters.XAxis1D,np.abs(self.parameters.WaveFunction1D)**2, color = "blue", label = f"$|\Psi_{{{self.parameters.WaveFunction1DLevel}}}(x)|^2$")
        else:
            self.WaveFunction1DImage.axes.plot(self.parameters.XAxis1D,self.parameters.WaveFunction1D, color = "blue", label = f"$\Psi_{{{self.parameters.WaveFunction1DLevel}}}(x)$")

        if self.parameters.WaveFunction1DType == "InfiniteSquareWell":
            self.WaveFunction1DImage.axes.axvline(0,color = "brown", label = "V(x)")
            self.WaveFunction1DImage.axes.axvline(self.parameters.WaveFunction1DParameters[0],color = "brown")
        elif self.parameters.WaveFunction1DType in ["QuantumHarmonicOscillator"]:
            self.WaveFunction1DImage.axes.plot(self.parameters.XAxis1D,self.parameters.Potential1D,color = "brown", label = "V(x)")

        self.WaveFunction1DImage.axes.axhline(0,color = "black",alpha = 0.5)

        self.WaveFunction1DImage.axes.grid()
        self.WaveFunction1DImage.axes.legend()
        self.WaveFunction1DImage.axes.set_xlabel("x")
        self.WaveFunction1DImage.axes.set_ylabel(f"$\Psi$(x)")
        self.WaveFunction1DImage.axes.set_title(QuantumMechanicsStrings.WaveFunctionGraphTitle[f"{self.language}"]+
                                                           "\n"+
                                                           f"$\Psi(x)$ = "+
                                                           QuantumMechanicsStrings.WaveFunctionEquation(self.parameters.WaveFunction1DType,
                                                                                                        self.parameters.WaveFunction1DParameters,
                                                                                                        self.parameters.WaveFunction1DLevel,
                                                                                                        self.parameters.combinedMass))
        self.WaveFunction1DImage.draw()

    def updateEnergyLevelImageWaveFunction1D(self):
        """Updates the Energy Levels Image"""
        try:
            self.EnergyLevel1DWaveFunctionImage.axes.cla()
        except:
            pass

        for i in range(self.parameters.EnergyLevelRange1D):
            self.EnergyLevel1DWaveFunctionImage.axes.axhline(self.parameters.EnergyLevelValues1D[i], color = "grey")
        self.EnergyLevel1DWaveFunctionImage.axes.axhline(self.parameters.Energy1D, color = "red")

        self.EnergyLevel1DWaveFunctionImage.axes.axhline(0,color = "black",alpha = 0.5)

        self.EnergyLevel1DWaveFunctionImage.axes.grid()
        self.EnergyLevel1DWaveFunctionImage.axes.set_ylabel("E")
        topValue = np.max([np.max(self.parameters.EnergyLevelValues1D), self.parameters.Energy1D])

        self.EnergyLevel1DWaveFunctionImage.axes.set_title(QuantumMechanicsStrings.EnergyLevelGraphTitle[f"{self.language}"]+
                                                           "\n"+
                                                           f"E$_n$ = "+
                                                           QuantumMechanicsStrings.EnergyLevelEquation(self.parameters.WaveFunction1DType,
                                                                                                       self.parameters.WaveFunction1DParameters,
                                                                                                        self.parameters.WaveFunction1DLevel,
                                                                                                        self.parameters.combinedMass,
                                                                                                        self.parameters.Energy1D))
        if self.parameters.logScale1DEnergies:
            self.EnergyLevel1DWaveFunctionImage.axes.set_yscale("log")
        else:
            self.EnergyLevel1DWaveFunctionImage.axes.set_ylim(top = topValue * 1.1,
                                                            bottom = 0)
        self.EnergyLevel1DWaveFunctionImage.draw()

    def updateTimeImageWaveFunction1D(self):
        """Updates the Time  Image"""
        try:
            self.Time1DWaveFunctionImage.axes.cla()
        except:
            pass

        self.Time1DWaveFunctionImage.axes.grid()
        self.Time1DWaveFunctionImage.axes.set_xlabel("t")
        self.Time1DWaveFunctionImage.axes.set_title(QuantumMechanicsStrings.EnergyLevelGraphTitle[f"{self.language}"]+"\n"+
                                                           f"$\phi(t)$ = "+
                                                           QuantumMechanicsStrings.TimeEquation(self.parameters.Energy1D))

        self.Time1DWaveFunctionImage.draw()

################################
    def onClick(self,event,which):
        """Allows to click on an image and update the interface"""
        ix, iy = event.xdata, event.ydata
        which.coords = []
        which.coords.append((ix, iy))
        if len(which.coords) == 2:
            which.fig.canvas.mpl_disconnect(self.cid)
        if which == self.EnergyLevel1DWaveFunctionImage:
            closestEIndex = 0
            for i in range(self.parameters.EnergyLevelRange1D):
                if (self.parameters.EnergyLevelValues1D[i] - iy)**2 < (self.parameters.EnergyLevelValues1D[closestEIndex] - iy)**2:
                    closestEIndex = i
            
            self.parameters.WaveFunction1DLevel = closestEIndex + 1
            self.WaveFunction1DEnergyLevelLineEdit.setText(f"{(closestEIndex + 1)}")
            self.updateValuesWaveFunction1DImages()
    def onRoll(self,event,which):
        """Allows to scroll on an image and update the interface"""
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1
            #print("+")
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = -1
            #print("-")
        if which == self.EnergyLevel1DWaveFunctionImage:
            if scale_factor > 0:
                self.parameters.WaveFunction1DLevel += 1
            elif self.parameters.WaveFunction1DLevel > 1 and scale_factor < 0:
                self.parameters.WaveFunction1DLevel -= 1
            self.WaveFunction1DEnergyLevelLineEdit.setText(f"{(self.parameters.WaveFunction1DLevel)}")
            self.updateValuesWaveFunction1DImages()
###
class MplCanvas(FigureCanvasQTAgg):
    """Class for the images and the graphs as a widget"""
    def __init__(self, parent=None, width:float=5, height:float=4, dpi:int=75):
        """Creates an empty figure with axes and fig as parameters"""
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout= True)
        self.axes = fig.add_subplot(111)
        self.fig = fig
        super(MplCanvas, self).__init__(fig)

if __name__ == "__main__":
    os.system('clear')
    print(f"Starting program at {time.strftime('%H:%M:%S')}")
    initial = time.time()
    app = QApplication([])
    window=QuantumMechanicsWindow()
    window.show()
    sys.exit(app.exec())