import  numpy as np

def FlatCurve(x,param: np.ndarray):
    return np.ones_like(x) * param[0]

def LinearCurve(x,param:np.ndarray):
    return param[0] * x + param[1]

def QuadraticCurve(x,param:np.ndarray):
    return param[0] * x ** 2 + param[1] * x + param[2]

def CubicCurve(x,param:np.ndarray):
    return param[0] * x ** 3 + param[1] * x **2 + param[2] * x + param[3]

def ExponentialCurve(x,param:np.ndarray):
    return param[0] * np.exp(param[1] * x) + param[2]

def CosCurve(x,param:np.ndarray):
    return param[0] * np.cos(x * param[1] + param[2]) + param[3]

def SinCurve(x,param:np.ndarray):
    return param[0] * np.sin(x * param[1] + param[2]) + param[3]

def TanCurve(x,param:np.ndarray):
    return param[0] * np.tan(x * param[1] + param[2]) + param[3]

def ArcSinCurve(x,param:np.ndarray):
    return param[0] * np.arcsin(x * param[1] + param[2]) + param[3]

def ArcCosCurve(x,param:np.ndarray):
    return param[0] * np.arccos(x * param[1] + param[2]) + param[3]

def ArcTanCurve(x,param:np.ndarray):
    return param[0] * np.arctan(x * param[1] + param[2]) + param[3]