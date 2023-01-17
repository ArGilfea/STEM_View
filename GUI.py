import os
import time

###
import numpy as np
import time
###
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from functools import partial
###
import GUIParameters
import PhotonBeams
###
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
###
import markdown

size_Image = 200

class Window(QMainWindow):
    """
    Main window of the GUI.
    """    
    def __init__(self):
        """Initializes the GUI Window"""
        self.parameters = GUIParameters.GUIParameters()

        self.tabs = QTabWidget()
        self.BUTTON_SIZE = 40
        self.DISPLAY_HEIGHT = 35
        self.current_linePBA = 1
        super().__init__(parent=None)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("My GUI")
        self.generalLayoutPBA = QGridLayout()
        self.generalLayoutTBA1 = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()
        centralWidgetPBA = QWidget(self)
        centralWidgetTBA1 = QWidget(self)
        centralWidgetReadMe = QWidget(self)
        centralWidgetPBA.setLayout(self.generalLayoutPBA)
        centralWidgetTBA1.setLayout(self.generalLayoutTBA1)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)
        self.tabs.addTab(centralWidgetPBA,"Photon Beam Attenuation")
        self.tabs.addTab(centralWidgetTBA1,"TBA")
        self.tabs.addTab(centralWidgetReadMe,"Read Me")

        self.setCentralWidget(self.tabs)
        self.setWindowTitle("PhyMedGUI")

        self._addSpecterImagePBA()
        self._addMaterialTypePBA()
        self._addDepthSliderPBA()

        self._createExitButton() 

        self._createReadMe()

        self.generalLayoutPBA.setColumnStretch(1,5)
        #self.generalLayoutPBA.setRowStretch(1,50)
        self.generalLayoutPBA.setColumnStretch(2,1)
        self.generalLayoutPBA.setColumnStretch(3,1)
    
    def _addSpecterImagePBA(self):
        """Adds the central image socket for Photon Beam Attenuation showing the Specter"""
        self.PBASpecter = MplCanvas(self, width=5, height=5, dpi=75)
        self.generalLayoutPBA.addWidget(self.PBASpecter,self.current_linePBA,1)

        self.updateImagePBA()

    def _addMaterialTypePBA(self):
        """Adds a Combo Box to determine the material for attenuation"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.PBAMaterialType = QComboBox()
        self.PBAMaterialType.addItem("None")
        self.PBAMaterialType.addItem("Al")
        self.PBAMaterialType.addItem("Pb")
        self.PBAMaterialType.addItem("Zn")

        self.PBASpecterType = QComboBox()
        self.PBASpecterType.addItem("Bump")
        self.PBASpecterType.addItem("Peak")
        self.PBASpecterType.addItem("Flat")
        self.PBASpecterType.addItem("Exponential")

        self.PBAMinLineEdit = QLineEdit()
        self.PBAMaxLineEdit = QLineEdit()
        self.PBAMinLineEdit.setFixedWidth(90)
        self.PBAMaxLineEdit.setFixedWidth(90)
        self.PBAMinLineEdit.setText(f"{self.parameters.SpecterMin}")
        self.PBAMaxLineEdit.setText(f"{self.parameters.SpecterMax}")

        self.PBAInitValue = QLineEdit()
        self.PBAKFactor = QLineEdit()
        self.PBAInitValue.setFixedWidth(90)
        self.PBAKFactor.setFixedWidth(90)
        self.PBAInitValue.setText(f"{self.parameters.SpecterInitialValue}")
        self.PBAKFactor.setText(f"{self.parameters.SpecterKFactor}")

        self.PBANormalizeBox = QCheckBox()
        self.PBASuperposeBox = QCheckBox()

        self.PBAAvgBox = QCheckBox()

        self.PBASaveButton = QPushButton("Save")
        self.PBAClearButton = QPushButton("Clear")
        self.PBAShowBox = QCheckBox()

        self.PBAMaterialType.activated[str].connect(self.update_Combo_MaterialPBA)
        self.PBASpecterType.activated[str].connect(self.update_Combo_SpecterPBA)

        self.PBAMinLineEdit.editingFinished.connect(self.updateMinMaxSpecter)
        self.PBAMaxLineEdit.editingFinished.connect(self.updateMinMaxSpecter)

        self.PBAInitValue.editingFinished.connect(self.updateInitKSpecter)
        self.PBAKFactor.editingFinished.connect(self.updateInitKSpecter)

        self.PBANormalizeBox.stateChanged.connect(self.updateCheckNormalizeBox)
        self.PBASuperposeBox.stateChanged.connect(self.updateCheckSuperposeBox)

        self.PBAAvgBox.stateChanged.connect(self.updateCheckAvgBox)

        self.PBASaveButton.clicked.connect(self.saveSavedSpecterPBA)
        self.PBAClearButton.clicked.connect(self.clearSavedSpecterPBA)
        self.PBAShowBox.stateChanged.connect(self.updateShowSavedSpecterPBA)

        layout.addWidget(self.PBAMaterialType,0,0)
        layout.addWidget(self.PBASpecterType,0,2)

        layout.addWidget(QLabel("Min."),1,0)
        layout.addWidget(self.PBAMinLineEdit,1,1)
        layout.addWidget(QLabel("Max."),1,2)
        layout.addWidget(self.PBAMaxLineEdit,1,3)

        layout.addWidget(QLabel("In. Value"),2,0)
        layout.addWidget(self.PBAInitValue,2,1)
        layout.addWidget(QLabel("Factor."),2,2)
        layout.addWidget(self.PBAKFactor,2,3)

        layout.addWidget(QLabel("Norm."),3,0)
        layout.addWidget(self.PBANormalizeBox,3,1)
        layout.addWidget(QLabel("Sup."),3,2)
        layout.addWidget(self.PBASuperposeBox,3,3)

        layout.addWidget(QLabel("Avg."),4,0)
        layout.addWidget(self.PBAAvgBox,4,1)

        layout.addWidget(self.PBASaveButton,5,0)
        layout.addWidget(self.PBAClearButton,5,1)
        layout.addWidget(QLabel("Show"),5,2)
        layout.addWidget(self.PBAShowBox,5,3)

        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,1)
        layout.setColumnStretch(2,1)
        layout.setColumnStretch(3,1)

        self.generalLayoutPBA.addWidget(subWidget,self.current_linePBA,2)
        self.current_linePBA += 1
        

    def _addDepthSliderPBA(self):
        """Adds the slider for the depth of the material in the attenuation"""
        subWidget = QWidget()
        layout = QHBoxLayout()
        subWidget.setLayout(layout)

        sizeText = 30

        self.sliderDepthPBA = QSlider(Qt.Horizontal)
        self.lineEditDepthPBA = QLineEdit()
        empty = QLineEdit()

        empty.setFixedWidth(sizeText)
        self.lineEditDepthPBA.setFixedWidth(sizeText)
        self.lineEditDepthPBA.setText("0")

        self.sliderDepthPBA.setMaximum(10000)
        self.sliderDepthPBA.setTickPosition(QSlider.TicksBothSides)
        self.sliderDepthPBA.setSingleStep(1000)
        self.sliderDepthPBA.setTickInterval(1000)

        self.lineEditDepthPBA.editingFinished.connect(self.updateLineEditDepthPBA)
        self.sliderDepthPBA.valueChanged.connect(self.updateSliderDepthPBA)

        layout.addWidget(self.sliderDepthPBA)
        layout.addWidget(self.lineEditDepthPBA)
        layout.addWidget(empty)

        self.generalLayoutPBA.addWidget(subWidget,self.current_linePBA,1)

    def _createExitButton(self):
        """Create an exit button"""
        self.exit = QPushButton("Exit")
        self.exit.setToolTip("Closes the GUI and its dependencies")
        self.exit.clicked.connect(self.closing_button)
        self.generalLayoutPBA.addWidget(self.exit,self.current_linePBA+1,3)  
        self.current_linePBA += 2

    def _createReadMe(self):
        """Creates a ReadMe tab with the ReadMe file infos"""
        self.ReadMeText = QTextEdit()
        self.ReadMeText.setReadOnly(True)
        f = open('ReadMe.md', 'r')
        htmlmarkdown = markdown.markdown( f.read() )
        self.ReadMeText.setText(htmlmarkdown)
        self.generalLayoutReadMe.addWidget(self.ReadMeText)

    def closing_button(self):
        try:
            self.generalLayout.removeWidget(self.GraphRunPlot)
            self.generalLayout.removeWidget(self.GraphTracePlot)
            self.generalLayout.removeWidget(self.GraphCornerPlot)
            self.GraphRunPlot.deleteLater()
            self.GraphTracePlot.deleteLater()
            self.GraphCornerPlot.deleteLater()
            self.GraphRunPlot = None
            self.GraphTracePlot = None
            self.GraphCornerPlot = None
            del self.GraphRunPlot
            del self.GraphTracePlot
            del self.GraphCornerPlot
        except: pass
        self.close()

    def updateImagePBA(self):
        """Updates the Image of the attenuation of the Photon Beam"""
        if self.parameters.ShowSavedPBA:
            self.updateImagePBASaved()
        else:
            self.updateImagePBANormal()

    def updateImagePBASaved(self):
        """Updates the Image with the Saved Specters"""
        try:
            self.PBASpecter.axes.cla()
        except:
            pass
        for i in range(len(self.parameters.SavedSpectersLabel)):
            self.PBASpecter.axes.plot(self.parameters.SavedSpectersE[i],self.parameters.SavedSpectersF[i],label = self.parameters.SavedSpectersLabel[i])
        self.baseImagePBA()
        self.PBASpecter.draw() 

    def updateImagePBANormal(self):
        """Updates the Image with the beam and attenuation"""
        try:
            self.PBASpecter.axes.cla()
        except:
            pass
        if self.parameters.MaterialTypePBA != "None":
            through = PhotonBeams.BeerLambert(self.parameters.Specter,
                                            self.parameters.depthPBA,mu_rho = self.parameters.XCOMData,rho = self.parameters.rho[f"{self.parameters.MaterialTypePBA}"])
        else:
            through = self.parameters.SpecterfValues
        if self.parameters.ShowBaseSpecterPBA:
            basic = self.parameters.SpecterfValues
        if self.parameters.NormalizePBA:
            through = through/np.sum(through)
            try:
                basic = basic/np.sum(basic)
            except:
                pass
        self.PBASpecter.axes.plot(self.parameters.SpecterEValues,through,label = "Attenuated")
        self.throughPBA = through
        if self.parameters.ShowBaseSpecterPBA:
            self.PBASpecter.axes.plot(self.parameters.SpecterEValues,basic,label="Base")
            if self.parameters.MeanEPBA:
                self.PBASpecter.axes.axvline(PhotonBeams.AverageE(self.parameters.Specter))
        if self.parameters.MeanEPBA:
            Specter_tmp = np.zeros((self.parameters.SpecterfValues.shape[0],2))
            Specter_tmp[:,0] = self.parameters.SpecterEValues
            Specter_tmp[:,1] = through
            self.PBASpecter.axes.axvline(PhotonBeams.AverageE(Specter_tmp),color = 'r')
        self.baseImagePBA()
        self.PBASpecter.draw() 


    def baseImagePBA(self):
        self.PBASpecter.axes.grid()
        if self.parameters.ShowBaseSpecterPBA or self.parameters.ShowSavedPBA:
            self.PBASpecter.axes.legend()
        self.PBASpecter.axes.set_xlabel("Energy (MeV)")
        if self.parameters.NormalizePBA and not self.parameters.ShowSavedPBA:
            self.PBASpecter.axes.set_ylabel("Frequency")
        else:
            self.PBASpecter.axes.set_ylabel("Distribution")
        if self.parameters.MaterialTypePBA == "None":
            if self.parameters.NormalizePBA:
                self.PBASpecter.axes.set_title(f"Normalized {self.parameters.SpecterTypePBA} spectrum")
            else:
                self.PBASpecter.axes.set_title(f"{self.parameters.SpecterTypePBA} spectrum")
        else:
            if self.parameters.NormalizePBA:
                self.PBASpecter.axes.set_title(f"Normalized attenuation of the {self.parameters.SpecterTypePBA} spectrum\n through {self.parameters.depthPBA} cm of {self.parameters.MaterialTypePBA}")
            else:
                self.PBASpecter.axes.set_title(f"Attenuation of the {self.parameters.SpecterTypePBA} spectrum\n through {self.parameters.depthPBA} cm of {self.parameters.MaterialTypePBA}")
        if self.parameters.ShowSavedPBA:
            self.PBASpecter.axes.set_title(f"Attenuated Spectrum")
    def update_Combo_MaterialPBA(self):
        """Updates the Combo of the Material of the PBA"""
        self.parameters.MaterialTypePBA = self.PBAMaterialType.currentText()

        if self.parameters.MaterialTypePBA != "None":
            self.parameters.XCOMData = np.loadtxt(f"XCOM_Data/XCOM_{self.parameters.MaterialTypePBA}.pl")

        self.updateImagePBA()

    def update_Combo_SpecterPBA(self):
        """Updates the Combo of the Spectrum of the PBA"""
        self.parameters.SpecterTypePBA = self.PBASpecterType.currentText()
        if self.parameters.SpecterTypePBA in ["Bump"]:
            self.parameters.Specter = np.loadtxt("Specters/"+self.parameters.SpecterTypePBA+".txt")
            self.parameters.SpecterEValues = self.parameters.Specter[:,0]
            self.parameters.SpecterfValues = self.parameters.Specter[:,1]
        elif self.parameters.SpecterTypePBA == "Peak":
            self.parameters.SpecterEValues = np.arange(self.parameters.SpecterMin-0.1,self.parameters.SpecterMin+0.1,0.001)
            self.parameters.SpecterfValues = np.zeros_like(self.parameters.SpecterEValues)
            self.parameters.SpecterfValues[int(self.parameters.SpecterfValues.shape[0]/2)] = 1
            self.parameters.Specter = np.zeros((self.parameters.SpecterfValues.shape[0],2))
            self.parameters.Specter[:,0] = self.parameters.SpecterEValues
            self.parameters.Specter[:,1] = self.parameters.SpecterfValues
        elif self.parameters.SpecterTypePBA == "Flat":
            self.parameters.SpecterEValues = np.linspace(self.parameters.SpecterMin-0.1,self.parameters.SpecterMax+0.1,100)
            self.parameters.SpecterfValues = np.zeros_like(self.parameters.SpecterEValues)
            self.parameters.Specter = np.zeros((self.parameters.SpecterfValues.shape[0],2))
            for i in range(self.parameters.SpecterfValues.shape[0]):
                if self.parameters.SpecterEValues[i] > self.parameters.SpecterMin and self.parameters.SpecterEValues[i] < self.parameters.SpecterMax:
                    self.parameters.SpecterfValues[i] = self.parameters.SpecterInitialValue
            self.parameters.Specter[:,0] = self.parameters.SpecterEValues
            self.parameters.Specter[:,1] = self.parameters.SpecterfValues
        elif self.parameters.SpecterTypePBA == "Exponential":
            self.parameters.SpecterEValues = np.linspace(self.parameters.SpecterMin-0.1,self.parameters.SpecterMax+0.1,100)
            self.parameters.SpecterfValues = np.zeros_like(self.parameters.SpecterEValues)
            self.parameters.Specter = np.zeros((self.parameters.SpecterfValues.shape[0],2))
            for i in range(self.parameters.SpecterfValues.shape[0]):
                if self.parameters.SpecterEValues[i] > self.parameters.SpecterMin and self.parameters.SpecterEValues[i] < self.parameters.SpecterMax:
                    self.parameters.SpecterfValues[i] = self.parameters.SpecterInitialValue*np.exp(self.parameters.SpecterKFactor*(self.parameters.SpecterEValues[i] - self.parameters.SpecterMin))
            self.parameters.Specter[:,0] = self.parameters.SpecterEValues
            self.parameters.Specter[:,1] = self.parameters.SpecterfValues
        self.updateImagePBA()

    def updateCheckNormalizeBox(self):
        """Updates the Check Box of Normalize"""
        if self.PBANormalizeBox.isChecked() == True:
            self.parameters.NormalizePBA = True
        else:
            self.parameters.NormalizePBA = False
        self.updateImagePBA()

    def updateCheckSuperposeBox(self):
        """Updates the Check Box of Normalize"""
        if self.PBASuperposeBox.isChecked() == True:
            self.parameters.ShowBaseSpecterPBA = True
        else:
            self.parameters.ShowBaseSpecterPBA = False
        self.updateImagePBA()

    def updateCheckAvgBox(self):
        """Updates the Check Box of Average"""
        if self.PBAAvgBox.isChecked() == True:
            self.parameters.MeanEPBA = True
        else:
            self.parameters.MeanEPBA = False
        self.updateImagePBA()

    def updateMinMaxSpecter(self):
        """Updates the min and max values of the specter"""
        try:
            self.parameters.SpecterMin = float(self.PBAMinLineEdit.text())
        except: pass
        try:
            self.parameters.SpecterMax = float(self.PBAMaxLineEdit.text())
        except: pass
        self.update_Combo_SpecterPBA()

    def updateInitKSpecter(self):
        """Updates the Initial and k Factor values of the specter"""
        try:
            self.parameters.SpecterInitialValue = float(self.PBAInitValue.text())
        except: pass
        try:
            self.parameters.SpecterKFactor = float(self.PBAKFactor.text())
        except: pass
        self.update_Combo_SpecterPBA()

    def updateLineEditDepthPBA(self):
        """Updates the Depth of attenuation based on the Line Edit"""
        try:
            self.parameters.depthPBA = float(self.lineEditDepthPBA.text())
        except:
            self.parameters.depthPBA = 0
        self.updateImagePBA()

    def updateSliderDepthPBA(self):
        """Updates the Depth of attenuation based on the Slider"""
        try:
            self.parameters.depthPBA = self.sliderDepthPBA.value()/1000
        except:
            self.parameters.depthPBA = 0
        self.updateImagePBA()

    def clearSavedSpecterPBA(self):
        """Clears the Saved Specters"""
        self.parameters.SavedSpectersE = []
        self.parameters.SavedSpectersF = []
        self.parameters.SavedSpectersLabel = []

    def saveSavedSpecterPBA(self):
        """Saves the current Specter"""
        self.parameters.SavedSpectersE.append(self.parameters.SpecterEValues)
        self.parameters.SavedSpectersF.append(self.throughPBA)
        self.parameters.SavedSpectersLabel.append(f"{self.parameters.MaterialTypePBA}: {self.parameters.depthPBA} cm")

    def updateShowSavedSpecterPBA(self):
        """Toggles the view to see the Saved Specters"""
        if self.PBAShowBox.isChecked():
            self.parameters.ShowSavedPBA = True
        else: 
            self.parameters.ShowSavedPBA = False
        self.updateImagePBA()



class MplCanvas(FigureCanvasQTAgg):
    """Class for the images and the graphs as a widget"""
    def __init__(self, parent=None, width:float=5, height:float=4, dpi:int=75):
        """Creates an empty figure with axes and fig as parameters"""
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.fig = fig
        super(MplCanvas, self).__init__(fig)

###
if __name__ == "__main__":
    os.system('clear')
    print(f"Starting program at {time.strftime('%H:%M:%S')}")
    initial = time.time()
    app = QApplication([])
    window=Window()
    window.show()
    sys.exit(app.exec())