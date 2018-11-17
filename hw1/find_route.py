#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 18:20:41 2018

@author: yangzhuronghuang
"""
import networkx
import matplotlib.pyplot as plt

BJ = 'Beijing'
SZ = 'Shenzhen'
GZ = 'Guangzhou'
WH = 'Wuhan'
HLG = 'Heilongjiang'
NY = 'New York City'
CM = 'Chiangmai'
SG = 'Singapore'
air_route = {
    BJ : {SZ, GZ, WH, HLG, NY}, 
    GZ : {WH, BJ, CM, SG},
    SZ : {BJ, SG},
    WH : {BJ, GZ},
    HLG : {BJ},
    CM : {GZ},
    NY : {BJ}
}
air_route = networkx.Graph(air_route)

networkx.draw(air_route, with_labels=True)

def search_destination(graph, start, destination):
    paths = [[start]]
    seen = set()
    chosen_paths=[]
    while paths:
        path=paths.pop(0)
        frontier = path[-1]
        if frontier in seen: continue
    #get new lines
        for city in graph[frontier]:
            new_path = path+[city]
            paths.append(new_path)
            if city == destination: return new_path
            
        seen.add(frontier)
    return chosen_paths

def draw_route(cities): return ' ✈️ -> '.join(cities)

