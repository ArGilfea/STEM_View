import numpy as np
import time
import matplotlib.pyplot as plt

import math                       #Pour pi
import scipy.fft                      #Pour la transformée de Fourier
from scipy.io import loadmat      #Pour lire un fichier matlab

from skimage.transform import radon, rescale

def create1DFunctions(CurveRange:np.ndarray,CurveParameters:np.ndarray,CurveType: np.ndarray, 
                      fullRange: bool = True, showCurve: bool = True) -> np.ndarray:
  """Creates a Filter of the same size as image, with specified parameters"""
  filter = np.zeros_like(CurveRange)
  for j in range(int(CurveParameters.shape[0])):
    if showCurve[j]:
      if CurveType[j] == "Hamming":
        for i in range(filter.shape[0]):
          if fullRange[j]:
            if CurveParameters[j,1] != 0 :
              filter[i] += 25/46 - (1-25/46)*np.cos(2*np.pi*(CurveRange[i]-CurveParameters[j,1]/2)/CurveParameters[j,1])
          else:
            if CurveParameters[j,1] != 0 :
              if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,1]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,1]/2:
                filter[i] += 25/46 - (1-25/46)*np.cos(2*np.pi*(CurveRange[i]-CurveParameters[j,1]/2)/CurveParameters[j,1])
      elif CurveType[j] == "Hann":
        for i in range(filter.shape[0]):
          if fullRange[j]:
            if CurveParameters[j,1] != 0 :
              filter[i] += 1/2 - (1-1/2)*np.cos(2*np.pi*(CurveRange[i]-CurveParameters[j,1]/2)/CurveParameters[j,1])
          else:
            if CurveParameters[j,1] != 0 :
              if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,1]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,1]/2:
                filter[i] += 1/2 - (1-1/2)*np.cos(2*np.pi*(CurveRange[i]-CurveParameters[j,1]/2)/CurveParameters[j,1])
      elif CurveType[j] == "Cosine-Sum":
        for i in range(filter.shape[0]):
          if fullRange[j]:
            if CurveParameters[j,1] != 0 :
              filter[i] += CurveParameters[j,2] - (1-CurveParameters[j,2])*np.cos(2*np.pi*(CurveRange[i]-CurveParameters[j,1]/2)/CurveParameters[j,1])
          else:
            if CurveParameters[j,1] != 0 :
              if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,1]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,1]/2:
                filter[i] += CurveParameters[j,2] - (1-CurveParameters[j,2])*np.cos(2*np.pi*(CurveRange[i]-CurveParameters[j,1]/2)/CurveParameters[j,1])

      elif CurveType[j] == "Low Pass Flat":
        for i in range(filter.shape[0]):
          if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,1]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,1]/2:
            if CurveParameters[j,2] != 0 :
              filter[i] += CurveParameters[j,2]

      elif CurveType[j] == "High Pass Flat":
        for i in range(filter.shape[0]):
          if  not (CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,1]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,1]/2):
            if CurveParameters[j,2] != 0 :
              filter[i] += CurveParameters[j,2]

      elif CurveType[j] == "Triangular":
        for i in range(filter.shape[0]):
          if fullRange[j]:
            pass
          else:
            if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,1]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,1]/2:
              filter[i] += 2*CurveParameters[j,2]*np.abs(np.abs(CurveRange[i] - CurveParameters[j,0]) - CurveParameters[j,1]/2)
      elif CurveType[j] == "Ramp":
        for i in range(filter.shape[0]):
            if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,1]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,1]/2:
              filter[i] += 2*CurveParameters[j,2] * np.abs(CurveRange[i] - CurveParameters[j,0])

      elif CurveType[j] == "Cosine":
        for i in range(filter.shape[0]):
          if fullRange[j]:
            if CurveParameters[j,2] != 0 :
                filter[i] += CurveParameters[j,2]*np.cos(2*np.pi*(CurveRange[i]-CurveParameters[j,0]/2)*(CurveParameters[j,1]))
          else:
            if CurveParameters[j,2] != 0 :
              if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,2]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,2]/2:
                filter[i] += CurveParameters[j,2]*np.cos(2*np.pi*(CurveRange[i]-CurveParameters[j,0]/2)*(CurveParameters[j,1]))

      elif CurveType[j] == "Gaussian":
        for i in range(filter.shape[0]):
          if fullRange[j]:
            if CurveParameters[j,1] != 0 :
              filter[i] += CurveParameters[j,2]*np.exp(-(1/2)*(CurveRange[i] - CurveParameters[j,0]/2)**2/(CurveParameters[j,1])**2) 
          else:
            if CurveParameters[j,1] != 0 :
              if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,2]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,2]/2:
                filter[i] += CurveParameters[j,2]*np.exp(-(1/2)*(CurveRange[i] - CurveParameters[j,0]/2)**2/(CurveParameters[j,1])**2) 

      elif CurveType[j] == "Exponential":
        for i in range(filter.shape[0]):
          if fullRange[j]:
            if CurveParameters[j,1] != 0 :
              filter[i] += CurveParameters[j,2] * np.exp(-(1/(CurveParameters[j,1]/2))*np.abs(CurveRange[i] - CurveParameters[j,0]/2))
          else:
            if CurveParameters[j,1] != 0 :
              if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,2]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,2]/2:
                filter[i] += CurveParameters[j,2] * np.exp(-(1/(CurveParameters[j,1]/2))*np.abs(CurveRange[i] - CurveParameters[j,0]/2))

      elif CurveType[j] == "Deltas":
        dx = CurveRange[1] - CurveRange[0]
        for i in range(filter.shape[0]):
          if (CurveRange[i] > CurveParameters[j,0] - dx/2) and (CurveRange[i] < CurveParameters[j,0] + dx/2):
            filter[i] += CurveParameters[j,1]
      elif CurveType[j] == "Sines":
        for i in range(filter.shape[0]):
          if fullRange[j]:
            if CurveParameters[j,2] != 0 :
                filter[i] += CurveParameters[j,2]*np.sin(2*np.pi*(CurveRange[i]-CurveParameters[j,0]/2)*(CurveParameters[j,1]))
          else:
            if CurveParameters[j,2] != 0 :
              if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,2]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,2]/2:
                filter[i] += CurveParameters[j,2]*np.sin(2*np.pi*(CurveRange[i]-CurveParameters[j,0]/2)*(CurveParameters[j,1]))
      elif CurveType[j] == "Half Circle":
        for i in range(filter.shape[0]):
            if CurveParameters[j,2] != 0 :
              if CurveRange[i] >= -CurveParameters[j,0] and CurveRange[i] <= CurveParameters[j,0]:
                filter[i] += CurveParameters[j,2] * (CurveParameters[j,0]**2-CurveRange[i]**2)**(1/2)
      elif CurveType[j] == "Gaussian Noise":
        for i in range(filter.shape[0]):
          if fullRange[j]:
            if CurveParameters[j,2] != 0 :
              filter[i] += np.random.normal(loc = 0,scale = CurveParameters[j,2])
          else:
            if CurveParameters[j,2] != 0 :
              if CurveRange[i] >=  CurveParameters[j,0]- CurveParameters[j,1]/2 and CurveRange[i] <=  CurveParameters[j,0] + CurveParameters[j,1]/2:
                filter[i] += np.random.normal(loc = 0,scale = CurveParameters[j,2])
      else:
        raise Exception("Invalid choice of Curve: ",CurveType[j])

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