import numpy as np
try:
    import Curves
except:
    import Calculus.Curves as Curves

class GUIParameters(object):
    """Class where the parameters of the GUI are stored"""
    def __init__(self):
        self.IntegralCurveName = "Constant"

        self.IntegralParameters = [1.0, 0.0, 0.0, 0.0]

        self.IntegralBoxNumber = 2
        self.IntegralShowBoxes = False
        self.IntegralBoxType = "Left Box"
        self.IntegralBoundsBox = np.array([-1.0,1.0])

        self.IntegralXAxis = np.linspace(-5,5,1000)

        self.IntegralCurve = Curves.FlatCurve
        self.IntegralYAxis = self.IntegralCurve(self.IntegralXAxis,self.IntegralParameters)
