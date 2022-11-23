import os
import csv
from struct import Struct
import numpy as np
import pandas as pd
from misc import FILENAME, LIST_FOR_LOADING_FW
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils import quat2euler
from show_model import quadrotor_visualizer
import argparse, textwrap
import copy
from dataclasses import dataclass

class TimeInfo:
    StartTime:float = None
    EndTime:float = None
    MinMax:float = None

def get_all_of_data(target_file_name, option_range):
    # scrap data
    path_dir = './data'
    file_list = os.listdir(path_dir)

    tmp1 = {}
    table = dict()
    table_out = dict()
    min_basetime = 0.0
    max_basetime = 0.0
    if len(file_list) == 0:
        print('Forder is empty')
        exit()
    else:
        for file_name in file_list:
            if(target_file_name not in file_name):
                print("{} not int {} ".format(target_file_name, file_name))
                continue
            target_file = path_dir + '/' + file_name
            for idx in range(len(LIST_FOR_LOADING_FW)):
                key = LIST_FOR_LOADING_FW[idx]
                if(file_name.find(key+'_0') != -1):
                    # print('Find key : {:30} -> {:50}'.format(key, file_name), end=' ')
                    with open(target_file, 'r') as loaded_file:
                        # loaded_data = csv.reader(loaded_file, delimiter=',')
                        loaded_data = pd.read_csv(filepath_or_buffer=target_file,
                                                    sep=",",
                                                    # keep_default_na=False,
                                                    )
                        tmp = np.transpose(loaded_data.values)
                        table[key] = {}
                        for i in range(len(loaded_data.columns)):
                            str_idx = str(loaded_data.columns[i])
                            if(key == 'position_setpoint_triplet'):
                                table[key][str_idx] = tmp[i]
                            else:
                                table[key][str_idx] = tmp[i][1:]

                        table[key]['timestamp'] = table[key]['timestamp'] * 1e-6
                            
                        if(key == 'angular_velocity'): # rates_setpoint
                            alpha = 0.3
                            print(len(table[key]['xyz[0]']))
                            p_filt = [table[key]['xyz[0]'][0],]
                            q_filt = [table[key]['xyz[1]'][0],]
                            r_filt = [table[key]['xyz[2]'][0],]
                            for i in range(len(table[key]['xyz[0]'])):
                                if (i != 0):
                                    # print(i, p_filt)
                                    # print(p_filt[i-1], table[key]['xyz[0]'][i])
                                    p_filt.append((1 - alpha) * p_filt[i-1] + alpha * table[key]['xyz[0]'][i])
                                    q_filt.append((1 - alpha) * q_filt[i-1] + alpha * table[key]['xyz[1]'][i])
                                    r_filt.append((1 - alpha) * r_filt[i-1] + alpha * table[key]['xyz[2]'][i])

                            table[key]['fxyz[0]'] = p_filt
                            table[key]['fxyz[1]'] = q_filt
                            table[key]['fxyz[2]'] = r_filt
                            
                        if(key == 'attitude'): # attitude
                            roll, pitch, yaw = quat2euler(table[key]['q[0]'],table[key]['q[1]'],table[key]['q[2]'],table[key]['q[3]'])
                            table[key]['roll_body'] = roll
                            table[key]['pitch_body'] = pitch
                            table[key]['yaw_body'] = yaw
                            
                        # elif(key == LIST_FOR_LOADING_FW[4]): # attitude_setpoint
                        elif(key == 'wind'):
                            wind_direction = np.arctan2(table[key]['windspeed_east'],table[key]['windspeed_north'])
                            wind_speed = np.sqrt(table[key]['windspeed_north'] * table[key]['windspeed_north'] + table[key]['windspeed_east'] * table[key]['windspeed_east'])
                            table[key]['wind_direction'] = wind_direction
                            table[key]['wind_speed_m_s'] = wind_speed
                            
                        elif(key == 'local_position'): # local_position
                            course = np.arctan2(table[key]['vy'],table[key]['vx'])
                            ground_speed = np.sqrt(table[key]['vy'] * table[key]['vy'] + table[key]['vx'] * table[key]['vx'])
                            fpa = -np.arctan2(table[key]['vz'], np.max([7, ground_speed.all()]))
                            table[key]['courseangle'] = course
                            table[key]['ground_speed_m_s'] = ground_speed
                            table[key]['fpa'] = fpa
                        
                        # elif(key == 'position_setpoint_triplet'):
                        #     print(table[key]['timestamp'])
                            
                        # Search Timeseries
                        # if(key == 'position_setpoint_triplet'):
                        #     min_time = min_basetime
                        # else:
                        min_time = min(table[key]['timestamp'])

                        if (min_basetime <= 0.1):
                            min_basetime = copy.deepcopy(min_time)
                        else:
                            min_basetime = copy.deepcopy(min([min_basetime, min_time]))
                            
                        max_time = max(table[key]['timestamp'])
                        if (max_basetime <= 0.1):
                            max_basetime = copy.deepcopy(max_time)
                        else:
                            max_basetime = copy.deepcopy(max([max_basetime, max_time]))
                            
                        table[key]['time_minmax'] = [min_time, max_time]
                        # print('/ {:.3f} ~ {:.3f}'.format(min_time, max_time))
                        
    # print('log_range : {:.3f} ~ {:.3f}'.format(min_basetime, max_basetime))
                    
    # Get Time Range : based on FCC Clock
    time_info = TimeInfo()
    time_info.StartTime = min_basetime
    time_info.EndTime   = min_basetime
    if(args.range != None):
        # Check min/max range to show
        max_log_range = max_basetime - min_basetime
        option_log_range = [np.float64(float(option_range[0])) + min_basetime, np.float64(float(option_range[1]) + min_basetime)]
        min_option_log_range = max([0.0, option_log_range[0]])
        max_option_log_range = option_log_range[1]
        print("log {:.3f} ~ {:.3f} / option {:.3f} ~ {:.3f}".format(min_basetime, max_basetime, option_log_range[0], option_log_range[1]))
        
        if(max_option_log_range > max_basetime):
            print("[WARNING] max time of range is too high : {:.3f} -> {:.3f}".format(max_option_log_range, max_log_range + min_basetime))
            max_option_log_range = max_log_range + min_basetime
        time_info.MinMax    = [min_option_log_range, max_option_log_range]
        
        # Identify min/max index and copy them
        for key1 in table.keys():
            min_idx, max_idx = search_time_idx(table[key1]['timestamp'], time_info)
            table_out[key1] = {}
            table_out[key1]['idx_minmax']  = copy.deepcopy([min_idx, max_idx])
            table_out[key1]['time_minmax'] = copy.deepcopy([table[key1]['timestamp'][min_idx], table[key1]['timestamp'][max_idx]])
            for key2 in table[key1].keys():
                if((key2 == 'idx_minmax') or (key2 == 'time_minmax')):
                    continue
                table_out[key1][key2] = table[key1][key2][min_idx:(max_idx+1)]
    else:
        time_info.MinMax    = [min_basetime, max_basetime]
        table_out = table
        for key1 in table.keys():
            table_out[key1]['idx_minmax']  = [0, len(table[key1]['timestamp'])-1]
            table_out[key1]['time_minmax'] = [table_out[key1]['timestamp'][table_out[key1]['idx_minmax'][0]],
                                              table_out[key1]['timestamp'][table_out[key1]['idx_minmax'][1]]]
        
    time_info.MinMax = copy.deepcopy([time_info.MinMax[0] - min_basetime, time_info.MinMax[1] - min_basetime])
    print("[INFO] Time Range : {:.3f}s -> {:.3f}s (for {:.3f}s)".format(time_info.MinMax[0], time_info.MinMax[1],
                                                                        time_info.MinMax[1]- time_info.MinMax[0]))
    
    print('         : keys                                     -> file name                                                    (  First [idx] ~      Last [   idx] ) -> (    Begin [   idx] ~       End [   idx])')
    for file_name in file_list:
        target_file = path_dir + '/' + file_name
        for idx in range(len(LIST_FOR_LOADING_FW)):
            key = LIST_FOR_LOADING_FW[idx]
            # if(key == 'position_setpoint_triplet'):
            #     continue
            if(file_name.find(key+'_0') != -1):
                print('Find key : {:40} -> {:60}'.format(key, file_name), end=' ')
                print('({:10.3f}[{:1d}] ~ {:10.3f}[{:6d}]) -> '.format(table[key]['time_minmax'][0], 0,
                                                                       table[key]['time_minmax'][1], len(table[key]['timestamp'])-1), end=' ')
                print('({:10.3f}[{:6d}] ~ {:10.3f}[{:6d}])'.format(    table_out[key]['time_minmax'][0], table_out[key]['idx_minmax'][0],
                                                                       table_out[key]['time_minmax'][1], table_out[key]['idx_minmax'][1]))
    

    return table_out, time_info

def search_time_idx(time_series, time_info):
    min_idx = 0
    max_idx = 0
    for i in range(len(time_series)):
        now_time = time_series[i]
        if now_time < time_info.MinMax[0]:
            min_idx = copy.deepcopy(i)
        if now_time < time_info.MinMax[1]:
            max_idx = copy.deepcopy(i)+1
    
    min_range_is_under_log = time_info.MinMax[0] < min(time_series)
    max_range_is_under_log = time_info.MinMax[1] < min(time_series)
    min_range_is_over_log  = time_info.MinMax[0] > max(time_series)
    max_range_is_over_log  = time_info.MinMax[1] > max(time_series)
    
    if(min_range_is_under_log):
        min_idx = 0
        # print('min boom')
        if(max_range_is_under_log):
            max_idx = len(time_series)-1
            # print('OOR')
            
    if(max_range_is_over_log):
        max_idx = len(time_series)-1
        # print('max boom')
        if(min_range_is_over_log):
            min_idx = 0
            # print('OOR')
    
        
    # print("MinMax : {:10.3f} at {:6d} ~ {:10.3f} at idx {:6d}".format(time_series[min_idx], min_idx, time_series[max_idx], max_idx))
    
    return min_idx, max_idx

def show_roll(time_info, log):
    min_time = time_info.StartTime
    plt.plot((log['attitude']['timestamp'] - min_time),             np.degrees(log['attitude']['roll_body']),'b',linewidth=1)
    plt.plot((log['attitude_setpoint']['timestamp'] - min_time),    np.degrees(log['attitude_setpoint']['roll_body']),'r:',linewidth=1)
    plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('Roll [deg]')
    print(time_info.MinMax, len(time_info.MinMax))
    if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
def show_pitch(time_info, log):
    min_time = time_info.StartTime
    plt.plot((log['attitude']['timestamp'] - min_time),             np.degrees(log['attitude']['pitch_body']),'b',linewidth=1)
    plt.plot((log['attitude_setpoint']['timestamp'] - min_time),    np.degrees(log['attitude_setpoint']['pitch_body']),'r:',linewidth=1)
    plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('Pitch [deg]')
    if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
def show_yaw(time_info, log):
    min_time = time_info.StartTime
    plt.plot((log['attitude']['timestamp'] - min_time),             np.degrees(log['attitude']['yaw_body']),'b',linewidth=1)
    plt.plot((log['attitude_setpoint']['timestamp'] - min_time),    np.degrees(log['attitude_setpoint']['yaw_body']),'r:',linewidth=1)
    plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('Yaw [deg]')
    if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
    
def show_wx(time_info, log):
    min_time = time_info.StartTime
    plt.plot((log['angular_velocity']['timestamp'] - min_time),     np.degrees(log['angular_velocity']['xyz[0]']),'b',linewidth=1)
    plt.plot((log['rates_setpoint']['timestamp'] - min_time),       np.degrees(log['rates_setpoint']['roll']),'r:',linewidth=1)
    plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('RollRate [deg]');
    if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
def show_wy(time_info, log):
    min_time = time_info.StartTime
    plt.plot((log['angular_velocity']['timestamp'] - min_time),     np.degrees(log['angular_velocity']['xyz[1]']),'b',linewidth=1)
    plt.plot((log['rates_setpoint']['timestamp'] - min_time),       np.degrees(log['rates_setpoint']['pitch']),'r:',linewidth=1)
    plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('PitchRate [deg]');
    if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
def show_wz(time_info, log):
    min_time = time_info.StartTime
    plt.plot((log['angular_velocity']['timestamp'] - min_time),     np.degrees(log['angular_velocity']['xyz[2]']),'b',linewidth=1)
    plt.plot((log['rates_setpoint']['timestamp'] - min_time),       np.degrees(log['rates_setpoint']['yaw']),'r:',linewidth=1)
    plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('YawRate [deg]');
    if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
    
def show_px(time_info, log):
    min_time = time_info.StartTime
    plt.plot((log['local_position']['timestamp'] - min_time),           log['local_position']['x'],'b',linewidth=1)
    plt.plot((log['local_position_setpoint']['timestamp'] - min_time),  log['local_position_setpoint']['x'],'r:',linewidth=2)
    plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('pN [m]')
    if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
def show_py(time_info, log):
    min_time = time_info.StartTime
    plt.plot((log['local_position']['timestamp'] - min_time),           log['local_position']['y'],'b',linewidth=1)
    plt.plot((log['local_position_setpoint']['timestamp'] - min_time),  log['local_position_setpoint']['y'],'r:',linewidth=2)
    plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('pE [m]')
    if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
def show_pz(time_info, log):
    min_time = time_info.StartTime
    plt.plot((log['local_position']['timestamp'] - min_time),           -log['local_position']['z'],'b',linewidth=1)
    plt.plot((log['local_position_setpoint']['timestamp'] - min_time),  -log['local_position_setpoint']['z'],'r:',linewidth=2)
    plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('Alt [m]')
    if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
        
class shows():
    def __init__(self, options:dict):
        self.figure_no = 1
        self.options = options
        
    def show_local_traj(self, time_info, log):
        fig = plt.figure(self.figure_no)
        self.figure_no = self.figure_no + 1

        # Start-End Indicator
        plt.plot(log['vehicle_local_position']['y'][0] ,log['vehicle_local_position']['x'][0] ,'bo',linewidth=0.5)
        plt.plot(log['vehicle_local_position']['y'][-1],log['vehicle_local_position']['x'][-1],'bp',linewidth=0.5)
        plt.text(log['vehicle_local_position']['y'][0] ,log['vehicle_local_position']['x'][0] , "Start")
        plt.text(log['vehicle_local_position']['y'][-1],log['vehicle_local_position']['x'][-1], "End")
        # Flight Path
        plt.plot(log['vehicle_local_position']['y'],log['vehicle_local_position']['x'],'b',linewidth=0.5)
        # Setpoint Path
        wp_idx = 0
        prev_xy = np.array([0,0])
        if('vehicle_local_position_setpoint' in log.keys()):
            plt.plot(log['vehicle_local_position_setpoint']['y'],log['vehicle_local_position_setpoint']['x'],'r:',linewidth=0.3)
            
            for i in range(len(log['vehicle_local_position_setpoint']['y'])):
                now_xy = np.array([log['vehicle_local_position_setpoint']['y'][i],log['vehicle_local_position_setpoint']['x'][i]])
                dxy = now_xy - prev_xy
                dist = np.linalg.norm(dxy)
                if(dist > 1):
                    wp_idx = wp_idx + 1
                    plt.text(log['vehicle_local_position_setpoint']['y'][i],log['vehicle_local_position_setpoint']['x'][i], "{:d}".format(wp_idx))
                    plt.plot(log['vehicle_local_position_setpoint']['y'][i],log['vehicle_local_position_setpoint']['x'][i], 'ro',linewidth=0.5)

                    prev_xy = now_xy
        plt.grid()
        plt.ylabel('pN [m]'); plt.xlabel('pE [m]')
        plt.tight_layout()
        
        if('save' in self.options):
            name_for_saving = "imgs/Ulg_{:s}_T_{:}_{:}_LocalTraj2D.png".format(self.options['name'], int(self.options['range'][0]), int(self.options['range'][1]))
            fig.savefig(name_for_saving, dpi=300)

    def show_global_traj(self, time_info, log):
        fig = plt.figure(num=self.figure_no, figsize=(8,14), layout='tight')
        # fig = plt.figure(self.figure_no)
        self.figure_no = self.figure_no + 1

        min_time = time_info.StartTime

        ax = plt.subplot(4,1,(1,2)) # Top View - XY Trajectories
        # Building and Runway
        Building_Road =[[126.610394, 37.518957],
                        [126.610543, 37.518945],
                        [126.610761, 37.520149],
                        [126.610575, 37.520146]]
        Building = [[126.610793, 37.519302],
                    [126.611085, 37.519275],
                    [126.611128, 37.519494],
                    [126.610873, 37.519489]]
        Runways  = [[126.609116, 37.519378],
                    [126.609222, 37.519358],
                    [126.609458, 37.520185],
                    [126.609300, 37.520220]]
        ax.add_patch(patches.Polygon(Building_Road,color='Gray'))
        ax.add_patch(patches.Polygon(Building,color='Gray'))
        ax.add_patch(patches.Polygon(Runways,color='Green'))

        # Start-End Indicator
        plt.plot(log['vehicle_global_position']['lon'][0] ,log['vehicle_global_position']['lat'][0] , 'bo',linewidth=0.5)
        plt.plot(log['vehicle_global_position']['lon'][-1],log['vehicle_global_position']['lat'][-1], 'bp',linewidth=0.5)
        plt.text(log['vehicle_global_position']['lon'][0] ,log['vehicle_global_position']['lat'][0] , "Start")
        plt.text(log['vehicle_global_position']['lon'][-1],log['vehicle_global_position']['lat'][-1], "End")
        plt.plot(log['vehicle_global_position']['lon']    ,log['vehicle_global_position']['lat'],'b',linewidth=0.5)
        # Setpoint Path
        wp_idx = 0
        prev_radius = 0
        prev_xy = np.array([0,0])
        if('position_setpoint_triplet' in log.keys()):
            plt.plot(   log['position_setpoint_triplet']['current.lon'],
                        log['position_setpoint_triplet']['current.lat'],'r:',linewidth=0.3)
            
            for i in range(len(log['position_setpoint_triplet']['current.lat'])):
                cur_lon = log['position_setpoint_triplet']['current.lon'][i]
                cur_lat = log['position_setpoint_triplet']['current.lat'][i]
                now_xy = np.array([ log['position_setpoint_triplet']['current.lon'][i],
                                    log['position_setpoint_triplet']['current.lat'][i]])
                now_loiter_radius = log['position_setpoint_triplet']['current.loiter_radius'][i]
                now_accept_radius = log['position_setpoint_triplet']['current.acceptance_radius'][i]
                dxy = now_xy - prev_xy
                dist = np.linalg.norm(dxy)
                if(dist > 1e-6):
                    wp_idx = wp_idx + 1
                    plt.text(cur_lon, cur_lat, "{:d}".format(wp_idx))
                    plt.plot(cur_lon, cur_lat, 'ro',linewidth=0.5)
                    prev_xy = now_xy

                    radius_polar        = 6356752.3 # WGS84
                    radius_equatorial   = 6378137.0
                    angles = np.linspace(0, 360, num=12*3+1)
                    if(now_loiter_radius > 10):
                        circle_x = now_loiter_radius * np.cos(np.radians(angles))
                        circle_y = now_loiter_radius * np.sin(np.radians(angles))
                        circle_lat_x = cur_lat + np.degrees(circle_x * np.arctan2(1, radius_polar))
                        circle_lon_y = cur_lon + np.degrees(circle_y * np.arctan2(1, radius_equatorial * np.cos(np.radians(cur_lat))))
                        plt.plot(circle_lon_y, circle_lat_x,':', color='orange',linewidth=1)
                    if(now_accept_radius > 5):
                        circle_x = now_accept_radius * np.cos(np.radians(angles))
                        circle_y = now_accept_radius * np.sin(np.radians(angles))
                        circle_lat_x = cur_lat + np.degrees(circle_x * np.arctan2(1, radius_polar))
                        circle_lon_y = cur_lon + np.degrees(circle_y * np.arctan2(1, radius_equatorial * np.cos(np.radians(cur_lat))))
                        plt.plot(circle_lon_y, circle_lat_x, ':', color='red',linewidth=1)
        plt.grid()
        plt.xlabel('Lon [deg]'); plt.ylabel('Lat [deg]')
        
        plt.subplot(413)
        plt.plot(log['vehicle_global_position']['timestamp'] - min_time ,log['vehicle_global_position']['alt'] , 'b',linewidth=0.5)
        for i in range(len(log['position_setpoint_triplet']['current.lat'])-1):
            plt.text(log['position_setpoint_triplet']['timestamp'][i] - min_time, log['position_setpoint_triplet']['current.alt'][i], "{:d}".format(i+1))
            plt.plot(   [log['position_setpoint_triplet']['timestamp'][i] - min_time,   log['position_setpoint_triplet']['timestamp'][i+1] - min_time],
                        [log['position_setpoint_triplet']['current.alt'][i], log['position_setpoint_triplet']['current.alt'][i]], ':r',linewidth=1)

        plt.grid()
        plt.xlabel('Time [sec]'); plt.ylabel('Alt [m]')
            
        plt.tight_layout()
        
        if('save' in self.options):
            name_for_saving = "imgs/Ulg_{:s}_T_{:}_{:}_GlobalTraj2D.png".format(self.options['name'], int(self.options['range'][0]), int(self.options['range'][1]))
            fig.savefig(name_for_saving, dpi=300)

    def show_atti(self, time_info, log):
        plt.figure(self.figure_no)
        self.figure_no = self.figure_no + 1
        plt.title("Attitude - Euler")
        plt.subplot(311);    show_roll( time_info,  log)
        plt.subplot(312);    show_pitch(time_info,  log)
        plt.subplot(313);    show_yaw(  time_info,  log)
        plt.tight_layout()

    def show_rates(self, time_info, log):
        plt.figure(self.figure_no)
        self.figure_no = self.figure_no + 1
        plt.title("AngularRate")
        plt.subplot(311);    show_wx(time_info, log)
        plt.subplot(312);    show_wy(time_info, log)
        plt.subplot(313);    show_wz(time_info, log)
        plt.tight_layout()
        
    def show_attis(self, time_info, log):
        plt.figure(self.figure_no)
        self.figure_no = self.figure_no + 1
        plt.subplot(321);    show_roll( time_info,   log)
        plt.subplot(323);    show_pitch(time_info,   log)
        plt.subplot(325);    show_yaw(  time_info,   log)
        plt.subplot(322);    show_wx(   time_info,   log)
        plt.subplot(324);    show_wy(   time_info,   log)
        plt.subplot(326);    show_wz(   time_info,   log)
        plt.tight_layout()
        
    def show_local_traj_timeseries(self,  time_info, log):
        plt.figure(self.figure_no)
        self.figure_no = self.figure_no + 1
        plt.subplot(311);   show_px(time_info,   log)
        plt.subplot(312);   show_py(time_info,   log)
        plt.subplot(313);   show_pz(time_info,   log)
        plt.tight_layout()
        
    def _get_nav_state_string(self, nav_state):
        text_string = "NONE"
        if(nav_state == 0):
            text_string = "MANUAL"
        elif(nav_state == 1):
            text_string = "ALTCTL"
        elif(nav_state == 2):
            text_string = "POSCTL"
        elif(nav_state == 3):
            text_string = "AUTO.MISSION"
        elif(nav_state == 4):
            text_string = "AUTO.LOITER"
        elif(nav_state == 5):
            text_string = "AUTO.RTL"
        elif(nav_state == 14):
            text_string = "OFFBOARD"
        elif(nav_state == 15):
            text_string = "STAB"
        elif(nav_state == 17):
            text_string = "AUTO.TO"
        elif(nav_state == 18):
            text_string = "AUTO.LD"
        elif(nav_state == 20):
            text_string = "AUTO.PREC_LD"
        else:
            text_string = "NONE"
        return text_string        
        
    def _show_flightmode(self, time_info, log):
        min_time = time_info.StartTime
        nav_states = log['vehicle_status']['nav_state']
        for idx in range(len(nav_states)-1):
            if((idx == 0) or (nav_states[idx+1] != nav_states[idx])):
                text_string = self._get_nav_state_string(nav_states[idx+1])
                plt.text(log['vehicle_status']['timestamp'][idx+1] - min_time, nav_states[idx+1], text_string)
            
        plt.plot((log['commander_state']['timestamp'] - min_time),          log['commander_state']['main_state'],linewidth=1)
        plt.plot((log['vehicle_status']['timestamp'] - min_time),           log['vehicle_status']['nav_state'],linewidth=1)
        plt.plot((log['vehicle_status']['timestamp'] - min_time),           log['vehicle_status']['arming_state'],linewidth=1)
        
        plt.legend(['Mode','nav','Arm'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]')
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)

    def show_lon_ctrl(self, time_info, log):
        fig = plt.figure(num=self.figure_no, figsize=(8,14), layout='tight')
        self.figure_no = self.figure_no + 1

        min_time = time_info.StartTime
        plt.subplot(9,1,1)
        plt.title("Lon_Ctrl Analysis")
        self._show_flightmode(time_info, log)

        plt.subplot(9,1,(2,3)) # TECS
        # # Yaw, Yaw_setpoint, rudder
        plt.plot((log['tecs_status']['timestamp'] - min_time),          log['tecs_status']['altitude_filtered'],linewidth=1)
        plt.plot((log['tecs_status']['timestamp'] - min_time),          log['tecs_status']['altitude_sp'],linewidth=1)
        
        # plt.plot((log['manual_control_setpoint']['timestamp'] - min_time),  np.degrees(log['manual_control_setpoint']['r']),linewidth=1)
        # plt.plot((log['attitude']['timestamp'] - min_time),                 np.degrees(log['attitude']['yaw_body']),linewidth=1)
        # plt.plot((log['local_position']['timestamp'] - min_time),           np.degrees(log['local_position']['courseangle']),linewidth=1)
        # plt.plot((log['attitude_setpoint']['timestamp'] - min_time),        np.degrees(log['attitude_setpoint']['yaw_body']),'r:',linewidth=1)
        # plt.plot((log['angular_velocity']['timestamp'] - min_time),         np.degrees(log['angular_velocity']['xyz[2]']),linewidth=1)
        plt.legend(['Alt', 'Alt_sp'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('Alt [m]')
        # plt.ylim([-200, 200])
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
        
        plt.subplot(9,1,(4,5))  # Airspeed
        plt.plot((log['airspeed']['timestamp'] - min_time),         log['airspeed']['indicated_airspeed_m_s'],linewidth=1)
        plt.plot((log['airspeed']['timestamp'] - min_time),         log['airspeed']['true_airspeed_m_s'],linewidth=1)
        plt.plot((log['tecs_status']['timestamp'] - min_time),      log['tecs_status']['true_airspeed_sp'],linewidth=1)
        plt.plot((log['local_position']['timestamp'] - min_time),   log['local_position']['ground_speed_m_s'],linewidth=1)
        plt.plot((log['wind']['timestamp'] - min_time),             log['wind']['wind_speed_m_s'],linewidth=1)
        plt.plot((log['tecs_status']['timestamp'] - min_time),              log['tecs_status']['height_rate'],linewidth=1)
        plt.plot((log['tecs_status']['timestamp'] - min_time),              log['tecs_status']['height_rate_setpoint'],'r:',linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),log['actuator_controls']['control[3]']*10,linewidth=1)
        plt.plot((log['manual_control_setpoint']['timestamp'] - min_time), log['manual_control_setpoint']['z']*10,linewidth=1)
        plt.legend(['IAS','TAS', 'TAS_sp','GS','est.Wind', "VV", "VV_sp", 'Thr*10', 'RC Thr*10'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('TECS : Speed [m/s]')
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)

        plt.subplot(9,1,(6,7)) # Pitch Control
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        np.degrees(log['actuator_controls']['control[1]']),linewidth=1)
        plt.plot((log['manual_control_setpoint']['timestamp'] - min_time), -log['manual_control_setpoint']['x']*10,linewidth=1)
        plt.plot((log['attitude']['timestamp'] - min_time),                 np.degrees(log['attitude']['pitch_body']),linewidth=1)
        plt.plot((log['attitude_setpoint']['timestamp'] - min_time),        np.degrees(log['attitude_setpoint']['pitch_body']),'r:',linewidth=1)
        plt.plot((log['local_position']['timestamp'] - min_time),           np.degrees(log['local_position']['fpa']),linewidth=1)
        plt.legend(['Elv', '-RC pitch', 'pitch', 'pitch_sp','FPA'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('Lon [deg]')
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
        

        plt.subplot(9,1,(8,9)) # Angular rate
        plt.plot((log['angular_velocity']['timestamp'] - min_time),         np.degrees(log['angular_velocity']['xyz[1]']),linewidth=1)
        plt.plot((log['rates_setpoint']['timestamp'] - min_time),           np.degrees(log['rates_setpoint']['pitch']),'m:',linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        np.degrees(log['actuator_controls']['control[1]']),linewidth=1)
        plt.legend(['q','q_sp','Elv'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('AngularRate')
        # plt.ylim([-180, 180])
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
        
        if('save' in self.options):
            name_for_saving = "imgs/Ulg_{:s}_T_{:}_{:}_lon_ctrl.png".format(self.options['name'], int(self.options['range'][0]), int(self.options['range'][1]))
            fig.savefig(name_for_saving, dpi=300)
            
    def show_lat_ctrl(self, time_info, log):
        plt.figure(num=self.figure_no, figsize=(8,14), layout='tight')
        self.figure_no = self.figure_no + 1

        min_time = time_info.StartTime
        
        plt.subplot(9,1,1) # Flight States
        plt.title("Lat_Ctrl Analysis")
        self._show_flightmode(time_info, log)

        plt.subplot(9,1,(4,5)) # Angular rate
        plt.plot((log['angular_velocity']['timestamp'] - min_time),         np.degrees(log['angular_velocity']['xyz[0]']),linewidth=1)
        plt.plot((log['rates_setpoint']['timestamp'] - min_time),           np.degrees(log['rates_setpoint']['roll']),'m:',linewidth=1)
        plt.plot((log['angular_velocity']['timestamp'] - min_time),         np.degrees(log['angular_velocity']['xyz[2]']),linewidth=1)
        plt.plot((log['rates_setpoint']['timestamp'] - min_time),           np.degrees(log['rates_setpoint']['yaw']),'m:',linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        log['actuator_controls']['control[0]'],linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        log['actuator_controls']['control[2]'],linewidth=1)
        plt.legend(['p','p_sp', 'r', 'r_sp','Ail', 'Rud'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('AngularRate')
        # plt.ylim([-180, 180])
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)

        plt.subplot(9,1,(6,7)) # Roll Control
        # Manual Roll Input, Roll, Roll_setpoint, Actuator_output_0
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        log['actuator_controls']['control[0]'],linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        log['actuator_controls']['control[2]'],linewidth=1)
        plt.plot((log['manual_control_setpoint']['timestamp'] - min_time),  log['manual_control_setpoint']['y'],linewidth=1)
        plt.plot((log['manual_control_setpoint']['timestamp'] - min_time),  log['manual_control_setpoint']['r'],linewidth=1)
        plt.plot((log['attitude']['timestamp'] - min_time),                 np.degrees(log['attitude']['roll_body']),linewidth=1)
        plt.plot((log['attitude_setpoint']['timestamp'] - min_time),        np.degrees(log['attitude_setpoint']['roll_body']),'r:',linewidth=1)
        plt.legend(['Ail', 'Rud', 'RC phi', 'RC psi', 'phi', 'phi_sp'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('Lat [deg]')
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)

        plt.subplot(9,1,(8,9)) # Heading Control
        # Yaw, Yaw_setpoint, rudder
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        log['actuator_controls']['control[2]'],linewidth=1)
        plt.plot((log['manual_control_setpoint']['timestamp'] - min_time),  log['manual_control_setpoint']['r'],linewidth=1)
        plt.plot((log['attitude']['timestamp'] - min_time),                 np.degrees(log['attitude']['yaw_body']),linewidth=1)
        plt.plot((log['local_position']['timestamp'] - min_time),           np.degrees(log['local_position']['courseangle']),linewidth=1)
        plt.plot((log['attitude_setpoint']['timestamp'] - min_time),        np.degrees(log['attitude_setpoint']['yaw_body']),'r:',linewidth=1)
        plt.plot((log['angular_velocity']['timestamp'] - min_time),         np.degrees(log['angular_velocity']['xyz[2]']),linewidth=1)
        plt.legend(['Rud', 'RC psi','course', 'psi', 'psi_sp','r'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('Dir [deg]')
        plt.ylim([-200, 200])
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)

    def show_lat_ctrl_zoom(self, time_info, log):
        fig = plt.figure(num=self.figure_no, figsize=(8,14), layout='tight')
        self.figure_no = self.figure_no + 1

        min_time = time_info.StartTime
        plt.subplot(9,1,1)
        plt.title("Lat_Ctrl Analysis - Zoom")
        self._show_flightmode(time_info, log)

        plt.subplot(9,1,(4,5))
        scaler = 50
        plt.plot((log['angular_velocity']['timestamp'] - min_time),         np.degrees(log['angular_velocity']['xyz[0]']),linewidth=1)
        plt.plot((log['angular_velocity']['timestamp'] - min_time),         np.degrees(log['angular_velocity']['fxyz[0]']),linewidth=1)
        plt.plot((log['rates_setpoint']['timestamp'] - min_time),           np.degrees(log['rates_setpoint']['roll']),'m:',linewidth=1)
        # plt.plot((log['angular_velocity']['timestamp'] - min_time),         np.degrees(log['angular_velocity']['xyz[2]']),linewidth=1)
        # plt.plot((log['rates_setpoint']['timestamp'] - min_time),           np.degrees(log['rates_setpoint']['yaw']),'m:',linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        log['actuator_controls']['control[0]']*scaler,linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        log['actuator_controls']['control[2]']*scaler,linewidth=1)
        # plt.legend(['p','p_sp', 'r', 'r_sp','Ail*50', 'Rud*50'],loc='upper right')
        plt.legend(['p','p_filtered','p_sp', 'Ail*50', 'Rud*50'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('AngularRate')
        # plt.ylim([-180, 180])
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)

        plt.subplot(9,1,(6,7))
        # Manual Roll Input, Roll, Roll_setpoint, Actuator_output_0
        scaler = 30
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        log['actuator_controls']['control[0]']*scaler,linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        log['actuator_controls']['control[2]']*scaler,linewidth=1)
        plt.plot((log['manual_control_setpoint']['timestamp'] - min_time),  log['manual_control_setpoint']['y']*scaler,linewidth=1)
        plt.plot((log['manual_control_setpoint']['timestamp'] - min_time),  log['manual_control_setpoint']['r']*scaler,linewidth=1)
        plt.plot((log['attitude']['timestamp'] - min_time),                 np.degrees(log['attitude']['roll_body']),linewidth=1)
        plt.plot((log['attitude_setpoint']['timestamp'] - min_time),        np.degrees(log['attitude_setpoint']['roll_body']),'r:',linewidth=1)
        plt.legend(['Ail*30', 'Rud*30', 'RC phi*30', 'RC psi*30', 'phi', 'phi_sp'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('Lat [deg]')
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)

        plt.subplot(9,1,(8,9))
        # Yaw, Yaw_setpoint, rudder
        scaler = 50
        plt.plot((log['actuator_controls']['timestamp'] - min_time),        log['actuator_controls']['control[2]']*scaler,linewidth=1)
        plt.plot((log['manual_control_setpoint']['timestamp'] - min_time),  log['manual_control_setpoint']['r']*scaler,linewidth=1)
        plt.plot((log['attitude']['timestamp'] - min_time),                 np.degrees(log['attitude']['yaw_body']),linewidth=1)
        plt.plot((log['local_position']['timestamp'] - min_time),           np.degrees(log['local_position']['courseangle']),linewidth=1)
        plt.plot((log['attitude_setpoint']['timestamp'] - min_time),        np.degrees(log['attitude_setpoint']['yaw_body']),'r:',linewidth=1)
        plt.plot((log['angular_velocity']['timestamp'] - min_time),         np.degrees(log['angular_velocity']['xyz[2]']),linewidth=1)
        plt.legend(['Rud*10', 'RC psi*10','course', 'psi', 'psi_sp','r'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]'); plt.ylabel('Dir [deg]')
        plt.ylim([-200, 200])
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
        
        if('save' in self.options):
            name_for_saving = "imgs/Ulg_{:s}_T_{:}_{:}_lat_ctrl_zoom.png".format(self.options['name'], int(self.options['range'][0]), int(self.options['range'][1]))
            fig.savefig(name_for_saving, dpi=300)
        
    def show_powers(self, time_info, log):
        plt.figure(self.figure_no)
        self.figure_no = self.figure_no + 1

        min_time = time_info.StartTime
        plt.title("Power System Analysis")
        plt.plot((log['battery_status']['timestamp'] - min_time),          log['battery_status']['voltage_v'],linewidth=1)
        plt.plot((log['battery_status']['timestamp'] - min_time),          log['battery_status']['voltage_filtered_v'],linewidth=1)
        plt.plot((log['battery_status']['timestamp'] - min_time),          log['battery_status']['current_a'],linewidth=1)
        plt.plot((log['battery_status']['timestamp'] - min_time),          log['battery_status']['current_filtered_a'],linewidth=1)
        plt.plot((log['system_power']['timestamp'] - min_time),            log['system_power']['voltage5v_v'],linewidth=1)
        plt.legend(['V.Batt [V]', 'V.Batt.filt [V]', 'Current [A]', 'Current.filt [A]', 'Sys5V [V]'],loc='upper right')
        plt.grid(); plt.xlabel('Time [sec]')
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
    def show_pwms(self, time_info, log):
        plt.figure(self.figure_no)
        self.figure_no = self.figure_no + 1
        plt.title("RC Input Analysis")
        min_time = time_info.StartTime
        plt.plot((log['input_rc']['timestamp'] - min_time),  log['input_rc']['values[0]'],linewidth=1)
        plt.plot((log['input_rc']['timestamp'] - min_time),  log['input_rc']['values[1]'],linewidth=1)
        plt.plot((log['input_rc']['timestamp'] - min_time),  log['input_rc']['values[2]'],linewidth=1)
        plt.plot((log['input_rc']['timestamp'] - min_time),  log['input_rc']['values[3]'],linewidth=1)
        plt.plot((log['input_rc']['timestamp'] - min_time),  log['input_rc']['values[4]'],linewidth=1)
        plt.plot((log['input_rc']['timestamp'] - min_time),  log['input_rc']['values[5]'],linewidth=1)
        plt.plot((log['input_rc']['timestamp'] - min_time),  log['input_rc']['values[6]'],linewidth=1)
        plt.plot((log['input_rc']['timestamp'] - min_time),  log['input_rc']['values[7]'],linewidth=1)
        plt.legend(['Ch1-Thr', 'Ch2-Ail', 'Ch3-Elv', 'Ch4-Rud', 'Ch5-Mod', 'Ch6-Kil', 'Ch7', 'Ch8'],loc='upper right')
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
        plt.grid()
        plt.tight_layout()
    def show_actuator_output(self, time_info, log):
        plt.figure(self.figure_no)
        self.figure_no = self.figure_no + 1
        
        plt.title("Actuator Output Analysis")
        min_time = time_info.StartTime
        plt.plot((log['actuator_controls']['timestamp'] - min_time),  log['actuator_controls']['control[0]'],linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),  log['actuator_controls']['control[1]'],linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),  log['actuator_controls']['control[2]'],linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),  log['actuator_controls']['control[3]'],linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),  log['actuator_controls']['control[4]'],linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),  log['actuator_controls']['control[5]'],linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),  log['actuator_controls']['control[6]'],linewidth=1)
        plt.plot((log['actuator_controls']['timestamp'] - min_time),  log['actuator_controls']['control[7]'],linewidth=1)
        plt.legend(['Ch1-Ail', 'Ch2-Elv', 'Ch3-Rud', 'Ch4-Thr', 'Ch5', 'Ch6', 'Ch7', 'Ch8'],loc='upper right')
        if(time_info.MinMax != None): plt.xlim(time_info.MinMax)
        plt.grid()
        plt.tight_layout()
    def show_anime(self, time_info, log):
        NowTime = copy.deepcopy(time_info.StartTime)
        dt = 0.1
        loop = dict()
        loop['attitude'] = 1
        loop['local_position'] = 1
        while(True):
            # Time Manager
            NowTime = NowTime + dt
            if(time_info.EndTime <= NowTime):
                break
            # Search Index
            while(True):
                end_cnt = 0
                for key in log.keys():
                    if (log[key]['timestamp'][loop[key]] < NowTime):
                        loop[key] = loop[key] + 1
                    else:
                        end_cnt = end_cnt + 1
                # print('end : ',end_cnt)
                # print('NowTime {} / at {} time {} / pos {} time {}'.format(NowTime, loop['attitude'],log['attitude']['timestamp'][loop[key]],loop['local_position'],log['local_position']['timestamp'][loop[key]]))
                if(end_cnt >= len(log)):
                    break
            
            # print(loop)            
            
            # Show Figure
            model.set_attitude(log['attitude']['roll_body'][loop['attitude']],          log['attitude']['pitch_body'][loop['attitude']],    log['attitude']['yaw_body'][loop['attitude']])
            model.set_position(-log['local_position']['x'][loop['local_position']],    -log['local_position']['y'][loop['local_position']],-log['local_position']['z'][loop['local_position']])
            model.show_fig()
            model.focus_on_it()
            # print('Time {:}'.format(log['attitude']['timestamp'][i]*1e-6))
            model.set_title('Time {:.6f} sec'.format(NowTime))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse PX4 Ulog", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t','--target', required=False, help='Give filename w/o extension')
    parser.add_argument('-o','--option', required=True,  help=textwrap.dedent('''\
        Plot Options :
            traj\t= Show local trajectories
            traj_t\t= Show local trajectories on timeseries
            moving\t= Show local traj and anime
            atti\t= Show attitude
            rate\t= Show angular velocity
            attis\t= Show attitude and rates
            anime\t= Show animation
            ctrl\t= Show control status ... '''))
    parser.add_argument('-r','--range', required=False, type=float, nargs='+', help='Time range you interest : <STARTSEC> <ENDSEC>')
    parser.add_argument('-s','--save',  required=False, type=int)
    args = parser.parse_args()

    

    # exist?
    table, time_info = get_all_of_data(args.target, args.range)
    options = dict()
    if(args.target != None):
        options['name'] = args.target
        print('[INFO] Name : {}'.format(options['name']))
    if(args.save != None):
        options['save']=True
        print('[INFO] Save Figures')
    if(args.range != None):
        options['range']=[np.float64(args.range[0]), np.float64(args.range[1])]
    else:
        options['range']=copy.deepcopy(time_info.MinMax)
    print('[INFO] Range : {} ~ {}'.format(options['range'][0], options['range'][1]))
    log = dict()
    log['attitude']                 = table['attitude']
    log['local_position']           = table['local_position']
    
        
    figure_maker = shows(options)
    
    if(args.option == 'traj'):
        log['local_position_setpoint']  = table['local_position_setpoint']
        figure_maker.show_local_traj(time_info, log)
        plt.show()
    
    elif(args.option == 'traj_t'):
        log['local_position_setpoint']  = table['local_position_setpoint']
        figure_maker.show_local_traj_timeseries(time_info, log)
        plt.show()
        
        
    elif(args.option == 'atti'):
        log['attitude_setpoint']    = table['attitude_setpoint']
        figure_maker.show_atti(time_info, log)
        plt.show()
        
    elif(args.option == 'rate'):
        log['rates_setpoint']       = table['rates_setpoint']
        log['angular_velocity']     = table['angular_velocity']
        figure_maker.show_rates(time_info, log)
        plt.show()
        
    elif(args.option == 'attis'):
        log['rates_setpoint']       = table['rates_setpoint']
        log['angular_velocity']     = table['angular_velocity']
        log['attitude_setpoint']    = table['attitude_setpoint']
        figure_maker.show_attis(time_info, log)
        plt.show()

    elif(args.option == 'anime'):
        model = quadrotor_visualizer()
        figure_maker.show_anime(time_info, log)
    
    elif(args.option == 'moving'):
        log['local_position_setpoint']  = table['local_position_setpoint']
        figure_maker.show_local_traj(log)
        log.__delitem__('local_position_setpoint')
        model = quadrotor_visualizer()
        figure_maker.show_anime(time_info, log)
    
    elif(args.option == 'ctrl'):
        log['rates_setpoint']       = table['rates_setpoint']
        log['angular_velocity']     = table['angular_velocity']
        log['attitude_setpoint']    = table['attitude_setpoint']
        figure_maker.show_attis(time_info, log)
        log['vehicle_local_position_setpoint']  = table['vehicle_local_position_setpoint']
        figure_maker.show_local_traj(time_info, log)
        figure_maker.show_local_traj_timeseries(time_info, log)
        plt.show()

    elif(args.option == 'all'):
        log['attitude_setpoint']    = table['attitude_setpoint']
        figure_maker.show_atti(time_info, log)

        log['vehicle_local_position']           = table['vehicle_local_position']
        if('vehicle_local_position_setpoint' in table.keys()):
            log['vehicle_local_position_setpoint']  = table['vehicle_local_position_setpoint']
        figure_maker.show_local_traj(time_info, log)
        log['rates_setpoint']       = table['rates_setpoint']
        log['angular_velocity']     = table['angular_velocity']
        figure_maker.show_rates(time_info, log)
        log['commander_state']                      = table['commander_state']
        log['manual_control_setpoint']              = table['manual_control_setpoint']
        log['vehicle_status']                       = table['vehicle_status']
        log['actuator_controls']                    = table['actuator_controls']
        log['airspeed']                             = table['airspeed']
        log['wind']                                 = table['wind']
        log['vehicle_global_position']              = table['vehicle_global_position']
        if('tecs_status' in table.keys()):
            log['tecs_status']                          = table['tecs_status']
        if('position_setpoint_triplet' in table.keys()):
            log['position_setpoint_triplet']            = table['position_setpoint_triplet']
            figure_maker.show_global_traj(time_info, log)
        figure_maker.show_lon_ctrl(time_info, log)
        figure_maker.show_lat_ctrl(time_info, log)
        figure_maker.show_lat_ctrl_zoom(time_info, log)
        
        log['battery_status'] = table['battery_status']
        log['system_power'] = table['system_power']
        figure_maker.show_powers(time_info, log)

        log['input_rc']             = table['input_rc']
        figure_maker.show_pwms(time_info, log)

        figure_maker.show_actuator_output(time_info, log)
        plt.show()


