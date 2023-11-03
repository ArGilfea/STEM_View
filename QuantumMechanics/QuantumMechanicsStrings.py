import numpy as np


WindowName = {
    "En" : "Quantum Mechanics",
    "Fr" : "Mécanique Quantique"
}
WaveFunction1DTab = {
    "En" : "1D WaveFunction",
    "Fr" : "Fonction d'Ondes 1D"
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
MassType = {
    "electron" : {
        "En" : "Electron",
        "Fr" : "Électron"
    },
    "proton" : {
        "En" : "Proton",
        "Fr" : "Proton"
    },
    "neutron" : {
        "En" : "Neutron",
        "Fr" : "Neutron"
    },
    "kg" : {
        "En" : "kg",
        "Fr" : "kg"
    }
}
Parameters = {
    "En" : "Parameters",
    "Fr" : "Paramètres"
}
Bounds = {
    "En" : "Bounds",
    "Fr" : "Bornes"
}
EnergyLevel = {
    "En" : "Energy Level",
    "Fr" : "Niveau d'Énergie"
}
############
WaveFunctionGraphTitle = {
    "En" : "WaveFunction",
    "Fr" : "Fonction d'Ondes"
}
EnergyLevelGraphTitle = {
    "En" : "Energy Levels",
    "Fr" : "Niveaux d'Énergie"
}
WaveFunction1DFunctions = {
    "InfiniteSquareWell" : {
        "En" : "Infinite Square Well",
        "Fr" : "Puit de Potentiel Infini"
    },
    "QuantumHarmonicOscillator" : {
        "En" : "Quantum Harmonic Oscillator",
        "Fr" : "Oscillateur Harmonique Quantique"
    }
}
LogEnergies = {
    "En" : "Log Energies",
    "Fr" : "Log des Énergies"
}
SquaredWaveFunction = {
    "En" : "Squared Wave Function",
    "Fr" : "Fonction d'Ondes au Carré"
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

def EnergyLevelEquation(curveType:str, parameters:np.ndarray, level:int, mass:float, energyValue:float):
    if curveType == "InfiniteSquareWell":
        return f"$\\frac{{n^2 \pi^2 \hbar^2}}{{2 * m a^2}}$ = $\\frac{{{level**2} * \pi^2 \hbar^2}}{{2 * ({mass:.2e}) * {(parameters[0]**2):.2f}}}$ = {energyValue:.2e}"
    elif curveType == "QuantumHarmonicOscillator":
        return f"$\left(n+\\frac{{1}}{{2}}\\right) \hbar \omega$ = $\left({level}+\\frac{{1}}{{2}}\\right) \hbar * {parameters[0]}$ = {energyValue:.2e}"

def TimeEquation(energy):
    return f"$e^{{-iE_n/\hbar}}$ = $e^{{-i({energy:.2e})/\hbar}}$"
