import numpy as np


WindowName = {
    "En" : "Mechanics",
    "Fr" : "Mécanique"
}
Trajectory1DTab = {
    "En" : "1D Trajectory",
    "Fr" : "Trajectoire 1D"
}
Trajectory2DTab = {
    "En" : "2D Trajectory",
    "Fr" : "Trajectoire 2D"
}
ThreeBodyProblem = {
    "En" : "Three Body Problem",
    "Fr" : "Problème à Trois Corps"
}
ReadMeName = {
    "En" : "ReadMe",
    "Fr" : "Lisez-Moi"
}
############
Mass = {
    "En" : "Mass",
    "Fr" : "Masse"
}
Factor = {
    "En" : "Factor",
    "Fr" : "Facteur"
}
MassFactor = {
    "SolarMass" : {
        "En" : "Solar Mass",
        "Fr" : "Masse Solaire"
    },
    "EarthMass" : {
        "En" : "Earth Masse",
        "Fr" : "Masse Terrestre"
    },
    "LunarMass" : {
        "En" : "Lunar Mass",
        "Fr" : "Masse Lunaire"
    },
    "kg" : {
        "En" : "kg",
        "Fr" : "kg"
    }
}
PositionFactor = {
    "AstronomicalUnit" : {
        "En" : "Astronomical Unit",
        "Fr" : "Unité Astronomique"
    },
    "m" : {
        "En" : "m",
        "Fr" : "m"
    }
}
SpeedFactor = {
    "EarthLinearSpeed" : {
        "En" : "Earth Linear Speed",
        "Fr" : "Vitesse Terrestre Linéaire"
    },
    "m/s" : {
        "En" : "m/s",
        "Fr" : "m/s"
    }
}
dynamic = {
    "En" : "Dynamic",
    "Fr" : "Dynamique"
}
dynamicSpeed = {
    "En" : "Animation Speed (ms)",
    "Fr" : "Vitesse d'Animation (ms)"
}
dynamicStep = {
    "En" : "Step Size",
    "Fr" : "Saut d'Animation"
}
static = {
    "En" : "Static",
    "Fr" : "Statique"
}
object = {
    "En" : "Object",
    "Fr" : "Objet"
}
objects = {
    "En" : "Objects",
    "Fr" : "Objets"
}
collision = {
    "En" : "Collision",
    "Fr" : "Collision"
}
Abs = {
    "En" : "Abs. Values",
    "Fr" : "Val. Abs."
}
Position = {
    "En" : "Position",
    "Fr" : "Position"
}
Pos = {
    "En" : "Pos.",
    "Fr" : "Pos."
}
Velocity = {
    "En" : "Velocity",
    "Fr" : "Vélocité"
}
Speed = {
    "En" : "Speed",
    "Fr" : "Vitesse"
}
Acceleration = {
    "En" : "Acceleration",
    "Fr" : "Accélération"
}
############
trajectory1D = {
    "En" : "Trajectory",
    "Fr" : "Trajectoire"
}
############
visualBox = {
    "En" : "Visual Box",
    "Fr" : "Boîte Visuelle"
}
StepNumber = {
    "En" : "Time Steps (10^)",
    "Fr" : "Points Temporels (10^)"
}
endTime = {
    "En" : "Time Lapse",
    "Fr" : "Durée Temporelle"
}
startRun = {
    "En" : "Run",
    "Fr" : "Démarrer"
}
restartRun = {
    "En" : "Restart",
    "Fr" : "Redémarrer"
}
reframeRun = {
    "En" : "Reframe",
    "Fr" : "Recentrer"
}
startRunToolTip = {
    "En" : "Runs a new simulation with the given inputs. Might be slow!",
    "Fr" : "Démarre la prochaine simulation avec les données fournies. Le processus peut être lent!"
}
reframeRunToolTip = {
    "En" : "Reframe the current simulation, by resetting size of the viewing window.",
    "Fr" : "Recadre la simulation actuelle, en réinitialisant le champ visuel."
}
restartRunToolTip = {
    "En" : "Restart the current simulation, by resetting the dynamic counter.",
    "Fr" : "Redémarre la simulation actuelle, en remettant le compteur dynamique."
}
minLabel = {
    "En" : "Min.",
    "Fr" : "Min."
}
maxLabel = {
    "En" : "Max.",
    "Fr" : "Max."
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
def WaveFunctionEquation(curveType:str, parameters:np.ndarray, level:int, mass:float):
    if curveType == "InfiniteSquareWell":
        return f"$\sqrt{{\\frac{{2}}{{a}}}}\sin\left(\\frac{{n\pi}}{{a}}x\\right)$ = $\sqrt{{\\frac{{2}}{{{parameters[0]:.2f}}}}}\sin\left(\\frac{{{level}*\pi}}{{{parameters[0]}}}x\\right)$"
    elif curveType == "QuantumHarmonicOscillator":
        return f"0"    
