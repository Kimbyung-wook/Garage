import numpy as np
from scipy.spatial.transform import Rotation as R

attr_list = ('dt','attitude','position')
class point_model():
  def __init__(self, attr:dict):
    self.dt = 1/10
    self.state0 = dict()
    self.att = R.from_euler('zyx',[0, 0, 0], degrees=True)
    self.vB_in  = np.zeros((3)) # linear velocity on body frame
    self.wB_in  = np.zeros((3)) # angular velocity on body frame
    self.pN     = np.zeros((3)) # linear position on body frame
    self.vB     = np.zeros((3)) # linear velocity on body frame
    self.vN     = np.zeros((3)) # linear velocity on flat earth model
    self.wB     = np.zeros((3)) # angular velocity on body frame
    self.wE     = np.zeros((3)) # Euler rate

    if 'dt' in attr:
      self.dt = attr['dt']
    if 'attitude' in attr:
      euler = np.array(attr['attitude'])
      euler = np.reshape(euler, (np.size(euler)))
      euler = np.flip(euler, 0)
      self.att = R.from_euler('zyx',euler, degrees=True)
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
    vB = self.vB_in
    wB = self.wB_in
    euler = np.array(self.att.as_euler('xyz'))
    p = wB[0]; phi   = euler[0]
    q = wB[1]; theta = euler[1]
    r = wB[2]; psi   = euler[2]
    quat = np.array(self.att.as_quat())
    quat = np.array([quat[3],quat[0],quat[1],quat[2]])
    w4   = np.array([ [ 0, p, q, r],
                      [-p, 0,-r, q],
                      [-q, r, 0,-p],
                      [-r,-q, p, 0] ])
    Euler2wB = np.array([ [1, np.sin(phi)*np.tan(theta), np.cos(phi)*np.tan(theta)],
                          [0, np.cos(phi),              -np.sin(phi)],
                          [0, np.sin(phi)/np.cos(theta), np.cos(phi)/np.cos(theta)] ])
    qdot  = - 0.5 * np.dot(w4, quat)
    qdot  = np.array([qdot[1],qdot[2],qdot[3],qdot[0]])
    quat  = np.array([quat[1],quat[2],quat[3],quat[0]])
    wE    = np.dot(Euler2wB, wB)
    vN    = np.dot(self.att.as_matrix(),vB)

    # Differential Equation
    pN   = self.pN + self.dt * vN
    quat = quat    + self.dt * qdot
    quat = quat / np.linalg.norm(quat)
    # print('pN ', pN)
    
    # State Output
    vB   = self.vB_in
    wB   = self.wB_in
    self.pN = pN; self.att= R.from_quat(quat)
    self.vN = vN; self.vB = vB
    self.wE = wE; self.wB = wB

  def get_state(self):
    tmp = np.concatenate((self.vB, self.wB))
    return tmp

  def get_all_state(self):
    tmp = np.concatenate((self.pN, self.att.as_euler('xyz'),
                          self.vN, self.vB,
                          self.wE, self.wB))
    return tmp
    
if __name__ == "__main__":
  attr = dict()
  attr['dt'] = 0.1

  model1 = point_model(attr)

