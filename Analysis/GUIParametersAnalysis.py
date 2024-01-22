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

        self.numberFilter = 2
        self.numberParameters = 5
        self.numberParameters2 = 3

        self.dxFourier1D = 0.01
        self.CurveRangeFourier1D = np.array([-5.0,5.0])
        self.XAxisFourier1D = np.arange(self.CurveRangeFourier1D[0],self.CurveRangeFourier1D[1],self.dxFourier1D)
        self.RangeFourierFourier1D = np.arange(-1/(2*self.dxFourier1D),1/(2*self.dxFourier1D),1/(self.dxFourier1D*self.XAxisFourier1D.shape[0]))

        self.CurveTypeFourier1D = np.zeros((self.numberFilter,self.numberParameters),dtype = object)
        self.fullRangeFourier1D = np.zeros((self.numberFilter, self.numberParameters), dtype = bool)
        self.directFourierCurve1D = np.zeros((self.numberFilter),dtype = bool)
        self.CurveParametersFourier1D = np.zeros((self.numberFilter,self.numberParameters,self.numberParameters2))

        self.BaseCurveFourier1D = np.zeros(self.numberFilter, dtype = object)
        self.FourierCurveFourier1DAbs = np.zeros(self.numberFilter, dtype = object)
        self.FourierCurveFourier1D = np.zeros(self.numberFilter, dtype = object)

        for i in range(self.numberFilter):
            for k in range(self.numberParameters):
                self.CurveTypeFourier1D[i,k] = "Low Pass Flat"
                self.fullRangeFourier1D[i,k] = False
            self.CurveParametersFourier1D[i,0,1] = 1.0
            self.CurveParametersFourier1D[i,0,2] = 1.0

            self.directFourierCurve1D[i] = False

            self.BaseCurveFourier1D[i] = Fourier1D.create1DFunctions(self.XAxisFourier1D,self.CurveParametersFourier1D[i,:,:],self.CurveTypeFourier1D[i,:],self.fullRangeFourier1D[i,:])
            self.FourierCurveFourier1DAbs[i], self.FourierCurveFourier1D[i] = Fourier1D.FourierTransform1D(self.BaseCurveFourier1D[i])
        
        self.ConvolutionFouried1DFourier = np.ones_like(self.FourierCurveFourier1DAbs[0])

        for i in range(self.numberFilter):
            if i == 0:
                self.Convolution1DFourier = np.copy(self.BaseCurveFourier1D[i])
            else:
                self.Convolution1DFourier = np.convolve(self.Convolution1DFourier,self.BaseCurveFourier1D[i],mode = 'same') * (self.XAxisFourier1D[1]-self.XAxisFourier1D[0])
            self.ConvolutionFouried1DFourier *= self.FourierCurveFourier1DAbs[i]


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