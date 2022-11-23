# FILENAME = '05_05_04'
FILENAME = '220210_01_25_10'


LIST_FOR_LOADING_FW = [
    'vehicle_status',
    'battery_status',
    'system_power',
    'actuator_controls',        # RPYT
    'attitude',                 # RPY
    'attitude_setpoint',        # RPY setpoint
    'angular_velocity',         # wB
    'rates_setpoint',           # wB setpoint
    'local_position',           # pNED, vNED
    # 'local_position_setpoint',  # pNED, vNED setpoint
    'commander_state',
    
    'ekf_gps_drift',
    'airspeed_validated',
    'actuator_controls',
    'vehicle_local_position_setpoint',
    'vehicle_local_position',
    'tecs_status',

    'manual_control_setpoint',
    'input_rc',
    
    'airspeed',
    'wind',
    'tecs_status',

    'vehicle_global_position',
    'position_setpoint_triplet', # Mission Status
    
    'actuator_armed',
    'global_position',          # global position
]