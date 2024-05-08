import numpy as np

hbar = 1.05457182 * 10**(-34)

electron_mass = 9.1093837 * 10**(-31)
proton_mass = 1.67262192 * 10**(-27)
neutron_mass = 1.674927498 * 10**(-27)

g = 9.814
G = 6.67430 * 10**-11
AstronomicalUnit = 1.495978707*10**11 #m

SolarMass = 2*10**30 #kg
EarthMass = 5.9722*10**24 #kg
LunarMass = 7.35*10**22 #kg

SolarRadius = 696340*10**3 #m
EarthRadius = 6371*10**3 #m
LunarRadius = 1737.4*10**3 #m

EarthLinearSpeed = 29784.8 #m/s

def getConstants(values):
    """Gets a string or a list of string as input and returns the relevant constant"""
    if isinstance(values,str):
        return getConstant(values)
    elif isinstance(values, (np.ndarray)):
        if len(values.shape) == 1:
            result = np.zeros(len(values))
            for i in range(result.shape[0]):
                result[i] = getConstant(values[i])
            return result
        elif len(values.shape) == 2:
            result = np.zeros_like(values)
            for i in range(result.shape[0]):
                for j in range(result.shape[1]):
                    result[i,j] = getConstant(values[i,j])
            return result            
    else:
        raise Exception(f"Invalid choice of operand for input. Must be string, or np.ndarray and {type(values)} was given.")



def getConstant(what:str):
    """Gets a string as input and returns the relevant constant"""
    if what in ["kg","m","s","m/s","m/s^2"]:
        return 1.0
    elif what == "SolarMass":
        return SolarMass
    elif what == "SolarRadius":
        return SolarRadius
    elif what == "LunarMass":
        return LunarMass
    elif what == "LunarRadius":
        return LunarRadius
    elif what == "EarthMass":
        return EarthMass
    elif what == "EarthRadius":
        return EarthRadius
    elif what == "EarthLinearSpeed":
        return EarthLinearSpeed
    elif what == "AstronomicalUnit":
        return AstronomicalUnit
    elif what == "ProtonMass":
        return proton_mass
    elif what == "Electron":
        return electron_mass
    elif what == "NeutronMass":
        return neutron_mass