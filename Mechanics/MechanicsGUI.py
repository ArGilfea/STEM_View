import os
import time

###
import sys
import numpy as np
import time
###
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from functools import partial
###
try:
    import MechanicsStrings
    import GUIParametersMechanics
    import Mechanics1D
except:
    import Mechanics.MechanicsStrings as MechanicsStrings
    import Mechanics.GUIParametersMechanics as GUIParametersMechanics
    import Mechanics.Mechanics1D as Mechanics1D
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

class MechanicsWindow(QMainWindow):
    """
    Main window of the GUI.
    """    
    def __init__(self,parent=None,language = "Fr"):
        """Initializes the GUI Window"""
        self.parameters = GUIParametersMechanics.GUIParameters()
        self.tabs = QTabWidget()
        self.current_line1DTrajectory = 1
        self.current_line2DTrajectory = 1
        self.current_line3BodyProblem = 1

        super().__init__(parent=parent)
        self.setMinimumSize(1200, 700)
        self.language = language
        self.setWindowTitle(MechanicsStrings.WindowName[f"{self.language}"])

        self.generalLayout1DTrajectory = QGridLayout()
        self.generalLayout2DTrajectory = QGridLayout()
        self.generalLayout3BodyProblem = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()

        centralWidget1DTrajectory = QWidget(self)
        centralWidget2DTrajectory = QWidget(self)
        centralWidget3BodyProblem = QWidget(self)
        centralWidgetReadMe = QWidget(self)

        centralWidget1DTrajectory.setLayout(self.generalLayout1DTrajectory)
        centralWidget2DTrajectory.setLayout(self.generalLayout2DTrajectory)
        centralWidget3BodyProblem.setLayout(self.generalLayout3BodyProblem)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)

        self.tabs.addTab(centralWidget1DTrajectory,MechanicsStrings.Trajectory1DTab[f"{self.language}"])
        self.tabs.addTab(centralWidget2DTrajectory,MechanicsStrings.Trajectory2DTab[f"{self.language}"])
        self.tabs.addTab(centralWidget3BodyProblem,MechanicsStrings.ThreeBodyProblem[f"{self.language}"])
        self.tabs.addTab(centralWidgetReadMe,MechanicsStrings.ReadMeName[f"{self.language}"])

        self.setCentralWidget(self.tabs)
        ### 1D Trajectory
        self._createTrajectory1DImage()
        self._createVelocityTrajectory1DImage()
        self._createAccelerationTrajectory1DImage()
        self._createOptions1DTrajectory()
        ### 2D Trajectory
        self._createTrajectory2DImage()
        self._createOptions2DTrajectory()
        self._createVelocityTrajectory2DImage()
        self._createAccelerationTrajectory2DImage()
        ### 3 Body Problem
        self._createTrajectory3BodyProlem()
        self._createOptions3BodyProblem()
        self._createVelocityTrajectory3BodyProlem()
        self._createAccelerationTrajectory3BodyProlem()
        ### Exit
        self._createExitButton() 

        self.generalLayout1DTrajectory.setColumnStretch(1,5)
        self.generalLayout1DTrajectory.setColumnStretch(2,5)

        self.generalLayout2DTrajectory.setColumnStretch(1,5)
        self.generalLayout2DTrajectory.setColumnStretch(2,5)
        self.generalLayout2DTrajectory.setRowStretch(1,5)
        self.generalLayout2DTrajectory.setRowStretch(2,5)

        self.generalLayout3BodyProblem.setColumnStretch(1,5)
        self.generalLayout3BodyProblem.setColumnStretch(2,5)
        self.generalLayout3BodyProblem.setRowStretch(1,5)
        self.generalLayout3BodyProblem.setRowStretch(2,5)
        self.showMaximized()

################################
    def _createTrajectory1DImage(self):
        """Creates the Image for the Position of the 1D Trajectory"""
        self.Trajectory1DImage = pg.PlotWidget()
        self.trajectory1DCounter = 0
        self.generalLayout1DTrajectory.addWidget(self.Trajectory1DImage,self.current_line1DTrajectory,1)
        self.initializeImage1DTrajectory()

        self.trajectory1DTimer = QtCore.QTimer()
        self.trajectory1DTimer.setInterval(self.parameters.dynamicSpeed1DTrajectory)
        self.trajectory1DTimer.timeout.connect(self.updateImages1DTrajectory)
        if self.parameters.toggleDynamic1DTrajectory:
            self.trajectory1DTimer.start()

    def _createVelocityTrajectory1DImage(self):
        """Creates the Image for the Velocity of the 1D Trajectory"""
        self.TrajectoryVelocity1DImage = pg.PlotWidget()
        self.generalLayout1DTrajectory.addWidget(self.TrajectoryVelocity1DImage,self.current_line1DTrajectory,2)
        self.initializeVelocityImage1DTrajectory()

        self.current_line1DTrajectory += 1

    def _createAccelerationTrajectory1DImage(self):
        """Creates the Image for the Acceleration of the 1D Trajectory"""
        self.TrajectoryAcceleration1DImage = pg.PlotWidget()
        self.generalLayout1DTrajectory.addWidget(self.TrajectoryAcceleration1DImage,self.current_line1DTrajectory,1)
        self.initializeAccelerationImage1DTrajectory()

    def _createOptions1DTrajectory(self):
        """Creates the docks for the options of the 1D Trajectory"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.Dynamic1DTrajectoryCheckBox = QCheckBox()
        self.Static1DTrajectoryCheckBox = QCheckBox()
        self.Dynamic1DTrajectoryCheckBox.setChecked(self.parameters.toggleDynamic1DTrajectory)
        self.Static1DTrajectoryCheckBox.setChecked(self.parameters.toggleStatic1DTrajectory)
        self.Dynamic1DTrajectoryCheckBox.stateChanged.connect(self.updateCheckBoxDynamic1DTrajectory)
        self.Static1DTrajectoryCheckBox.stateChanged.connect(self.updateCheckBoxStatic1DTrajectory)

        self.Position1DTrajectoryLineEdit = np.zeros(2,dtype = object)
        self.Velocity1DTrajectoryLineEdit = np.zeros(2,dtype = object)
        self.Acceleration1DTrajectoryLineEdit = np.zeros(2,dtype = object)
        for i in range(2):
            self.Position1DTrajectoryLineEdit[i] = QLineEdit()
            self.Velocity1DTrajectoryLineEdit[i] = QLineEdit()
            self.Acceleration1DTrajectoryLineEdit[i] = QLineEdit()
            self.Position1DTrajectoryLineEdit[i].setFixedWidth(90)
            self.Velocity1DTrajectoryLineEdit[i].setFixedWidth(90)
            self.Acceleration1DTrajectoryLineEdit[i].setFixedWidth(90)
            self.Position1DTrajectoryLineEdit[i].setText(f"{(self.parameters.initialPosition1D[i]):.2f}")
            self.Velocity1DTrajectoryLineEdit[i].setText(f"{(self.parameters.initialVelocity1D[i]):.2f}")
            self.Acceleration1DTrajectoryLineEdit[i].setText(f"{(self.parameters.initialAcceleration1D[i]):.2f}")
            self.Position1DTrajectoryLineEdit[i].editingFinished.connect(self.update1DTrajectoryInitCond)
            self.Velocity1DTrajectoryLineEdit[i].editingFinished.connect(self.update1DTrajectoryInitCond)
            self.Acceleration1DTrajectoryLineEdit[i].editingFinished.connect(self.update1DTrajectoryInitCond)

        self.DynamicSpeed1DTrajectoryLineEdit = QLineEdit()
        self.DynamicSpeed1DTrajectoryLineEdit.setFixedWidth(90)
        self.DynamicSpeed1DTrajectoryLineEdit.setText(f"{(self.parameters.dynamicSpeed1DTrajectory)}")
        self.DynamicSpeed1DTrajectoryLineEdit.editingFinished.connect(self.update1DTrajectoryDynamicSpeed)


        layout.addWidget(QLabel("x"),1,1)
        layout.addWidget(QLabel("y"),1,2)
        layout.addWidget(QLabel(MechanicsStrings.Position[f"{self.language}"]),2,0)
        for i in range(2):
            layout.addWidget(self.Position1DTrajectoryLineEdit[i],2,1+i)
        layout.addWidget(QLabel(MechanicsStrings.Velocity[f"{self.language}"]),3,0)
        for i in range(2):
            layout.addWidget(self.Velocity1DTrajectoryLineEdit[i],3,1+i)
        layout.addWidget(QLabel(MechanicsStrings.Acceleration[f"{self.language}"]),4,0)
        for i in range(2):
            layout.addWidget(self.Acceleration1DTrajectoryLineEdit[i],4,1+i)

        layout.addWidget(QLabel(MechanicsStrings.dynamic[f"{self.language}"]),5,0)
        layout.addWidget(self.Dynamic1DTrajectoryCheckBox,5,1)
        layout.addWidget(QLabel(MechanicsStrings.static[f"{self.language}"]),5,2)
        layout.addWidget(self.Static1DTrajectoryCheckBox,5,3)
        layout.addWidget(QLabel(MechanicsStrings.dynamicSpeed[f"{self.language}"]),6,0)
        layout.addWidget(self.DynamicSpeed1DTrajectoryLineEdit,6,1)

        self.generalLayout1DTrajectory.addWidget(subWidget,self.current_line1DTrajectory,2)
        self.current_line1DTrajectory += 1

    def _createTrajectory2DImage(self):
        """Creates the Image for the Position of the 2D Trajectory"""
        self.Trajectory2DImage = pg.PlotWidget()
        self.trajectory2DCounter = 0
        self.generalLayout2DTrajectory.addWidget(self.Trajectory2DImage,self.current_line2DTrajectory,1)
        self.initializeImage2DTrajectory()

    def _createVelocityTrajectory2DImage(self):
        """Creates the Image for the Velocity of the 2D Trajectory"""
        self.TrajectoryVelocity2DImage = pg.PlotWidget()
        self.generalLayout2DTrajectory.addWidget(self.TrajectoryVelocity2DImage,self.current_line2DTrajectory,1)
        self.initializeVelocityImage2DTrajectory()



    def _createAccelerationTrajectory2DImage(self):
        """Creates the Image for the Acceleration of the 2D Trajectory"""
        self.TrajectoryAcceleration2DImage = pg.PlotWidget()
        self.trajectory2DCounter = 0
        self.generalLayout2DTrajectory.addWidget(self.TrajectoryAcceleration2DImage,self.current_line2DTrajectory,2)
        self.initializeAccelerationImage2DTrajectory()

        self.trajectory2DTimer = QtCore.QTimer()
        self.trajectory2DTimer.setInterval(self.parameters.dynamicSpeed2DTrajectory)
        self.trajectory2DTimer.timeout.connect(self.updateImages2DTrajectory)
        if self.parameters.toggleDynamic2DTrajectory or self.parameters.toggleObjectPositions2DTrajectory:
            self.trajectory2DTimer.start()
        self.current_line2DTrajectory += 1


    def _createOptions2DTrajectory(self):
        """Creates the docks for the options of the 2D Trajectory"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.Mass12DTrajectoryLineEdit = QLineEdit()
        self.Mass22DTrajectoryLineEdit = QLineEdit()
        self.Mass12DTrajectoryLineEdit.setFixedWidth(90)
        self.Mass22DTrajectoryLineEdit.setFixedWidth(90)
        self.Mass12DTrajectoryLineEdit.setText(f"{(self.parameters.mass2DTrajectory[0]):.2f}")
        self.Mass22DTrajectoryLineEdit.setText(f"{(self.parameters.mass2DTrajectory[1]):.2f}")
        self.Mass12DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)
        self.Mass22DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)

        self.Mass1Factor2DTrajectoryComboxBox = QComboBox()
        self.Mass2Factor2DTrajectoryComboxBox = QComboBox()
        for _, names in MechanicsStrings.MassFactor.items():
            self.Mass1Factor2DTrajectoryComboxBox.addItem(names[f"{self.language}"])
            self.Mass2Factor2DTrajectoryComboxBox.addItem(names[f"{self.language}"])
        self.Mass1Factor2DTrajectoryComboxBox.setCurrentText(MechanicsStrings.MassFactor[f"{self.parameters.massFactor2DTrajectory[0]}"][f"{self.language}"])
        self.Mass2Factor2DTrajectoryComboxBox.setCurrentText(MechanicsStrings.MassFactor[f"{self.parameters.massFactor2DTrajectory[1]}"][f"{self.language}"])
        self.Mass1Factor2DTrajectoryComboxBox.activated[str].connect(self.updateParameters2DTrajectory)
        self.Mass2Factor2DTrajectoryComboxBox.activated[str].connect(self.updateParameters2DTrajectory)

        self.Position1Factor2DTrajectoryComboxBox = QComboBox()
        self.Position2Factor2DTrajectoryComboxBox = QComboBox()
        for _, names in MechanicsStrings.PositionFactor.items():
            self.Position1Factor2DTrajectoryComboxBox.addItem(names[f"{self.language}"])
            self.Position2Factor2DTrajectoryComboxBox.addItem(names[f"{self.language}"])
        self.Position1Factor2DTrajectoryComboxBox.setCurrentText(MechanicsStrings.PositionFactor[f"{self.parameters.factorInitialPosition2DTrajectory[0]}"][f"{self.language}"])
        self.Position2Factor2DTrajectoryComboxBox.setCurrentText(MechanicsStrings.PositionFactor[f"{self.parameters.factorInitialPosition2DTrajectory[1]}"][f"{self.language}"])
        self.Position1Factor2DTrajectoryComboxBox.activated[str].connect(self.updateParameters2DTrajectory)
        self.Position2Factor2DTrajectoryComboxBox.activated[str].connect(self.updateParameters2DTrajectory)

        self.Speed1Factor2DTrajectoryComboxBox = QComboBox()
        self.Speed2Factor2DTrajectoryComboxBox = QComboBox()
        for _, names in MechanicsStrings.SpeedFactor.items():
            self.Speed1Factor2DTrajectoryComboxBox.addItem(names[f"{self.language}"])
            self.Speed2Factor2DTrajectoryComboxBox.addItem(names[f"{self.language}"])
        self.Speed1Factor2DTrajectoryComboxBox.setCurrentText(MechanicsStrings.SpeedFactor[f"{self.parameters.factorInitialVelocity2DTrajectory[0]}"][f"{self.language}"])
        self.Speed2Factor2DTrajectoryComboxBox.setCurrentText(MechanicsStrings.SpeedFactor[f"{self.parameters.factorInitialVelocity2DTrajectory[1]}"][f"{self.language}"])
        self.Speed1Factor2DTrajectoryComboxBox.activated[str].connect(self.updateParameters2DTrajectory)
        self.Speed2Factor2DTrajectoryComboxBox.activated[str].connect(self.updateParameters2DTrajectory)

        self.Dynamic2DTrajectoryCheckBox = QCheckBox()
        self.Static2DTrajectoryCheckBox = QCheckBox()
        self.Object2DTrajectoryCheckBox = QCheckBox()
        self.Collision2DTrajectoryCheckBox = QCheckBox()
        self.Absolute2DTrajectoryCheckBox = QCheckBox()
        self.Dynamic2DTrajectoryCheckBox.setChecked(self.parameters.toggleDynamic2DTrajectory)
        self.Static2DTrajectoryCheckBox.setChecked(self.parameters.toggleStatic2DTrajectory)
        self.Object2DTrajectoryCheckBox.setChecked(self.parameters.toggleObjectPositions2DTrajectory)
        self.Collision2DTrajectoryCheckBox.setChecked(self.parameters.toggleCollision2DTrajectory)
        self.Absolute2DTrajectoryCheckBox.setChecked(self.parameters.toggleAbsValues2DTrajectory)
        self.Dynamic2DTrajectoryCheckBox.stateChanged.connect(self.updateCheckBoxDynamic2DTrajectory)
        self.Static2DTrajectoryCheckBox.stateChanged.connect(self.updateCheckBoxStatic2DTrajectory)
        self.Object2DTrajectoryCheckBox.stateChanged.connect(self.updateCheckBoxObject2DTrajectory)
        self.Collision2DTrajectoryCheckBox.stateChanged.connect(self.updateCheckBoxCollision2DTrajectory)
        self.Absolute2DTrajectoryCheckBox.stateChanged.connect(self.updateCheckBoxAbsolute2DTrajectory)

        self.Position1x2DTrajectoryLineEdit = QLineEdit()
        self.Position1y2DTrajectoryLineEdit = QLineEdit()
        self.Position2x2DTrajectoryLineEdit = QLineEdit()
        self.Position2y2DTrajectoryLineEdit = QLineEdit()
        self.Position1x2DTrajectoryLineEdit.setFixedWidth(90)
        self.Position1y2DTrajectoryLineEdit.setFixedWidth(90)
        self.Position2x2DTrajectoryLineEdit.setFixedWidth(90)
        self.Position2y2DTrajectoryLineEdit.setFixedWidth(90)
        self.Position1x2DTrajectoryLineEdit.setText(f"{(self.parameters.initialPosition2DTrajectory[0,0]):.2f}")
        self.Position1y2DTrajectoryLineEdit.setText(f"{(self.parameters.initialPosition2DTrajectory[0,1]):.2f}")
        self.Position2x2DTrajectoryLineEdit.setText(f"{(self.parameters.initialPosition2DTrajectory[1,0]):.2f}")
        self.Position2y2DTrajectoryLineEdit.setText(f"{(self.parameters.initialPosition2DTrajectory[1,1]):.2f}")
        self.Position1x2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)
        self.Position1y2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)
        self.Position2x2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)
        self.Position2y2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)

        self.Speed1x2DTrajectoryLineEdit = QLineEdit()
        self.Speed1y2DTrajectoryLineEdit = QLineEdit()
        self.Speed2x2DTrajectoryLineEdit = QLineEdit()
        self.Speed2y2DTrajectoryLineEdit = QLineEdit()
        self.Speed1x2DTrajectoryLineEdit.setFixedWidth(90)
        self.Speed1y2DTrajectoryLineEdit.setFixedWidth(90)
        self.Speed2x2DTrajectoryLineEdit.setFixedWidth(90)
        self.Speed2y2DTrajectoryLineEdit.setFixedWidth(90)
        self.Speed1x2DTrajectoryLineEdit.setText(f"{(self.parameters.initialVelocity2DTrajectory[0,0]):.2f}")
        self.Speed1y2DTrajectoryLineEdit.setText(f"{(self.parameters.initialVelocity2DTrajectory[0,1]):.2f}")
        self.Speed2x2DTrajectoryLineEdit.setText(f"{(self.parameters.initialVelocity2DTrajectory[1,0]):.2f}")
        self.Speed2y2DTrajectoryLineEdit.setText(f"{(self.parameters.initialVelocity2DTrajectory[1,1]):.2f}")
        self.Speed1x2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)
        self.Speed1y2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)
        self.Speed2x2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)
        self.Speed2y2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)

        self.endTime2DTrajectoryLineEdit = QLineEdit()
        self.numberSteps2DTrajectoryLineEdit = QLineEdit()
        self.dynamicSpeed2DTrajectoryLineEdit = QLineEdit()
        self.dynamicStep2DTrajectoryLineEdit = QLineEdit()
        self.endTime2DTrajectoryLineEdit.setFixedWidth(90)
        self.numberSteps2DTrajectoryLineEdit.setFixedWidth(90)
        self.dynamicSpeed2DTrajectoryLineEdit.setFixedWidth(90)
        self.dynamicStep2DTrajectoryLineEdit.setFixedWidth(90)
        self.endTime2DTrajectoryLineEdit.setText(f"{(self.parameters.finalTime2DTrajectory)}")
        self.numberSteps2DTrajectoryLineEdit.setText(f"{(self.parameters.numberSteps2DTrajectory)}")
        self.dynamicSpeed2DTrajectoryLineEdit.setText(f"{(self.parameters.dynamicSpeed2DTrajectory)}")
        self.dynamicStep2DTrajectoryLineEdit.setText(f"{(self.parameters.step2DTrajectory)}")
        self.endTime2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)
        self.numberSteps2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)
        self.dynamicSpeed2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)
        self.dynamicStep2DTrajectoryLineEdit.editingFinished.connect(self.updateParameters2DTrajectory)

        self.RunTrajectory2DPushButton = QPushButton(MechanicsStrings.startRun[f"{self.language}"])
        self.RunTrajectory2DPushButton.setToolTip(MechanicsStrings.startRunToolTip[f"{self.language}"] + 
                             " (Ctrl+S)")
        self.RunTrajectory2DPushButton.clicked.connect(self.start2DTrajectorySimulation)
        self.RunTrajectory2DPushButton.setShortcut("Ctrl+S")

        self.ReRunTrajectory2DPushButton = QPushButton(MechanicsStrings.restartRun[f"{self.language}"])
        self.ReRunTrajectory2DPushButton.setToolTip(MechanicsStrings.restartRunToolTip[f"{self.language}"] + 
                             " (Ctrl+R)")
        self.ReRunTrajectory2DPushButton.clicked.connect(self.restart2DTrajectorySimulation)
        self.ReRunTrajectory2DPushButton.setShortcut("Ctrl+R")

        self.ReFrameTrajectory2DPushButton = QPushButton(MechanicsStrings.reframeRun[f"{self.language}"])
        self.ReFrameTrajectory2DPushButton.setToolTip(MechanicsStrings.reframeRunToolTip[f"{self.language}"] + 
                             " (Ctrl+F)")
        self.ReFrameTrajectory2DPushButton.clicked.connect(self.reframe2DTrajectorySimulation)
        self.ReFrameTrajectory2DPushButton.setShortcut("Ctrl+F")

        layout.addWidget(QLabel(MechanicsStrings.Mass[f"{self.language}"]+" 1"),0,0)
        layout.addWidget(self.Mass12DTrajectoryLineEdit,0,1)
        layout.addWidget(QLabel(MechanicsStrings.Factor[f"{self.language}"]),0,2)
        layout.addWidget(self.Mass1Factor2DTrajectoryComboxBox,0,3)

        layout.addWidget(QLabel(MechanicsStrings.Mass[f"{self.language}"]+" 2"),1,0)
        layout.addWidget(self.Mass22DTrajectoryLineEdit,1,1)
        layout.addWidget(QLabel(MechanicsStrings.Factor[f"{self.language}"]),1,2)
        layout.addWidget(self.Mass2Factor2DTrajectoryComboxBox,1,3)




        layout.addWidget(QLabel(MechanicsStrings.dynamic[f"{self.language}"]),5,0)
        layout.addWidget(self.Dynamic2DTrajectoryCheckBox,5,1)
        layout.addWidget(QLabel(MechanicsStrings.static[f"{self.language}"]),5,2)
        layout.addWidget(self.Static2DTrajectoryCheckBox,5,3)
        layout.addWidget(QLabel(MechanicsStrings.objects[f"{self.language}"]),6,0)
        layout.addWidget(self.Object2DTrajectoryCheckBox,6,1)
        layout.addWidget(QLabel(MechanicsStrings.collision[f"{self.language}"]),6,2)
        layout.addWidget(self.Collision2DTrajectoryCheckBox,6,3)

        layout.addWidget(QLabel(MechanicsStrings.Abs[f"{self.language}"]),7,0)
        layout.addWidget(self.Absolute2DTrajectoryCheckBox,7,1)


        layout.addWidget(QLabel(MechanicsStrings.visualBox[f"{self.language}"]),8,0)
        layout.addWidget(QLabel("x"),8,1)
        layout.addWidget(QLabel("y"),8,2)
        layout.addWidget(QLabel(MechanicsStrings.Factor[f"{self.language}"]),8,3)
        layout.addWidget(QLabel(MechanicsStrings.Pos[f"{self.language}"]+" "+MechanicsStrings.object[f"{self.language}"]+ " 1"),9,0)
        layout.addWidget(self.Position1x2DTrajectoryLineEdit,9,1)
        layout.addWidget(self.Position1y2DTrajectoryLineEdit,9,2)
        layout.addWidget(self.Position1Factor2DTrajectoryComboxBox,9,3)
        layout.addWidget(QLabel(MechanicsStrings.Pos[f"{self.language}"]+" "+MechanicsStrings.object[f"{self.language}"]+ " 2"),10,0)
        layout.addWidget(self.Position2x2DTrajectoryLineEdit,10,1)
        layout.addWidget(self.Position2y2DTrajectoryLineEdit,10,2)
        layout.addWidget(self.Position2Factor2DTrajectoryComboxBox,10,3)
        layout.addWidget(QLabel(MechanicsStrings.Speed[f"{self.language}"]+" "+MechanicsStrings.object[f"{self.language}"]+ " 1"),11,0)
        layout.addWidget(self.Speed1x2DTrajectoryLineEdit,11,1)
        layout.addWidget(self.Speed1y2DTrajectoryLineEdit,11,2)
        layout.addWidget(self.Speed1Factor2DTrajectoryComboxBox,11,3)
        layout.addWidget(QLabel(MechanicsStrings.Speed[f"{self.language}"]+" "+MechanicsStrings.object[f"{self.language}"]+ " 2"),12,0)
        layout.addWidget(self.Speed2x2DTrajectoryLineEdit,12,1)
        layout.addWidget(self.Speed2y2DTrajectoryLineEdit,12,2)
        layout.addWidget(self.Speed2Factor2DTrajectoryComboxBox,12,3)

        layout.addWidget(QLabel(MechanicsStrings.endTime[f"{self.language}"]),13,0)
        layout.addWidget(self.endTime2DTrajectoryLineEdit,13,1)
        layout.addWidget(QLabel(MechanicsStrings.StepNumber[f"{self.language}"]),13,2)
        layout.addWidget(self.numberSteps2DTrajectoryLineEdit,13,3)
        layout.addWidget(QLabel(MechanicsStrings.dynamicSpeed[f"{self.language}"]),14,0)
        layout.addWidget(self.dynamicSpeed2DTrajectoryLineEdit,14,1)
        layout.addWidget(QLabel(MechanicsStrings.dynamicStep[f"{self.language}"]),14,2)
        layout.addWidget(self.dynamicStep2DTrajectoryLineEdit,14,3)


        layout.addWidget(self.RunTrajectory2DPushButton,15,0)
        layout.addWidget(self.ReRunTrajectory2DPushButton,15,1)
        layout.addWidget(self.ReFrameTrajectory2DPushButton,15,2)

        self.generalLayout2DTrajectory.addWidget(subWidget,self.current_line2DTrajectory,2)
        self.current_line2DTrajectory += 1

    def _createTrajectory3BodyProlem(self):
        """Creates the Image for the Position of the 3BodyProblem"""
        self.Trajectory3BodyProblemImage = pg.PlotWidget()
        self.trajectory3BodyProblemCounter = 0
        self.generalLayout3BodyProblem.addWidget(self.Trajectory3BodyProblemImage,self.current_line3BodyProblem,1)
        self.initializeImage3BodyProblem()

        self.trajectory3BodyProblemTimer = QtCore.QTimer()
        self.trajectory3BodyProblemTimer.setInterval(self.parameters.dynamicSpeed3BodyProblem)
        self.trajectory3BodyProblemTimer.timeout.connect(self.updateImages3BodyProblem)
        if self.parameters.toggleDynamic3BodyProblem or self.parameters.toggleObjectPositions3BodyProblem:
            self.trajectory3BodyProblemTimer.start()

    def _createVelocityTrajectory3BodyProlem(self):
        """Creates the Image for the Velocity of the 3BodyProblem"""
        self.TrajectoryVelocity3BodyProblem = pg.PlotWidget()
        self.generalLayout3BodyProblem.addWidget(self.TrajectoryVelocity3BodyProblem,self.current_line3BodyProblem,1)
        self.initializeVelocityImage3BodyProblem()


    def _createAccelerationTrajectory3BodyProlem(self):
        """Creates the Image for the Acceleration of the 3BodyProblem"""
        self.TrajectoryAcceleration3BodyProblem = pg.PlotWidget()
        self.generalLayout3BodyProblem.addWidget(self.TrajectoryAcceleration3BodyProblem,self.current_line3BodyProblem,2)
        self.initializeAccelerationImage3BodyProblem()
        self.current_line3BodyProblem += 1

    def _createOptions3BodyProblem(self):
        """Creates the docks for the options of the 3BodyProblem"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.Mass3BodyProblemLineEdit = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        self.MassFactor3BodyProblemComboBox = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        self.PositionFactor3BodyProblemComboxBox = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        self.SpeedFactor3BodyProblemComboxBox = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        for i in range(self.parameters.numberOfMass3BodyProblem):
            self.Mass3BodyProblemLineEdit[i] = QLineEdit()
            self.Mass3BodyProblemLineEdit[i].setFixedWidth(90)
            self.Mass3BodyProblemLineEdit[i].setText(f"{(self.parameters.mass3BodyProblem[i]):.2f}")
            self.Mass3BodyProblemLineEdit[i].editingFinished.connect(self.updateParameters3BodyProblem)

            self.MassFactor3BodyProblemComboBox[i] = QComboBox()
            for _, names in MechanicsStrings.MassFactor.items():
                self.MassFactor3BodyProblemComboBox[i].addItem(names[f"{self.language}"])
            self.MassFactor3BodyProblemComboBox[i].setCurrentText(MechanicsStrings.MassFactor[f"{self.parameters.massFactor3BodyProblem[i]}"][f"{self.language}"])
            self.MassFactor3BodyProblemComboBox[i].activated[str].connect(self.updateParameters3BodyProblem)

            self.PositionFactor3BodyProblemComboxBox[i] = QComboBox()
            for _, names in MechanicsStrings.PositionFactor.items():
                self.PositionFactor3BodyProblemComboxBox[i].addItem(names[f"{self.language}"])
            self.PositionFactor3BodyProblemComboxBox[i].setCurrentText(MechanicsStrings.PositionFactor[f"{self.parameters.factorInitialPosition3BodyProblem[i,0]}"][f"{self.language}"])
            self.PositionFactor3BodyProblemComboxBox[i].activated[str].connect(self.updateParameters3BodyProblem)

            self.SpeedFactor3BodyProblemComboxBox[i] = QComboBox()
            for _, names in MechanicsStrings.SpeedFactor.items():
                self.SpeedFactor3BodyProblemComboxBox[i].addItem(names[f"{self.language}"])
            self.SpeedFactor3BodyProblemComboxBox[i].setCurrentText(MechanicsStrings.SpeedFactor[f"{self.parameters.factorInitialVelocity3BodyProblem[i,0]}"][f"{self.language}"])
            self.SpeedFactor3BodyProblemComboxBox[i].activated[str].connect(self.updateParameters3BodyProblem)

        self.Dynamic3BodyProblemCheckBox = QCheckBox()
        self.Static3BodyProblemCheckBox = QCheckBox()
        self.Object3BodyProblemCheckBox = QCheckBox()
        self.Collision3BodyProblemCheckBox = QCheckBox()
        self.AbsValues3BodyProblemCheckBox = QCheckBox()
        self.Dynamic3BodyProblemCheckBox.setChecked(self.parameters.toggleDynamic3BodyProblem)
        self.Static3BodyProblemCheckBox.setChecked(self.parameters.toggleStatic3BodyProblem)
        self.Object3BodyProblemCheckBox.setChecked(self.parameters.toggleObjectPositions3BodyProblem)
        self.Collision3BodyProblemCheckBox.setChecked(self.parameters.toggleCollision3BodyProblem)
        self.AbsValues3BodyProblemCheckBox.setChecked(self.parameters.toggleAbsValues3BodyProblem)
        self.Dynamic3BodyProblemCheckBox.stateChanged.connect(self.updateCheckBoxDynamic3BodyProblem)
        self.Static3BodyProblemCheckBox.stateChanged.connect(self.updateCheckBoxStatic3BodyProblem)
        self.Object3BodyProblemCheckBox.stateChanged.connect(self.updateCheckBoxObject3BodyProblem)
        self.Collision3BodyProblemCheckBox.stateChanged.connect(self.updateCheckBoxCollision3BodyProblem)
        self.AbsValues3BodyProblemCheckBox.stateChanged.connect(self.updateCheckBoxAbsValue3BodyProblem)

        self.Position3BodyProblemLineEdit = np.zeros((self.parameters.numberOfMass3BodyProblem,2), dtype = object)
        self.Speed3BodyProblemLineEdit = np.zeros((self.parameters.numberOfMass3BodyProblem,2), dtype = object)

        for i in range(self.parameters.numberOfMass3BodyProblem):
            for j in range(2):
                self.Position3BodyProblemLineEdit[i,j] = QLineEdit()
                self.Position3BodyProblemLineEdit[i,j].setFixedWidth(90)
                self.Position3BodyProblemLineEdit[i,j].setText(f"{(self.parameters.initialPosition3BodyProblem[i,j]):.2f}")
                self.Position3BodyProblemLineEdit[i,j].editingFinished.connect(self.updateParameters3BodyProblem)

                self.Speed3BodyProblemLineEdit[i,j] = QLineEdit()
                self.Speed3BodyProblemLineEdit[i,j].setFixedWidth(90)
                self.Speed3BodyProblemLineEdit[i,j].setText(f"{(self.parameters.initialVelocity3BodyProblem[i,j]):.2f}")
                self.Speed3BodyProblemLineEdit[i,j].editingFinished.connect(self.updateParameters3BodyProblem)

        self.endTime3BodyProblemLineEdit = QLineEdit()
        self.numberSteps3BodyProblemLineEdit = QLineEdit()
        self.dynamicSpeed3BodyProblemLineEdit = QLineEdit()
        self.dynamicStep3BodyProblemLineEdit = QLineEdit()
        self.endTime3BodyProblemLineEdit.setFixedWidth(90)
        self.numberSteps3BodyProblemLineEdit.setFixedWidth(90)
        self.dynamicSpeed3BodyProblemLineEdit.setFixedWidth(90)
        self.dynamicStep3BodyProblemLineEdit.setFixedWidth(90)
        self.endTime3BodyProblemLineEdit.setText(f"{(self.parameters.finalTime3BodyProblem)}")
        self.numberSteps3BodyProblemLineEdit.setText(f"{(self.parameters.numberSteps3BodyProblem)}")
        self.dynamicSpeed3BodyProblemLineEdit.setText(f"{(self.parameters.dynamicSpeed3BodyProblem)}")
        self.dynamicStep3BodyProblemLineEdit.setText(f"{(self.parameters.step3BodyProblem)}")
        self.endTime3BodyProblemLineEdit.editingFinished.connect(self.updateParameters3BodyProblem)
        self.numberSteps3BodyProblemLineEdit.editingFinished.connect(self.updateParameters3BodyProblem)
        self.dynamicSpeed3BodyProblemLineEdit.editingFinished.connect(self.updateParameters3BodyProblem)
        self.dynamicStep3BodyProblemLineEdit.editingFinished.connect(self.updateParameters3BodyProblem)

        self.RunTrajectory3BPPushButton = QPushButton(MechanicsStrings.startRun[f"{self.language}"])
        self.RunTrajectory3BPPushButton.setToolTip(MechanicsStrings.startRunToolTip[f"{self.language}"] + 
                             " (Ctrl+S)")
        self.RunTrajectory3BPPushButton.clicked.connect(self.start3BodyProblemSimulation)
        self.RunTrajectory3BPPushButton.setShortcut("Ctrl+S")

        self.ReRunTrajectory3BPPushButton = QPushButton(MechanicsStrings.restartRun[f"{self.language}"])
        self.ReRunTrajectory3BPPushButton.setToolTip(MechanicsStrings.restartRunToolTip[f"{self.language}"] + 
                             " (Ctrl+R)")
        self.ReRunTrajectory3BPPushButton.clicked.connect(self.restart3BodyProblemSimulation)
        self.ReRunTrajectory3BPPushButton.setShortcut("Ctrl+R")

        self.ReFrameTrajectory3BPPushButton = QPushButton(MechanicsStrings.reframeRun[f"{self.language}"])
        self.ReFrameTrajectory3BPPushButton.setToolTip(MechanicsStrings.reframeRunToolTip[f"{self.language}"] + 
                             " (Ctrl+F)")
        self.ReFrameTrajectory3BPPushButton.clicked.connect(self.reframe3BodyProblemSimulation)
        self.ReFrameTrajectory3BPPushButton.setShortcut("Ctrl+F")

        tmp_counter = 0

        for i in range(self.parameters.numberOfMass3BodyProblem):
            layout.addWidget(QLabel(MechanicsStrings.Mass[f"{self.language}"]+f" {i+1}"),tmp_counter,0)
            layout.addWidget(self.Mass3BodyProblemLineEdit[i],tmp_counter,1)
            layout.addWidget(QLabel(MechanicsStrings.Factor[f"{self.language}"]),tmp_counter,2)
            layout.addWidget(self.MassFactor3BodyProblemComboBox[i],tmp_counter,3)
            tmp_counter += 1

        layout.addWidget(QLabel(MechanicsStrings.dynamic[f"{self.language}"]),tmp_counter,0)
        layout.addWidget(self.Dynamic3BodyProblemCheckBox,tmp_counter,1)
        layout.addWidget(QLabel(MechanicsStrings.static[f"{self.language}"]),tmp_counter,2)
        layout.addWidget(self.Static3BodyProblemCheckBox,tmp_counter,3)
        layout.addWidget(QLabel(MechanicsStrings.objects[f"{self.language}"]),tmp_counter+1,0)
        layout.addWidget(self.Object3BodyProblemCheckBox,tmp_counter+1,1)
        layout.addWidget(QLabel(MechanicsStrings.collision[f"{self.language}"]),tmp_counter+1,2)
        layout.addWidget(self.Collision3BodyProblemCheckBox,tmp_counter+1,3)
        layout.addWidget(QLabel(MechanicsStrings.Abs[f"{self.language}"]),tmp_counter+2,0)
        layout.addWidget(self.AbsValues3BodyProblemCheckBox,tmp_counter+2,1)

        tmp_counter += 3

        layout.addWidget(QLabel("x"),tmp_counter,1)
        layout.addWidget(QLabel("y"),tmp_counter,2)
        layout.addWidget(QLabel(MechanicsStrings.Factor[f"{self.language}"]),tmp_counter,3)
        tmp_counter += 1

        for i in range(self.parameters.numberOfMass3BodyProblem):
            layout.addWidget(QLabel(MechanicsStrings.Pos[f"{self.language}"]+" "+MechanicsStrings.object[f"{self.language}"]+ f" {i+1}"),tmp_counter,0)
            layout.addWidget(self.Position3BodyProblemLineEdit[i,0],tmp_counter,1)
            layout.addWidget(self.Position3BodyProblemLineEdit[i,1],tmp_counter,2)
            layout.addWidget(self.PositionFactor3BodyProblemComboxBox[i],tmp_counter,3)
            tmp_counter += 1

        for i in range(self.parameters.numberOfMass3BodyProblem):
            layout.addWidget(QLabel(MechanicsStrings.Speed[f"{self.language}"]+" "+MechanicsStrings.object[f"{self.language}"]+ f" {i+1}"),tmp_counter,0)
            layout.addWidget(self.Speed3BodyProblemLineEdit[i,0],tmp_counter,1)
            layout.addWidget(self.Speed3BodyProblemLineEdit[i,1],tmp_counter,2)
            layout.addWidget(self.SpeedFactor3BodyProblemComboxBox[i],tmp_counter,3)
            tmp_counter += 1





        layout.addWidget(QLabel(MechanicsStrings.endTime[f"{self.language}"]),tmp_counter,0)
        layout.addWidget(self.endTime3BodyProblemLineEdit,tmp_counter,1)
        layout.addWidget(QLabel(MechanicsStrings.StepNumber[f"{self.language}"]),tmp_counter,2)
        layout.addWidget(self.numberSteps3BodyProblemLineEdit,tmp_counter,3)
        layout.addWidget(QLabel(MechanicsStrings.dynamicSpeed[f"{self.language}"]),tmp_counter+1,0)
        layout.addWidget(self.dynamicSpeed3BodyProblemLineEdit,tmp_counter+1,1)
        layout.addWidget(QLabel(MechanicsStrings.dynamicStep[f"{self.language}"]),tmp_counter+1,2)
        layout.addWidget(self.dynamicStep3BodyProblemLineEdit,tmp_counter+1,3)
        tmp_counter += 2


        layout.addWidget(self.RunTrajectory3BPPushButton,tmp_counter,0)
        layout.addWidget(self.ReRunTrajectory3BPPushButton,tmp_counter,1)
        layout.addWidget(self.ReFrameTrajectory3BPPushButton,tmp_counter,2)
        tmp_counter += 1

        self.generalLayout3BodyProblem.addWidget(subWidget,self.current_line3BodyProblem,2)
        self.current_line3BodyProblem += 1
################################
    def _createExitButton(self):
        """Creates an exit button"""
        self.exit1DTrajectory = QPushButton(MechanicsStrings.ExitLabel[f"{self.language}"])
        self.exit2DTrajectory = QPushButton(MechanicsStrings.ExitLabel[f"{self.language}"])
        self.exit3BodyProblem = QPushButton(MechanicsStrings.ExitLabel[f"{self.language}"])

        self.exit1DTrajectory.setToolTip(MechanicsStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exit2DTrajectory.setToolTip(MechanicsStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exit3BodyProblem.setToolTip(MechanicsStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        
        self.exit1DTrajectory.setShortcut("Ctrl+Shift+E")
        self.exit2DTrajectory.setShortcut("Ctrl+Shift+E")
        self.exit3BodyProblem.setShortcut("Ctrl+Shift+E")

        self.exit1DTrajectory.clicked.connect(self.close)
        self.exit2DTrajectory.clicked.connect(self.close)
        self.exit3BodyProblem.clicked.connect(self.close)

        self.generalLayout1DTrajectory.addWidget(self.exit1DTrajectory,self.current_line1DTrajectory+1,3)  
        self.generalLayout2DTrajectory.addWidget(self.exit2DTrajectory,self.current_line2DTrajectory+1,3)  
        self.generalLayout3BodyProblem.addWidget(self.exit3BodyProblem,self.current_line3BodyProblem+1,3)  

        self.current_line1DTrajectory += 1
        self.current_line2DTrajectory += 1
        self.current_line3BodyProblem += 1
################################
    def updateCheckBoxDynamic1DTrajectory(self):
        """Updates the Dynamic CheckBox for the 1D Trajectory"""
        if self.Dynamic1DTrajectoryCheckBox.isChecked():
            self.parameters.toggleDynamic1DTrajectory = True
            self.parameters.toggleDynamic2DTrajectory = False
            self.parameters.toggleDynamic3BodyProblem = False
            self.trajectory1DTimer.start()
            self.trajectory2DTimer.stop()
            self.trajectory3BodyProblemTimer.stop()
            self.Dynamic2DTrajectoryCheckBox.setChecked(self.parameters.toggleDynamic2DTrajectory)
            self.Dynamic3BodyProblemCheckBox.setChecked(self.parameters.toggleDynamic3BodyProblem)
        else:
            self.parameters.toggleDynamic1DTrajectory = False
            self.trajectory1DTimer.stop()
        self.updateImages1DTrajectory()

    def updateCheckBoxStatic1DTrajectory(self):
        """Updates the Static CheckBox for the 1D Trajectory"""
        if self.Static1DTrajectoryCheckBox.isChecked():
            self.parameters.toggleStatic1DTrajectory = True
        else:
            self.parameters.toggleStatic1DTrajectory = False
        self.updateImages1DTrajectory()

    def update1DTrajectoryDynamicSpeed(self):
        """Updates the speed of the video"""
        self.parameters.dynamicSpeed1DTrajectory = int(self.DynamicSpeed1DTrajectoryLineEdit.text())
        self.trajectory1DTimer.setInterval(self.parameters.dynamicSpeed1DTrajectory)

    def update1DTrajectoryInitCond(self):
        """Update the 1D Trajectory initial parameters. Also resets the video"""
        for i in range(2):
            try:
                self.parameters.initialPosition1D[i] = float(self.Position1DTrajectoryLineEdit[i].text())
            except:
                self.parameters.initialPosition1D[i] = 0.0
            try:
                self.parameters.initialVelocity1D[i] = float(self.Velocity1DTrajectoryLineEdit[i].text())
            except:
                self.parameters.initialVelocity1D[i] = 0.0
            try:
                self.parameters.initialAcceleration1D[i] = float(self.Acceleration1DTrajectoryLineEdit[i].text())
            except:
                self.parameters.initialAcceleration1D[i] = 0.0
        self.updateCurve1DTrajectory()

    def updateCurve1DTrajectory(self):
        """Updates the curve. Also resets the video"""
        self.trajectory1DCounter = 0
        self.parameters.trajectory1D, self.parameters.Velocitiestrajectory1D, self.parameters.trajectory1DEndValue = Mechanics1D.MechanicsTrajectory1D(self.parameters.initialPosition1D,
                                                                self.parameters.initialVelocity1D,self.parameters.initialAcceleration1D,
                                                                timeScale=self.parameters.timeScale1D, toggleGround= self.parameters.toggleGround1D)
        width = np.max(self.parameters.Velocitiestrajectory1D[:,0])-np.min(self.parameters.Velocitiestrajectory1D[:,0])
        height = np.max(self.parameters.Velocitiestrajectory1D[:,1])-np.min(self.parameters.Velocitiestrajectory1D[:,1])
        self.TrajectoryVelocity1DImage.setXRange(np.min(self.parameters.Velocitiestrajectory1D[:,0])-0.1*width,np.max(self.parameters.Velocitiestrajectory1D[:,0])+0.1*width)
        self.TrajectoryVelocity1DImage.setYRange(np.min(self.parameters.Velocitiestrajectory1D[:,1])-0.1*height,np.max(self.parameters.Velocitiestrajectory1D[:,1])+0.1*height)

        width = np.max(self.parameters.trajectory1D[:,0])-np.min(self.parameters.trajectory1D[:,0])
        height = np.max(self.parameters.trajectory1D[:,1])-np.min(self.parameters.trajectory1D[:,1])
        self.Trajectory1DImage.setXRange(np.min(self.parameters.trajectory1D[:,0])-0.1*width,np.max(self.parameters.trajectory1D[:,0])+0.1*width)
        self.Trajectory1DImage.setYRange(np.min(self.parameters.trajectory1D[:,1])-0.1*height,np.max(self.parameters.trajectory1D[:,1])+0.1*height)

        self.updateImages1DTrajectory()

    def updateCheckBoxDynamic2DTrajectory(self):
        """Updates the Dynamic CheckBox for the 2D Trajectory"""
        if self.Dynamic2DTrajectoryCheckBox.isChecked():
            self.parameters.toggleDynamic2DTrajectory = True
            self.parameters.toggleDynamic1DTrajectory = False
            self.parameters.toggleDynamic3BodyProblem = False
            self.trajectory2DTimer.start()
            self.trajectory1DTimer.stop()
            self.trajectory3BodyProblemTimer.stop()
            self.Dynamic1DTrajectoryCheckBox.setChecked(self.parameters.toggleDynamic1DTrajectory)
            self.Dynamic3BodyProblemCheckBox.setChecked(self.parameters.toggleDynamic3BodyProblems)
        else:
            self.parameters.toggleDynamic2DTrajectory = False
            if not self.Static2DTrajectoryCheckBox.isChecked():
                self.trajectory2DTimer.stop()
        self.updateImages2DTrajectory()

    def updateCheckBoxStatic2DTrajectory(self):
        """Updates the Static CheckBox for the 2D Trajectory"""
        if self.Static2DTrajectoryCheckBox.isChecked():
            self.parameters.toggleStatic2DTrajectory = True
        else:
            self.parameters.toggleStatic2DTrajectory = False
        self.updateStaticImages2DTrajectory()

    def updateCheckBoxObject2DTrajectory(self):
        """Updates the Objects CheckBox for the 2D Trajectory"""
        if self.Object2DTrajectoryCheckBox.isChecked():
            self.parameters.toggleObjectPositions2DTrajectory = True
        else:
            self.parameters.toggleObjectPositions2DTrajectory = False
        self.updateImages2DTrajectory()

    def updateCheckBoxCollision2DTrajectory(self):
        """Updates the Collision CheckBox for the 2D Trajectory"""
        if self.Collision2DTrajectoryCheckBox.isChecked():
            self.parameters.toggleCollision2DTrajectory = True
        else:
            self.parameters.toggleCollision2DTrajectory = False

    def updateCheckBoxAbsolute2DTrajectory(self):
        """Updates the Absolute CheckBox for the 2D Trajectory"""
        if self.Absolute2DTrajectoryCheckBox.isChecked():
            self.parameters.toggleAbsValues2DTrajectory = True
        else:
            self.parameters.toggleAbsValues2DTrajectory = False
        self.updateStaticImages2DTrajectory()
        self.reframe2DTrajectorySimulation()
        self.relabelGraphs2DTrajectory()

    def updateParameters2DTrajectory(self):
        """Updates the inner parameter for the 2D Trajectory. Doesn't restart the simulation until run is pressed."""
        try:
            self.parameters.mass2DTrajectory[0] = float(self.Mass12DTrajectoryLineEdit.text())
        except:
            self.parameters.mass2DTrajectory[0] = Constants.SolarMass
            self.Mass12DTrajectoryLineEdit.setText(f"{self.parameters.mass2DTrajectory[0]}")
        try:
            self.parameters.mass2DTrajectory[1] = float(self.Mass22DTrajectoryLineEdit.text())
        except:
            self.parameters.mass2DTrajectory[1] = Constants.SolarMass
            self.Mass22DTrajectoryLineEdit.setText(f"{self.parameters.mass2DTrajectory[1]}")
        name_tmp = self.Mass1Factor2DTrajectoryComboxBox.currentText()
        for dict, names in MechanicsStrings.MassFactor.items():
            if name_tmp in names.values():
                self.parameters.massFactor2DTrajectory[0] = dict
        name_tmp = self.Mass2Factor2DTrajectoryComboxBox.currentText()
        for dict, names in MechanicsStrings.MassFactor.items():
            if name_tmp in names.values():
                self.parameters.massFactor2DTrajectory[1] = dict


        try:
            self.parameters.initialPosition2DTrajectory[0,0] = float(self.Position1x2DTrajectoryLineEdit.text())
        except:
            self.parameters.initialPosition2DTrajectory[0,0] = 1.0
            self.Position1x2DTrajectoryLineEdit.setText(f"{self.parameters.initialPosition2DTrajectory[0,0]}")
        try:
            self.parameters.initialPosition2DTrajectory[0,1] = float(self.Position1y2DTrajectoryLineEdit.text())
        except:
            self.parameters.initialPosition2DTrajectory[0,1] = 0.0
            self.Position1y2DTrajectoryLineEdit.setText(f"{self.parameters.initialPosition2DTrajectory[0,1]}")
        try:
            self.parameters.initialPosition2DTrajectory[1,0] = float(self.Position2x2DTrajectoryLineEdit.text())
        except:
            self.parameters.initialPosition2DTrajectory[1,0] = 0.0
            self.Position2x2DTrajectoryLineEdit.setText(f"{self.parameters.initialPosition2DTrajectory[1,0]}")
        try:
            self.parameters.initialPosition2DTrajectory[1,1] = float(self.Position2y2DTrajectoryLineEdit.text())
        except:
            self.parameters.initialPosition2DTrajectory[1,1] = 0.0
            self.Position2y2DTrajectoryLineEdit.setText(f"{self.parameters.initialPosition2DTrajectory[1,1]}")
        name_tmp = self.Position1Factor2DTrajectoryComboxBox.currentText()
        for dict, names in MechanicsStrings.PositionFactor.items():
            if name_tmp in names.values():
                self.parameters.factorInitialPosition2DTrajectory[0] = dict
        name_tmp = self.Position2Factor2DTrajectoryComboxBox.currentText()
        for dict, names in MechanicsStrings.PositionFactor.items():
            if name_tmp in names.values():
                self.parameters.factorInitialPosition2DTrajectory[1] = dict

        try:
            self.parameters.initialVelocity2DTrajectory[0,0] = float(self.Speed1x2DTrajectoryLineEdit.text())
        except:
            self.parameters.initialVelocity2DTrajectory[0,0] = 1.0
            self.Speed1x2DTrajectoryLineEdit.setText(f"{self.parameters.initialVelocity2DTrajectory[0,0]}")
        try:
            self.parameters.initialVelocity2DTrajectory[0,1] = float(self.Speed1y2DTrajectoryLineEdit.text())
        except:
            self.parameters.initialVelocity2DTrajectory[0,1] = 0.0
            self.Speed1y2DTrajectoryLineEdit.setText(f"{self.parameters.initialVelocity2DTrajectory[0,1]}")
        try:
            self.parameters.initialVelocity2DTrajectory[1,0] = float(self.Speed2x2DTrajectoryLineEdit.text())
        except:
            self.parameters.initialVelocity2DTrajectory[1,0] = 0.0
            self.Speed2x2DTrajectoryLineEdit.setText(f"{self.parameters.initialVelocity2DTrajectory[1,0]}")
        try:
            self.parameters.initialVelocity2DTrajectory[1,1] = float(self.Speed2y2DTrajectoryLineEdit.text())
        except:
            self.parameters.initialVelocity2DTrajectory[1,1] = 0.0
            self.Speed2y2DTrajectoryLineEdit.setText(f"{self.parameters.initialVelocity2DTrajectory[1,1]}")
        name_tmp = self.Speed1Factor2DTrajectoryComboxBox.currentText()
        for dict, names in MechanicsStrings.SpeedFactor.items():
            if name_tmp in names.values():
                self.parameters.factorInitialVelocity2DTrajectory[0] = dict
        name_tmp = self.Speed2Factor2DTrajectoryComboxBox.currentText()
        for dict, names in MechanicsStrings.SpeedFactor.items():
            if name_tmp in names.values():
                self.parameters.factorInitialVelocity2DTrajectory[1] = dict


        try:
            self.parameters.finalTime2DTrajectory = float(self.endTime2DTrajectoryLineEdit.text())
        except:
            self.parameters.finalTime2DTrajectory = 10*10**7
            self.endTime2DTrajectoryLineEdit.setText(f"{self.parameters.finalTime2DTrajectory}")
        try:
            self.parameters.numberSteps2DTrajectory = float(self.numberSteps2DTrajectoryLineEdit.text())
        except:
            self.parameters.numberSteps2DTrajectory = 4
            self.numberSteps2DTrajectoryLineEdit.setText(f"{self.parameters.numberSteps2DTrajectory}")
        try:
            self.parameters.dynamicSpeed2DTrajectory = int(self.dynamicSpeed2DTrajectoryLineEdit.text())
            self.trajectory2DTimer.setInterval(self.parameters.dynamicSpeed2DTrajectory)
        except:
            self.parameters.dynamicSpeed2DTrajectory = 100
            self.trajectory2DTimer.setInterval(self.parameters.dynamicSpeed2DTrajectory)
            self.dynamicSpeed2DTrajectoryLineEdit.setText(f"{self.parameters.dynamicSpeed2DTrajectory}")
        try:
            self.parameters.step2DTrajectory = int(self.dynamicStep2DTrajectoryLineEdit.text())
        except:
            self.parameters.step2DTrajectory = 25
            self.dynamicStep2DTrajectoryLineEdit.setText(f"{self.parameters.step2DTrajectory}")

    def start2DTrajectorySimulation(self):
        """Runs a new simulation for the 2D Trajectory"""
        self.parameters.timeScale2DTrajectory = np.linspace(0,self.parameters.finalTime2DTrajectory,int(10**self.parameters.numberSteps2DTrajectory))

        self.parameters.PositionsTrajectory2D, self.parameters.VelocitiesTrajectory2D, self.parameters.AccelerationsTrajectory2D, self.parameters.trajectory2DEndValue = Mechanics1D.ManyBodiesGravitationalEvolution(
            mass = self.parameters.mass2DTrajectory*Constants.getConstants(self.parameters.massFactor2DTrajectory), 
            timeScale= self.parameters.timeScale2DTrajectory, 
            initialPos= self.parameters.initialPosition2DTrajectory*Constants.getConstants(self.parameters.factorInitialPosition2DTrajectory),
            initialVel=self.parameters.initialVelocity2DTrajectory*Constants.getConstants(self.parameters.factorInitialVelocity2DTrajectory), 
            massFixed=self.parameters.massesFix2DTrajectory,collision=self.parameters.toggleCollision2DTrajectory,
            radii = self.parameters.radius2DTrajectory*Constants.getConstants(self.parameters.radiusFactor2DTrajectory)
        )
        self.reframe2DTrajectorySimulation()
        self.restart2DTrajectorySimulation()

    def restart2DTrajectorySimulation(self):
        """Restarts the current simulation for the 2D Trajectory"""
        self.trajectory2DCounter = 0

        self.updateImages2DTrajectory()
        self.updateStaticImages2DTrajectory()

    def reframe2DTrajectorySimulation(self):
        """Reframes the current simulation for the 2D Trajectory"""
        width = np.max(self.parameters.PositionsTrajectory2D[:,:,0])-np.min(self.parameters.PositionsTrajectory2D[:,:,0])
        height = np.max(self.parameters.PositionsTrajectory2D[:,:,1])-np.min(self.parameters.PositionsTrajectory2D[:,:,1])
        self.Trajectory2DImage.setXRange(np.min(self.parameters.PositionsTrajectory2D[:,:,0])-0.1*width,np.max(self.parameters.PositionsTrajectory2D[:,:,0])+0.1*width)
        self.Trajectory2DImage.setYRange(np.min(self.parameters.PositionsTrajectory2D[:,:,1])-0.1*height,np.max(self.parameters.PositionsTrajectory2D[:,:,1])+0.1*height)
        if not self.parameters.toggleAbsValues2DTrajectory:
            width = np.max(self.parameters.VelocitiesTrajectory2D[:,:,0])-np.min(self.parameters.VelocitiesTrajectory2D[:,:,0])
            height = np.max(self.parameters.VelocitiesTrajectory2D[:,:,1])-np.min(self.parameters.VelocitiesTrajectory2D[:,:,1])
            self.TrajectoryVelocity2DImage.setXRange(np.min(self.parameters.VelocitiesTrajectory2D[:,:,0])-0.1*width,np.max(self.parameters.VelocitiesTrajectory2D[:,:,0])+0.1*width)
            self.TrajectoryVelocity2DImage.setYRange(np.min(self.parameters.VelocitiesTrajectory2D[:,:,1])-0.1*height,np.max(self.parameters.VelocitiesTrajectory2D[:,:,1])+0.1*height)
        else:
            heightTop = np.max((self.parameters.VelocitiesTrajectory2D[:,:,0]**2+self.parameters.VelocitiesTrajectory2D[:,:,1]**2)**(1/2))
            heightBot = np.min((self.parameters.VelocitiesTrajectory2D[:,:,0]**2+self.parameters.VelocitiesTrajectory2D[:,:,1]**2)**(1/2))
            self.TrajectoryVelocity2DImage.setXRange(0,self.parameters.timeScale2DTrajectory[-1])
            self.TrajectoryVelocity2DImage.setYRange(0.9*heightBot,1.1*heightTop)

        if not self.parameters.toggleAbsValues2DTrajectory:
            width = np.max(self.parameters.AccelerationsTrajectory2D[:,:,0])-np.min(self.parameters.AccelerationsTrajectory2D[:,:,0])
            height = np.max(self.parameters.AccelerationsTrajectory2D[:,:,1])-np.min(self.parameters.AccelerationsTrajectory2D[:,:,1])
            self.TrajectoryAcceleration2DImage.setXRange(np.min(self.parameters.AccelerationsTrajectory2D[:,:,0])-0.1*width,np.max(self.parameters.AccelerationsTrajectory2D[:,:,0])+0.1*width)
            self.TrajectoryAcceleration2DImage.setYRange(np.min(self.parameters.AccelerationsTrajectory2D[:,:,1])-0.1*height,np.max(self.parameters.AccelerationsTrajectory2D[:,:,1])+0.1*height)
        else:
            heightTop = np.max((self.parameters.AccelerationsTrajectory2D[:,:,0]**2+self.parameters.AccelerationsTrajectory2D[:,:,1]**2)**(1/2))
            heightBot = np.min((self.parameters.AccelerationsTrajectory2D[:,:,0]**2+self.parameters.AccelerationsTrajectory2D[:,:,1]**2)**(1/2))
            self.TrajectoryAcceleration2DImage.setXRange(0,self.parameters.timeScale2DTrajectory[-1])
            self.TrajectoryAcceleration2DImage.setYRange(0.9*heightBot,1.1*heightTop)

    def relabelGraphs2DTrajectory(self):
        """Relabels the graphs of the 2D trajectory depending on whether absolute value or not"""

        if not self.parameters.toggleAbsValues2DTrajectory:
            self.TrajectoryVelocity2DImage.setLabel("left","v_y",color = 'black')
            self.TrajectoryVelocity2DImage.setLabel("bottom","v_x",color = 'black')
            self.TrajectoryVelocity2DImage.setTitle(MechanicsStrings.Velocity[f"{self.language}"],color = 'black')

            self.TrajectoryAcceleration2DImage.setLabel("left","a_y",color = 'black')
            self.TrajectoryAcceleration2DImage.setLabel("bottom","a_x",color = 'black')
            self.TrajectoryAcceleration2DImage.setTitle(MechanicsStrings.Acceleration[f"{self.language}"],color = 'black')

        else:
            self.TrajectoryVelocity2DImage.setLabel("left","|v|",color = 'black')
            self.TrajectoryVelocity2DImage.setLabel("bottom","t",color = 'black')
            self.TrajectoryVelocity2DImage.setTitle("|"+MechanicsStrings.Velocity[f"{self.language}"]+"|",color = 'black')

            self.TrajectoryAcceleration2DImage.setLabel("left","|a|",color = 'black')
            self.TrajectoryAcceleration2DImage.setLabel("bottom","t",color = 'black')
            self.TrajectoryAcceleration2DImage.setTitle("|"+MechanicsStrings.Acceleration[f"{self.language}"]+"|",color = 'black')


    def updateCheckBoxDynamic3BodyProblem(self):
        """Updates the Dynamic CheckBox for the 3BodyProblem"""
        if self.Dynamic3BodyProblemCheckBox.isChecked():
            self.parameters.toggleDynamic2DTrajectory = False
            self.parameters.toggleDynamic1DTrajectory = False
            self.parameters.toggleDynamic3BodyProblem = True
            self.trajectory3BodyProblemTimer.start()
            self.trajectory2DTimer.stop()
            self.trajectory1DTimer.stop()
            self.Dynamic1DTrajectoryCheckBox.setChecked(self.parameters.toggleDynamic1DTrajectory)
            self.Dynamic2DTrajectoryCheckBox.setChecked(self.parameters.toggleDynamic2DTrajectory)
        else:
            self.parameters.toggleDynamic3BodyProblem = False
            if not self.Object3BodyProblemCheckBox.isChecked():
                self.trajectory3BodyProblemTimer.stop()
        self.updateImages3BodyProblem()

    def updateCheckBoxStatic3BodyProblem(self):
        """Updates the Static CheckBox for the 3BodyProblem"""
        if self.Static3BodyProblemCheckBox.isChecked():
            self.parameters.toggleStatic3BodyProblem = True
        else:
            self.parameters.toggleStatic3BodyProblem = False
        self.updateStaticImages3BodyProblem()

    def updateCheckBoxObject3BodyProblem(self):
        """Updates the Objects CheckBox for the 3BodyProblem"""
        if self.Object3BodyProblemCheckBox.isChecked():
            self.parameters.toggleObjectPositions3BodyProblem = True
        else:
            self.parameters.toggleObjectPositions3BodyProblem = False
        self.updateImages3BodyProblem()

    def updateCheckBoxCollision3BodyProblem(self):
        """Updates the Collision CheckBox for the 2D Trajectory"""
        if self.Collision3BodyProblemCheckBox.isChecked():
            self.parameters.toggleCollision3BodyProblem = True
        else:
            self.parameters.toggleCollision3BodyProblem = False

    def updateCheckBoxAbsValue3BodyProblem(self):
        """Updates the Absolute Values CheckBox for the 2D Trajectory"""
        if self.AbsValues3BodyProblemCheckBox.isChecked():
            self.parameters.toggleAbsValues3BodyProblem = True
        else:
            self.parameters.toggleAbsValues3BodyProblem = False

        self.updateStaticImages3BodyProblem()
        self.reframe3BodyProblemSimulation()
        self.relabelGraphs3BodyProblem()


    def start3BodyProblemSimulation(self):
        """Runs a new simulation for the 3BodyProblem"""
        self.parameters.timeScale3BodyProblem = np.linspace(0,self.parameters.finalTime3BodyProblem,int(10**self.parameters.numberSteps3BodyProblem))

        self.parameters.PositionsTrajectory3BodyProblem, self.parameters.VelocitiesTrajectory3BodyProblem, self.parameters.AccelerationsTrajectory3BodyProblem, self.parameters.trajectory3BodyProblemEndValue = Mechanics1D.ManyBodiesGravitationalEvolution(
            mass = self.parameters.mass3BodyProblem*Constants.getConstants(self.parameters.massFactor3BodyProblem), 
            timeScale= self.parameters.timeScale3BodyProblem, 
            initialPos= self.parameters.initialPosition3BodyProblem*Constants.getConstants(self.parameters.factorInitialPosition3BodyProblem),
            initialVel=self.parameters.initialVelocity3BodyProblem*Constants.getConstants(self.parameters.factorInitialVelocity3BodyProblem), 
            massFixed=self.parameters.massesFix3BodyProblem,collision=self.parameters.toggleCollision3BodyProblem,
            radii = self.parameters.radius3BodyProblem*Constants.getConstants(self.parameters.radiusFactor3BodyProblem)
        )
        self.restart3BodyProblemSimulation()
        self.reframe3BodyProblemSimulation()

    def restart3BodyProblemSimulation(self):
        """Restarts the current simulation for the 3BodyProblem"""
        self.trajectory3BodyProblemCounter = 0

        self.updateImages3BodyProblem()
        self.updateStaticImages3BodyProblem()

    def reframe3BodyProblemSimulation(self):
        """Reframes the current simulation for the 3BodyProblem"""
        width = np.max(self.parameters.PositionsTrajectory3BodyProblem[:,:,0])-np.min(self.parameters.PositionsTrajectory3BodyProblem[:,:,0])
        height = np.max(self.parameters.PositionsTrajectory3BodyProblem[:,:,1])-np.min(self.parameters.PositionsTrajectory3BodyProblem[:,:,1])
        self.Trajectory3BodyProblemImage.setXRange(np.min(self.parameters.PositionsTrajectory3BodyProblem[:,:,0])-0.1*width,np.max(self.parameters.PositionsTrajectory3BodyProblem[:,:,0])+0.1*width)
        self.Trajectory3BodyProblemImage.setYRange(np.min(self.parameters.PositionsTrajectory3BodyProblem[:,:,1])-0.1*height,np.max(self.parameters.PositionsTrajectory3BodyProblem[:,:,1])+0.1*height)
        if not self.parameters.toggleAbsValues3BodyProblem:
            width = np.max(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,0])-np.min(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,0])
            height = np.max(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,1])-np.min(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,1])
            self.TrajectoryVelocity3BodyProblem.setXRange(np.min(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,0])-0.1*width,np.max(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,0])+0.1*width)
            self.TrajectoryVelocity3BodyProblem.setYRange(np.min(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,1])-0.1*height,np.max(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,1])+0.1*height)
            width = np.max(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,0])-np.min(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,0])
            height = np.max(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,1])-np.min(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,1])
            self.TrajectoryAcceleration3BodyProblem.setXRange(np.min(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,0])-0.1*width,np.max(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,0])+0.1*width)
            self.TrajectoryAcceleration3BodyProblem.setYRange(np.min(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,1])-0.1*height,np.max(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,1])+0.1*height)
        else:
            heightTop = np.max((self.parameters.VelocitiesTrajectory3BodyProblem[:,:,0]**2+self.parameters.VelocitiesTrajectory3BodyProblem[:,:,1]**2)**(1/2))
            heightBot = np.min((self.parameters.VelocitiesTrajectory3BodyProblem[:,:,0]**2+self.parameters.VelocitiesTrajectory3BodyProblem[:,:,1]**2)**(1/2))
            self.TrajectoryVelocity3BodyProblem.setXRange(0,self.parameters.timeScale3BodyProblem[-1])
            self.TrajectoryVelocity3BodyProblem.setYRange(0.9*heightBot,1.1*heightTop)

            heightTop = np.max((self.parameters.AccelerationsTrajectory3BodyProblem[:,:,0]**2+self.parameters.AccelerationsTrajectory3BodyProblem[:,:,1]**2)**(1/2))
            heightBot = np.min((self.parameters.AccelerationsTrajectory3BodyProblem[:,:,0]**2+self.parameters.AccelerationsTrajectory3BodyProblem[:,:,1]**2)**(1/2))
            self.TrajectoryAcceleration3BodyProblem.setXRange(0,self.parameters.timeScale3BodyProblem[-1])
            self.TrajectoryAcceleration3BodyProblem.setYRange(0.9*heightBot,1.1*heightTop)

    def relabelGraphs3BodyProblem(self):
        """Relabels the graphs of the 3 Body Problem depending on whether absolute value or not"""

        if not self.parameters.toggleAbsValues3BodyProblem:
            self.TrajectoryVelocity3BodyProblem.setLabel("left","v_y",color = 'black')
            self.TrajectoryVelocity3BodyProblem.setLabel("bottom","v_x",color = 'black')
            self.TrajectoryVelocity3BodyProblem.setTitle(MechanicsStrings.Velocity[f"{self.language}"],color = 'black')

            self.TrajectoryAcceleration3BodyProblem.setLabel("left","a_y",color = 'black')
            self.TrajectoryAcceleration3BodyProblem.setLabel("bottom","a_x",color = 'black')
            self.TrajectoryAcceleration3BodyProblem.setTitle(MechanicsStrings.Acceleration[f"{self.language}"],color = 'black')

        else:
            self.TrajectoryVelocity3BodyProblem.setLabel("left","|v|",color = 'black')
            self.TrajectoryVelocity3BodyProblem.setLabel("bottom","t",color = 'black')
            self.TrajectoryVelocity3BodyProblem.setTitle("|"+MechanicsStrings.Velocity[f"{self.language}"]+"|",color = 'black')

            self.TrajectoryAcceleration3BodyProblem.setLabel("left","|a|",color = 'black')
            self.TrajectoryAcceleration3BodyProblem.setLabel("bottom","t",color = 'black')
            self.TrajectoryAcceleration3BodyProblem.setTitle("|"+MechanicsStrings.Acceleration[f"{self.language}"]+"|",color = 'black')


    def updateParameters3BodyProblem(self):
        """Updates the inner parameter for the 3BodyProblem. Doesn't restart the simulation until run is pressed."""
        for i in range(self.parameters.numberOfMass3BodyProblem):
            try:
                self.parameters.mass3BodyProblem[i] = float(self.Mass3BodyProblemLineEdit[i].text())
            except:
                self.parameters.mass3BodyProblem[i] = Constants.SolarMass
                self.Mass3BodyProblemLineEdit[i].setText(f"{self.parameters.mass2DTrajectory[0]}")
            name_tmp = self.MassFactor3BodyProblemComboBox[i].currentText()
            for dict, names in MechanicsStrings.MassFactor.items():
                if name_tmp in names.values():
                    self.parameters.massFactor3BodyProblem[i] = dict

            name_tmp = self.PositionFactor3BodyProblemComboxBox[i].currentText()
            for dict, names in MechanicsStrings.PositionFactor.items():
                if name_tmp in names.values():
                    self.parameters.factorInitialPosition3BodyProblem[i] = dict

            name_tmp = self.SpeedFactor3BodyProblemComboxBox[i].currentText()
            for dict, names in MechanicsStrings.SpeedFactor.items():
                if name_tmp in names.values():
                    self.parameters.factorInitialVelocity3BodyProblem[i] = dict

        for i in range(self.parameters.numberOfMass3BodyProblem):
            for j in range(2):
                try:
                    self.parameters.initialPosition3BodyProblem[i,j] = float(self.Position3BodyProblemLineEdit[i,j].text())
                except:
                    self.parameters.initialPosition3BodyProblem[i,j] = 1.0
                    self.Position3BodyProblemLineEdit[i,j].setText(f"{self.parameters.initialPosition3BodyProblem[i,j]}")
                try:
                    self.parameters.initialVelocity3BodyProblem[i,j] = float(self.Speed3BodyProblemLineEdit[i,j].text())
                except:
                    self.parameters.initialVelocity3BodyProblem[i,j] = 1.0
                    self.Speed3BodyProblemLineEdit[i,j].setText(f"{self.parameters.initialVelocity3BodyProblem[i,j]}")




        try:
            self.parameters.finalTime3BodyProblem = float(self.endTime3BodyProblemLineEdit.text())
        except:
            self.parameters.finalTime3BodyProblem = 10*10**7
            self.endTime3BodyProblemLineEdit.setText(f"{self.parameters.finalTime3BodyProblem}")
        try:
            self.parameters.numberSteps3BodyProblem = float(self.numberSteps3BodyProblemLineEdit.text())
        except:
            self.parameters.numberSteps3BodyProblem = 4
            self.numberSteps3BodyProblemLineEdit.setText(f"{self.parameters.numberSteps3BodyProblem}")
        try:
            self.parameters.dynamicSpeed3BodyProblem = int(self.dynamicSpeed3BodyProblemLineEdit.text())
            self.trajectory3BodyProblemTimer.setInterval(self.parameters.dynamicSpeed3BodyProblem)
        except:
            self.parameters.dynamicSpeed3BodyProblem = 100
            self.trajectory3BodyProblemTimer.setInterval(self.parameters.dynamicSpeed3BodyProblem)
            self.dynamicSpeed3BodyProblemLineEdit.setText(f"{self.parameters.dynamicSpeed3BodyProblem}")
        try:
            self.parameters.step3BodyProblem = int(self.dynamicStep3BodyProblemLineEdit.text())
        except:
            self.parameters.step3BodyProblem = 25
            self.dynamicStep3BodyProblemLineEdit.setText(f"{self.parameters.step3BodyProblem}")

################################
    def updateImages1DTrajectory(self):
        """Updates all the 1D Trajectory Images"""
        self.updateVelocityImage1DTrajectory()
        self.updateAccelerationImage1DTrajectory()
        self.updateImage1DTrajectory()

        if self.trajectory1DCounter <= self.parameters.trajectory1DEndValue:
            self.trajectory1DCounter +=1
        else:
            self.trajectory1DCounter = 0

    def updateVelocityImage1DTrajectory(self):
        if self.parameters.toggleDynamic1DTrajectory:
            self.TrajectoryVelocity1DImageDynamic.setData(self.parameters.Velocitiestrajectory1D[:self.trajectory1DCounter,0],
                                         self.parameters.Velocitiestrajectory1D[:self.trajectory1DCounter,1])
        else: self.TrajectoryVelocity1DImageDynamic.setData()
        if self.parameters.toggleStatic1DTrajectory:
            self.TrajectoryVelocity1DImageStatic.setData(self.parameters.Velocitiestrajectory1D[:self.parameters.trajectory1DEndValue+1,0],
                                         self.parameters.Velocitiestrajectory1D[:self.parameters.trajectory1DEndValue+1,1])   
        else: self.TrajectoryVelocity1DImageStatic.setData()

    def updateAccelerationImage1DTrajectory(self):
        if self.parameters.toggleDynamic1DTrajectory or self.parameters.toggleStatic1DTrajectory:
            self.AccelerationStatic1DTrajectory.setData([self.parameters.initialAcceleration1D[0]],
                                                     [self.parameters.initialAcceleration1D[1]])       
    def updateImage1DTrajectory(self):
        if self.parameters.toggleDynamic1DTrajectory:
            self.Trajectory1DImageDynamic.setData(self.parameters.trajectory1D[:self.trajectory1DCounter,0],
                                         self.parameters.trajectory1D[:self.trajectory1DCounter,1])
        else: self.Trajectory1DImageDynamic.setData()
        if self.parameters.toggleStatic1DTrajectory:
            self.Trajectory1DImageStatic.setData(self.parameters.trajectory1D[:self.parameters.trajectory1DEndValue+1,0],
                                         self.parameters.trajectory1D[:self.parameters.trajectory1DEndValue+1,1])    
        else: self.Trajectory1DImageStatic.setData()

    def updateImages2DTrajectory(self):
        """Updates all the 2D Trajectory Images"""
        self.updateVelocityImage2DTrajectory()
        self.updateAccelerationImage2DTrajectory()
        self.updateImage2DTrajectory()

        if self.trajectory2DCounter + self.parameters.step2DTrajectory < self.parameters.trajectory2DEndValue:
            self.trajectory2DCounter += self.parameters.step2DTrajectory
        else:
            self.trajectory2DCounter = 0

    def updateStaticImages2DTrajectory(self):
        if self.parameters.toggleStatic2DTrajectory:
            if not self.parameters.toggleAbsValues2DTrajectory:
                self.TrajectoryVelocity2DImageStatic1.setData(self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,0,0],
                                         self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,0,1])   
                self.TrajectoryVelocity2DImageStatic2.setData(self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,1,0],
                                         self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,1,1])   
            else:
                self.TrajectoryVelocity2DImageStatic1.setData(self.parameters.timeScale2DTrajectory[:self.parameters.trajectory2DEndValue],
                                                              (self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,0,0]**2+
                                         self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,0,1]**2)**(1/2))   
                self.TrajectoryVelocity2DImageStatic2.setData(self.parameters.timeScale2DTrajectory[:self.parameters.trajectory2DEndValue],
                                                              (self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,1,0]**2+
                                         self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,1,1]**2)**(1/2))   
        else: 
            self.TrajectoryVelocity2DImageStatic1.setData()
            self.TrajectoryVelocity2DImageStatic2.setData()
        if self.parameters.toggleStatic2DTrajectory:
            if not self.parameters.toggleAbsValues2DTrajectory:
                self.TrajectoryAcceleration2DImageStatic1.setData(self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,0,0],
                                        self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,0,1])   
                self.TrajectoryAcceleration2DImageStatic2.setData(self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,1,0],
                                        self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,1,1])   
            else:
                self.TrajectoryAcceleration2DImageStatic1.setData(self.parameters.timeScale2DTrajectory[1:self.parameters.trajectory2DEndValue],
                                                                  (self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,0,0]**2+
                                        self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,0,1]**2)**(1/2))   
                self.TrajectoryAcceleration2DImageStatic2.setData(self.parameters.timeScale2DTrajectory[1:self.parameters.trajectory2DEndValue],
                                                                  (self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,1,0]**2+
                                        self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,1,1]**2)**(1/2))
        else: 
            self.TrajectoryAcceleration2DImageStatic1.setData()
            self.TrajectoryAcceleration2DImageStatic2.setData()
        if self.parameters.toggleStatic2DTrajectory:
            self.Trajectory2DImageStatic1.setData(self.parameters.PositionsTrajectory2D[:self.parameters.trajectory2DEndValue,0,0],
                                         self.parameters.PositionsTrajectory2D[:self.parameters.trajectory2DEndValue,0,1])    
            self.Trajectory2DImageStatic2.setData(self.parameters.PositionsTrajectory2D[:self.parameters.trajectory2DEndValue,1,0],
                                         self.parameters.PositionsTrajectory2D[:self.parameters.trajectory2DEndValue,1,1])    

        else: 
            self.Trajectory2DImageStatic1.setData()
            self.Trajectory2DImageStatic2.setData()

    def updateVelocityImage2DTrajectory(self):
        if self.parameters.toggleDynamic2DTrajectory:
            if not self.parameters.toggleAbsValues2DTrajectory:
                self.TrajectoryVelocity2DImageDynamic1.setData(self.parameters.VelocitiesTrajectory2D[:self.trajectory2DCounter:10,0,0],
                                         self.parameters.VelocitiesTrajectory2D[:self.trajectory2DCounter:10,0,1])
                self.TrajectoryVelocity2DImageDynamic2.setData(self.parameters.VelocitiesTrajectory2D[:self.trajectory2DCounter:10,1,0],
                                         self.parameters.VelocitiesTrajectory2D[:self.trajectory2DCounter:10,1,1])
            else:
                self.TrajectoryVelocity2DImageDynamic1.setData(self.parameters.timeScale2DTrajectory[:self.trajectory2DCounter:10],
                                                               (self.parameters.VelocitiesTrajectory2D[:self.trajectory2DCounter:10,0,0]**2+
                                         self.parameters.VelocitiesTrajectory2D[:self.trajectory2DCounter:10,0,1]**2)**(1/2))
                self.TrajectoryVelocity2DImageDynamic2.setData(self.parameters.timeScale2DTrajectory[:self.trajectory2DCounter:10],
                                                               (self.parameters.VelocitiesTrajectory2D[:self.trajectory2DCounter:10,1,0]**2+
                                         self.parameters.VelocitiesTrajectory2D[:self.trajectory2DCounter:10,1,1]**2)**(1/2))
        else: 
            self.TrajectoryVelocity2DImageDynamic1.setData()
            self.TrajectoryVelocity2DImageDynamic2.setData()

        if self.parameters.toggleObjectPositions2DTrajectory:
            if not self.parameters.toggleAbsValues2DTrajectory:
                self.TrajectoryVelocity2DImageObject1.setData([self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,0,0]],
                                                                        [self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,0,1]])
                self.TrajectoryVelocity2DImageObject2.setData([self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,1,0]],
                                                                            [self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,1,1]])
            else:
                self.TrajectoryVelocity2DImageObject1.setData([self.parameters.timeScale2DTrajectory[self.trajectory2DCounter]],
                                                              [(self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,0,0]**2+self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,0,1]**2)**(1/2)])
                self.TrajectoryVelocity2DImageObject2.setData([self.parameters.timeScale2DTrajectory[self.trajectory2DCounter]],
                                                              [(self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,1,0]**2+self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,1,1]**2)**(1/2)])                
        else: 
            self.TrajectoryVelocity2DImageObject1.setData()
            self.TrajectoryVelocity2DImageObject2.setData()

    def updateAccelerationImage2DTrajectory(self):
        if self.parameters.toggleDynamic2DTrajectory:
            if not self.parameters.toggleAbsValues2DTrajectory:
                self.TrajectoryAcceleration2DImageDynamic1.setData(self.parameters.AccelerationsTrajectory2D[1:self.trajectory2DCounter:10,0,0],
                                         self.parameters.AccelerationsTrajectory2D[1:self.trajectory2DCounter:10,0,1])
                self.TrajectoryAcceleration2DImageDynamic2.setData(self.parameters.AccelerationsTrajectory2D[1:self.trajectory2DCounter:10,1,0],
                                         self.parameters.AccelerationsTrajectory2D[1:self.trajectory2DCounter:10,1,1])
            else:
                self.TrajectoryAcceleration2DImageDynamic1.setData(self.parameters.timeScale2DTrajectory[1:self.trajectory2DCounter:10],
                                                                   (self.parameters.AccelerationsTrajectory2D[1:self.trajectory2DCounter:10,0,0]**2+
                                         self.parameters.AccelerationsTrajectory2D[1:self.trajectory2DCounter:10,0,1]**2)**(1/2))
                self.TrajectoryAcceleration2DImageDynamic2.setData(self.parameters.timeScale2DTrajectory[1:self.trajectory2DCounter:10],
                                                                   (self.parameters.AccelerationsTrajectory2D[1:self.trajectory2DCounter:10,1,0]**2+
                                         self.parameters.AccelerationsTrajectory2D[1:self.trajectory2DCounter:10,1,1]**2)**(1/2))

        else: 
            self.TrajectoryAcceleration2DImageDynamic1.setData()
            self.TrajectoryAcceleration2DImageDynamic2.setData()

        if self.parameters.toggleObjectPositions2DTrajectory:
            if not self.parameters.toggleAbsValues2DTrajectory:
                self.TrajectoryAcceleration2DImageObject1.setData([self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,0,0]],
                                                                        [self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,0,1]])
                self.TrajectoryAcceleration2DImageObject2.setData([self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,1,0]],
                                                                        [self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,1,1]])
            else:
                self.TrajectoryAcceleration2DImageObject1.setData([self.parameters.timeScale2DTrajectory[self.trajectory2DCounter]],
                                                                  [(self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,0,0]**2+
                                                                        self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,0,1]**2)**(1/2)])
                self.TrajectoryAcceleration2DImageObject2.setData([self.parameters.timeScale2DTrajectory[self.trajectory2DCounter]],
                                                                  [(self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,1,0]**2+
                                                                        self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,1,1]**2)**(1/2)])
 
        else: 
            self.TrajectoryAcceleration2DImageObject1.setData()
            self.TrajectoryAcceleration2DImageObject2.setData()      
    def updateImage2DTrajectory(self):
        if self.parameters.toggleDynamic2DTrajectory:
            self.Trajectory2DImageDynamic1.setData(self.parameters.PositionsTrajectory2D[:self.trajectory2DCounter:10,0,0],
                                         self.parameters.PositionsTrajectory2D[:self.trajectory2DCounter:10,0,1])
            self.Trajectory2DImageDynamic2.setData(self.parameters.PositionsTrajectory2D[:self.trajectory2DCounter:10,1,0],
                                         self.parameters.PositionsTrajectory2D[:self.trajectory2DCounter:10,1,1])
        else: 
            self.Trajectory2DImageDynamic1.setData()
            self.Trajectory2DImageDynamic2.setData()

        if self.parameters.toggleObjectPositions2DTrajectory:
            self.Trajectory2DImageObject1.setData([self.parameters.PositionsTrajectory2D[self.trajectory2DCounter,0,0]],
                                                                        [self.parameters.PositionsTrajectory2D[self.trajectory2DCounter,0,1]])
            self.Trajectory2DImageObject2.setData([self.parameters.PositionsTrajectory2D[self.trajectory2DCounter,1,0]],
                                                                        [self.parameters.PositionsTrajectory2D[self.trajectory2DCounter,1,1]])
        else: 
            self.Trajectory2DImageObject1.setData()
            self.Trajectory2DImageObject2.setData()

    def updateImages3BodyProblem(self):
        """Updates all the 3BodyProblem Images"""
        self.updateVelocityImage3BodyProblem()
        self.updateAccelerationImage3BodyProblem()
        self.updateImage3BodyProblem()

        if self.trajectory3BodyProblemCounter + self.parameters.step3BodyProblem < self.parameters.trajectory3BodyProblemEndValue:
            self.trajectory3BodyProblemCounter += self.parameters.step3BodyProblem
        else:
            self.trajectory3BodyProblemCounter = 0

    def updateImage3BodyProblem(self):
        for i in range(self.parameters.numberOfMass3BodyProblem):
            if self.parameters.toggleDynamic3BodyProblem:
                self.Trajectory3BodyProblemDynamic[i].setData(self.parameters.PositionsTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter:10,i,0],
                                            self.parameters.PositionsTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter:10,i,1])
            else: 
                self.Trajectory3BodyProblemDynamic[i].setData()

            if self.parameters.toggleObjectPositions3BodyProblem:
                self.Trajectory3BodyProblemObject[i].setData([self.parameters.PositionsTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,0]],
                                                                            [self.parameters.PositionsTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,1]])
            else: 
                self.Trajectory3BodyProblemObject[i].setData()

    def updateVelocityImage3BodyProblem(self):
        for i in range(self.parameters.numberOfMass3BodyProblem):
            if self.parameters.toggleDynamic3BodyProblem:
                if not self.parameters.toggleAbsValues3BodyProblem:
                    self.TrajectoryVelocity3BodyProblemDynamic[i].setData(self.parameters.VelocitiesTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter:10,i,0],
                                            self.parameters.VelocitiesTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter:10,i,1])
                else:
                    self.TrajectoryVelocity3BodyProblemDynamic[i].setData(self.parameters.timeScale3BodyProblem[:self.trajectory3BodyProblemCounter:10],
                                            (self.parameters.VelocitiesTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter:10,i,0]**2+
                                            self.parameters.VelocitiesTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter:10,i,1]**2)**(1/2))

            else: 
                self.TrajectoryVelocity3BodyProblemDynamic[i].setData()

            if self.parameters.toggleObjectPositions3BodyProblem:
                if not self.parameters.toggleAbsValues3BodyProblem:
                    self.TrajectoryVelocity3BodyProblemObject[i].setData([self.parameters.VelocitiesTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,0]],
                                                                            [self.parameters.VelocitiesTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,1]])
                else:
                    self.TrajectoryVelocity3BodyProblemObject[i].setData([self.parameters.timeScale3BodyProblem[self.trajectory3BodyProblemCounter]],
                                            [(self.parameters.VelocitiesTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,0]**2+
                                            self.parameters.VelocitiesTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,1]**2)**(1/2)])
            else: 
                self.TrajectoryVelocity3BodyProblemObject[i].setData()

    def updateAccelerationImage3BodyProblem(self):
        for i in range(self.parameters.numberOfMass3BodyProblem):
            if self.parameters.toggleDynamic3BodyProblem:
                if not self.parameters.toggleAbsValues3BodyProblem:
                    self.TrajectoryAcceleration3BodyProblemDynamic[i].setData(self.parameters.AccelerationsTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter:10,i,0],
                                            self.parameters.AccelerationsTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter:10,i,1])
                else:
                    self.TrajectoryAcceleration3BodyProblemDynamic[i].setData(self.parameters.timeScale3BodyProblem[:self.trajectory3BodyProblemCounter:10],
                                            (self.parameters.AccelerationsTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter:10,i,0]**2+
                                            self.parameters.AccelerationsTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter:10,i,1]**2)*(1/2))
            else: 
                self.TrajectoryAcceleration3BodyProblemDynamic[i].setData()

            if self.parameters.toggleObjectPositions3BodyProblem:
                if not self.parameters.toggleAbsValues3BodyProblem:
                    self.TrajectoryAcceleration3BodyProblemObject[i].setData([self.parameters.AccelerationsTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,0]],
                                                                            [self.parameters.AccelerationsTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,1]])
                else:
                    self.TrajectoryAcceleration3BodyProblemObject[i].setData([self.parameters.timeScale3BodyProblem[self.trajectory3BodyProblemCounter]],
                                                [(self.parameters.AccelerationsTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,0]**2+
                                                self.parameters.AccelerationsTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,1]**2)**(1/2)])
            else: 
                self.TrajectoryAcceleration3BodyProblemObject[i].setData()


    def updateStaticImages3BodyProblem(self):
        for i in range(self.parameters.numberOfMass3BodyProblem):
            if self.parameters.toggleStatic3BodyProblem:
                if not self.parameters.toggleAbsValues3BodyProblem:
                    self.TrajectoryVelocity3BodyProblemStatic[i].setData(self.parameters.VelocitiesTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,0],
                                         self.parameters.VelocitiesTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,1])   
                    self.TrajectoryAcceleration3BodyProblemStatic[i].setData(self.parameters.AccelerationsTrajectory3BodyProblem[1:self.parameters.trajectory3BodyProblemEndValue,i,0],
                                         self.parameters.AccelerationsTrajectory3BodyProblem[1:self.parameters.trajectory3BodyProblemEndValue,i,1])   
                else:
                    self.TrajectoryVelocity3BodyProblemStatic[i].setData(self.parameters.timeScale3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue],
                                        (self.parameters.VelocitiesTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,0]**2+
                                        self.parameters.VelocitiesTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,1]**2)**(1/2))   
                    self.TrajectoryAcceleration3BodyProblemStatic[i].setData(self.parameters.timeScale3BodyProblem[1:self.parameters.trajectory3BodyProblemEndValue],
                                        (self.parameters.AccelerationsTrajectory3BodyProblem[1:self.parameters.trajectory3BodyProblemEndValue,i,0]**2+
                                        self.parameters.AccelerationsTrajectory3BodyProblem[1:self.parameters.trajectory3BodyProblemEndValue,i,1]**2)**(1/2))   

                self.Trajectory3BodyProblemStatic[i].setData(self.parameters.PositionsTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,0],
                                         self.parameters.PositionsTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,1])    
            else: 
                self.TrajectoryVelocity3BodyProblemStatic[i].setData()
                self.TrajectoryAcceleration3BodyProblemStatic[i].setData()
                self.Trajectory3BodyProblemStatic[i].setData()

    def initializeVelocityImage1DTrajectory(self):
        """Updates the 1D Velocity Trajectory Image"""
        pen1 = pg.mkPen(color="blue", width = 5)
        pen2 = pg.mkPen(color="orange", width = 3, style=QtCore.Qt.DashLine)

        self.TrajectoryVelocity1DImageDynamic = self.TrajectoryVelocity1DImage.plot(self.parameters.Velocitiestrajectory1D[:self.trajectory1DCounter,0],
                                         self.parameters.Velocitiestrajectory1D[:self.trajectory1DCounter,1], pen = pen1)
        self.TrajectoryVelocity1DImageStatic = self.TrajectoryVelocity1DImage.plot(self.parameters.Velocitiestrajectory1D[:self.parameters.trajectory1DEndValue+1,0],
                                         self.parameters.Velocitiestrajectory1D[:self.parameters.trajectory1DEndValue+1,1], pen = pen2)


        width = np.max(self.parameters.Velocitiestrajectory1D[:,0])-np.min(self.parameters.Velocitiestrajectory1D[:,0])
        height = np.max(self.parameters.Velocitiestrajectory1D[:,1])-np.min(self.parameters.Velocitiestrajectory1D[:,1])
        self.TrajectoryVelocity1DImage.setXRange(np.min(self.parameters.Velocitiestrajectory1D[:,0])-0.1*width,np.max(self.parameters.Velocitiestrajectory1D[:,0])+0.1*width)
        self.TrajectoryVelocity1DImage.setYRange(np.min(self.parameters.Velocitiestrajectory1D[:,1])-0.1*height,np.max(self.parameters.Velocitiestrajectory1D[:,1])+0.1*height)

        self.TrajectoryVelocity1DImage.setBackground("w")

        self.TrajectoryVelocity1DImage.showGrid(x=True, y=True)
        self.TrajectoryVelocity1DImage.setLabel("left","v_y",color = 'black')
        self.TrajectoryVelocity1DImage.setLabel("bottom","v_x",color = 'black')
        self.TrajectoryVelocity1DImage.setTitle(MechanicsStrings.Velocity[f"{self.language}"],color = 'black')

    def initializeAccelerationImage1DTrajectory(self):
        """Updates the 1D Velocity Trajectory Image"""

        self.AccelerationStatic1DTrajectory = self.TrajectoryAcceleration1DImage.plot([self.parameters.initialAcceleration1D[0]],
                                                     [self.parameters.initialAcceleration1D[1]],
                                                     symbol = '+', symbolsize = 15, symbolBrush = "blue")
        self.TrajectoryAcceleration1DImage.setBackground("w")

        self.TrajectoryAcceleration1DImage.showGrid(x=True, y=True)
        self.TrajectoryAcceleration1DImage.setLabel("left","a_y",color = 'black')
        self.TrajectoryAcceleration1DImage.setLabel("bottom","a_x",color = 'black')
        self.TrajectoryAcceleration1DImage.setTitle(MechanicsStrings.Acceleration[f"{self.language}"],color = 'black')


    def initializeImage1DTrajectory(self):
        """Updates the 1D Trajectory Image"""
        pen1 = pg.mkPen(color="blue", width = 5)
        pen2 = pg.mkPen(color="orange", width = 3, style=QtCore.Qt.DashLine)
        self.Trajectory1DImageDynamic = self.Trajectory1DImage.plot(self.parameters.trajectory1D[:self.trajectory1DCounter,0],
                                         self.parameters.trajectory1D[:self.trajectory1DCounter,1], pen = pen1)
        self.Trajectory1DImageStatic = self.Trajectory1DImage.plot(self.parameters.trajectory1D[:self.parameters.trajectory1DEndValue+1,0],
                                         self.parameters.trajectory1D[:self.parameters.trajectory1DEndValue+1,1], pen = pen2)
        if self.parameters.toggleGround1D:
            self.Trajectory1DImage.plot([-10000,10000],[0,0])

        self.Trajectory1DImage.setBackground("w")
        width = np.max(self.parameters.trajectory1D[:,0])-np.min(self.parameters.trajectory1D[:,0])
        height = np.max(self.parameters.trajectory1D[:,1])-np.min(self.parameters.trajectory1D[:,1])
        self.Trajectory1DImage.setXRange(np.min(self.parameters.trajectory1D[:,0])-0.1*width,np.max(self.parameters.trajectory1D[:,0])+0.1*width)
        self.Trajectory1DImage.setYRange(np.min(self.parameters.trajectory1D[:,1])-0.1*height,np.max(self.parameters.trajectory1D[:,1])+0.1*height)

        self.Trajectory1DImage.showGrid(x=True,y=True)
        self.Trajectory1DImage.setLabel("bottom","x",color = 'black')
        self.Trajectory1DImage.setLabel("left","y",color = 'black')
        self.Trajectory1DImage.setTitle(MechanicsStrings.trajectory1D[f"{self.language}"],color = 'black')


    def initializeImage2DTrajectory(self):
        """Updates the 2D Trajectory Image"""
        self.pen1 = pg.mkPen(color="blue", width = 5)
        self.pen2 = pg.mkPen(color="green", width = 5)
        self.pen3 = pg.mkPen(color="orange", width = 3, style=QtCore.Qt.DashLine)
        self.pen4 = pg.mkPen(color="red", width = 3, style=QtCore.Qt.DashLine)
        self.Trajectory2DImageDynamic1 = self.Trajectory2DImage.plot(self.parameters.PositionsTrajectory2D[:self.trajectory2DCounter,0,0],
                                         self.parameters.PositionsTrajectory2D[:self.trajectory2DCounter,0,1], pen = self.pen1)
        self.Trajectory2DImageDynamic2 = self.Trajectory2DImage.plot(self.parameters.PositionsTrajectory2D[:self.trajectory2DCounter,1,0],
                                         self.parameters.PositionsTrajectory2D[:self.trajectory2DCounter,1,1], pen = self.pen2)

        self.Trajectory2DImageStatic1 = self.Trajectory2DImage.plot(self.parameters.PositionsTrajectory2D[:self.parameters.trajectory2DEndValue,0,0],
                                         self.parameters.PositionsTrajectory2D[:self.parameters.trajectory2DEndValue,0,1], pen = self.pen3)
        self.Trajectory2DImageStatic2 = self.Trajectory2DImage.plot(self.parameters.PositionsTrajectory2D[:self.parameters.trajectory2DEndValue,1,0],
                                         self.parameters.PositionsTrajectory2D[:self.parameters.trajectory2DEndValue,1,1], pen = self.pen4)

        self.Trajectory2DImageObject1 = self.Trajectory2DImage.plot([self.parameters.PositionsTrajectory2D[self.trajectory2DCounter,0,0]],
                                                                        [self.parameters.PositionsTrajectory2D[self.trajectory2DCounter,0,1]],
                                                                        symbol = "o",
                                                                        pen = self.pen1)
        self.Trajectory2DImageObject2 = self.Trajectory2DImage.plot([self.parameters.PositionsTrajectory2D[self.trajectory2DCounter,1,0]],
                                                                        [self.parameters.PositionsTrajectory2D[self.trajectory2DCounter,1,1]],
                                                                        symbol = "o",
                                                                        pen = self.pen2)

        self.Trajectory2DImage.setBackground("w")
        width = np.max(self.parameters.PositionsTrajectory2D[:,:,0])-np.min(self.parameters.PositionsTrajectory2D[:,:,0])
        height = np.max(self.parameters.PositionsTrajectory2D[:,:,1])-np.min(self.parameters.PositionsTrajectory2D[:,:,1])
        self.Trajectory2DImage.setXRange(np.min(self.parameters.PositionsTrajectory2D[:,:,0])-0.1*width,np.max(self.parameters.PositionsTrajectory2D[:,:,0])+0.1*width)
        self.Trajectory2DImage.setYRange(np.min(self.parameters.PositionsTrajectory2D[:,:,1])-0.1*height,np.max(self.parameters.PositionsTrajectory2D[:,:,1])+0.1*height)

        self.Trajectory2DImage.showGrid(x=True,y=True)
        self.Trajectory2DImage.setLabel("bottom","x",color = 'black')
        self.Trajectory2DImage.setLabel("left","y",color = 'black')
        self.Trajectory2DImage.setTitle(MechanicsStrings.trajectory1D[f"{self.language}"],color = 'black')

    def initializeVelocityImage2DTrajectory(self):
        """Updates the 2D Velocity Trajectory Image"""

        self.TrajectoryVelocity2DImageDynamic1 = self.TrajectoryVelocity2DImage.plot(self.parameters.VelocitiesTrajectory2D[:self.trajectory1DCounter,0,0],
                                        self.parameters.VelocitiesTrajectory2D[:self.trajectory1DCounter,0,1], pen = self.pen1)
        self.TrajectoryVelocity2DImageDynamic2 = self.TrajectoryVelocity2DImage.plot(self.parameters.VelocitiesTrajectory2D[:self.trajectory1DCounter,1,0],
                                        self.parameters.VelocitiesTrajectory2D[:self.trajectory1DCounter,1,1], pen = self.pen2)

        self.TrajectoryVelocity2DImageStatic1 = self.TrajectoryVelocity2DImage.plot(self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,0,0],
                                         self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,0,1], pen = self.pen3)
        self.TrajectoryVelocity2DImageStatic2 = self.TrajectoryVelocity2DImage.plot(self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,1,0],
                                         self.parameters.VelocitiesTrajectory2D[:self.parameters.trajectory2DEndValue,1,1], pen = self.pen4)

        self.TrajectoryVelocity2DImageObject1 = self.TrajectoryVelocity2DImage.plot([self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,0,0]],
                                                                        [self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,0,1]],
                                                                        symbol = "o",
                                                                        pen = self.pen1)
        self.TrajectoryVelocity2DImageObject2 = self.TrajectoryVelocity2DImage.plot([self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,1,0]],
                                                                        [self.parameters.VelocitiesTrajectory2D[self.trajectory2DCounter,1,1]],
                                                                        symbol = "o",
                                                                        pen = self.pen2)


        width = np.max(self.parameters.VelocitiesTrajectory2D[:,:,0])-np.min(self.parameters.VelocitiesTrajectory2D[:,:,0])
        height = np.max(self.parameters.VelocitiesTrajectory2D[:,:,1])-np.min(self.parameters.VelocitiesTrajectory2D[:,:,1])
        self.TrajectoryVelocity2DImage.setXRange(np.min(self.parameters.VelocitiesTrajectory2D[:,:,0])-0.1*width,np.max(self.parameters.VelocitiesTrajectory2D[:,:,0])+0.1*width)
        self.TrajectoryVelocity2DImage.setYRange(np.min(self.parameters.VelocitiesTrajectory2D[:,:,1])-0.1*height,np.max(self.parameters.VelocitiesTrajectory2D[:,:,1])+0.1*height)

        self.TrajectoryVelocity2DImage.setBackground("w")

        self.TrajectoryVelocity2DImage.showGrid(x=True, y=True)
        self.TrajectoryVelocity2DImage.setLabel("left","v_y",color = 'black')
        self.TrajectoryVelocity2DImage.setLabel("bottom","v_x",color = 'black')
        self.TrajectoryVelocity2DImage.setTitle(MechanicsStrings.Velocity[f"{self.language}"],color = 'black')

    def initializeAccelerationImage2DTrajectory(self):
        """Updates the 2D Acceleration Trajectory Image"""

        self.TrajectoryAcceleration2DImageDynamic1 = self.TrajectoryAcceleration2DImage.plot(self.parameters.AccelerationsTrajectory2D[1:self.trajectory1DCounter,0,0],
                                         self.parameters.AccelerationsTrajectory2D[1:self.trajectory1DCounter,0,1], pen = self.pen1)
        self.TrajectoryAcceleration2DImageDynamic2 = self.TrajectoryAcceleration2DImage.plot(self.parameters.AccelerationsTrajectory2D[1:self.trajectory1DCounter,1,0],
                                         self.parameters.AccelerationsTrajectory2D[1:self.trajectory1DCounter,1,1], pen = self.pen2)

        self.TrajectoryAcceleration2DImageStatic1 = self.TrajectoryAcceleration2DImage.plot(self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,0,0],
                                         self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,0,1], pen = self.pen3)
        self.TrajectoryAcceleration2DImageStatic2 = self.TrajectoryAcceleration2DImage.plot(self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,1,0],
                                         self.parameters.AccelerationsTrajectory2D[1:self.parameters.trajectory2DEndValue,1,1], pen = self.pen4)

        self.TrajectoryAcceleration2DImageObject1 = self.TrajectoryAcceleration2DImage.plot([self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,0,0]],
                                                                        [self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,0,1]],
                                                                        symbol = "o",
                                                                        pen = self.pen1)
        self.TrajectoryAcceleration2DImageObject2 = self.TrajectoryAcceleration2DImage.plot([self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,1,0]],
                                                                        [self.parameters.AccelerationsTrajectory2D[self.trajectory2DCounter,1,1]],
                                                                        symbol = "o",
                                                                        pen = self.pen2)



        width = np.max(self.parameters.AccelerationsTrajectory2D[:,:,0])-np.min(self.parameters.AccelerationsTrajectory2D[:,:,0])
        height = np.max(self.parameters.AccelerationsTrajectory2D[:,:,1])-np.min(self.parameters.AccelerationsTrajectory2D[:,:,1])
        self.TrajectoryAcceleration2DImage.setXRange(np.min(self.parameters.AccelerationsTrajectory2D[:,:,0])-0.1*width,np.max(self.parameters.AccelerationsTrajectory2D[:,:,0])+0.1*width)
        self.TrajectoryAcceleration2DImage.setYRange(np.min(self.parameters.AccelerationsTrajectory2D[:,:,1])-0.1*height,np.max(self.parameters.AccelerationsTrajectory2D[:,:,1])+0.1*height)

        self.TrajectoryAcceleration2DImage.setBackground("w")

        self.TrajectoryAcceleration2DImage.showGrid(x=True, y=True)
        self.TrajectoryAcceleration2DImage.setLabel("left","a_y",color = 'black')
        self.TrajectoryAcceleration2DImage.setLabel("bottom","a_x",color = 'black')
        self.TrajectoryAcceleration2DImage.setTitle(MechanicsStrings.Acceleration[f"{self.language}"],color = 'black')


    def initializeImage3BodyProblem(self):
        """Updates the 3BodyProblem Trajectory Image"""
        colours = ["blue","red","orange","green"]
        self.pen13BP = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        self.pen23BP = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        for i in range(self.parameters.numberOfMass3BodyProblem):
            self.pen13BP[i] = pg.mkPen(colours[i],width = 5)
            self.pen23BP[i] = pg.mkPen(colours[i],width = 3, style=QtCore.Qt.DashLine)


        self.Trajectory3BodyProblemDynamic = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        self.Trajectory3BodyProblemStatic = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        self.Trajectory3BodyProblemObject = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)

        for i in range(self.parameters.numberOfMass3BodyProblem):
            self.Trajectory3BodyProblemStatic[i] = self.Trajectory3BodyProblemImage.plot(self.parameters.PositionsTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,0],
                                         self.parameters.PositionsTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,1], pen = self.pen23BP[i])
        for i in range(self.parameters.numberOfMass3BodyProblem):
            self.Trajectory3BodyProblemDynamic[i] = self.Trajectory3BodyProblemImage.plot(self.parameters.PositionsTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter,i,0],
                                         self.parameters.PositionsTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter,i,1], pen = self.pen13BP[i])
        for i in range(self.parameters.numberOfMass3BodyProblem):
            self.Trajectory3BodyProblemObject[i] = self.Trajectory3BodyProblemImage.plot([self.parameters.PositionsTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,0]],
                                                                        [self.parameters.PositionsTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,1]],
                                                                        symbol = "o",
                                                                        pen = self.pen13BP[i])

        self.Trajectory3BodyProblemImage.setBackground("w")
        width = np.max(self.parameters.PositionsTrajectory3BodyProblem[:,:,0])-np.min(self.parameters.PositionsTrajectory3BodyProblem[:,:,0])
        height = np.max(self.parameters.PositionsTrajectory3BodyProblem[:,:,1])-np.min(self.parameters.PositionsTrajectory3BodyProblem[:,:,1])
        self.Trajectory3BodyProblemImage.setXRange(np.min(self.parameters.PositionsTrajectory3BodyProblem[:,:,0])-0.1*width,np.max(self.parameters.PositionsTrajectory3BodyProblem[:,:,0])+0.1*width)
        self.Trajectory3BodyProblemImage.setYRange(np.min(self.parameters.PositionsTrajectory3BodyProblem[:,:,1])-0.1*height,np.max(self.parameters.PositionsTrajectory3BodyProblem[:,:,1])+0.1*height)

        self.Trajectory3BodyProblemImage.showGrid(x=True,y=True)
        self.Trajectory3BodyProblemImage.setLabel("bottom","x",color = 'black')
        self.Trajectory3BodyProblemImage.setLabel("left","y",color = 'black')
        self.Trajectory3BodyProblemImage.setTitle(MechanicsStrings.trajectory1D[f"{self.language}"],color = 'black')

    def initializeAccelerationImage3BodyProblem(self):
        """Updates the 3BodyProblem Acceleration Image"""
        self.TrajectoryAcceleration3BodyProblemDynamic = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        self.TrajectoryAcceleration3BodyProblemStatic = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        self.TrajectoryAcceleration3BodyProblemObject = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)

        for i in range(self.parameters.numberOfMass3BodyProblem):
            self.TrajectoryAcceleration3BodyProblemDynamic[i] = self.TrajectoryAcceleration3BodyProblem.plot(self.parameters.AccelerationsTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter,i,0],
                                         self.parameters.AccelerationsTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter,i,1], pen = self.pen13BP[i])
            self.TrajectoryAcceleration3BodyProblemStatic[i] = self.TrajectoryAcceleration3BodyProblem.plot(self.parameters.AccelerationsTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,0],
                                         self.parameters.AccelerationsTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,1], pen = self.pen23BP[i])
            self.TrajectoryAcceleration3BodyProblemObject[i] = self.TrajectoryAcceleration3BodyProblem.plot([self.parameters.AccelerationsTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,0]],
                                                                        [self.parameters.AccelerationsTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,1]],
                                                                        symbol = "o",
                                                                        pen = self.pen13BP[i])

        self.TrajectoryAcceleration3BodyProblem.setBackground("w")
        width = np.max(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,0])-np.min(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,0])
        height = np.max(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,1])-np.min(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,1])
        self.TrajectoryAcceleration3BodyProblem.setXRange(np.min(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,0])-0.1*width,np.max(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,0])+0.1*width)
        self.TrajectoryAcceleration3BodyProblem.setYRange(np.min(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,1])-0.1*height,np.max(self.parameters.AccelerationsTrajectory3BodyProblem[:,:,1])+0.1*height)

        self.TrajectoryAcceleration3BodyProblem.showGrid(x=True,y=True)
        self.TrajectoryAcceleration3BodyProblem.setLabel("bottom","a_x",color = 'black')
        self.TrajectoryAcceleration3BodyProblem.setLabel("left","a_y",color = 'black')
        self.TrajectoryAcceleration3BodyProblem.setTitle(MechanicsStrings.Acceleration[f"{self.language}"],color = 'black')

    def initializeVelocityImage3BodyProblem(self):
        """Updates the 3BodyProblem Velocity Image"""
        self.TrajectoryVelocity3BodyProblemDynamic = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        self.TrajectoryVelocity3BodyProblemStatic = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)
        self.TrajectoryVelocity3BodyProblemObject = np.zeros(self.parameters.numberOfMass3BodyProblem, dtype = object)

        for i in range(self.parameters.numberOfMass3BodyProblem):
            self.TrajectoryVelocity3BodyProblemDynamic[i] = self.TrajectoryVelocity3BodyProblem.plot(self.parameters.VelocitiesTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter,i,0],
                                         self.parameters.VelocitiesTrajectory3BodyProblem[:self.trajectory3BodyProblemCounter,i,1], pen = self.pen13BP[i])
            self.TrajectoryVelocity3BodyProblemStatic[i] = self.TrajectoryVelocity3BodyProblem.plot(self.parameters.VelocitiesTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,0],
                                         self.parameters.VelocitiesTrajectory3BodyProblem[:self.parameters.trajectory3BodyProblemEndValue,i,1], pen = self.pen23BP[i])
            self.TrajectoryVelocity3BodyProblemObject[i] = self.TrajectoryVelocity3BodyProblem.plot([self.parameters.VelocitiesTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,0]],
                                                                        [self.parameters.VelocitiesTrajectory3BodyProblem[self.trajectory3BodyProblemCounter,i,1]],
                                                                        symbol = "o",
                                                                        pen = self.pen13BP[i])

        self.TrajectoryVelocity3BodyProblem.setBackground("w")
        width = np.max(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,0])-np.min(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,0])
        height = np.max(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,1])-np.min(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,1])
        self.TrajectoryVelocity3BodyProblem.setXRange(np.min(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,0])-0.1*width,np.max(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,0])+0.1*width)
        self.TrajectoryVelocity3BodyProblem.setYRange(np.min(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,1])-0.1*height,np.max(self.parameters.VelocitiesTrajectory3BodyProblem[:,:,1])+0.1*height)

        self.TrajectoryVelocity3BodyProblem.showGrid(x=True,y=True)
        self.TrajectoryVelocity3BodyProblem.setLabel("bottom","v_x",color = 'black')
        self.TrajectoryVelocity3BodyProblem.setLabel("left","v_y",color = 'black')
        self.TrajectoryVelocity3BodyProblem.setTitle(MechanicsStrings.Velocity[f"{self.language}"],color = 'black')


################################
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
    window=MechanicsWindow()
    window.show()
    sys.exit(app.exec_())