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
VectorTab = {
    "En" : "Vectors",
    "Fr" : "Vecteurs"
}
TaylorTab = {
    "En" : "Taylor Series",
    "Fr" : "Séries de Taylor"
}
PolarFunctionsTab = {
    "En" : "Polar Functions",
    "Fr" : "Fonctions Polaires"
}
Parametric2DFunctionsTab = {
    "En" : "Parametric 2D Functions",
    "Fr" : "Fonctions Paramétriques 2D"
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
    "Logarithmic" : {
        "En" : "Logarithmic",
        "Fr" : "Logarithmique"
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
    },
    "Sinc" : {
        "En" : "Sinc",
        "Fr" : "Sinc"
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
CenterLabel = {
    "En" : "Center",
    "Fr" : "Center"
}
TrapezoidLabel = {
    "En" : "Trapezoid",
    "Fr" : "Trapézoïde"
}
############
BoxesLabel = {
    "En" : "Boxes",
    "Fr" : "Boîtes"
}
BoxeNumberLabel = {
    "En" : "Box Number",
    "Fr" : "Nombre de Boîtes"
}
TotalAreaLabel = {
    "En" : "Total Area",
    "Fr" : "Aire Totale"
}
MeasureAreaTitle = {
    "En" : "Measured Area by Method of Integration and Number of Boxes",
    "Fr" : "Aire Mesurée pour Chaque Méthode d'Intégration et Nombre de Boîtes"
}
FunctionIntegralLabel = {
    "En" : "Integral Function of",
    "Fr" : "Intégrale de la fonction"
}

############
Vector = {
    "En" : "Vector",
    "Fr" : "Vecteur"
}
Cartesian = {
    "En" : "Cartesian",
    "Fr" : "Cartésiennes"
}
Polar = {
    "En" : "Polar",
    "Fr" : "Polaires"
}
VectorAddition = {
    "En" : "Addition",
    "Fr" : "Addition"
}
Components = {
    "En" : "Components",
    "Fr" : "Composantes"
}
############
CenterTaylor = {
    "En" : "Center",
    "Fr" : "Centre"
}
PointOfInterestTaylor = {
    "En" : "Point of Interest",
    "Fr" : "Point d'Intérêt"
}
DegreeTaylor = {
    "En" : "Degree",
    "Fr" : "Degré"
}
DegreeAllTaylor = {
    "En" : "All smaller degrees",
    "Fr" : "Tous les degrés plus bas"
}
GraphTitleTaylor = {
    "En" : "Function and its Taylor Approximation of degree ",
    "Fr" : "Fonction et son approximation de Taylor de degrée "
}
GraphTitleTaylor2 = {
    "En" : "with center at a = ",
    "Fr" : "avec comme centre a = "
}
DifferenceGraphTitleTaylor = {
    "En" : "Difference between the function and the Taylor polynomial\n"+r"f(x) - T$_n$",
    "Fr" : "Différence entre la fonction et son polynôme de Taylor\n"+r"f(x) - T$_n$"
}
ConvergenceGraphTitleTaylor = {
    "En" : "Convergence of the function and the Taylor polynomial\n for x = ",
    "Fr" : "Convergence de la fonction et son polynôme de Taylor\npour x = "
}
############
ParametricFunctionGraphTitle = {
    "En" : "Parametric 2D Function",
    "Fr" : "Fonction Paramétrique"
}
Parametric2DFunctionTValueLabel = {
    "En" : "Value of t",
    "Fr" : "Valeur de t"
}
Parametric2DFunctionNames = {
    "Fresnel" : {
        "En" : "Fresnel",
        "Fr" : "Fresnel"
    },
    "cos" : {
        "En" : "Cos",
        "Fr" : "Cos"
    },
    "sin" : {
        "En" : "Sin",
        "Fr" : "Sin"
    },
    "hypocycloid" : {
        "En" : "Hypocycloid",
        "Fr" : "Hypocycloïde"
    },
    "astroid" : {
        "En" : "Astroid",
        "Fr" : "Astroïde"
    },
    "superellipse" : {
        "En" : "Super Ellipse",
        "Fr" : "Super Ellipse"
    }
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
def CurveEquation(curveType:str, parameters:np.ndarray,operator : str = "None",polar:bool = False):
    if polar == True:
        symbol = f"\phi"
    else:
        symbol = "x"
    if curveType == "Constant":
        if operator == "None":
            return f"{parameters[0]}"
        elif operator == "Derivative":
            return "0"
    elif curveType == "Line":
        if operator == "None":
            return f'{parameters[0]}${symbol}$ + {parameters[1]}'
        elif operator == "Derivative":
            return f'{parameters[0]:.2g}'
    elif curveType == "Quadratic":
        if operator == "None":
            return f'{parameters[0]}${symbol}^2$ + {parameters[1]}${symbol}$ + {parameters[2]}'
        elif operator == "Derivative":
            return f'{2*parameters[0]:.2g}${symbol}$ + {parameters[1]}'
    elif curveType == "Cubic":
        if operator == "None":
            return f'{parameters[0]}${symbol}^3$ + {parameters[1]}${symbol}^2$ + {parameters[2]}${symbol}$ + {parameters[3]}'
        elif operator == "Derivative":
            return f'{3*parameters[0]:.2g}${symbol}$ + {2*parameters[1]:.2g}${symbol}$ + {parameters[2]}'
    elif curveType == "Exponential":
        if operator == "None":
            return f'{parameters[0]}$e^{{{parameters[1]}{symbol}}}$ + {parameters[2]}'
        elif operator == "Derivative":
            return f'{parameters[0] * parameters[1]:.2g}$e^{{{parameters[1]}{symbol}}}$'
    elif curveType == "Exp. Power":
        if operator == "None":
            return f'{parameters[0]}$e^{{{parameters[1]}{symbol} ^{{{parameters[2]}}}}}$ + {parameters[3]}'
        elif operator == "Derivative":
            return "0"
    elif curveType == "Logarithmic":
        if operator == "None":
            return f'{parameters[0]}ln({parameters[1]}{symbol} + {parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return f"({parameters[0] * parameters[1]})/({parameters[1]}{symbol} + {parameters[2]})"
    elif curveType == "Sin":
        if operator == "None":
            return f'{parameters[0]}sin({parameters[1]}${symbol}$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return f'{parameters[0] * parameters[1]:.2g}cos({parameters[1]}${symbol}$+{parameters[2]})'
    elif curveType == "Cos":
        if operator == "None":
            return f'{parameters[0]}cos({parameters[1]}${symbol}$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return f'{-parameters[0]*parameters[1]:.2g}sin({parameters[1]}${symbol}$+{parameters[2]})'
    elif curveType == "Tan":
        if operator == "None":
            return f'{parameters[0]}tan({parameters[1]}${symbol}$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return f'{parameters[0] * parameters[1]:.2g}tan$^2$({parameters[1]}${symbol}$+{parameters[2]})'
    elif curveType == "ArcSin":
        if operator == "None":
            return f'{parameters[0]}arcsin({parameters[1]}${symbol}$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return "0"
    elif curveType == "ArcCos":
        if operator == "None":
            return f'{parameters[0]}arccos({parameters[1]}${symbol}$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return "0"
    elif curveType == "ArcTan":
        if operator == "None":
            return f'{parameters[0]}arctan({parameters[1]}${symbol}$+{parameters[2]}) + {parameters[3]}'
        elif operator == "Derivative":
            return f'{parameters[0] * parameters[1]:.2g}$(1 + ({parameters[1]}${symbol}$+{parameters[2]})^2)^{{-1}}$'
    elif curveType == "Sinc":
        if operator == "None":
            return f'${parameters[0]}\\frac{{sin({parameters[1]} {symbol})}}{{{parameters[2]} {symbol}}} + {parameters[3]}$'
        elif operator == "Derivative":
            return '0'
        
    else:
        return ""

def Parametric2DFunctionEquation(curveType:str, parameters:np.ndarray,operator : str = "None"):
    if curveType == "Fresnel":
        if operator == "None":
            x = f'$\int_0^t \sin\left(\\frac{{1}}{{2}}\pi t^2\\right)$dt'
            y = f'$\int_0^t \cos\left(\\frac{{1}}{{2}}\pi t^2\\right)$dt'
            return [x,y]
        elif operator == "Derivative":
            return ["-","-"]
            x = f'$\int_0^t e^{{{parameters[1]}x}}$'
    elif curveType == "cos":
        if operator == "None":
            x = f'{parameters[0,0]:.2f} cos ({parameters[0,1]:.2f}$\pi$t + {parameters[0,2]:.2f}) + {parameters[0,3]:.2f}'
            y = f'{parameters[1,0]:.2f} cos ({parameters[1,1]:.2f}$\pi$t + {parameters[1,2]:.2f}) + {parameters[1,3]:.2f}'
            return [x,y]
        elif operator == "Derivative":
            x = f'{(- parameters[0,0] * parameters[0,1]):.2f} $\pi$ sin ({parameters[0,1]:.2f}$\pi$t + {parameters[0,2]:.2f})'
            y = f'{(- parameters[1,0] * parameters[1,1]):.2f} $\pi$ sin ({parameters[1,1]:.2f}$\pi$t + {parameters[1,2]:.2f})'
            return [x,y]
    elif curveType == "sin":
        if operator == "None":
            x = f'{parameters[0,0]:.2f} sin ({parameters[0,1]:.2f}$\pi$t + {parameters[0,2]:.2f}) + {parameters[0,3]:.2f}'
            y = f'{parameters[1,0]:.2f} sin ({parameters[1,1]:.2f}$\pi$t + {parameters[1,2]:.2f}) + {parameters[1,3]:.2f}'
            return [x,y]
        elif operator == "Derivative":
            x = f'{( parameters[0,0] * parameters[0,1]):.2f} $\pi$ cos ({parameters[0,1]:.2f}$\pi$t + {parameters[0,2]:.2f})'
            y = f'{( parameters[1,0] * parameters[1,1]):.2f} $\pi$ cos ({parameters[1,1]:.2f}$\pi$t + {parameters[1,2]:.2f})'
            return [x,y]
    elif curveType == "hypocycloid":
        if operator == "None":
            x = f"({(parameters[0,0]):.2f} - {(parameters[1,0]):.2f}) cos (t) + {(parameters[1,0]):.2f} cos$\left(\\frac{{{(parameters[0,0]):.2f}-{(parameters[1,0]):.2f}}}{{{(parameters[1,0]):.2f}}}t\\right)$"
            y = f"({(parameters[0,0]):.2f} - {(parameters[1,0]):.2f}) sin (t) - {(parameters[1,0]):.2f} sin$\left(\\frac{{{(parameters[0,0]):.2f}-{(parameters[1,0]):.2f}}}{{{(parameters[1,0]):.2f}}}t\\right)$"
            return [x,y]
        elif operator == "Derivative":
            return ["-","-"]
    elif curveType == "astroid":
        if operator == "None":
            x = f"{parameters[0,0]:.2f} cos$^3$({parameters[0,1]:.2f}t + {parameters[0,2]:.2f}) + {parameters[0,3]:.2f}"
            y = f"{parameters[0,0]:.2f} sin$^3$({parameters[1,1]:.2f}t + {parameters[1,2]:.2f}) + {parameters[1,3]:.2f}"
            return [x,y]
        elif operator == "Derivative":
            return ["-","-"]
    elif curveType == "superellipse":
        if operator == "None":
            x = f"{parameters[0,0]:.2f} cos$^{{2/{parameters[0,1]}}}$({parameters[0,2]:.2f}t + {parameters[0,3]:.2f})"
            y = f"{parameters[1,0]:.2f} sin$^{{2/{parameters[1,1]}}}$({parameters[1,2]:.2f}t + {parameters[1,3]:.2f})"
            return [x,y]
        elif operator == "Derivative":
            return ["-","-"]
