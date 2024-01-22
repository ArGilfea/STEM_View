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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.fft                      #Pour la transformée de Fourier
import cmath
###
try:
    import GUIParametersAnalysis
    import AnalysisStrings
    import Fourier1D
    import Filters
except:
    import Analysis.GUIParametersAnalysis as GUIParametersAnalysis
    import Analysis.AnalysisStrings as AnalysisStrings
    import Analysis.Fourier1D as Fourier1D
    import Analysis.Filters as Filters
    import Analysis.Filters as Filters


size_Image = 200
basedir = os.path.dirname(__file__)

class AnalysisWindow(QMainWindow):
    """
    Main window of the GUI.
    """    
    def __init__(self,parent=None,language= "Fr"):
        """Initializes the GUI Window"""
        self.language = language
        self.parameters = GUIParametersAnalysis.GUIParametersAnalysis()
        self.tabs = QTabWidget()
        self.currentLineFourier1D = 1
        self.currentLineFilters = 1
        self.currentLineComplexNumbers = 1
        super().__init__(parent=parent)
        self.setMinimumSize(1200, 700)
        self.setWindowTitle(AnalysisStrings.WindowName[f"{self.language}"])

        self.generalLayoutFourier1D = QGridLayout()
        self.generalLayoutFilters = QGridLayout()
        self.generalLayoutComplexNumbers = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()

        centralWidgetFourier1D = QWidget(self)
        centralWidgetFilters = QWidget(self)
        centralWidgetComplexNumbers = QWidget(self)
        centralWidgetReadMe = QWidget(self)

        centralWidgetFourier1D.setLayout(self.generalLayoutFourier1D)
        centralWidgetFilters.setLayout(self.generalLayoutFilters)
        centralWidgetComplexNumbers.setLayout(self.generalLayoutComplexNumbers)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)

        self.tabs.addTab(centralWidgetFourier1D,AnalysisStrings.Fourier1DTabName[f"{self.language}"])
        self.tabs.addTab(centralWidgetFilters,AnalysisStrings.FiltersName[f"{self.language}"])
        self.tabs.addTab(centralWidgetComplexNumbers,AnalysisStrings.ComplexNumbersName[f"{self.language}"])
        self.tabs.addTab(centralWidgetReadMe,AnalysisStrings.ReadMeName[f"{self.language}"])

        self.setCentralWidget(self.tabs)

        #Fourier 1D Tab
        self._createBaseFunctionImageFourier1D()
        self._createFilterFouriedImageFourier1D()

        self._createConvolutionImageFourier1D()
        self._createConvolutionFouriedImageFourier1D()

        self._createParametersImageButtonsFourier1D()
        #Filters Tab
        self._createBaseImageFilters()
        self._createFilterImageFilters()
        self._createFourierBaseImageFilters()
        self._createFourierFilterFilters()
        self._createConvolvedImageFilters()
        self._createParametersButtonsFilters()
        #Complex Number Tab
        self._createImageComplexNumbers()
        self._createParametersButtonsComplexNumbers()
        #Exit Button
        self._createExitButton()

        self.generalLayoutFourier1D.setColumnStretch(1,5)
        self.generalLayoutFourier1D.setColumnStretch(2,5)
        self.generalLayoutFilters.setColumnStretch(1,5)
        self.generalLayoutFilters.setColumnStretch(2,5)
        self.showMaximized()
        self.complexClicker = 1

    ###Create Interface###
    def _createBaseFunctionImageFourier1D(self):
        """Creates Images for the Spatial Functions of Fourier 1D"""
        self.Fourier1DBaseImage = np.zeros(self.parameters.numberFilter, dtype = object)
        for i in range(self.parameters.numberFilter):
            self.Fourier1DBaseImage[i] = MplCanvas(self, width=6, height=6, dpi=75)
            self.generalLayoutFourier1D.addWidget(self.Fourier1DBaseImage[i],self.currentLineFourier1D,i + 1)
        self.currentLineFourier1D += 1

    def _createFilterFouriedImageFourier1D(self):
        """Creates the Fouried Image of Fourier 1D"""
        self.Fourier1DFouriedImage = np.zeros(self.parameters.numberFilter, dtype = object)
        for i in range(self.parameters.numberFilter):
            self.Fourier1DFouriedImage[i] = MplCanvas(self, width=6, height=6, dpi=75)
            self.generalLayoutFourier1D.addWidget(self.Fourier1DFouriedImage[i],self.currentLineFourier1D,i+1)
        self.currentLineFourier1D += 1

    def _createConvolutionImageFourier1D(self):
        """Creates an Image for the Base function of Fourier 1D"""
        self.Fourier1DConvolvedImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutFourier1D.addWidget(self.Fourier1DConvolvedImage,self.currentLineFourier1D,1)

    def _createConvolutionFouriedImageFourier1D(self):
        """Creates an Image for the Base function of Fourier 1D"""
        self.Fourier1DConvolvedFouriedImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutFourier1D.addWidget(self.Fourier1DConvolvedFouriedImage,self.currentLineFourier1D,2)
        self.currentLineFourier1D += 1

        self.updateImagesFourier1D()


    def _createParametersImageButtonsFourier1D(self):
        """Creates the Buttons for the Parameters of the Fourier 1D"""
        self.CurveTypeComboBoxFourier1D = np.zeros((self.parameters.numberFilter,self.parameters.numberParameters),dtype = object)
        self.CurveDirectFourierComboBoxFourier1D = np.zeros(self.parameters.numberFilter,dtype = object)
        self.FullRangeComboBoxFourier1D = np.zeros((self.parameters.numberFilter,self.parameters.numberParameters),dtype = object)
        self.ParameterLineEditFourier1D = np.zeros((self.parameters.numberFilter,self.parameters.numberParameters,self.parameters.numberParameters2),dtype = object)

        self.RangeMinLineEditFourier1D = QLineEdit()
        self.RangeMaxLineEditFourier1D = QLineEdit()

        for i in range(self.parameters.numberFilter):
            subWidget = QWidget()
            layout = QGridLayout()
            subWidget.setLayout(layout)
            for j in range(self.parameters.numberParameters):
                self.CurveTypeComboBoxFourier1D[i,j] = QComboBox()
                for _, names in AnalysisStrings.CurvesTypeFourier1D.items():
                    self.CurveTypeComboBoxFourier1D[i,j].addItem(names[f"{self.language}"])
                self.CurveTypeComboBoxFourier1D[i,j].setCurrentText(AnalysisStrings.CurvesTypeFilters[f"{self.parameters.CurveTypeFourier1D[i,j]}"][f"{self.language}"])
                self.CurveTypeComboBoxFourier1D[i,j].activated[str].connect(self.update_Combo_CurveFourier1D)

                self.FullRangeComboBoxFourier1D[i,j] = QCheckBox()
                self.FullRangeComboBoxFourier1D[i,j].stateChanged.connect(self.update_Check_FullRangeFourier1D)

            self.CurveDirectFourierComboBoxFourier1D[i] = QCheckBox()
            self.CurveDirectFourierComboBoxFourier1D[i].stateChanged.connect(self.update_Check_DirectFourierFourier1D)

            for j in range(self.parameters.numberParameters):
                for k in range(self.parameters.numberParameters2):
                    self.ParameterLineEditFourier1D[i,j,k] = QLineEdit()
                    self.ParameterLineEditFourier1D[i,j,k].setFixedWidth(90)
                    self.ParameterLineEditFourier1D[i,j,k].setText(str(self.parameters.CurveParametersFourier1D[i,j,k]))
                    self.ParameterLineEditFourier1D[i,j,k].editingFinished.connect(self.updateParametersFourier1D)

            layout.addWidget(QLabel(AnalysisStrings.ParametersImageFourier1D[f"{self.language}"]),0,1)
            layout.addWidget(QLabel(AnalysisStrings.FourierDirectFourier1D[f"{self.language}"]),0,3)
            layout.addWidget(self.CurveDirectFourierComboBoxFourier1D[i],0,4)
            for j in range(self.parameters.numberParameters):
                layout.addWidget(self.CurveTypeComboBoxFourier1D[i,j],j+3,1)
                layout.addWidget(QLabel(AnalysisStrings.Parameters2Fourier1D[f"{self.language}"]+f" {j+1}"),j+3,2)
                for k in range(self.parameters.numberParameters2):

                    layout.addWidget(self.ParameterLineEditFourier1D[i,j,k],j+3,k+2)
                layout.addWidget(self.FullRangeComboBoxFourier1D[i,j],j+3,k+4)
            for k in range(self.parameters.numberParameters2):
                if k == 0:
                    layout.addWidget(QLabel(AnalysisStrings.Phase[f"{self.language}"]),2,k+2)
                elif k == 1:
                    layout.addWidget(QLabel(AnalysisStrings.Frequency[f"{self.language}"]),2,k+2)
                elif k == 2:
                    layout.addWidget(QLabel(AnalysisStrings.Amplitude[f"{self.language}"]),2,k+2)
            layout.addWidget(QLabel(AnalysisStrings.FullRangeFourier1D[f"{self.language}"]),2,k+4)

            self.generalLayoutFourier1D.addWidget(subWidget,self.currentLineFourier1D,i+1)
        self.currentLineFourier1D += 1

    def _createBaseImageFilters(self):
        """Creates an Image for the Base Image of Filters"""
        self.BaseImageFilters = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutFilters.addWidget(self.BaseImageFilters,self.currentLineFilters,1)
    def _createFilterImageFilters(self):
        """Creates an Image for the Base Image of Filters"""
        self.FilterImageFilters = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutFilters.addWidget(self.FilterImageFilters,self.currentLineFilters,2)
        self.currentLineFilters += 1
    def _createFourierBaseImageFilters(self):
        """Creates an Image for the Base Image of Filters"""
        self.FourierBaseImageFilters = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutFilters.addWidget(self.FourierBaseImageFilters,self.currentLineFilters,1)
    def _createFourierFilterFilters(self):
        """Creates an Image for the Base Image of Filters"""
        self.FourierFilterImageFilters = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutFilters.addWidget(self.FourierFilterImageFilters,self.currentLineFilters,2)
        self.currentLineFilters += 1
    def _createConvolvedImageFilters(self):
        """Creates an Image for the Base Image of Filters"""
        self.ConvolutedBaseImageFilters = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutFilters.addWidget(self.ConvolutedBaseImageFilters,self.currentLineFilters,1)
        self.updateImagesFilters()
    def _createParametersButtonsFilters(self):
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.ImageTypeComboBoxFilters = QComboBox()
        for _, names in AnalysisStrings.ImageNameFilters.items():
            self.ImageTypeComboBoxFilters.addItem(names[f"{self.language}"])
        self.ImageTypeComboBoxFilters.setCurrentText(AnalysisStrings.ImageNameFilters[f"{self.parameters.ImageFiltersName}"][f"{self.language}"])
        self.ImageTypeComboBoxFilters.activated[str].connect(self.update_Combo_ImageFilters)        

        self.FilterTypeComboBoxFilters = QComboBox()
        for _, names in AnalysisStrings.CurvesTypeFilters.items():
            self.FilterTypeComboBoxFilters.addItem(names[f"{self.language}"])
        self.FilterTypeComboBoxFilters.setCurrentText(AnalysisStrings.CurvesTypeFilters[f"{self.parameters.FilterFiltersName}"][f"{self.language}"])
        self.FilterTypeComboBoxFilters.activated[str].connect(self.update_Combo_CurveFilters)  

        self.ParametersFullRangeCheckBox = QCheckBox()
        self.ParametersFullRangeCheckBox.stateChanged.connect(self.update_Check_FullRangeFilters)

        self.LogViewComboBoxFilters = QCheckBox()
        self.LogViewComboBoxFilters.stateChanged.connect(self.update_Check_logViewFilters)

        self.Parameter1LineEditFilters = QLineEdit()
        self.Parameter2LineEditFilters = QLineEdit()
        self.Parameter1LineEditFilters.setFixedWidth(90)
        self.Parameter2LineEditFilters.setFixedWidth(90)
        self.Parameter1LineEditFilters.setText(f"{str(self.parameters.ParametersFilters[0])}")
        self.Parameter2LineEditFilters.setText(f"{str(self.parameters.ParametersFilters[1])}")
        self.Parameter1LineEditFilters.editingFinished.connect(self.updateParametersFilters)
        self.Parameter2LineEditFilters.editingFinished.connect(self.updateParametersFilters)


        layout.addWidget(QLabel(AnalysisStrings.ImageHeaderFilters[f"{self.language}"]),1,1)
        layout.addWidget(self.ImageTypeComboBoxFilters,1,2)
        layout.addWidget(QLabel(AnalysisStrings.FilterHeaderFilters[f"{self.language}"]),2,1)
        layout.addWidget(self.FilterTypeComboBoxFilters,2,2)
        layout.addWidget(QLabel(AnalysisStrings.FullRangeFourier1D[f"{self.language}"]),3,1)
        layout.addWidget(self.ParametersFullRangeCheckBox,3,2)
        layout.addWidget(QLabel(AnalysisStrings.LogViewFilters[f"{self.language}"]),4,1)
        layout.addWidget(self.LogViewComboBoxFilters,4,2)
        layout.addWidget(QLabel(AnalysisStrings.Parameters2Fourier1D[f"{self.language}"] + " 1"),5,1)
        layout.addWidget(self.Parameter1LineEditFilters,5,2)
        layout.addWidget(QLabel(AnalysisStrings.Parameters2Fourier1D[f"{self.language}"] + " 2"),6,1)
        layout.addWidget(self.Parameter2LineEditFilters,6,2)

        self.generalLayoutFilters.addWidget(subWidget,self.currentLineFilters,2)
        self.currentLineFilters += 1
    def _createImageComplexNumbers(self):
        """Creates an Image for the Base Image of Complex Numbers"""
        self.ImageComplexNumbers = MplCanvas(self, width=6, height=6, dpi=75)
        self.ImageComplexNumbers_cid = self.ImageComplexNumbers.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.ImageComplexNumbers))
        self.generalLayoutComplexNumbers.addWidget(self.ImageComplexNumbers,self.currentLineComplexNumbers,1)
        self.updateImagesComplexNumber()
    def _createParametersButtonsComplexNumbers(self):
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.Parameter1ComplexNumber = QLineEdit()
        self.Parameter1jComplexNumber = QLineEdit()
        self.Parameter1PolarRComplexNumber = QLineEdit()
        self.Parameter1PolarThetaComplexNumber = QLineEdit()
        self.Parameter2ComplexNumber = QLineEdit()
        self.Parameter2jComplexNumber = QLineEdit()
        self.Parameter2PolarRComplexNumber = QLineEdit()
        self.Parameter2PolarThetaComplexNumber = QLineEdit()
        self.Parameter3ComplexNumber = QLineEdit()
        self.Parameter3jComplexNumber = QLineEdit()
        self.Parameter3PolarRComplexNumber = QLineEdit()
        self.Parameter3PolarThetaComplexNumber = QLineEdit()

        self.Parameter1ComplexNumber.setFixedWidth(90)
        self.Parameter1jComplexNumber.setFixedWidth(90)
        self.Parameter1PolarRComplexNumber.setFixedWidth(90)
        self.Parameter1PolarThetaComplexNumber.setFixedWidth(90)
        self.Parameter2ComplexNumber.setFixedWidth(90)
        self.Parameter2jComplexNumber.setFixedWidth(90)
        self.Parameter2PolarRComplexNumber.setFixedWidth(90)
        self.Parameter2PolarThetaComplexNumber.setFixedWidth(90)
        self.Parameter3ComplexNumber.setFixedWidth(90)
        self.Parameter3jComplexNumber.setFixedWidth(90)
        self.Parameter3PolarRComplexNumber.setFixedWidth(90)
        self.Parameter3PolarThetaComplexNumber.setFixedWidth(90)

        self.Parameter1ComplexNumber.setText(f"{str(self.parameters.ComplexNumber1.real)}")
        self.Parameter1jComplexNumber.setText(f"{str(self.parameters.ComplexNumber1.imag)}")
        self.Parameter1PolarRComplexNumber.setText(f"{str(abs(self.parameters.ComplexNumber1))}")
        self.Parameter1PolarThetaComplexNumber.setText(f"{str(cmath.phase(self.parameters.ComplexNumber1))}")
        self.Parameter2ComplexNumber.setText(f"{str(self.parameters.ComplexNumber2.real)}")
        self.Parameter2jComplexNumber.setText(f"{str(self.parameters.ComplexNumber2.imag)}")
        self.Parameter2PolarRComplexNumber.setText(f"{str(abs(self.parameters.ComplexNumber2))}")
        self.Parameter2PolarThetaComplexNumber.setText(f"{str(cmath.phase(self.parameters.ComplexNumber2))}")
        self.Parameter3ComplexNumber.setText(f"{str(self.parameters.ComplexNumberResult.real)}")
        self.Parameter3jComplexNumber.setText(f"{str(self.parameters.ComplexNumberResult.imag)}")
        self.Parameter3PolarRComplexNumber.setText(f"{str(abs(self.parameters.ComplexNumberResult))}")
        self.Parameter3PolarThetaComplexNumber.setText(f"{str(cmath.phase(self.parameters.ComplexNumberResult))}")

        self.Parameter1ComplexNumber.editingFinished.connect(self.updateParametersCartesianComplexNumber)
        self.Parameter1jComplexNumber.editingFinished.connect(self.updateParametersCartesianComplexNumber)
        self.Parameter2ComplexNumber.editingFinished.connect(self.updateParametersCartesianComplexNumber)
        self.Parameter2jComplexNumber.editingFinished.connect(self.updateParametersCartesianComplexNumber)

        self.Parameter1PolarRComplexNumber.editingFinished.connect(self.updateParametersPolarComplexNumber)
        self.Parameter1PolarThetaComplexNumber.editingFinished.connect(self.updateParametersPolarComplexNumber)
        self.Parameter2PolarRComplexNumber.editingFinished.connect(self.updateParametersPolarComplexNumber)
        self.Parameter2PolarThetaComplexNumber.editingFinished.connect(self.updateParametersPolarComplexNumber)


        self.Parameter3ComplexNumber.setEnabled(False)
        self.Parameter3jComplexNumber.setEnabled(False)
        self.Parameter3PolarRComplexNumber.setEnabled(False)
        self.Parameter3PolarThetaComplexNumber.setEnabled(False)

        self.OperationComboBoxComplexNumber = QComboBox()
        for _, names in AnalysisStrings.ComplexNumberOperation.items():
            self.OperationComboBoxComplexNumber.addItem(names[f"{self.language}"])
        self.OperationComboBoxComplexNumber.setCurrentText(AnalysisStrings.ComplexNumberOperation[f"{self.parameters.ComplexNumberOperation}"][f"{self.language}"])
        self.OperationComboBoxComplexNumber.activated[str].connect(self.update_Combo_ComplexNumber)        

        self.ClickerComboBoxComplexNumber = QComboBox()
        self.ClickerComboBoxComplexNumber.addItem("1")
        self.ClickerComboBoxComplexNumber.addItem("2")
        self.ClickerComboBoxComplexNumber.addItem(AnalysisStrings.ComplexNumberClickerSwitch[f"{self.language}"])
        self.ClickerComboBoxComplexNumber.setCurrentText(self.parameters.ComplexNumberClicker)
        self.ClickerComboBoxComplexNumber.activated[str].connect(self.update_ComboClicker_ComplexNumber)        

        layout.addWidget(QLabel(AnalysisStrings.ComplexNumber1Header[f"{self.language}"]),1,1)
        layout.addWidget(QLabel(AnalysisStrings.ComplexNumberCartesianHeader[f"{self.language}"]),1,2)
        layout.addWidget(self.Parameter1ComplexNumber,1,3)
        layout.addWidget(self.Parameter1jComplexNumber,1,4)
        layout.addWidget(QLabel(AnalysisStrings.ComplexNumberPolarHeader[f"{self.language}"]),2,2)
        layout.addWidget(self.Parameter1PolarRComplexNumber,2,3)
        layout.addWidget(self.Parameter1PolarThetaComplexNumber,2,4)
        layout.addWidget(QLabel(AnalysisStrings.ComplexNumber2Header[f"{self.language}"]),3,1)
        layout.addWidget(QLabel(AnalysisStrings.ComplexNumberCartesianHeader[f"{self.language}"]),3,2)
        layout.addWidget(self.Parameter2ComplexNumber,3,3)
        layout.addWidget(self.Parameter2jComplexNumber,3,4)
        layout.addWidget(QLabel(AnalysisStrings.ComplexNumberPolarHeader[f"{self.language}"]),4,2)
        layout.addWidget(self.Parameter2PolarRComplexNumber,4,3)
        layout.addWidget(self.Parameter2PolarThetaComplexNumber,4,4)
        layout.addWidget(QLabel(AnalysisStrings.ComplexNumberResultHeader[f"{self.language}"]),5,1)
        layout.addWidget(QLabel(AnalysisStrings.ComplexNumberCartesianHeader[f"{self.language}"]),5,2)
        layout.addWidget(self.Parameter3ComplexNumber,5,3)
        layout.addWidget(self.Parameter3jComplexNumber,5,4)
        layout.addWidget(QLabel(AnalysisStrings.ComplexNumberPolarHeader[f"{self.language}"]),6,2)
        layout.addWidget(self.Parameter3PolarRComplexNumber,6,3)
        layout.addWidget(self.Parameter3PolarThetaComplexNumber,6,4)
        layout.addWidget(QLabel(AnalysisStrings.ComplexNumberOperationHeader[f"{self.language}"]),7,1)
        layout.addWidget(self.OperationComboBoxComplexNumber,7,4)
        layout.addWidget(QLabel(AnalysisStrings.ComplexNumberClickerHeader[f"{self.language}"]),8,1)
        layout.addWidget(self.ClickerComboBoxComplexNumber,8,4)

        self.generalLayoutComplexNumbers.addWidget(subWidget,self.currentLineComplexNumbers,2)
        self.currentLineComplexNumbers += 1
    def _createExitButton(self):
        """Creates exit buttons"""
        self.exitFourier1D = QPushButton(AnalysisStrings.ExitButton[f"{self.language}"])
        self.exitFilters = QPushButton(AnalysisStrings.ExitButton[f"{self.language}"])
        self.exitComplexNumbers = QPushButton(AnalysisStrings.ExitButton[f"{self.language}"])
        self.exitFourier1D.setToolTip(AnalysisStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitFilters.setToolTip(AnalysisStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitComplexNumbers.setToolTip(AnalysisStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitFourier1D.setShortcut("Ctrl+Shift+E")
        self.exitFilters.setShortcut("Ctrl+Shift+E")
        self.exitComplexNumbers.setShortcut("Ctrl+Shift+E")

        self.exitFourier1D.clicked.connect(self.close)
        self.exitFilters.clicked.connect(self.close)
        self.exitComplexNumbers.clicked.connect(self.close)
        self.generalLayoutFourier1D.addWidget(self.exitFourier1D,self.currentLineFourier1D+1,3)  
        self.generalLayoutFilters.addWidget(self.exitFilters,self.currentLineFilters+1,3)  
        self.generalLayoutComplexNumbers.addWidget(self.exitComplexNumbers,self.currentLineComplexNumbers+1,3)  
        self.currentLineFourier1D += 1
        self.currentLineFilters += 1
        self.currentLineComplexNumbers += 1
    ###Update Interface###
    def update_Combo_CurveFourier1D(self):
        """Updates the Curve Type"""
        for i in range(self.parameters.numberFilter):
            for j in range(self.parameters.numberParameters):
                name_tmp = self.CurveTypeComboBoxFourier1D[i,j].currentText()
                for dict, names in AnalysisStrings.CurvesTypeFourier1D.items():
                    if name_tmp in names.values():
                        self.parameters.CurveTypeFourier1D[i,j] = dict

        self.updateImagesFourier1D()

    def update_Check_FullRangeFourier1D(self):
        """Updates the Boolean for Full Range"""
        for i in range(self.parameters.numberFilter):
            for j in range(self.parameters.numberParameters):
                if self.FullRangeComboBoxFourier1D[i,j].isChecked():
                    self.parameters.fullRangeFourier1D[i,j] = True
                else:
                    self.parameters.fullRangeFourier1D[i,j] = False

        self.updateImagesFourier1D()

    def update_Check_DirectFourierFourier1D(self):
        """Updates the Boolean for Direct Fourier"""
        for i in range(self.parameters.numberFilter):
            if self.CurveDirectFourierComboBoxFourier1D[i].isChecked():
                self.parameters.directFourierCurve1D[i] = True
            else:
                self.parameters.directFourierCurve1D[i] = False

        self.updateImagesFourier1D()

    def updateParametersFourier1D(self):
        """Updates the Parameters of the Fourier 1D"""
        try:
            self.parameters.CurveRangeFourier1D[0] = float(self.RangeMinLineEditFourier1D.text())
        except:
            self.parameters.CurveRangeFourier1D[0] = -5.0
        try:
            self.parameters.CurveRangeFourier1D[1] = float(self.RangeMaxLineEditFourier1D.text())
        except:
            self.parameters.CurveRangeFourier1D[1] = 5.0
        self.parameters.XAxisFourier1D = np.arange(self.parameters.CurveRangeFourier1D[0],
                                                    self.parameters.CurveRangeFourier1D[1],
                                                    self.parameters.dxFourier1D)
        self.parameters.RangeFourierFourier1D = np.arange(-1/(2*self.parameters.dxFourier1D),
                                                            1/(2*self.parameters.dxFourier1D),
                                                            1/(self.parameters.dxFourier1D*self.parameters.XAxisFourier1D.shape[0]))
        self.parameters.XAxisFilterFourier1D = np.copy(self.parameters.XAxisFourier1D)
        self.parameters.RangeFilterFourierFourier1D = np.copy(self.parameters.RangeFourierFourier1D)
        
        for i in range(self.parameters.numberFilter):
            for j in range(self.parameters.numberParameters):
                for k in range(self.parameters.numberParameters2):
                    try:
                        self.parameters.CurveParametersFourier1D[i,j,k] = float(self.ParameterLineEditFourier1D[i,j,k].text())
                    except:
                        self.parameters.CurveParametersFourier1D[0] = 0.0
                        self.ParameterLineEditFourier1D[i,j,k].setText("0.0")

        self.updateImagesFourier1D()

    def updateImagesFourier1D(self):
        """Updates all the Images"""
        self.updateCurvesFourier1D()
        self.updateConvolutionFourier1D()

        self.updateFourierBaseImage()
        self.updateFouriedFourierImage()
        self.updateFourierConvolutionImage()
        self.updateFourierConvolutionFouriedImage()

    def updateCurvesFourier1D(self):
        """Updates the Curve"""
        for i in range(self.parameters.numberFilter):
            if not self.parameters.directFourierCurve1D[i]:
                self.parameters.BaseCurveFourier1D[i] = Fourier1D.create1DFunctions(self.parameters.XAxisFourier1D,
                                                                    self.parameters.CurveParametersFourier1D[i,:,:],
                                                                    self.parameters.CurveTypeFourier1D[i,:],
                                                                    self.parameters.fullRangeFourier1D[i,:])
                self.parameters.FourierCurveFourier1DAbs[i], self.parameters.FourierCurveFourier1D = Fourier1D.FourierTransform1D(self.parameters.BaseCurveFourier1D[i])
            else:
                self.parameters.FourierCurveFourier1DAbs[i] = Fourier1D.create1DFunctions(self.parameters.XAxisFourier1D,
                                                                    self.parameters.CurveParametersFourier1D[i,:,:],
                                                                    self.parameters.CurveTypeFourier1D[i,:],
                                                                    self.parameters.fullRangeFourier1D[i,:])
                self.parameters.BaseCurveFourier1D[i], _ = Fourier1D.InverseFourierTransform1D(self.parameters.FourierCurveFourier1DAbs[i])

    def updateConvolutionFourier1D(self):
        """Updates the Convolution"""
        """if (self.parameters.directFourierCurve1D[i] or self.parameters.directFourierFilter1D[i]):
            self.parameters.ConvolutionFouried1DFourier = self.parameters.FourierCurveFourier1DAbs*self.parameters.FourierFilterFourier1DAbs
            self.parameters.Convolution1DFourier, tmp = Fourier1D.InverseFourierTransform1D(self.parameters.ConvolutionFouried1DFourier)
            #self.parameters.Convolution1DFourier = np.real(self.parameters.Convolution1DFourier)"""
        
        if True:
            for i in range(self.parameters.numberFilter):
                if i == 0:
                    self.parameters.Convolution1DFourier = np.copy(self.parameters.BaseCurveFourier1D[i])
                    self.parameters.ConvolutionFouried1DFourier = np.copy(self.parameters.FourierCurveFourier1DAbs[i])
                else:
                    self.parameters.Convolution1DFourier = np.convolve(self.parameters.Convolution1DFourier,self.parameters.BaseCurveFourier1D[i],mode = 'same') * (self.parameters.XAxisFourier1D[1]-self.parameters.XAxisFourier1D[0])
                    self.parameters.ConvolutionFouried1DFourier *= self.parameters.FourierCurveFourier1DAbs[i]
 
    def updateFourierBaseImage(self):
        """Updates the Basic Fourier Image"""
        for i in range(self.parameters.numberFilter):
            try:
                self.Fourier1DBaseImage[i].axes.cla()
            except:
                pass
            self.Fourier1DBaseImage[i].axes.plot(self.parameters.XAxisFourier1D,self.parameters.BaseCurveFourier1D[i])

            self.Fourier1DBaseImage[i].axes.grid()
            self.Fourier1DBaseImage[i].axes.set_xlabel("x")
            self.Fourier1DBaseImage[i].axes.set_ylabel("y")
            self.Fourier1DBaseImage[i].axes.set_title(AnalysisStrings.CurvesTypeFourier1D[f"{self.parameters.CurveTypeFourier1D[i,0]}"][f"{self.language}"])

            self.Fourier1DBaseImage[i].draw()
    def updateFouriedFourierImage(self):
        """Updates the Basic Fourier Image"""
        for i in range(self.parameters.numberFilter):
            try:
                self.Fourier1DFouriedImage[i].axes.cla()
            except:
                pass
            self.Fourier1DFouriedImage[i].axes.plot(self.parameters.RangeFourierFourier1D,self.parameters.FourierCurveFourier1DAbs[i])

            self.Fourier1DFouriedImage[i].axes.grid()
            self.Fourier1DFouriedImage[i].axes.set_xlabel("$k_x$")
            self.Fourier1DFouriedImage[i].axes.set_ylabel("$k_y$")
            self.Fourier1DFouriedImage[i].axes.set_title(AnalysisStrings.FourierGraphNameFourier1D[f"{self.language}"] + 
                                                        AnalysisStrings.CurvesTypeFourier1D[f"{self.parameters.CurveTypeFourier1D[i,0]}"][f"{self.language}"])

            #self.Fourier1DFouriedImage.axes.set_xlim(-4,4)
            self.Fourier1DFouriedImage[i].draw()

    def updateFourierConvolutionImage(self):
        """Updates the Basic Fourier Image"""
        try:
            self.Fourier1DConvolvedImage.axes.cla()
        except:
            pass

        self.Fourier1DConvolvedImage.axes.plot(self.parameters.XAxisFourier1D,self.parameters.Convolution1DFourier)

        self.Fourier1DConvolvedImage.axes.grid()
        self.Fourier1DConvolvedImage.axes.set_xlabel("x")
        self.Fourier1DConvolvedImage.axes.set_ylabel("y")
        self.Fourier1DConvolvedImage.axes.set_title(AnalysisStrings.ConvolutionGraphNameFourier1D[f"{self.language}"])

        self.Fourier1DConvolvedImage.draw()

    def updateFourierConvolutionFouriedImage(self):
        """Updates the Basic Fourier Image"""
        try:
            self.Fourier1DConvolvedFouriedImage.axes.cla()
        except:
            pass

        self.Fourier1DConvolvedFouriedImage.axes.plot(self.parameters.RangeFourierFourier1D,self.parameters.ConvolutionFouried1DFourier)

        self.Fourier1DConvolvedFouriedImage.axes.grid()
        self.Fourier1DConvolvedFouriedImage.axes.set_xlabel("$k_x$")
        self.Fourier1DConvolvedFouriedImage.axes.set_ylabel("$k_y$")
        self.Fourier1DConvolvedFouriedImage.axes.set_title(AnalysisStrings.ConvolutionFouriedGraphNameFourier1D[f"{self.language}"])

        self.Fourier1DConvolvedFouriedImage.draw()

    def update_Combo_ImageFilters(self):
        """Updates the Curve Type"""
        name_tmp = self.ImageTypeComboBoxFilters.currentText()
        for dict, names in AnalysisStrings.ImageNameFilters.items():
            if name_tmp in names.values():
                self.parameters.ImageFiltersName = dict
        self.parameters.ImageFilters = mpimg.imread(f'{basedir}/AnalysisImage/{self.parameters.ImageFiltersName}.pgm')
        self.updateImagesFilters()

    def update_Combo_CurveFilters(self):
        """Updates the Curve Type"""
        name_tmp = self.FilterTypeComboBoxFilters.currentText()
        for dict, names in AnalysisStrings.CurvesTypeFilters.items():
            if name_tmp in names.values():
                self.parameters.FilterFiltersName = dict
        self.updateImagesFilters()

    def update_Check_FullRangeFilters(self):
        """Updates the Boolean for Full Range"""
        if self.ParametersFullRangeCheckBox.isChecked():
            self.parameters.fullRangeFilters = True
        else:
            self.parameters.fullRangeFilters = False
        self.updateImagesFilters()

    def update_Check_logViewFilters(self):
        """Updates the Full View for Filters"""
        if self.LogViewComboBoxFilters.isChecked():
            self.parameters.logViewFourier = True
        else:
            self.parameters.logViewFourier = False
        self.updateImagesFilters()

    def updateParametersFilters(self):
        """Updates the Parameters of the Filters"""
        try:
            self.parameters.ParametersFilters[0] = float(self.Parameter1LineEditFilters.text())
        except:
            self.parameters.ParametersFilters[0] = 30
        try:
            self.parameters.ParametersFilters[1] = float(self.Parameter2LineEditFilters.text())
        except:
            self.parameters.ParametersFilters[1] = 25/46
        self.updateImagesFilters()

    def updateImagesFilters(self):
        """Updates all the Images of Filters"""
        self.updateCurvesFilters()
        self.updateBaseImageFilters()
        self.updateFilterImageFilters()
        self.updateFourierBaseImageFilters()
        self.updateFourierFilterImageFilters()
        self.updateConvolvedImageFilters()

    def updateCurvesFilters(self):
        """Updates the Data of Filters"""
        if self.parameters.FilterFiltersName not in ["Bilateral"]:
            self.parameters.FilterFilters = Filters.createFilters(self.parameters.ImageFilters,self.parameters.ParametersFilters,
                                                    self.parameters.FilterFiltersName,self.parameters.fullRangeFilters)
        if self.parameters.FilterFiltersName in ["Low Pass Flat", "High Pass Flat"]:
            self.parameters.FilterFourierAbsFilters = np.copy(self.parameters.FilterFilters)
            self.parameters.FilterFourierFilters = scipy.fft.fftshift(np.copy(self.parameters.FilterFilters))
            self.parameters.FilterFilters, _ = Filters.InverseFourierTransform(self.parameters.FilterFourierFilters) 
        elif self.parameters.FilterFiltersName in ["Bilateral"]:
            pass
        else:
            self.parameters.FilterFourierAbsFilters, self.parameters.FilterFourierFilters = Filters.FourierTransform(self.parameters.FilterFilters)

        if self.parameters.FilterFiltersName not in ["Bilateral"]:
            self.parameters.ImageFourierAbsFilters, self.parameters.ImageFourierFilters = Filters.FourierTransform(self.parameters.ImageFilters)
            self.parameters.ImageFourierFilteredAbsFilters, self.parameters.ImageFourierFilteredFilters = Filters.FourierConvolution(self.parameters.FilterFourierFilters,self.parameters.ImageFourierFilters)

            self.parameters.ImageConvolvedAbsFilters, self.parameters.ImageConvolvedFilters = Filters.InverseFourierTransform(self.parameters.ImageFourierFilteredFilters) 
            if self.parameters.FilterFiltersName in ["Low Pass Flat", "High Pass Flat"]:
                self.parameters.ImageConvolvedAbsFilters = scipy.fft.fftshift(self.parameters.ImageConvolvedAbsFilters,axes=[0,1])
        elif self.parameters.FilterFiltersName in ["Bilateral"]:
            self.parameters.ImageConvolvedAbsFilters = np.zeros_like(self.parameters.ImageFilters)
            self.parameters.FilterFilters = np.zeros_like(self.parameters.ImageFilters)
            self.parameters.FilterFourierAbsFilters = np.zeros_like(self.parameters.ImageFilters)
            self.parameters.ImageFourierAbsFilters = np.zeros_like(self.parameters.ImageFilters)
            self.parameters.FilterFourierFilters = np.zeros_like(self.parameters.ImageFilters)
            for i in range(self.parameters.ImageFilters.shape[0]):
                for j in range(self.parameters.ImageFilters.shape[1]):
                    N = 3
                    C = 0
                    numerator = 0
                    for k in range(-N,N+1):
                        for l in range(-N,N+1):
                            if i + k >= 0 and i + k <= self.parameters.ImageFilters.shape[0] - 1:
                                if j + l >= 0 and j + l <= self.parameters.ImageFilters.shape[1] - 1:
                                    exp1 = np.exp((k**2 + l**2)**(1)/(2*self.parameters.ParametersFilters[0]))
                                    exp2 = np.exp((self.parameters.ImageFilters[i, j]-self.parameters.ImageFilters[i + k, j + l])**2/(2*self.parameters.ImageFilters[i, j]*self.parameters.ParametersFilters[1]))
                                    w = exp1 * exp2
                                    C += w
                                    numerator += w * self.parameters.ImageFilters[i + k, j + l]
                    self.parameters.ImageConvolvedAbsFilters[i,j] = numerator/C
    def updateBaseImageFilters(self):
        try:
            self.BaseImageFilters.axes.cla()
        except : pass

        self.BaseImageFilters.axes.pcolormesh(self.parameters.ImageFilters,cmap = 'Greys_r')
        self.BaseImageFilters.axes.set_title(AnalysisStrings.ImageNameFilters[f"{self.parameters.ImageFiltersName}"][f"{self.language}"])
        self.BaseImageFilters.axes.invert_yaxis()

        self.BaseImageFilters.draw()
    def updateFilterImageFilters(self):
        try:
            self.FilterImageFilters.axes.cla()
        except : pass
        if self.parameters.logViewFourier:
            self.FilterImageFilters.axes.pcolormesh(np.log(self.parameters.FilterFilters + 1e-10),cmap = 'Greys_r')
        else:
            self.FilterImageFilters.axes.pcolormesh(self.parameters.FilterFilters,cmap = 'Greys_r')

        #self.FilterImageFilters.axes.pcolormesh(self.parameters.FilterFilters,cmap = 'Greys_r')
        self.FilterImageFilters.axes.set_title(AnalysisStrings.CurvesTypeFilters[f"{self.parameters.FilterFiltersName}"][f"{self.language}"])

        self.FilterImageFilters.draw()
    def updateFourierBaseImageFilters(self):
        try:
            self.FourierBaseImageFilters.axes.cla()
        except : pass

        if self.parameters.logViewFourier:
            self.FourierBaseImageFilters.axes.pcolormesh(np.log(self.parameters.ImageFourierAbsFilters + 1e-10),cmap = 'Greys_r')
        else:
            self.FourierBaseImageFilters.axes.pcolormesh(self.parameters.ImageFourierAbsFilters,cmap = 'Greys_r')
        self.FourierBaseImageFilters.axes.set_title(AnalysisStrings.ImageNameFilters[f"{self.parameters.ImageFiltersName}"][f"{self.language}"]+" "+AnalysisStrings.FourierTitleFilters[f"{self.language}"])

        self.FourierBaseImageFilters.draw()
    def updateFourierFilterImageFilters(self):
        try:
            self.FourierFilterImageFilters.axes.cla()
        except : pass

        if self.parameters.logViewFourier:
            self.FourierFilterImageFilters.axes.pcolormesh(np.log(self.parameters.FilterFourierAbsFilters),cmap = 'Greys_r')
        else:
            self.FourierFilterImageFilters.axes.pcolormesh(self.parameters.FilterFourierAbsFilters,cmap = 'Greys_r')
        self.FourierFilterImageFilters.axes.set_title(AnalysisStrings.CurvesTypeFilters[f"{self.parameters.FilterFiltersName}"][f"{self.language}"]+" "+AnalysisStrings.FourierTitleFilters[f"{self.language}"])

        self.FourierFilterImageFilters.draw()
    def updateConvolvedImageFilters(self):
        try:
            self.ConvolutedBaseImageFilters.axes.cla()
        except : pass

        self.ConvolutedBaseImageFilters.axes.pcolormesh(self.parameters.ImageConvolvedAbsFilters,cmap = 'Greys_r')
        self.ConvolutedBaseImageFilters.axes.set_title(AnalysisStrings.ImageNameFilters[f"{self.parameters.ImageFiltersName}"][f"{self.language}"]+" "+AnalysisStrings.GraphConvolutedFilters[f"{self.language}"])
        self.ConvolutedBaseImageFilters.axes.invert_yaxis()

        self.ConvolutedBaseImageFilters.draw()
    def updateParametersCartesianComplexNumber(self):
        """Updates the Cartesian Parameters of the Complex Numbers"""
        try:
            x = float(self.Parameter1ComplexNumber.text())
            y = float(self.Parameter1jComplexNumber.text())
            self.parameters.ComplexNumber1 = complex(x,y)
        except:
            self.parameters.ComplexNumber1 = 0+0j
        try:
            x = float(self.Parameter2ComplexNumber.text())
            y = float(self.Parameter2jComplexNumber.text())
            self.parameters.ComplexNumber2 = complex(x,y)
        except:
            self.parameters.ComplexNumber2 = 0+0j
        self.Parameter1PolarRComplexNumber.setText(f"{(abs(self.parameters.ComplexNumber1)):.2f}")
        self.Parameter1PolarThetaComplexNumber.setText(f"{(cmath.phase(self.parameters.ComplexNumber1)):.2f}")
        self.Parameter2PolarRComplexNumber.setText(f"{(abs(self.parameters.ComplexNumber2)):.2f}")
        self.Parameter2PolarThetaComplexNumber.setText(f"{(cmath.phase(self.parameters.ComplexNumber2)):.2f}")
        self.updateResultOperationComplexNumber()
    def updateParametersPolarComplexNumber(self):
        """Updates the Polar Parameters of the Complex Numbers"""
        try:
            x = float(self.Parameter1PolarRComplexNumber.text())
            y = float(self.Parameter1PolarThetaComplexNumber.text())
            self.parameters.ComplexNumber1 = cmath.rect(x,y)
        except:
            self.parameters.ComplexNumber1 = 0+0j
        try:
            x = float(self.Parameter2PolarRComplexNumber.text())
            y = float(self.Parameter2PolarThetaComplexNumber.text())
            self.parameters.ComplexNumber2 = cmath.rect(x,y)
        except:
            self.parameters.ComplexNumber2 = 0+0j
        self.Parameter1ComplexNumber.setText(f"{(self.parameters.ComplexNumber1.real):.2f}")
        self.Parameter1jComplexNumber.setText(f"{(self.parameters.ComplexNumber1.imag):.2f}")
        self.Parameter2ComplexNumber.setText(f"{(self.parameters.ComplexNumber2.real):.2f}")
        self.Parameter2jComplexNumber.setText(f"{(self.parameters.ComplexNumber2.imag):.2f}")

        self.updateResultOperationComplexNumber()

    def update_Combo_ComplexNumber(self):
        """Updates the Operation for Complex Numbers"""
        name_tmp = self.OperationComboBoxComplexNumber.currentText()
        for dict, names in AnalysisStrings.ComplexNumberOperation.items():
            if name_tmp in names.values():
                self.parameters.ComplexNumberOperation = dict
        self.updateResultOperationComplexNumber()
    def update_ComboClicker_ComplexNumber(self):
        """Updates the Clicker for Complex Numbers"""
        self.parameters.ComplexNumberClicker = self.ClickerComboBoxComplexNumber.currentText()


    def updateResultOperationComplexNumber(self):
        """Do the computation for the complex numbers"""
        if self.parameters.ComplexNumberOperation == "+":
            self.parameters.ComplexNumberResult = self.parameters.ComplexNumber1 + self.parameters.ComplexNumber2
            self.parameters.ComplexNumberLine = self.parameters.ComplexNumber1 + (self.parameters.ComlexAlphaFactor*self.parameters.ComplexNumber2)
        elif self.parameters.ComplexNumberOperation == "-":
            self.parameters.ComplexNumberResult = self.parameters.ComplexNumber1 - self.parameters.ComplexNumber2
            self.parameters.ComplexNumberLine = self.parameters.ComplexNumber1 - (self.parameters.ComlexAlphaFactor*self.parameters.ComplexNumber2)
        elif self.parameters.ComplexNumberOperation == "*":
            self.parameters.ComplexNumberResult = self.parameters.ComplexNumber1 * self.parameters.ComplexNumber2
            self.parameters.ComplexNumberLine = self.parameters.ComplexNumber1 * (self.parameters.ComlexAlphaFactor*self.parameters.ComplexNumber2)
        elif self.parameters.ComplexNumberOperation == "/":
            self.parameters.ComplexNumberResult = self.parameters.ComplexNumber1 / self.parameters.ComplexNumber2
            self.parameters.ComplexNumberLine = self.parameters.ComplexNumber1 / (self.parameters.ComlexAlphaFactor*self.parameters.ComplexNumber2)
        elif self.parameters.ComplexNumberOperation == "^":
            self.parameters.ComplexNumberResult = self.parameters.ComplexNumber1 ** self.parameters.ComplexNumber2
            self.parameters.ComplexNumberLine = self.parameters.ComplexNumber1 ** (self.parameters.ComlexAlphaFactor*self.parameters.ComplexNumber2)
        elif self.parameters.ComplexNumberOperation == "Comp":
            self.parameters.ComplexNumberResult = complex(self.parameters.ComplexNumber1.real,-self.parameters.ComplexNumber1.imag)
        elif self.parameters.ComplexNumberOperation == "ln":
            self.parameters.ComplexNumberResult = cmath.log(self.parameters.ComplexNumber1)
            for i in range(self.parameters.ComlexAlphaFactor.shape[0]):
                self.parameters.ComplexNumberLine[i] = cmath.log(self.parameters.ComlexAlphaFactor[i]*self.parameters.ComplexNumber1)
        elif self.parameters.ComplexNumberOperation == "log10":
            self.parameters.ComplexNumberResult = cmath.log10(self.parameters.ComplexNumber1)
            for i in range(self.parameters.ComlexAlphaFactor.shape[0]):
                self.parameters.ComplexNumberLine[i] = cmath.log10(self.parameters.ComlexAlphaFactor[i]*self.parameters.ComplexNumber1)
        elif self.parameters.ComplexNumberOperation == "sin":
            self.parameters.ComplexNumberResult = cmath.sin(self.parameters.ComplexNumber1)
            for i in range(self.parameters.ComlexAlphaFactor.shape[0]):
                self.parameters.ComplexNumberLine[i] = cmath.sin(self.parameters.ComlexAlphaFactor[i]*self.parameters.ComplexNumber1)
        elif self.parameters.ComplexNumberOperation == "cos":
            self.parameters.ComplexNumberResult = cmath.cos(self.parameters.ComplexNumber1)
            for i in range(self.parameters.ComlexAlphaFactor.shape[0]):
                self.parameters.ComplexNumberLine[i] = cmath.cos(self.parameters.ComlexAlphaFactor[i]*self.parameters.ComplexNumber1)
        elif self.parameters.ComplexNumberOperation == "tan":
            self.parameters.ComplexNumberResult = cmath.tan(self.parameters.ComplexNumber1)
            for i in range(self.parameters.ComlexAlphaFactor.shape[0]):
                self.parameters.ComplexNumberLine[i] = cmath.tan(self.parameters.ComlexAlphaFactor[i]*self.parameters.ComplexNumber1)
        elif self.parameters.ComplexNumberOperation == "exp":
            self.parameters.ComplexNumberResult = cmath.exp(self.parameters.ComplexNumber1)
            for i in range(self.parameters.ComlexAlphaFactor.shape[0]):
                self.parameters.ComplexNumberLine[i] = cmath.exp(self.parameters.ComlexAlphaFactor[i]*self.parameters.ComplexNumber1)
        elif self.parameters.ComplexNumberOperation == "arcsin":
            self.parameters.ComplexNumberResult = cmath.asin(self.parameters.ComplexNumber1)
            for i in range(self.parameters.ComlexAlphaFactor.shape[0]):
                self.parameters.ComplexNumberLine[i] = cmath.asin(self.parameters.ComlexAlphaFactor[i]*self.parameters.ComplexNumber1)
        elif self.parameters.ComplexNumberOperation == "arccos":
            self.parameters.ComplexNumberResult = cmath.acos(self.parameters.ComplexNumber1)
            for i in range(self.parameters.ComlexAlphaFactor.shape[0]):
                self.parameters.ComplexNumberLine[i] = cmath.acos(self.parameters.ComlexAlphaFactor[i]*self.parameters.ComplexNumber1)
        elif self.parameters.ComplexNumberOperation == "arctan":
            self.parameters.ComplexNumberResult = cmath.atan(self.parameters.ComplexNumber1)
            for i in range(self.parameters.ComlexAlphaFactor.shape[0]):
                self.parameters.ComplexNumberLine[i] = cmath.atan(self.parameters.ComlexAlphaFactor[i]*self.parameters.ComplexNumber1)

        self.Parameter3ComplexNumber.setText(f"{(self.parameters.ComplexNumberResult.real):.2f}")
        self.Parameter3jComplexNumber.setText(f"{(self.parameters.ComplexNumberResult.imag):.2f}")
        self.Parameter3PolarRComplexNumber.setText(f"{(abs(self.parameters.ComplexNumberResult)):.2f}")
        self.Parameter3PolarThetaComplexNumber.setText(f"{(cmath.phase(self.parameters.ComplexNumberResult)):.2f}")

        self.updateImagesComplexNumber()

    def updateImagesComplexNumber(self):
        """Updates the Image of the Complex Numbers"""
        try:
            self.ImageComplexNumbers.axes.cla()
        except : pass
        self.ImageComplexNumbers.axes.plot(self.parameters.ComplexNumber1.real,
                                           self.parameters.ComplexNumber1.imag,
                                           color = "r",
                                           marker = "o")
        self.ImageComplexNumbers.axes.plot(self.parameters.ComplexNumber2.real,
                                           self.parameters.ComplexNumber2.imag,
                                           color="g",
                                           marker = "o")
        self.ImageComplexNumbers.axes.plot(self.parameters.ComplexNumberResult.real,
                                           self.parameters.ComplexNumberResult.imag,
                                           color="b",
                                           marker = "*")
        if self.parameters.ComplexNumberOperation in ["+","-","/","*",
                                                      "^","ln","log10",
                                                      "sin","cos","tan","exp",
                                                      "arcsin","arccos","arctan"]:
            c = self.parameters.ComlexAlphaFactor
            col = cm.jet((c-np.min(c))/(np.max(c)-np.min(c)))
            for i in range(self.parameters.ComlexAlphaFactor.shape[0]-1):
                self.ImageComplexNumbers.axes.plot([self.parameters.ComplexNumberLine[i].real,self.parameters.ComplexNumberLine[i+1].real],
                                               [self.parameters.ComplexNumberLine[i].imag,self.parameters.ComplexNumberLine[i+1].imag],
                                               color = col[i])
        self.ImageComplexNumbers.axes.axvline(0, color = "k",alpha = 0.5)
        self.ImageComplexNumbers.axes.axhline(0, color = "k",alpha = 0.5)
        self.ImageComplexNumbers.axes.set_xlim(left = min([-5,min([0,
                                                        self.parameters.ComplexNumber1.real,
                                                        self.parameters.ComplexNumber2.real,
                                                        self.parameters.ComplexNumberResult.real])-1]),
                                                right= max([5,max([0,
                                                        self.parameters.ComplexNumber1.real,
                                                        self.parameters.ComplexNumber2.real,
                                                        self.parameters.ComplexNumberResult.real])+1]))
        self.ImageComplexNumbers.axes.set_ylim(bottom = min([-5,min([0,
                                                             self.parameters.ComplexNumber1.imag,
                                                             self.parameters.ComplexNumber2.imag,
                                                             self.parameters.ComplexNumberResult.imag])-1]),
                                                top = max([5,max([0,
                                                             self.parameters.ComplexNumber1.imag,
                                                             self.parameters.ComplexNumber2.imag,
                                                             self.parameters.ComplexNumberResult.imag])+1]))

        self.ImageComplexNumbers.axes.grid()
        self.ImageComplexNumbers.axes.set_xlabel(AnalysisStrings.ComplexNumberImageXAxis[f"{self.language}"])
        self.ImageComplexNumbers.axes.set_ylabel(AnalysisStrings.ComplexNumberImageYAxis[f"{self.language}"])
        self.ImageComplexNumbers.axes.set_title(AnalysisStrings.ComplexNumberImageTitle[f"{self.language}"])
        self.ImageComplexNumbers.draw()

    def onClick(self,event,which):
        """Allows to click on an image and update the interface"""
        ix, iy = event.xdata, event.ydata
        which.coords = []
        which.coords.append((ix, iy))
        if len(which.coords) == 2:
            which.fig.canvas.mpl_disconnect(self.cid)
        if which == self.ImageComplexNumbers:
            if self.parameters.ComplexNumberClicker == "1":
                self.parameters.ComplexNumber1 = complex(ix,iy)
                self.Parameter1ComplexNumber.setText(f"{(ix):.2f}")
                self.Parameter1jComplexNumber.setText(f"{(iy):.2f}")
            elif self.parameters.ComplexNumberClicker == "2":
                self.parameters.ComplexNumber2 = complex(ix,iy)
                self.Parameter2ComplexNumber.setText(f"{(ix):.2f}")
                self.Parameter2jComplexNumber.setText(f"{(iy):.2f}")
            else:
                if self.complexClicker > 0 :
                    self.parameters.ComplexNumber1 = complex(ix,iy)
                    self.Parameter1ComplexNumber.setText(f"{(ix):.2f}")
                    self.Parameter1jComplexNumber.setText(f"{(iy):.2f}")                    
                elif self.complexClicker < 0 :
                    self.parameters.ComplexNumber2 = complex(ix,iy)
                    self.Parameter2ComplexNumber.setText(f"{(ix):.2f}")
                    self.Parameter2jComplexNumber.setText(f"{(iy):.2f}")
                self.complexClicker *= -1
            self.updateParametersCartesianComplexNumber()
class MplCanvas(FigureCanvasQTAgg):
    """Class for the images and the graphs as a widget"""
    def __init__(self, parent=None, width:float=5, height:float=4, dpi:int=75):
        """Creates an empty figure with axes and fig as parameters"""
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout= True)
        self.axes = fig.add_subplot(111)
        self.fig = fig
        super(MplCanvas, self).__init__(fig)
###
if __name__ == "__main__":
    os.system('clear')
    print(f"Starting program at {time.strftime('%H:%M:%S')}")
    initial = time.time()
    app = QApplication([])
    window=AnalysisWindow()
    window.show()
    sys.exit(app.exec())
