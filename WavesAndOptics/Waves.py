import numpy as np

def SimpleHarmonicMotion(TimeLapse:np.ndarray,parameters:np.ndarray,parametersPhysical:np.ndarray,TypeMotion: str = "sin",TypeSHM: str = 'SHM') -> np.ndarray:
    """Creates an Oscillatory Motion, according to the given parameters"""
    Position = np.zeros(TimeLapse.shape[0])
    Speed = np.zeros(TimeLapse.shape[0])
    Acceleration = np.zeros(TimeLapse.shape[0])
    if TypeSHM == "SHM":
        if TypeMotion == "sin":
            Position = parameters[0] * np.sin(parameters[1]*TimeLapse + parameters[2])
            Speed = parameters[0] * parameters[1] * np.cos(parameters[1]*TimeLapse + parameters[2])
            Acceleration = - parameters[0] * parameters[1] ** 2 * np.sin(parameters[1]*TimeLapse + parameters[2])
        elif TypeMotion == "cos":
            Position = parameters[0] * np.cos(parameters[1]*TimeLapse + parameters[2])
            Speed = - parameters[0] * parameters[1] * np.sin(parameters[1]*TimeLapse + parameters[2])
            Acceleration = - parameters[0] * parameters[1] ** 2 * np.cos(parameters[1]*TimeLapse + parameters[2])
        else:
            raise Exception("Invalid Motion Type ",TypeMotion)
    elif TypeSHM == "Damped":
        if TypeMotion == "sin":
            Position = parameters[0] * np.exp(-parameters[3]*TimeLapse/(2*parametersPhysical[0])) * np.sin(parameters[4]*TimeLapse + parameters[2])
            Speed = parameters[0] * (-parameters[3]/(2*parametersPhysical[0])* np.exp(-parameters[3]*TimeLapse/(2*parametersPhysical[0]))* np.sin(parameters[4]*TimeLapse + parameters[2]) + parameters[4] * np.exp(-parameters[3]*TimeLapse/(2*parametersPhysical[0]))* np.cos(parameters[4]*TimeLapse + parameters[2]))
            Acceleration = - parametersPhysical[1]/parametersPhysical[0] * Position - parameters[3]/parametersPhysical[0] * Speed
        elif TypeMotion == "cos":
            Position = parameters[0] * np.exp(-parameters[3]*TimeLapse/(2*parametersPhysical[0])) * np.cos(parameters[4]*TimeLapse + parameters[2])
            Speed = parameters[0] * (-parameters[3]/(2*parametersPhysical[0])* np.exp(-parameters[3]*TimeLapse/(2*parametersPhysical[0]))* np.cos(parameters[4]*TimeLapse + parameters[2]) - parameters[4] * np.exp(-parameters[3]*TimeLapse/(2*parametersPhysical[0]))* np.sin(parameters[4]*TimeLapse + parameters[2]))
            Acceleration = - parametersPhysical[1]/parametersPhysical[0] * Position - parameters[3]/parametersPhysical[0] * Speed
        else:
            raise Exception("Invalid Motion Type ",TypeMotion)
    else:
        raise Exception("Invalid Motion Type ",TypeSHM)

    return Position, Speed, Acceleration

def DampedOscillation(TimeLapse:np.ndarray,parameters:np.ndarray,TypeMotion: str = "sin",TypeSHM: str = 'SHM') -> np.ndarray:
    """Creates a Damped Oscillatory Motion"""
    Position = np.zeros(TimeLapse.shape[0])
    Speed = np.zeros(TimeLapse.shape[0])
    Acceleration = np.zeros(TimeLapse.shape[0])

    if TypeMotion == "sin":
        pass
    elif TypeMotion == "cos":
        pass
    else:
        raise Exception("Invalid Motion Type ",TypeMotion)

    return Position, Speed, Acceleration

def EnergySHM(Position:np.ndarray,Speed:np.ndarray,parametersPhysical:np.ndarray) -> np.ndarray:
    """Creates the Energy vectors"""
    Kinetic = np.zeros_like(Position)
    Potential = np.zeros_like(Position)
    Total = np.zeros_like(Position)

    Kinetic = 0.5 * parametersPhysical[0] * Speed ** 2
    Potential = 0.5 * parametersPhysical[1] * Position ** 2

    Total = Kinetic + Potential

    return Kinetic, Potential, Total

def Waves2D(TimeLapse:np.ndarray,Positions:np.ndarray,parameters:np.ndarray,TypeMotion:str = 'sin',TypeMovement:str = "Full"):
    """Creates an n x n array of a 2D wave"""
    layout = np.zeros((TimeLapse.shape[0],Positions.shape[0]))
    if TypeMovement == "Full":
        if TypeMotion == 'sin':
            for i in range(layout.shape[0]):
                layout[i,:] = parameters[0] * np.sin(parameters[1] * Positions + parameters[2] * TimeLapse[i] + parameters[3])
        elif TypeMotion == 'cos':
            for i in range(layout.shape[0]):
                layout[i,:] = parameters[0] * np.cos(parameters[1] * Positions + parameters[2] * TimeLapse[i] + parameters[3])
        else:
            raise Exception("Invalid Motion Type ",TypeMotion)
    elif TypeMovement == "Standing":
        for i in range(layout.shape[0]):
            layout[i,:] = 2 * parameters[0] * np.sin(parameters[1] * Positions) * np.cos(parameters[2] * TimeLapse[i])
    else:
        raise Exception("Invalid Movement Type ",TypeMovement)
    return layout

def Waves2DX(TimeLapse:np.ndarray,XValue,parameters:np.ndarray,TypeMotion:str = 'sin',TypeMovement:str = "Full"):
    """Creates a n array of the Position Slice of the 2D wave"""
    wave = np.zeros_like(TimeLapse)
    if TypeMovement == "Full":
        if TypeMotion == 'sin':
            wave = parameters[0] * np.sin(parameters[1] * XValue + parameters[2] * TimeLapse + parameters[3])
        elif TypeMotion == 'cos':
            wave = parameters[0] * np.cos(parameters[1] * XValue + parameters[2] * TimeLapse + parameters[3])
    elif TypeMovement == "Standing":
        wave = 2 * parameters[0] * np.sin(parameters[1] * XValue) * np.cos(parameters[2] * TimeLapse)
    else:
        raise Exception("Invalid Movement Type ",TypeMovement)
    return wave

def Waves2DT(Position:np.ndarray,TValue,parameters:np.ndarray,TypeMotion:str = 'sin',TypeMovement:str = "Full"):
    """Creates a n array of the Time Slice of the 2D wave"""
    wave = np.zeros_like(Position)
    if TypeMovement == "Full":
        if TypeMotion == 'sin':
            wave = parameters[0] * np.sin(parameters[1] * Position + parameters[2] * TValue + parameters[3])
        elif TypeMotion == 'cos':
            wave = parameters[0] * np.cos(parameters[1] * Position + parameters[2] * TValue + parameters[3])
    elif TypeMovement == "Standing":
        wave = 2 * parameters[0] * np.sin(parameters[1] * Position) * np.cos(parameters[2] * TValue)
    else:
        raise Exception("Invalid Movement Type ",TypeMovement)
    return wave
