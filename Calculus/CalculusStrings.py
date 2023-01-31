import numpy as np
try:
    import Curves
except:
    import Calculus.Curves as Curves

def CurveEquation(curveType:str, parameters:np.ndarray):
    if curveType == "Constant":
        return f"{parameters[0]}"
    elif curveType == "Line":
        return f'{parameters[0]}$x$ + {parameters[1]}'
    elif curveType == "Quadratic":
        return f'{parameters[0]}$x^2$ + {parameters[1]}$x$ + {parameters[2]}'
    elif curveType == "Cubic":
        return f'{parameters[0]}$x^3$ + {parameters[1]}$x^2$ + {parameters[2]}$x$ + {parameters[3]}'
    elif curveType == "Exponential":
        return f'{parameters[0]}$e^{{{parameters[1]}x}}$ + {parameters[2]}'
    elif curveType == "Sin":
        return f'{parameters[0]}sin({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
    elif curveType == "Cos":
        return f'{parameters[0]}cos({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
    elif curveType == "Tan":
        return f'{parameters[0]}tan({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
    elif curveType == "ArcSin":
        return f'{parameters[0]}arcsin({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
    elif curveType == "ArcCos":
        return f'{parameters[0]}arccos({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
    elif curveType == "ArcTan":
        return f'{parameters[0]}arctan({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'

    else:
        return ""
