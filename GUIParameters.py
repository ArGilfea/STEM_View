import numpy as np

class GUIParameters(object):
    """Class where the parameters of the GUI are stored"""
    def __init__(self):
        self.SpecterTypePBA = "Bump"
        self.MaterialTypePBA = "None"

        self.Specter = np.loadtxt("Specters/"+self.SpecterTypePBA+".txt")

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

        self.rho = {
            "Al" : 2.6989,
            "Cu" : 8.96,
            "H" : 0,
            "H2O" : 1,
            "I" : 0,
            "O" : 0,
            "Pb" : 10.66,
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