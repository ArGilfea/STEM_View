import numpy as np

def BeerLambert(spectrum:np.ndarray,x:float,mu_rho:np.ndarray,rho:float) -> np.ndarray:
  """Computes the attenuation of a photon spectrum\n
  Keyword Arguments:\n
  spectrum -- spectrum of the photon beam\n
  x -- depth of penetration\n
  mu_rho -- array of the attenuation coefficients\n
  rho -- density of the material\n
  """
  output = np.zeros_like(spectrum[:,0])
  for i in range(output.shape[0]):
    closest = closest_E(spectrum[i,0],mu_rho[:,0],mu_rho[:,6])
    output[i] = spectrum[i,1]*np.exp(-closest*x*rho)
  return output

def closest_E(E:float,E_range:np.ndarray,f_range:np.ndarray) -> float:
  f = np.interp(E,E_range,f_range)
  return f

def AverageE(f:np.ndarray) -> float:
    return np.sum(f[:,1]*f[:,0])/np.sum(f[:,1])

def TotalAttenuation(spectrum:np.ndarray,mu_rho:np.ndarray,rho:float,rangeDepth:np.ndarray) -> np.ndarray:
  energy = np.zeros_like(rangeDepth)

  for i in range(rangeDepth.shape[0]):
    AttSpectrum = BeerLambert(spectrum= spectrum, x = rangeDepth[i], mu_rho = mu_rho, rho = rho)
    energy[i] = np.sum(AttSpectrum)

  return energy