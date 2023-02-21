import numpy as np
try:
    import Curves
except:
    import Calculus.Curves as Curves

WindowName = {
    "En" : "Calculus",
    "Fr" : "Calcul"
}
DerivativeTab = {
    "En" : "Derivatives",
    "Fr" : "Dérivées"
}
IntegralTab = {
    "En" : "Integrals",
    "Fr" : "Intégrales"
}
ReadMeName = {
    "En" : "ReadMe",
    "Fr" : "Lisez-Moi"
}
############
hDerivatives = {
    "En" : "h",
    "Fr" : "h"
}
SlopeDerivatives = {
    "En" : "Slope",
    "Fr" : "Pente"
}
SlopeTitleDerivatives = {
    "En" : "Derivative depending on the side and size of step",
    "Fr" : "Dérivée en fonction de la distance"
}
ParametersLabel = {
    "En" : "Parameters",
    "Fr" : "Paramètres"
}
ButtonChoiceFunction = {
    "Constant" : {
        "En" : "Constant",
        "Fr" : "Constante"
    },
    "Line" : {
        "En" : "Line",
        "Fr" : "Ligne"
    },
    "Quadratic" : {
        "En" : "Quadratic",
        "Fr" : "Quadratique"
    },
    "Cubic" : {
        "En" : "Cubic",
        "Fr" : "Cubique"
    },
    "Exponential" : {
        "En" : "Exponential",
        "Fr" : "Exponentielle"
    },
    "Exp. Power" : {
        "En" : "Exp. Power",
        "Fr" : "Puissance Exp."
    },
    "Sin" : {
        "En" : "Sin",
        "Fr" : "Sin"
    },
    "Cos" : {
        "En" : "Cos",
        "Fr" : "Cos"
    },
    "Tan" : {
        "En" : "Tan",
        "Fr" : "Tan"
    },
    "ArcSin" : {
        "En" : "ArcSin",
        "Fr" : "ArcSin"
    },
    "ArcCos" : {
        "En" : "ArcCos",
        "Fr" : "ArcCos"
    },
    "ArcTan" : {
        "En" : "ArcTan",
        "Fr" : "ArcTan"
    }
}
BoundsLabel = {
    "En" : "Bounds",
    "Fr" : "Bornes"
}
FunctionLabel = {
    "En" : "Function",
    "Fr" : "Fonction"
}
DerivativeLabel = {
    "En" : "Derivative",
    "Fr" : "Dérivée"
}
SideDerivativesFunction = {
    "None" : {
        "En" : "None",
        "Fr" : "Aucun"
    },
    "Middle" : {
        "En" : "Middle",
        "Fr" : "Centrée"
    },
    "Left" : {
        "En" : "Left",
        "Fr" : "Gauche"
    },
    "Right" : {
        "En" : "Right",
        "Fr" : "Droite"
    },
    "Exact" : {
        "En" : "Exact",
        "Fr" : "Exacte"
    },
    "All" : {
        "En" : "All",
        "Fr" : "Toutes"
    }
}
############
BoxesLabel = {
    "En" : "Boxes",
    "Fr" : "Boîtes"
}
############
ExitLabel = {
    "En" : "Exit",
    "Fr" : "Quitter"
}
ExitButtonTooltip = {
    "En" : "Closes the GUI and its dependencies",
    "Fr" : "Ferme le GUI"
}
############
def CurveEquation(curveType:str, parameters:np.ndarray,operator : str = "None"):
    if curveType == "Constant":
        if operator == "None":
            return f"{parameters[0]}"
        elif operator == "Derivative":
            return "0"
    elif curveType == "Line":
        if operator == "None":
            return f'{parameters[0]}$x$ + {parameters[1]}'
        elif operator == "Derivative":
            return f'{parameters[0]:.2g}'
    elif curveType == "Quadratic":
        if operator == "None":
            return f'{parameters[0]}$x^2$ + {parameters[1]}$x$ + {parameters[2]}'
        elif operator == "Derivative":
            return f'{2*parameters[0]:.2g}$x$ + {parameters[1]}'
    elif curveType == "Cubic":
        if operator == "None":
            return f'{parameters[0]}$x^3$ + {parameters[1]}$x^2$ + {parameters[2]}$x$ + {parameters[3]}'
        elif operator == "Derivative":
            return f'{3*parameters[0]:.2g}$x$ + {2*parameters[1]:.2g}$x$ + {parameters[2]}'
    elif curveType == "Exponential":
        if operator == "None":
            return f'{parameters[0]}$e^{{{parameters[1]}x}}$ + {parameters[2]}'
        elif operator == "Derivative":
            return f'{parameters[0] * parameters[1]:.2g}$e^{{{parameters[1]}x}}$'
    elif curveType == "Exp. Power":
        if operator == "None":
            return f'{parameters[0]}$e^{{{parameters[1]}x ^{{{parameters[2]}}}}}$ + {parameters[3]}'
        elif operator == "Derivative":
            return "0"
    elif curveType == "Sin":
        if operator == "None":
            return f'{parameters[0]}sin({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return f'{parameters[0] * parameters[1]:.2g}cos({parameters[1]}$x$+{parameters[2]})'
    elif curveType == "Cos":
        if operator == "None":
            return f'{parameters[0]}cos({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return f'{-parameters[0]*parameters[1]:.2g}sin({parameters[1]}$x$+{parameters[2]})'
    elif curveType == "Tan":
        if operator == "None":
            return f'{parameters[0]}tan({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return f'{parameters[0] * parameters[1]:.2g}tan$^2$({parameters[1]}$x$+{parameters[2]})'
    elif curveType == "ArcSin":
        if operator == "None":
            return f'{parameters[0]}arcsin({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return "0"
    elif curveType == "ArcCos":
        if operator == "None":
            return f'{parameters[0]}arccos({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return "0"
    elif curveType == "ArcTan":
        if operator == "None":
            return f'{parameters[0]}arctan({parameters[1]}$x$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return f'{parameters[0] * parameters[1]:.2g}$(1 + ({parameters[1]}$x$+{parameters[2]})^2)^{{-1}}$'

    else:
        return ""
