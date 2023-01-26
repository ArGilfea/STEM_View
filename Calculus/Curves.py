import  numpy as np

def FlatCurve(x,param: np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return np.ones_like(x) * param[0]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass

def LinearCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * x + param[1]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass

def QuadraticCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * x ** 2 + param[1] * x + param[2]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass

def CubicCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * x ** 3 + param[1] * x **2 + param[2] * x + param[3]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass

def ExponentialCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.exp(param[1] * x) + param[2]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass

def CosCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.cos(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass

def SinCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.sin(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass

def TanCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.tan(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass

def ArcSinCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.arcsin(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass

def ArcCosCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.arccos(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass

def ArcTanCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.arctan(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        pass