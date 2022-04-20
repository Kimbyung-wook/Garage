import numpy as np
from scipy.spatial.transform import Rotation as R

class model_2d():
  def __init__(self):
    self.pN = np.array([0.0, 0.0, 0.0])
    self.att = R.from_euler()