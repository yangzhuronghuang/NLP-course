#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17  2018

@author: yangzhuronghuang
"""
import networkx
import matplotlib.pyplot as plt
    

graph_long = {
    '1': '2 7',
    '2': '3', 
    '3': '4', 
    '4': '5', 
    '5': '6 10', 
    '7': '8',
    '6': '5',
    '8': '9',
    '9': '10', 
    '10': '5 11', 
    '11': '12',
    '12': '11',
}
for k in graph_long:
    graph_long[k] = set(graph_long[k].split())
    
def search(graph, mode):
    seen = set()
    need_visited = ['1']
    
    while need_visited:
        node = need_visited.pop(0)
        if node in seen:
            continue  
        print('    I am looking at {}'.format(node))
        seen.add(node)
        new_discovered = graph[node]
        if(mode == 'dfs'):
            need_visited = [t for t in new_discovered]+need_visited
        else:
            need_visited += new_discovered
            
def dfs(graph):
    return search(graph, 'dfs')            
def bfs(graph):
    return search(graph, 'bfs')


