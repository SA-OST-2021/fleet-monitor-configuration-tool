###############################################################################
# file    SystemConfigurator.py
###############################################################################
# brief   Script to easily generate a system configuration file
###############################################################################
# author  Florian Baumgartner
# version 1.0
# date    2021-12-15
###############################################################################
# MIT License
#
# Copyright (c) 2021 Institute for Networked Solutions OST
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