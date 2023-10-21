import matplotlib.pyplot as plt
import control as ctrl
import numpy as np

def show_bode_plot(model, fignum = 1, margin:bool = False):
    mag, phase, omega = ctrl.bode_plot(model, plot=False)

    fig = plt.figure(fignum)
    fig.clf()
    ax1 = fig.add_subplot(211)
    ax1.semilogx(omega, 20*np.log10(mag))
    ax1.set_xlim([omega[0], omega[-1]])
    ax1.set_ylabel('Magnitude [dB]'); ax1.grid()

    ax2 = fig.add_subplot(212)
    ax2.semilogx(omega, np.rad2deg(phase))
    ax2.set_xlim([omega[0], omega[-1]])
    ax2.set_xlabel('Omega [rad/s]'); ax2.set_ylabel('Phase [deg]'); ax2.grid()

    ax1.semilogx([omega[0], omega[-1]], [0, 0],'k:') # Zero-Crossing Line

    if(margin == True):
        gm, pm, wcg, wcp = ctrl.margin(model)
        if(not np.isinf(pm) or not np.isinf(gm)):
            phase_limit = np.ceil(np.min(phase)/(2*np.pi))*360 - 180
            ax2.semilogx([omega[0], omega[-1]],[phase_limit, phase_limit], 'k:') # Imaginary line
        if(not np.isinf(gm)):
            ax1.semilogx([wcg], [-20*np.log10(gm)], 'or', markersize=2)
            ax1.semilogx([wcg, wcg], [0, -20*np.log10(gm)], 'k:') # perpendicular line @ phase margin
            ax2.semilogx([wcg], [phase_limit], 'or', markersize=2) # perpendicular line @ phase margin
            ax1.set_title("Gm {:.2f} dB @ {:.1f} rad/s".format(20*np.log10(gm), wcg))
        if(not np.isinf(pm)):
            ax1.semilogx([wcp], [0], 'or', markersize=2) # Gain cross-over point
            ax2.semilogx([wcp], [phase_limit+pm], 'or', markersize=2) # Phase margin point
            ax2.semilogx([wcp, wcp], [phase_limit, phase_limit+pm], 'k:') # perpendicular line @ phase margin
            ax2.set_title("Pm {:.2f} deg @ {:.1f} rad/s".format(pm, wcp))
    plt.tight_layout()

def design_pid(model, pid_type, wco_target, pm_target=None):
    '''
        model : Linear system model
        pid_type ::

            p
            pi
            pd
            pid
            
        wco_target : Gain cross-over frequency
        pm_target : Phase margin for pi, pd
    '''
    gm, pm, wcg, wcp = ctrl.margin(model) # _, deg, rad/s, rad/s
    mag, phase, omega = ctrl.freqresp(model, wco_target)
    _, phase_end, _ = ctrl.freqresp(model, wco_target*100)
    print("phase {:.2f} deg @ wco {:.2f} rad/s".format(np.rad2deg(phase[0]), wco_target))

    if(pid_type.lower() == 'p'):
        kp  = 1 / mag[0]
        Gc  = kp
        print("[Designer] P    = kp {:.3f}".format(kp))
        print(Gc)
        return Gc, kp
    
    elif(pid_type.lower() == 'pi'):
        phase_limit = np.ceil(np.min(phase_end)/(2*np.pi))*360 - 180
        taui= 1 / (wco_target * np.tan(np.deg2rad((np.rad2deg(phase[0]) + phase_limit) - pm_target)))
        kp  = 1 / (mag[0] * np.linalg.norm([1, 1/(taui * wco_target)]))
        ki  = kp / taui
        Gc  = kp * ctrl.tf([taui, 1],[taui, 0])
        print("[Designer] PI   = kp {:.3f} ki {:.3f} taui {:.3f}".format(kp, ki, taui))
        print(Gc)
        if(taui < 0):
            _, now_pm, _ = ctrl.freqresp(model/mag[0], wco_target)
            assert False, "[Designer] Failed to design PI : PM should be under {:.2f} deg".format(np.rad2deg(now_pm[0])+phase_limit)
        return Gc, kp, ki

    elif(pid_type.lower() == 'pd'):
        phase_limit = np.ceil(np.min(phase_end)/(2*np.pi))*360 - 180
        taud= np.tan(np.deg2rad((-np.rad2deg(phase[0]) + phase_limit) + pm_target))/wco_target
        kp  = 1 / (mag[0] * np.linalg.norm([1, (taud * wco_target)]))
        kd  = kp / taud
        Gc  = kp * ctrl.tf([taud, 1],[1])
        print("[Designer] PD   = kp {:.3f} kd {:.3f} taud {:.3f}".format(kp, kd, taud))
        print(Gc)
        if(taud < 0):
            _, now_pm, _ = ctrl.freqresp(model/mag[0], wco_target)
            assert False, "[Designer] Failed to design PD : PM should be under {:.2f} deg".format(np.rad2deg(now_pm[0])+phase_limit)
        return Gc, kp, ki