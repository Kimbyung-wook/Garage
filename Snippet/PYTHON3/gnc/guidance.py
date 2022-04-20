import numpy as np
import math
import matplotlib.pyplot as plt
from drawnow import *

class guidance_l1():
  '''
  Park, Deyst and How,
  "Performance and Lyapunov Stability of a Nonlinear Path Following Guidance Method"
  Journal of Guidance, Control, and Dynamics, Vol.30, No.6, 2007.
  '''
  def __init__(self):
    self.r_ref = 200.0
    self.k_eta = 1.0
    self.direction = 0.0
    self.set_dir = False
    self.eta = 0.0

  def set_desired_radius(self, r_d:float):
    self.r_ref = np.max((1.0, r_d))

  def set_k_eta(self, k_eta:float):
    self.k_eta = k_eta

  def set_dir_cw(self):
    self.set_dir = True
    self.direction = 1.0

  def set_dir_ccw(self):
    self.set_dir = True
    self.direction =-1.0
  
  def set_dir_auto(self):
    self.set_dir = False
    self.direction = 0.0

  def get_eta(self):
    return self.eta
  
  def get_desired_radius(self):
    return self.r_ref

  def step_tracking(self, target_pos, my_pos, vel):
    '''
    input
      target_pos [m, m, m]
      my_pos [m, m, m]
      vel [m/s, m/s, m/s]
    output
      an_cmd [m/s2, m/s2, m/s2] on nav frame
    '''
    TpN = np.array([target_pos])
    TpN = np.reshape(TpN, np.size(TpN))
    MpN = np.array([my_pos])
    MpN = np.reshape(MpN, np.size(MpN))

    L = np.array(TpN - MpN)
    V = np.array([vel])
    an_cmd = 2.0 * np.cross(np.cross(V,L),V) / np.max([np.sum(np.square(L),1)])
    return an_cmd

  def step_tracking_2d(self, target_pos, my_pos, vel):
    '''
    input  
      target_pos [m, m, m]  
      my_pos [m, m, m]  
      vel [m/s, m/s, m/s]
    output
      an_cmd [m/s2, m/s2] on nav frame
    '''
    target_pos[2] = 0.0
    my_pos[2] = 0.0
    vel[2] = 0.0
    an_cmd = self.step_tracking(target_pos, my_pos, vel)
    return [an_cmd[0], an_cmd[1]]

  def step_loitering(self, target_pos, my_pos, vel):
    '''
    input
      target_pos [m, m, m]
      my_pos [m, m, m]
      vel [m/s, m/s, m/s]
    output
      an_cmd [m/s2, m/s2, m/s2] on nav frame
    '''
    TpN = np.array([target_pos])
    TpN = np.reshape(TpN, np.size(TpN))
    MpN = np.array([my_pos])
    MpN = np.reshape(MpN, np.size(MpN))
    L = np.array(TpN - MpN)
    V = np.array(vel)

    ## Loitering Guidance
    an      = np.cross(np.cross(V,L),V)
    e_an    = an / np.max([np.linalg.norm(an),0.000001])
    e_L     = L  / np.max([np.linalg.norm(L),0.000001])
    e_V     = V  / np.max([np.linalg.norm(V),0.000001])
    eta     = math.asin(np.cross(e_an,e_L)[2])
    self.eta= eta
    if self.set_dir:
      cwccw  = self.direction
    else:
      cwccw   = np.sign(math.asin(np.dot(np.array([0,0,1]),np.cross(e_V,e_L)))) # Determine Which direction
    m_an_cmd = np.sum(np.square(V))/self.r_ref + cwccw * self.k_eta * math.sin(eta)
    an_cmd = e_an * m_an_cmd
    return an_cmd
    
  def step_loitering_2d(self, target_pos, my_pos, vel):
    '''
    input
      target_pos [m, m, m]
      my_pos [m, m, m]
      vel [m/s, m/s, m/s]
    output
      an_cmd [m/s2, m/s2] on nav frame
    '''
    target_pos[2] = 0.0
    my_pos[2] = 0.0
    vel[2] = 0.0
    an_cmd = self.step_loitering(target_pos, my_pos, vel)
    return [an_cmd[0], an_cmd[1]]

class guidance_vf_loiter():
  def __init__(self):
    self.r_ref = 200.0
    self.direction = 1.0
    self.pcl = 0.4

  def set_desired_radius(self, r_d:float):
    self.r_ref = np.max((1.0, r_d))

  def set_dir_cw(self):
    self.direction = 1.0

  def set_dir_ccw(self):
    self.direction =-1.0

  def set_pcl(self, pcl):
    self.pcl = np.max((0.0001, pcl))

  def step(self, target_pos, my_pos, Yaw):
    '''
    input
      target_pos [m, m, m]
      my_pos [m, m, m]
      Yaw [rad]
    output
      yaw_error [rad]
    '''
    n_vf = target_pos[0] - my_pos[0]
    e_vf = target_pos[1] - my_pos[1]
    r_vf      = np.max((1.0, np.sqrt(n_vf*n_vf + e_vf*e_vf)))
    theta_vf  = np.arctan2(e_vf, n_vf)
    chicmd_vf = (theta_vf + self.direction * np.arctan2(self.pcl*r_vf, -(r_vf - self.r_ref)))
    chicmd_vf = np.remainder(chicmd_vf, 2*np.pi) # range 0.0 ~ 2*pi
    yaw = np.remainder(Yaw, 2*np.pi)
    yaw_error = np.remainder(chicmd_vf - yaw + np.pi, 2*np.pi) - np.pi

    return yaw_error
    
class guidance_vf_lyapunov_loiter():
  '''
  Lawrence, Frew and Pisano,
  "Lyapunov Vector Fields for Autonomous UAV Flight Control,"
  AIAA Guidance, Navigatino and Control Conference and Exhibit, 2007.
  '''
  def __init__(self):
    self.r_ref = 200.0
    self.direction = 1.0

  def set_desired_radius(self, r_d:float):
    self.r_ref = np.max((1.0, r_d))

  def set_dir_cw(self):
    self.direction = 1.0

  def set_dir_ccw(self):
    self.direction =-1.0

  