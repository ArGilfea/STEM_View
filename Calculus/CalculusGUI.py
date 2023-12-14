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
    import ParametricFunctions
    import Integration
    import CalculusStrings
except:
    import Calculus.GUIParametersCalculus as GUIParametersCalculus
    import Calculus.Curves as Curves
    import Calculus.ParametricFunctions as ParametricFunctions
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
import math
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
        self.current_lineVector = 1
        self.current_lineTaylor = 1
        self.current_linePolarFunctions = 1
        self.current_lineParametric2DFunctions = 1
        super().__init__(parent=parent)
        self.setMinimumSize(1200, 700)
        self.language = language
        self.setWindowTitle(CalculusStrings.WindowName[f"{self.language}"])

        self.generalLayoutDerivatives = QGridLayout()
        self.generalLayoutIntegral = QGridLayout()
        self.generalLayoutVector = QGridLayout()
        self.generalLayoutTaylor = QGridLayout()
        self.generalLayoutPolarFunctions = QGridLayout()
        self.generalLayoutParametric2DFunctions = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()

        centralWidgetDerivatives = QWidget(self)
        centralWidgetIntegral = QWidget(self)
        centralWidgetVector = QWidget(self)
        centralWidgetTaylor = QWidget(self)
        centralWidgetPolarFunctions = QWidget(self)
        centralWidgetParametric2DFunctions = QWidget(self)
        centralWidgetReadMe = QWidget(self)

        centralWidgetDerivatives.setLayout(self.generalLayoutDerivatives)
        centralWidgetIntegral.setLayout(self.generalLayoutIntegral)
        centralWidgetVector.setLayout(self.generalLayoutVector)
        centralWidgetTaylor.setLayout(self.generalLayoutTaylor)
        centralWidgetPolarFunctions.setLayout(self.generalLayoutPolarFunctions)
        centralWidgetParametric2DFunctions.setLayout(self.generalLayoutParametric2DFunctions)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)

        self.tabs.addTab(centralWidgetDerivatives,CalculusStrings.DerivativeTab[f"{self.language}"])
        self.tabs.addTab(centralWidgetIntegral,CalculusStrings.IntegralTab[f"{self.language}"])
        self.tabs.addTab(centralWidgetVector,CalculusStrings.VectorTab[f"{self.language}"])
        self.tabs.addTab(centralWidgetTaylor,CalculusStrings.TaylorTab[f"{self.language}"])
        self.tabs.addTab(centralWidgetPolarFunctions,CalculusStrings.PolarFunctionsTab[f"{self.language}"])
        self.tabs.addTab(centralWidgetParametric2DFunctions,CalculusStrings.Parametric2DFunctionsTab[f"{self.language}"])
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
        ### Vectors
        self._createVectorImage()
        self._createOptionsVector()
        ### Taylor
        self._createCurvesTaylor()
        self._createOptionsTaylor()
        self._createDifferenceTaylor()
        self._createConvergenceTaylor()
        ### Polar
        self._createPolarImage()
        self._createOptionsPolarFunctions()
        ### Parametric
        self._createParametric2DXY()
        self._createParametric2DY()
        self._createParametric2DX()
        self._createOptionsParametric2DFunctions()
        ### Exit
        self._createExitButton() 
        self.generalLayoutDerivatives.setColumnStretch(1,5)
        self.generalLayoutDerivatives.setColumnStretch(2,5)
        self.generalLayoutIntegral.setColumnStretch(1,5)
        self.generalLayoutIntegral.setColumnStretch(2,5)
        self.generalLayoutVector.setColumnStretch(1,5)
        self.generalLayoutVector.setColumnStretch(2,5)
        self.generalLayoutTaylor.setColumnStretch(1,5)
        self.generalLayoutTaylor.setColumnStretch(2,5)
        self.generalLayoutPolarFunctions.setColumnStretch(1,5)
        self.generalLayoutPolarFunctions.setColumnStretch(2,5)
        self.generalLayoutParametric2DFunctions.setColumnStretch(1,5)
        self.generalLayoutParametric2DFunctions.setColumnStretch(2,5)

    def _createCurveBaseDerivatives(self):
        """Creates an Image for a basic curve for the Derivatives"""
        self.DerivativesBasicImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.DerivativesBasicImage_cid = self.DerivativesBasicImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.DerivativesBasicImage))
        self.DerivativesBasicImage_cod = self.DerivativesBasicImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.DerivativesBasicImage))

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
        self.LimitDerivativesImage_cid = self.LimitDerivativesImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.LimitDerivativesImage))
        self.LimitDerivativesImage_cod = self.LimitDerivativesImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.LimitDerivativesImage))
        self.generalLayoutDerivatives.addWidget(self.LimitDerivativesImage,self.current_lineDerivatives,1)
        self.updateLimitImageDerivatives()
    def _createCurveDerivedDerivatives(self):
        """Creates the derivative of the function Image"""
        self.DerivativesDerivedImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.DerivativesDerivedImage_cid = self.DerivativesDerivedImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.DerivativesDerivedImage))
        self.DerivativesDerivedImage_cod = self.DerivativesDerivedImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.DerivativesDerivedImage))
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
        for _, names in CalculusStrings.ButtonChoiceFunction.items():
            self.IntegralCurveType.addItem(names[f"{self.language}"])
        self.IntegralCurveType.setCurrentText(CalculusStrings.ButtonChoiceFunction[self.parameters.DerivativesCurveName][self.language])
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
        self.IntegralMin.editingFinished.connect(self.updateCurveBoundsIntegral)
        self.IntegralMax.editingFinished.connect(self.updateCurveBoundsIntegral)

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
        self.IntegralSumImage_cid = self.IntegralSumImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.IntegralSumImage))
        self.IntegralSumImage_cod = self.IntegralSumImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.IntegralSumImage))


        self.generalLayoutIntegral.addWidget(self.IntegralSumImage,self.current_lineIntegral,1)

        self.updateBoxImageIntegral()
    def _createCurveOtherIntegral(self):
        """Creates another Image"""
        self.IntegralOtherImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutIntegral.addWidget(self.IntegralOtherImage,self.current_lineIntegral,2)
        self.current_lineIntegral += 1
        self.updateBoundedImageIntegral()

    def _createVectorImage(self):
        """Creates the Image for the Vectors"""
        self.VectorBaseImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.VectorBaseImage_cid = self.VectorBaseImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.VectorBaseImage))
        self.VectorBaseImage_cod = self.VectorBaseImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.VectorBaseImage))
        self.generalLayoutVector.addWidget(self.VectorBaseImage,self.current_lineVector,1)
        self.updateVectorImage()

    def _createOptionsVector(self):
        """Creates the docks for the options of the Vectors"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.Vector1ShowCheckBox = QCheckBox()
        self.Vector1ShowCheckBox.setChecked(self.parameters.ShowVector1)
        self.Vector1Component1CheckBox = QCheckBox()
        self.Vector1Component1CheckBox.setChecked(self.parameters.ShowComponents1Vector1)
        self.Vector1Component2CheckBox = QCheckBox()
        self.Vector1Component2CheckBox.setChecked(self.parameters.ShowComponents2Vector1)

        self.Vector1XComponentLineEdit = QLineEdit()
        self.Vector1YComponentLineEdit = QLineEdit()
        self.Vector1RComponentLineEdit = QLineEdit()
        self.Vector1ThetaComponentLineEdit = QLineEdit()

        self.Vector2ShowCheckBox = QCheckBox()
        self.Vector2ShowCheckBox.setChecked(self.parameters.ShowVector2)
        self.Vector2Component1CheckBox = QCheckBox()
        self.Vector2Component1CheckBox.setChecked(self.parameters.ShowComponents1Vector2)
        self.Vector2Component2CheckBox = QCheckBox()
        self.Vector2Component2CheckBox.setChecked(self.parameters.ShowComponents2Vector2)

        self.Vector2XComponentLineEdit = QLineEdit()
        self.Vector2YComponentLineEdit = QLineEdit()
        self.Vector2RComponentLineEdit = QLineEdit()
        self.Vector2ThetaComponentLineEdit = QLineEdit()

        self.Vector1XComponentLineEdit.setFixedWidth(90)
        self.Vector1YComponentLineEdit.setFixedWidth(90)
        self.Vector1RComponentLineEdit.setFixedWidth(90)
        self.Vector1ThetaComponentLineEdit.setFixedWidth(90)
        self.Vector2XComponentLineEdit.setFixedWidth(90)
        self.Vector2YComponentLineEdit.setFixedWidth(90)
        self.Vector2RComponentLineEdit.setFixedWidth(90)
        self.Vector2ThetaComponentLineEdit.setFixedWidth(90)

        self.Vector1XComponentLineEdit.setText(str(self.parameters.Vectors1[0]))
        self.Vector1YComponentLineEdit.setText(str(self.parameters.Vectors1[1]))
        self.Vector1RComponentLineEdit.setText(f"{self.parameters.Vectors1[2]:.2f}")
        self.Vector1ThetaComponentLineEdit.setText(f"{self.parameters.Vectors1[3]:.1f}")
        self.Vector2XComponentLineEdit.setText(str(self.parameters.Vectors2[0]))
        self.Vector2YComponentLineEdit.setText(str(self.parameters.Vectors2[1]))
        self.Vector2RComponentLineEdit.setText(f"{self.parameters.Vectors2[2]:.2f}")
        self.Vector2ThetaComponentLineEdit.setText(f"{self.parameters.Vectors2[3]:.1f}")

        self.VectorAdditionCheckBox = QCheckBox()
        self.VectorAdditionCheckBox.setChecked(self.parameters.VectorSum)
        self.VectorAdditionComponent1CheckBox = QCheckBox()
        self.VectorAdditionComponent1CheckBox.setChecked(self.parameters.VectorSumComponent1)
        self.VectorAdditionComponent2CheckBox = QCheckBox()
        self.VectorAdditionComponent2CheckBox.setChecked(self.parameters.VectorSumComponent2)
        self.VectorAdditionComposition1CheckBox = QCheckBox()
        self.VectorAdditionComposition1CheckBox.setChecked(self.parameters.VectorSumComposition1)
        self.VectorAdditionComposition2CheckBox = QCheckBox()
        self.VectorAdditionComposition2CheckBox.setChecked(self.parameters.VectorSumComposition2)

        self.Vector1ShowCheckBox.stateChanged.connect(self.updateParametersVectors)
        self.Vector1Component1CheckBox.stateChanged.connect(self.updateParametersVectors)
        self.Vector1Component2CheckBox.stateChanged.connect(self.updateParametersVectors)
        self.Vector2ShowCheckBox.stateChanged.connect(self.updateParametersVectors)
        self.Vector2Component1CheckBox.stateChanged.connect(self.updateParametersVectors)
        self.Vector2Component2CheckBox.stateChanged.connect(self.updateParametersVectors)
        self.Vector1XComponentLineEdit.editingFinished.connect(self.updateParametersVectors)
        self.Vector1YComponentLineEdit.editingFinished.connect(self.updateParametersVectors)
        self.Vector1RComponentLineEdit.editingFinished.connect(self.updateParametersPolarVectors)
        self.Vector1ThetaComponentLineEdit.editingFinished.connect(self.updateParametersPolarVectors)
        self.Vector2XComponentLineEdit.editingFinished.connect(self.updateParametersVectors)
        self.Vector2YComponentLineEdit.editingFinished.connect(self.updateParametersVectors)
        self.Vector2RComponentLineEdit.editingFinished.connect(self.updateParametersPolarVectors)
        self.Vector2ThetaComponentLineEdit.editingFinished.connect(self.updateParametersPolarVectors)
        self.VectorAdditionCheckBox.stateChanged.connect(self.updateParametersVectors)
        self.VectorAdditionComponent1CheckBox.stateChanged.connect(self.updateParametersVectors)
        self.VectorAdditionComponent2CheckBox.stateChanged.connect(self.updateParametersVectors)
        self.VectorAdditionComposition1CheckBox.stateChanged.connect(self.updateParametersVectors)
        self.VectorAdditionComposition2CheckBox.stateChanged.connect(self.updateParametersVectors)

        layout.addWidget(QLabel(CalculusStrings.Vector[f"{self.language}"]+" 1"),0,0)
        layout.addWidget(self.Vector1ShowCheckBox,0,1)
        layout.addWidget(QLabel(CalculusStrings.Components[f"{self.language}"]),0,2)
        layout.addWidget(self.Vector1Component1CheckBox,0,3)
        layout.addWidget(self.Vector1Component2CheckBox,0,4)
        layout.addWidget(QLabel(CalculusStrings.Cartesian[f"{self.language}"]),1,1)
        layout.addWidget(self.Vector1XComponentLineEdit,1,2)
        layout.addWidget(self.Vector1YComponentLineEdit,1,3)
        layout.addWidget(QLabel(CalculusStrings.Polar[f"{self.language}"]),2,1)
        layout.addWidget(self.Vector1RComponentLineEdit,2,2)
        layout.addWidget(self.Vector1ThetaComponentLineEdit,2,3)

        layout.addWidget(QLabel(CalculusStrings.Vector[f"{self.language}"]+" 2"),3,0)
        layout.addWidget(self.Vector2ShowCheckBox,3,1)
        layout.addWidget(QLabel(CalculusStrings.Components[f"{self.language}"]),3,2)
        layout.addWidget(self.Vector2Component1CheckBox,3,3)
        layout.addWidget(self.Vector2Component2CheckBox,3,4)
        layout.addWidget(QLabel(CalculusStrings.Cartesian[f"{self.language}"]),4,1)
        layout.addWidget(self.Vector2XComponentLineEdit,4,2)
        layout.addWidget(self.Vector2YComponentLineEdit,4,3)
        layout.addWidget(QLabel(CalculusStrings.Polar[f"{self.language}"]),5,1)
        layout.addWidget(self.Vector2RComponentLineEdit,5,2)
        layout.addWidget(self.Vector2ThetaComponentLineEdit,5,3)

        layout.addWidget(QLabel(CalculusStrings.VectorAddition[f"{self.language}"]),6,0)
        layout.addWidget(self.VectorAdditionCheckBox,6,1)
        layout.addWidget(QLabel(CalculusStrings.Components[f"{self.language}"]),6,2)
        layout.addWidget(self.VectorAdditionComponent1CheckBox,6,3)
        layout.addWidget(self.VectorAdditionComponent2CheckBox,6,4)
        layout.addWidget(QLabel(CalculusStrings.Parallelogram[f"{self.language}"]),7,0)
        layout.addWidget(self.VectorAdditionComposition1CheckBox,7,1)
        layout.addWidget(self.VectorAdditionComposition2CheckBox,7,2)


        self.generalLayoutVector.addWidget(subWidget,self.current_lineVector,2)
        self.current_lineVector += 1

    def _createCurvesTaylor(self):
        """Creates the Image for the Function and the Taylor approximation"""
        self.TaylorBaseImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.TaylorBaseImage_cid = self.TaylorBaseImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.TaylorBaseImage))
        self.TaylorBaseImage_cod = self.TaylorBaseImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.TaylorBaseImage))
        self.generalLayoutTaylor.addWidget(self.TaylorBaseImage,self.current_lineTaylor,1)
        #self.current_lineTaylor += 1

    def _createOptionsTaylor(self):
        """Creates the docks for the options of the Taylor Series"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.TaylorCurveType = QComboBox()
        for _, names in CalculusStrings.ButtonChoiceFunction.items():
            self.TaylorCurveType.addItem(names[f"{self.language}"])
        self.TaylorCurveType.setCurrentText(self.parameters.TaylorCurveName)
        self.TaylorCurveType.activated[str].connect(self.update_Combo_CurveTaylor)

        self.FirstParameterTaylor = QLineEdit()
        self.SecondParameterTaylor = QLineEdit()
        self.ThirdParameterTaylor = QLineEdit()
        self.FourthParameterTaylor = QLineEdit()
        self.CenterParameterTaylor = QLineEdit()
        self.PointOfInterestParameterTaylor = QLineEdit()
        self.DegreeParameterTaylor = QLineEdit()

        self.DegreeShowAllBoxTaylor = QCheckBox()
        
        self.TaylorMin = QLineEdit()
        self.TaylorMax = QLineEdit()

        self.FirstParameterTaylor.setFixedWidth(90)
        self.SecondParameterTaylor.setFixedWidth(90)
        self.ThirdParameterTaylor.setFixedWidth(90)
        self.FourthParameterTaylor.setFixedWidth(90)
        self.CenterParameterTaylor.setFixedWidth(90)
        self.PointOfInterestParameterTaylor.setFixedWidth(90)
        self.DegreeParameterTaylor.setFixedWidth(90)
        self.TaylorMin.setFixedWidth(90)
        self.TaylorMax.setFixedWidth(90)

        self.FirstParameterTaylor.setText(str(self.parameters.TaylorParameters[0]))
        self.SecondParameterTaylor.setText(str(self.parameters.TaylorParameters[1]))
        self.ThirdParameterTaylor.setText(str(self.parameters.TaylorParameters[2]))
        self.FourthParameterTaylor.setText(str(self.parameters.TaylorParameters[3]))
        self.CenterParameterTaylor.setText(str(self.parameters.TaylorCenter))
        self.PointOfInterestParameterTaylor.setText(str(self.parameters.TaylorXValue))
        self.DegreeParameterTaylor.setText(str(self.parameters.TaylorDegree))
        self.TaylorMin.setText(str(self.parameters.TaylorBounds[0]))
        self.TaylorMax.setText(str(self.parameters.TaylorBounds[1]))

        self.FirstParameterTaylor.editingFinished.connect(self.updateCurveParametersTaylor)
        self.SecondParameterTaylor.editingFinished.connect(self.updateCurveParametersTaylor)
        self.ThirdParameterTaylor.editingFinished.connect(self.updateCurveParametersTaylor)
        self.FourthParameterTaylor.editingFinished.connect(self.updateCurveParametersTaylor)
        self.CenterParameterTaylor.editingFinished.connect(self.updateCurveParametersTaylor)
        self.PointOfInterestParameterTaylor.editingFinished.connect(self.updateCurveParametersTaylor)
        self.DegreeParameterTaylor.editingFinished.connect(self.updateCurveParametersTaylor)
        self.DegreeShowAllBoxTaylor.stateChanged.connect(self.updateCurveParametersTaylor)
        self.TaylorMin.editingFinished.connect(self.updateCurveBoundsTaylor)
        self.TaylorMax.editingFinished.connect(self.updateCurveBoundsTaylor)

        layout.addWidget(QLabel(CalculusStrings.FunctionLabel[f"{self.language}"]),0,0)
        layout.addWidget(self.TaylorCurveType,0,1)
        layout.addWidget(QLabel(CalculusStrings.ParametersLabel[f"{self.language}"]),1,0)
        layout.addWidget(self.FirstParameterTaylor,1,1)
        layout.addWidget(self.SecondParameterTaylor,1,2)
        layout.addWidget(self.ThirdParameterTaylor,2,1)
        layout.addWidget(self.FourthParameterTaylor,2,2)
        layout.addWidget(QLabel(CalculusStrings.CenterTaylor[f"{self.language}"]),3,0)
        layout.addWidget(self.CenterParameterTaylor,3,2)
        layout.addWidget(QLabel(CalculusStrings.PointOfInterestTaylor[f"{self.language}"]),4,0)
        layout.addWidget(self.PointOfInterestParameterTaylor,4,2)
        layout.addWidget(QLabel(CalculusStrings.DegreeTaylor[f"{self.language}"]),5,0)
        layout.addWidget(self.DegreeParameterTaylor,5,1)
        layout.addWidget(QLabel(CalculusStrings.DegreeAllTaylor[f"{self.language}"]),6,0)
        layout.addWidget(self.DegreeShowAllBoxTaylor,6,1)
        layout.addWidget(QLabel(CalculusStrings.BoundsLabel[f"{self.language}"]),7,0)
        layout.addWidget(self.TaylorMin,7,1)
        layout.addWidget(self.TaylorMax,7,2)

        self.generalLayoutTaylor.addWidget(subWidget,self.current_lineTaylor,2)
        self.current_lineTaylor += 1

    def _createDifferenceTaylor(self):
        """Creates the Image for the Difference of the Taylor Series"""
        self.TaylorDifferenceImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.TaylorDifferenceImage_cid = self.TaylorDifferenceImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.TaylorDifferenceImage))
        self.TaylorDifferenceImage_cod = self.TaylorDifferenceImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.TaylorDifferenceImage))
        self.generalLayoutTaylor.addWidget(self.TaylorDifferenceImage,self.current_lineTaylor,1)
        #self.current_lineTaylor += 1

    def _createConvergenceTaylor(self):
        """Creates the Image for the Convergence of the Taylor Series"""
        self.TaylorConvergenceImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.TaylorConvergenceImage_cid = self.TaylorConvergenceImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.TaylorConvergenceImage))
        self.TaylorConvergenceImage_cod = self.TaylorConvergenceImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.TaylorConvergenceImage))
        self.generalLayoutTaylor.addWidget(self.TaylorConvergenceImage,self.current_lineTaylor,2)
        self.current_lineTaylor += 1
        self.updateImagesTaylor()

    def _createPolarImage(self):
        """Creates the Image for the Polar Curve"""
        self.PolarImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.PolarImage_cid = self.PolarImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.PolarImage))
        self.PolarImage_cod = self.PolarImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.PolarImage))
        self.generalLayoutPolarFunctions.addWidget(self.PolarImage,self.current_linePolarFunctions,1)
        self.updateImagePolarCurve()

    def _createOptionsPolarFunctions(self):
        """Creates the docks for the options of the Parametric 2D Functions"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.PolarCurveType = QComboBox()
        for _, names in CalculusStrings.ButtonChoiceFunction.items():
            self.PolarCurveType.addItem(names[f"{self.language}"])
        self.PolarCurveType.setCurrentText(self.parameters.PolarCurveName)
        self.PolarCurveType.activated[str].connect(self.update_Combo_CurvePolarFunctions)

        self.Parameter1Polar = QLineEdit()
        self.Parameter2Polar = QLineEdit()
        self.Parameter3Polar = QLineEdit()
        self.Parameter4Polar = QLineEdit()
        self.ParameterPolarBoundMin = QLineEdit()
        self.ParameterPolarBoundMax = QLineEdit()

        self.Parameter1Polar.setFixedWidth(90)
        self.Parameter2Polar.setFixedWidth(90)
        self.Parameter3Polar.setFixedWidth(90)
        self.Parameter4Polar.setFixedWidth(90)
        self.ParameterPolarBoundMin.setFixedWidth(90)
        self.ParameterPolarBoundMax.setFixedWidth(90)

        self.Parameter1Polar.setText(str(self.parameters.PolarCurveParameters[0]))
        self.Parameter2Polar.setText(str(self.parameters.PolarCurveParameters[1]))
        self.Parameter3Polar.setText(str(self.parameters.PolarCurveParameters[2]))
        self.Parameter4Polar.setText(str(self.parameters.PolarCurveParameters[3]))
        self.ParameterPolarBoundMin.setText(str(self.parameters.PolarPhiBounds[0]))
        self.ParameterPolarBoundMax.setText(str(self.parameters.PolarPhiBounds[1]))

        self.Parameter1Polar.editingFinished.connect(self.updateCurveParametersPolar)
        self.Parameter2Polar.editingFinished.connect(self.updateCurveParametersPolar)
        self.Parameter3Polar.editingFinished.connect(self.updateCurveParametersPolar)
        self.Parameter4Polar.editingFinished.connect(self.updateCurveParametersPolar)
        self.ParameterPolarBoundMin.editingFinished.connect(self.updateCurveParametersPolar)
        self.ParameterPolarBoundMax.editingFinished.connect(self.updateCurveParametersPolar)


        layout.addWidget(QLabel(CalculusStrings.Parametric2DFunctionTValueLabel[f"{self.language}"]),0,0)
        layout.addWidget(self.PolarCurveType,0,1)
        layout.addWidget(QLabel(CalculusStrings.ParametersLabel[f"{self.language}"]),1,0)
        layout.addWidget(self.Parameter1Polar,1,1)
        layout.addWidget(self.Parameter2Polar,1,2)
        layout.addWidget(self.Parameter3Polar,2,1)
        layout.addWidget(self.Parameter4Polar,2,2)
        layout.addWidget(QLabel(CalculusStrings.BoundsLabel[f"{self.language}"]),3,0)
        layout.addWidget(self.ParameterPolarBoundMin,3,1)
        layout.addWidget(self.ParameterPolarBoundMax,3,2)


        self.generalLayoutPolarFunctions.addWidget(subWidget,self.current_linePolarFunctions,2)
        self.current_linePolarFunctions += 1

    def _createParametric2DXY(self):
        """Creates the Image for the Convergence of the Taylor Series"""
        self.Parametric2DXYImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.Parametric2DXYImage_cid = self.Parametric2DXYImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.Parametric2DXYImage))
        self.Parametric2DXYImage_cod = self.Parametric2DXYImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.Parametric2DXYImage))
        self.generalLayoutParametric2DFunctions.addWidget(self.Parametric2DXYImage,self.current_lineParametric2DFunctions,1)
    def _createParametric2DY(self):
        """Creates the Image for the Convergence of the Taylor Series"""
        self.Parametric2DYImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.Parametric2DYImage_cid = self.Parametric2DYImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.Parametric2DYImage))
        self.Parametric2DYImage_cod = self.Parametric2DYImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.Parametric2DYImage))
        self.generalLayoutParametric2DFunctions.addWidget(self.Parametric2DYImage,self.current_lineParametric2DFunctions,2)
        self.current_lineParametric2DFunctions += 1
    def _createParametric2DX(self):
        """Creates the Image for the Convergence of the Taylor Series"""
        self.Parametric2DXImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.Parametric2DXImage_cid = self.Parametric2DXImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.Parametric2DXImage))
        self.Parametric2DXImage_cod = self.Parametric2DXImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.Parametric2DXImage))
        self.generalLayoutParametric2DFunctions.addWidget(self.Parametric2DXImage,self.current_lineParametric2DFunctions,1)
        self.updateImagesParametric2DFunctions()

    def _createOptionsParametric2DFunctions(self):
        """Creates the docks for the options of the Parametric 2D Functions"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.Parametric2DCurveTypeX = QComboBox()
        for _, names in CalculusStrings.Parametric2DFunctionNames.items():
            self.Parametric2DCurveTypeX.addItem(names[f"{self.language}"])
        self.Parametric2DCurveTypeX.setCurrentText(self.parameters.Parametric2DFunctionsXName)
        self.Parametric2DCurveTypeX.activated[str].connect(self.update_Combo_CurveParametric2DFunctions)

        self.Parametric2DCurveTypeY = QComboBox()
        for _, names in CalculusStrings.Parametric2DFunctionNames.items():
            self.Parametric2DCurveTypeY.addItem(names[f"{self.language}"])
        self.Parametric2DCurveTypeY.setCurrentText(self.parameters.Parametric2DFunctionsYName)
        self.Parametric2DCurveTypeY.activated[str].connect(self.update_Combo_CurveParametric2DFunctions)

        self.Parametric2DCurveSameType = QCheckBox()
        self.Parametric2DCurveSameType = QCheckBox()
        self.Parametric2DCurveSameType.setChecked(self.parameters.Parametric2DFunctionsSame)
        self.Parametric2DCurveSameType.stateChanged.connect(self.update_Combo_CurveParametric2DFunctions)

        self.ParameterTValueParametric2DFunctions = QLineEdit()
        self.Parameter00Parametric2DFunctions = QLineEdit()
        self.Parameter01Parametric2DFunctions = QLineEdit()
        self.Parameter02Parametric2DFunctions = QLineEdit()
        self.Parameter03Parametric2DFunctions = QLineEdit()
        self.Parameter10Parametric2DFunctions = QLineEdit()
        self.Parameter11Parametric2DFunctions = QLineEdit()
        self.Parameter12Parametric2DFunctions = QLineEdit()
        self.Parameter13Parametric2DFunctions = QLineEdit()
        self.ParameterBoundMinParametric2DFunctions = QLineEdit()
        self.ParameterBoundMaxParametric2DFunctions = QLineEdit()

        self.ParameterTValueParametric2DFunctions.setFixedWidth(90)
        self.Parameter00Parametric2DFunctions.setFixedWidth(90)
        self.Parameter01Parametric2DFunctions.setFixedWidth(90)
        self.Parameter02Parametric2DFunctions.setFixedWidth(90)
        self.Parameter03Parametric2DFunctions.setFixedWidth(90)
        self.Parameter10Parametric2DFunctions.setFixedWidth(90)
        self.Parameter11Parametric2DFunctions.setFixedWidth(90)
        self.Parameter12Parametric2DFunctions.setFixedWidth(90)
        self.Parameter13Parametric2DFunctions.setFixedWidth(90)
        self.ParameterBoundMinParametric2DFunctions.setFixedWidth(90)
        self.ParameterBoundMaxParametric2DFunctions.setFixedWidth(90)

        self.ParameterTValueParametric2DFunctions.setText(f"{(self.parameters.Parametric2DFunctionsTValue):.2f}")
        self.Parameter00Parametric2DFunctions.setText(str(self.parameters.Parametric2DFunctionsParameters[0,0]))
        self.Parameter01Parametric2DFunctions.setText(str(self.parameters.Parametric2DFunctionsParameters[0,1]))
        self.Parameter02Parametric2DFunctions.setText(str(self.parameters.Parametric2DFunctionsParameters[0,2]))
        self.Parameter03Parametric2DFunctions.setText(str(self.parameters.Parametric2DFunctionsParameters[0,3]))
        self.Parameter10Parametric2DFunctions.setText(str(self.parameters.Parametric2DFunctionsParameters[1,0]))
        self.Parameter11Parametric2DFunctions.setText(str(self.parameters.Parametric2DFunctionsParameters[1,1]))
        self.Parameter12Parametric2DFunctions.setText(str(self.parameters.Parametric2DFunctionsParameters[1,2]))
        self.Parameter13Parametric2DFunctions.setText(str(self.parameters.Parametric2DFunctionsParameters[1,3]))
        self.ParameterBoundMinParametric2DFunctions.setText(str(self.parameters.Parametric2DFunctionsTAxisBounds[0]))
        self.ParameterBoundMaxParametric2DFunctions.setText(str(self.parameters.Parametric2DFunctionsTAxisBounds[1]))

        self.ParameterTValueParametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)
        self.Parameter00Parametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)
        self.Parameter01Parametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)
        self.Parameter02Parametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)
        self.Parameter03Parametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)
        self.Parameter10Parametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)
        self.Parameter11Parametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)
        self.Parameter12Parametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)
        self.Parameter13Parametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)
        self.ParameterBoundMinParametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)
        self.ParameterBoundMaxParametric2DFunctions.editingFinished.connect(self.updateParametersParametric2DFunctions)


        layout.addWidget(QLabel(CalculusStrings.Parametric2DFunctionTValueLabel[f"{self.language}"]),0,0)
        layout.addWidget(self.ParameterTValueParametric2DFunctions,0,1)
        layout.addWidget(QLabel(CalculusStrings.FunctionLabel[f"{self.language}"]),1,0)
        layout.addWidget(self.Parametric2DCurveTypeX,1,1)
        layout.addWidget(self.Parametric2DCurveTypeY,1,2)
        layout.addWidget(self.Parametric2DCurveSameType,1,3)
        layout.addWidget(QLabel(CalculusStrings.ParametersLabel[f"{self.language}"] + " 1"),2,0)
        layout.addWidget(self.Parameter00Parametric2DFunctions,2,1)
        layout.addWidget(self.Parameter01Parametric2DFunctions,2,2)
        layout.addWidget(self.Parameter02Parametric2DFunctions,3,1)
        layout.addWidget(self.Parameter03Parametric2DFunctions,3,2)

        layout.addWidget(QLabel(CalculusStrings.ParametersLabel[f"{self.language}"] + " 2"),4,0)
        layout.addWidget(self.Parameter10Parametric2DFunctions,4,1)
        layout.addWidget(self.Parameter11Parametric2DFunctions,4,2)
        layout.addWidget(self.Parameter12Parametric2DFunctions,5,1)
        layout.addWidget(self.Parameter13Parametric2DFunctions,5,2)

        layout.addWidget(QLabel(CalculusStrings.BoundsLabel[f"{self.language}"]),6,0)
        layout.addWidget(self.ParameterBoundMinParametric2DFunctions,6,1)
        layout.addWidget(self.ParameterBoundMaxParametric2DFunctions,6,2)

        self.generalLayoutParametric2DFunctions.addWidget(subWidget,self.current_lineParametric2DFunctions,2)
        self.current_lineParametric2DFunctions += 1

    def _createExitButton(self):
        """Creates an exit button"""
        self.exitDerivatives = QPushButton(CalculusStrings.ExitLabel[f"{self.language}"])
        self.exitIntegral = QPushButton(CalculusStrings.ExitLabel[f"{self.language}"])
        self.exitVector = QPushButton(CalculusStrings.ExitLabel[f"{self.language}"])
        self.exitTaylor = QPushButton(CalculusStrings.ExitLabel[f"{self.language}"])
        self.exitPolarFunctions = QPushButton(CalculusStrings.ExitLabel[f"{self.language}"])
        self.exitParametric2DFunctions = QPushButton(CalculusStrings.ExitLabel[f"{self.language}"])
        self.exitDerivatives.setToolTip(CalculusStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitIntegral.setToolTip(CalculusStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitVector.setToolTip(CalculusStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitTaylor.setToolTip(CalculusStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitPolarFunctions.setToolTip(CalculusStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitParametric2DFunctions.setToolTip(CalculusStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitDerivatives.setShortcut("Ctrl+Shift+E")
        self.exitIntegral.setShortcut("Ctrl+Shift+E")
        self.exitVector.setShortcut("Ctrl+Shift+E")
        self.exitTaylor.setShortcut("Ctrl+Shift+E")
        self.exitPolarFunctions.setShortcut("Ctrl+Shift+E")
        self.exitParametric2DFunctions.setShortcut("Ctrl+Shift+E")
        self.exitDerivatives.clicked.connect(self.close)
        self.exitIntegral.clicked.connect(self.close)
        self.exitVector.clicked.connect(self.close)
        self.exitTaylor.clicked.connect(self.close)
        self.exitPolarFunctions.clicked.connect(self.close)
        self.exitParametric2DFunctions.clicked.connect(self.close)
        self.generalLayoutDerivatives.addWidget(self.exitDerivatives,self.current_lineDerivatives+1,3)  
        self.generalLayoutIntegral.addWidget(self.exitIntegral,self.current_lineIntegral+1,3)  
        self.generalLayoutVector.addWidget(self.exitVector,self.current_lineVector+1,3)  
        self.generalLayoutTaylor.addWidget(self.exitTaylor,self.current_lineTaylor+1,3)  
        self.generalLayoutPolarFunctions.addWidget(self.exitPolarFunctions,self.current_linePolarFunctions+1,3)  
        self.generalLayoutParametric2DFunctions.addWidget(self.exitParametric2DFunctions,self.current_lineParametric2DFunctions+1,3)  
        self.current_lineIntegral += 1
        self.current_lineDerivatives += 1
        self.current_lineVector += 1
        self.current_lineTaylor += 1
        self.current_linePolarFunctions += 1
        self.current_lineParametric2DFunctions += 1
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
            self.parameters.DerivativesXAxisBounds[0] = 0.001
        try:
            self.parameters.DerivativesXAxisBounds[1] = float(self.DerivativesMax.text())
        except:
            self.parameters.DerivativesXAxisBounds[1] = 1.0
        self.parameters.HValueRange = np.linspace(1e-5,np.abs(self.parameters.DerivativesXAxisBounds[1] - self.parameters.DerivativesXAxisBounds[0])/4,100)
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
        elif self.parameters.DerivativesCurveName == "Logarithmic":
            self.parameters.DerivativesCurve = Curves.LogarithmicCurve
        elif self.parameters.DerivativesCurveName == "Sin":
            self.parameters.DerivativesCurve = Curves.SinCurve
        elif self.parameters.DerivativesCurveName == "Cos":
            self.parameters.DerivativesCurve = Curves.CosCurve
        elif self.parameters.DerivativesCurveName == "Tan":
            self.parameters.DerivativesCurve = Curves.TanCurve
        elif self.parameters.DerivativesCurveName == "ArcSin":
            self.parameters.DerivativesCurve = Curves.ArcSinCurve
        elif self.parameters.DerivativesCurveName == "ArcCos":
            self.parameters.DerivativesCurve = Curves.ArcCosCurve
        elif self.parameters.DerivativesCurveName == "ArcTan":
            self.parameters.DerivativesCurve = Curves.ArcTanCurve  
        elif self.parameters.DerivativesCurveName == "Sinc":
            self.parameters.DerivativesCurve = Curves.Sinc   
        self.parameters.DerivativesYAxis = self.parameters.DerivativesCurve(self.parameters.DerivativesXAxis,self.parameters.DerivativesParameters)
        self.parameters.DerivativesDerivedYAxis = self.parameters.DerivativesCurve(self.parameters.DerivativesXAxis,self.parameters.DerivativesParameters,typeCurve = 'Derivative')
        self.parameters.DerivativesLeft = Curves.discreteDerivative(self.parameters.DerivativesCursorValue,
                                                            h = self.parameters.DerivativesHValue,
                                                            curve = self.parameters.DerivativesCurve,
                                                            parameters= self.parameters.DerivativesParameters,
                                                            side = "left",
                                                            imageRange= self.parameters.DerivativesXAxisBounds)
        self.parameters.DerivativesBoth = Curves.discreteDerivative(self.parameters.DerivativesCursorValue,
                                                            h = self.parameters.DerivativesHValue,
                                                            curve = self.parameters.DerivativesCurve,
                                                            parameters= self.parameters.DerivativesParameters,
                                                            side = "both",
                                                            imageRange= self.parameters.DerivativesXAxisBounds)
        self.parameters.DerivativesRight = Curves.discreteDerivative(self.parameters.DerivativesCursorValue,
                                                            h = self.parameters.DerivativesHValue,
                                                            curve = self.parameters.DerivativesCurve,
                                                            parameters= self.parameters.DerivativesParameters,
                                                            side = "right",
                                                            imageRange= self.parameters.DerivativesXAxisBounds)
        self.parameters.DerivativesCursorValueY = self.parameters.DerivativesCurve(self.parameters.DerivativesCursorValue,
                                                                        self.parameters.DerivativesParameters,
                                                                        typeCurve = 'Normal')
        derivativeExactValue = self.parameters.DerivativesCurve(self.parameters.DerivativesCursorValue,
                                                            self.parameters.DerivativesParameters,
                                                            typeCurve = 'Derivative')
        bValue = self.parameters.DerivativesCursorValueY - derivativeExactValue * self.parameters.DerivativesCursorValue
        #xArray = np.linspace(0.8*self.parameters.DerivativesXAxisBounds[0],0.8*self.parameters.DerivativesXAxisBounds[1],100)
        xArray = self.parameters.DerivativesBoth[0]
        self.parameters.DerivativeTangentExact = Curves.LinearCurve(x = xArray,
                                                                    param = np.array([derivativeExactValue,bValue]),
                                                                    typeCurve= "Normal")

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
        if self.parameters.DerivativesTypeName in ["Exact","All"]:
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesBoth[0],self.parameters.DerivativeTangentExact,color = 'black')
            self.DerivativesBasicImage.axes.plot(self.parameters.DerivativesCursorValue,self.parameters.DerivativesCursorValueY,'o',color = 'black')
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
        try: self.DerivativesDerivedImage.axes.set_ylim(np.min(self.parameters.DerivativesDerivedYAxis)-1,np.max(self.parameters.DerivativesDerivedYAxis)+1)
        except: pass
        self.DerivativesDerivedImage.draw()

    def update_Combo_CurveIntegral(self):
        """Updates the Curve Type"""
        name_tmp = self.IntegralCurveType.currentText()
        for dict, names in CalculusStrings.ButtonChoiceFunction.items():
            if name_tmp in names.values():
                self.parameters.IntegralCurveName = dict

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

    def updateCurveBoundsIntegral(self):
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
        self.parameters.IntegralXAxis = np.linspace(self.parameters.IntegralBoundsBox[0] - 1,self.parameters.IntegralBoundsBox[1] + 1,1000)
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
        elif self.parameters.IntegralCurveName == "Logarithmic":
            self.parameters.IntegralCurve = Curves.LogarithmicCurve
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
        elif self.parameters.IntegralCurveName == "Sinc":
            self.parameters.IntegralCurve = Curves.Sinc        
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
        self.IntegralBasicImage.axes.set_title(CalculusStrings.FunctionLabel[f"{self.language}"] + " " +
                                                    CalculusStrings.ButtonChoiceFunction[f"{self.parameters.IntegralCurveName}"][f"{self.language}"] +  
                                                    f" : y = {CalculusStrings.CurveEquation(self.parameters.IntegralCurveName,self.parameters.IntegralParameters)}")

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
                            ), label = CalculusStrings.SideDerivativesFunction["Left"][f"{self.language}"] + " " + CalculusStrings.BoxesLabel[f"{self.language}"]
        )
        self.IntegralSumImage.axes.plot(boxRange,
                            Integration.BoxedAreaRange(
                                boxRange, BoxType = "Right Box", Curve= self.parameters.IntegralCurve,
                                CurveParameters= self.parameters.IntegralParameters,
                                Boundaries= self.parameters.IntegralBoundsBox
                            ), label = CalculusStrings.SideDerivativesFunction["Right"][f"{self.language}"]+ " " + CalculusStrings.BoxesLabel[f"{self.language}"]
        )
        self.IntegralSumImage.axes.plot(boxRange,
                            Integration.BoxedAreaRange(
                                boxRange, BoxType = "Center Box", Curve= self.parameters.IntegralCurve,
                                CurveParameters= self.parameters.IntegralParameters,
                                Boundaries= self.parameters.IntegralBoundsBox
                            ), label = CalculusStrings.CenterLabel[f"{self.language}"]+ " " + CalculusStrings.BoxesLabel[f"{self.language}"]
        )
        self.IntegralSumImage.axes.plot(boxRange,
                            Integration.BoxedAreaRange(
                                boxRange, BoxType = "Trapezoid", Curve= self.parameters.IntegralCurve,
                                CurveParameters= self.parameters.IntegralParameters,
                                Boundaries= self.parameters.IntegralBoundsBox
                            ), label = CalculusStrings.TrapezoidLabel[f"{self.language}"]
        )
        self.IntegralSumImage.axes.axhline(
                                self.parameters.IntegralCurve(self.parameters.IntegralBoundsBox[1],self.parameters.IntegralParameters,typeCurve= 'Integral') -
                                self.parameters.IntegralCurve(self.parameters.IntegralBoundsBox[0],self.parameters.IntegralParameters,typeCurve= 'Integral'),
                                color = 'g', label= CalculusStrings.SideDerivativesFunction["Exact"][f"{self.language}"])
        self.IntegralSumImage.axes.grid()
        self.IntegralSumImage.axes.legend(loc = 'upper right')
        self.IntegralSumImage.axes.set_xlabel(CalculusStrings.BoxeNumberLabel[f"{self.language}"])
        self.IntegralSumImage.axes.set_ylabel(CalculusStrings.TotalAreaLabel[f"{self.language}"])
        self.IntegralSumImage.axes.set_title(CalculusStrings.MeasureAreaTitle[f"{self.language}"])
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
        self.IntegralOtherImage.axes.set_title(CalculusStrings.FunctionIntegralLabel[f"{self.language}"] + " " +
                                                    CalculusStrings.ButtonChoiceFunction[f"{self.parameters.IntegralCurveName}"][f"{self.language}"] +  
                                                    f" : y = {CalculusStrings.CurveEquation(self.parameters.IntegralCurveName,self.parameters.IntegralParameters)}")

        self.IntegralOtherImage.draw()
    def updateParametersPolarVectors(self):
        """Updates the Polar Parameters of the Vectors"""
        try:
            self.parameters.Vectors1[2] = float(self.Vector1RComponentLineEdit.text())
        except:
            self.parameters.Vectors1[2] = 1.0
        try:
            self.parameters.Vectors1[3] = float(self.Vector1ThetaComponentLineEdit.text())
        except:
            self.parameters.Vectors1[3] = 45.0
        try:
            self.parameters.Vectors2[2] = float(self.Vector2RComponentLineEdit.text())
        except:
            self.parameters.Vectors2[2] = 1.0
        try:
            self.parameters.Vectors2[3] = float(self.Vector2ThetaComponentLineEdit.text())
        except:
            self.parameters.Vectors2[3] = 135.0

        self.parameters.Vectors1[0] = self.parameters.Vectors1[2] * np.cos(self.parameters.Vectors1[3]*np.pi/180)
        self.parameters.Vectors1[1] = self.parameters.Vectors1[2] * np.sin(self.parameters.Vectors1[3]*np.pi/180)
        self.parameters.Vectors2[0] = self.parameters.Vectors2[2] * np.cos(self.parameters.Vectors2[3]*np.pi/180)
        self.parameters.Vectors2[1] = self.parameters.Vectors2[2] * np.sin(self.parameters.Vectors2[3]*np.pi/180)

        self.Vector1XComponentLineEdit.setText(f"{self.parameters.Vectors1[0]:.2f}")
        self.Vector1YComponentLineEdit.setText(f"{self.parameters.Vectors1[1]:.2f}")
        self.Vector2XComponentLineEdit.setText(f"{self.parameters.Vectors2[0]:.2f}")
        self.Vector2YComponentLineEdit.setText(f"{self.parameters.Vectors2[1]:.2f}")

        self.updateVectorImage()


    def updateParametersVectors(self):
        """Updates the Parameters of the Vectors"""
        if self.Vector1ShowCheckBox.isChecked():
            self.parameters.ShowVector1 = True
        else: 
            self.parameters.ShowVector1 = False
        if self.Vector1Component1CheckBox.isChecked():
            self.parameters.ShowComponents1Vector1 = True
        else: 
            self.parameters.ShowComponents1Vector1 = False
        if self.Vector1Component2CheckBox.isChecked():
            self.parameters.ShowComponents2Vector1 = True
        else: 
            self.parameters.ShowComponents2Vector1 = False

        if self.Vector2ShowCheckBox.isChecked():
            self.parameters.ShowVector2 = True
        else: 
            self.parameters.ShowVector2 = False
        if self.Vector2Component1CheckBox.isChecked():
            self.parameters.ShowComponents1Vector2 = True
        else: 
            self.parameters.ShowComponents1Vector2 = False
        if self.Vector2Component2CheckBox.isChecked():
            self.parameters.ShowComponents2Vector2 = True
        else: 
            self.parameters.ShowComponents2Vector2 = False

        try:
            self.parameters.Vectors1[0] = float(self.Vector1XComponentLineEdit.text())
        except:
            self.parameters.Vectors1[0] = 1.0
        try:
            self.parameters.Vectors1[1] = float(self.Vector1YComponentLineEdit.text())
        except:
            self.parameters.Vectors1[1] = 1.0
        try:
            self.parameters.Vectors2[0] = float(self.Vector2XComponentLineEdit.text())
        except:
            self.parameters.Vectors2[0] = 1.0
        try:
            self.parameters.Vectors2[1] = float(self.Vector2YComponentLineEdit.text())
        except:
            self.parameters.Vectors2[1] = 1.0
        if self.VectorAdditionCheckBox.isChecked():
            self.parameters.VectorSum = True
        else: 
            self.parameters.VectorSum = False
        if self.VectorAdditionComponent1CheckBox.isChecked():
            self.parameters.VectorSumComponent1 = True
        else: 
            self.parameters.VectorSumComponent1 = False
        if self.VectorAdditionComponent2CheckBox.isChecked():
            self.parameters.VectorSumComponent2 = True
        else: 
            self.parameters.VectorSumComponent2 = False
        if self.VectorAdditionComposition1CheckBox.isChecked():
            self.parameters.VectorSumComposition1 = True
        else: 
            self.parameters.VectorSumComposition1 = False
        if self.VectorAdditionComposition2CheckBox.isChecked():
            self.parameters.VectorSumComposition2 = True
        else: 
            self.parameters.VectorSumComposition2 = False

        self.parameters.Vectors1[2] = (self.parameters.Vectors1[0]**2 + self.parameters.Vectors1[1]**2)**(1/2)
        self.parameters.Vectors2[2] = (self.parameters.Vectors2[0]**2 + self.parameters.Vectors2[1]**2)**(1/2)
        self.parameters.Vectors1[3] = np.arctan2(self.parameters.Vectors1[1],self.parameters.Vectors1[0]) *180/np.pi
        self.parameters.Vectors2[3] = np.arctan2(self.parameters.Vectors2[1],self.parameters.Vectors2[0]) *180/np.pi

        self.Vector1RComponentLineEdit.setText(f"{self.parameters.Vectors1[2]:.2f}")
        self.Vector1ThetaComponentLineEdit.setText(f"{self.parameters.Vectors1[3]:.1f}")
        self.Vector2RComponentLineEdit.setText(f"{self.parameters.Vectors2[2]:.2f}")
        self.Vector2ThetaComponentLineEdit.setText(f"{self.parameters.Vectors2[3]:.1f}")
        
        self.updateVectorImage()

    def updateVectorImage(self):
        """Updates the Integral Curve"""
        try:
            self.VectorBaseImage.axes.cla()
        except:
            pass

        if self.parameters.ShowVector1:
            self.VectorBaseImage.axes.quiver(0,0,self.parameters.Vectors1[0],self.parameters.Vectors1[1], 
                                         angles='xy', scale_units='xy',scale = 1,color = 'blue')
        if self.parameters.ShowComponents1Vector1:
            self.VectorBaseImage.axes.plot([0, self.parameters.Vectors1[0]],[0, 0],
                                              color = 'blue', linestyle = '--')
            self.VectorBaseImage.axes.plot([self.parameters.Vectors1[0], self.parameters.Vectors1[0]],[0, self.parameters.Vectors1[1]],
                                              color = 'blue', linestyle = '--')
        if self.parameters.ShowComponents2Vector1:
            self.VectorBaseImage.axes.plot([0, 0],[0, self.parameters.Vectors1[1]],
                                              color = 'blue', linestyle = '--')
            self.VectorBaseImage.axes.plot([0, self.parameters.Vectors1[0]],[self.parameters.Vectors1[1], self.parameters.Vectors1[1]],
                                              color = 'blue', linestyle = '--')

        if self.parameters.ShowVector2:
            self.VectorBaseImage.axes.quiver(0,0,self.parameters.Vectors2[0],self.parameters.Vectors2[1], 
                                         angles='xy', scale_units='xy',scale = 1,color = 'red')
        if self.parameters.ShowComponents1Vector2:
            self.VectorBaseImage.axes.plot([0, self.parameters.Vectors2[0]],[0, 0],
                                              color = 'red', linestyle = '--')
            self.VectorBaseImage.axes.plot([self.parameters.Vectors2[0], self.parameters.Vectors2[0]],[0, self.parameters.Vectors2[1]],
                                              color = 'red', linestyle = '--')
        if self.parameters.ShowComponents2Vector2:
            self.VectorBaseImage.axes.plot([0, 0],[0, self.parameters.Vectors2[1]],
                                              color = 'red', linestyle = '--')
            self.VectorBaseImage.axes.plot([0, self.parameters.Vectors2[0]],[self.parameters.Vectors2[1], self.parameters.Vectors2[1]],
                                              color = 'red', linestyle = '--')

        if self.parameters.VectorSum:
            self.VectorBaseImage.axes.quiver(0,0,self.parameters.Vectors1[0]+self.parameters.Vectors2[0],
                                             self.parameters.Vectors1[1]+ self.parameters.Vectors2[1], 
                                            angles='xy', scale_units='xy',scale = 1,color = 'green')        
        if self.parameters.VectorSumComposition2:
            self.VectorBaseImage.axes.quiver(self.parameters.Vectors1[0],self.parameters.Vectors1[1],self.parameters.Vectors2[0],
                                             self.parameters.Vectors2[1], 
                                            angles='xy', scale_units='xy',scale = 1,color = 'black')     
        if self.parameters.VectorSumComposition1:
            self.VectorBaseImage.axes.quiver(self.parameters.Vectors2[0],self.parameters.Vectors2[1],self.parameters.Vectors1[0],
                                             self.parameters.Vectors1[1], 
                                            angles='xy', scale_units='xy',scale = 1,color = 'black')     

        if self.parameters.VectorSumComponent1:
            self.VectorBaseImage.axes.plot([0, self.parameters.Vectors1[0]+self.parameters.Vectors2[0]],[0, 0],
                                              color = 'green', linestyle = '--')
            self.VectorBaseImage.axes.plot([self.parameters.Vectors1[0]+self.parameters.Vectors2[0], self.parameters.Vectors1[0]+self.parameters.Vectors2[0]],
                                           [0, self.parameters.Vectors1[1]+self.parameters.Vectors2[1]],
                                              color = 'green', linestyle = '--')
        if self.parameters.VectorSumComponent2:
            self.VectorBaseImage.axes.plot([0, 0],[0, self.parameters.Vectors1[1]+self.parameters.Vectors2[1]],
                                              color = 'green', linestyle = '--')
            self.VectorBaseImage.axes.plot([0, self.parameters.Vectors1[0]+self.parameters.Vectors2[0]],
                                           [self.parameters.Vectors1[1]+self.parameters.Vectors2[1], self.parameters.Vectors1[1]+self.parameters.Vectors2[1]],
                                              color = 'green', linestyle = '--')

        self.VectorBaseImage.axes.axvline(0,color = 'black',alpha = 0.25)
        self.VectorBaseImage.axes.axhline(0,color = 'black',alpha = 0.25)

        self.VectorBaseImage.axes.set_xlim(min([-3,self.parameters.Vectors1[0]-1,self.parameters.Vectors2[0]-1,
                                                self.parameters.Vectors1[0]-self.parameters.Vectors2[0]-1]),
                                           max([3,self.parameters.Vectors1[0]+1,self.parameters.Vectors2[0]+1,
                                                self.parameters.Vectors1[0]+self.parameters.Vectors2[0]+1]))

        self.VectorBaseImage.axes.set_ylim(min([-3,self.parameters.Vectors1[1]-1,self.parameters.Vectors2[1]-1,
                                                self.parameters.Vectors1[1]-self.parameters.Vectors2[1]-1]),
                                           max([3,self.parameters.Vectors1[1]+1,self.parameters.Vectors2[1]+1,
                                                self.parameters.Vectors1[1]+self.parameters.Vectors2[1]+1]))
        


        self.VectorBaseImage.axes.grid()

        self.VectorBaseImage.draw()


    def update_Combo_CurveTaylor(self):
        """Updates the Curve Type"""
        name_tmp = self.TaylorCurveType.currentText()
        for dict, names in CalculusStrings.ButtonChoiceFunction.items():
            if name_tmp in names.values():
                self.parameters.TaylorCurveName = dict

        self.updateCurveTaylor()
    def updateCurveParametersTaylor(self):
        """Updates the Parameters of the Taylor Part"""
        try:
            self.parameters.TaylorParameters[0] = float(self.FirstParameterTaylor.text())
        except:
            self.parameters.TaylorParameters[0] = 1.0
        try:
            self.parameters.TaylorParameters[1] = float(self.SecondParameterTaylor.text())
        except:
            self.parameters.TaylorParameters[1] = 1.0
        try:
            self.parameters.TaylorParameters[2] = float(self.ThirdParameterTaylor.text())
        except:
            self.parameters.TaylorParameters[2] = 1.0
        try:
            self.parameters.TaylorParameters[3] = float(self.FourthParameterTaylor.text())
        except:
            self.parameters.TaylorParameters[3] = 1.0
        try:
            self.parameters.TaylorCenter = float(self.CenterParameterTaylor.text())
        except:
            self.parameters.TaylorCenter = 0.0
        try:
            self.parameters.TaylorXValue = float(self.PointOfInterestParameterTaylor.text())
        except:
            self.parameters.TaylorXValue = 0.0
        try:
            self.parameters.TaylorDegree = int(self.DegreeParameterTaylor.text())
        except:
            self.parameters.TaylorDegree = 1
        if self.DegreeShowAllBoxTaylor.isChecked():
            self.parameters.TaylorShowAll = True
        else: 
            self.parameters.TaylorShowAll = False
        self.updateCurveTaylor()
    def updateCurveBoundsTaylor(self):
        """Updates the Bounds of the Taylor Series"""
        try:
            self.parameters.TaylorBounds[0] = float(self.TaylorMin.text())
        except:
            self.parameters.TaylorBounds[0] = 0.0
        try:
            self.parameters.TaylorBounds[1] = float(self.TaylorMax.text())
        except:
            self.parameters.TaylorBounds[1] = 1.0
        self.updateCurveTaylor()
    def updateCurveTaylor(self):
        """Updates the Base Curve for the Taylor Series"""
        self.parameters.TaylorXAxis = np.linspace(self.parameters.TaylorBounds[0],self.parameters.TaylorBounds[1],1000)
        if self.parameters.TaylorCurveName == "Constant":
            self.parameters.TaylorCurve = Curves.FlatCurve
        elif self.parameters.TaylorCurveName == "Line":
            self.parameters.TaylorCurve = Curves.LinearCurve
        elif self.parameters.TaylorCurveName == "Quadratic":
            self.parameters.TaylorCurve = Curves.QuadraticCurve
        elif self.parameters.TaylorCurveName == "Cubic":
            self.parameters.TaylorCurve = Curves.CubicCurve
        elif self.parameters.TaylorCurveName == "Exponential":
            self.parameters.TaylorCurve = Curves.ExponentialCurve
        elif self.parameters.TaylorCurveName == "Exp. Power":
            self.parameters.TaylorCurve = Curves.ExponentialPowerCurve
        elif self.parameters.TaylorCurveName == "Logarithmic":
            self.parameters.TaylorCurve = Curves.LogarithmicCurve
        elif self.parameters.TaylorCurveName == "Sin":
            self.parameters.TaylorCurve = Curves.SinCurve
        elif self.parameters.TaylorCurveName == "Cos":
            self.parameters.TaylorCurve = Curves.CosCurve
        elif self.parameters.TaylorCurveName == "Tan":
            self.parameters.TaylorXAxis = np.linspace(self.parameters.TaylorBoundsBox[0],self.parameters.TaylorBoundsBox[1],1000)
            self.parameters.TaylorCurve = Curves.TanCurve
        elif self.parameters.TaylorCurveName == "ArcSin":
            self.parameters.TaylorCurve = Curves.ArcSinCurve
        elif self.parameters.TaylorCurveName == "ArcCos":
            self.parameters.TaylorCurve = Curves.ArcCosCurve
        elif self.parameters.TaylorCurveName == "ArcTan":
            self.parameters.TaylorCurve = Curves.ArcTanCurve   
        elif self.parameters.TaylorCurveName == "Sinc":
            self.parameters.TaylorCurve = Curves.Sinc        
        self.parameters.TaylorYAxis = self.parameters.TaylorCurve(self.parameters.TaylorXAxis,self.parameters.TaylorParameters)
        self.updateImagesTaylor()

    def updateImagesTaylor(self):
        """Updates all the Images for the Taylor Part"""
        self.updateBaseImageTaylor()
        self.updateDifferenceImageTaylor()
        self.updateConvergenceImageTaylor()

    def updateBaseImageTaylor(self):
        """Updates the Taylor Curve"""
        try:
            self.TaylorBaseImage.axes.cla()
        except:
            pass
        self.TaylorBaseImage.axes.plot(self.parameters.TaylorXAxis,
                                       self.parameters.TaylorYAxis,
                                       color = "b",
                                       label = "f(x)")

        if self.parameters.TaylorShowAll:
            TaylorCurveDegree = np.zeros_like(self.parameters.TaylorXAxis)
            for i in range(self.parameters.TaylorDegree):
                if i == 0:
                    TaylorCurveDegree += self.parameters.TaylorCurve(self.parameters.TaylorCenter,param = self.parameters.TaylorParameters,typeCurve="Normal",degree = i)*(self.parameters.TaylorXAxis-self.parameters.TaylorCenter)**(i)/(math.factorial(i))
                else:
                    TaylorCurveDegree += self.parameters.TaylorCurve(self.parameters.TaylorCenter,param = self.parameters.TaylorParameters,typeCurve="Derivative",degree = i)*(self.parameters.TaylorXAxis-self.parameters.TaylorCenter)**(i)/(math.factorial(i))
                self.TaylorBaseImage.axes.plot(self.parameters.TaylorXAxis,
                                       TaylorCurveDegree,
                                       label = f"T$_{{{i}}}$(x)")

        TaylorCurveDegree = np.zeros_like(self.parameters.TaylorXAxis)
        for i in range(self.parameters.TaylorDegree + 1):
            if i == 0:
                TaylorCurveDegree += self.parameters.TaylorCurve(self.parameters.TaylorCenter,param = self.parameters.TaylorParameters,typeCurve="Normal",degree = i)*(self.parameters.TaylorXAxis-self.parameters.TaylorCenter)**(i)/(math.factorial(i))
            else:
                TaylorCurveDegree += self.parameters.TaylorCurve(self.parameters.TaylorCenter,param = self.parameters.TaylorParameters,typeCurve="Derivative",degree = i)*(self.parameters.TaylorXAxis-self.parameters.TaylorCenter)**(i)/(math.factorial(i))
        self.TaylorBaseImage.axes.plot(self.parameters.TaylorXAxis,
                                       TaylorCurveDegree,
                                       color = "r",
                                       label = f"T$_{{{(self.parameters.TaylorDegree)}}}$(x)")
        self.TaylorBaseImage.axes.axvline(self.parameters.TaylorCenter,color = "grey", alpha = 0.5)
        self.TaylorBaseImage.axes.axvline(self.parameters.TaylorXValue,color = "brown", alpha = 0.5)
        self.TaylorBaseImage.axes.legend()
        self.TaylorBaseImage.axes.grid()
        self.TaylorBaseImage.axes.set_xlabel("x")
        self.TaylorBaseImage.axes.set_ylabel("y")
        self.TaylorBaseImage.axes.set_ylim(top = 2*max(self.parameters.TaylorYAxis)-0.1,bottom = 2*min(self.parameters.TaylorYAxis)+0.1)
        self.TaylorBaseImage.axes.set_title(CalculusStrings.GraphTitleTaylor[f"{self.language}"]+
                                            str(self.parameters.TaylorDegree) +
                                            "\n" + 
                                            f"f(x) = {CalculusStrings.CurveEquation(self.parameters.TaylorCurveName,self.parameters.TaylorParameters)}"+
                                            "\n" + CalculusStrings.GraphTitleTaylor2[f"{self.language}"]
                                            + f"{self.parameters.TaylorCenter:.2f}")
        self.TaylorBaseImage.draw()

    def updateDifferenceImageTaylor(self):
        """Updates the difference Image"""
        try:
            self.TaylorDifferenceImage.axes.cla()
        except:
            pass
        if self.parameters.TaylorShowAll:
            TaylorCurveDegree = np.zeros_like(self.parameters.TaylorXAxis)
            for i in range(self.parameters.TaylorDegree):
                if i == 0:
                    TaylorCurveDegree += self.parameters.TaylorCurve(self.parameters.TaylorCenter,param = self.parameters.TaylorParameters,typeCurve="Normal",degree = i)*(self.parameters.TaylorXAxis-self.parameters.TaylorCenter)**(i)/(math.factorial(i))
                else:
                    TaylorCurveDegree += self.parameters.TaylorCurve(self.parameters.TaylorCenter,param = self.parameters.TaylorParameters,typeCurve="Derivative",degree = i)*(self.parameters.TaylorXAxis-self.parameters.TaylorCenter)**(i)/(math.factorial(i))
                self.TaylorDifferenceImage.axes.plot(self.parameters.TaylorXAxis,
                                       self.parameters.TaylorYAxis - TaylorCurveDegree,
                                       label = f"T$_{{{i}}}$")

        TaylorCurveDegree = np.zeros_like(self.parameters.TaylorXAxis)
        for i in range(self.parameters.TaylorDegree + 1):
            if i == 0:
                TaylorCurveDegree += self.parameters.TaylorCurve(self.parameters.TaylorCenter,param = self.parameters.TaylorParameters,typeCurve="Normal",degree = i)*(self.parameters.TaylorXAxis-self.parameters.TaylorCenter)**(i)/(math.factorial(i))
            else:
                TaylorCurveDegree += self.parameters.TaylorCurve(self.parameters.TaylorCenter,param = self.parameters.TaylorParameters,typeCurve="Derivative",degree = i)*(self.parameters.TaylorXAxis-self.parameters.TaylorCenter)**(i)/(math.factorial(i))
        self.TaylorDifferenceImage.axes.plot(self.parameters.TaylorXAxis,
                                       self.parameters.TaylorYAxis - TaylorCurveDegree,
                                       color = "r",
                                       label = f"T$_{{{(self.parameters.TaylorDegree)}}}$")

        self.TaylorDifferenceImage.axes.axvline(self.parameters.TaylorCenter,color = "grey", alpha = 0.5)
        self.TaylorDifferenceImage.axes.axvline(self.parameters.TaylorXValue,color = "brown", alpha = 0.5)
        self.TaylorDifferenceImage.axes.legend()
        self.TaylorDifferenceImage.axes.grid()
        self.TaylorDifferenceImage.axes.set_xlabel("x")
        self.TaylorDifferenceImage.axes.set_ylabel(r"f(x) - T$_n$")
        self.TaylorDifferenceImage.axes.set_title(CalculusStrings.DifferenceGraphTitleTaylor[f"{self.language}"])
        self.TaylorDifferenceImage.draw()

    def updateConvergenceImageTaylor(self):
        """Updates the difference Image"""
        try:
            self.TaylorConvergenceImage.axes.cla()
        except:
            pass

        n_values = np.arange(15)
        T_n_values = np.zeros(n_values.shape[0])
        y_value = self.parameters.TaylorCurve(self.parameters.TaylorXValue,param = self.parameters.TaylorParameters,typeCurve="Normal")

        TaylorCurveDegree = 0
        for i in range(n_values.shape[0]):
            if i == 0:
                TaylorCurveDegree += self.parameters.TaylorCurve(self.parameters.TaylorCenter,param = self.parameters.TaylorParameters,typeCurve="Normal",degree = i)*(self.parameters.TaylorXValue-self.parameters.TaylorCenter)**(i)/(math.factorial(i))
            else:
                TaylorCurveDegree += self.parameters.TaylorCurve(self.parameters.TaylorCenter,param = self.parameters.TaylorParameters,typeCurve="Derivative",degree = i)*(self.parameters.TaylorXValue-self.parameters.TaylorCenter)**(i)/(math.factorial(i))
            T_n_values[i] = TaylorCurveDegree
        self.TaylorConvergenceImage.axes.plot(n_values,
                                       y_value - T_n_values,
                                       color = "r")

        self.TaylorConvergenceImage.axes.axvline(self.parameters.TaylorDegree,color = "grey")
        self.TaylorConvergenceImage.axes.grid()
        self.TaylorConvergenceImage.axes.set_xlabel(CalculusStrings.DegreeTaylor[f"{self.language}"]+" n")
        self.TaylorConvergenceImage.axes.set_ylabel(r"f(a) - T$_n$(a)")
        self.TaylorConvergenceImage.axes.set_title(CalculusStrings.ConvergenceGraphTitleTaylor[f"{self.language}"]+
                                                   str(self.parameters.TaylorXValue))
        self.TaylorConvergenceImage.draw()

    def update_Combo_CurvePolarFunctions(self):
        """Updates the Polar Curve Type"""
        name_tmp = self.PolarCurveType.currentText()
        for dict, names in CalculusStrings.ButtonChoiceFunction.items():
            if name_tmp in names.values():
                self.parameters.PolarCurveName = dict
        self.updatePolarCurves()

    def updatePolarCurves(self):
        """Updates the Polar Curves"""
        if self.parameters.PolarCurveName == "Constant":
            self.parameters.PolarCurveFunction = Curves.FlatCurve
        elif self.parameters.PolarCurveName == "Line":
            self.parameters.PolarCurveFunction = Curves.LinearCurve
        elif self.parameters.PolarCurveName == "Quadratic":
            self.parameters.PolarCurveFunction = Curves.QuadraticCurve
        elif self.parameters.PolarCurveName == "Cubic":
            self.parameters.PolarCurveFunction = Curves.CubicCurve
        elif self.parameters.PolarCurveName == "Exponential":
            self.parameters.PolarCurveFunction = Curves.ExponentialCurve
        elif self.parameters.PolarCurveName == "Exp. Power":
            self.parameters.PolarCurveFunction = Curves.ExponentialPowerCurve
        elif self.parameters.PolarCurveName == "Logarithmic":
            self.parameters.PolarCurveFunction = Curves.LogarithmicCurve
        elif self.parameters.PolarCurveName == "Sin":
            self.parameters.PolarCurveFunction = Curves.SinCurve
        elif self.parameters.PolarCurveName == "Cos":
            self.parameters.PolarCurveFunction = Curves.CosCurve
        elif self.parameters.PolarCurveName == "Tan":
            self.parameters.PolarCurveFunction = Curves.TanCurve
        elif self.parameters.PolarCurveName == "ArcSin":
            self.parameters.PolarCurveFunction = Curves.ArcSinCurve
        elif self.parameters.PolarCurveName == "ArcCos":
            self.parameters.PolarCurveFunction = Curves.ArcCosCurve
        elif self.parameters.PolarCurveName == "ArcTan":
            self.parameters.PolarCurveFunction = Curves.ArcTanCurve  
        elif self.parameters.PolarCurveName == "Sinc":
            self.parameters.PolarCurveFunction = Curves.Sinc 
        self.updatePolarAxes()

    def updateCurveParametersPolar(self):
        """Updates the Parameters of the Taylor Part"""
        try:
            self.parameters.PolarCurveParameters[0] = float(self.Parameter1Polar.text())
        except:
            self.parameters.PolarCurveParameters[0] = 1.0
        try:
            self.parameters.PolarCurveParameters[1] = float(self.Parameter2Polar.text())
        except:
            self.parameters.PolarCurveParameters[1] = 1.0
        try:
            self.parameters.PolarCurveParameters[2] = float(self.Parameter3Polar.text())
        except:
            self.parameters.PolarCurveParameters[2] = 1.0
        try:
            self.parameters.PolarCurveParameters[3] = float(self.Parameter4Polar.text())
        except:
            self.parameters.PolarCurveParameters[3] = 1.0
        try:
            self.parameters.PolarPhiBounds[0] = float(self.ParameterPolarBoundMin.text())
        except:
            self.parameters.PolarPhiBounds[0] = 0.0
        try:
            self.parameters.PolarPhiBounds[1] = float(self.ParameterPolarBoundMax.text())
        except:
            self.parameters.PolarPhiBounds[1] = 2.0
        self.updatePolarAxes()

    def updatePolarAxes(self):
        self.parameters.PolarPhiAxis = np.linspace(self.parameters.PolarPhiBounds[0] * np.pi,self.parameters.PolarPhiBounds[1]*np.pi,10000)
        self.parameters.PolarRAxis = self.parameters.PolarCurveFunction(self.parameters.PolarPhiAxis,self.parameters.PolarCurveParameters)
        self.updateImagePolarCurve()

    def updateImagePolarCurve(self):
        """Updates the Polar Curve"""
        try:
            self.PolarImage.axes.cla()
        except:
            pass

        self.PolarImage.axes.plot(self.parameters.PolarRAxis*np.cos(self.parameters.PolarPhiAxis), 
                                  self.parameters.PolarRAxis*np.sin(self.parameters.PolarPhiAxis))

        r_max = np.max(self.parameters.PolarRAxis) + 1


        self.PolarImage.axes.set_title(CalculusStrings.FunctionLabel[f"{self.language}"] + " " +
                                    CalculusStrings.ButtonChoiceFunction[f"{self.parameters.PolarCurveName}"][f"{self.language}"] +  
                                    f" : r($\phi$) = {CalculusStrings.CurveEquation(self.parameters.PolarCurveName,self.parameters.PolarCurveParameters,polar = True)}")
 
        self.PolarImage.axes.grid()
        try:
            self.PolarImage.axes.set_xlim(left = -r_max,right = r_max)
            self.PolarImage.axes.set_ylim(bottom = -r_max,top = r_max)
        except: pass
        self.PolarImage.draw()

    def update_Combo_CurveParametric2DFunctions(self):
        """Updates the Curve Type"""
        name_tmp = self.Parametric2DCurveTypeX.currentText()
        for dict, names in CalculusStrings.Parametric2DFunctionNames.items():
            if name_tmp in names.values():
                self.parameters.Parametric2DFunctionsXName = dict

        name_tmp = self.Parametric2DCurveTypeY.currentText()
        for dict, names in CalculusStrings.Parametric2DFunctionNames.items():
            if name_tmp in names.values():
                self.parameters.Parametric2DFunctionsYName = dict

        if self.Parametric2DCurveSameType.isChecked():
            self.parameters.Parametric2DFunctionsSame = True
        else:
            self.parameters.Parametric2DFunctionsSame = False

        if self.parameters.Parametric2DFunctionsSame:
            self.parameters.Parametric2DFunctionsYName = self.parameters.Parametric2DFunctionsXName
            self.Parametric2DCurveTypeY.setCurrentText(CalculusStrings.Parametric2DFunctionNames[self.parameters.Parametric2DFunctionsYName][self.language])

        self.updateFunctionsTypeParametric2DFunctions()

    def updateFunctionsTypeParametric2DFunctions(self):
        """Updates the Derivatives Curves"""
        if self.parameters.Parametric2DFunctionsXName == "Fresnel":
            self.parameters.Parametric2DFunctionsX = ParametricFunctions.FresnelIntegrals
        elif self.parameters.Parametric2DFunctionsXName == "cos":
            self.parameters.Parametric2DFunctionsX = ParametricFunctions.Cos
        elif self.parameters.Parametric2DFunctionsXName == "sin":
            self.parameters.Parametric2DFunctionsX = ParametricFunctions.Sin
        elif self.parameters.Parametric2DFunctionsXName == "hypocycloid":
            self.parameters.Parametric2DFunctionsX = ParametricFunctions.hypocycloid
        elif self.parameters.Parametric2DFunctionsXName == "astroid":
            self.parameters.Parametric2DFunctionsX = ParametricFunctions.astroid
        elif self.parameters.Parametric2DFunctionsXName == "superellipse":
            self.parameters.Parametric2DFunctionsX = ParametricFunctions.superellipse

        if self.parameters.Parametric2DFunctionsYName == "Fresnel":
            self.parameters.Parametric2DFunctionsY = ParametricFunctions.FresnelIntegrals
        elif self.parameters.Parametric2DFunctionsYName == "cos":
            self.parameters.Parametric2DFunctionsY = ParametricFunctions.Cos
        elif self.parameters.Parametric2DFunctionsYName == "sin":
            self.parameters.Parametric2DFunctionsY = ParametricFunctions.Sin
        elif self.parameters.Parametric2DFunctionsYName == "hypocycloid":
            self.parameters.Parametric2DFunctionsY = ParametricFunctions.hypocycloid
        elif self.parameters.Parametric2DFunctionsYName == "astroid":
            self.parameters.Parametric2DFunctionsY = ParametricFunctions.astroid
        elif self.parameters.Parametric2DFunctionsYName == "superellipse":
            self.parameters.Parametric2DFunctionsY = ParametricFunctions.superellipse


        self.updateFunctionsParametric2DFunctions()

    def updateParametersParametric2DFunctions(self):
        """Updates the Parameters of the Parametric 2D Functions"""
        try:
            self.parameters.Parametric2DFunctionsTValue = float(self.ParameterTValueParametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsTValue = 0.0
        try:
            self.parameters.Parametric2DFunctionsParameters[0,0] = float(self.Parameter00Parametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsParameters[0,0] = 1.0
        try:
            self.parameters.Parametric2DFunctionsParameters[0,1] = float(self.Parameter01Parametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsParameters[0,1] = 1.0
        try:
            self.parameters.Parametric2DFunctionsParameters[0,2] = float(self.Parameter02Parametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsParameters[0,2] = 1.0
        try:
            self.parameters.Parametric2DFunctionsParameters[0,3] = float(self.Parameter03Parametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsParameters[0,3] = 1.0
        try:
            self.parameters.Parametric2DFunctionsParameters[1,0] = float(self.Parameter10Parametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsParameters[1,0] = 1.0
        try:
            self.parameters.Parametric2DFunctionsParameters[1,1] = float(self.Parameter11Parametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsParameters[1,1] = 1.0
        try:
            self.parameters.Parametric2DFunctionsParameters[1,2] = float(self.Parameter12Parametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsParameters[1,2] = 1.0
        try:
            self.parameters.Parametric2DFunctionsParameters[1,3] = float(self.Parameter13Parametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsParameters[1,3] = 1.0
        try:
            self.parameters.Parametric2DFunctionsTAxisBounds[0] = float(self.ParameterBoundMinParametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsTAxisBounds[0] = -10.0
        try:
            self.parameters.Parametric2DFunctionsTAxisBounds[1] = float(self.ParameterBoundMaxParametric2DFunctions.text())
        except:
            self.parameters.Parametric2DFunctionsTAxisBounds[1] = 10.0
        self.updateFunctionsParametric2DFunctions()

    def updateFunctionsParametric2DFunctions(self):
        self.parameters.Parametric2DFunctionsTAxis = np.linspace(self.parameters.Parametric2DFunctionsTAxisBounds[0],self.parameters.Parametric2DFunctionsTAxisBounds[1],1000)
        self.parameters.Parametric2DFunctionsXValue, _ = self.parameters.Parametric2DFunctionsX(self.parameters.Parametric2DFunctionsTValue,self.parameters.Parametric2DFunctionsParameters)
        _, self.parameters.Parametric2DFunctionsYValue = self.parameters.Parametric2DFunctionsY(self.parameters.Parametric2DFunctionsTValue,self.parameters.Parametric2DFunctionsParameters)
        self.parameters.Parametric2DFunctionsXAxis, _ = self.parameters.Parametric2DFunctionsX(self.parameters.Parametric2DFunctionsTAxis,self.parameters.Parametric2DFunctionsParameters)
        _, self.parameters.Parametric2DFunctionsYAxis = self.parameters.Parametric2DFunctionsY(self.parameters.Parametric2DFunctionsTAxis,self.parameters.Parametric2DFunctionsParameters)
        self.updateImagesParametric2DFunctions()

    def updateImagesParametric2DFunctions(self):
        """Updates all the Images for the Taylor Part"""
        self.updateXYImageParametric2DFunctions()
        self.updateYImageParametric2DFunctions()
        self.updateXImageParametric2DFunctions()
    def updateXYImageParametric2DFunctions(self):
        """Updates the Parametric2D XY Image"""
        try:
            self.Parametric2DXYImage.axes.cla()
        except:
            pass
        self.Parametric2DXYImage.axes.grid()
        self.Parametric2DXYImage.axes.set_xlabel("x")
        self.Parametric2DXYImage.axes.set_ylabel("y")

        self.Parametric2DXYImage.axes.plot(self.parameters.Parametric2DFunctionsXAxis,self.parameters.Parametric2DFunctionsYAxis)
        self.Parametric2DXYImage.axes.plot(self.parameters.Parametric2DFunctionsXValue,
                                      self.parameters.Parametric2DFunctionsYValue,
                                      marker = '*')

        self.Parametric2DXYImage.axes.set_title(CalculusStrings.ParametricFunctionGraphTitle[f"{self.language}"]+ " : "+
                                           CalculusStrings.Parametric2DFunctionNames[f"{self.parameters.Parametric2DFunctionsXName}"][f"{self.language}"])
        self.Parametric2DXYImage.draw()
    def updateYImageParametric2DFunctions(self):
        """Updates the Parametric2D Y Image"""
        try:
            self.Parametric2DYImage.axes.cla()
        except:
            pass

        self.Parametric2DYImage.axes.plot(self.parameters.Parametric2DFunctionsTAxis,self.parameters.Parametric2DFunctionsYAxis)
        self.Parametric2DYImage.axes.plot(self.parameters.Parametric2DFunctionsTValue,
                                      self.parameters.Parametric2DFunctionsYValue,
                                      marker = '*')

        x, y = CalculusStrings.Parametric2DFunctionEquation(self.parameters.Parametric2DFunctionsYName, self.parameters.Parametric2DFunctionsParameters)
        self.Parametric2DYImage.axes.grid()
        self.Parametric2DYImage.axes.set_xlabel("t")
        self.Parametric2DYImage.axes.set_ylabel("y")
        self.Parametric2DYImage.axes.set_title("y(t) = " + y)
        self.Parametric2DYImage.draw()
    def updateXImageParametric2DFunctions(self):
        """Updates the Parametric2D X Image"""
        try:
            self.Parametric2DXImage.axes.cla()
        except:
            pass

        self.Parametric2DXImage.axes.plot(self.parameters.Parametric2DFunctionsTAxis,self.parameters.Parametric2DFunctionsXAxis)
        self.Parametric2DXImage.axes.plot(self.parameters.Parametric2DFunctionsTValue,
                                      self.parameters.Parametric2DFunctionsXValue,
                                      marker = '*')

        x, y = CalculusStrings.Parametric2DFunctionEquation(self.parameters.Parametric2DFunctionsXName, self.parameters.Parametric2DFunctionsParameters)
        self.Parametric2DXImage.axes.grid()
        self.Parametric2DXImage.axes.set_xlabel("t")
        self.Parametric2DXImage.axes.set_ylabel("x")
        self.Parametric2DXImage.axes.set_title("x(t) = " + x)
        self.Parametric2DXImage.draw()

    def onClick(self,event,which):
        """Allows to click on an image and update the interface"""
        ix, iy = event.xdata, event.ydata
        which.coords = []
        which.coords.append((ix, iy))
        if len(which.coords) == 2:
            which.fig.canvas.mpl_disconnect(self.cid)
        if which == self.DerivativesBasicImage or which == self.DerivativesDerivedImage:
            self.parameters.DerivativesCursorValue = ix
            self.lineEditPositionCursorDerivatives.setText(f"{float(ix):.2f}")
            self.updateAllDerivatives()
        elif which == self.LimitDerivativesImage:
            self.parameters.DerivativesHValue = ix
            self.DerivativesH.setText(f"{float(ix):.2f}")
            self.updateAllDerivatives()
        elif which == self.IntegralSumImage:
            if int(ix) > 0:
                self.parameters.IntegralBoxNumber = round(ix)
                self.NumberBoxIntegral.setText(f"{int(ix)}")
            self.updateCurveBoundsIntegral()
            self.updateCurveNumberBoxesIntegral()
        elif which in [self.TaylorBaseImage,self.TaylorDifferenceImage]:
            self.parameters.TaylorCenter = ix
            self.CenterParameterTaylor.setText(f"{float(ix):.2f}")

            self.updateCurveTaylor()
        elif which == self.TaylorConvergenceImage:
            self.parameters.TaylorDegree = round(ix)
            self.DegreeParameterTaylor.setText(f"{int(ix)}")
            self.updateCurveTaylor()
        elif which == self.Parametric2DYImage:
            self.ParameterTValueParametric2DFunctions.setText(f"{float(ix):.2f}")
            self.parameters.Parametric2DFunctionsTValue = ix
            self.updateFunctionsParametric2DFunctions()
        elif which == self.Parametric2DXImage:
            self.ParameterTValueParametric2DFunctions.setText(f"{float(ix):.2f}")
            self.parameters.Parametric2DFunctionsTValue = ix
            self.updateFunctionsParametric2DFunctions()
        elif which == self.Parametric2DXYImage:
            #Find the closest X and Y values
            closestX, closestY = 1e10, 1e10
            for i in range(self.parameters.Parametric2DFunctionsTAxis.shape[0]):
                if (self.parameters.Parametric2DFunctionsXAxis[i]-ix)**2 + (self.parameters.Parametric2DFunctionsYAxis[i]-iy)**2 < (closestX-ix)**2 + (closestY-iy)**2:
                    closestX = self.parameters.Parametric2DFunctionsXAxis[i]
                    closestY = self.parameters.Parametric2DFunctionsYAxis[i]
            #Infer t: do the same
            currentTotal = 1e100
            closestT = self.parameters.Parametric2DFunctionsTAxis[0]
            for i in range(self.parameters.Parametric2DFunctionsTAxis.shape[0]):
                XValue, _ = self.parameters.Parametric2DFunctionsX(self.parameters.Parametric2DFunctionsTAxis[i],self.parameters.Parametric2DFunctionsParameters)
                _, YValue = self.parameters.Parametric2DFunctionsY(self.parameters.Parametric2DFunctionsTAxis[i],self.parameters.Parametric2DFunctionsParameters)
                if (XValue - closestX)**2 + (YValue - closestY)**2 < currentTotal:
                    closestT = self.parameters.Parametric2DFunctionsTAxis[i]
                    currentTotal = (XValue - closestX)**2 + (YValue - closestY)**2
            self.parameters.Parametric2DFunctionsTValue = closestT
            self.updateFunctionsParametric2DFunctions()

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
        if which == self.DerivativesBasicImage or which == self.DerivativesDerivedImage:
            actual = float(self.lineEditPositionCursorDerivatives.text())
            scale_factor = scale_factor*self.parameters.DerivativesXAxisBounds[-1]/100
            self.parameters.DerivativesCursorValue += scale_factor
            self.lineEditPositionCursorDerivatives.setText(f"{(float(actual) + scale_factor):.2f}")
            self.updateAllDerivatives()
        elif which == self.LimitDerivativesImage:
            actual = float(self.DerivativesH.text())
            #scale_factor = - scale_factor*self.parameters.HValueRange[-1]/100
            if scale_factor > 0:
                scale_factor = 2
            else:
                scale_factor = 1/2
            self.parameters.DerivativesHValue *= scale_factor
            self.DerivativesH.setText(f"{(float(actual)*scale_factor):.2f}")
            self.updateAllDerivatives()
        elif which == self.IntegralSumImage:
            if self.parameters.IntegralBoxNumber + scale_factor > 0:
                actual = int(self.NumberBoxIntegral.text())
                self.parameters.IntegralBoxNumber += scale_factor
                self.NumberBoxIntegral.setText(f"{actual + int(scale_factor)}")
            self.updateCurveBoundsIntegral()
            self.updateCurveNumberBoxesIntegral()
        elif which in [self.TaylorBaseImage,self.TaylorDifferenceImage]:
            actual = float(self.CenterParameterTaylor.text())
            scale_factor = scale_factor*(self.parameters.TaylorBounds[1] - self.parameters.TaylorBounds[0])/100
            self.parameters.TaylorCenter += scale_factor
            self.CenterParameterTaylor.setText(f"{(float(actual) + scale_factor):.2f}")

            self.updateCurveTaylor()
        elif which == self.TaylorConvergenceImage:
            actual = int(self.DegreeParameterTaylor.text())
            self.parameters.TaylorDegree += scale_factor
            self.DegreeParameterTaylor.setText(f"{(int(actual) + scale_factor)}")
            self.updateCurveTaylor()
        elif which in [self.Parametric2DYImage,self.Parametric2DXImage,self.Parametric2DXYImage]:
            #actual = int(self.DegreeParameterTaylor.text())
            scale_factor = scale_factor*(self.parameters.Parametric2DFunctionsTAxis[-1] - self.parameters.Parametric2DFunctionsTAxis[0])/1000
            self.parameters.Parametric2DFunctionsTValue += scale_factor
            self.ParameterTValueParametric2DFunctions.setText(f"{float(self.parameters.Parametric2DFunctionsTValue):.2f}")
            self.updateFunctionsParametric2DFunctions()

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