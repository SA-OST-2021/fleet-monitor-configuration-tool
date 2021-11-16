# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 11:14:34 2021

@author: flori
"""

import json


class FileHandler():
    def __init__(self):
        pass


if __name__ == "__main__":
    data = {}
    data['people'] = []
    data['people'].append({
        'name': 'Scott',
        'website': 'stackabuse.com',
        'from': 'Nebraska'
    })
    data['people'].append({
        'name': 'Larry',
        'website': 'google.com',
        'from': 'Michigan'
    })
    data['people'].append({
        'name': 'Tim',
        'website': 'apple.com',
        'from': 'Alabama'
    })
    
    with open('demo.json', 'w') as outfile:
        json.dump(data, outfile)