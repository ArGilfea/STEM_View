import numpy as np
try:
    import Curves
    import ParametricFunctions as ParametricFunctions
    import PolarFunctions as PolarFunctions
except:
    import Calculus.Curves as Curves
    import Calculus.ParametricFunctions as ParametricFunctions
    import Calculus.PolarFunctions as PolarFunctions

class GUIParameters(object):
    """Class where the parameters of the GUI are stored"""
    def __init__(self):
        self.DerivativesCurveName = "Cubic"
        self.DerivativesTypeName = "None"
        self.DerivativesParameters = [1.0, 0.0, 0.0, 0.0]
        self.DerivativesHValue = 1.0
        self.DerivativesCursorValue = 0.0
        self.DerivativesXAxisBounds = np.array([-5.0,5.0])
        self.DerivativesXAxis = np.linspace(self.DerivativesXAxisBounds[0],self.DerivativesXAxisBounds[1],1000)
        self.DerivativesCurve = Curves.CubicCurve
        self.DerivativesCursorValueY = self.DerivativesCurve(self.DerivativesCursorValue,self.DerivativesParameters,typeCurve = 'Normal')
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

        self.IntegralCurveName = "Cubic"

        self.IntegralParameters = [1.0, 0.0, 0.0, 0.0]

        self.IntegralBoxNumber = 2
        self.IntegralShowBoxes = False
        self.IntegralBoxType = "Left Box"
        self.IntegralBoundsBox = np.array([-1.0,1.0])

        self.IntegralXAxis = np.linspace(-5,5,1000)

        self.IntegralCurve = Curves.CubicCurve
        self.IntegralYAxis = self.IntegralCurve(self.IntegralXAxis,self.IntegralParameters)

        self.ShowVector1 = True
        self.ShowComponents1Vector1 = False
        self.ShowComponents2Vector1 = False
        self.ShowVector2 = True
        self.ShowComponents1Vector2 = False
        self.ShowComponents2Vector2 = False
        self.Vectors1 = np.array([1.0,1.0,np.sqrt(2), 45])
        self.Vectors2 = np.array([-1.0,1.0,np.sqrt(2), 135])
        self.VectorSum = False
        self.VectorSumComponent1 = False
        self.VectorSumComponent2 = False
        self.VectorSumComposition = False
        
        self.TaylorCurveName = "Cubic"
        self.TaylorParameters = [1.0, 1.0, 0.0, 0.0]
        self.TaylorDegree = 2
        self.TaylorShowAll = False
        self.TaylorCenter = 0.0
        self.TaylorXValue = 0.0
        self.TaylorBounds = np.array([-3.0,3.0])

        self.TaylorXAxis = np.linspace(self.TaylorBounds[0],self.TaylorBounds[1],1000)
        self.TaylorCurve = Curves.CubicCurve
        self.TaylorYAxis = self.TaylorCurve(self.TaylorXAxis,self.TaylorParameters)

        self.PolarCurveName = "Constant"
        self.PolarCurveFunction = Curves.FlatCurve
        
        self.PolarCurveParameters = np.array([1.0,0.0,0.0,0.0])

        self.PolarPhiBounds = np.array([0.0,2.0])
        self.PolarPhiAxis = np.linspace(self.PolarPhiBounds[0] * np.pi,self.PolarPhiBounds[1]*np.pi,1000)
        self.PolarRAxis = self.PolarCurveFunction(self.PolarPhiAxis,self.PolarCurveParameters)

        self.Parametric2DFunctionsXName = "Fresnel"
        self.Parametric2DFunctionsYName = "Fresnel"
        self.Parametric2DFunctionsX = ParametricFunctions.FresnelIntegrals
        self.Parametric2DFunctionsY = ParametricFunctions.FresnelIntegrals
        self.Parametric2DFunctionsSame = False
        self.Parametric2DFunctionsParameters = np.array([[1.0, 1.0, 0.0, 0.0],
                                                       [1.0, 1.0, 0.0, 0.0]])

        self.Parametric2DFunctionsTValue = 0.0
        self.Parametric2DFunctionsTAxisBounds = np.array([-10.0,10.0])
        self.Parametric2DFunctionsTAxis = np.linspace(self.Parametric2DFunctionsTAxisBounds[0],self.Parametric2DFunctionsTAxisBounds[1],1000)

        self.Parametric2DFunctionsXValue, _ = self.Parametric2DFunctionsX(self.Parametric2DFunctionsTValue,self.Parametric2DFunctionsParameters)
        _, self.Parametric2DFunctionsYValue = self.Parametric2DFunctionsY(self.Parametric2DFunctionsTValue,self.Parametric2DFunctionsParameters)
        self.Parametric2DFunctionsXAxis, _ = self.Parametric2DFunctionsX(self.Parametric2DFunctionsTAxis,self.Parametric2DFunctionsParameters)
        _, self.Parametric2DFunctionsYAxis = self.Parametric2DFunctionsY(self.Parametric2DFunctionsTAxis,self.Parametric2DFunctionsParameters)
