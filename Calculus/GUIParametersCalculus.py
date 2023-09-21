import numpy as np
try:
    import Curves
except:
    import Calculus.Curves as Curves

class GUIParameters(object):
    """Class where the parameters of the GUI are stored"""
    def __init__(self):
        self.DerivativesCurveName = "Constant"
        self.DerivativesTypeName = "None"
        self.DerivativesParameters = [1.0, 0.0, 0.0, 0.0]
        self.DerivativesHValue = 1.0
        self.DerivativesCursorValue = 0.0
        self.DerivativesXAxisBounds = np.array([-5,5])
        self.DerivativesXAxis = np.linspace(self.DerivativesXAxisBounds[0],self.DerivativesXAxisBounds[1],1000)
        self.DerivativesCurve = Curves.FlatCurve
        self.DerivativesYAxis = self.DerivativesCurve(self.DerivativesXAxis,self.DerivativesParameters)
        self.DerivativesDerivedYAxis = self.DerivativesCurve(self.DerivativesXAxis,self.DerivativesParameters,typeCurve = 'Derivative')

        self.DerivativesLeft = Curves.discreteDerivative(self.DerivativesCursorValue,
                                                            h = self.DerivativesHValue,
                                                            curve = self.DerivativesCurve,
                                                            parameters= self.DerivativesParameters,
                                                            side = "left")
        self.DerivativesBoth = Curves.discreteDerivative(self.DerivativesCursorValue,
                                                            h = self.DerivativesHValue,
                                                            curve = self.DerivativesCurve,
                                                            parameters= self.DerivativesParameters,
                                                            side = "both")
        self.DerivativesRight = Curves.discreteDerivative(self.DerivativesCursorValue,
                                                            h = self.DerivativesHValue,
                                                            curve = self.DerivativesCurve,
                                                            parameters= self.DerivativesParameters,
                                                            side = "right")
        self.HValueRange = np.linspace(1e-5,np.abs(self.DerivativesXAxisBounds[1] - self.DerivativesXAxisBounds[0])/4,100)
        self.DerivativesLeftRange = np.zeros(self.HValueRange.shape[0])
        self.DerivativesRightRange = np.zeros(self.HValueRange.shape[0])
        self.DerivativesBothRange = np.zeros(self.HValueRange.shape[0])
        for i in range(self.HValueRange.shape[0]):
            self.DerivativesLeftRange[i] = Curves.discreteDerivative(self.DerivativesCursorValue,
                                                            h = self.HValueRange[i],
                                                            curve = self.DerivativesCurve,
                                                            parameters= self.DerivativesParameters,
                                                            side = "left")[6]
            self.DerivativesRightRange[i] = Curves.discreteDerivative(self.DerivativesCursorValue,
                                                            h = self.HValueRange[i],
                                                            curve = self.DerivativesCurve,
                                                            parameters= self.DerivativesParameters,
                                                            side = "right")[6]
            self.DerivativesBothRange[i] = Curves.discreteDerivative(self.DerivativesCursorValue,
                                                            h = self.HValueRange[i],
                                                            curve = self.DerivativesCurve,
                                                            parameters= self.DerivativesParameters,
                                                            side = "both")[6]   

        self.IntegralCurveName = "Constant"

        self.IntegralParameters = [1.0, 0.0, 0.0, 0.0]

        self.IntegralBoxNumber = 2
        self.IntegralShowBoxes = False
        self.IntegralBoxType = "Left Box"
        self.IntegralBoundsBox = np.array([-1.0,1.0])

        self.IntegralXAxis = np.linspace(-5,5,1000)

        self.IntegralCurve = Curves.FlatCurve
        self.IntegralYAxis = self.IntegralCurve(self.IntegralXAxis,self.IntegralParameters)
