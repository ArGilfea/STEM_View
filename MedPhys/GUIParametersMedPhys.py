import numpy as np
import matplotlib.image as mpimg
import os
try:
    import Tomography
except:
    import MedPhys.Tomography as Tomography

class GUIParameters(object):
    """Class where the parameters of the GUI are stored"""
    def __init__(self):
        basedir = os.path.dirname(__file__)

        self.SpecterTypePBA = "Bump"
        self.MaterialTypePBA = "None"

        self.Specter = np.loadtxt(f"{basedir}/Specters/"+self.SpecterTypePBA+".txt")

        self.SpecterEValues = self.Specter[:,0]
        self.SpecterfValues = self.Specter[:,1]
        self.SpecterMin = 0.010
        self.SpecterMax = 0.080
        self.SpecterInitialValue = 1
        self.SpecterKFactor = -1

        self.ShowSavedPBA = False
        self.SavedSpectersE = []
        self.SavedSpectersF = []
        self.SavedSpectersLabel = []
        self.SavedCounterPBA = 0

        self.rho = {
            "Al" : 2.6989,
            "C" : 0,
            "Ca" : 0,
            "Cu" : 8.96,
            "H" : 0,
            "H2O" : 1,
            "I" : 0,
            "N" : 0,
            "O" : 0,
            "P" : 0,
            "Pb" : 10.66,
            "Skull" : 1.517,
            "Zn" : 7.13,
        }
        self.XCOMData = []


        self.ShowBaseSpecterPBA = False
        self.NormalizePBA = False
        self.MeanEPBA = False

        self.depthPBA = 0
        self.maxDepthPBA = 3.0
        self.depthRangePBA = np.linspace(0,self.maxDepthPBA,1000)

        self.attenuatedEnergy = []

        self.angleTomo = 0

        self.NumberParameterTomo1= 4
        self.NumberParameterTomo2 = 2
        self.NumberShapesTomo = 3
        self.ImageTomoName = np.zeros(self.NumberShapesTomo, dtype = object)
        self.ImageTomoName[:] = "Lenna"

        self.ParameterTomo = np.zeros((self.NumberShapesTomo,self.NumberParameterTomo1,self.NumberParameterTomo2))
        self.ParameterTomo[:,0,:] = 50
        self.ParameterTomo[0,1,:] = self.ParameterTomo[0,0,:]/2
        self.ParameterTomo[0,2:,:] = 1

        self.ImageTomo = mpimg.imread(f'{basedir}/TomoImage/{self.ImageTomoName[0]}.pgm')        
        self.ImageRotatedTomo =  np.copy(self.ImageTomo)

        self.AngleStepTomo = 1
        self.FlatImageAngleTomo = np.sum(self.ImageRotatedTomo,axis=1)
        self.SinogramTomo = Tomography.Sinogram(self.ImageTomo, angles_step = self.AngleStepTomo)
        self.ReconstructedTomo = Tomography.Reconstruction(self.SinogramTomo, angles_step = self.AngleStepTomo)
        self.ReconstructedRotatedTomo = np.copy(self.ReconstructedTomo)
        self.ReconstructionFilterName = "ramp"
        self.logImagesTomo = False