import numpy as np
import time
import matplotlib.pyplot as plt

import math                       #Pour pi
import scipy.fft                      #Pour la transformée de Fourier
from scipy.io import loadmat      #Pour lire un fichier matlab

from skimage.transform import radon, rescale


def createFilters(Image:np.ndarray,FilterParameters:np.ndarray,FilterType: str = "Hamming", fullRange: bool = True) -> np.ndarray:
  """Creates a Filter of the same size as image, with specified parameters"""
  filter = np.zeros((Image.shape[0],Image.shape[1]))
  if fullRange:
    RangeValue = [0, Image.shape[0], 0, Image.shape[1]]
  else:
    RangeValue = [int(Image.shape[0]/2 - FilterParameters[0]/2-1),  int(Image.shape[0]/2 + FilterParameters[0]/2)-1, 
                    int(Image.shape[1]/2 - FilterParameters[0]/2-1), int(Image.shape[1]/2 + FilterParameters[0]/2-1)]

  if FilterType == "Hamming":
    for i in range(RangeValue[0],RangeValue[1]):
      for j in range(RangeValue[2], RangeValue[3]):
          filter[i,j] = (25/46 - (1-25/46)*np.cos(2*np.pi*(i-int(Image.shape[0]/2 - FilterParameters[0]/2))/FilterParameters[0])) * (25/46 - (1-25/46)*np.cos(2*np.pi*(j-int(Image.shape[1]/2 - FilterParameters[0]/2))/FilterParameters[0]))
  elif FilterType == "Hann":
    for i in range(RangeValue[0],RangeValue[1]):
      for j in range(RangeValue[2], RangeValue[3]):
          filter[i,j] = (1/2 - (1-1/2)*np.cos(2*np.pi*(i-int(Image.shape[0]/2 - FilterParameters[0]/2))/FilterParameters[0])) * (1/2 - (1-1/2)*np.cos(2*np.pi*(j-int(Image.shape[1]/2 - FilterParameters[0]/2))/FilterParameters[0]))
  elif FilterType == "Cosine-Sum":
    for i in range(RangeValue[0],RangeValue[1]):
      for j in range(RangeValue[2], RangeValue[3]):
          filter[i,j] = (FilterParameters[1] - (1-FilterParameters[1])*np.cos(2*np.pi*(i-int(Image.shape[0]/2 - FilterParameters[0]/2))/FilterParameters[0])) * (FilterParameters[1] - (1-FilterParameters[1])*np.cos(2*np.pi*(j-int(Image.shape[1]/2 - FilterParameters[0]/2))/FilterParameters[0]))
  elif FilterType == "Low Pass Flat":
    for i in range(RangeValue[0],RangeValue[1]):
      for j in range(RangeValue[2], RangeValue[3]):
        filter[i,j] = FilterParameters[1]
  elif FilterType == "High Pass Flat":
    for i in range(Image.shape[0]):
      for j in range(Image.shape[1]):
        if (i < Image.shape[0]/2 - FilterParameters[0]/2 or i > Image.shape[0]/2 + FilterParameters[0]/2) or (j < Image.shape[0]/2 - FilterParameters[0]/2 or j > Image.shape[0]/2 + FilterParameters[0]/2):
          filter[i,j] = FilterParameters[1]
  elif FilterType == "Low Pass Circular":
    for i in range(Image.shape[0]):
      for j in range(Image.shape[1]):
        if (i - Image.shape[0]/2)**2 + (j - Image.shape[1]/2)**2 < FilterParameters[0] ** 2:
          filter[i,j] = FilterParameters[1]
  elif FilterType == "High Pass Circular":
    for i in range(Image.shape[0]):
      for j in range(Image.shape[1]):
        if (i - Image.shape[0]/2)**2 + (j - Image.shape[1]/2)**2 > FilterParameters[0] ** 2:
          filter[i,j] = FilterParameters[1]
  elif FilterType == "Triangular":
    for i in range(RangeValue[0],RangeValue[1]):
      for j in range(RangeValue[2], RangeValue[3]):
        filter[i,j] = (RangeValue[1] - RangeValue[0] - np.abs((i - Image.shape[0]/2)/(FilterParameters[0]/2))) * (RangeValue[3] - RangeValue[2] - np.abs((j - Image.shape[1]/2)/(FilterParameters[0]/2)))/(RangeValue[3] - RangeValue[2] + RangeValue[1] - RangeValue[0])
  elif FilterType == "Ramp":
    for i in range(RangeValue[0],RangeValue[1]):
      for j in range(RangeValue[2], RangeValue[3]):
        filter[i,j] = np.abs((i - Image.shape[0]/2)/(FilterParameters[0]/2)) * np.abs((j - Image.shape[1]/2)/(FilterParameters[0]/2))
  elif FilterType == "Welch":
    for i in range(RangeValue[0],RangeValue[1]):
      for j in range(RangeValue[2], RangeValue[3]):
        filter[i,j] = (RangeValue[1] - RangeValue[0] -((i - Image.shape[0]/2)/(FilterParameters[0]/2))**2) * (RangeValue[2] - RangeValue[3] - ((j - Image.shape[1]/2)/(FilterParameters[0]/2))**2)
  elif FilterType == "Cosine":
    for i in range(RangeValue[0],RangeValue[1]):
      for j in range(RangeValue[2], RangeValue[3]):
        filter[i,j] = np.cos(np.pi*(i - Image.shape[0]/2)/(FilterParameters[0])) * np.cos(np.pi*(j - Image.shape[1]/2)/(FilterParameters[0]))
  elif FilterType == "Gaussian":
    for i in range(RangeValue[0],RangeValue[1]):
      for j in range(RangeValue[2], RangeValue[3]):
        filter[i,j] = np.exp(-(1/2)*(i - Image.shape[0]/2)**2/(FilterParameters[0]/2)**2) * np.exp(-(1/2)*(j - Image.shape[1]/2)**2/(FilterParameters[0]/2)**2) 
  elif FilterType == "Exponential":
    for i in range(RangeValue[0],RangeValue[1]):
      for j in range(RangeValue[2], RangeValue[3]):
        filter[i,j] = np.exp(-(1/(FilterParameters[0]/2))*np.abs(i - Image.shape[0]/2)) * np.exp(-(1/(FilterParameters[0]/2))*np.abs(j - Image.shape[1]/2))
  else:
    raise Exception("Invalid choice of Filter")

  return filter

def FourierTransform(Img:np.ndarray) -> np.ndarray:
  """Returns the Fourier transform of a 2-D image"""
  ImageFourier = scipy.fft.fft2(Img)
  ImageFourierAbs = scipy.fft.fftshift(np.abs(ImageFourier),axes=[0,1])

  return ImageFourierAbs, ImageFourier

def InverseFourierTransform(Img:np.ndarray) -> np.ndarray:
  """Returns the Inverse Fourier transform of a 2-D image"""
  ImageiFourier = scipy.fft.ifft2(Img)
  ImageiFourierAbs = scipy.fft.fftshift(np.abs(ImageiFourier),axes=[0,1])

  return ImageiFourierAbs, ImageiFourier

def FourierConvolution(Img1:np.ndarray, Img2:np.ndarray) -> np.ndarray:
  """Returns the Fourier domain product of a convolution"""
  NewImg = Img1 * Img2
  return np.abs(NewImg), NewImg