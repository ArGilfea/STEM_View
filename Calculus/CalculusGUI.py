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
    import GUIParametersCalculus
    import Curves
except:
    import Calculus.GUIParametersCalculus as GUIParametersCalculus
    import Calculus.Curves as Curves
###
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
###
import markdown

size_Image = 200

class CalculusWindow(QMainWindow):
    """
    Main window of the GUI.
    """    
    def __init__(self,parent=None,language = "En"):
        """Initializes the GUI Window"""
        self.parameters = GUIParametersCalculus.GUIParameters()
        self.tabs = QTabWidget()
        self.current_lineIntegral = 1
        super().__init__(parent=parent)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Calculus")
        self.language = language

        self.generalLayoutIntegral = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()

        centralWidgetIntegral = QWidget(self)
        centralWidgetReadMe = QWidget(self)

        centralWidgetIntegral.setLayout(self.generalLayoutIntegral)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)

        self.tabs.addTab(centralWidgetIntegral,"Integral")
        self.tabs.addTab(centralWidgetReadMe,"ReadMe")

        self.setCentralWidget(self.tabs)

        self._createCurveBaseIntegral()
        self._createOptionsIntegral()
        self._createCurveSumIntegral()
        self._createCurveOtherIntegral()

        self._createExitButton() 

    def _createCurveBaseIntegral(self):
        """Creates an Image for a basic curve for the Integrals"""
        self.IntegralBasicImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutIntegral.addWidget(self.IntegralBasicImage,self.current_lineIntegral,1)

        self.updateBaseImageIntegral()

    def _createOptionsIntegral(self):
        """Creates the docks for the options of the Integrals"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.IntegralCurveType = QComboBox()
        self.IntegralCurveType.addItem("Constant")
        self.IntegralCurveType.addItem("Line")
        self.IntegralCurveType.addItem("Quadratic")
        self.IntegralCurveType.addItem("Cubic")
        self.IntegralCurveType.addItem("Exponential")
        self.IntegralCurveType.addItem("Sin")
        self.IntegralCurveType.addItem("Cos")
        self.IntegralCurveType.addItem("Tan")
        self.IntegralCurveType.addItem("ArcSin")
        self.IntegralCurveType.addItem("ArcCos")
        self.IntegralCurveType.addItem("ArcTan")
        self.IntegralCurveType.setCurrentText(self.parameters.IntegralCurveName)
        self.IntegralCurveType.activated[str].connect(self.update_Combo_CurveIntegral)

        self.IntegralBoxTypeCombo = QComboBox()
        self.IntegralBoxTypeCombo.addItem("Left Box")
        self.IntegralBoxTypeCombo.addItem("Right Box")
        self.IntegralBoxTypeCombo.addItem("Center Box")
        self.IntegralBoxTypeCombo.setCurrentText(self.parameters.IntegralBoxType)
        self.IntegralBoxTypeCombo.activated[str].connect(self.update_Combo_BoxTypeIntegral)

        self.FirstParameterIntegral = QLineEdit()
        self.SecondParameterIntegral = QLineEdit()
        self.ThirdParameterIntegral = QLineEdit()
        self.FourthParameterIntegral = QLineEdit()
        self.ShowBoxIntegral = QCheckBox()
        self.NumberBoxIntegral = QLineEdit()
        self.IntegralMin = QLineEdit()
        self.IntegralMax = QLineEdit()

        self.FirstParameterIntegral.setFixedWidth(90)
        self.SecondParameterIntegral.setFixedWidth(90)
        self.ThirdParameterIntegral.setFixedWidth(90)
        self.FourthParameterIntegral.setFixedWidth(90)
        self.NumberBoxIntegral.setFixedWidth(90)
        self.IntegralMin.setFixedWidth(90)
        self.IntegralMax.setFixedWidth(90)

        self.FirstParameterIntegral.setText(str(self.parameters.IntegralParameters[0]))
        self.SecondParameterIntegral.setText(str(self.parameters.IntegralParameters[1]))
        self.ThirdParameterIntegral.setText(str(self.parameters.IntegralParameters[2]))
        self.FourthParameterIntegral.setText(str(self.parameters.IntegralParameters[3]))
        self.NumberBoxIntegral.setText(str(self.parameters.IntegralBoxNumber))
        self.IntegralMin.setText(str(self.parameters.IntegralMinBox))
        self.IntegralMax.setText(str(self.parameters.IntegralMaxBox))

        self.FirstParameterIntegral.editingFinished.connect(self.updateCurveParametersIntegral)
        self.SecondParameterIntegral.editingFinished.connect(self.updateCurveParametersIntegral)
        self.ThirdParameterIntegral.editingFinished.connect(self.updateCurveParametersIntegral)
        self.FourthParameterIntegral.editingFinished.connect(self.updateCurveParametersIntegral)
        self.NumberBoxIntegral.editingFinished.connect(self.updateCurveNumberBoxesIntegral)
        self.ShowBoxIntegral.stateChanged.connect(self.updateCurveNumberBoxesIntegral)
        self.IntegralMin.editingFinished.connect(self.updateCureBoundsIntegral)
        self.IntegralMax.editingFinished.connect(self.updateCureBoundsIntegral)

        layout.addWidget(self.IntegralCurveType,0,0)
        layout.addWidget(self.IntegralBoxTypeCombo,0,1)
        layout.addWidget(QLabel("Parameters"),1,0)
        layout.addWidget(self.FirstParameterIntegral,1,1)
        layout.addWidget(self.SecondParameterIntegral,1,2)
        layout.addWidget(self.ThirdParameterIntegral,2,1)
        layout.addWidget(self.FourthParameterIntegral,2,2)
        layout.addWidget(QLabel("Boxes"),3,0)
        layout.addWidget(self.ShowBoxIntegral,3,1)        
        layout.addWidget(self.NumberBoxIntegral,3,2)
        layout.addWidget(QLabel("Bounds"),4,0)
        layout.addWidget(self.IntegralMin,4,1)
        layout.addWidget(self.IntegralMax,4,2)

        self.generalLayoutIntegral.addWidget(subWidget,self.current_lineIntegral,2)
        self.current_lineIntegral += 1

    def _createCurveSumIntegral(self):
        """Creates an Image for the Integral Result"""
        self.IntegralSumImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutIntegral.addWidget(self.IntegralSumImage,self.current_lineIntegral,1)
    def _createCurveOtherIntegral(self):
        """Creates another Image"""
        self.IntegralOtherImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutIntegral.addWidget(self.IntegralOtherImage,self.current_lineIntegral,2)
        self.current_lineIntegral += 1



    def _createExitButton(self):
        """Creates an exit button"""
        self.exitIntegral = QPushButton("Exit")
        self.exitIntegral.setToolTip("Closes the GUI and its dependencies")
        self.exitIntegral.setToolTip("Closes the GUI and its dependencies")
        self.exitIntegral.clicked.connect(self.close)
        self.generalLayoutIntegral.addWidget(self.exitIntegral,self.current_lineIntegral+1,3)  
        self.current_lineIntegral += 1

    def update_Combo_CurveIntegral(self):
        """Updates the Curve Type"""
        self.parameters.IntegralCurveName = self.IntegralCurveType.currentText()

        self.updateCurveIntegral()

    def update_Combo_BoxTypeIntegral(self):
        """Updates the Curve Type"""
        self.parameters.IntegralBoxType = self.IntegralBoxTypeCombo.currentText()

        self.updateBaseImageIntegral()

    def updateCurveParametersIntegral(self):
        """Updates the Parameters of the Curve"""
        try:
            self.parameters.IntegralParameters[0] = float(self.FirstParameterIntegral.text())
        except:
            self.parameters.IntegralParameters[0] = 1.0
        try:
            self.parameters.IntegralParameters[1] = float(self.SecondParameterIntegral.text())
        except:
            self.parameters.IntegralParameters[1] = 1.0
        try:
            self.parameters.IntegralParameters[2] = float(self.ThirdParameterIntegral.text())
        except:
            self.parameters.IntegralParameters[2] = 1.0
        try:
            self.parameters.IntegralParameters[3] = float(self.FourthParameterIntegral.text())
        except:
            self.parameters.IntegralParameters[4] = 1.0

        self.updateCurveIntegral()

    def updateCurveNumberBoxesIntegral(self):
        """Updates the number of boxes for the integral"""
        try:
            self.parameters.IntegralBoxNumber = int(self.NumberBoxIntegral.text())
        except:
            self.parameters.IntegralBoxNumber = 1
        if self.ShowBoxIntegral.isChecked():
            self.parameters.IntegralShowBoxes = True
        else: 
            self.parameters.IntegralShowBoxes = False

        self.updateCurveIntegral()

    def updateCureBoundsIntegral(self):
        """Updates the Bounds of the Integration"""
        try:
            self.parameters.IntegralMinBox = float(self.IntegralMin.text())
        except:
            self.parameters.IntegralMinBox = 0.0
        try:
            self.parameters.IntegralMaxBox = float(self.IntegralMax.text())
        except:
            self.parameters.IntegralMaxBox = 1.0
        self.updateCurveIntegral()


    def updateCurveIntegral(self):
        """Updates the Base Curve"""
        self.parameters.IntegralXAxis = self.IntegralXAxis = np.linspace(self.parameters.IntegralMinBox - 1,self.parameters.IntegralMaxBox + 1,1000)
        if self.parameters.IntegralCurveName == "Constant":
            self.parameters.IntegralCurve = Curves.FlatCurve
        elif self.parameters.IntegralCurveName == "Line":
            self.parameters.IntegralCurve = Curves.LinearCurve
        elif self.parameters.IntegralCurveName == "Quadratic":
            self.parameters.IntegralCurve = Curves.QuadraticCurve
        elif self.parameters.IntegralCurveName == "Cubic":
            self.parameters.IntegralCurve = Curves.CubicCurve
        elif self.parameters.IntegralCurveName == "Exponential":
            self.parameters.IntegralCurve = Curves.ExponentialCurve
        elif self.parameters.IntegralCurveName == "Sin":
            self.parameters.IntegralCurve = Curves.SinCurve
        elif self.parameters.IntegralCurveName == "Cos":
            self.parameters.IntegralCurve = Curves.CosCurve
        elif self.parameters.IntegralCurveName == "Tan":
            self.parameters.IntegralXAxis = self.IntegralXAxis = np.linspace(self.parameters.IntegralMinBox,self.parameters.IntegralMaxBox,1000)
            self.parameters.IntegralCurve = Curves.TanCurve
        elif self.parameters.IntegralCurveName == "ArcSin":
            self.parameters.IntegralCurve = Curves.ArcSinCurve
        elif self.parameters.IntegralCurveName == "ArcCos":
            self.parameters.IntegralCurve = Curves.ArcCosCurve
        elif self.parameters.IntegralCurveName == "ArcTan":
            self.parameters.IntegralCurve = Curves.ArcTanCurve        
        self.parameters.IntegralYAxis = self.parameters.IntegralCurve(self.parameters.IntegralXAxis,self.parameters.IntegralParameters)

        self.updateBaseImageIntegral()

    def updateBaseImageIntegral(self):
        """Updates the Base Curve"""
        try:
            self.IntegralBasicImage.axes.cla()
        except:
            pass

        self.IntegralBasicImage.axes.plot(self.parameters.IntegralXAxis,self.parameters.IntegralYAxis)

        if self.parameters.IntegralShowBoxes:
            dx = (self.parameters.IntegralMaxBox - self.parameters.IntegralMinBox)/self.parameters.IntegralBoxNumber
            for i in range(self.parameters.IntegralBoxNumber):
                if self.parameters.IntegralBoxType == "Left Box":
                    self.IntegralBasicImage.axes.add_patch(Rectangle((self.parameters.IntegralMinBox + i * dx,0),
                                                                        dx,
                                                                        self.parameters.IntegralCurve(self.parameters.IntegralMinBox + i * dx,
                                                                        self.parameters.IntegralParameters),
                                                                        alpha=0.3))
                elif self.parameters.IntegralBoxType == "Right Box":
                    self.IntegralBasicImage.axes.add_patch(Rectangle((self.parameters.IntegralMinBox + i * dx,0),
                                                                        dx,
                                                                        self.parameters.IntegralCurve(self.parameters.IntegralMinBox + (i + 1) * dx,
                                                                        self.parameters.IntegralParameters),
                                                                        alpha=0.3))
                elif self.parameters.IntegralBoxType == "Center Box":
                    self.IntegralBasicImage.axes.add_patch(Rectangle((self.parameters.IntegralMinBox + i * dx,0),
                                                                        dx,
                                                                        self.parameters.IntegralCurve(self.parameters.IntegralMinBox + (i + 0.5) * dx,
                                                                        self.parameters.IntegralParameters),
                                                                        alpha=0.3))                                                                        
        self.IntegralBasicImage.axes.axhline(y = 0, color = 'grey')
        self.IntegralBasicImage.axes.grid()
        self.IntegralBasicImage.axes.set_title(f"{self.parameters.IntegralCurveName}")

        self.IntegralBasicImage.draw()
###
class MplCanvas(FigureCanvasQTAgg):
    """Class for the images and the graphs as a widget"""
    def __init__(self, parent=None, width:float=5, height:float=4, dpi:int=75):
        """Creates an empty figure with axes and fig as parameters"""
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.fig = fig
        super(MplCanvas, self).__init__(fig)

if __name__ == "__main__":
    os.system('clear')
    print(f"Starting program at {time.strftime('%H:%M:%S')}")
    initial = time.time()
    app = QApplication([])
    window=CalculusWindow()
    window.show()
    sys.exit(app.exec())