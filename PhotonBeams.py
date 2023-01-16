import numpy as np

def BeerLambert(f,x,mu_rho,rho):
  output = np.zeros_like(f[:,0])
  for i in range(output.shape[0]):
    closest = closest_E(f[i,0],mu_rho[:,0],mu_rho[:,7])
    output[i] = f[i,1]*np.exp(-closest*x*rho)
  return output

def closest_E(E,E_range,f_range):
  f = np.interp(E,E_range,f_range)
  return f

def AverageE(f):
    return np.sum(f[:,1]*f[:,0])/np.sum(f[:,1])