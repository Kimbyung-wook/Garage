from matplotlib import projections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pth
import mpl_toolkits.mplot3d.art3d as art3d
import math
from scipy.spatial.transform import Rotation as R
from drawnow import *
import copy

class quadrotor_visualizer():
    def __init__(self):
        self.pn = 0
        self.pe = 0
        self.pd = 0
        self.R = R.from_euler('xyz',(0,0,0), degrees=False)
        ct = [  4,  0,  0.0]
        r  = 4
        self.arm    =[[  ct,
                        [ct[0]+r,ct[1],  0.0],
                        [     10,   10,  0.0],
                        [ct[0]  ,    r,  0.0],
                        ct],
                      [  ct,
                        [ct[0]+r,ct[1],  0.0],
                        [     10,  -10,  0.0],
                        [ct[0]  ,   -r,  0.0],
                        ct],
                      [  ct,
                        [ct[0]-r,ct[1],  0.0],
                        [    -10,  -10,  0.0],
                        [ct[0]  ,   -r,  0.0],
                        ct],
                      [  ct,
                        [ct[0]-r,ct[1],  0.0],
                        [    -10,   10,  0.0],
                        [ct[0]  ,    r,  0.0],
                        ct]]
        # print(self.arm, len(self.arm))
        for i in range(len(self.arm)):
            self.arm[i] = np.array(self.arm[i]) / 10
        # print(self.arm, len(self.arm))
        self.fig = plt.figure(3)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.x_min = -10; self.x_max = 10
        self.y_min = -10; self.y_max = 10
        self.z_min = -10; self.z_max = 10
        self.do_focus_on_it = False
        self.title = None
        
    def set_position(self, pn,pe,pd):
        self.pn = pn
        self.pe = pe
        self.pd = pd
        
    def set_attitude(self, roll, pitch, yaw):
        self.R = R.from_euler('xyz',[roll, pitch, yaw], degrees=False)
        # print('input : ',yaw)
    
    def show_fig(self):
        drawnow(self._make_figure)    
    
    def _make_figure(self):
        self.fig = plt.figure(3)
        self.ax = self.fig.add_subplot(111, projection='3d')
        pn = self.pn
        pe = self.pe
        pd = self.pd
        euler = self.R.as_euler('xyz',degrees=False)
        roll    = euler[0]
        pitch   = euler[1]
        yaw     = euler[2]
        # print('real : ',yaw)
        cg = np.array([pn, pe, pd])
        euler = np.array([roll, pitch, yaw])
        arm = copy.deepcopy(self.arm)
        
        mat = self.R.as_matrix()
        for i in range(len(arm)):
            for j in range(len(arm[i])):
                # arm[i][j] = np.transpose(mat * np.transpose(arm[i][j]))
                arm[i][j] = np.dot(mat,arm[i][j])
        
        for i in range(len(arm)):
            arm[i] = cg + arm[i]
        # lf_arm = np.transpose(mat * np.transpose(lf_arm))
        # rf_arm = np.transpose(mat * np.transpose(rf_arm))
        # rb_arm = np.transpose(mat * np.transpose(rb_arm))
        # lb_arm = np.transpose(mat * np.transpose(lb_arm))
        
        
        for i in range(len(arm)):
             self.ax.add_collection(art3d.Poly3DCollection([list(arm[i])]))

        # self.ax.set_xlim(-10, 10)
        # self.ax.set_ylim(-10, 10)
        # self.ax.set_zlim(-10, 10)
        if (self.do_focus_on_it == True):
            self.ax.set_xlim(self.pn-5, self.pn+5)
            self.ax.set_ylim(self.pe-5, self.pe+5)
            self.ax.set_zlim(self.pd-5, self.pd+5)
        else:
            self.ax.set_xlim(self.x_min, self.x_max)
            self.ax.set_ylim(self.y_min, self.y_max)
            self.ax.set_zlim(self.z_min, self.z_max)
        if(self.title != None):
            self.ax.set_title(self.title)
        # plt.show()
        
    def focus_on_it(self):
        self.do_focus_on_it = True
        
    def focus_off(self):
        self.do_focus_on_it = False
    
    def set_view(self,x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_min = x_min; self.x_max = x_max
        self.y_min = y_min; self.y_max = y_max
        self.z_min = z_min; self.z_max = z_max
        
    def set_title(self, title):
        self.title = title
    
    
    
    
    
if __name__ == '__main__':
    
    model = quadrotor_visualizer()
    
    angle = 0
    while(True):
        angle = angle + 10 * np.pi/180.0
        # angle = math.remainder(angle + np.pi, 2*np.pi) - np.pi
        model.set_attitude(0,0,angle)
        model.set_position(np.cos(angle),np.sin(angle),0)
        # model._make_figure()
        model.show_fig()