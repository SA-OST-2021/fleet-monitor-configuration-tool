# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 11:14:34 2021

@author: flori
"""

import json
# from pathlib import path


class FileHandler():
    def __init__(self):
        pass
    
    def loadFile(self, name):
        with open(name) as f:
            return json.load(f)

    def saveFile(self, name, data):
        with open(name, 'w') as f:
            json.dump(data, f)



if __name__ == "__main__":
    
    initial = {
        'FEE9': 'Fuel Consumption: LFC',
        'FEFC': 'Dash Display 1: DD1',
        'F004': 'Electronic Engine Controller #1: EEC1',
        'FEE5': 'Engine Hours, Revolutions: HOURS',
        'FEEC': 'Vehicle Identification: VI',
        'FDD1': 'FMS-standard Interface Identity / Capabilities: FMS',
        'FEC1': 'High Resolution Vehicle Distance: VDHR',
    }
    
    
    data = {}
    data['frames'] = []
    for i in initial:
        data['frames'].append({'pgn': i, 'name': initial[i], 'filter': 'never'})
    
    
    with open('demo.json', 'w') as f:
        json.dump(data, f)