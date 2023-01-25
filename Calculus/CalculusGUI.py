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
except:
    import Calculus.GUIParametersCalculus as GUIParametersCalculus
###
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.image as mpimg
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
        self.IntegralCurveType.addItem("Flat")
        self.IntegralCurveType.addItem("Line")
        self.IntegralCurveType.addItem("Quadratic")
        self.IntegralCurveType.addItem("Cubic")
        self.IntegralCurveType.activated[str].connect(self.update_Combo_CurveIntegral)

        self.FirstParameterIntegral = QLineEdit()
        self.SecondParameterIntegral = QLineEdit()
        self.ThirdParameterIntegral = QLineEdit()
        self.FourthParameterIntegral = QLineEdit()

        self.FirstParameterIntegral.setFixedWidth(90)
        self.SecondParameterIntegral.setFixedWidth(90)
        self.ThirdParameterIntegral.setFixedWidth(90)
        self.FourthParameterIntegral.setFixedWidth(90)

        self.FirstParameterIntegral.setText(str(self.parameters.IntegralFirstParam))
        self.SecondParameterIntegral.setText(str(self.parameters.IntegralSecondParam))
        self.ThirdParameterIntegral.setText(str(self.parameters.IntegralThirdParam))
        self.FourthParameterIntegral.setText(str(self.parameters.IntegralFourthParam))

        self.FirstParameterIntegral.editingFinished.connect(self.updateCurveParametersIntegral)
        self.SecondParameterIntegral.editingFinished.connect(self.updateCurveParametersIntegral)
        self.ThirdParameterIntegral.editingFinished.connect(self.updateCurveParametersIntegral)
        self.FourthParameterIntegral.editingFinished.connect(self.updateCurveParametersIntegral)

        layout.addWidget(self.IntegralCurveType,0,0)
        layout.addWidget(QLabel("First param."),1,0)
        layout.addWidget(self.FirstParameterIntegral,1,1)
        layout.addWidget(QLabel("Second param."),2,0)
        layout.addWidget(self.SecondParameterIntegral,2,1)
        layout.addWidget(QLabel("Third param."),3,0)
        layout.addWidget(self.ThirdParameterIntegral,3,1)
        layout.addWidget(QLabel("Fourth param."),4,0)
        layout.addWidget(self.FourthParameterIntegral,4,1)

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
        self.parameters.IntegralCurve = self.IntegralCurveType.currentText()

        self.updateCurveIntegral()

    def updateCurveParametersIntegral(self):
        """Updates the Parameters of the Curve"""
        try:
            self.parameters.IntegralFirstParam = float(self.FirstParameterIntegral.text())
        except:
            self.parameters.IntegralFirstParam = 1.0
        try:
            self.parameters.IntegralSecondParam = float(self.SecondParameterIntegral.text())
        except:
            self.parameters.IntegralSecondParam = 1.0
        try:
            self.parameters.IntegralThirdParam = float(self.ThirdParameterIntegral.text())
        except:
            self.parameters.IntegralThirdParam = 1.0
        try:
            self.parameters.IntegralFourthParam = float(self.FourthParameterIntegral.text())
        except:
            self.parameters.IntegralFourthParam = 1.0

        self.updateCurveIntegral()

    def updateCurveIntegral(self):
        """Updates the Base Curve"""
        if self.parameters.IntegralCurve == "Flat":
            self.parameters.IntegralYAxis = np.ones_like(self.parameters.IntegralXAxis) * self.parameters.IntegralFirstParam
        elif self.parameters.IntegralCurve == "Line":
            self.parameters.IntegralYAxis = self.parameters.IntegralXAxis * self.parameters.IntegralFirstParam + self.parameters.IntegralSecondParam
        elif self.parameters.IntegralCurve == "Quadratic":
            self.parameters.IntegralYAxis = (self.parameters.IntegralXAxis)**2 * self.parameters.IntegralFirstParam + \
                                                self.parameters.IntegralXAxis*self.parameters.IntegralSecondParam + \
                                                self.parameters.IntegralThirdParam
        elif self.parameters.IntegralCurve == "Cubic":
            self.parameters.IntegralYAxis = (self.parameters.IntegralXAxis)**3 * self.parameters.IntegralFirstParam + \
                                                (self.parameters.IntegralXAxis)**2 * self.parameters.IntegralSecondParam + \
                                                self.parameters.IntegralXAxis * self.parameters.IntegralThirdParam + \
                                                self.parameters.IntegralFourthParam

        self.updateBaseImageIntegral()

    def updateBaseImageIntegral(self):
        """Updates the Base Curve"""
        try:
            self.IntegralBasicImage.axes.cla()
        except:
            pass

        self.IntegralBasicImage.axes.plot(self.parameters.IntegralXAxis,self.parameters.IntegralYAxis)

        self.IntegralBasicImage.axes.grid()
        self.IntegralBasicImage.axes.set_title(f"{self.parameters.IntegralCurve}")

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