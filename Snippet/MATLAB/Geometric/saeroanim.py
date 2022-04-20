%matplotlib tk
import matplotlib.pyplot as plt
import numpy as np
from drawnow import *

class saeroanim():
  def __init__(self):
    self.fig = plt.figure(1)
    self.pN = []
    self.pE = []
    self.H = []

    

  def draw(self, pN, pE, pD, phi, theta, psi):
    self.pN.append(pN)
    self.pE.append(pE)
    self.H.append(-pD)

