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
from skimage.transform import rescale
###
try:
    import GUIParametersMedPhys
    import PhotonBeams
    import Tomography
    import MedPhysStrings
except:
    import MedPhys.GUIParametersMedPhys as GUIParametersMedPhys
    import MedPhys.PhotonBeams as PhotonBeams
    import MedPhys.Tomography as Tomography
    import MedPhys.MedPhysStrings as MedPhysStrings
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
basedir = os.path.dirname(__file__)

class MedPhysWindow(QMainWindow):
    """
    Main window of the GUI.
    """    
    def __init__(self,parent=None,language= "Fr"):
        """Initializes the GUI Window"""
        self.parameters = GUIParametersMedPhys.GUIParameters()
        self.language = language
        self.tabs = QTabWidget()
        self.BUTTON_SIZE = 40
        self.DISPLAY_HEIGHT = 35
        self.current_linePBA = 1
        self.current_lineFilter = 1
        self.current_lineTomo = 1
        super().__init__(parent=parent)
        self.setMinimumSize(1200, 700)
        self.setWindowTitle(MedPhysStrings.WindowName[f"{self.language}"])
        self.generalLayoutPBA = QGridLayout()
        self.generalLayoutTomo = QGridLayout()
        self.generalLayoutFilter = QGridLayout()
        self.generalLayoutTBA1 = QGridLayout()
        self.generalLayoutReadMe = QGridLayout()
        centralWidgetPBA = QWidget(self)
        centralWidgetTomo = QWidget(self)
        centralWidgetFilter = QWidget(self)
        centralWidgetTBA1 = QWidget(self)
        centralWidgetReadMe = QWidget(self)
        centralWidgetPBA.setLayout(self.generalLayoutPBA)
        centralWidgetFilter.setLayout(self.generalLayoutFilter)
        centralWidgetTomo.setLayout(self.generalLayoutTomo)
        centralWidgetTBA1.setLayout(self.generalLayoutTBA1)
        centralWidgetReadMe.setLayout(self.generalLayoutReadMe)
        self.tabs.addTab(centralWidgetPBA,MedPhysStrings.PhotonBeamTabName[f"{self.language}"])
        #self.tabs.addTab(centralWidgetFilter,"Filters & Fourier")
        self.tabs.addTab(centralWidgetTomo,MedPhysStrings.TomographyTabName[f"{self.language}"])
        self.tabs.addTab(centralWidgetTBA1,"TBA")
        self.tabs.addTab(centralWidgetReadMe,MedPhysStrings.ReadMeName[f"{self.language}"])

        self.setCentralWidget(self.tabs)
        #PBA
        self._addSpecterImagePBA()
        self._addMaterialTypePBA()
        self._addDepthSliderPBA()
        self._addXCOMDataImagePBA()
        self._addDataImageAttenuationPBA()
        #Tomo
        self._addImageTomo()
        self._addImageReconsTomo()
        self._addAngleSliderTomo()
        self._addFlatImageTomo()
        self._addSinoImageTomo()
        self._addParamTomo()
        self._addOptionsTomo()


        self._createExitButton() 

        self._createReadMe()

        self.generalLayoutPBA.setColumnStretch(1,5)
        self.generalLayoutPBA.setColumnStretch(2,5)
    
    def _addSpecterImagePBA(self):
        """Adds the central image socket for Photon Beam Attenuation showing the Specter"""
        self.PBASpecter = MplCanvas(self, width=6, height=6, dpi=75)
        self.PBASpecter_cid = self.PBASpecter.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.PBASpecter))
        self.PBASpecter_cod = self.PBASpecter.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.PBASpecter))

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
        self.PBAAttenuation_cid = self.PBAAttenuation.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.PBAAttenuation))
        self.PBAAttenuation_cod = self.PBAAttenuation.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.PBAAttenuation))

        self.generalLayoutPBA.addWidget(self.PBAAttenuation,self.current_linePBA,2)
        self.current_linePBA += 1

        self.updateAttenuationImagePBA()

    def _addImageTomo(self):
        """Adds the original image for tomography"""
        self.TomoImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutTomo.addWidget(self.TomoImage,self.current_lineTomo,1)

        self.updateImageTomoBase()

    def _addImageReconsTomo(self):
        """Adds the Reconstructed image for tomography"""
        self.TomoReconstructed = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutTomo.addWidget(self.TomoReconstructed,self.current_lineTomo,2)
        self.current_lineTomo += 1

        self.updateImageTomoBase()
        self.updateImageReconstructed()

    def _addAngleSliderTomo(self):
        """Adds the slider for the angle of the tomography"""
        subWidget = QWidget()
        layout = QHBoxLayout()
        subWidget.setLayout(layout)

        sizeText = 45

        self.sliderAngleTomo = QSlider(Qt.Horizontal)
        self.lineEditAngleTomo = QLineEdit()

        self.lineEditAngleTomo.setFixedWidth(sizeText)
        self.lineEditAngleTomo.setText("0")

        self.sliderAngleTomo.setMaximum(360)
        self.sliderAngleTomo.setTickPosition(QSlider.TicksBothSides)
        self.sliderAngleTomo.setSingleStep(90)
        self.sliderAngleTomo.setTickInterval(90)

        self.lineEditAngleTomo.editingFinished.connect(self.updateLineEditAngleTomo)
        self.sliderAngleTomo.valueChanged.connect(self.updateSliderAngleTomo)

        layout.addWidget(QLabel(MedPhysStrings.AngleTomoLabel[f"{self.language}"]))
        layout.addWidget(self.sliderAngleTomo)
        layout.addWidget(self.lineEditAngleTomo)

        self.generalLayoutTomo.addWidget(subWidget,self.current_lineTomo,1)
        self.current_lineTomo += 1

    def _addFlatImageTomo(self):
        """Adds the flattened line image for tomography"""
        self.FlatImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.generalLayoutTomo.addWidget(self.FlatImage,self.current_lineTomo,1)

        self.updateImageTomoSlice()

    def _addSinoImageTomo(self):
        """Adds the sinogram of the image for tomography"""
        self.SinoImage = MplCanvas(self, width=6, height=6, dpi=75)
        self.SinoImage_cid = self.SinoImage.fig.canvas.mpl_connect('button_press_event', partial(self.onClick, which = self.SinoImage))
        self.SinoImage_cod = self.SinoImage.fig.canvas.mpl_connect('scroll_event', partial(self.onRoll, which = self.SinoImage))

        self.generalLayoutTomo.addWidget(self.SinoImage,self.current_lineTomo,2)
        self.current_lineTomo += 1

        self.updateImageTomoSino()

    def _addMaterialTypePBA(self):
        """Adds a Combo Box to determine the material for attenuation"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)

        self.PBAMaterialType = QComboBox()
        for _, names in MedPhysStrings.ElementsNamePBA.items():
            self.PBAMaterialType.addItem(names[f"{self.language}"])
        self.PBAMaterialType.setCurrentText(MedPhysStrings.ElementsNamePBA[f"{self.parameters.MaterialTypePBA}"][f"{self.language}"])

        self.PBASpecterType = QComboBox()
        for _, names in MedPhysStrings.SpecterPBAName.items():
            self.PBASpecterType.addItem(names[f"{self.language}"])
        self.PBASpecterType.setCurrentText(MedPhysStrings.SpecterPBAName[f"{self.parameters.SpecterTypePBA}"][f"{self.language}"])

        self.PBAMaterialType.activated[str].connect(self.update_Combo_MaterialPBA)
        self.PBASpecterType.activated[str].connect(self.update_Combo_SpecterPBA)

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

        self.PBASaveButton = QPushButton(MedPhysStrings.SaveLabel[self.language])
        self.PBAClearButton = QPushButton(MedPhysStrings.ClearLabel[self.language])
        self.PBASavedNumber = QLineEdit()
        self.PBASavedNumber.setFixedWidth(30)
        self.PBASavedNumber.setText(f"{self.parameters.SavedCounterPBA}")
        self.PBASavedNumber.setReadOnly(True)
        self.PBAShowBox = QCheckBox()

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
        layout.addWidget(self.PBASpecterType,0,1)

        layout.addWidget(QLabel(MedPhysStrings.MinLabel[self.language]),1,0)
        layout.addWidget(self.PBAMinLineEdit,1,1)
        layout.addWidget(QLabel(MedPhysStrings.MaxLabel[self.language]),1,2)
        layout.addWidget(self.PBAMaxLineEdit,1,3)

        layout.addWidget(QLabel(MedPhysStrings.InitValueLabel[self.language]),2,0)
        layout.addWidget(self.PBAInitValue,2,1)
        layout.addWidget(QLabel(MedPhysStrings.FactorLabel[self.language]),2,2)
        layout.addWidget(self.PBAKFactor,2,3)

        layout.addWidget(QLabel(MedPhysStrings.MaxDepthLabel[self.language]),3,0)
        layout.addWidget(self.PBAMaxDepthValue,3,1)

        layout.addWidget(QLabel(MedPhysStrings.NormalizeLabel[self.language]),4,0)
        layout.addWidget(self.PBANormalizeBox,4,1)
        layout.addWidget(QLabel(MedPhysStrings.SuperposeLabel[self.language]),4,2)
        layout.addWidget(self.PBASuperposeBox,4,3)

        layout.addWidget(QLabel(MedPhysStrings.AverageLabel[self.language]),5,0)
        layout.addWidget(self.PBAAvgBox,5,1)

        layout.addWidget(self.PBASaveButton,6,0)
        layout.addWidget(self.PBAClearButton,6,1)
        layout.addWidget(self.PBASavedNumber,6,2)
        layout.addWidget(QLabel(MedPhysStrings.ShowLabel[self.language]),7,0)
        layout.addWidget(self.PBAShowBox,7,1)

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
        self.exitPBA = QPushButton(MedPhysStrings.ExitButton[f"{self.language}"])
        self.exitFilter = QPushButton(MedPhysStrings.ExitButton[f"{self.language}"])
        self.exitTomo = QPushButton(MedPhysStrings.ExitButton[f"{self.language}"])
        self.exitPBA.setToolTip(MedPhysStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitFilter.setToolTip(MedPhysStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitTomo.setToolTip(MedPhysStrings.ExitButtonTooltip[f"{self.language}"] + " (Ctrl+Shift+E)")
        self.exitPBA.setShortcut("Ctrl+Shift+E")
        self.exitFilter.setShortcut("Ctrl+Shift+E")
        self.exitTomo.setShortcut("Ctrl+Shift+E")

        self.exitPBA.clicked.connect(self.closing_button)
        self.exitFilter.clicked.connect(self.closing_button)
        self.exitTomo.clicked.connect(self.closing_button)
        self.generalLayoutPBA.addWidget(self.exitPBA,self.current_linePBA+1,3)  
        #self.generalLayoutFilter.addWidget(self.exitFilter,self.current_lineFilter+1,3)  
        self.generalLayoutTomo.addWidget(self.exitTomo,self.current_lineTomo+1,3)  
        self.current_linePBA += 1
        self.current_lineFilter += 1
        self.current_lineTomo += 1
    
    def _addParamTomo(self):
        """Creates parameters buttons for the Tomography"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)        
        sizeText = 40
        self.ParametersLineEditTomo = np.zeros((self.parameters.NumberShapesTomo,self.parameters.NumberParameterTomo1,self.parameters.NumberParameterTomo2),dtype = object)

        for k in range(self.parameters.NumberShapesTomo):
            for i in range(self.parameters.NumberParameterTomo1):
                for j in range(self.parameters.NumberParameterTomo2):
                    self.ParametersLineEditTomo[k,i,j] = QLineEdit()
                    self.ParametersLineEditTomo[k,i,j].setFixedWidth(sizeText)
                    self.ParametersLineEditTomo[k,i,j].setText(str(self.parameters.ParameterTomo[k,i,j]))
                    self.ParametersLineEditTomo[k,i,j].editingFinished.connect(self.updateParametersTomo)

                    if (k ==0 or i != 0):
                        layout.addWidget(self.ParametersLineEditTomo[k,i,j],i+2,k*self.parameters.NumberParameterTomo1 + j+1)
                    if i == 0:
                        if j % 2 == 0: layout.addWidget(QLabel("x"),1,k*self.parameters.NumberParameterTomo1 + j+1)
                        elif j % 2 == 1: layout.addWidget(QLabel("y"),1,k*self.parameters.NumberParameterTomo1 + j+1)

                if i == 0: layout.addWidget(QLabel(MedPhysStrings.ParametersDimensionsTomo[f"{self.language}"]),i+2,0)
                if i == 1: layout.addWidget(QLabel(MedPhysStrings.ParametersCenterTomo[f"{self.language}"]),i+2,0)
                if i == 2: layout.addWidget(QLabel(MedPhysStrings.ParametersSizeTomo[f"{self.language}"]),i+2,0)
                if i == 3: layout.addWidget(QLabel(MedPhysStrings.ParametersHeightTomo[f"{self.language}"]),i+2,0)

        layout.addWidget(QLabel(MedPhysStrings.ParametersImageTomo[f"{self.language}"]),0,0)
        self.generalLayoutTomo.addWidget(subWidget,self.current_lineTomo,1)

    def _addOptionsTomo(self):
        """Creates the Option parameters for the Tomography"""
        subWidget = QWidget()
        layout = QGridLayout()
        subWidget.setLayout(layout)        
        sizeText = 30

        self.generalLayoutTomo.addWidget(subWidget,self.current_lineTomo,2)

        self.ImageChoiceTomo = np.zeros((self.parameters.NumberShapesTomo),dtype = object)
        for i in range(self.parameters.NumberShapesTomo):
            self.ImageChoiceTomo[i] = QComboBox()
            for _, names in MedPhysStrings.ImageTomoName.items():
                self.ImageChoiceTomo[i].addItem(names[f"{self.language}"])
            self.ImageChoiceTomo[i].setCurrentText(MedPhysStrings.ImageTomoName[f"{self.parameters.ImageTomoName[i]}"][f"{self.language}"])
            self.ImageChoiceTomo[i].activated[str].connect(self.update_Combo_ImageTomo)

        self.ImageFilterTomo = QComboBox()
        for _, names in MedPhysStrings.FilterTomoName.items():
            self.ImageFilterTomo.addItem(names[f"{self.language}"])
        self.ImageFilterTomo.setCurrentText(MedPhysStrings.FilterTomoName[f"{self.parameters.ReconstructionFilterName}"][f"{self.language}"])

        self.StepAngleTomoLineEdit = QLineEdit()
        self.StepAngleTomoLineEdit.setText(f"{self.parameters.AngleStepTomo}")
        self.StepAngleTomoLineEdit.setFixedWidth(sizeText)

        self.logImageTomoQCheckBox = QCheckBox()
        self.logImageTomoQCheckBox.setChecked(self.parameters.logImagesTomo)
        self.logImageTomoQCheckBox.stateChanged.connect(self.update_Check_logImageTomo)

        self.ImageFilterTomo.activated[str].connect(self.update_Combo_FilterTomo)
        self.StepAngleTomoLineEdit.editingFinished.connect(self.update_Step_AngleTomo)

        layout.addWidget(QLabel(MedPhysStrings.FilterTomoLabel[f"{self.language}"]),0,0)
        layout.addWidget(self.ImageFilterTomo,0,1)
        layout.addWidget(QLabel(MedPhysStrings.StepTomoLabel[f"{self.language}"]),1,0)
        layout.addWidget(self.StepAngleTomoLineEdit,1,1)

        layout.addWidget(QLabel(MedPhysStrings.LogImageTomoLabel[f"{self.language}"]),2,0)
        layout.addWidget(self.logImageTomoQCheckBox,2,1)

        for i in range(self.parameters.NumberShapesTomo):
            layout.addWidget(QLabel(MedPhysStrings.ImageTomoLabel[f"{self.language}"]+f" {i+1}"),3+i,0)
            layout.addWidget(self.ImageChoiceTomo[i],3+i,1)

        self.generalLayoutTomo.addWidget(subWidget,self.current_lineTomo,2)
        self.current_lineTomo += 1

    def _createReadMe(self):
        """Creates a ReadMe tab with the ReadMe file infos"""
        self.ReadMeText = QTextEdit()
        self.ReadMeText.setReadOnly(True)
        f = open(f'{basedir}/ReadMePhysMed.md', 'r')
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
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,6],label=MedPhysStrings.TotalLabel[self.language])
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,1],label="Rayleigh")
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,2],label="Compton")
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,3],label="P-E")
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,4],label=MedPhysStrings.PairLabel[self.language])
            self.PBAXCOMData.axes.loglog(self.parameters.XCOMData[:,0],self.parameters.XCOMData[:,5],label=MedPhysStrings.TripleLabel[self.language])

            self.PBAXCOMData.axes.set_title(MedPhysStrings.OfLabel[self.language] +
                                               MedPhysStrings.ElementsNamePBA[self.parameters.MaterialTypePBA][self.language])
            self.PBAXCOMData.axes.set_ylabel(MedPhysStrings.XCOMDataYLabel[self.language])
            self.PBAXCOMData.axes.set_ylim(1e-5)
            self.PBAXCOMData.axes.set_xlabel(MedPhysStrings.EnergyLabel[self.language])
            self.PBAXCOMData.axes.legend(loc = 'upper right')
            self.PBAXCOMData.axes.grid()

            self.PBAXCOMData.axes.axvline(self.parameters.SpecterMin,color='y',linestyle='dashed')
            self.PBAXCOMData.axes.axvline(self.parameters.SpecterMax,color='y',linestyle='dashed')
            self.PBAXCOMData.axes.axvline(2*0.511,ymax = 1e-1, color='r',linestyle='dashed')
            self.PBAXCOMData.axes.axvline(4*0.511,ymax = 1e-1, color='r',linestyle='dashed')
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
                                                color = 'y',linestyle = 'dashed',label=f"HVL = {valueHVL:.3g} cm")
                self.PBAAttenuation.axes.axhline(0.1,xmin = 0,xmax = valueTVL/self.parameters.maxDepthPBA,
                                                color = 'g',linestyle = 'dashed',label=f"TVL = {valueTVL:.3g} cm")
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
                                                color = 'y',linestyle = 'dashed',label=f"HVL = {valueHVL:.3g} cm")
                self.PBAAttenuation.axes.axvline(valueHVL,
                                                ymin = 0, ymax = 1/2,
                                                color = 'y',linestyle = 'dashed')
                self.PBAAttenuation.axes.axhline(self.parameters.attenuatedEnergy[0]/10,xmin = 0,xmax = valueTVL/self.parameters.maxDepthPBA,
                                                color = 'g',linestyle = 'dashed',label=f"TVL = {valueTVL:.3g} cm")
                self.PBAAttenuation.axes.axvline(valueTVL,
                                                ymin = 0, ymax = 1/10,
                                                color = 'g',linestyle = 'dashed')

            self.PBAAttenuation.axes.set_xlim([0,self.parameters.maxDepthPBA])
            if not self.parameters.NormalizePBA:
                self.PBAAttenuation.axes.set_ylim([0,self.parameters.attenuatedEnergy[0]])
            else:
                self.PBAAttenuation.axes.set_ylim([0,1])
            self.PBAAttenuation.axes.set_xlabel(MedPhysStrings.DepthCmLabel[self.language])
            self.PBAAttenuation.axes.set_ylabel(MedPhysStrings.RemainingSpectrumLabel[self.language])
            self.PBAAttenuation.axes.set_title(MedPhysStrings.TitleRemainingSpectrumLabel[self.language] +
                                                MedPhysStrings.ElementsNamePBA[self.parameters.MaterialTypePBA][self.language])
            self.PBAAttenuation.axes.grid()
            self.PBAAttenuation.axes.axvline(self.parameters.depthPBA,color='r')
            self.PBAAttenuation.axes.legend(loc = 'upper right')
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
                self.PBASpecter.axes.plot(self.parameters.SpecterEValues,basic,label= MedPhysStrings.BaseLabel[self.language] + f", μ = {PhotonBeams.AverageE(self.parameters.Specter):.3g}MeV",color = 'b')
                self.PBASpecter.axes.axvline(PhotonBeams.AverageE(self.parameters.Specter),color = 'b')
            else:
                self.PBASpecter.axes.plot(self.parameters.SpecterEValues,basic,label=MedPhysStrings.BaseLabel[self.language],color = 'b')
        if self.parameters.MeanEPBA:
            Specter_tmp = np.zeros((self.parameters.SpecterfValues.shape[0],2))
            Specter_tmp[:,0] = self.parameters.SpecterEValues
            Specter_tmp[:,1] = through
            self.PBASpecter.axes.plot(self.parameters.SpecterEValues,through,label = MedPhysStrings.AttenuatedLabel[self.language] + f", μ = {PhotonBeams.AverageE(Specter_tmp):.3g}MeV",color = 'r')
            self.PBASpecter.axes.axvline(PhotonBeams.AverageE(Specter_tmp),color = 'r')
        else:
            self.PBASpecter.axes.plot(self.parameters.SpecterEValues,through,label = MedPhysStrings.AttenuatedLabel[self.language],color = 'r')
        self.baseImagePBA()
        self.PBASpecter.draw() 

    def updateImageTomoBase(self):
        """Updates the basic Image for the Tomography"""
        try:
            self.TomoImage.axes.cla()
        except:
            pass

        if not self.parameters.logImagesTomo:
            self.TomoImage.axes.pcolormesh(self.parameters.ImageRotatedTomo,cmap = 'Greys_r')
        else:
            self.TomoImage.axes.pcolormesh(np.log10(self.parameters.ImageRotatedTomo+1),cmap = 'Greys_r')
        self.TomoImage.axes.invert_yaxis()
        self.TomoImage.axes.axvline(self.parameters.ImageRotatedTomo.shape[0]/2)
        self.TomoImage.axes.axhline(self.parameters.ImageRotatedTomo.shape[0]/2)
        self.TomoImage.axes.set_title(MedPhysStrings.ImageTomoName[self.parameters.ImageTomoName[0]][self.language] +
                                        ", " +
                                        MedPhysStrings.AngleTomoLabel[self.language] +  
                                        " = " + 
                                        str(f"{self.parameters.angleTomo:.1f}"))
        self.TomoImage.draw()

    def updateImageReconstructed(self):
        """Updates the reconstructed Image for the Tomography"""
        try:
            self.TomoReconstructed.axes.cla()
        except:
            pass
        if not self.parameters.logImagesTomo:
            self.TomoReconstructed.axes.pcolormesh(self.parameters.ReconstructedRotatedTomo,cmap = 'Greys_r')
        else:
            self.TomoReconstructed.axes.pcolormesh(np.log10(self.parameters.ReconstructedRotatedTomo+1),cmap = 'Greys_r')
        self.TomoReconstructed.axes.invert_yaxis()

        if self.language in ["En"]:
            self.TomoReconstructed.axes.set_title(MedPhysStrings.ReconstructedLabel[self.language] + 
                                                    " " +
                                                    MedPhysStrings.ImageTomoName[self.parameters.ImageTomoName[0]][self.language] + 
                                                    ", " + 
                                                    MedPhysStrings.FilterTomoName[self.parameters.ReconstructionFilterName][self.language] +
                                                    " " + 
                                                    MedPhysStrings.Reconstructed2Label[self.language])
        elif self.language in ["Fr"]:
            self.TomoReconstructed.axes.set_title(MedPhysStrings.ReconstructedLabel[self.language] + 
                                                    " " +
                                                    MedPhysStrings.ImageTomoName[self.parameters.ImageTomoName[0]][self.language] + 
                                                    " " +
                                                    MedPhysStrings.Reconstructed2Label[self.language]+ 
                                                    ", " + 
                                                    MedPhysStrings.Reconstructed3Label[self.language] + 
                                                    " " +
                                                    MedPhysStrings.FilterTomoName[self.parameters.ReconstructionFilterName][self.language])
        self.TomoReconstructed.draw()

    def updateImageTomoSlice(self):
        """Updates the Slice Image for the Tomography"""
        try:
            self.FlatImage.axes.cla()
        except:
            pass

        self.FlatImage.axes.plot(self.parameters.FlatImageAngleTomo)
        self.FlatImage.axes.set_title(MedPhysStrings.LineIntensityLabel[self.language] +
                                        self.parameters.ImageTomoName[0] +
                                        MedPhysStrings.LineIntensity2Label[self.language] +
                                        f"{self.parameters.angleTomo:.1f}" +
                                        MedPhysStrings.LineIntensity3Label[self.language])
        self.FlatImage.axes.grid()
        self.FlatImage.axes.set_xlabel(MedPhysStrings.PositionLabel[self.language])
        self.FlatImage.axes.set_ylabel(MedPhysStrings.SummedIntensityLabel[self.language])

        self.FlatImage.draw()

    def updateImageTomoSino(self):
        """Update the Sinogram Image for the Tomography"""
        try:
            self.SinoImage.axes.cla()
        except:
            pass
        if not self.parameters.logImagesTomo:
            self.SinoImage.axes.pcolormesh(self.parameters.SinogramTomo,cmap = 'Greys_r')
        else:
            self.SinoImage.axes.pcolormesh(np.log10(self.parameters.SinogramTomo+1),cmap = 'Greys_r')
        self.SinoImage.axes.axhline(self.parameters.SinogramTomo.shape[0]/2,color = 'r',alpha=0.3)
        self.SinoImage.axes.axvline(self.parameters.angleTomo/self.parameters.AngleStepTomo,color = 'r',alpha=0.3)
        self.SinoImage.axes.set_title(MedPhysStrings.SinogramTitleLabel[self.language] +
                                        MedPhysStrings.ImageTomoName[self.parameters.ImageTomoName[0]][self.language] +
                                        MedPhysStrings.SinogramTitle2Label[self.language] +
                                        str(f"{self.parameters.AngleStepTomo:.2f}") +
                                        MedPhysStrings.LineIntensity3Label[self.language])

        self.SinoImage.draw()

    def baseImagePBA(self):
        self.PBASpecter.axes.grid()
        if self.parameters.ShowBaseSpecterPBA or self.parameters.ShowSavedPBA:
            self.PBASpecter.axes.legend(loc = 'upper right')
        self.PBASpecter.axes.set_xlabel(MedPhysStrings.EnergyLabel[self.language])
        if self.parameters.NormalizePBA and not self.parameters.ShowSavedPBA:
            self.PBASpecter.axes.set_ylabel(MedPhysStrings.FrequencyLabel[self.language])
        else:
            self.PBASpecter.axes.set_ylabel(MedPhysStrings.DistributionLabel[self.language])
        if self.parameters.MaterialTypePBA == "None":
            if self.parameters.NormalizePBA:
                if self.language in ["En"]:
                    self.PBASpecter.axes.set_title(MedPhysStrings.NormalizedTitleLabel[self.language] + 
                                                    " " + 
                                                    MedPhysStrings.SpecterPBAName[self.parameters.SpecterTypePBA][self.language] + 
                                                    " " + 
                                                    MedPhysStrings.SpectrumTitleLabel[self.language])
                elif self.language in ["Fr"]:
                    self.PBASpecter.axes.set_title(MedPhysStrings.SpectrumTitleLabel[self.language] + 
                                                    " " + 
                                                    MedPhysStrings.NormalizedTitleLabel[self.language] +
                                                    " " +
                                                    MedPhysStrings.SpecterPBAName[self.parameters.SpecterTypePBA][self.language])
            else:
                if self.language in ["En"]:
                    self.PBASpecter.axes.set_title(MedPhysStrings.SpecterPBAName[self.parameters.SpecterTypePBA][self.language] + " " + MedPhysStrings.SpectrumTitleLabel[self.language])
                elif self.language in ["Fr"]:
                    self.PBASpecter.axes.set_title(MedPhysStrings.SpectrumTitleLabel[self.language] + 
                                                    " " + 
                                                    MedPhysStrings.SpecterPBAName[self.parameters.SpecterTypePBA][self.language])
        else:
            if self.parameters.NormalizePBA:
                self.PBASpecter.axes.set_title(MedPhysStrings.AttenuatedTitle0Label[self.language] + 
                                                MedPhysStrings.SpecterPBAName[self.parameters.SpecterTypePBA][self.language]+
                                                MedPhysStrings.AttenuatedTitle2Label[self.language] + 
                                                str(self.parameters.depthPBA) +
                                                MedPhysStrings.AttenuatedTitle3Label[self.language] +
                                                MedPhysStrings.ElementsNamePBA[self.parameters.MaterialTypePBA][self.language])
            else:
                self.PBASpecter.axes.set_title(MedPhysStrings.AttenuatedTitle1Label[self.language] + 
                                                MedPhysStrings.SpecterPBAName[self.parameters.SpecterTypePBA][self.language]+
                                                MedPhysStrings.AttenuatedTitle2Label[self.language] + 
                                                str(self.parameters.depthPBA) +
                                                MedPhysStrings.AttenuatedTitle3Label[self.language] +
                                                MedPhysStrings.ElementsNamePBA[self.parameters.MaterialTypePBA][self.language])
        if self.parameters.ShowSavedPBA:
            self.PBASpecter.axes.set_title(MedPhysStrings.AttenuatedSpectrumTitleLabel[self.language])
        self.PBASpecter.axes.set_xlim(left = 0)
    def update_Combo_MaterialPBA(self):
        """Updates the Combo of the Material of the PBA"""
        name_tmp = self.PBAMaterialType.currentText()
        for dict, names in MedPhysStrings.ElementsNamePBA.items():
            if name_tmp in names.values():
                self.parameters.MaterialTypePBA = dict

        if self.parameters.MaterialTypePBA != "None":
            self.parameters.XCOMData = np.loadtxt(f"{basedir}/XCOM_Data/XCOM_{self.parameters.MaterialTypePBA}.pl")

        self.updateAttenuatedPBA()

        self.updateImagePBA()
        self.updateXCOMImagePBA()
        self.updateAttenuationImagePBA()

    def update_Combo_ImageTomo(self):
        """Updates the Combo of the Image of the Tomo"""
        self.parameters.ImageTomo = np.zeros((int(self.parameters.ParameterTomo[0,0,0]),int(self.parameters.ParameterTomo[0,0,1])))
        for i in range(self.parameters.NumberShapesTomo):
            name_tmp = self.ImageChoiceTomo[i].currentText()
            for dict, names in MedPhysStrings.ImageTomoName.items():
                if name_tmp in names.values():
                    self.parameters.ImageTomoName[i] = dict
            if self.parameters.ImageTomoName[i] not in ["Rectangle","Ellipsoid","Dense Shell Ellipsoid","Dense Core Ellipsoid",
                                                    "Gaussian","Sinc"]:
                tmpImg = mpimg.imread(f'{basedir}/TomoImage/{self.parameters.ImageTomoName[i]}.pgm')
                self.parameters.ImageTomo += self.parameters.ParameterTomo[i,3,0]*rescale(tmpImg, scale = [self.parameters.ParameterTomo[0,0,0]/tmpImg.shape[0],self.parameters.ParameterTomo[0,0,1]/tmpImg.shape[1]])
            else:
                self.parameters.ImageTomo += Tomography.CreateImage(self.parameters.ParameterTomo[i,:,:],self.parameters.ImageTomoName[i])
        self.update_ImageTomo()

    def update_ImageTomo(self):
        self.parameters.ImageRotatedTomo = Tomography.Rotate(self.parameters.ImageTomo,angle = self.parameters.angleTomo*2*np.pi/360)

        self.parameters.FlatImageAngleTomo = np.sum(self.parameters.ImageRotatedTomo,axis=1)
        self.parameters.SinogramTomo = Tomography.Sinogram(self.parameters.ImageTomo, angles_step = self.parameters.AngleStepTomo)
        self.parameters.ReconstructedTomo = Tomography.Reconstruction(self.parameters.SinogramTomo, 
                                                                angles_step = self.parameters.AngleStepTomo,
                                                                filter=self.parameters.ReconstructionFilterName)
        self.parameters.ReconstructedRotatedTomo = Tomography.Rotate(self.parameters.ReconstructedTomo,angle = self.parameters.angleTomo*2*np.pi/360)

        self.updateAllImagesTomo()

    def updateAllImagesTomo(self):
        self.updateImageTomoSlice()
        self.updateImageTomoBase()
        self.updateImageTomoSino()
        self.updateImageReconstructed()

    def updateParametersTomo(self):
        """Updates the Parameters of the Tomo Image"""

        for k in range(self.parameters.NumberShapesTomo):
            for i in range(self.parameters.NumberParameterTomo1):
                for j in range(self.parameters.NumberParameterTomo2):
                    try:
                        self.parameters.ParameterTomo[k,i,j] = float(self.ParametersLineEditTomo[k,i,j].text())
                    except:
                        self.parameters.ParameterTomo[k,i,j] = 1.0
                        self.ParametersLineEditTomo[k,i,j].setText("0.0")
                    if i == 0:
                        self.parameters.ParameterTomo[k,i,j] = self.parameters.ParameterTomo[0,i,j]
        """if self.parameters.ImageTomoName in ["Rectangle","Ellipsoid","Dense Shell Ellipsoid","Dense Core Ellipsoid",
                                             "Gaussian","Sinc"]:"""
        if True: self.update_Combo_ImageTomo()

    def update_Check_logImageTomo(self):
        """Updates the Boolean for Full Range"""
        if self.logImageTomoQCheckBox.isChecked():
            self.parameters.logImagesTomo = True
        else:
            self.parameters.logImagesTomo = False
        self.updateImageSliceTomo()

    def update_Combo_FilterTomo(self):
        self.parameters.ReconstructionFilterName = self.ImageFilterTomo.currentText()
        name_tmp = self.ImageFilterTomo.currentText()
        for dict, names in MedPhysStrings.FilterTomoName.items():
            if name_tmp in names.values():
                self.parameters.ReconstructionFilterName = dict
        self.parameters.ReconstructedTomo = Tomography.Reconstruction(self.parameters.SinogramTomo, 
                                                                angles_step = self.parameters.AngleStepTomo,
                                                                filter=self.parameters.ReconstructionFilterName)
        self.parameters.ReconstructedRotatedTomo = Tomography.Rotate(self.parameters.ReconstructedTomo,angle = self.parameters.angleTomo*2*np.pi/360)

        self.updateImageReconstructed()

    def update_Step_AngleTomo(self):
        """Updates the Step in Angles"""
        self.parameters.AngleStepTomo = float(self.StepAngleTomoLineEdit.text())

        self.parameters.SinogramTomo = Tomography.Sinogram(self.parameters.ImageTomo, angles_step = self.parameters.AngleStepTomo)
        self.parameters.ReconstructedTomo = Tomography.Reconstruction(self.parameters.SinogramTomo, 
                                                        angles_step = self.parameters.AngleStepTomo,
                                                        filter=self.parameters.ReconstructionFilterName)
        self.parameters.ReconstructedRotatedTomo = Tomography.Rotate(self.parameters.ReconstructedTomo,angle = self.parameters.angleTomo*2*np.pi/360)

        self.updateImageTomoSino()
        self.updateImageReconstructed()

    def update_Combo_SpecterPBA(self):
        """Updates the Combo of the Spectrum of the PBA"""
        name_tmp = self.PBASpecterType.currentText()
        for dict, names in MedPhysStrings.SpecterPBAName.items():
            if name_tmp in names.values():
                self.parameters.SpecterTypePBA = dict

        if self.parameters.SpecterTypePBA in ["Bump"]:
            self.parameters.Specter = np.loadtxt(f"{basedir}/Specters/"+self.parameters.SpecterTypePBA+".txt")
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
        self.parameters.SavedCounterPBA = 0
        self.PBASavedNumber.setText(f"{self.parameters.SavedCounterPBA}")

    def saveSavedSpecterPBA(self):
        """Saves the current Specter"""
        self.parameters.SavedSpectersE.append(self.parameters.SpecterEValues)
        self.parameters.SavedSpectersF.append(self.throughPBA)
        self.parameters.SavedSpectersLabel.append(f"{MedPhysStrings.ElementsNamePBA[self.parameters.MaterialTypePBA][self.language]}: {self.parameters.depthPBA} cm")
        self.parameters.SavedCounterPBA += 1
        self.PBASavedNumber.setText(f"{self.parameters.SavedCounterPBA}")

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
                                                self.parameters.depthRangePBA)*(self.parameters.SpecterEValues[1]-self.parameters.SpecterEValues[0])
        else:
            self.parameters.attenuatedEnergy = []

    def updateLineEditAngleTomo(self):
        """Updates the Angle of tomography based on the Line Edit"""
        try:
            self.parameters.angleTomo = int(self.lineEditAngleTomo.text())
        except:
            self.parameters.angleTomo = 0
        self.updateRotatedImageTomo()
        self.updateImageSliceTomo()

    def updateSliderAngleTomo(self):
        """Updates the Angle of tomography based on the Slider"""
        try:
            self.parameters.angleTomo = int(self.sliderAngleTomo.value())
        except:
            self.parameters.angleTomo = 0
        self.updateRotatedImageTomo()
        self.updateImageSliceTomo()
        

    def updateRotatedImageTomo(self):
        """Rotate the stored image around an axis"""
        self.parameters.ImageRotatedTomo = Tomography.Rotate(self.parameters.ImageTomo,angle = self.parameters.angleTomo*2*np.pi/360)
        self.parameters.ReconstructedRotatedTomo = Tomography.Rotate(self.parameters.ReconstructedTomo,angle = self.parameters.angleTomo*2*np.pi/360)
        self.updateImageTomoSlice()
        self.updateImageTomoBase()
        self.updateImageTomoSino()
        self.updateImageReconstructed()

    def updateSinogramImageTomo(self):
        """Updates the Sinogram"""
        self.parameters.SinogramTomo = Tomography.Sinogram(self.ImageTomo, angles_step = self.parameters.angleTomo)
        self.parameters.ReconstructedTomo = Tomography.Reconstruction(self.parameters.SinogramTomo, 
                                                                angles_step = self.parameters.AngleStepTomo,
                                                                filter=self.parameters.ReconstructionFilterName)
        self.parameters.ReconstructedRotatedTomo = Tomography.Rotate(self.parameters.ReconstructedTomo,angle = self.parameters.angleTomo*2*np.pi/360)
        self.updateImageTomoSlice()
        self.updateImageTomoBase()
        self.updateImageTomoSino()
        self.updateImageReconstructed()

    def updateImageSliceTomo(self):
        self.parameters.FlatImageAngleTomo = np.sum(self.parameters.ImageRotatedTomo,axis=1)
        self.updateImageTomoSlice()
        self.updateImageTomoBase()
        self.updateImageTomoSino()
        self.updateImageReconstructed()

    def onClick(self,event,which):
        """Allows to click on an image and update the interface"""
        ix, iy = event.xdata, event.ydata
        which.coords = []
        which.coords.append((ix, iy))
        if len(which.coords) == 2:
            which.fig.canvas.mpl_disconnect(self.cid)
        if which == self.PBAAttenuation:
            self.parameters.depthPBA = ix
            self.lineEditDepthPBA.setText(str(f"{ix:.2f}"))
            self.update_Combo_SpecterPBA()
        elif which == self.SinoImage:
            self.parameters.angleTomo = ix * self.parameters.AngleStepTomo
            self.lineEditAngleTomo.setText(str(f"{ix:.1f}"))
            self.updateRotatedImageTomo()
            self.updateImageSliceTomo()
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
        if which in [self.PBAAttenuation,self.PBASpecter]:
            actual = float(self.lineEditDepthPBA.text())
            scale_factor = scale_factor*self.parameters.depthRangePBA[-1]/20
            if actual + scale_factor >= 0:
                self.lineEditDepthPBA.setText(str(f"{(actual + scale_factor):.2f}"))
            else:
                self.lineEditDepthPBA.setText(str(f"{(0):.2f}"))
            self.parameters.depthPBA = float(self.lineEditDepthPBA.text())
            self.update_Combo_SpecterPBA()
        elif which == self.SinoImage:
            actual = float(self.lineEditAngleTomo.text())
            self.parameters.angleTomo = actual + scale_factor * self.parameters.AngleStepTomo
            self.lineEditAngleTomo.setText(str(f"{(actual + scale_factor * self.parameters.AngleStepTomo):.1f}"))
            self.updateImageSliceTomo()
            self.updateRotatedImageTomo()

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
    window=MedPhysWindow()
    window.show()
    sys.exit(app.exec())