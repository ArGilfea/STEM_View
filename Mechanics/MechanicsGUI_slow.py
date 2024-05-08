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
        ### Exit
        self._createExitButton() 

        self.generalLayout1DTrajectory.setColumnStretch(1,5)
        self.generalLayout1DTrajectory.setColumnStretch(2,5)

################################
    def _createTrajectory1DImage(self):
        """Creates the Image for the Position of the 1D Trajectory"""
        self.Trajectory1DImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.trajectory1DCounter = 0
        self.Trajectory1DImage_cid = self.Trajectory1DImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.Trajectory1DImage))
        self.Trajectory1DImage_cod = self.Trajectory1DImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.Trajectory1DImage))
        self.generalLayout1DTrajectory.addWidget(self.Trajectory1DImage,self.current_line1DTrajectory,1)
        self.updateImage1DTrajectory()

        self.trajectory1DTimer = QtCore.QTimer()
        self.trajectory1DTimer.setInterval(self.parameters.dynamicSpeed1DTrajectory)
        self.trajectory1DTimer.timeout.connect(self.updateImages1DTrajectory)
        if self.parameters.toggleDynamic1DTrajectory:
            self.trajectory1DTimer.start()

    def _createVelocityTrajectory1DImage(self):
        """Creates the Image for the Velocity of the 1D Trajectory"""
        self.TrajectoryVelocity1DImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.TrajectoryVelocity1DImage_cid = self.TrajectoryVelocity1DImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.TrajectoryVelocity1DImage))
        self.TrajectoryVelocity1DImage_cod = self.TrajectoryVelocity1DImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.TrajectoryVelocity1DImage))
        self.generalLayout1DTrajectory.addWidget(self.TrajectoryVelocity1DImage,self.current_line1DTrajectory,2)
        self.updateVelocityImage1DTrajectory()

        self.current_line1DTrajectory += 1

    def _createAccelerationTrajectory1DImage(self):
        """Creates the Image for the Acceleration of the 1D Trajectory"""
        self.TrajectoryAcceleration1DImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.TrajectoryAcceleration1DImage_cid = self.TrajectoryAcceleration1DImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.TrajectoryAcceleration1DImage))
        self.TrajectoryAcceleration1DImage_cod = self.TrajectoryAcceleration1DImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.TrajectoryAcceleration1DImage))
        self.generalLayout1DTrajectory.addWidget(self.TrajectoryAcceleration1DImage,self.current_line1DTrajectory,1)
        self.updateAccelerationImage1DTrajectory()

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
            self.trajectory1DTimer.start()
        else:
            self.parameters.toggleDynamic1DTrajectory = False
            self.trajectory1DTimer.stop()
        self.updateImage1DTrajectory()

    def updateCheckBoxStatic1DTrajectory(self):
        """Updates the Static CheckBox for the 1D Trajectory"""
        if self.Static1DTrajectoryCheckBox.isChecked():
            self.parameters.toggleStatic1DTrajectory = True
        else:
            self.parameters.toggleStatic1DTrajectory = False
        self.updateImage1DTrajectory()

    def update1DTrajectoryDynamicSpeed(self):
        """Updates the speed of the video"""
        self.parameters.dynamicSpeed1DTrajectory = int(self.DynamicSpeed1DTrajectoryLineEdit.text())
        self.trajectory1DTimer.setInterval(self.parameters.dynamicSpeed1DTrajectory)

    def update1DTrajectoryInitCond(self):
        """Update the 1D Trajectory initial parameters. Also resets the video"""
        for i in range(2):
            self.parameters.initialPosition1D[i] = float(self.Position1DTrajectoryLineEdit[i].text())
            self.parameters.initialVelocity1D[i] = float(self.Velocity1DTrajectoryLineEdit[i].text())
            self.parameters.initialAcceleration1D[i] = float(self.Acceleration1DTrajectoryLineEdit[i].text())
        self.updateCurve1DTrajectory()

    def updateCurve1DTrajectory(self):
        """Updates the curve. Also resets the video"""
        self.trajectory1DCounter = 0
        self.parameters.trajectory1D, self.parameters.Velocitiestrajectory1D, self.parameters.trajectory1DEndValue = Mechanics1D.MechanicsTrajectory1D(self.parameters.initialPosition1D,
                                                                self.parameters.initialVelocity1D,self.parameters.initialAcceleration1D,
                                                                timeScale=self.parameters.timeScale1D, toggleGround= self.parameters.toggleGround1D)
        self.updateImages1DTrajectory()

################################
    def updateImages1DTrajectory(self):
        """Updates all the 1D Trajectory Images"""
        self.updateVelocityImage1DTrajectory()
        self.updateAccelerationImage1DTrajectory()
        self.updateImage1DTrajectory()

    def updateVelocityImage1DTrajectory(self):
        """Updates the 1D Velocity Trajectory Image"""
        try:
            self.TrajectoryVelocity1DImage.axes.cla()
        except:
            pass

        if self.parameters.toggleDynamic1DTrajectory:
            self.TrajectoryVelocity1DImage.axes.plot(self.parameters.Velocitiestrajectory1D[:self.trajectory1DCounter,0],
                                         self.parameters.Velocitiestrajectory1D[:self.trajectory1DCounter,1],
                                         color = 'blue', linewidth = 3.5)
        if self.parameters.toggleStatic1DTrajectory:
            self.TrajectoryVelocity1DImage.axes.plot(self.parameters.Velocitiestrajectory1D[:self.parameters.trajectory1DEndValue+1,0],
                                         self.parameters.Velocitiestrajectory1D[:self.parameters.trajectory1DEndValue+1,1],
                                         linestyle = "--", color = 'orange', linewidth = 1.8)


        width = np.max(self.parameters.Velocitiestrajectory1D[:,0])-np.min(self.parameters.Velocitiestrajectory1D[:,0])
        height = np.max(self.parameters.Velocitiestrajectory1D[:,1])-np.min(self.parameters.Velocitiestrajectory1D[:,1])
        self.TrajectoryVelocity1DImage.axes.set_xlim(np.min(self.parameters.Velocitiestrajectory1D[:,0])-0.1*width,np.max(self.parameters.Velocitiestrajectory1D[:,0])+0.1*width)
        self.TrajectoryVelocity1DImage.axes.set_ylim(np.min(self.parameters.Velocitiestrajectory1D[:,1])-0.1*height,np.max(self.parameters.Velocitiestrajectory1D[:,1])+0.1*height)


        self.TrajectoryVelocity1DImage.axes.grid()
        self.TrajectoryVelocity1DImage.axes.set_xlabel("v_x")
        self.TrajectoryVelocity1DImage.axes.set_ylabel("v_y")
        self.TrajectoryVelocity1DImage.axes.set_title(MechanicsStrings.Acceleration[f"{self.language}"])

        self.TrajectoryVelocity1DImage.draw()

    def updateAccelerationImage1DTrajectory(self):
        """Updates the 1D Velocity Trajectory Image"""
        try:
            self.TrajectoryAcceleration1DImage.axes.cla()
        except:
            pass

        self.TrajectoryAcceleration1DImage.axes.plot(self.parameters.initialAcceleration1D[0],
                                                     self.parameters.initialAcceleration1D[1],
                                                     marker = '*')

        self.TrajectoryAcceleration1DImage.axes.grid()
        self.TrajectoryAcceleration1DImage.axes.set_xlabel("a_x")
        self.TrajectoryAcceleration1DImage.axes.set_ylabel("a_y")
        self.TrajectoryAcceleration1DImage.axes.set_title(MechanicsStrings.Acceleration[f"{self.language}"])

        self.TrajectoryAcceleration1DImage.draw()

    def updateImage1DTrajectory(self):
        """Updates the 1D Trajectory Image"""
        try:
            self.Trajectory1DImage.axes.cla()
        except:
            pass
        if self.parameters.toggleDynamic1DTrajectory:
            self.Trajectory1DImage.axes.plot(self.parameters.trajectory1D[:self.trajectory1DCounter,0],
                                         self.parameters.trajectory1D[:self.trajectory1DCounter,1],
                                         color = 'blue', linewidth = 3.5)
        if self.parameters.toggleStatic1DTrajectory:
            self.Trajectory1DImage.axes.plot(self.parameters.trajectory1D[:self.parameters.trajectory1DEndValue+1,0],
                                         self.parameters.trajectory1D[:self.parameters.trajectory1DEndValue+1,1],
                                         linestyle = "--", color = 'orange', linewidth = 1.8)
        if self.parameters.toggleGround1D:
            self.Trajectory1DImage.axes.axhline(0, color = 'red',alpha = 0.1)

        width = np.max(self.parameters.trajectory1D[:,0])-np.min(self.parameters.trajectory1D[:,0])
        height = np.max(self.parameters.trajectory1D[:,1])-np.min(self.parameters.trajectory1D[:,1])
        self.Trajectory1DImage.axes.set_xlim(np.min(self.parameters.trajectory1D[:,0])-0.1*width,np.max(self.parameters.trajectory1D[:,0])+0.1*width)
        self.Trajectory1DImage.axes.set_ylim(np.min(self.parameters.trajectory1D[:,1])-0.1*height,np.max(self.parameters.trajectory1D[:,1])+0.1*height)

        self.Trajectory1DImage.axes.grid()
        self.Trajectory1DImage.axes.set_xlabel("x")
        self.Trajectory1DImage.axes.set_ylabel("y")
        self.Trajectory1DImage.axes.set_title(MechanicsStrings.trajectory1D[f"{self.language}"])

        self.Trajectory1DImage.draw()
        if self.trajectory1DCounter <= self.parameters.trajectory1DEndValue:
            self.trajectory1DCounter +=1
        else:
            self.trajectory1DCounter = 0
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
    window=MechanicsWindow()
    window.show()
    sys.exit(app.exec())