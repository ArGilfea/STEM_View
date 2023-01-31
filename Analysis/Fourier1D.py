import numpy as np
import time
import matplotlib.pyplot as plt

import math                       #Pour pi
import scipy.fft                      #Pour la transformée de Fourier
from scipy.io import loadmat      #Pour lire un fichier matlab

from skimage.data import shepp_logan_phantom
from skimage.transform import radon, rescale

def create1DFunctions(CurveRange:np.ndarray,CurveParameters:np.ndarray,CurveType: str = "Hamming", fullRange: bool = True) -> np.ndarray:
  """Creates a Filter of the same size as image, with specified parameters"""
  filter = np.zeros_like(CurveRange)
  if fullRange:
    RangeValue = [0, CurveRange.shape[0]]
  else:
    for i in range(CurveRange.shape[0]):
      if CurveRange[i] < CurveParameters[0]/2:
        indexValue = i
    RangeValue = [CurveRange.shape[0] - indexValue, indexValue]
  if CurveType == "Hamming":
    for i in range(RangeValue[0],RangeValue[1]):
        filter[i] = 25/46 - (1-25/46)*np.cos(2*np.pi*(CurveRange[i]-CurveRange[RangeValue[0]])/CurveParameters[0])
  elif CurveType == "Hann":
    for i in range(RangeValue[0],RangeValue[1]):
        filter[i] = 1/2 - (1-1/2)*np.cos(2*np.pi*(CurveRange[i]-CurveRange[RangeValue[0]])/CurveParameters[0])
  elif CurveType == "Cosine-Sum":
    for i in range(RangeValue[0],RangeValue[1]):
        filter[i] = CurveParameters[1] - (1-CurveParameters[1])*np.cos(2*np.pi*(CurveRange[i]-CurveRange[RangeValue[0]])/CurveParameters[0])
  elif CurveType == "Low Pass Flat":
    for i in range(RangeValue[0],RangeValue[1]):
      filter[i] = CurveParameters[1]
  elif CurveType == "High Pass Flat":
    for i in range(filter.shape[0]):
      if (CurveRange[i] < -CurveParameters[0]/2 or CurveRange[i] > CurveParameters[0]/2):
        filter[i] = CurveParameters[1]
  elif CurveType == "Triangular":
    for i in range(RangeValue[0],RangeValue[1]):
      filter[i] = (RangeValue[1] - RangeValue[0] - np.abs((i - filter.shape[0]/2)/(CurveParameters[0]/2)))
  elif CurveType == "Ramp":
    for i in range(RangeValue[0],RangeValue[1]):
      filter[i] = np.abs((i - filter.shape[0]/2)/(CurveParameters[0]/2))
  elif CurveType == "Welch":
    for i in range(RangeValue[0],RangeValue[1]):
      filter[i] = (RangeValue[1] - RangeValue[0] -((i - filter.shape[0]/2)/(CurveParameters[0]/2))**2)
  elif CurveType == "Cosine":
    for i in range(RangeValue[0],RangeValue[1]):
      filter[i] = np.cos(np.pi*(i - filter.shape[0]/2)/(CurveParameters[0]))
  elif CurveType == "Gaussian":
    for i in range(RangeValue[0],RangeValue[1]):
      filter[i] = np.exp(-(1/2)*(i - filter.shape[0]/2)**2/(CurveParameters[0]/2)**2) 
  elif CurveType == "Exponential":
    for i in range(RangeValue[0],RangeValue[1]):
      filter[i] = np.exp(-(1/(CurveParameters[0]/2))*np.abs(i - filter.shape[0]/2))
  elif CurveType == "Deltas":
    dx = CurveRange[1] - CurveRange[0]
    for i in range(int(CurveParameters.shape[0]/2 - 1)):
      for j in range(RangeValue[0],RangeValue[1]):
        if (CurveRange[j] > CurveParameters[2*i + 2] - dx/2) and (CurveRange[j] < CurveParameters[2*i + 2] + dx/2):
          filter[j] = CurveParameters[2*i + 3]
          filter[CurveRange.shape[0] - j] = CurveParameters[2*i + 3]
  elif CurveType == "Sines":
    dx = CurveRange[1] - CurveRange[0]
    for i in range(int(CurveParameters.shape[0]/2 - 1)):
      for j in range(RangeValue[0],RangeValue[1]):
        filter[j] += CurveParameters[2*i + 3] * np.sin(2*np.pi*CurveParameters[2*i + 2] * CurveRange[j])
  else:
    raise Exception("Invalid choice of Curve: ",CurveType)

  return filter

def FourierTransform1D(Curve:np.ndarray) -> np.ndarray:
  """Returns the Fourier transform of a 1-D image"""
  ImageFourier = scipy.fft.fft(Curve)
  ImageFourierAbs = scipy.fft.fftshift(np.abs(ImageFourier),axes=[0])

  return ImageFourierAbs, ImageFourier

def InverseFourierTransform1D(Curve:np.ndarray) -> np.ndarray:
  """Returns the Inverse Fourier transform of a 2-D image"""
  ImageiFourier = scipy.fft.ifft(Curve)
  ImageiFourierAbs = scipy.fft.fftshift(np.abs(ImageiFourier),axes=[0])

  return ImageiFourierAbs, ImageiFourier

def FourierConvolution(Curve1:np.ndarray, Curve2:np.ndarray) -> np.ndarray:
  """Returns the Fourier domain product of a convolution"""
  NewImg = Curve1 * Curve2
  return np.abs(NewImg), NewImg