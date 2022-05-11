import numpy as np
import math
from misc import lpf_1st
from point_model import *
import matplotlib.pyplot as plt

class uav_model_wrapper(point_model):
  def __init__(self, attr:dict):
    super().__init__(attr)
    self.action_in = np.zeros((1,6))
    self.action_out = np.zeros((1,6))
    self._angleI = 0.0
    self.do_loiter = False

    self.attr = dict()
    self.attr['tauU']  = np.array(      1.0, dtype=float)
    self.attr['tauP']  = np.array(     10.0, dtype=float)
    self.attr['tauQ']  = np.array(      5.0, dtype=float)
    self.attr['tauR']  = np.array(      2.0, dtype=float)
    self.attr['u_min'] = np.array( 50 / 3.6, dtype=float)
    self.attr['u_max'] = np.array(130 / 3.6, dtype=float)
    self.attr['p_min'] = np.deg2rad(-60.0)
    self.attr['p_max'] = np.deg2rad( 60.0)
    self.attr['q_min'] = np.deg2rad(-30.0)
    self.attr['q_max'] = np.deg2rad( 30.0)
    self.attr['r_min'] = np.deg2rad(-30.0)
    self.attr['r_max'] = np.deg2rad( 30.0)
    self.attr['phi_max'] = 45.0

    # Dynamic Model like real things
    self.u_model = lpf_1st(self.attr['tauU'])
    self.p_model = lpf_1st(self.attr['tauP'])
    self.q_model = lpf_1st(self.attr['tauQ'])
    self.r_model = lpf_1st(self.attr['tauR'])
    if 'u0' in attr:
      self.vB[0] = attr['u0']
      self.u_model.reset(attr['u0'])
      

  # def set_state(self, roll, pitch, yaw, pN, pE, pD, u, v, w):
  # def set_state(self, roll, pitch, yaw, pN, pE, pD, vN, vE, vD):
  def set_state(self, roll, pitch, yaw, lla, lla_ref, u,v,w):
    '''
      Input
        roll, pitch, yaw : deg
        pN, pE, pD : m
        u : m/s
    '''
    euler = np.array([roll, pitch, yaw])
    euler = np.reshape(euler, (np.size(euler)))
    euler = np.flip(euler, 0)
    self.att = R.from_euler('zyx',euler, degrees=True)

    # lla_ref_deg = np.array([lla_ref[0] / np.pi * 180.0, lla_ref[1] / np.pi * 180.0, lla_ref[2]])
    # lla_deg     = np.array([lla[0] / np.pi * 180.0, lla[1] / np.pi * 180.0, lla[2]])
    # print("degree:", lla_ref_deg, lla_deg)

    pNED = lla2flat(lla, lla_ref)
    # print(lla, lla_ref, pNED)
    self.pN[0] = pNED[0]
    self.pN[1] = pNED[1]
    self.pN[2] = pNED[2]
    
    # self.vN[0] = vN
    # self.vN[1] = vE
    # self.vN[2] = vD
    # self.vB    = np.dot(self.att.inv().as_matrix(), self.vN)
    # self.pN[0] = pN
    # self.pN[1] = pE
    # self.pN[2] = pD
    self.vB[0] = u
    self.vB[1] = 0.0
    self.vB[2] = 0.0
    self.vN    = np.dot(self.att.as_matrix(),self.vB)

  def set_raw_action(self, action_in):
    '''
      action item : [u,v,w,p,q,r]
    '''
    self.action_in = action_in
    return self.action_in

  def set_wp_lla_action(self, target_lla, lla_ref, desired_speed, desired_radius, direction):
    target_ned = lla2flat(target_lla, lla_ref)
    action_out = np.array([target_ned[0],target_ned[1],target_ned[2],
                            desired_speed, desired_radius, direction])
    output = self.set_wp_acion(action_out)
    return output

  def set_wp_action(self, action_in):
    '''
      action item : [TpN, TpE, TpD, Spd, Rd, Dir]
    '''
    # print('action_in ', action_in)
    euler   =  self.att.as_euler('xyz', degrees=False)
    phi     =  euler[0]
    theta   =  euler[1]
    psi     =  euler[2]
    n_vf    =  action_in[0] - self.pN[0]
    e_vf    =  action_in[1] - self.pN[1]
    dH      =-(action_in[2] - self.pN[2])
    Spd_cmd =  action_in[3]
    Rd      =  action_in[4]
    Dir     =  action_in[5]
    Spd     =    self.vB[0]

    Distance = np.sqrt(n_vf * n_vf + e_vf * e_vf)
    # print(Distance, n_vf, e_vf, self.pN)

    # # Approach
    if (self.do_loiter == False):
      chi_cmd = np.rad2deg(np.arctan2(e_vf, n_vf)) + 180.0

    if (Distance < 10):
      print(Distance, n_vf, e_vf)
      exit()

    # # Loitering : Vector Field Guidance
    # if (self.do_loiter == True):
    #   chi_cmd = self._loiter_vf(n_vf, e_vf, Rd, -Dir)

    # Exit
    chi_cmd = self._loiter_vf(n_vf, e_vf, Rd, -Dir)

    phi_cmd = self._heading_ctrl(chi_cmd, psi)
    omega = self._get_omega_from_phi_cmd(phi_cmd, Spd)

    # Something Control Mode
    dH_out = 0.01 * dH
    dH_sat = np.max((np.deg2rad(-10.0),np.min((dH_out, np.deg2rad(10.0)))))
    theta_out = 3.0 * (dH_sat - theta)
    pqr_att   = [ 5.0 * (phi_cmd - phi), 0.0, 0.0]
    pqr_coord = [-omega*np.sin(theta),
                  omega*np.cos(theta)*np.sin(phi),
                  omega*np.cos(theta)*np.cos(phi)]
    pqr_alt   = [ 0.0,
                  np.cos(phi) * theta_out, 
                 -np.sin(phi) * theta_out]

    # action output
    u_cmd = Spd_cmd
    p_cmd = pqr_coord[0] + pqr_att[0] + pqr_alt[0]
    q_cmd = pqr_coord[1] + pqr_att[1] + pqr_alt[1]
    r_cmd = pqr_coord[2] + pqr_att[2] + pqr_alt[2]

    action_out = [u_cmd, 0.0, 0.0, p_cmd, q_cmd, r_cmd]
    # print(action_out)
    self.action_in = action_out

    return self.action_in

  def mimic_model(self):
    '''
      UseCase
      set_state()
      set_raw_action() or set_wp_action()
      new_state = mimic_model()
    '''
    # Mimic Coyote Model
    # print(self.action_in)
    # print('euler ',self.att.as_euler('zyx', degrees=True), ' pN ', self.pN, ' vB ', self.vB, ' vN ', self.vN, ' actions ',self.action_out)

    u_cmd = np.max((self.attr['u_min'], np.min((self.action_in[0], self.attr['u_max'])))); 
    p_cmd = np.max((self.attr['p_min'], np.min((self.action_in[3], self.attr['p_max'])))); 
    q_cmd = np.max((self.attr['q_min'], np.min((self.action_in[4], self.attr['q_max'])))); 
    r_cmd = np.max((self.attr['r_min'], np.min((self.action_in[5], self.attr['r_max'])))); 
    u = self.u_model.step(self.dt, u_cmd) # u_cmd
    p = self.p_model.step(self.dt, p_cmd) # p_cmd
    q = self.q_model.step(self.dt, q_cmd) # q_cmd
    r = self.r_model.step(self.dt, r_cmd) # r_cmd

    self.action_out = np.array([u, 0, 0, p, q, r])

    return self.action_out


  def step(self):
    self.action_out = self.mimic_model()

    # Set input of point_model
    super().set_action(self.action_out)
    super().step()

  def _loiter_vf(self, n_vf, e_vf, Rd, Dir):
    pcl = 0.4

    dirs     = Dir / np.abs(Dir)
    r_vf     = np.max((1.0, np.sqrt(n_vf*n_vf + e_vf*e_vf)))
    theta_vf = np.arctan2(e_vf, n_vf)
    chicmd_vf= np.rad2deg(theta_vf + dirs * np.arctan2(pcl*r_vf, -(r_vf - Rd)))
    chicmd_vf = np.remainder(chicmd_vf, 360.0)
    # print("chi_c/yaw {:6.1f}/{:6.1f} : phiC/phi {:6.1f}/{:6.1f} | PQR {:6.3f}, {:6.3f}, {:6.3f}"
    #   .format(chicmd_vf, yaw, np.rad2deg(phi_cmd)[0],self.att.as_euler('zyx',degrees=True)[2], self.action_out[3], self.action_out[4], self.action_out[5]))
    # print('chi_c ',chicmd_vf, " / yaw ", yaw, 'eyaw ', eYaw, " -> phi_cmd/phi ",
    #   np.rad2deg(phi_cmd),self.att.as_euler('zyx',degrees=True)[2], ' actionPQR ',np.rad2deg(self.action_out[3:]) )
    return chicmd_vf

  def _heading_ctrl(self, chi_cmd, Yaw):
    yawP = 1.0
    yawI = 0.2
    yaw = np.remainder(np.rad2deg(Yaw) + 180, 360.0) # np.rad2deg(Yaw) + 180.0
    eYaw = np.remainder(chi_cmd - yaw + 180.0, 360.0) - 180.0

    # Directional Control
    angleP = eYaw*yawP;  # Roll
    self._angleI = eYaw*yawI*self.dt + self._angleI; # Roll
    sYaw  = angleP + self._angleI
    if (sYaw > self.attr['phi_max']):
        self._angleI = - angleP + self.attr['phi_max']
    elif (sYaw < (-self.attr['phi_max'])):
        self._angleI = - angleP + (-self.attr['phi_max'])
    sYaw  = angleP + self._angleI
    phi_cmd = np.deg2rad(sYaw)

    return phi_cmd

  def _get_omega_from_phi_cmd(self, phi_cmd, Spd):
    # Get Yawrate
    omega = np.tan(phi_cmd) * 9.80665 / np.max((Spd,1.0))

    return omega

if __name__ == "__main__":
  D2R = np.pi / 180.0
  attr = dict()
  attr['dt'] = 1/7.5
  attr['attitude'] = np.array([0.0, 0.0, 0.0])
  attr['position'] = np.array([0.0, 0.0, 0.0])
  attr['u0'] = 20.0

  action_in = np.array([20.0, 0.0, 0.0, 0.0, 0.0, 0.0])
  # wp_in     = np.array([0.0, 0.0, -0.0, 13.88, 50.0, -1.0])
  wp_in     = np.array([500.0, 0.0, -50.0, 20.0, 100.0, 1.0])

  coyote1 = uav_model_wrapper(attr)
  time  = []
  pN    = []
  pE    = []
  Alt   = []
  phi   = []
  theta = []
  psi   = []
  u     = []
  yawrate=[]
  p     = []
  q     = []
  EndTime = 10.0
  for i in range(int(EndTime / attr['dt'])):
    Time = i * attr['dt']

    # if (Time < 1.0):
    #   action_in = np.array([20.0, 0.0, 0.0, 45.0*D2R, 0.0, 0.0])
    # else:
    #   action_in = np.array([20.0, 0.0, 0.0, 0.0, 10.0*D2R, 10.0*D2R])

    # coyote1.set_raw_action(action_in)
    coyote1.set_wp_action(wp_in)
    coyote1.step()
    outputs = coyote1.get_all_state()


    # For Drawing
    time.append(      Time)
    pN.append(        outputs[0])
    pE.append(        outputs[1])
    Alt.append(      -outputs[2])
    phi.append(       outputs[3])
    theta.append(     outputs[4])
    psi.append(       outputs[5])
    u.append(         outputs[9])
    yawrate.append(   outputs[14])
    p.append(         outputs[15])
    q.append(         outputs[16])
    # print(Time,       outputs[0], outputs[1], -outputs[2],  outputs[3], outputs[4], outputs[5],
    #                   outputs[9], outputs[14], outputs[15], outputs[16])
    if (Time >= EndTime):
      break
  print("Loop End")
  
  fig1 = plt.figure(1,figsize=(8,6))
  plt.subplot(3,3,1); plt.plot(pN,              pE); plt.xlabel('pN [m]');         plt.ylabel('pE [m]'); plt.grid()
  # plt.plot(wp_in[0], wp_in[1], color='red',marker='p')
  plt.subplot(3,3,2); plt.plot(time,           Alt); plt.xlabel('Time [sec]');     plt.ylabel('H [m]');  plt.grid(); plt.xlim(0, time[-1])
  # plt.plot([time[0], time[-1]], [-wp_in[2], -wp_in[2]], color='red')
  plt.subplot(3,3,3); plt.plot(time,             u); plt.xlabel('Time [sec]');     plt.ylabel('u [m/s]'); plt.grid(); plt.xlim(0, time[-1])

  plt.subplot(3,3,4); plt.plot(time, np.rad2deg(p)); plt.xlabel('Time [sec]');     plt.ylabel('p [deg/s]'); plt.grid(); plt.xlim(0, time[-1])
  plt.subplot(3,3,5); plt.plot(time, np.rad2deg(q)); plt.xlabel('Time [sec]');     plt.ylabel('q [deg/s]'); plt.grid(); plt.xlim(0, time[-1])

  plt.subplot(3,3,6); plt.plot(time,np.rad2deg(yawrate)); plt.xlabel('Time [sec]');plt.ylabel('yawrate [deg/s]');  plt.grid(); plt.xlim(0, time[-1])

  plt.subplot(3,3,7); plt.plot(time,   np.rad2deg(phi)); plt.xlabel('Time [sec]'); plt.ylabel('phi [deg]'); plt.grid(); plt.xlim(0, time[-1])
  plt.subplot(3,3,8); plt.plot(time, np.rad2deg(theta)); plt.xlabel('Time [sec]'); plt.ylabel('theta [deg]'); plt.grid(); plt.xlim(0, time[-1])
  plt.subplot(3,3,9); plt.plot(time,   np.rad2deg(psi)); plt.xlabel('Time [sec]'); plt.ylabel('psi [deg]'); plt.grid(); plt.xlim(0, time[-1])
  plt.tight_layout()

  fig2 = plt.figure(2,figsize=(8,6))
  ax = plt.axes(projection='3d')
  ax.plot3D(pN, pE, np.zeros(np.size(Alt)),'red')
  ax.plot3D(pN, pE, Alt ,'blue')
  ax.set_xlabel('pN [m]'); ax.set_xlim(0, 400)
  ax.set_ylabel('pE [m]'); ax.set_ylim(-150, 150)
  ax.set_zlabel('H [m]');  ax.set_zlim(-100, 200)
  ax.invert_xaxis()
  ax.view_init(10,-45)
  plt.tight_layout()
  plt.show()

