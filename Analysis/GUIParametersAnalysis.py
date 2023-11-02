import numpy as np
import matplotlib.image as mpimg
import os
try:
    import Fourier1D
    import Filters
except:
    import Analysis.Fourier1D as Fourier1D
    import Analysis.Filters as Filters
import cmath

class GUIParametersAnalysis(object):
    """Class where the parameters of the GUI are stored"""
    def __init__(self):
        basedir = os.path.dirname(__file__)
        self.CurveTypeFourier1D = "Hamming"
        self.CurveParametersFourier1D = np.array([1.0,1.0, 0.25, 0.3, 0.1, 0.7, 1.0, 0.1])
        self.dxFourier1D = 0.01
        self.CurveRangeFourier1D = np.array([-5.0,5.0])
        self.XAxisFourier1D = np.arange(self.CurveRangeFourier1D[0],self.CurveRangeFourier1D[1],self.dxFourier1D)
        self.fullRangeFourier1D = False

        self.RangeFourierFourier1D = np.arange(-1/(2*self.dxFourier1D),1/(2*self.dxFourier1D),1/(self.dxFourier1D*self.XAxisFourier1D.shape[0]))

        self.BaseCurveFourier1D = Fourier1D.create1DFunctions(self.XAxisFourier1D,self.CurveParametersFourier1D,self.CurveTypeFourier1D,self.fullRangeFourier1D)
        self.FourierCurveFourier1DAbs, self.FourierCurveFourier1D = Fourier1D.FourierTransform1D(self.BaseCurveFourier1D)


        self.ImageFiltersName = "Phantom"
        self.ImageFilters = mpimg.imread(f'{basedir}/AnalysisImage/{self.ImageFiltersName}.pgm')

        self.FilterFiltersName = "Hamming"
        self.ParametersFilters = np.array([30,0.5435])
        self.fullRangeFilters = False
        self.logViewFourier = False
        self.FilterFilters = Filters.createFilters(self.ImageFilters,self.ParametersFilters,
                                                    self.FilterFiltersName,self.fullRangeFilters)
        self.FilterFourierAbsFilters, self.FilterFourierFilters = Filters.FourierTransform(self.FilterFilters)
        self.ImageFourierAbsFilters, self.ImageFourierFilters = Filters.FourierTransform(self.ImageFilters)
        self.ImageFourierFilteredAbsFilters,  self.ImageFourierFilteredFilters= Filters.FourierConvolution(self.FilterFourierFilters,self.ImageFourierFilters)

        self.ImageConvolvedAbsFilters, self.ImageConvolvedFilters = Filters.InverseFourierTransform(self.ImageFourierFilteredFilters)

        self.ComplexNumber1 = 0 + 0j
        self.ComplexNumber2 = 0 + 0j
        self.ComplexNumberOperation = "+"
        self.ComplexNumberResult = self.ComplexNumber1 + self.ComplexNumber2
        self.ComlexAlphaFactor = np.linspace(-5,5,300)
        self.ComplexNumberLine = self.ComplexNumber1 ** (self.ComlexAlphaFactor*self.ComplexNumber2)
        self.ComplexNumberClicker = "1"