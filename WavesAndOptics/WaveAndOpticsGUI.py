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
    import GUIParametersWaveAndOptics
    import WavesAndOpticsStrings
    import Waves
except:
    import WavesAndOptics.GUIParametersWaveAndOptics as GUIParametersWaveAndOptics
    import WavesAndOptics.WavesAndOpticsStrings as WavesAndOpticsStrings
    import WavesAndOptics.Waves as Waves
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from matplotlib.patches import Circle
from matplotlib.patches import Polygon

size_Image = 200

class WavesAndOpticsWindow(QMainWindow):
    """
    Main window of the GUI.
    """    
    def __init__(self,parent=None,language= "Fr"):
        """Initializes the GUI Window"""
        self.language = language
        self.parameters = GUIParametersWaveAndOptics.GUIParameters()
        self.tabs = QTabWidget()
        self.currentLineSHM = 1
        self.currentLineDamped = 1
        self.currentLine2DWaves = 1
        super().__init__(parent=parent)
        self.setMinimumSize(1200, 700)
        self.setWindowTitle(WavesAndOpticsStrings.WindowName[f"{self.language}"])

        self.generalLayoutSHM = QGridLayout()
        self.generalLayoutDamped = QGridLayout()
        self.generalLayout2DWaves = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()

        centralWidgetSHM = QWidget(self)
        centralWidgetDamped = QWidget(self)
        centralWidget2DWaves = QWidget(self)
        centralWidgetReadMe = QWidget(self)

        centralWidgetSHM.setLayout(self.generalLayoutSHM)
        centralWidgetDamped.setLayout(self.generalLayoutDamped)
        centralWidget2DWaves.setLayout(self.generalLayout2DWaves)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)

        self.tabs.addTab(centralWidgetSHM,WavesAndOpticsStrings.SHMTabName[f"{self.language}"])
        #self.tabs.addTab(centralWidgetDamped,WavesAndOpticsStrings.DampedTabName[f"{self.language}"])
        self.tabs.addTab(centralWidget2DWaves,WavesAndOpticsStrings.Waves2DTabName[f"{self.language}"])
        self.tabs.addTab(centralWidgetReadMe,WavesAndOpticsStrings.ReadMeTabName[f"{self.language}"])

        self.setCentralWidget(self.tabs)

        self._createPositionImageSHM()
        self._createSpeedImageSHM()
        self._createAccelerationImageSHM()
        self._createCircleImageSHM()
        self._createEnergyImageSHM()
        self._createParametersButtonsSHM()
        ###
        self._createFullImage2DWaves()
        self._createTimeSliceImage2DWaves()
        self._createPositionSliceImage2DWaves()
        self._createParametersButtons2DWaves()
        ###
        self._createExitButton()

        self.generalLayoutSHM.setColumnStretch(1,5)
        self.generalLayoutSHM.setColumnStretch(2,5)
        self.generalLayout2DWaves.setColumnStretch(1,5)
        self.generalLayout2DWaves.setColumnStretch(2,5)
################################################################################################
################################################################################################
################################################################################################
################################################################################################
    def _createPositionImageSHM(self):
        """Creates the Position Image for SHM"""
        self.PositionImageSHM = MplCanvas(self, width=6, height=6, dpi=75)
        self.PositionImageSHM_cid = self.PositionImageSHM.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.PositionImageSHM))
        self.PositionImageSHM_cod = self.PositionImageSHM.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.PositionImageSHM))

        self.generalLayoutSHM.addWidget(self.PositionImageSHM,self.currentLineSHM,1)
    def _createSpeedImageSHM(self):
        """Creates the Speed Image for SHM"""
        self.SpeedImageSHM = MplCanvas(self, width=6, height=6, dpi=75)
        self.SpeedImageSHM_cid = self.SpeedImageSHM.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.SpeedImageSHM))
        self.SpeedImageSHM_cod = self.SpeedImageSHM.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.SpeedImageSHM))

        self.generalLayoutSHM.addWidget(self.SpeedImageSHM,self.currentLineSHM,2)
        self.generalLayoutSHM.setRowStretch(self.currentLineSHM,5)
        self.currentLineSHM += 1
    def _createAccelerationImageSHM(self):
        """Creates the Position Image for SHM"""
        self.AccelerationImageSHM = MplCanvas(self, width=6, height=6, dpi=75)
        self.AccelerationImageSHM_cid = self.AccelerationImageSHM.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.AccelerationImageSHM))
        self.AccelerationImageSHM_cod = self.AccelerationImageSHM.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.AccelerationImageSHM))

        self.generalLayoutSHM.addWidget(self.AccelerationImageSHM,self.currentLineSHM,1)
    def _createCircleImageSHM(self):
        """Creates the Position Image for SHM"""
        self.CircleImageSHM = MplCanvas(self, width=6, height=6, dpi=75)
        self.CircleImageSHM_cid = self.CircleImageSHM.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.CircleImageSHM))
        self.CircleImageSHM_cod = self.CircleImageSHM.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.CircleImageSHM))

        self.generalLayoutSHM.addWidget(self.CircleImageSHM,self.currentLineSHM,2)
        self.generalLayoutSHM.setRowStretch(self.currentLineSHM,5)
        self.currentLineSHM += 1
    def _createEnergyImageSHM(self):
        """Creates the Position Image for SHM"""
        self.EnergyImageSHM = MplCanvas(self, width=6, height=6, dpi=75)
        self.EnergyImageSHM_cid = self.EnergyImageSHM.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.EnergyImageSHM))
        self.EnergyImageSHM_cod = self.EnergyImageSHM.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.EnergyImageSHM))
        self.generalLayoutSHM.addWidget(self.EnergyImageSHM,self.currentLineSHM,1)

    def _createParametersButtonsSHM(self):
        """Creates the Parameters Buttons for SHM"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.TypeMotionComboBoxSHM = QComboBox()
        for _, names in WavesAndOpticsStrings.ButtonChoiceSHM.items():
            self.TypeMotionComboBoxSHM.addItem(names[f"{self.language}"])
        self.TypeMotionComboBoxSHM.setCurrentText(self.parameters.TypeMovementSHM)
        self.TypeMotionComboBoxSHM.activated[str].connect(self.updateComboTypeSHM)

        self.TypeSHMComboBoxSHM = QComboBox()
        for _, names in WavesAndOpticsStrings.ButtonChoiceTypeMotionSHM.items():
            self.TypeSHMComboBoxSHM.addItem(names[f"{self.language}"])
        self.TypeSHMComboBoxSHM.setCurrentText(self.parameters.TypeMotionSHM)
        self.TypeSHMComboBoxSHM.activated[str].connect(self.updateComboTypeSHM)

        self.CursorSHM = QLineEdit()
        self.CursorSHM.setFixedWidth(90)
        self.CursorSHM.setText(str(self.parameters.CursorSHM))
        self.CursorSHM.editingFinished.connect(self.updateCursorSHM)

        self.sliderCursorSHM = QSlider(Qt.Horizontal)
        self.sliderCursorSHM.setMinimum(int(self.parameters.BoundsSHM[0]*100))
        self.sliderCursorSHM.setMaximum(int(self.parameters.BoundsSHM[1]*100))
        self.sliderCursorSHM.setTickPosition(QSlider.TicksBothSides)
        self.sliderCursorSHM.setSingleStep(1)
        self.sliderCursorSHM.valueChanged.connect(self.updateSliderCursorSHM)

        self.RangeMinSHM = QLineEdit()
        self.RangeMaxSHM = QLineEdit()
        self.RangeMinSHM.setFixedWidth(90)
        self.RangeMaxSHM.setFixedWidth(90)
        self.RangeMinSHM.setText(str(self.parameters.BoundsSHM[0]))
        self.RangeMaxSHM.setText(str(self.parameters.BoundsSHM[1]))
        self.RangeMinSHM.editingFinished.connect(self.updateBoundsSHM)
        self.RangeMaxSHM.editingFinished.connect(self.updateBoundsSHM)

        self.ParamASHM = QLineEdit()
        self.ParamOmegaSHM = QLineEdit()
        self.ParamPhiSHM = QLineEdit()
        self.ParamGammaSHM = QLineEdit()
        self.ParamMassSHM = QLineEdit()
        self.ParamKSHM = QLineEdit()
        self.ParamASHM.setFixedWidth(90)
        self.ParamOmegaSHM.setFixedWidth(90)
        self.ParamPhiSHM.setFixedWidth(90)
        self.ParamGammaSHM.setFixedWidth(90)
        self.ParamMassSHM.setFixedWidth(90)
        self.ParamKSHM.setFixedWidth(90)
        self.ParamASHM.setText(str(self.parameters.ParametersSHM[0]))
        self.ParamOmegaSHM.setText(str(self.parameters.ParametersSHM[1]))
        self.ParamPhiSHM.setText(str(self.parameters.ParametersSHM[2]))
        self.ParamGammaSHM.setText(str(self.parameters.ParametersSHM[3]))
        self.ParamMassSHM.setText(str(self.parameters.PhysicalParametersSHM[0]))
        self.ParamKSHM.setText(str(self.parameters.PhysicalParametersSHM[1]))
        self.ParamASHM.editingFinished.connect(self.updateParametersSHM)
        self.ParamOmegaSHM.editingFinished.connect(self.updateParametersSHM)
        self.ParamPhiSHM.editingFinished.connect(self.updateParametersSHM)
        self.ParamGammaSHM.editingFinished.connect(self.updateParametersSHM)
        self.ParamMassSHM.editingFinished.connect(self.updateParametersSHM)
        self.ParamKSHM.setReadOnly(True)

        self.ShowAllSHM = QCheckBox()
        self.ShowAllSHM.stateChanged.connect(self.update_Check_ShowAllSHM)

        layout.addWidget(QLabel(WavesAndOpticsStrings.ButtonTypeSHM[f"{self.language}"]),1,1)
        layout.addWidget(self.TypeMotionComboBoxSHM,1,2)
        layout.addWidget(QLabel(WavesAndOpticsStrings.ButtonTypeMotionSHM[f"{self.language}"]),1,3)
        layout.addWidget(self.TypeSHMComboBoxSHM,1,4)

        layout.addWidget(QLabel(WavesAndOpticsStrings.RangeSHM[f"{self.language}"]),2,1)
        layout.addWidget(self.RangeMinSHM,2,2)
        layout.addWidget(self.RangeMaxSHM,2,4)
        layout.addWidget(QLabel(WavesAndOpticsStrings.AmplitudeSHM[f"{self.language}"]),3,1)
        layout.addWidget(self.ParamASHM,3,2)
        layout.addWidget(QLabel(WavesAndOpticsStrings.OmegaSHM[f"{self.language}"]),3,3)
        layout.addWidget(self.ParamOmegaSHM,3,4)
        layout.addWidget(QLabel(WavesAndOpticsStrings.PhiSHM[f"{self.language}"]),4,1)
        layout.addWidget(self.ParamPhiSHM,4,2)
        layout.addWidget(QLabel(WavesAndOpticsStrings.GammaSHM[f"{self.language}"]),4,3)
        layout.addWidget(self.ParamGammaSHM,4,4)
        layout.addWidget(QLabel(WavesAndOpticsStrings.MassSHM[f"{self.language}"]),5,1)
        layout.addWidget(self.ParamMassSHM,5,2)
        layout.addWidget(QLabel(WavesAndOpticsStrings.KSHM[f"{self.language}"]),5,3)
        layout.addWidget(self.ParamKSHM,5,4)
        layout.addWidget(QLabel(WavesAndOpticsStrings.ShowAllButtonSHM[f"{self.language}"]),6,1)
        layout.addWidget(self.ShowAllSHM,6,2)
        layout.addWidget(self.CursorSHM,6,3)
        layout.addWidget(self.sliderCursorSHM,6,4)

        self.generalLayoutSHM.addWidget(subWidget,self.currentLineSHM,2)
        self.generalLayoutSHM.setRowStretch(self.currentLineSHM,5)
        self.currentLineSHM += 1
        self.updateAllSHM()
################################################################################################
################################################################################################
################################################################################################
################################################################################################
    def tmp(self):
        pass
################################################################################################
################################################################################################
################################################################################################
################################################################################################
    def _createFullImage2DWaves(self):
        """Creates the Complete View Image for 2D Waves"""
        self.FullImage2DWaves = MplCanvas(self, width=6, height=6, dpi=75)
        self.FullImage2DWaves_cid = self.FullImage2DWaves.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.FullImage2DWaves))
        self.FullImage2DWaves_cod = self.FullImage2DWaves.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.FullImage2DWaves))

        self.generalLayout2DWaves.addWidget(self.FullImage2DWaves,self.currentLine2DWaves,1)
    def _createTimeSliceImage2DWaves(self):
        """Creates the Complete View Image for 2D Waves"""
        self.TimeSliceImage2DWaves = MplCanvas(self, width=6, height=6, dpi=75)
        self.TimeSliceImage2DWaves_cid = self.TimeSliceImage2DWaves.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.TimeSliceImage2DWaves))
        self.TimeSliceImage2DWaves_cod = self.TimeSliceImage2DWaves.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.TimeSliceImage2DWaves))

        self.generalLayout2DWaves.addWidget(self.TimeSliceImage2DWaves,self.currentLine2DWaves,2)
        self.currentLine2DWaves += 1
    def _createPositionSliceImage2DWaves(self):
        """Creates the Complete View Image for 2D Waves"""
        self.PositionSliceImage2DWaves = MplCanvas(self, width=6, height=6, dpi=75)
        self.PositionSliceImage2DWaves_cid = self.PositionSliceImage2DWaves.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.PositionSliceImage2DWaves))
        self.PositionSliceImage2DWaves_cod = self.PositionSliceImage2DWaves.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.PositionSliceImage2DWaves))

        self.generalLayout2DWaves.addWidget(self.PositionSliceImage2DWaves,self.currentLine2DWaves,1)
    def _createParametersButtons2DWaves(self):
        """Creates the Parameters Buttons for 2D Waves"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.TypeMovementComboBox2DWaves = QComboBox()
        for _, names in WavesAndOpticsStrings.ButtonChoiceSHM.items():
            self.TypeMovementComboBox2DWaves.addItem(names[f"{self.language}"])
        self.TypeMovementComboBox2DWaves.setCurrentText(self.parameters.TypeMovement2DWaves)
        self.TypeMovementComboBox2DWaves.activated[str].connect(self.updateComboType2DWaves)

        self.TypeMotionComboBox2DWaves = QComboBox()
        for _, names in WavesAndOpticsStrings.ButtonChoiceTypeMotion2DWaves.items():
            self.TypeMotionComboBox2DWaves.addItem(names[f"{self.language}"])
        self.TypeMotionComboBox2DWaves.setCurrentText(self.parameters.TypeMotion2DWaves)
        self.TypeMotionComboBox2DWaves.activated[str].connect(self.updateComboType2DWaves)
        
        self.CursorX2DWave = QLineEdit()
        self.CursorT2DWave = QLineEdit()
        self.CursorX2DWave.setFixedWidth(90)
        self.CursorT2DWave.setFixedWidth(90)
        self.CursorX2DWave.setText(str(self.parameters.CursorX2DWaves))
        self.CursorT2DWave.setText(str(self.parameters.CursorT2DWaves))
        self.CursorX2DWave.editingFinished.connect(self.updateCursor2DWaves)
        self.CursorT2DWave.editingFinished.connect(self.updateCursor2DWaves)

        self.sliderCursorX2DWaves = QSlider(Qt.Horizontal)
        self.sliderCursorT2DWaves = QSlider(Qt.Horizontal)
        self.sliderCursorX2DWaves.setMinimum(int(self.parameters.BoundsX2DWaves[0]*100))
        self.sliderCursorT2DWaves.setMinimum(int(self.parameters.BoundsT2DWaves[0]*100))
        self.sliderCursorX2DWaves.setMaximum(int(self.parameters.BoundsX2DWaves[1]*100))
        self.sliderCursorT2DWaves.setMaximum(int(self.parameters.BoundsT2DWaves[1]*100))
        self.sliderCursorX2DWaves.setTickPosition(QSlider.TicksBothSides)
        self.sliderCursorT2DWaves.setTickPosition(QSlider.TicksBothSides)
        self.sliderCursorX2DWaves.setSingleStep(1)
        self.sliderCursorT2DWaves.setSingleStep(1)
        self.sliderCursorX2DWaves.valueChanged.connect(self.updateSliderCursor2DWaves)
        self.sliderCursorT2DWaves.valueChanged.connect(self.updateSliderCursor2DWaves)

        self.RangeMin2DWave = QLineEdit()
        self.RangeMax2DWave = QLineEdit()
        self.RangeMin2DWave.setFixedWidth(90)
        self.RangeMax2DWave.setFixedWidth(90)
        self.RangeMin2DWave.setText(str(self.parameters.BoundsX2DWaves[0]))
        self.RangeMax2DWave.setText(str(self.parameters.BoundsX2DWaves[1]))
        self.RangeMin2DWave.editingFinished.connect(self.updateBounds2DWaves)
        self.RangeMax2DWave.editingFinished.connect(self.updateBounds2DWaves)

        self.ParamA2DWave = QLineEdit()
        self.ParamOmega2DWave = QLineEdit()
        self.ParamPhi2DWave = QLineEdit()
        self.Paramk2DWave = QLineEdit()
        self.ParamA2DWave.setFixedWidth(90)
        self.ParamOmega2DWave.setFixedWidth(90)
        self.ParamPhi2DWave.setFixedWidth(90)
        self.Paramk2DWave.setFixedWidth(90)
        self.ParamA2DWave.setText(str(self.parameters.ParametersSHM[0]))
        self.ParamOmega2DWave.setText(str(self.parameters.ParametersSHM[1]))
        self.ParamPhi2DWave.setText(str(self.parameters.ParametersSHM[2]))
        self.Paramk2DWave.setText(str(self.parameters.PhysicalParametersSHM[0]))
        self.ParamA2DWave.editingFinished.connect(self.updateParameters2DWaves)
        self.ParamOmega2DWave.editingFinished.connect(self.updateParameters2DWaves)
        self.ParamPhi2DWave.editingFinished.connect(self.updateParameters2DWaves)
        self.Paramk2DWave.editingFinished.connect(self.updateParameters2DWaves)

        layout.addWidget(QLabel(WavesAndOpticsStrings.ButtonTypeSHM[f"{self.language}"]),1,1)
        layout.addWidget(self.TypeMovementComboBox2DWaves,1,2)
        layout.addWidget(QLabel(WavesAndOpticsStrings.ButtonTypeSHM[f"{self.language}"]),1,3)
        layout.addWidget(self.TypeMotionComboBox2DWaves,1,4)
        layout.addWidget(QLabel(WavesAndOpticsStrings.TimeCursor2DWave[f"{self.language}"]),2,1)
        layout.addWidget(self.CursorT2DWave,2,2)
        layout.addWidget(self.sliderCursorT2DWaves,2,3)
        layout.addWidget(QLabel(WavesAndOpticsStrings.PositionCursor2DWave[f"{self.language}"]),3,1)
        layout.addWidget(self.CursorX2DWave,3,2)
        layout.addWidget(self.sliderCursorX2DWaves,3,3)
        layout.addWidget(QLabel(WavesAndOpticsStrings.RangeSHM[f"{self.language}"]),4,1)
        layout.addWidget(self.RangeMin2DWave,4,2)
        layout.addWidget(self.RangeMax2DWave,4,3)
        layout.addWidget(QLabel(WavesAndOpticsStrings.AmplitudeSHM[f"{self.language}"]),5,1)
        layout.addWidget(self.ParamA2DWave,5,2)
        layout.addWidget(QLabel(WavesAndOpticsStrings.k2DWaves[f"{self.language}"]),5,3)
        layout.addWidget(self.Paramk2DWave,5,4)
        layout.addWidget(QLabel(WavesAndOpticsStrings.OmegaSHM[f"{self.language}"]),6,1)
        layout.addWidget(self.ParamOmega2DWave,6,2)
        layout.addWidget(QLabel(WavesAndOpticsStrings.PhiSHM[f"{self.language}"]),6,3)
        layout.addWidget(self.ParamPhi2DWave,6,4)

        self.generalLayout2DWaves.addWidget(subWidget,self.currentLine2DWaves,2)
        self.currentLine2DWaves += 1
        self.updateAll2DWave()
################################################################################################
################################################################################################
################################################################################################
################################################################################################
    def _createExitButton(self):
        """Creates exit buttons"""
        self.exitSHM = QPushButton(WavesAndOpticsStrings.ExitButton[f"{self.language}"])
        self.exitDamped = QPushButton(WavesAndOpticsStrings.ExitButton[f"{self.language}"])
        self.exit2DWaves = QPushButton(WavesAndOpticsStrings.ExitButton[f"{self.language}"])
        self.exitSHM.setToolTip(WavesAndOpticsStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitDamped.setToolTip(WavesAndOpticsStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exit2DWaves.setToolTip(WavesAndOpticsStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")

        self.exitSHM.setShortcut("Ctrl+Shift+E")
        self.exitDamped.setShortcut("Ctrl+Shift+E")
        self.exit2DWaves.setShortcut("Ctrl+Shift+E")


        self.exitSHM.clicked.connect(self.close)
        self.exitDamped.clicked.connect(self.close)
        self.exit2DWaves.clicked.connect(self.close)
        self.generalLayoutSHM.addWidget(self.exitSHM,self.currentLineSHM+1,3)  
        #self.generalLayoutDamped.addWidget(self.exitDamped,self.currentLineDamped+1,3)  
        self.generalLayout2DWaves.addWidget(self.exit2DWaves,self.currentLine2DWaves+1,3)  
        self.currentLineSHM += 1
        self.currentLineDamped += 1
        self.currentLine2DWaves += 1
################################################################################################
################################################################################################
################################################################################################
################################################################################################
    def updateComboTypeSHM(self):
        """Updates the Type of Curve"""
        name_tmp = self.TypeMotionComboBoxSHM.currentText()
        for dict, names in WavesAndOpticsStrings.ButtonChoiceSHM.items():
            if name_tmp in names.values():
                self.parameters.TypeMovementSHM = dict
        name_tmp = self.TypeSHMComboBoxSHM.currentText()
        for dict, names in WavesAndOpticsStrings.ButtonChoiceTypeMotionSHM.items():
            if name_tmp in names.values():
                self.parameters.TypeMotionSHM = dict
        self.updateAllSHM()

    def updateCursorSHM(self):
        """Updates the Cursor of the SHM"""
        try:
            self.parameters.CursorSHM = float(self.CursorSHM.text())
        except:
            self.parameters.CursorSHM = 0.0
        self.updateAllSHM()
    def updateSliderCursorSHM(self):
        """Updates the Cursor of the SHM"""
        try:
            self.parameters.CursorSHM = self.sliderCursorSHM.value()/100
        except:
            self.parameters.CursorSHM = 0.0
        self.CursorSHM.setText(str(self.parameters.CursorSHM))
        self.updateAllSHM()

    def updateBoundsSHM(self):
        """Updates the Bounds of the SHM"""
        try:
            self.parameters.BoundsSHM[0] = float(self.RangeMinSHM.text())
        except:
            self.parameters.BoundsSHM[0] = 0.0
        try:
            self.parameters.BoundsSHM[1] = float(self.RangeMaxSHM.text())
        except:
            self.parameters.BoundsSHM[1] = 10.0
        self.sliderCursorSHM.setMinimum(int(self.parameters.BoundsSHM[0]*100))
        self.sliderCursorSHM.setMaximum(int(self.parameters.BoundsSHM[1]*100))
        self.updateAllSHM()
    def updateParametersSHM(self):
        """Updates the Bounds of the SHM"""
        try:
            self.parameters.ParametersSHM[0] = float(self.ParamASHM.text())
        except:
            self.parameters.ParametersSHM[0] = 1.0
        try:
            self.parameters.ParametersSHM[1] = float(self.ParamOmegaSHM.text())
        except:
            self.parameters.ParametersSHM[1] = 1.0
        try:
            self.parameters.ParametersSHM[2] = float(self.ParamPhiSHM.text())
        except:
            self.parameters.ParametersSHM[2] = 0.0
        try:
            self.parameters.ParametersSHM[3] = float(self.ParamGammaSHM.text())
        except:
            self.parameters.ParametersSHM[3] = 1.0
        try:
            self.parameters.PhysicalParametersSHM[0] = float(self.ParamMassSHM.text())
        except:
            self.parameters.PhysicalParametersSHM[0] = 1.0
        self.parameters.PhysicalParametersSHM[1] = self.parameters.PhysicalParametersSHM[0] * self.parameters.ParametersSHM[1] ** 2
        self.parameters.ParametersSHM[4] = np.sqrt(self.parameters.ParametersSHM[1]**2 - (self.parameters.ParametersSHM[3]/(2*self.parameters.PhysicalParametersSHM[0]))**2)

        self.ParamKSHM.setText(str(self.parameters.PhysicalParametersSHM[1]))
        
        self.updateAllSHM()

    def update_Check_ShowAllSHM(self):
        """Updates the Boolean for Show All on SHM"""
        if self.ShowAllSHM.isChecked():
            self.parameters.ShowAllSHM = True
        else:
            self.parameters.ShowAllSHM = False
        self.updateAllSHM()


    def updateAllSHM(self):
        """Updates all images of the SHM"""
        self.updateCurvesSHM()
        self.updatePositionImageSHM()
        self.updateSpeedImageSHM()
        self.updateAccelerationImageSHM()
        self.updateEnergyImageSHM()
        self.updateCircleImageSHM()

    def updateCurvesSHM(self):
        """Updates the SHM Curves in the Parameters"""
        self.parameters.XAxisSHM = np.linspace(self.parameters.BoundsSHM[0],self.parameters.BoundsSHM[1],1000)
        self.parameters.PositionSHM, self.parameters.SpeedSHM, self.parameters.AccelerationSHM = Waves.SimpleHarmonicMotion(self.parameters.XAxisSHM,self.parameters.ParametersSHM,self.parameters.PhysicalParametersSHM,self.parameters.TypeMovementSHM,self.parameters.TypeMotionSHM)        
        self.parameters.KineticSHM, self.parameters.PotentialSHM, self.parameters.TotaleSHM = Waves.EnergySHM(self.parameters.PositionSHM,self.parameters.SpeedSHM,self.parameters.PhysicalParametersSHM)

    def updatePositionImageSHM(self):
        """Updates the Position Image of SHM"""
        try:
            self.PositionImageSHM.axes.cla()
        except : pass

        self.PositionImageSHM.axes.plot(self.parameters.XAxisSHM,self.parameters.PositionSHM)
        if self.parameters.TypeMotionSHM == "Damped":
            self.PositionImageSHM.axes.plot(self.parameters.XAxisSHM,self.parameters.ParametersSHM[0]*np.exp(-self.parameters.ParametersSHM[3]*self.parameters.XAxisSHM/(2*self.parameters.PhysicalParametersSHM[0])),linestyle = 'dashed',color='orange')
            self.PositionImageSHM.axes.plot(self.parameters.XAxisSHM,-self.parameters.ParametersSHM[0]*np.exp(-self.parameters.ParametersSHM[3]*self.parameters.XAxisSHM/(2*self.parameters.PhysicalParametersSHM[0])),linestyle = 'dashed',color='orange')
        self.PositionImageSHM.axes.axvline(self.parameters.CursorSHM,color='r')
        self.PositionImageSHM.axes.set_title(WavesAndOpticsStrings.PositionTitleLabelSHM[f"{self.language}"]
                                                +" : "
                                                +WavesAndOpticsStrings.EquationSHM(self.parameters.TypeMovementSHM,"Position",self.parameters.ParametersSHM,self.parameters.PhysicalParametersSHM,self.parameters.TypeMotionSHM))
        self.PositionImageSHM.axes.set_xlabel(WavesAndOpticsStrings.XLabelSHM[f"{self.language}"])        
        self.PositionImageSHM.axes.set_ylabel(WavesAndOpticsStrings.PositionYLabelSHM[f"{self.language}"])        
        self.PositionImageSHM.axes.grid()
        self.PositionImageSHM.draw()
    def updateSpeedImageSHM(self):
        """Updates the Speed Image of SHM"""
        try:
            self.SpeedImageSHM.axes.cla()
        except : pass

        self.SpeedImageSHM.axes.plot(self.parameters.XAxisSHM,self.parameters.SpeedSHM)
        self.SpeedImageSHM.axes.axvline(self.parameters.CursorSHM,color='r')
        self.SpeedImageSHM.axes.set_title(WavesAndOpticsStrings.SpeedTitleLabelSHM[f"{self.language}"]
                                                +" : "
                                                +WavesAndOpticsStrings.EquationSHM(self.parameters.TypeMovementSHM,"Speed",self.parameters.ParametersSHM,self.parameters.PhysicalParametersSHM,self.parameters.TypeMotionSHM))
        self.SpeedImageSHM.axes.set_xlabel(WavesAndOpticsStrings.XLabelSHM[f"{self.language}"])        
        self.SpeedImageSHM.axes.set_ylabel(WavesAndOpticsStrings.PositionYLabelSHM[f"{self.language}"])        
        self.SpeedImageSHM.axes.grid()
        self.SpeedImageSHM.draw()
    def updateAccelerationImageSHM(self):
        """Updates the Acceleration Image of SHM"""
        try:
            self.AccelerationImageSHM.axes.cla()
        except : pass
        if not self.parameters.ShowAllSHM:
            self.AccelerationImageSHM.axes.plot(self.parameters.XAxisSHM,self.parameters.AccelerationSHM)
            self.AccelerationImageSHM.axes.axvline(self.parameters.CursorSHM,color='r')
            self.AccelerationImageSHM.axes.set_title(WavesAndOpticsStrings.AccelerationTitleLabelSHM[f"{self.language}"]
                                                    +" : "
                                                    +WavesAndOpticsStrings.EquationSHM(self.parameters.TypeMovementSHM,"Acceleration",self.parameters.ParametersSHM,self.parameters.PhysicalParametersSHM,self.parameters.TypeMotionSHM))
            self.AccelerationImageSHM.axes.set_ylabel(WavesAndOpticsStrings.AccelerationYLabelSHM[f"{self.language}"])   
        else:   
            self.AccelerationImageSHM.axes.plot(self.parameters.XAxisSHM,self.parameters.PositionSHM, color = 'b',label='x')
            self.AccelerationImageSHM.axes.plot(self.parameters.XAxisSHM,self.parameters.SpeedSHM,color = 'g',label = 'v')
            self.AccelerationImageSHM.axes.plot(self.parameters.XAxisSHM,self.parameters.AccelerationSHM, color='orange', label = 'a')
            self.AccelerationImageSHM.axes.axvline(self.parameters.CursorSHM,color='r')  
            self.AccelerationImageSHM.axes.set_xlabel(WavesAndOpticsStrings.XLabelSHM[f"{self.language}"])        
            self.AccelerationImageSHM.axes.set_title(WavesAndOpticsStrings.ShowAllTitleSHM[f"{self.language}"])        
            self.AccelerationImageSHM.axes.legend(loc = 'upper right')
        self.AccelerationImageSHM.axes.set_xlabel(WavesAndOpticsStrings.XLabelSHM[f"{self.language}"])        
        self.AccelerationImageSHM.axes.grid()
        self.AccelerationImageSHM.draw()

    def updateEnergyImageSHM(self):
        """Updates the Energy Image of SHM"""
        try:
            self.EnergyImageSHM.axes.cla()
        except : pass

        self.EnergyImageSHM.axes.plot(self.parameters.XAxisSHM,self.parameters.KineticSHM,color = 'b',label='K')
        self.EnergyImageSHM.axes.plot(self.parameters.XAxisSHM,self.parameters.PotentialSHM,color = 'g',label = 'U')
        self.EnergyImageSHM.axes.plot(self.parameters.XAxisSHM,self.parameters.TotaleSHM,color = 'orange',label = 'T')
        self.EnergyImageSHM.axes.axvline(self.parameters.CursorSHM,color='r')
        self.EnergyImageSHM.axes.set_title(WavesAndOpticsStrings.EnergyTitleLabelSHM[f"{self.language}"] + ' : ' 
                                            + WavesAndOpticsStrings.ODESHM(self.parameters.PhysicalParametersSHM,self.parameters.ParametersSHM,self.parameters.TypeMotionSHM))
        self.EnergyImageSHM.axes.set_xlabel(WavesAndOpticsStrings.XLabelSHM[f"{self.language}"])        
        self.EnergyImageSHM.axes.set_ylabel(WavesAndOpticsStrings.EnergyYLabelSHM[f"{self.language}"])        
        self.EnergyImageSHM.axes.grid()
        self.EnergyImageSHM.axes.legend(loc = 'upper right')
        self.EnergyImageSHM.draw()

    def updateCircleImageSHM(self):
        """Updates the Circle Image of SHM"""
        try:
            self.CircleImageSHM.axes.cla()
        except : pass

        x, v, _ = Waves.SimpleHarmonicMotion(np.array([self.parameters.CursorSHM]),self.parameters.ParametersSHM,self.parameters.PhysicalParametersSHM,self.parameters.TypeMovementSHM,self.parameters.TypeMotionSHM)
        x = x[0]/self.parameters.ParametersSHM[0]
        v = v[0]/(self.parameters.ParametersSHM[0] * self.parameters.ParametersSHM[1])
        LineCos = [[0,v], [x,v]]
        LineSin = [[x,0], [x,v]]
        LineCircle = [[0,0],[x,v]]

        self.CircleImageSHM.axes.add_patch(Circle((0,0),1,fill = False))
        self.CircleImageSHM.axes.add_patch(Polygon(LineCircle,color = 'r'))
        self.CircleImageSHM.axes.add_patch(Polygon(LineCos, color = 'r'))
        self.CircleImageSHM.axes.add_patch(Polygon(LineSin, color = 'r'))
        self.CircleImageSHM.axes.axvline(0,color='black',alpha = 0.3)
        self.CircleImageSHM.axes.axhline(0,color='black', alpha = 0.3)
        self.CircleImageSHM.axes.set_title(WavesAndOpticsStrings.CircleTitleLabelSHM[f"{self.language}"])
        self.CircleImageSHM.axes.set_xlabel(WavesAndOpticsStrings.CircleXLabelSHM[f"{self.language}"])        
        self.CircleImageSHM.axes.set_ylabel(WavesAndOpticsStrings.CircleYLabelSHM[f"{self.language}"])        
        self.CircleImageSHM.axes.grid()
        self.CircleImageSHM.axes.set_xlim(-1.5,1.5)
        self.CircleImageSHM.axes.set_ylim(-1.5,1.5)
        self.CircleImageSHM.draw()
################################################################################################
################################################################################################
################################################################################################
################################################################################################
    def updateCursor2DWaves(self):
        """Updates the Cursor of the 2D Waves"""
        try:
            self.parameters.CursorX2DWaves = float(self.CursorX2DWave.text())
        except:
            self.parameters.CursorX2DWaves = 0.0
        try:
            self.parameters.CursorT2DWaves = float(self.CursorT2DWave.text())
        except:
            self.parameters.CursorT2DWaves = 0.0
        self.updateAll2DWave()
    def updateSliderCursor2DWaves(self):
        """Updates the Cursor of the SHM"""
        try:
            self.parameters.CursorX2DWaves = self.sliderCursorX2DWaves.value()/100
        except:
            self.parameters.CursorX2DWaves = 0.0
        try:
            self.parameters.CursorT2DWaves = self.sliderCursorT2DWaves.value()/100
        except:
            self.parameters.CursorT2DWaves = 0.0
        self.CursorX2DWave.setText(str(self.parameters.CursorX2DWaves))
        self.CursorT2DWave.setText(str(self.parameters.CursorT2DWaves))
        self.updateAll2DWave()
    def updateComboType2DWaves(self):
        """Updates the Type of Curve for 2D Waves"""
        name_tmp = self.TypeMovementComboBox2DWaves.currentText()
        for dict, names in WavesAndOpticsStrings.ButtonChoiceSHM.items():
            if name_tmp in names.values():
                self.parameters.TypeMovement2DWaves = dict
        name_tmp = self.TypeMotionComboBox2DWaves.currentText()
        for dict, names in WavesAndOpticsStrings.ButtonChoiceTypeMotion2DWaves.items():
            if name_tmp in names.values():
                self.parameters.TypeMotion2DWaves = dict
        
        self.updateAll2DWave()
    def updateParameters2DWaves(self):
        """Updates the Parameters of the 2DWaves"""
        try:
            self.parameters.Parameters2DWaves[0] = float(self.ParamA2DWave.text())
        except:
            self.parameters.Parameters2DWaves[0] = 1.0
        try:
            self.parameters.Parameters2DWaves[1] = float(self.Paramk2DWave.text())
        except:
            self.parameters.Parameters2DWaves[1] = 1.0
        try:
            self.parameters.Parameters2DWaves[2] = float(self.ParamOmega2DWave.text())
        except:
            self.parameters.Parameters2DWaves[2] = 1.0
        try:
            self.parameters.Parameters2DWaves[3] = float(self.ParamPhi2DWave.text())
        except:
            self.parameters.Parameters2DWaves[3] = 0.0       
        self.updateAll2DWave()
    def updateBounds2DWaves(self):
        """Updates the Bounds of the SHM"""
        try:
            self.parameters.BoundsX2DWaves[0] = float(self.RangeMin2DWave.text())
            self.parameters.BoundsT2DWaves[0] = float(self.RangeMin2DWave.text())
        except:
            self.parameters.BoundsX2DWaves[0] = 0.0
            self.parameters.BoundsT2DWaves[0] = 0.0
        try:
            self.parameters.BoundsX2DWaves[1] = float(self.RangeMax2DWave.text())
            self.parameters.BoundsT2DWaves[1] = float(self.RangeMax2DWave.text())
        except:
            self.parameters.BoundsX2DWaves[1] = 10.0
            self.parameters.BoundsT2DWaves[1] = 10.0
        self.sliderCursorX2DWaves.setMinimum(int(self.parameters.BoundsX2DWaves[0]*100))
        self.sliderCursorT2DWaves.setMinimum(int(self.parameters.BoundsT2DWaves[0]*100))
        self.sliderCursorX2DWaves.setMaximum(int(self.parameters.BoundsX2DWaves[1]*100))
        self.sliderCursorT2DWaves.setMaximum(int(self.parameters.BoundsT2DWaves[1]*100))
        self.updateAll2DWave()

    def updateAll2DWave(self):
        """Updates everything of the 2D Waves"""
        self.updateCurves2DWaves()
        self.updateFullImage2DWave()
        self.updateTImageImage2DWave()
        self.updateXImageImage2DWave()

    def updateCurves2DWaves(self):
        """Updates the Data of the 2D Waves"""
        self.parameters.XAxis2DWaves = np.linspace(self.parameters.BoundsX2DWaves[0],self.parameters.BoundsX2DWaves[1],100)
        self.parameters.TAxis2DWaves = np.linspace(self.parameters.BoundsT2DWaves[0],self.parameters.BoundsT2DWaves[1],100)
        self.parameters.Position2DWaves = Waves.Waves2D(
                                                            self.parameters.TAxis2DWaves,
                                                            self.parameters.XAxis2DWaves,
                                                            self.parameters.Parameters2DWaves,
                                                            self.parameters.TypeMovement2DWaves,
                                                            self.parameters.TypeMotion2DWaves
                                                        )
        self.parameters.TimeSlice2DWave = Waves.Waves2DT(
                                                            self.parameters.XAxis2DWaves,
                                                            self.parameters.CursorT2DWaves,
                                                            self.parameters.Parameters2DWaves,
                                                            self.parameters.TypeMovement2DWaves,
                                                            self.parameters.TypeMotion2DWaves
                                                        )                                                        
        self.parameters.PositionSlice2DWave = Waves.Waves2DX(
                                                            self.parameters.TAxis2DWaves,
                                                            self.parameters.CursorX2DWaves,
                                                            self.parameters.Parameters2DWaves,
                                                            self.parameters.TypeMovement2DWaves,
                                                            self.parameters.TypeMotion2DWaves
                                                        )   

    def updateFullImage2DWave(self):
        """Updates the Image of the Full 2D Waves"""
        try:
            self.FullImage2DWaves.axes.cla()
        except : pass

        self.FullImage2DWaves.axes.pcolormesh(self.parameters.TAxis2DWaves,self.parameters.XAxis2DWaves,
                                                self.parameters.Position2DWaves)
        self.FullImage2DWaves.axes.plot(self.parameters.CursorT2DWaves,
                                        self.parameters.CursorX2DWaves,
                                        '*',markersize = 6,color='r') 
        self.FullImage2DWaves.axes.axvline(self.parameters.CursorT2DWaves,color = 'r', alpha = 0.5, linestyle = '-')
        self.FullImage2DWaves.axes.axhline(self.parameters.CursorX2DWaves,color = 'r', alpha = 0.5, linestyle = '-')
        self.FullImage2DWaves.axes.set_title(WavesAndOpticsStrings.FullTitleLabel2DWave[f"{self.language}"]+
                                                WavesAndOpticsStrings.Equation2DWave(
                                                    self.parameters.TypeMovement2DWaves,
                                                    self.parameters.Parameters2DWaves,
                                                    slice = 'full',
                                                    typeMovement = self.parameters.TypeMotion2DWaves
                                                ))
        self.FullImage2DWaves.axes.set_xlabel(WavesAndOpticsStrings.FullTLabel2DWave[f"{self.language}"])        
        self.FullImage2DWaves.axes.set_ylabel(WavesAndOpticsStrings.FullXLabel2DWave[f"{self.language}"])    
        self.FullImage2DWaves.draw()
    def updateTImageImage2DWave(self):
        """Updates the Image of the Time Slice 2D Waves"""
        try:
            self.TimeSliceImage2DWaves.axes.cla()
        except : pass

        self.TimeSliceImage2DWaves.axes.plot(self.parameters.TimeSlice2DWave,self.parameters.TAxis2DWaves)
        self.TimeSliceImage2DWaves.axes.axhline(self.parameters.CursorX2DWaves, color = 'r')

        self.TimeSliceImage2DWaves.axes.set_title(WavesAndOpticsStrings.TimeSliceTitleLabel2DWave[f"{self.language}"]+
                                                WavesAndOpticsStrings.Equation2DWave(
                                                    self.parameters.TypeMovement2DWaves,
                                                    self.parameters.Parameters2DWaves,
                                                    slice = 'position',
                                                    cursor = self.parameters.CursorT2DWaves,
                                                    typeMovement = self.parameters.TypeMotion2DWaves
                                                ))
        self.TimeSliceImage2DWaves.axes.set_ylabel(WavesAndOpticsStrings.FullXLabel2DWave[f"{self.language}"])        
        self.TimeSliceImage2DWaves.axes.set_xlabel(WavesAndOpticsStrings.FullYLabel2DWave[f"{self.language}"])    
        self.TimeSliceImage2DWaves.axes.set_ylim(self.parameters.BoundsT2DWaves[0],self.parameters.BoundsT2DWaves[1])  
        if self.parameters.TypeMotion2DWaves == "Standing":
            self.TimeSliceImage2DWaves.axes.set_xlim(-2.1*self.parameters.Parameters2DWaves[0],2.1*self.parameters.Parameters2DWaves[0])  
        self.TimeSliceImage2DWaves.axes.grid()   
        self.TimeSliceImage2DWaves.draw()
    def updateXImageImage2DWave(self):
        """Updates the Image of the Time Slice 2D Waves"""
        try:
            self.PositionSliceImage2DWaves.axes.cla()
        except : pass

        self.PositionSliceImage2DWaves.axes.plot(self.parameters.XAxis2DWaves,self.parameters.PositionSlice2DWave)
        self.PositionSliceImage2DWaves.axes.axvline(self.parameters.CursorT2DWaves, color = 'r')

        self.PositionSliceImage2DWaves.axes.set_title(WavesAndOpticsStrings.PositionSliceTitleLabel2DWave[f"{self.language}"]+
                                                WavesAndOpticsStrings.Equation2DWave(
                                                    self.parameters.TypeMovement2DWaves,
                                                    self.parameters.Parameters2DWaves,
                                                    slice = 'time',
                                                    cursor = self.parameters.CursorX2DWaves,
                                                    typeMovement = self.parameters.TypeMotion2DWaves
                                                ))
        self.PositionSliceImage2DWaves.axes.set_xlabel(WavesAndOpticsStrings.FullTLabel2DWave[f"{self.language}"])        
        self.PositionSliceImage2DWaves.axes.set_ylabel(WavesAndOpticsStrings.FullYLabel2DWave[f"{self.language}"])    
        self.PositionSliceImage2DWaves.axes.set_xlim(self.parameters.BoundsX2DWaves[0],self.parameters.BoundsX2DWaves[1])  
        if self.parameters.TypeMotion2DWaves == "Standing":
            self.PositionSliceImage2DWaves.axes.set_ylim(-2.1*self.parameters.Parameters2DWaves[0],2.1*self.parameters.Parameters2DWaves[0])  
        self.PositionSliceImage2DWaves.axes.grid()   
        self.PositionSliceImage2DWaves.draw()

    def onClick(self,event,which):
        """Allows to click on an image and update the interface"""
        ix, iy = event.xdata, event.ydata
        which.coords = []
        which.coords.append((ix, iy))
        if len(which.coords) == 2:
            which.fig.canvas.mpl_disconnect(self.cid)
        if which in [self.PositionImageSHM, 
                     self.SpeedImageSHM, 
                     self.AccelerationImageSHM,
                     self.EnergyImageSHM]:
            self.parameters.CursorSHM = ix
            self.CursorSHM.setText(str(f"{ix:.2f}"))
            self.updateAllSHM()
        elif which == self.CircleImageSHM:
            angle = np.arctan(iy/ix)
            if self.parameters.TypeMotionSHM == "sin":
                pass
            elif self.parameters.TypeMotionSHM == "cos":
                pass
            self.updateAllSHM()
        elif which == self.FullImage2DWaves:
            self.parameters.CursorT2DWaves = ix
            self.parameters.CursorX2DWaves = iy
            self.CursorT2DWave.setText(str(f"{ix:.2f}"))
            self.CursorX2DWave.setText(str(f"{iy:.2f}"))
            self.updateAll2DWave()
        elif which == self.TimeSliceImage2DWaves:
            self.parameters.CursorX2DWaves = iy
            self.CursorX2DWave.setText(str(f"{iy:.2f}"))
            self.updateAll2DWave()
        elif which == self.PositionSliceImage2DWaves:
            self.parameters.CursorT2DWaves = ix
            self.CursorT2DWave.setText(str(f"{ix:.2f}"))
            self.updateAll2DWave()

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
        if which in [self.PositionImageSHM, 
                     self.SpeedImageSHM, 
                     self.AccelerationImageSHM,
                     self.EnergyImageSHM]:
            self.updateAllSHM()
################################################################################################
################################################################################################
################################################################################################
################################################################################################        
class MplCanvas(FigureCanvasQTAgg):
    """Class for the images and the graphs as a widget"""
    def __init__(self, parent=None, width:float=5, height:float=4, dpi:int=75):
        """Creates an empty figure with axes and fig as parameters"""
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout= True)
        self.axes = fig.add_subplot(111)
        self.fig = fig
        super(MplCanvas, self).__init__(fig)
################################################################################################
################################################################################################
################################################################################################
################################################################################################
if __name__ == "__main__":
    os.system('clear')
    print(f"Starting program at {time.strftime('%H:%M:%S')}")
    initial = time.time()
    app = QApplication([])
    window=WavesAndOpticsWindow()
    window.show()
    sys.exit(app.exec())