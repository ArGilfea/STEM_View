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
try:
    import GUIParameters as GUIParameters
    import PhotonBeams as PhotonBeams
except:
    import MedPhys.GUIParameters as GUIParameters
    import MedPhys.PhotonBeams as PhotonBeams
###
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
###
import markdown

size_Image = 200

class MedPhysWindow(QMainWindow):
    """
    Main window of the GUI.
    """    
    def __init__(self,parent=None):
        """Initializes the GUI Window"""
        self.parameters = GUIParameters.GUIParameters()

        self.tabs = QTabWidget()
        self.BUTTON_SIZE = 40
        self.DISPLAY_HEIGHT = 35
        self.current_linePBA = 1
        super().__init__(parent=parent)
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
        self._addXCOMDataImagePBA()
        self._addDataImageAttenuationPBA()

        self._createExitButton() 

        self._createReadMe()

        self.generalLayoutPBA.setColumnStretch(1,5)
        #self.generalLayoutPBA.setRowStretch(1,50)
        self.generalLayoutPBA.setColumnStretch(2,1)
        self.generalLayoutPBA.setColumnStretch(3,1)
    
    def _addSpecterImagePBA(self):
        """Adds the central image socket for Photon Beam Attenuation showing the Specter"""
        self.PBASpecter = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutPBA.addWidget(self.PBASpecter,self.current_linePBA,1)

        self.updateImagePBA()

    def _addXCOMDataImagePBA(self):
        """Adds the image of the XCOM Data"""
        self.PBAXCOMData = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutPBA.addWidget(self.PBAXCOMData,self.current_linePBA,1)

        self.updateImagePBA()
        self.updateXCOMImagePBA()

    def _addDataImageAttenuationPBA(self):
        """Adds the image of the total attenuation"""
        self.PBAAttenuation = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutPBA.addWidget(self.PBAAttenuation,self.current_linePBA,2)
        self.current_linePBA += 1

        self.updateAttenuationImagePBA()

    def _addMaterialTypePBA(self):
        """Adds a Combo Box to determine the material for attenuation"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.PBAMaterialType = QComboBox()
        self.PBAMaterialType.addItem("None")
        self.PBAMaterialType.addItem("Al")
        self.PBAMaterialType.addItem("Cu")
        self.PBAMaterialType.addItem("H")
        self.PBAMaterialType.addItem("H2O")
        self.PBAMaterialType.addItem("I")
        self.PBAMaterialType.addItem("O")
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

        self.PBAMaxDepthValue = QLineEdit()
        self.PBAMaxDepthValue.setText(f"{self.parameters.maxDepthPBA}")

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

        self.PBAMaxDepthValue.editingFinished.connect(self.updateMaxDepth)

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
        layout.addWidget(QLabel("Factor"),2,2)
        layout.addWidget(self.PBAKFactor,2,3)

        layout.addWidget(QLabel("Max Depth"),3,0)
        layout.addWidget(self.PBAMaxDepthValue,3,1)

        layout.addWidget(QLabel("Norm."),4,0)
        layout.addWidget(self.PBANormalizeBox,4,1)
        layout.addWidget(QLabel("Sup."),4,2)
        layout.addWidget(self.PBASuperposeBox,4,3)

        layout.addWidget(QLabel("Avg."),5,0)
        layout.addWidget(self.PBAAvgBox,5,1)

        layout.addWidget(self.PBASaveButton,6,0)
        layout.addWidget(self.PBAClearButton,6,1)
        layout.addWidget(QLabel("Show"),6,2)
        layout.addWidget(self.PBAShowBox,6,3)

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

        self.lineEditDepthPBA.setFixedWidth(sizeText)
        self.lineEditDepthPBA.setText("0")

        self.sliderDepthPBA.setMaximum(int(self.parameters.maxDepthPBA * 1000))
        self.sliderDepthPBA.setTickPosition(QSlider.TicksBothSides)
        self.sliderDepthPBA.setSingleStep(1000)
        self.sliderDepthPBA.setTickInterval(1000)

        self.lineEditDepthPBA.editingFinished.connect(self.updateLineEditDepthPBA)
        self.sliderDepthPBA.valueChanged.connect(self.updateSliderDepthPBA)

        layout.addWidget(self.sliderDepthPBA)
        layout.addWidget(self.lineEditDepthPBA)

        self.generalLayoutPBA.addWidget(subWidget,self.current_linePBA,1)
        self.current_linePBA += 1

    def _createExitButton(self):
        """Create an exit button"""
        self.exit = QPushButton("Exit")
        self.exit.setToolTip("Closes the GUI and its dependencies")
        self.exit.clicked.connect(self.closing_button)
        self.generalLayoutPBA.addWidget(self.exit,self.current_linePBA+1,3)  
        self.current_linePBA += 1

    def _createReadMe(self):
        """Creates a ReadMe tab with the ReadMe file infos"""
        self.ReadMeText = QTextEdit()
        self.ReadMeText.setReadOnly(True)
        f = open('MedPhys/ReadMe.md', 'r')
        htmlmarkdown = markdown.markdown( f.read() )
        self.ReadMeText.setText(htmlmarkdown)
        self.generalLayoutReadMe.addWidget(self.ReadMeText)

    def closing_button(self):
        self.close()

    def updateImagePBA(self):
        """Updates the Image of the attenuation of the Photon Beam"""
        if self.parameters.ShowSavedPBA:
            self.updateImagePBASaved()
        else:
            self.updateImagePBANormal()

    def updateXCOMImagePBA(self):
        """Updates the Image of the XCOM Data"""
        try:
            self.PBAXCOMData.axes.cla()
        except:
            pass
        if self.parameters.MaterialTypePBA != "None":
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,6],label="Total")
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,1],label="Rayleigh")
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,2],label="Compton")
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,3],label="P-E")
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,4],label="Pair")
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,5],label="Triple")

            self.PBAXCOMData.axes.set_title(f"μ/ρ of {self.parameters.MaterialTypePBA}")
            self.PBAXCOMData.axes.set_ylabel(r'μ/ρ (cm$^2$/g)')
            self.PBAXCOMData.axes.set_ylim(1e-5)
            self.PBAXCOMData.axes.set_xlabel("Energy (MeV)")
            self.PBAXCOMData.axes.legend()
            self.PBAXCOMData.axes.grid()

            self.PBAXCOMData.axes.axvline(self.parameters.SpecterMin,color='y',linestyle='dashed')
            self.PBAXCOMData.axes.axvline(self.parameters.SpecterMax,color='y',linestyle='dashed')
            self.PBAXCOMData.axes.axvline(2*0.511,ymax = 1e-2, color='r',linestyle='dashed')
            self.PBAXCOMData.axes.axvline(4*0.511,ymax = 1e-2, color='r',linestyle='dashed')
        self.PBAXCOMData.draw() 

    def updateAttenuationImagePBA(self):
        """Updates the Image of the whole attenuation"""
        try:
            self.PBAAttenuation.axes.cla()
        except:
            pass
        if self.parameters.MaterialTypePBA != "None":
            if self.parameters.NormalizePBA:
                self.PBAAttenuation.axes.plot(self.parameters.depthRangePBA,self.parameters.attenuatedEnergy/self.parameters.attenuatedEnergy[0],color='b')
            else:
                self.PBAAttenuation.axes.plot(self.parameters.depthRangePBA,self.parameters.attenuatedEnergy,color='b')

            if self.parameters.NormalizePBA:
                valueHVL = np.interp(1/2,np.flip(self.parameters.attenuatedEnergy)/self.parameters.attenuatedEnergy[0],np.flip(self.parameters.depthRangePBA))
                valueTVL = np.interp(1/10,np.flip(self.parameters.attenuatedEnergy)/self.parameters.attenuatedEnergy[0],np.flip(self.parameters.depthRangePBA))

                self.PBAAttenuation.axes.axhline(0.5,xmin = 0,xmax = valueHVL/self.parameters.maxDepthPBA,
                                                color = 'y',linestyle = 'dashed',label=f"HVL = {valueHVL:.3f} cm")
                self.PBAAttenuation.axes.axhline(0.1,xmin = 0,xmax = valueTVL/self.parameters.maxDepthPBA,
                                                color = 'g',linestyle = 'dashed',label=f"TVL = {valueTVL:.3f} cm")
                self.PBAAttenuation.axes.axvline(valueHVL,
                                                ymin = 0, ymax = 0.5,
                                                color = 'y',linestyle = 'dashed')
                self.PBAAttenuation.axes.axvline(valueTVL,
                                                ymin = 0, ymax = 0.1,
                                                color = 'g',linestyle = 'dashed')                                                
            else:
                valueHVL = np.interp(self.parameters.attenuatedEnergy[0]/2,np.flip(self.parameters.attenuatedEnergy),np.flip(self.parameters.depthRangePBA))
                valueTVL = np.interp(self.parameters.attenuatedEnergy[0]/10,np.flip(self.parameters.attenuatedEnergy),np.flip(self.parameters.depthRangePBA))

                self.PBAAttenuation.axes.axhline(self.parameters.attenuatedEnergy[0]/2,xmin = 0,xmax = valueHVL/self.parameters.maxDepthPBA,
                                                color = 'y',linestyle = 'dashed',label=f"HVL = {valueHVL:.3f} cm")
                self.PBAAttenuation.axes.axvline(valueHVL,
                                                ymin = 0, ymax = 1/2,
                                                color = 'y',linestyle = 'dashed')
                self.PBAAttenuation.axes.axhline(self.parameters.attenuatedEnergy[0]/10,xmin = 0,xmax = valueTVL/self.parameters.maxDepthPBA,
                                                color = 'g',linestyle = 'dashed',label=f"TVL = {valueTVL:.3f} cm")
                self.PBAAttenuation.axes.axvline(valueTVL,
                                                ymin = 0, ymax = 1/10,
                                                color = 'g',linestyle = 'dashed')

            self.PBAAttenuation.axes.set_xlim([0,self.parameters.maxDepthPBA])
            if not self.parameters.NormalizePBA:
                self.PBAAttenuation.axes.set_ylim([0,self.parameters.attenuatedEnergy[0]])
            else:
                self.PBAAttenuation.axes.set_ylim([0,1])
            self.PBAAttenuation.axes.set_xlabel("Depth (cm)")
            self.PBAAttenuation.axes.set_ylabel("Remaining Spectrum")
            self.PBAAttenuation.axes.set_title(f"Total attenuated spectrum for {self.parameters.MaterialTypePBA}")
            self.PBAAttenuation.axes.grid()
            self.PBAAttenuation.axes.axvline(self.parameters.depthPBA,color='r')
            self.PBAAttenuation.axes.legend()
        self.PBAAttenuation.draw() 

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
        
        self.throughPBA = through
        if self.parameters.ShowBaseSpecterPBA:
            if self.parameters.MeanEPBA:
                self.PBASpecter.axes.axvline(PhotonBeams.AverageE(self.parameters.Specter),color = 'b')
                self.PBASpecter.axes.plot(self.parameters.SpecterEValues,basic,label=f"Base, μ = {PhotonBeams.AverageE(self.parameters.Specter):.3f}MeV",color = 'b')
            else:
                self.PBASpecter.axes.plot(self.parameters.SpecterEValues,basic,label="Base",color = 'b')
        if self.parameters.MeanEPBA:
            Specter_tmp = np.zeros((self.parameters.SpecterfValues.shape[0],2))
            Specter_tmp[:,0] = self.parameters.SpecterEValues
            Specter_tmp[:,1] = through
            self.PBASpecter.axes.axvline(PhotonBeams.AverageE(Specter_tmp),color = 'r')
            self.PBASpecter.axes.plot(self.parameters.SpecterEValues,through,label = f"Attenuated, μ = {PhotonBeams.AverageE(Specter_tmp):.3f}MeV",color = 'r')
        else:
            self.PBASpecter.axes.plot(self.parameters.SpecterEValues,through,label = "Attenuated",color = 'r')
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
            self.parameters.XCOMData = np.loadtxt(f"MedPhys/XCOM_Data/XCOM_{self.parameters.MaterialTypePBA}.pl")

        self.updateAttenuatedPBA()

        self.updateImagePBA()
        self.updateXCOMImagePBA()
        self.updateAttenuationImagePBA()

    def update_Combo_SpecterPBA(self):
        """Updates the Combo of the Spectrum of the PBA"""
        self.parameters.SpecterTypePBA = self.PBASpecterType.currentText()
        if self.parameters.SpecterTypePBA in ["Bump"]:
            self.parameters.Specter = np.loadtxt("MedPhys/Specters/"+self.parameters.SpecterTypePBA+".txt")
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
        self.updateAttenuatedPBA()

        self.updateImagePBA()
        self.updateXCOMImagePBA()
        self.updateAttenuationImagePBA()

    def updateCheckNormalizeBox(self):
        """Updates the Check Box of Normalize"""
        if self.PBANormalizeBox.isChecked() == True:
            self.parameters.NormalizePBA = True
        else:
            self.parameters.NormalizePBA = False
        self.updateImagePBA()
        self.updateAttenuationImagePBA()

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
        self.updateAttenuatedPBA()
        self.update_Combo_SpecterPBA()
        self.updateAttenuationImagePBA()

    def updateInitKSpecter(self):
        """Updates the Initial and k Factor values of the specter"""
        try:
            self.parameters.SpecterInitialValue = float(self.PBAInitValue.text())
        except: pass
        try:
            self.parameters.SpecterKFactor = float(self.PBAKFactor.text())
        except: pass
        self.updateAttenuatedPBA()
        self.update_Combo_SpecterPBA()
        self.updateAttenuationImagePBA()

    def updateMaxDepth(self):
        """Updates the max depth value of the parameters"""
        try:
            self.parameters.maxDepthPBA = float(self.PBAMaxDepthValue.text())
            self.parameters.depthRangePBA = np.linspace(0,self.parameters.maxDepthPBA,1000)
            self.sliderDepthPBA.setMaximum(int(self.parameters.maxDepthPBA * 1000))
        except: pass
        self.updateAttenuatedPBA()
        self.update_Combo_SpecterPBA()
        self.updateAttenuationImagePBA()

    def updateLineEditDepthPBA(self):
        """Updates the Depth of attenuation based on the Line Edit"""
        try:
            self.parameters.depthPBA = float(self.lineEditDepthPBA.text())
        except:
            self.parameters.depthPBA = 0
        self.updateImagePBA()
        self.updateAttenuationImagePBA()

    def updateSliderDepthPBA(self):
        """Updates the Depth of attenuation based on the Slider"""
        try:
            self.parameters.depthPBA = self.sliderDepthPBA.value()/1000
        except:
            self.parameters.depthPBA = 0
        self.updateImagePBA()
        self.updateAttenuationImagePBA()

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

    def updateAttenuatedPBA(self):
        """Updates the Attenuated Beam in the parameters"""
        if self.parameters.MaterialTypePBA != "None":
            self.parameters.attenuatedEnergy = PhotonBeams.TotalAttenuation(self.parameters.Specter,
                                                self.parameters.XCOMData,self.parameters.rho[f"{self.parameters.MaterialTypePBA}"],
                                                self.parameters.depthRangePBA)
        else:
            self.parameters.attenuatedEnergy = []



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
    window=MedPhysWindow()
    window.show()
    sys.exit(app.exec())