import matplotlib.pyplot as plt
# from control.matlab import *
import control as ctrl
import numpy as np
from control_lib import *

# 1st-order model
mag = 2
tau = 0.1
# model = ctrl.tf([mag], [tau, 1])

# 2nd-order model
# mag = 2
# wn = 10
# zeta = 1
# model = ctrl.tf([mag*wn*wn], [1, 2*zeta*wn, wn*wn])

# 3rd-order model
mag = 2
tau = 1
wn = 10
zeta = 1
model = ctrl.tf([mag*wn*wn], [1, 2*zeta*wn, wn*wn]) * ctrl.tf([mag], [tau, 1])

mag, phase, omega = ctrl.bode_plot(model, plot=False, margins=True)
gm, pm, wcg, wcp = ctrl.margin(model)
print("Gain cross  : {:6.2f} dB  at {:6.2f} rad/s".format(20*np.log10(gm), wcg))
print("Phase cross : {:6.2f} deg at {:6.2f} rad/s".format(pm, wcp))

wco_target=wcg/6
Gc, kp, ki = design_pid(model=model, pid_type='pi', wco_target=wco_target, pm_target=60)
mag, phase, omega = ctrl.bode_plot(model*Gc, plot=False, margins=True)

show_bode_plot(model, fignum=1, margin=True)
show_bode_plot(model*Gc, fignum=2, margin=True)

#####################################################################
# Step response
end_time = 5
t1, y1 = ctrl.step_response(model, end_time)
t2, y2 = ctrl.step_response(ctrl.feedback(model*Gc), end_time)
fig = plt.figure(10)
ax = fig.add_subplot(111)
ax.plot(t1, y1)
ax.plot(t2, y2)
ax.set_xlabel('Time [sec]'); ax.set_ylabel('Amplitude'); ax.grid()
ax.legend(['Model','Feedback'])

plt.tight_layout()
plt.show()