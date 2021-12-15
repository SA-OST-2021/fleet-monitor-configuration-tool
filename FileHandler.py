###############################################################################
# file    Filehandler.py
###############################################################################
# brief   Module for importing and exporting JSON configuration files
###############################################################################
# author  Florian Baumgartner
# version 1.0
# date    2021-12-15
###############################################################################
# MIT License
#
# Copyright (c) 2021 Florian Baumgartner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

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
        'FEE9': "Fuel Consumption: LFC",
        'FEFC': "Dash Display 1: DD1",
        'F004': "Electronic Engine Controller #1: EEC1",
        'FEE5': "Engine Hours, Revolutions: HOURS",
        'FEEC': "Vehicle Identification: VI",
        'FDD1': "MS-standard Interface Identity / Capabilities: FMS",
        'FEC1': "High Resolution Vehicle Distance: VDHR",
        'FE6C': "Tachograph : TCO1",
        'FEEE': "Engine Temperature 1: ET1",
        'FEF5': "Ambient Conditions: AMB",
        'FE6B': "Driver's Identification: DI",
        'FEF2': "Fuel Economy: LFE",
        'FEAE': "Air Supply Pressure : AIR1",
        'FD09': "High Resolution Fuel Consumption (Liquid): HRLFC",
        'FE56': "Aftertreatment 1 Diesel Exhaust Fluid Tank 1 Information: AT1T1I",
        'FD7D': "FMS Tell Tale Status: FMS1",
        'F001': "Electronic Brake Controller 1: EBC1",
        'FDC2': "Electronic Engine Controller 14: EEC14",
        'FEAF': "Fuel Consumption (Gaseous): GFC",
        'F000': "Electronic Retarder Controller 1: ERC1",
        'FEF1': "Cruise Control/Vehicle Speed 1: CCVS1",
        'F003': "Electronic Engine Controller #2: EEC2",
        'FEEA': "Vehicle Weight: VW",
        'FEC0': "Service Information: SERV",
        'FDA4': "PTO Drive Engagement: PTODE",
        'FE70': "Combination Vehicle Weight: CVW",
        # 'FEF1': "Cruise Control/Vehicle Speed: CCVS",
        # 'F003': "Electronic Engine Controller #2 : EEC2",
        'FE4E': "Door Control 1: DC1",
        'FDA5': "Door Control 2: DC2",
        'FEE6': "Time / Date : TD",
        'FED5': "Alternator Speed : AS",
        'F005': "Electronic Transmission Controller 2 : ETC2",
        'FE58': "Air Suspension Control 4 : ASC4",
        'FCB7': "Vehicle Electrical Power #4 : VEP4",
        'F009': "Vehicle Dynamic Stability Control 2 : VDC2",
    }
    
    
    data = {}
    data['frames'] = []
    for i in initial:
        data['frames'].append({'pgn': i,
                               'name': initial[i],
                               'active': True,
                               'filter': 'nofilter'})
    
    
    with open('config.json', 'w') as f:
        json.dump(data, f)