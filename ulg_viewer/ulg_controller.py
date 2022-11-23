import os
from pyulog.core import ULog
from misc import FILENAME
import argparse, textwrap
import pandas as pd
import numpy as np

def _get_nav_state_string(nav_state):
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

def get_all_of_data(target_name):
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
            if(target_name not in file_name):
                continue
            target_file = path_dir + '/' + file_name
            key = 'vehicle_status'
            if(file_name.find(key+'_0') != -1):
                # print('Find key : {:30} -> {:50}'.format(key, file_name), end=' ')
                with open(target_file, 'r') as loaded_file:
                    loaded_data = pd.read_csv(filepath_or_buffer=target_file,
                                                sep=",",
                                                # keep_default_na=False,
                                                )
                    tmp = np.transpose(loaded_data.values)
                    table[key] = {}
                    for i in range(len(loaded_data.columns)):
                        str_idx = str(loaded_data.columns[i])
                        table[key][str_idx] = tmp[i][1:]

                    table[key]['timestamp'] = table[key]['timestamp'] * 1e-6

    return table

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV maker from ulg", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t','--target',  required=False, default=FILENAME, help='Target File Name')
    parser.add_argument('-c','--command', required=True,  help=textwrap.dedent('''\
        Control Options :
            create : create csv files frome ulg
            remove : remove all of them
            '''))
    args = parser.parse_args()
    filename    = args.target
    ctrl_option = args.command
    
    if (ctrl_option == 'create'):
        ulog_file_name  = './ulgs/{}.ulg'.format(filename)
        messages        = None
        output          = 'data'
        delimiter       = ','
        disable_str_exceptions=False

        msg_filter = messages.split(',') if messages else None

        ulog = ULog(ulog_file_name, msg_filter, disable_str_exceptions)
        data = ulog.data_list

        output_file_prefix = ulog_file_name
        # strip '.ulg'
        if output_file_prefix.lower().endswith('.ulg'):
            output_file_prefix = output_file_prefix[:-4]

        # write to different output path?
        if output:
            base_name = os.path.basename(output_file_prefix)
            output_file_prefix = os.path.join(output, base_name)


        for d in data:
            # print(d.name)
            fmt = '{0}_{1}_{2}.csv'
            output_file_name = fmt.format(output_file_prefix, d.name, d.multi_id)

            fmt = 'Writing : {0} ({1} data points)'
            print(fmt.format(output_file_name, len(d.data['timestamp'])))

            with open(output_file_name, 'w') as csvfile:

                # use same field order as in the log, except for the timestamp
                data_keys = [f.field_name for f in d.field_data]
                data_keys.remove('timestamp')
                data_keys.insert(0, 'timestamp')  # we want timestamp at first position

                # for key in data_keys:
                #     print(key,end=' ')
                # print('')

                # we don't use np.savetxt, because we have multiple arrays with
                # potentially different data types. However the following is quite
                # slow...

                # write the header
                csvfile.write(delimiter.join(data_keys) + '\n')

                # write the data
                last_elem = len(data_keys)-1
                for i in range(len(d.data['timestamp'])):
                    for k in range(len(data_keys)):
                        csvfile.write(str(d.data[data_keys[k]][i]))
                        if k != last_elem:
                            csvfile.write(delimiter)
                    csvfile.write('\n')
                    
        print("Create csv files from {}.ulg".format(filename))
        
        log = get_all_of_data(filename)
        min_time = min(log['vehicle_status']['timestamp'])
        max_time = max(log['vehicle_status']['timestamp'])
        nav_states = log['vehicle_status']['nav_state']
        
        fid = open("Log_id_{}.txt".format(filename),'w')
        print("python plot_fw.py -t {} -o all -s 1\n".format(filename))
        fid.write("python plot_fw.py -t {} -o all -s 1\n".format(filename))
        prev_time = log['vehicle_status']['timestamp'][0] - min_time
        for idx in range(len(nav_states)-1):
            if((nav_states[idx+1] != nav_states[idx]) or (idx == len(nav_states)-1)):
                text_string = _get_nav_state_string(nav_states[idx])
                print("Mode Changed {:10} @ {:10.2f}".format(text_string, log['vehicle_status']['timestamp'][idx+1] - min_time))
                start_time  = max([0, int(prev_time)-1])
                end_time    = min([int(log['vehicle_status']['timestamp'][idx+1] - min_time)+1, int(max_time)])
                text_for_writing = "python plot_fw.py -t {} -o all -r {} {} -s 1 # {}".format(filename, start_time, end_time, text_string)
                fid.write(text_for_writing + "\n")
                print(text_for_writing)
                prev_time   = log['vehicle_status']['timestamp'][idx+1] - min_time
        fid.close()

                
    elif(ctrl_option == 'remove'):
        path_dir = './data'
        file_list = os.listdir(path_dir)

        if len(file_list) == 0:
            print('Forder is empty')
            exit()
        else:
            if (filename==FILENAME):
                for file_name in file_list:
                    target_file = path_dir + '/' + file_name
                    print("Remove : {}".format(file_name))
                    os.remove(target_file)


            for file_name in file_list:
                target_file = path_dir + '/' + file_name
                if(file_name.find(filename) != -1):
                    print("Remove : {}".format(file_name))
                    os.remove(target_file)
                    
        print("remove csv files for {}.ulg".format(filename))
        
    elif(ctrl_option == 'info'):
        ulog_file_name  = './ulgs/{}.ulg'.format(filename)
        verbose         = True
        output          = 'data'
        disable_str_exceptions = False
        ulog = ULog(ulog_file_name, None, disable_str_exceptions)

        output_file_prefix = ulog_file_name
        # strip '.ulg'
        if output_file_prefix.lower().endswith('.ulg'):
            output_file_prefix = output_file_prefix[:-4]
            
        # write to different output path?
        if output:
            base_name = os.path.basename(output_file_prefix)
            output_file_prefix = os.path.join(output, base_name)
        output_file_name = output_file_prefix + '_info.txt'

        with open(output_file_name, 'w') as infofile:
            
            def print_save(arg):
                infofile.write(arg + '\n')
                print(arg)

            """Show general information from an ULog"""
            m1, s1 = divmod(int(ulog.start_timestamp/1e6), 60)
            h1, m1 = divmod(m1, 60)
            m2, s2 = divmod(int((ulog.last_timestamp - ulog.start_timestamp)/1e6), 60)
            h2, m2 = divmod(m2, 60)
            print_save("Logging start time: {:d}:{:02d}:{:02d}, duration: {:d}:{:02d}:{:02d}".format(
                h1, m1, s1, h2, m2, s2))

            dropout_durations = [dropout.duration for dropout in ulog.dropouts]
            if len(dropout_durations) == 0:
                print_save("No Dropouts")
            else:
                print_save("Dropouts: count: {:}, total duration: {:.1f} s, max: {:} ms, mean: {:} ms"
                        .format(len(dropout_durations), sum(dropout_durations)/1000.,
                                max(dropout_durations),
                                int(sum(dropout_durations)/len(dropout_durations))))

            version = ulog.get_version_info_str()
            if not version is None:
                print_save('SW Version: {}'.format(version))

            print_save("Info Messages:")
            for k in sorted(ulog.msg_info_dict):
                if not k.startswith('perf_') or verbose:
                    print_save(" {0}: {1}".format(k, ulog.msg_info_dict[k]))


            # if len(ulog.msg_info_multiple_dict) > 0:
            #     if verbose:
            #         print_save("Info Multiple Messages:")
            #         for k in sorted(ulog.msg_info_multiple_dict):
            #             print_save(" {0}: {1}".format(k, ulog.msg_info_multiple_dict[k]))
            #     else:
            #         print_save("Info Multiple Messages: {}".format(
            #             ", ".join(["[{}: {}]".format(k, len(ulog.msg_info_multiple_dict[k])) for k in
            #                         sorted(ulog.msg_info_multiple_dict)])))

            print_save("")
            print_save("{:<41} {:7}, {:10}".format("Name (multi id, message size in bytes)",
                                                "number of data points", "total bytes"))

            data_list_sorted = sorted(ulog.data_list, key=lambda d: d.name + str(d.multi_id))
            for d in data_list_sorted:
                message_size = sum([ULog.get_field_size(f.type_str) for f in d.field_data])
                num_data_points = len(d.data['timestamp'])
                name_id = "{:} ({:}, {:})".format(d.name, d.multi_id, message_size)
                print_save(" {:<40} {:7d} {:10d}".format(name_id, num_data_points,
                                                    message_size * num_data_points))
        print("show info for {}.ulg".format(filename))
        
    else:
        print("Wrong Command : {}".format(ctrl_option))
                    
