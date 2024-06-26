import numpy as np
from skimage.transform import radon, rescale, iradon

def Sinogram(Image:np.ndarray,angles_step:np.ndarray = 1):
    """Creates the sinogram from an image"""
    angles = np.arange(0,360,angles_step)
    return radon(Image, theta=angles)

def Reconstruction(Sinogram: np.ndarray,angles_step:np.ndarray = 1, filter: str = 'ramp'):
    """Reconstructs an Image from a Sinogram"""
    angles = np.arange(0,360,angles_step)
    if filter != "None":
        return iradon(Sinogram, angles, filter_name=filter)
    else:
        return iradon(Sinogram, angles, filter_name=None)

def Rotate(array:np.ndarray,angle:float):
    """Rotate a slice of an array around a point"""
    center = np.array([int(array.shape[0]/2),int(array.shape[1]/2)])
    rotated_array = np.zeros_like(array)
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            new_I = i - center[0]
            new_J = j - center[1]
            new_X = new_I*np.cos(angle)+new_J*np.sin(angle)
            new_Y = -new_I*np.sin(angle)+new_J*np.cos(angle)
            new_X_replaced = new_X + center[0]
            new_Y_replaced = new_Y + center[1]
            if (new_X_replaced >= 0 and new_X_replaced <= array.shape[0]) and (new_Y_replaced >= 0 and new_Y_replaced <= array.shape[1]):
                rotated_array[i,j] = segm_interpolation_2D(array,new_X_replaced,new_Y_replaced)
                #rotated_array[i,j] = array[int(new_X_replaced),int(new_Y_replaced)]
    return rotated_array

def segm_interpolation_2D(slice:np.ndarray,p1:float,p2:float) -> float:
    """
    This function interpolates the segmentation between two points\n
    Keyword arguments:\n
    slice -- slice to use for the interpolation\n
    p1 -- point along the first axis\n
    p2 -- point along the second axis\n
    """
    intX = int(p1)
    intY = int(p2)

    try:
        xd = p1 - intX
        yd = p2 - intY

        c0 = slice[intX,intY]*(1 - xd) + slice[intX+1,intY] * xd
        c1 = slice[intX,intY+1]*(1 - xd) + slice[intX+1,intY+1] * xd

        xprimeyprime = c0*(1-yd) + c1 * yd

    except:
        xprimeyprime = 0

    return xprimeyprime

def CreateImage(parameters: np.ndarray, name: str)->np.ndarray:
    """Creates an Image based on parameters"""
    newImage = np.zeros((int(parameters[0,0]),int(parameters[0,1])))
    
    if name == "Rectangle":
        for i in range(newImage.shape[0]):
            for j in range(newImage.shape[1]):
                if (i <= parameters[1,0] + parameters[2,0]/2) and (i >= parameters[1,0] - parameters[2,0]/2):
                    if (j <= parameters[1,1] + parameters[2,1]/2) and (j >= parameters[1,1] - parameters[2,1]/2):
                        newImage[i,j] = parameters[3,0]
    elif name == "Ellipsoid":
        for i in range(newImage.shape[0]):
            for j in range(newImage.shape[1]):
                if (((i-parameters[1,0])/parameters[2,0])**2 + ((j - parameters[1,1])/parameters[2,1])**2) <= 1:
                    newImage[i,j] = parameters[3,0]
    elif name == "Dense Shell Ellipsoid":
        for i in range(newImage.shape[0]):
            for j in range(newImage.shape[1]):
                if (((i-parameters[1,0])/parameters[2,0])**2 + ((j - parameters[1,1])/parameters[2,1])**2) <= 1:
                    newImage[i,j] = parameters[3,0] * ((i-parameters[1,0])/parameters[2,0])**2 + parameters[3,1] * ((j - parameters[1,1])/parameters[2,1])**2
    elif name == "Dense Core Ellipsoid":
        for i in range(newImage.shape[0]):
            for j in range(newImage.shape[1]):
                if (((i-parameters[1,0])/parameters[2,0])**2 + ((j - parameters[1,1])/parameters[2,1])**2) <= 1:
                    newImage[i,j] = 1/(parameters[3,0] * ((i-parameters[1,0]))**2 + parameters[3,1] * ((j - parameters[1,1]))**2 + 1)
 
    elif name == "Gaussian":
        if parameters[2,0] != 0:
            for i in range(newImage.shape[0]):
                newImage[i,:] = parameters[3,0] * np.exp(-(i-parameters[1,0])**2/(2*parameters[2,0]**2))
        if parameters[2,1] != 0:
            for j in range(newImage.shape[1]):
                newImage[:,j] *= parameters[3,1] * np.exp(-(j-parameters[1,1])**2/(2*parameters[2,1]**2))
    elif name == "Sinc":
        for i in range(newImage.shape[0]):
            newImage[i,:] = parameters[3,0] * np.sin(2*np.pi*parameters[2,0]*(i-parameters[1,0]))
        for j in range(newImage.shape[1]):
            newImage[:,j] *= parameters[3,1] * np.sin(2*np.pi*parameters[2,1]*(j-parameters[1,1]))
    else:
        raise Exception(f"Invalid choice of Image with : {name}")

    return newImage