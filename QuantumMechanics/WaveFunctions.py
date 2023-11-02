import numpy as np
from scipy import special
import math
try:
    import Constants
except:
    import sys
    import os
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)
    import Constants

def InfiniteSquareWell(param, level, mass, bounds, wholeComputations: bool = True):
    """Infinite Square Well in which a single particle is"""
    XAxis = np.linspace(0,param[0],1000)

    if wholeComputations:
        wavefunction = np.sqrt(2/param[0])*np.sin(level*np.pi*XAxis/param[0])
    else:
        wavefunction = 0

    energy = (level*np.pi*Constants.hbar)**2/(2*mass*param[0]**2)

    potential = 0

    return XAxis, wavefunction, energy, potential


def QuantumHarmonicOscillator(param, level, mass, bounds, wholeComputations: bool = True):
    """
    Quantum Harmonic Oscillator in which a single particle is
    param[0] is the omega
    """
    XAxis = np.linspace(bounds[0],bounds[1],1000)

    if wholeComputations:
        p_monic = special.hermite(level, monic=False)
        xi = np.sqrt(mass*param[0]/Constants.hbar)*XAxis
        wavefunction = ((mass * param[0])/(np.pi*Constants.hbar))**(1/4)/((2**level*math.factorial(level))**(1/2))*p_monic(xi) * np.exp(- xi**2/2)
    else:
        wavefunction = 0

    energy = (level + 1/2) * Constants.hbar * param[0]

    if wholeComputations:
        potential = 0.5 * mass * param[0]**2 * XAxis**2
    else:
        potential = 0

    return XAxis, wavefunction, energy, potential

def TimePart(bounds, energy):
    """Computes the Time-dependent part of the Schrodinger's equation"""
    TAxis = np.linspace(bounds[0],bounds[1],100)
    phiT = np.exp(- complex(0,1) * energy * TAxis/Constants.hbar)

    return TAxis, phiT
