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
    import Integration
    import CalculusStrings
except:
    import Calculus.GUIParametersCalculus as GUIParametersCalculus
    import Calculus.Curves as Curves
    import Calculus.Integration as Integration
    import Calculus.CalculusStrings as CalculusStrings
###
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon

###
import markdown

size_Image = 200

class CalculusWindow(QMainWindow):
    """
    Main window of the GUI.
    """    
    def __init__(self,parent=None,language = "Fr"):
        """Initializes the GUI Window"""
        self.parameters = GUIParametersCalculus.GUIParameters()
        self.tabs = QTabWidget()
        self.current_lineDerivatives = 1
        self.current_lineIntegral = 1
        super().__init__(parent=parent)
        self.setMinimumSize(1200, 700)
        self.language = language
        self.setWindowTitle(CalculusStrings.WindowName[f"{self.language}"])

        self.generalLayoutDerivatives = QGridLayout()
        self.generalLayoutIntegral = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()

        centralWidgetDerivatives = QWidget(self)
        centralWidgetIntegral = QWidget(self)
        centralWidgetReadMe = QWidget(self)

        centralWidgetDerivatives.setLayout(self.generalLayoutDerivatives)
        centralWidgetIntegral.setLayout(self.generalLayoutIntegral)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)

        self.tabs.addTab(centralWidgetDerivatives,CalculusStrings.DerivativeTab[f"{self.language}"])
        self.tabs.addTab(centralWidgetIntegral,CalculusStrings.IntegralTab[f"{self.language}"])
        self.tabs.addTab(centralWidgetReadMe,CalculusStrings.ReadMeName[f"{self.language}"])

        self.setCentralWidget(self.tabs)
        ### Derivatives
        self._createCurveBaseDerivatives()
        self._createOptionsDerivatives()
        self._createCursonButton()
        self._createCurveLimitDerivatives()
        self._createCurveDerivedDerivatives()
        ### Integrals
        self._createCurveBaseIntegral()
        self._createOptionsIntegral()
        self._createCurveSumIntegral()
        self._createCurveOtherIntegral()

        self._createExitButton() 
        self.generalLayoutDerivatives.setColumnStretch(1,5)
        self.generalLayoutDerivatives.setColumnStretch(2,5)
        self.generalLayoutIntegral.setColumnStretch(1,5)
        self.generalLayoutIntegral.setColumnStretch(2,5)

    def _createCurveBaseDerivatives(self):
        """Creates an Image for a basic curve for the Derivatives"""
        self.DerivativesBasicImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutDerivatives.addWidget(self.DerivativesBasicImage,self.current_lineDerivatives,1)

        self.updateBaseImageDerivatives()
    def _createCursonButton(self):
        """Creates the cursor button for the position of the derivative"""
        subWidget = QWidget()
        layout = QHBoxLayout()
        subWidget.setLayout(layout)

        sizeText = 45

        self.sliderPositionCursorDerivatives = QSlider(Qt.Horizontal)
        self.lineEditPositionCursorDerivatives = QLineEdit()

        self.lineEditPositionCursorDerivatives.setFixedWidth(sizeText)
        self.lineEditPositionCursorDerivatives.setText(str(self.parameters.DerivativesCursorValue))

        self.sliderPositionCursorDerivatives.setMinimum(0)
        self.sliderPositionCursorDerivatives.setMaximum(int((self.parameters.DerivativesXAxisBounds[1] - self.parameters.DerivativesXAxisBounds[0]) * 100))
        self.sliderPositionCursorDerivatives.setSliderPosition(int(self.parameters.DerivativesCursorValue * (self.parameters.DerivativesXAxisBounds[1] - self.parameters.DerivativesXAxisBounds[0]) + (self.parameters.DerivativesXAxisBounds[1] - self.parameters.DerivativesXAxisBounds[0]) * 100/2))
        self.sliderPositionCursorDerivatives.setTickPosition(QSlider.TicksBothSides)
        self.sliderPositionCursorDerivatives.setSingleStep(1000)
        self.sliderPositionCursorDerivatives.setTickInterval(1000)

        self.lineEditPositionCursorDerivatives.editingFinished.connect(self.updateLineEditCursorDerivative)
        self.sliderPositionCursorDerivatives.valueChanged.connect(self.updateSliderCursorDerivative)

        layout.addWidget(self.lineEditPositionCursorDerivatives)
        layout.addWidget(self.sliderPositionCursorDerivatives)

        self.generalLayoutDerivatives.addWidget(subWidget,self.current_lineDerivatives,1)
        self.current_lineDerivatives += 1
    def _createOptionsDerivatives(self):
        """Creates the docks for the options of the Derivatives"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.TypeCurveDerivativesBox = QComboBox()
        for _, names in CalculusStrings.ButtonChoiceFunction.items():
            self.TypeCurveDerivativesBox.addItem(names[f"{self.language}"])
        self.TypeCurveDerivativesBox.setCurrentText(CalculusStrings.ButtonChoiceFunction[self.parameters.DerivativesCurveName][self.language])
        self.TypeCurveDerivativesBox.activated[str].connect(self.updateComboTypeCurveDerivatives)
        self.TypeDerivativeDerivativesBox = QComboBox()
        for _, names in CalculusStrings.SideDerivativesFunction.items():
            self.TypeDerivativeDerivativesBox.addItem(names[f"{self.language}"])
        self.TypeDerivativeDerivativesBox.setCurrentText(CalculusStrings.SideDerivativesFunction[self.parameters.DerivativesTypeName][self.language])
        self.TypeDerivativeDerivativesBox.activated[str].connect(self.updateComboTypeApproachDerivatives)

        self.FirstParameterDerivatives = QLineEdit()
        self.SecondParameterDerivatives = QLineEdit()
        self.ThirdParameterDerivatives = QLineEdit()
        self.FourthParameterDerivatives = QLineEdit()
        self.DerivativesH = QLineEdit()
        self.DerivativesMin = QLineEdit()
        self.DerivativesMax = QLineEdit()

        self.FirstParameterDerivatives.setFixedWidth(90)
        self.SecondParameterDerivatives.setFixedWidth(90)
        self.ThirdParameterDerivatives.setFixedWidth(90)
        self.FourthParameterDerivatives.setFixedWidth(90)
        self.DerivativesH.setFixedWidth(90)
        self.DerivativesMin.setFixedWidth(90)
        self.DerivativesMax.setFixedWidth(90)

        self.FirstParameterDerivatives.setText(str(self.parameters.DerivativesParameters[0]))
        self.SecondParameterDerivatives.setText(str(self.parameters.DerivativesParameters[1]))
        self.ThirdParameterDerivatives.setText(str(self.parameters.DerivativesParameters[2]))
        self.FourthParameterDerivatives.setText(str(self.parameters.DerivativesParameters[3]))
        self.DerivativesH.setText(str(self.parameters.DerivativesHValue))
        self.DerivativesMin.setText(str(self.parameters.DerivativesXAxisBounds[0]))
        self.DerivativesMax.setText(str(self.parameters.DerivativesXAxisBounds[1]))

        self.FirstParameterDerivatives.editingFinished.connect(self.updateCurveParametersDerivatives)
        self.SecondParameterDerivatives.editingFinished.connect(self.updateCurveParametersDerivatives)
        self.ThirdParameterDerivatives.editingFinished.connect(self.updateCurveParametersDerivatives)
        self.FourthParameterDerivatives.editingFinished.connect(self.updateCurveParametersDerivatives)
        self.DerivativesH.editingFinished.connect(self.updateHValueDerivatives)
        self.DerivativesMin.editingFinished.connect(self.updateCurveBoundsDerivatives)
        self.DerivativesMax.editingFinished.connect(self.updateCurveBoundsDerivatives)

        layout.addWidget(self.TypeCurveDerivativesBox,0,1)
        layout.addWidget(self.TypeDerivativeDerivativesBox,0,2)
        layout.addWidget(QLabel(CalculusStrings.ParametersLabel[f"{self.language}"]),1,0)
        layout.addWidget(self.FirstParameterDerivatives,1,1)
        layout.addWidget(self.SecondParameterDerivatives,1,2)
        layout.addWidget(self.ThirdParameterDerivatives,2,1)
        layout.addWidget(self.FourthParameterDerivatives,2,2)
        layout.addWidget(QLabel(CalculusStrings.hDerivatives[f"{self.language}"]),3,0)
        layout.addWidget(self.DerivativesH,3,1)
        layout.addWidget(QLabel(CalculusStrings.BoundsLabel[f"{self.language}"]),4,0)
        layout.addWidget(self.DerivativesMin,4,1)
        layout.addWidget(self.DerivativesMax,4,2)

        self.generalLayoutDerivatives.addWidget(subWidget,self.current_lineDerivatives,2)
        self.current_lineDerivatives += 1
    def _createCurveLimitDerivatives(self):
        """Creates an Image for the limit in derivatives"""
        self.LimitDerivativesImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutDerivatives.addWidget(self.LimitDerivativesImage,self.current_lineDerivatives,1)
        self.updateLimitImageDerivatives()
    def _createCurveDerivedDerivatives(self):
        """Creates the derivative of the function Image"""
        self.DerivativesDerivedImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutDerivatives.addWidget(self.DerivativesDerivedImage,self.current_lineDerivatives,2)
        self.current_lineDerivatives += 1
        self.updateDerivedImageDerivatives()

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
        self.IntegralCurveType.addItem("Exp. Power")
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
        self.IntegralBoxTypeCombo.addItem("Trapezoid")
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
        self.IntegralMin.setText(str(self.parameters.IntegralBoundsBox[0]))
        self.IntegralMax.setText(str(self.parameters.IntegralBoundsBox[1]))

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
        layout.addWidget(QLabel(CalculusStrings.ParametersLabel[f"{self.language}"]),1,0)
        layout.addWidget(self.FirstParameterIntegral,1,1)
        layout.addWidget(self.SecondParameterIntegral,1,2)
        layout.addWidget(self.ThirdParameterIntegral,2,1)
        layout.addWidget(self.FourthParameterIntegral,2,2)
        layout.addWidget(QLabel(CalculusStrings.BoxesLabel[f"{self.language}"]),3,0)
        layout.addWidget(self.ShowBoxIntegral,3,1)        
        layout.addWidget(self.NumberBoxIntegral,3,2)
        layout.addWidget(QLabel(CalculusStrings.BoundsLabel[f"{self.language}"]),4,0)
        layout.addWidget(self.IntegralMin,4,1)
        layout.addWidget(self.IntegralMax,4,2)

        self.generalLayoutIntegral.addWidget(subWidget,self.current_lineIntegral,2)
        self.current_lineIntegral += 1


    def _createCurveSumIntegral(self):
        """Creates an Image for the Integral Result"""
        self.IntegralSumImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutIntegral.addWidget(self.IntegralSumImage,self.current_lineIntegral,1)

        self.updateBoxImageIntegral()
    def _createCurveOtherIntegral(self):
        """Creates another Image"""
        self.IntegralOtherImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutIntegral.addWidget(self.IntegralOtherImage,self.current_lineIntegral,2)
        self.current_lineIntegral += 1
        self.updateBoundedImageIntegral()



    def _createExitButton(self):
        """Creates an exit button"""
        self.exitDerivatives = QPushButton(CalculusStrings.ExitLabel[f"{self.language}"])
        self.exitIntegral = QPushButton(CalculusStrings.ExitLabel[f"{self.language}"])
        self.exitDerivatives.setToolTip(CalculusStrings.ExitButtonTooltip[f"{self.language}"])
        self.exitIntegral.setToolTip(CalculusStrings.ExitButtonTooltip[f"{self.language}"])
        self.exitDerivatives.clicked.connect(self.close)
        self.exitIntegral.clicked.connect(self.close)
        self.generalLayoutDerivatives.addWidget(self.exitDerivatives,self.current_lineDerivatives+1,3)  
        self.generalLayoutIntegral.addWidget(self.exitIntegral,self.current_lineIntegral+1,3)  
        self.current_lineIntegral += 1
        self.current_lineDerivatives += 1
################################
    def updateLineEditCursorDerivative(self):
        """Updates the value of the cursor with the cursor"""
        try:
            self.parameters.DerivativesCursorValue = float(self.lineEditPositionCursorDerivatives.text())
        except:
            self.parameters.DerivativesCursorValue = 0.0
        self.updateAllDerivatives()

    def updateSliderCursorDerivative(self):
        """Updates the value of the cursor with the slider"""
        try:
            self.parameters.DerivativesCursorValue = self.sliderPositionCursorDerivatives.value()/100 + self.parameters.DerivativesXAxisBounds[0]
        except:
            self.parameters.DerivativesCursorValue = 0.0
        self.lineEditPositionCursorDerivatives.setText(f"{(self.sliderPositionCursorDerivatives.value()/100 + self.parameters.DerivativesXAxisBounds[0]):.2g}")

        self.updateAllDerivatives()

    def updateComboTypeCurveDerivatives(self):
        """Updates the Type of Curve for the Derivatives"""
        name_tmp = self.TypeCurveDerivativesBox.currentText()
        for dict, names in CalculusStrings.ButtonChoiceFunction.items():
            if name_tmp in names.values():
                self.parameters.DerivativesCurveName = dict
        self.updateAllDerivatives()

    def updateComboTypeApproachDerivatives(self):
        """Updates the Type of Tangent Line for the Derivatives"""
        name_tmp = self.TypeDerivativeDerivativesBox.currentText()
        for dict, names in CalculusStrings.SideDerivativesFunction.items():
            if name_tmp in names.values():
                self.parameters.DerivativesTypeName = dict
        self.updateAllDerivatives()

    def updateCurveBoundsDerivatives(self):
        """Updates the Bounds of the Derivatives"""
        try:
            self.parameters.DerivativesXAxisBounds[0] = float(self.DerivativesMin.text())
        except:
            self.parameters.DerivativesXAxisBounds[0] = 0.0
        try:
            self.parameters.DerivativesXAxisBounds[1] = float(self.DerivativesMax.text())
        except:
            self.parameters.DerivativesXAxisBounds[1] = 1.0
        self.sliderPositionCursorDerivatives.setMaximum(int((self.parameters.DerivativesXAxisBounds[1] - self.parameters.DerivativesXAxisBounds[0]) * 100))
        self.updateAllDerivatives()
    def updateHValueDerivatives(self):
        """Updates the h Value of the Derivatives"""
        try:
            self.parameters.DerivativesHValue = float(self.DerivativesH.text())
        except:
            self.parameters.DerivativesHValue = 1.0
        self.updateAllDerivatives()
    def updateCurveParametersDerivatives(self):
        """Updates the Parameters of the Derivatives Curve"""
        try:
            self.parameters.DerivativesParameters[0] = float(self.FirstParameterDerivatives.text())
        except:
            self.parameters.DerivativesParameters[0] = 1.0
        try:
            self.parameters.DerivativesParameters[1] = float(self.SecondParameterDerivatives.text())
        except:
            self.parameters.DerivativesParameters[1] = 1.0
        try:
            self.parameters.DerivativesParameters[2] = float(self.ThirdParameterDerivatives.text())
        except:
            self.parameters.DerivativesParameters[2] = 1.0
        try:
            self.parameters.DerivativesParameters[3] = float(self.FourthParameterDerivatives.text())
        except:
            self.parameters.DerivativesParameters[4] = 1.0

        self.updateAllDerivatives()

    def updateAllDerivatives(self):
        """Updates all aspect of the Derivatives Tab"""
        self.updateDerivativeCurves()
        self.updateBaseImageDerivatives()
        self.updateLimitImageDerivatives()
        self.updateDerivedImageDerivatives()
    
    def updateDerivativeCurves(self):
        """Updates the Derivatives Curves"""
        self.parameters.DerivativesXAxis = np.linspace(self.parameters.DerivativesXAxisBounds[0],self.parameters.DerivativesXAxisBounds[1],1000)
        if self.parameters.DerivativesCurveName == "Constant":
            self.parameters.DerivativesCurve = Curves.FlatCurve
        elif self.parameters.DerivativesCurveName == "Line":
            self.parameters.DerivativesCurve = Curves.LinearCurve
        elif self.parameters.DerivativesCurveName == "Quadratic":
            self.parameters.DerivativesCurve = Curves.QuadraticCurve
        elif self.parameters.DerivativesCurveName == "Cubic":
            self.parameters.DerivativesCurve = Curves.CubicCurve
        elif self.parameters.DerivativesCurveName == "Exponential":
            self.parameters.DerivativesCurve = Curves.ExponentialCurve
        elif self.parameters.DerivativesCurveName == "Exp. Power":
            self.parameters.DerivativesCurve = Curves.ExponentialPowerCurve
        elif self.parameters.DerivativesCurveName == "Sin":
            self.parameters.DerivativesCurve = Curves.SinCurve
        elif self.parameters.DerivativesCurveName == "Cos":
            self.parameters.DerivativesCurve = Curves.CosCurve
        elif self.parameters.DerivativesCurveName == "Tan":
            self.parameters.IntegralXAxis = self.IntegralXAxis = np.linspace(self.parameters.IntegralBoundsBox[0],self.parameters.IntegralBoundsBox[1],1000)
            self.parameters.DerivativesCurve = Curves.TanCurve
        elif self.parameters.DerivativesCurveName == "ArcSin":
            self.parameters.DerivativesCurve = Curves.ArcSinCurve
        elif self.parameters.DerivativesCurveName == "ArcCos":
            self.parameters.DerivativesCurve = Curves.ArcCosCurve
        elif self.parameters.DerivativesCurveName == "ArcTan":
            self.parameters.DerivativesCurve = Curves.ArcTanCurve        
        self.parameters.DerivativesYAxis = self.parameters.DerivativesCurve(self.parameters.DerivativesXAxis,self.parameters.DerivativesParameters)
        self.parameters.DerivativesDerivedYAxis = self.parameters.DerivativesCurve(self.parameters.DerivativesXAxis,self.parameters.DerivativesParameters,typeCurve = 'Derivative')
        self.parameters.DerivativesLeft = Curves.discreteDerivative(self.parameters.DerivativesCursorValue,
                                                            h = self.parameters.DerivativesHValue,
                                                            curve = self.parameters.DerivativesCurve,
                                                            parameters= self.parameters.DerivativesParameters,
                                                            side = "left")
        self.parameters.DerivativesBoth = Curves.discreteDerivative(self.parameters.DerivativesCursorValue,
                                                            h = self.parameters.DerivativesHValue,
                                                            curve = self.parameters.DerivativesCurve,
                                                            parameters= self.parameters.DerivativesParameters,
                                                            side = "both")
        self.parameters.DerivativesRight = Curves.discreteDerivative(self.parameters.DerivativesCursorValue,
                                                            h = self.parameters.DerivativesHValue,
                                                            curve = self.parameters.DerivativesCurve,
                                                            parameters= self.parameters.DerivativesParameters,
                                                            side = "right")

        self.parameters.DerivativesLeftRange = np.zeros(self.parameters.HValueRange.shape[0])
        self.parameters.DerivativesRightRange = np.zeros(self.parameters.HValueRange.shape[0])
        self.parameters.DerivativesBothRange = np.zeros(self.parameters.HValueRange.shape[0])
        for i in range(self.parameters.HValueRange.shape[0]):
            self.parameters.DerivativesLeftRange[i] = Curves.discreteDerivative(self.parameters.DerivativesCursorValue,
                                                            h = self.parameters.HValueRange[i],
                                                            curve = self.parameters.DerivativesCurve,
                                                            parameters= self.parameters.DerivativesParameters,
                                                            side = "left")[6]
            self.parameters.DerivativesRightRange[i] = Curves.discreteDerivative(self.parameters.DerivativesCursorValue,
                                                            h = self.parameters.HValueRange[i],
                                                            curve = self.parameters.DerivativesCurve,
                                                            parameters= self.parameters.DerivativesParameters,
                                                            side = "right")[6]
            self.parameters.DerivativesBothRange[i] = Curves.discreteDerivative(self.parameters.DerivativesCursorValue,
                                                            h = self.parameters.HValueRange[i],
                                                            curve = self.parameters.DerivativesCurve,
                                                            parameters= self.parameters.DerivativesParameters,
                                                            side = "both")[6]                                                            
    def updateBaseImageDerivatives(self):
        """Updates the Base Derivatives Curve"""
        try:
            self.DerivativesBasicImage.axes.cla()
        except:
            pass

        self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesXAxis,self.parameters.DerivativesYAxis)
        self.DerivativesBasicImage.axes.set_title(CalculusStrings.FunctionLabel[f"{self.language}"] + " " +
                                                    CalculusStrings.ButtonChoiceFunction[f"{self.parameters.DerivativesCurveName}"][f"{self.language}"] +  
                                                    f" : y = {CalculusStrings.CurveEquation(self.parameters.DerivativesCurveName,self.parameters.DerivativesParameters)}")
        
        if self.parameters.DerivativesTypeName in ["Left","All"]:
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesLeft[0],self.parameters.DerivativesLeft[1],color = 'orange')
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesLeft[2],self.parameters.DerivativesLeft[4],'o',color = 'orange')
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesLeft[3],self.parameters.DerivativesLeft[5],'o',color = 'orange')
        if self.parameters.DerivativesTypeName in ["Right","All"]:
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesRight[0],self.parameters.DerivativesRight[1],color = 'red')
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesRight[2],self.parameters.DerivativesRight[4],'o',color = 'red')
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesRight[3],self.parameters.DerivativesRight[5],'o',color = 'red')
        if self.parameters.DerivativesTypeName in ["Middle","All"]:
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesBoth[0],self.parameters.DerivativesBoth[1],color = 'green')
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesBoth[2],self.parameters.DerivativesBoth[4],'o',color = 'green')
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesBoth[3],self.parameters.DerivativesBoth[5],'o',color = 'green')
        self.DerivativesBasicImage.axes.grid()
        try:
            self.DerivativesBasicImage.axes.set_ylim(np.min(self.parameters.DerivativesYAxis)-1,np.max(self.parameters.DerivativesYAxis)+1)
        except: pass
        self.DerivativesBasicImage.draw()
    def updateLimitImageDerivatives(self):
        """Updates the Limit Derivatives Curve"""
        try:
            self.LimitDerivativesImage.axes.cla()
        except:
            pass
        self.LimitDerivativesImage.axes.axvline(self.parameters.DerivativesHValue)
        self.LimitDerivativesImage.axes.axhline(self.parameters.DerivativesCurve(self.parameters.DerivativesCursorValue,self.parameters.DerivativesParameters,typeCurve = 'Derivative'),label=CalculusStrings.SideDerivativesFunction["Exact"][self.language])
        self.LimitDerivativesImage.axes.plot(self.parameters.HValueRange,self.parameters.DerivativesRightRange,label = CalculusStrings.SideDerivativesFunction["Right"][self.language])
        self.LimitDerivativesImage.axes.plot(self.parameters.HValueRange,self.parameters.DerivativesLeftRange,label = CalculusStrings.SideDerivativesFunction["Left"][self.language])
        self.LimitDerivativesImage.axes.plot(self.parameters.HValueRange,self.parameters.DerivativesBothRange,label = CalculusStrings.SideDerivativesFunction["Middle"][self.language])

        self.LimitDerivativesImage.axes.set_xlabel(CalculusStrings.hDerivatives[f"{self.language}"])
        self.LimitDerivativesImage.axes.set_ylabel(CalculusStrings.SlopeDerivatives[f"{self.language}"])
        self.LimitDerivativesImage.axes.set_title(CalculusStrings.SlopeTitleDerivatives[f"{self.language}"])
        self.LimitDerivativesImage.axes.legend()
        self.LimitDerivativesImage.axes.grid()
        self.LimitDerivativesImage.axes.invert_xaxis()
        try:
            self.LimitDerivativesImage.axes.set_ylim(np.min([self.parameters.DerivativesRightRange,self.parameters.DerivativesLeftRange,self.parameters.DerivativesBothRange])-1,np.max([self.parameters.DerivativesRightRange,self.parameters.DerivativesLeftRange,self.parameters.DerivativesBothRange])+1)
        except: pass
        self.LimitDerivativesImage.draw()

    def updateDerivedImageDerivatives(self):
        """Updates the Derived Derivatives Curve"""
        try:
            self.DerivativesDerivedImage.axes.cla()
        except:
            pass

        self.DerivativesDerivedImage.axes.axvline(self.parameters.DerivativesCursorValue)
        self.DerivativesDerivedImage.axes.plot(self.parameters.DerivativesXAxis,self.parameters.DerivativesDerivedYAxis)
        self.DerivativesDerivedImage.axes.set_title(CalculusStrings.DerivativeLabel[f"{self.language}"] + 
                                                    f" : y' = {CalculusStrings.CurveEquation(self.parameters.DerivativesCurveName,self.parameters.DerivativesParameters,operator= 'Derivative')}")

        self.DerivativesDerivedImage.axes.grid()
        self.DerivativesDerivedImage.axes.set_ylim(np.min(self.parameters.DerivativesDerivedYAxis)-1,np.max(self.parameters.DerivativesDerivedYAxis)+1)
        self.DerivativesDerivedImage.draw()

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
        self.updateBoxImageIntegral()
        self.updateBoundedImageIntegral()

    def updateCureBoundsIntegral(self):
        """Updates the Bounds of the Integration"""
        try:
            self.parameters.IntegralBoundsBox[0] = float(self.IntegralMin.text())
        except:
            self.parameters.IntegralBoundsBox[0] = 0.0
        try:
            self.parameters.IntegralBoundsBox[1] = float(self.IntegralMax.text())
        except:
            self.parameters.IntegralBoundsBox[1] = 1.0
        self.updateCurveIntegral()
        self.updateBoxImageIntegral()
        self.updateBoundedImageIntegral()


    def updateCurveIntegral(self):
        """Updates the Base Curve"""
        self.parameters.IntegralXAxis = self.IntegralXAxis = np.linspace(self.parameters.IntegralBoundsBox[0] - 1,self.parameters.IntegralBoundsBox[1] + 1,1000)
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
        elif self.parameters.IntegralCurveName == "Exp. Power":
            self.parameters.IntegralCurve = Curves.ExponentialPowerCurve
        elif self.parameters.IntegralCurveName == "Sin":
            self.parameters.IntegralCurve = Curves.SinCurve
        elif self.parameters.IntegralCurveName == "Cos":
            self.parameters.IntegralCurve = Curves.CosCurve
        elif self.parameters.IntegralCurveName == "Tan":
            self.parameters.IntegralXAxis = self.IntegralXAxis = np.linspace(self.parameters.IntegralBoundsBox[0],self.parameters.IntegralBoundsBox[1],1000)
            self.parameters.IntegralCurve = Curves.TanCurve
        elif self.parameters.IntegralCurveName == "ArcSin":
            self.parameters.IntegralCurve = Curves.ArcSinCurve
        elif self.parameters.IntegralCurveName == "ArcCos":
            self.parameters.IntegralCurve = Curves.ArcCosCurve
        elif self.parameters.IntegralCurveName == "ArcTan":
            self.parameters.IntegralCurve = Curves.ArcTanCurve        
        self.parameters.IntegralYAxis = self.parameters.IntegralCurve(self.parameters.IntegralXAxis,self.parameters.IntegralParameters)

        self.updateBaseImageIntegral()
        self.updateBoxImageIntegral()
        self.updateBoundedImageIntegral()

    def updateBaseImageIntegral(self):
        """Updates the Base Curve"""
        try:
            self.IntegralBasicImage.axes.cla()
        except:
            pass

        self.IntegralBasicImage.axes.plot(self.parameters.IntegralXAxis,self.parameters.IntegralYAxis)

        if self.parameters.IntegralShowBoxes:
            dx = (self.parameters.IntegralBoundsBox[1] - self.parameters.IntegralBoundsBox[0])/self.parameters.IntegralBoxNumber
            for i in range(self.parameters.IntegralBoxNumber):
                if self.parameters.IntegralBoxType == "Left Box":
                    self.IntegralBasicImage.axes.add_patch(Rectangle((self.parameters.IntegralBoundsBox[0] + i * dx,0),
                                                                        dx,
                                                                        self.parameters.IntegralCurve(self.parameters.IntegralBoundsBox[0] + i * dx,
                                                                        self.parameters.IntegralParameters),
                                                                        alpha=0.3))
                elif self.parameters.IntegralBoxType == "Right Box":
                    self.IntegralBasicImage.axes.add_patch(Rectangle((self.parameters.IntegralBoundsBox[0] + i * dx,0),
                                                                        dx,
                                                                        self.parameters.IntegralCurve(self.parameters.IntegralBoundsBox[0] + (i + 1) * dx,
                                                                        self.parameters.IntegralParameters),
                                                                        alpha=0.3))
                elif self.parameters.IntegralBoxType == "Center Box":
                    self.IntegralBasicImage.axes.add_patch(Rectangle((self.parameters.IntegralBoundsBox[0] + i * dx,0),
                                                                        dx,
                                                                        self.parameters.IntegralCurve(self.parameters.IntegralBoundsBox[0] + (i + 0.5) * dx,
                                                                        self.parameters.IntegralParameters),
                                                                        alpha=0.3))      
                elif self.parameters.IntegralBoxType == "Trapezoid":
                    x = [[self.parameters.IntegralBoundsBox[0] + i * dx,0],
                            [self.parameters.IntegralBoundsBox[0] + (i + 1) * dx,0],
                            [self.parameters.IntegralBoundsBox[0] + (i + 1) * dx,self.parameters.IntegralCurve(self.parameters.IntegralBoundsBox[0] + (i + 1) * dx, self.parameters.IntegralParameters)],
                            [self.parameters.IntegralBoundsBox[0] + i * dx,self.parameters.IntegralCurve(self.parameters.IntegralBoundsBox[0] + i * dx, self.parameters.IntegralParameters)]]
                    self.IntegralBasicImage.axes.add_patch(Polygon(x, alpha=0.3))                                                                     
        self.IntegralBasicImage.axes.axhline(y = 0, color = 'grey')
        if self.parameters.IntegralShowBoxes:
            self.IntegralBasicImage.axes.axvline(self.parameters.IntegralBoundsBox[0],color='g')
            self.IntegralBasicImage.axes.axvline(self.parameters.IntegralBoundsBox[1],color='g')
        self.IntegralBasicImage.axes.grid()
        self.IntegralBasicImage.axes.set_xlabel("x")
        self.IntegralBasicImage.axes.set_ylabel("f(x)")
        self.IntegralBasicImage.axes.set_title(f"{self.parameters.IntegralCurveName}: y = {CalculusStrings.CurveEquation(self.parameters.IntegralCurveName,self.parameters.IntegralParameters)}")

        self.IntegralBasicImage.draw()

    def updateBoxImageIntegral(self):
        """Updates the Box Image of the Integral"""
        try:
            self.IntegralSumImage.axes.cla()
        except:
            pass

        if self.parameters.IntegralShowBoxes:
            self.IntegralSumImage.axes.axvline(self.parameters.IntegralBoxNumber)

        boxRange = np.arange(1,100)
        self.IntegralSumImage.axes.plot(boxRange,
                            Integration.BoxedAreaRange(
                                boxRange, BoxType = "Left Box", Curve= self.parameters.IntegralCurve,
                                CurveParameters= self.parameters.IntegralParameters,
                                Boundaries= self.parameters.IntegralBoundsBox
                            ), label = 'Left Box'
        )
        self.IntegralSumImage.axes.plot(boxRange,
                            Integration.BoxedAreaRange(
                                boxRange, BoxType = "Right Box", Curve= self.parameters.IntegralCurve,
                                CurveParameters= self.parameters.IntegralParameters,
                                Boundaries= self.parameters.IntegralBoundsBox
                            ), label = 'Right Box'
        )
        self.IntegralSumImage.axes.plot(boxRange,
                            Integration.BoxedAreaRange(
                                boxRange, BoxType = "Center Box", Curve= self.parameters.IntegralCurve,
                                CurveParameters= self.parameters.IntegralParameters,
                                Boundaries= self.parameters.IntegralBoundsBox
                            ), label = 'Center Box'
        )
        self.IntegralSumImage.axes.plot(boxRange,
                            Integration.BoxedAreaRange(
                                boxRange, BoxType = "Trapezoid", Curve= self.parameters.IntegralCurve,
                                CurveParameters= self.parameters.IntegralParameters,
                                Boundaries= self.parameters.IntegralBoundsBox
                            ), label = 'Trapezoid'
        )
        self.IntegralSumImage.axes.axhline(
                                self.parameters.IntegralCurve(self.parameters.IntegralBoundsBox[1],self.parameters.IntegralParameters,typeCurve= 'Integral') -
                                self.parameters.IntegralCurve(self.parameters.IntegralBoundsBox[0],self.parameters.IntegralParameters,typeCurve= 'Integral'),
                                color = 'g', label='Exact Value')
        self.IntegralSumImage.axes.grid()
        self.IntegralSumImage.axes.legend(loc = 'upper right')
        self.IntegralSumImage.axes.set_xlabel("Box Number")
        self.IntegralSumImage.axes.set_ylabel("Total Area")
        self.IntegralSumImage.axes.set_title("Measured Area by Method of Integration and Number of Boxes")
        self.IntegralSumImage.axes.set_xscale("log")

        self.IntegralSumImage.draw()

    def updateBoundedImageIntegral(self):
        """Updates the Integral Curve"""
        try:
            self.IntegralOtherImage.axes.cla()
        except:
            pass

        self.IntegralOtherImage.axes.plot(self.parameters.IntegralXAxis,
                                        self.parameters.IntegralCurve(self.parameters.IntegralXAxis,
                                            self.parameters.IntegralParameters,typeCurve= 'Integral'))

        if self.parameters.IntegralShowBoxes:
            self.IntegralOtherImage.axes.axvline(self.parameters.IntegralBoundsBox[0],color='g')
            self.IntegralOtherImage.axes.axvline(self.parameters.IntegralBoundsBox[1],color='g')

        self.IntegralOtherImage.axes.axhline(y = 0, color = 'grey')

        self.IntegralOtherImage.axes.grid()
        self.IntegralOtherImage.axes.set_xlabel("x")
        self.IntegralOtherImage.axes.set_ylabel("F(x)")
        self.IntegralOtherImage.axes.set_title(f"Integral Function of {self.parameters.IntegralCurveName}")        
        self.IntegralOtherImage.draw()
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
    window=CalculusWindow()
    window.show()
    sys.exit(app.exec())