import numpy as np

def MirrorEquation(value:float, f:float, PorQ:str)->float:
    """Mirror Equations. Returns either p or q, depending on which one is given"""

    if PorQ == "p":
        p = value
        q = f*p/(p-f)
        return q
    elif PorQ == "q":
        q = value
        p = f*q/(q-f)
        return p
    else:
        raise Exception(f"Invalid choice of argument. Must be either p or q and {PorQ} was given.")
    
def RefractionLaw(n1,theta1,n2)->float:
    """Snell's-Descartes Law for refraction"""

    theta2 = np.arcsin(n1 * np.sin(theta1*np.pi/180)/n2)*180/np.pi
    return theta2
