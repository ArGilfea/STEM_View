import numpy as np
try:
    import WaveFunctions
except:
    import QuantumMechanics.WaveFunctions as WaveFunctions

try:
    import Constants
except:
    import sys
    import os

    # getting the name of the directory
    # where the this file is present.
    current = os.path.dirname(os.path.realpath(__file__))
    
    # Getting the parent directory name
    # where the current directory is present.
    parent = os.path.dirname(current)
    
    # adding the parent directory to 
    # the sys.path.
    sys.path.append(parent)
    
    # now we can import the module in the parent
    # directory.
    import Constants

class GUIParameters(object):
    """Class where the parameters of the GUI are stored"""
    def __init__(self):
        self.mass = 1
        self.massFactorType = "electron"
        self.massFactorValue = Constants.electron_mass

        self.combinedMass = self.mass * self.massFactorValue
        

        self.WaveFunction1DType = "InfiniteSquareWell"
        self.WaveFunction1DFunction = WaveFunctions.InfiniteSquareWell

        self.EnergyLevelRange1D = 20
        self.EnergyLevelValues1D = np.zeros(self.EnergyLevelRange1D)

        self.WaveFunction1DTime = 0.0

        self.WaveFunction1DXBounds = np.array([-1.0,1.0])
        self.WaveFunction1DTBounds = np.array([0.0,1.0])

        self.WaveFunction1DLevel = 1
        self.WaveFunction1DParameters = np.array([1.0])

        self.XAxis1D, self.WaveFunction1D, self.Energy1D, self.Potential1D = self.WaveFunction1DFunction(param = self.WaveFunction1DParameters, level = self.WaveFunction1DLevel, mass = self.combinedMass, bounds = self.WaveFunction1DXBounds)

        self.TAxis1D, self.TimeWaveFunction1D = WaveFunctions.TimePart(bounds= self.WaveFunction1DTBounds, energy= self.Energy1D)

        for i in range(self.EnergyLevelRange1D):
            _, _, self.EnergyLevelValues1D[i], _ = self.WaveFunction1DFunction(param = self.WaveFunction1DParameters, level = i + 1, mass = self.combinedMass, bounds = self.WaveFunction1DXBounds,wholeComputations=False)

        self.logScale1DEnergies = False
        self.squaredWaveFunction = False