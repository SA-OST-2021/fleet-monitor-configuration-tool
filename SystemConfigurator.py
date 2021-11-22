# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 11:14:34 2021

@author: flori
"""

import json

if __name__ == "__main__":
    
    system = {
        'ssid':     'fleet-network',
        'password': 'admin',
        'mode':     'auto'        # auto, lan, wlan
    }
    
    with open('system.json', 'w') as f:
        json.dump(system, f)