import numpy as np
import scipy.special as sc

def FresnelIntegrals(t, param:np.ndarray, typeCurve:str = "Normal"):
    """Returns the Fresnel Integrals"""
    if typeCurve == "Normal":
        S, C = sc.fresnel(t)
        return [S,C]
    elif typeCurve == "Derivative":
        x = np.zeros_like(t)
        return [x, x]

def Cos(t, param:np.ndarray, typeCurve:str = "Normal"):
    """Returns the cos cos functions"""
    if typeCurve == "Normal":
        x = param[0,0] * np.cos(param[0,1]*np.pi*t + param[0,2]) + param[0,3]
        y = param[1,0] * np.cos(param[1,1]*np.pi*t + param[1,2]) + param[1,3]
        return [x, y]
    elif typeCurve == "Derivative":
        x =  - param[0,0] * np.pi*param[0,1] * np.sin(param[0,1]*np.pi*t + param[0,2])
        y =  - param[1,0] * np.pi*param[1,1] * np.sin(param[1,1]*np.pi*t + param[1,2])
        return [x, x]

def Sin(t, param:np.ndarray, typeCurve:str = "Normal"):
    """Returns the sin sin functions"""
    if typeCurve == "Normal":
        x = param[0,0] * np.sin(param[0,1]*np.pi*t + param[0,2]) + param[0,3]
        y = param[1,0] * np.sin(param[1,1]*np.pi*t + param[1,2]) + param[1,3]
        return [x, y]
    elif typeCurve == "Derivative":
        x =  param[0,0] * np.pi*param[0,1] * np.cos(param[0,1]*np.pi*t + param[0,2])
        y =  param[1,0] * np.pi*param[1,1] * np.cos(param[1,1]*np.pi*t + param[1,2])
        return [x, x]
    
def hypocycloid(t, param:np.ndarray, typeCurve:str = "Normal"):
    """Returns the hypocycloid functions"""
    if typeCurve == "Normal":
        a = param[0,0]
        b = param[1,0]
        x = (a - b) * np.cos(t) + b * np.cos((a-b)/b*t)
        y = (a - b) * np.sin(t) - b * np.sin((a-b)/b*t)
        return [x, y]
    elif typeCurve == "Derivative":
        x = np.zeros_like(t)
        return [x, x]
def astroid(t, param:np.ndarray, typeCurve:str = "Normal"):
    """Returns the hypocycloid functions"""
    if typeCurve == "Normal":
        a = param[0,0]
        x = a * (np.cos(param[0,1]*t + param[0,2]))**3 + param[0,3]
        y = a * (np.sin(param[1,1]*t + param[1,2]))**3 + param[1,3]
        return [x, y]
    elif typeCurve == "Derivative":
        x = np.zeros_like(t)
        return [x, x]
def superellipse(t, param:np.ndarray, typeCurve:str = "Normal"):
    """Returns the super ellipse functions"""
    if typeCurve == "Normal":
        a = param[0,0]
        b = param[0,1]
        x = a * np.abs(np.cos(param[0,2]*t + param[0,3]))**(2/param[0,1]) * np.sign(np.cos(param[0,2]*t + param[0,3]))
        y = b * np.abs(np.sin(param[1,2]*t + param[1,3]))**(2/param[1,1]) * np.sign(np.sin(param[1,2]*t + param[1,3]))
        return [x, y]
    elif typeCurve == "Derivative":
        x = np.zeros_like(t)
        return [x, x]
