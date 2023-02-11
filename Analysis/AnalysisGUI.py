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
import matplotlib.image as mpimg
import scipy.fft                      #Pour la transformée de Fourier

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
        super().__init__(parent=parent)
        self.setMinimumSize(1200, 700)
        self.setWindowTitle(AnalysisStrings.WindowName[f"{self.language}"])

        self.generalLayoutFourier1D = QGridLayout()
        self.generalLayoutFilters = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()

        centralWidgetFourier1D = QWidget(self)
        centralWidgetFilters = QWidget(self)
        centralWidgetReadMe = QWidget(self)

        centralWidgetFourier1D.setLayout(self.generalLayoutFourier1D)
        centralWidgetFilters.setLayout(self.generalLayoutFilters)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)

        self.tabs.addTab(centralWidgetFourier1D,AnalysisStrings.Fourier1DTabName[f"{self.language}"])
        self.tabs.addTab(centralWidgetFilters,AnalysisStrings.FiltersName[f"{self.language}"])
        self.tabs.addTab(centralWidgetReadMe,AnalysisStrings.ReadMeName[f"{self.language}"])

        self.setCentralWidget(self.tabs)

        #Fourier 1D Tab
        self._createBaseFunctionImageFourier1D()
        self._createFourierFunctionImageFourier1D()
        self._createNoisedFunctionImageFourier1D()
        self._createParametersButtonsFourier1D()
        #Filters Tab
        self._createBaseImageFilters()
        self._createFilterImageFilters()
        self._createFourierBaseImageFilters()
        self._createFourierFilterFilters()
        self._createConvolvedImageFilters()
        self._createParametersButtonsFilters()
        #Exit Button
        self._createExitButton()

        self.generalLayoutFourier1D.setColumnStretch(1,5)
        self.generalLayoutFourier1D.setColumnStretch(2,5)
        self.generalLayoutFilters.setColumnStretch(1,5)
        self.generalLayoutFilters.setColumnStretch(2,5)
    ###Create Interface###
    def _createBaseFunctionImageFourier1D(self):
        """Creates an Image for the Base function of Fourier 1D"""
        self.Fourier1DBaseImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutFourier1D.addWidget(self.Fourier1DBaseImage,self.currentLineFourier1D,1)
        self.currentLineFourier1D += 1
    def _createParametersButtonsFourier1D(self):
        """Creates the Buttons for the Parameters of the Fourier 1D"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.CurveTypeComboBoxFourier1D = QComboBox()
        for _, names in AnalysisStrings.CurvesTypeFourier1D.items():
            self.CurveTypeComboBoxFourier1D.addItem(names[f"{self.language}"])
        self.CurveTypeComboBoxFourier1D.setCurrentText(self.parameters.CurveTypeFourier1D)
        self.CurveTypeComboBoxFourier1D.activated[str].connect(self.update_Combo_CurveFourier1D)

        self.FullRangeComboBoxFourier1D = QCheckBox()
        self.FullRangeComboBoxFourier1D.stateChanged.connect(self.update_Check_FullRangeFourier1D)

        self.RangeMinLineEditFourier1D = QLineEdit()
        self.RangeMaxLineEditFourier1D = QLineEdit()
        self.Parameter1LineEditFourier1D = QLineEdit()
        self.Parameter2LineEditFourier1D = QLineEdit()
        self.Parameter3LineEditFourier1D = QLineEdit()
        self.Parameter4LineEditFourier1D = QLineEdit()
        self.Parameter5LineEditFourier1D = QLineEdit()
        self.Parameter6LineEditFourier1D = QLineEdit()
        self.Parameter7LineEditFourier1D = QLineEdit()
        self.Parameter8LineEditFourier1D = QLineEdit()

        self.RangeMinLineEditFourier1D.setFixedWidth(90)
        self.RangeMaxLineEditFourier1D.setFixedWidth(90)
        self.Parameter1LineEditFourier1D.setFixedWidth(90)
        self.Parameter2LineEditFourier1D.setFixedWidth(90)
        self.Parameter3LineEditFourier1D.setFixedWidth(90)
        self.Parameter4LineEditFourier1D.setFixedWidth(90)
        self.Parameter5LineEditFourier1D.setFixedWidth(90)
        self.Parameter6LineEditFourier1D.setFixedWidth(90)
        self.Parameter7LineEditFourier1D.setFixedWidth(90)
        self.Parameter8LineEditFourier1D.setFixedWidth(90)

        self.RangeMinLineEditFourier1D.setText(str(self.parameters.CurveRangeFourier1D[0]))
        self.RangeMaxLineEditFourier1D.setText(str(self.parameters.CurveRangeFourier1D[1]))
        self.Parameter1LineEditFourier1D.setText(str(self.parameters.CurveParametersFourier1D[0]))
        self.Parameter2LineEditFourier1D.setText(str(self.parameters.CurveParametersFourier1D[1]))
        self.Parameter3LineEditFourier1D.setText(str(self.parameters.CurveParametersFourier1D[2]))
        self.Parameter4LineEditFourier1D.setText(str(self.parameters.CurveParametersFourier1D[3]))
        self.Parameter5LineEditFourier1D.setText(str(self.parameters.CurveParametersFourier1D[4]))
        self.Parameter6LineEditFourier1D.setText(str(self.parameters.CurveParametersFourier1D[5]))
        self.Parameter7LineEditFourier1D.setText(str(self.parameters.CurveParametersFourier1D[6]))
        self.Parameter8LineEditFourier1D.setText(str(self.parameters.CurveParametersFourier1D[7]))

        self.RangeMinLineEditFourier1D.editingFinished.connect(self.updateParametersFourier1D)
        self.RangeMaxLineEditFourier1D.editingFinished.connect(self.updateParametersFourier1D)
        self.Parameter1LineEditFourier1D.editingFinished.connect(self.updateParametersFourier1D)
        self.Parameter2LineEditFourier1D.editingFinished.connect(self.updateParametersFourier1D)
        self.Parameter3LineEditFourier1D.editingFinished.connect(self.updateParametersFourier1D)
        self.Parameter4LineEditFourier1D.editingFinished.connect(self.updateParametersFourier1D)
        self.Parameter5LineEditFourier1D.editingFinished.connect(self.updateParametersFourier1D)
        self.Parameter6LineEditFourier1D.editingFinished.connect(self.updateParametersFourier1D)
        self.Parameter7LineEditFourier1D.editingFinished.connect(self.updateParametersFourier1D)
        self.Parameter8LineEditFourier1D.editingFinished.connect(self.updateParametersFourier1D)


        layout.addWidget(self.CurveTypeComboBoxFourier1D,1,1)
        layout.addWidget(QLabel(AnalysisStrings.FullRangeFourier1D[f"{self.language}"]),2,1)
        layout.addWidget(self.FullRangeComboBoxFourier1D,2,2)
        layout.addWidget(self.RangeMinLineEditFourier1D,2,3)
        layout.addWidget(self.RangeMaxLineEditFourier1D,2,4)
        layout.addWidget(QLabel(AnalysisStrings.Parameters1Fourier1D[f"{self.language}"]),3,1)
        layout.addWidget(self.Parameter1LineEditFourier1D,3,2)
        layout.addWidget(self.Parameter2LineEditFourier1D,3,3)
        layout.addWidget(QLabel(AnalysisStrings.Parameters2Fourier1D[f"{self.language}"] + " 1"),4,1)
        layout.addWidget(self.Parameter3LineEditFourier1D,4,2)
        layout.addWidget(self.Parameter4LineEditFourier1D,4,3)
        layout.addWidget(QLabel(AnalysisStrings.Parameters2Fourier1D[f"{self.language}"] + " 2"),5,1)
        layout.addWidget(self.Parameter5LineEditFourier1D,5,2)
        layout.addWidget(self.Parameter6LineEditFourier1D,5,3)
        layout.addWidget(QLabel(AnalysisStrings.Parameters2Fourier1D[f"{self.language}"] + " 3"),6,1)
        layout.addWidget(self.Parameter7LineEditFourier1D,6,2)
        layout.addWidget(self.Parameter8LineEditFourier1D,6,3)

        self.generalLayoutFourier1D.addWidget(subWidget,self.currentLineFourier1D,2)
        self.currentLineFourier1D += 1
    def _createFourierFunctionImageFourier1D(self):
        """Creates an Image for the Fourier of the function of Fourier 1D"""
        self.Fourier1DFourierImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutFourier1D.addWidget(self.Fourier1DFourierImage,self.currentLineFourier1D,1)
    def _createNoisedFunctionImageFourier1D(self):
        """Creates an Image for the Base function of Fourier 1D"""
        self.Fourier1DNoiseImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutFourier1D.addWidget(self.Fourier1DNoiseImage,self.currentLineFourier1D,2)
        self.currentLineFourier1D += 1

        self.updateImagesFourier1D()

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
    def _createExitButton(self):
        """Creates exit buttons"""
        self.exitFourier1D = QPushButton(AnalysisStrings.ExitButton[f"{self.language}"])
        self.exitFilters = QPushButton(AnalysisStrings.ExitButton[f"{self.language}"])
        self.exitFourier1D.setToolTip(AnalysisStrings.ExitButtonTooltip[f"{self.language}"])
        self.exitFilters.setToolTip(AnalysisStrings.ExitButtonTooltip[f"{self.language}"])

        self.exitFourier1D.clicked.connect(self.close)
        self.exitFilters.clicked.connect(self.close)
        self.generalLayoutFourier1D.addWidget(self.exitFourier1D,self.currentLineFourier1D+1,3)  
        self.generalLayoutFilters.addWidget(self.exitFilters,self.currentLineFilters+1,3)  
        self.currentLineFourier1D += 1
        self.currentLineFilters += 1
    ###Update Interface###
    def update_Combo_CurveFourier1D(self):
        """Updates the Curve Type"""
        name_tmp = self.CurveTypeComboBoxFourier1D.currentText()
        for dict, names in AnalysisStrings.CurvesTypeFourier1D.items():
            if name_tmp in names.values():
                self.parameters.CurveTypeFourier1D = dict
        self.updateImagesFourier1D()

    def update_Check_FullRangeFourier1D(self):
        """Updates the Boolean for Full Range"""
        if self.FullRangeComboBoxFourier1D.isChecked():
            self.parameters.fullRangeFourier1D = True
        else:
            self.parameters.fullRangeFourier1D = False
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
        try:
            self.parameters.CurveParametersFourier1D[0] = float(self.Parameter1LineEditFourier1D.text())
        except:
            self.parameters.CurveParametersFourier1D[0] = 1.0
        try:
            self.parameters.CurveParametersFourier1D[1] = float(self.Parameter2LineEditFourier1D.text())
        except:
            self.parameters.CurveParametersFourier1D[1] = 1.0
        try:
            self.parameters.CurveParametersFourier1D[2] = float(self.Parameter3LineEditFourier1D.text())
        except:
            self.parameters.CurveParametersFourier1D[2] = 1.0
        try:
            self.parameters.CurveParametersFourier1D[3] = float(self.Parameter4LineEditFourier1D.text())
        except:
            self.parameters.CurveParametersFourier1D[3] = 1.0
        try:
            self.parameters.CurveParametersFourier1D[4] = float(self.Parameter5LineEditFourier1D.text())
        except:
            self.parameters.CurveParametersFourier1D[4] = 1.0
        try:
            self.parameters.CurveParametersFourier1D[5] = float(self.Parameter6LineEditFourier1D.text())
        except:
            self.parameters.CurveParametersFourier1D[5] = 1.0
        try:
            self.parameters.CurveParametersFourier1D[6] = float(self.Parameter7LineEditFourier1D.text())
        except:
            self.parameters.CurveParametersFourier1D[6] = 1.0
        try:
            self.parameters.CurveParametersFourier1D[7] = float(self.Parameter8LineEditFourier1D.text())
        except:
            self.parameters.CurveParametersFourier1D[7] = 1.0

        self.updateImagesFourier1D()

    def updateImagesFourier1D(self):
        """Updates all the Images"""
        self.updateCurvesFourier1D()
        self.updateFourierBaseImage()
        self.updateFourierFourierImage()

    def updateCurvesFourier1D(self):
        """Updates the Curve"""
        self.parameters.BaseCurveFourier1D = Fourier1D.create1DFunctions(self.parameters.XAxisFourier1D,
                                                                self.parameters.CurveParametersFourier1D,
                                                                self.parameters.CurveTypeFourier1D,
                                                                self.parameters.fullRangeFourier1D)
        self.parameters.FourierCurveFourier1DAbs, self.parameters.FourierCurveFourier1D = Fourier1D.FourierTransform1D(self.parameters.BaseCurveFourier1D)

    def updateFourierBaseImage(self):
        """Updates the Basic Fourier Image"""
        try:
            self.Fourier1DBaseImage.axes.cla()
        except:
            pass
        self.Fourier1DBaseImage.axes.plot(self.parameters.XAxisFourier1D,self.parameters.BaseCurveFourier1D)

        self.Fourier1DBaseImage.axes.grid()
        self.Fourier1DBaseImage.axes.set_xlabel("x")
        self.Fourier1DBaseImage.axes.set_ylabel("y")
        self.Fourier1DBaseImage.axes.set_title(AnalysisStrings.CurvesTypeFourier1D[f"{self.parameters.CurveTypeFourier1D}"][f"{self.language}"])

        self.Fourier1DBaseImage.draw()
    def updateFourierFourierImage(self):
        """Updates the Basic Fourier Image"""
        try:
            self.Fourier1DFourierImage.axes.cla()
        except:
            pass
        self.Fourier1DFourierImage.axes.plot(self.parameters.RangeFourierFourier1D,self.parameters.FourierCurveFourier1DAbs)

        self.Fourier1DFourierImage.axes.grid()
        self.Fourier1DFourierImage.axes.set_xlabel("x")
        self.Fourier1DFourierImage.axes.set_ylabel("y")
        self.Fourier1DFourierImage.axes.set_title(AnalysisStrings.FourierGraphNameFourier1D[f"{self.language}"] + 
                                                    AnalysisStrings.CurvesTypeFourier1D[f"{self.parameters.CurveTypeFourier1D}"][f"{self.language}"])

        self.Fourier1DFourierImage.axes.set_xlim(-4,4)
        self.Fourier1DFourierImage.draw()

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
        self.parameters.FilterFilters = Filters.createFilters(self.parameters.ImageFilters,self.parameters.ParametersFilters,
                                                    self.parameters.FilterFiltersName,self.parameters.fullRangeFilters)
        if self.parameters.FilterFiltersName in ["Low Pass Flat", "High Pass Flat"]:
            self.parameters.FilterFourierAbsFilters = np.copy(self.parameters.FilterFilters)
            self.parameters.FilterFourierFilters = scipy.fft.fftshift(np.copy(self.parameters.FilterFilters))
            self.parameters.FilterFilters, _ = Filters.InverseFourierTransform(self.parameters.FilterFourierFilters) 
        else:
            self.parameters.FilterFourierAbsFilters, self.parameters.FilterFourierFilters = Filters.FourierTransform(self.parameters.FilterFilters)
        self.parameters.ImageFourierAbsFilters, self.parameters.ImageFourierFilters = Filters.FourierTransform(self.parameters.ImageFilters)
        self.parameters.ImageFourierFilteredAbsFilters, self.parameters.ImageFourierFilteredFilters = Filters.FourierConvolution(self.parameters.FilterFourierFilters,self.parameters.ImageFourierFilters)

        self.parameters.ImageConvolvedAbsFilters, self.parameters.ImageConvolvedFilters = Filters.InverseFourierTransform(self.parameters.ImageFourierFilteredFilters) 
        if self.parameters.FilterFiltersName in ["Low Pass Flat", "High Pass Flat"]:
            self.parameters.ImageConvolvedAbsFilters = scipy.fft.fftshift(self.parameters.ImageConvolvedAbsFilters,axes=[0,1])
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

        self.FilterImageFilters.axes.pcolormesh(self.parameters.FilterFilters,cmap = 'Greys_r')
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
