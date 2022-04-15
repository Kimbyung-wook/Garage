import numpy as np

class lpf_1st():
  def __init__(self, tau):
    self.x = 0.0
    self.tau = np.max((0.000001, tau))

  def reset(self, x0):
    self.x = x0

  def set_tau(self, tau):
    self.tau = tau

  def step(self, dt, u):
    alpha = dt * self.tau
    x_new = (1-alpha) * self.x + alpha * u
    self.x = x_new
    return self.x

def pqr2eulerrate(pqr_in, att_in):
  '''
  input  : pqr [rad/s]
  output : att(euler angle) [rad]
  '''
  pqr = np.array(pqr_in)
  pqr = np.reshape(pqr, (1, np.size(pqr)))
  att = np.array(att_in)
  att = np.reshape(att, (np.size(att)))
  phi = att[1]; theta = att[2]; psi = att[3]

  wB2Euler = np.array([
    [1, 0,           -np.sin(theta)],
    [0, np.cos(phi),  np.cos(theta)*np.sin(phi)],
    [0,-np.sin(phi),  np.cos(theta)*np.cos(phi)]
  ])
  eulerrate = wB2Euler * pqr

  return eulerrate
  
def eulerrate2pqr(eulerrate_in, att_in):
  '''
  input  : att(euler angle) [rad]
  output : pqr [rad/s]
  '''
  eulerrate = np.array(eulerrate_in)
  eulerrate = np.reshape(eulerrate, (1, np.size(eulerrate)))
  att = np.array(att_in)
  att = np.reshape(att, (np.size(att)))
  phi = att[1]; theta = att[2]; psi = att[3]

  Euler2wB = np.array([
    [1, np.sin(phi)*np.tan(theta), np.cos(phi)*np.tan(theta)],
    [0, np.cos(phi),              -np.sin(phi)],
    [0, np.sin(phi)/np.cos(theta), np.cos(phi)/np.cos(theta)]
  ])
  pqr = Euler2wB * eulerrate

  return pqr


def lla2ecef(lla):
  '''
    geodetic 2 ECEF
    Input : lla = [lat [rad], lon [rad], alt [m]]
    Output : ecef [m]
  '''
  lat = lla[0]
  lon = lla[1]
  alt = lla[2]
  Re = 6378137.0
  f  = 0.00335281066 # 1/298.257223563
  e2 = f * (2 - f)
  N = Re / np.sqrt(1 - e2 * np.power(np.sin(lat),2.0))

  ECEF_x = (alt +        N)*np.cos(lat)*np.cos(lon)
  ECEF_y = (alt +        N)*np.cos(lat)*np.sin(lon)
  ECEF_z = (alt + (1-e2)*N)*np.sin(lat)

  return [ECEF_x, ECEF_y, ECEF_z]

def lla2flat(lla, lla_ref):
  '''
    Input  : lla = [lat [rad], lon [rad], alt [m]]
    Output : pNED on flat earth model (from WGS84)
  '''

  Re = 6378137.0
  f  = 0.00335281066 # 1/298.257223563

  e2 = f * (2 - f)
  Rn = Re / np.sqrt(1 - e2 * np.power(np.sin(lla_ref[0]),2.0))# Prime vertical
  Rm = Rn (1-e2) / (1 - e2 * np.power(np.sin(lla_ref[0]),2.0))# meridian

  pN = (lla[0] - lla_ref[0]) * np.atan2(1, Rn)
  pE = (lla[1] - lla_ref[1]) * np.atan2(1, Rm * np.cos(lla_ref[0]))
  pD =-(lla[2] - lla_ref[2]) 

  return [pN, pE, pD]

def flat2lla(pNED, lla_ref):
  '''
    Input  : pNED on flat earth model (from WGS84)
    Output : lla = [lat [rad], lon [rad], alt [m]]
  '''
  Re = 6378137.0
  f  = 0.00335281066 # 1/298.257223563
  
  e2 = f * (2 - f)
  Rn = Re / np.sqrt(1 - e2 * np.power(np.sin(lla_ref[0]),2.0))# Prime vertical
  Rm = Rn (1-e2) / (1 - e2 * np.power(np.sin(lla_ref[0]),2.0))# meridian

  lat = lla_ref[0] + pNED[0] / np.atan2(1, Rn)
  lon = lla_ref[1] + pNED[1] / np.atan2(1, Rm * np.cos(lla_ref[0]))
  alt = lla_ref[2] - pNED[2]

  return [lat, lon, alt]