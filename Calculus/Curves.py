import  numpy as np

def FlatCurve(x,param: np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return np.ones_like(x) * param[0]
    elif typeCurve == 'Derivative':
        return np.zeros_like(x)
    elif typeCurve == 'Integral':
        return param[0] * x

def LinearCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * x + param[1]
    elif typeCurve == 'Derivative':
        return np.ones_like(x) * param[0]
    elif typeCurve == 'Integral':
        return param[0]/2 * x ** 2 + param[1] * x + param[2]

def QuadraticCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * x ** 2 + param[1] * x + param[2]
    elif typeCurve == 'Derivative':
        return 2 * param[0] * x + param[1]
    elif typeCurve == 'Integral':
        return param[0]/3 * x ** 3 + param[1]/2 * x **2 + param[2] * x + param[3]

def CubicCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * x ** 3 + param[1] * x **2 + param[2] * x + param[3]
    elif typeCurve == 'Derivative':
        return 3 * param[0] * x ** 2 + 2 * param[1] * x + param[2]
    elif typeCurve == 'Integral':
        return param[0]/4 * x ** 4 + param[1]/3 * x **3 + param[2]/2 * x ** 2 + param[3] * x

def ExponentialCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.exp(param[1] * x) + param[2]
    elif typeCurve == 'Derivative':
        return param[0] * param[1] * np.exp(param[1] * x)
    elif typeCurve == 'Integral':
        try: return param[0] / param[1] * np.exp(param[1] * x) + param[2] * x
        except: return param[0] / (param[1] + 1e-10) * np.exp(param[1] * x) + param[2] * x

def CosCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.cos(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        return - param[0] * param[1] * np.sin(x * param[1] + param[2])
    elif typeCurve == 'Integral':
        try: return param[0] / param[1] * np.sin(x * param[1] + param[2]) + param[3] * x
        except: return param[0] / (param[1] + 1e-10) * np.sin(x * param[1] + param[2]) + param[3] * x

def SinCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.sin(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        return param[0] * param[1] * np.cos(x * param[1] + param[2])
    elif typeCurve == 'Integral':
        try: return - param[0] / param[1] * np.cos(x * param[1] + param[2]) + param[3] * x
        except: return - param[0] / (param[1] + 1e-10) * np.cos(x * param[1] + param[2]) + param[3] * x

def TanCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.tan(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        return param[0] * param[1] * (np.sec(x * param[1] + param[2])) ** 2
    elif typeCurve == 'Integral':
        try: return - param[0] * np.log(np.cos(x * param[1] + param[2]))/param[1] + param[3] * x
        except: return - param[0] * np.log(np.cos(x * param[1] + param[2]))/(param[1]+1e-10) + param[3] * x

def ArcSinCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.arcsin(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        return np.zeros_like(x)
def ArcCosCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.arccos(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        return np.zeros_like(x)

def ArcTanCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.arctan(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        pass
    elif typeCurve == 'Integral':
        return np.zeros_like(x)
