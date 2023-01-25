import numpy as np

class GUIParameters(object):
    """Class where the parameters of the GUI are stored"""
    def __init__(self):
        self.IntegralCurve = "Constant"

        self.IntegralXAxis = np.linspace(-5,5,1000)

        self.IntegralYAxis = np.zeros_like(self.IntegralXAxis)

        self.IntegralFirstParam = 1.0
        self.IntegralSecondParam = 1.0
        self.IntegralThirdParam = 1.0
        self.IntegralFourthParam = 1.0
