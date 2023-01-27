import numpy as np

def BoxedArea(numberBox: int, BoxType:str ,Curve, 
                CurveParameters:np.ndarray, dx: float,
                Boundaries: np.ndarray) -> float:
    area = 0.0

    for i in range(numberBox):
        if BoxType == 'Left Box':
            area += dx * Curve(Boundaries[0] + i * dx,CurveParameters)
        elif BoxType == 'Right Box':
            area += dx * Curve(Boundaries[0] + (i + 1) * dx,CurveParameters)
        elif BoxType == 'Center Box':
            area += dx * Curve(Boundaries[0] + (i + 0.5) * dx,CurveParameters)
        elif BoxType == 'Trapezoid':
            area += dx * (Curve(Boundaries[0] + i * dx,CurveParameters) + Curve(Boundaries[0] + (i + 1) * dx,CurveParameters))/2
        else:
            raise Exception("Invalid Box Type")
        
    return area

def BoxedAreaRange(rangeBox: np.ndarray, BoxType: str,Curve,
                    CurveParameters: np.ndarray,
                    Boundaries: np.ndarray) -> np.ndarray:
    boxedArea = np.zeros_like(rangeBox,dtype = float)

    for i in range(boxedArea.shape[0]):
        dx = (Boundaries[1] - Boundaries[0])/rangeBox[i]
        boxedArea[i] = BoxedArea(rangeBox[i], BoxType = BoxType ,Curve = Curve, 
                CurveParameters = CurveParameters, dx = dx,
                Boundaries = Boundaries)
    return boxedArea