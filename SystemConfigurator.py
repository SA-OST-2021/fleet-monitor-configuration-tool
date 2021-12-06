# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 11:14:34 2021

@author: flori
"""

import json

if __name__ == "__main__":
    
    system = {
        'ssid':             'fleet-monitor',
        'password':         'password',
        'connection':       'auto',              # auto, lan, wlan
        'config':           'local',             # remote
        'host_ip':          '10.3.141.1',
        'host_port':        8080,
        'overwrite_file':   False,  
        'bootloader':       True,
    }
    
    with open('system.json', 'w') as f:
        json.dump(system, f)