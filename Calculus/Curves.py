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

def ExponentialPowerCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.exp(param[1] * x ** param[2]) + param[3]
    elif typeCurve == 'Derivative':
        try: return param[0] * param[1] * param[2] * x ** (param[2] - 1) * np.exp(param[1] * x ** param[2])
        except: return param[0] * param[1] * param[2] * (x + 1e-10) ** (param[2] - 1) * np.exp(param[1] * (x+1e-10) ** param[2])
    elif typeCurve == 'Integral':
        return np.zeros_like(x)

def LogarithmicCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.log(param[1] * x + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        try: return param[0] * param[1]/(param[1] * x + param[2]) 
        except: return np.zeros_like(x)
    elif typeCurve == 'Integral':
        try: return param[0]/param[1] * (param[1] * x + param[2]) * np.log(param[1] * x + param[2]) - x + param[3] * x
        except: return np.zeros_like(x)


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
        return np.zeros_like(x)
    elif typeCurve == 'Integral':
        return np.zeros_like(x)
def ArcCosCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.arccos(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        return np.zeros_like(x)
    elif typeCurve == 'Integral':
        return np.zeros_like(x)

def ArcTanCurve(x,param:np.ndarray, typeCurve = 'Normal'):
    if typeCurve == 'Normal':
        return param[0] * np.arctan(x * param[1] + param[2]) + param[3]
    elif typeCurve == 'Derivative':
        return param[0] * param[1]/(1 + (x * param[1] + param[2])**2)
    elif typeCurve == 'Integral':
        return np.zeros_like(x)

def discreteDerivative(x_0,h, curve,parameters: np.ndarray, side:str = 'both',imageRange = [0,0]):
    y_0 = curve(x_0,parameters)
    if side == 'both':
        x_2 = x_0 + h/2
        x_1 = x_0 - h/2
        y_2 = curve(x_2,parameters)
        y_1 = curve(x_1,parameters)
    elif side == 'left':
        x_2 = x_0
        x_1 = x_0 - h
        y_2 = curve(x_2,parameters)
        y_1 = curve(x_1,parameters)
    elif side == 'right':
        x_2 = x_0 + h
        x_1 = x_0
        y_2 = curve(x_2,parameters)
        y_1 = curve(x_1,parameters)
    slope = (y_2-y_1)/h
    b = y_2 - slope * x_2
    if imageRange[0] > imageRange[1]:
        if x_1 < 0: 
            p1 = 1.1 * x_1
        else:
            p1 = 0.9 * x_1
        if x_2 < 0: 
            p2 = 0.9 * x_2
        else:
            p2 = 1.1 * x_2
    else:
        if imageRange[0] < 0: 
            p1 = 1.1 * imageRange[0]
        else:
            p1 = 0.8 * imageRange[0]
        if imageRange[1] < 0: 
            p2 = 0.8 * imageRange[1]
        else:
            p2 = 1.1 * imageRange[1]        
    new_x = np.linspace(p1,p2,100)
    return [new_x, new_x * slope + b, x_1, x_2, y_1, y_2, slope]