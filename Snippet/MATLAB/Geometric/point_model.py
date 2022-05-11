import numpy as np
from scipy.spatial.transform import Rotation as R

attr_list = ('dt','attitude','position')
class point_model():
  def __init__(self, attr:dict):
    self.dt = 1/10
    self.state0 = dict()
    self.att = R.from_euler('xyz',[0, 0, 0], degrees=True)
    self.vB_in  = np.zeros((3)) # linear velocity on body frame
    self.wB_in  = np.zeros((3)) # angular velocity on body frame
    self.pN     = np.zeros((3)) # linear position on body frame
    self.vB     = np.zeros((3)) # linear velocity on body frame
    self.vN     = np.zeros((3)) # linear velocity on flat earth model
    self.wB     = np.zeros((3)) # angular velocity on body frame
    self.wE     = np.zeros((3)) # Euler rate

    if 'dt' in attr:
      self.dt = attr['dt']
      print("dT : ", self.dt)
    if 'attitude' in attr:
      euler = np.array(attr['attitude'])
      # euler = np.reshape(euler, (np.size(euler)))
      # euler = np.flip(euler, 0)
      self.att = R.from_euler('xyz',euler, degrees=True)
    if 'position' in attr:
      pN = np.array(attr['position'])
      pN = np.reshape(pN, (np.size(pN)))
      self.pN = pN

  def set_action(self, action_in):
    '''
      action item : [u,v,w,p,q,r]
    '''
    action = np.array(action_in)
    action = np.reshape(action, (np.size(action)))

    self.vB_in = np.reshape(action[:3], (3))
    self.wB_in = np.reshape(action[3:], (3))

  def step(self):
    R2D = 180.0 / np.pi
    vB = self.vB_in
    wB = self.wB_in
    euler = self.att.as_euler('xyz', degrees=False)
    vN    = np.dot(self.att.as_matrix(),vB)
    p = wB[0]; phi   = euler[0]
    q = wB[1]; theta = euler[1]
    r = wB[2]; psi   = euler[2]
    # print("RPY {:8.5f} {:8.5f} {:8.5f}".format(phi*R2D,theta*R2D,psi*R2D))
    wB2Euler = np.array([ [1, np.sin(phi)*np.tan(theta), np.cos(phi)*np.tan(theta)],
                          [0, np.cos(phi),              -np.sin(phi)],
                          [0, np.sin(phi)/np.cos(theta), np.cos(phi)/np.cos(theta)] ])
    wE    = np.dot(wB2Euler, wB)
    # Euler2wB = np.array([
    #   [1, 0,           -np.sin(theta)],
    #   [0, np.cos(phi),  np.cos(theta)*np.sin(phi)],
    #   [0,-np.sin(phi),  np.cos(theta)*np.cos(phi)]
    # ])

    if (True):
      quat = np.array(self.att.as_quat())
      quat = np.array([quat[3],quat[0],quat[1],quat[2]])
      quat = quat / np.linalg.norm(quat)
      u = np.concatenate((wB,quat))
      qdot = [- 0.5 * (u[4]*u[0] + u[5]*u[1] + u[6]*u[2]),
              + 0.5 * (u[3]*u[0] + u[5]*u[2] - u[6]*u[1]),
              + 0.5 * (u[3]*u[1] + u[6]*u[0] - u[4]*u[2]),
              + 0.5 * (u[3]*u[2] + u[4]*u[1] - u[5]*u[0])]
      qdot  = np.array([qdot[1],qdot[2],qdot[3],qdot[0]])
      quat  = np.array([quat[1],quat[2],quat[3],quat[0]])
      quat = quat    + self.dt * qdot
      quat = quat / np.linalg.norm(quat)
      self.att = R.from_quat(quat)
    else: # Euler Differential Equation
      phi   = phi   + wE[0] * self.dt
      theta = theta + wE[1] * self.dt
      psi   = psi   + wE[2] * self.dt
      euler = np.array([phi, theta, psi])
      self.att = R.from_euler('xyz',euler, degrees=False)
      
    pN   = self.pN + self.dt * vN
    # State Output
    self.pN = pN; 
    self.vN = vN; self.vB = vB
    self.wE = wE; self.wB = wB

  def get_state(self):
    tmp = np.concatenate((self.vB, self.wB))
    return tmp

  def get_all_state(self):
    test = self.att.as_euler('xyz', degrees=False)
    # test = np.flip(test, 0)
    tmp = np.concatenate((self.pN, test,
                          self.vN, self.vB,
                          self.wE, self.wB))
    return tmp
    
if __name__ == "__main__":
  attr = dict()
  attr['dt'] = 0.1

  model1 = point_model(attr)

